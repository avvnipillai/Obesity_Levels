import os, joblib, traceback, warnings
from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# ─────────────────────────────────────────────────────────────
#  SAFE LOADER  — strips use_label_encoder from XGBoost models
#  that were saved with older xgboost versions
# ─────────────────────────────────────────────────────────────
def _patch_xgb(obj):
    """Remove stale use_label_encoder from XGBClassifier at any level."""
    try:
        # 1. Instance __dict__
        if hasattr(obj, '__dict__'):
            obj.__dict__.pop('use_label_encoder', None)
        # 2. Class __dict__ (where newer XGBoost puts it as a property)
        cls = type(obj)
        if 'use_label_encoder' in vars(cls):
            try:
                delattr(cls, 'use_label_encoder')
            except (AttributeError, TypeError):
                pass
        # 3. __init_params__ dict used internally by xgboost
        ip = getattr(obj, '__init_params__', None)
        if isinstance(ip, dict):
            ip.pop('use_label_encoder', None)
        # 4. xgboost get_xgb_params() cache
        if hasattr(obj, '_Booster') and obj._Booster is not None:
            pass  # Booster itself is fine; no patching needed
    except Exception:
        pass
    return obj

def safe_load(path):
    obj = joblib.load(path)
    _patch_xgb(obj)
    return obj

# ─────────────────────────────────────────────────────────────
#  LABEL NORMALIZATION
#  The UCI dataset uses inconsistent casing across columns
#  (e.g. "Sometimes", "Frequently", "Always" but "no"/"yes"
#  lowercase). The frontend always sends lowercase values.
#  This maps any incoming value to whatever exact casing the
#  trained LabelEncoder actually knows, case-insensitively,
#  so "sometimes" matches "Sometimes" automatically.
# ─────────────────────────────────────────────────────────────
def build_case_lookup(le_dict):
    """For each encoder, build a {lowercase_label: real_label} map."""
    lookup = {}
    for col, le in le_dict.items():
        lookup[col] = {str(c).lower(): str(c) for c in le.classes_}
    return lookup

def normalize_value(col, value, lookup):
    """Return the exact label the encoder expects, or the original
    value unchanged if no case-insensitive match is found (so the
    real 'unseen label' error still surfaces for genuinely bad input)."""
    if col not in lookup:
        return value
    key = str(value).strip().lower()
    return lookup[col].get(key, value)

# ─────────────────────────────────────────────────────────────
#  LOAD ARTEFACTS
# ─────────────────────────────────────────────────────────────
model = scaler = le_dict = tgt_enc = cat_cols = metadata = None
case_lookup = {}
_load_error = None

try:
    model    = safe_load('xgboost_model.pkl')
    scaler   = safe_load('scaler.pkl')
    le_dict  = safe_load('label_encoders.pkl')
    tgt_enc  = safe_load('target_encoder.pkl')
    cat_cols = safe_load('categorical_cols.pkl')
    metadata = safe_load('model_metadata.pkl')

    # Warm-up: catch any remaining attribute errors at startup
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        _dummy = np.zeros((1, len(metadata['feature_names'])))
        model.predict(_dummy)

    case_lookup = build_case_lookup(le_dict)

    print("✓ Models loaded and verified")

except FileNotFoundError as e:
    _load_error = f"Missing file: {e}"
    print(f"✗ {_load_error}")
except Exception as e:
    _load_error = str(e)
    print(f"✗ Load error: {e}")
    print(traceback.format_exc())

# ─────────────────────────────────────────────────────────────
#  CLASS METADATA
# ─────────────────────────────────────────────────────────────
OB_META = {
    0: dict(name="Insufficient Weight", risk="Underweight",    color="#38bdf8", emoji="⚠️"),
    1: dict(name="Normal Weight",        risk="Healthy",        color="#34d399", emoji="✅"),
    2: dict(name="Overweight Level I",   risk="Moderate Risk",  color="#fbbf24", emoji="🟡"),
    3: dict(name="Overweight Level II",  risk="Elevated Risk",  color="#f97316", emoji="🟠"),
    4: dict(name="Obesity Type I",       risk="High Risk",      color="#f87171", emoji="🔴"),
    5: dict(name="Obesity Type II",      risk="Very High Risk", color="#ef4444", emoji="🔴"),
    6: dict(name="Obesity Type III",     risk="Critical Risk",  color="#dc2626", emoji="🚨"),
}

# ─────────────────────────────────────────────────────────────
#  RECOMMENDATIONS
# ─────────────────────────────────────────────────────────────
def personalized_recs(d):
    recs   = []
    favc   = d.get('FAVC', 'no')
    fcvc   = float(d.get('FCVC', 2))
    ch2o   = float(d.get('CH2O', 2))
    faf    = float(d.get('FAF', 2))
    smoke  = d.get('SMOKE', 'no')
    calc   = d.get('CALC', 'no')
    scc    = d.get('SCC', 'no')
    caec   = d.get('CAEC', 'no')
    tue    = float(d.get('TUE', 2))
    mtrans = d.get('MTRANS', 'Automobile')
    ncp    = float(d.get('NCP', 3))

    if favc == 'yes':
        recs.append({"icon":"🍔","title":"Cut Back on High-Calorie Foods",
            "steps":["Swap one processed meal a day for something home-cooked.",
                     "Replace sugary drinks with water, herbal teas, or sparkling water.",
                     "Read nutrition labels and aim for under 400 kcal per snack.",
                     "Cook in batches so healthy food is always within reach."]})
    else:
        recs.append({"icon":"🥙","title":"Your Diet Choices Are Already a Win",
            "steps":["Keep avoiding ultra-processed and high-calorie packaged foods.",
                     "Continue cooking at home where you control your ingredients.",
                     "Introduce new whole foods each week to keep meals interesting."]})

    if fcvc < 2:
        recs.append({"icon":"🥦","title":"More Vegetables, More Energy",
            "steps":["Add a handful of leafy greens to every meal.",
                     "Try roasting vegetables — it transforms even boring ones.",
                     "Frozen vegetables are just as nutritious and more convenient.",
                     "Aim for at least 3 different colours on your plate each day."]})

    if ch2o < 2:
        recs.append({"icon":"💧","title":"Hydration Is Underrated",
            "steps":["Keep a 1-litre bottle at your desk and refill it twice daily.",
                     "Start every morning with a full glass of water before coffee.",
                     "Add lemon, cucumber, or mint if plain water feels boring.",
                     "Daily goal: 2.5 to 3 litres."]})

    if faf < 2:
        recs.append({"icon":"🏃","title":"Move More and Start Small",
            "steps":["A 20-minute walk after dinner is a great place to start.",
                     "Find one activity you enjoy: dancing, cycling, or swimming.",
                     "Build gradually to 150 minutes of moderate activity per week.",
                     "Take the stairs, park further away, treat every step as progress."]})
    else:
        recs.append({"icon":"💪","title":"Your Activity Level Is a Real Strength",
            "steps":["Keep up your exercise habit — it predicts long-term health strongly.",
                     "Consider adding strength training 2 days a week.",
                     "Recover well: prioritise sleep and protein after workouts."]})

    if smoke == 'yes':
        recs.append({"icon":"🚭","title":"Quitting Smoking Is the Single Best Thing You Can Do",
            "steps":["Speak to your doctor about nicotine replacement therapy.",
                     "Try a certified quit programme such as the NHS Stop Smoking service.",
                     "Set a quit date and tell someone you trust to keep you accountable.",
                     "Replace the habit with something physical: a walk or deep breathing."]})

    if calc in ['frequently', 'always']:
        recs.append({"icon":"🍷","title":"Moderate Your Alcohol Intake",
            "steps":["Limit to 1 drink for women and 2 for men per day at most.",
                     "Alcohol adds significant empty calories, often more than a full meal.",
                     "Designate alcohol-free days each week to reset your habits.",
                     "Swap cocktails for sparkling water with a splash of juice."]})

    if scc == 'no':
        recs.append({"icon":"📊","title":"Start Tracking What You Eat",
            "steps":["Try MyFitnessPal or Cronometer for just one week.",
                     "Most people are surprised by how many calories light meals contain.",
                     "Track until you develop a clear sense of portions, then stop.",
                     "Focus on protein and fibre, not just total calories."]})

    if caec in ['frequently', 'always']:
        recs.append({"icon":"🍎","title":"Bring Mindfulness to Snacking",
            "steps":["Before reaching for a snack, drink water and wait 10 minutes.",
                     "Prepare healthy portions in advance: nuts, fruit, or yoghurt.",
                     "Avoid eating in front of screens — it leads to far more consumption.",
                     "Keep unhealthy snacks out of the house entirely."]})

    if tue > 4:
        recs.append({"icon":"📱","title":"Break the Screen-Sitting Cycle",
            "steps":["Set a timer to stand and stretch for 5 minutes every hour.",
                     "Try 25 minutes of work followed by 5 minutes of movement.",
                     "Walk while taking calls. Stretch while watching TV.",
                     "Limit recreational screen time to under 2 hours after work."]})

    if mtrans in ['Automobile', 'Motorbike']:
        recs.append({"icon":"🚴","title":"Add Movement to Your Commute",
            "steps":["Try cycling or walking for trips under 2 km.",
                     "Get off public transport one stop early and walk the rest.",
                     "Parking further away adds meaningful daily steps.",
                     "Active commuting is exercise you never have to separately schedule."]})

    if ncp > 4:
        recs.append({"icon":"🍽️","title":"Simplify Your Meal Structure",
            "steps":["Aim for 3 balanced meals with at most 1 or 2 planned snacks.",
                     "Large meals spread across the day are easier to manage.",
                     "Consistent meal timing helps regulate hunger hormones.",
                     "Each main meal should include protein, fibre, and healthy fat."]})

    return recs[:8]


# ─────────────────────────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def results_page():
    return render_template('results.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')


# ─────────────────────────────────────────────────────────────
#  PREDICT
# ─────────────────────────────────────────────────────────────
@app.route('/api/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({
            'success': False,
            'error': _load_error or 'Models not loaded. Check .pkl files.'
        }), 500

    try:
        d = request.get_json()
        if not d:
            return jsonify({'success': False, 'error': 'No JSON received.'}), 400

        # Unit conversions
        h = float(d.get('Height', 0))
        w = float(d.get('Weight', 0))
        if d.get('height_unit') == 'ft':
            h = round(h * 0.3048, 3)
        if d.get('weight_unit') == 'lbs':
            w = round(w * 0.453592, 2)

        if h <= 0 or w <= 0:
            return jsonify({'success': False,
                            'error': 'Height and weight must be greater than zero.'}), 400

        inp = {
            'Gender':                         d.get('Gender', 'Male'),
            'Age':                            float(d.get('Age', 25)),
            'Height':                         round(h, 3),
            'Weight':                         round(w, 2),
            'family_history_with_overweight': d.get('family_history_with_overweight', 'no'),
            'FAVC':                           d.get('FAVC', 'no'),
            'FCVC':                           float(d.get('FCVC', 2)),
            'NCP':                            float(d.get('NCP', 3)),
            'CAEC':                           d.get('CAEC', 'Sometimes'),
            'CH2O':                           float(d.get('CH2O', 2)),
            'CALC':                           d.get('CALC', 'no'),
            'SMOKE':                          d.get('SMOKE', 'no'),
            'SCC':                            d.get('SCC', 'no'),
            'FAF':                            float(d.get('FAF', 1)),
            'TUE':                            float(d.get('TUE', 1)),
            'MTRANS':                         d.get('MTRANS', 'Public_Transportation'),
        }

        # Normalize categorical casing to match what each LabelEncoder
        # was actually trained on (case-insensitive lookup).
        for col in cat_cols:
            if col in inp:
                inp[col] = normalize_value(col, inp[col], case_lookup)

        df_in = pd.DataFrame([inp])
        df_in = df_in[metadata['feature_names']]

        for col in cat_cols:
            if col in df_in.columns:
                try:
                    df_in[col] = le_dict[col].transform(df_in[col].astype(str))
                except ValueError as ve:
                    known = list(le_dict[col].classes_)
                    return jsonify({
                        'success': False,
                        'error': (f"Invalid value for '{col}': '{inp[col]}'. "
                                  f"Expected one of: {known}")
                    }), 400

        X = scaler.transform(df_in)

        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            pred_idx  = int(model.predict(X)[0])
            pred_prob = model.predict_proba(X)[0]

        bmi  = round(w / (h ** 2), 1)
        meta = OB_META.get(pred_idx, OB_META[1])
        recs = personalized_recs(d)

        prob_dict = {
            cls: round(float(pred_prob[i]) * 100, 1)
            for i, cls in enumerate(tgt_enc.classes_)
        }

        return jsonify({
            'success':         True,
            'prediction':      {
                'index': pred_idx,
                'name':  meta['name'],
                'risk':  meta['risk'],
                'color': meta['color'],
                'emoji': meta['emoji'],
            },
            'bmi':             bmi,
            'height_m':        round(h, 3),
            'weight_kg':       round(w, 2),
            'probabilities':   prob_dict,
            'recommendations': recs,
            'user_inputs':     d,
        })

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 400


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Server error'}), 500


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0',
            port=int(os.environ.get('PORT', 5000)))
