import os, joblib, traceback, warnings
from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# ── Load models ───────────────────────────────────────────────────────────────
model = scaler = le_dict = tgt_enc = cat_cols = metadata = None
try:
    model    = joblib.load('xgboost_model.pkl')
    scaler   = joblib.load('scaler.pkl')
    le_dict  = joblib.load('label_encoders.pkl')
    tgt_enc  = joblib.load('target_encoder.pkl')
    cat_cols = joblib.load('categorical_cols.pkl')
    metadata = joblib.load('model_metadata.pkl')

    # ── XGBoost version-compatibility patch ───────────────────────────────────
    # Models trained with xgboost < 1.6 store use_label_encoder in __dict__.
    # xgboost >= 1.6 removed that attribute and raises AttributeError on predict().
    # Deleting it from the instance dict is the correct fix (model weights intact).
    if hasattr(model, 'use_label_encoder'):
        try:
            del model.__dict__['use_label_encoder']
        except KeyError:
            pass

    print("Models loaded OK")
except FileNotFoundError as e:
    print(f"Missing model file: {e}")
except Exception as e:
    print(f"Model load error: {e}")
    print(traceback.format_exc())

# ── Class metadata ────────────────────────────────────────────────────────────
OB_META = {
    0: dict(name="Insufficient Weight", risk="Underweight",    color="#38bdf8", emoji="⚠️"),
    1: dict(name="Normal Weight",        risk="Healthy",        color="#34d399", emoji="✅"),
    2: dict(name="Overweight Level I",   risk="Moderate Risk",  color="#fbbf24", emoji="🟡"),
    3: dict(name="Overweight Level II",  risk="Elevated Risk",  color="#f97316", emoji="🟠"),
    4: dict(name="Obesity Type I",       risk="High Risk",      color="#f87171", emoji="🔴"),
    5: dict(name="Obesity Type II",      risk="Very High Risk", color="#ef4444", emoji="🔴"),
    6: dict(name="Obesity Type III",     risk="Critical Risk",  color="#dc2626", emoji="🚨"),
}

# ── Personalised recommendations ──────────────────────────────────────────────
def personalized_recs(d):
    recs  = []
    favc  = d.get('FAVC', 'no')
    fcvc  = float(d.get('FCVC', 2))
    ch2o  = float(d.get('CH2O', 2))
    faf   = float(d.get('FAF', 2))
    smoke = d.get('SMOKE', 'no')
    calc  = d.get('CALC', 'no')
    scc   = d.get('SCC', 'no')
    caec  = d.get('CAEC', 'no')
    tue   = float(d.get('TUE', 2))
    mtrans= d.get('MTRANS', 'Automobile')
    ncp   = float(d.get('NCP', 3))

    if favc == 'yes':
        recs.append({"icon":"🍔","title":"Cut Back on High-Calorie Foods",
            "steps":["Start by swapping one processed meal a day for something home-cooked.",
                     "Replace sugary drinks with water, herbal teas, or sparkling water.",
                     "Read nutrition labels and aim for under 400 kcal per snack.",
                     "Cook in batches so healthy food is always within reach."]})
    else:
        recs.append({"icon":"🥙","title":"Your Diet Choices Are Already a Win",
            "steps":["Keep avoiding ultra-processed and high-calorie packaged foods.",
                     "Continue cooking at home where you control your ingredients.",
                     "Introduce new whole foods each week to keep meals exciting."]})

    if fcvc < 2:
        recs.append({"icon":"🥦","title":"More Vegetables, More Energy",
            "steps":["Add one handful of leafy greens to every meal.",
                     "Try roasting vegetables — it transforms even the boring ones.",
                     "Frozen vegetables are just as nutritious and far more convenient.",
                     "Aim for at least 3 different colours on your plate each day."]})

    if ch2o < 2:
        recs.append({"icon":"💧","title":"Hydration Is Underrated",
            "steps":["Keep a 1-litre water bottle at your desk and refill it twice daily.",
                     "Start every morning with a full glass of water before coffee or tea.",
                     "Add lemon, cucumber, or mint if plain water feels boring.",
                     "Your daily goal: 2.5 to 3 litres."]})

    if faf < 2:
        recs.append({"icon":"🏃","title":"Move More and Start Small",
            "steps":["A 20-minute walk after dinner is a powerful place to start.",
                     "Find one activity you genuinely enjoy: dancing, cycling, or swimming.",
                     "Build gradually to 150 minutes of moderate activity per week.",
                     "Take the stairs, park further away, and treat every step as progress."]})
    else:
        recs.append({"icon":"💪","title":"Your Activity Level Is a Strength",
            "steps":["Keep up your exercise habit — it is one of the strongest predictors of long-term health.",
                     "Consider adding strength training 2 days a week if you have not already.",
                     "Recover well: prioritise sleep and protein after workouts."]})

    if smoke == 'yes':
        recs.append({"icon":"🚭","title":"Quitting Smoking Is the Single Best Thing You Can Do",
            "steps":["Speak to your doctor about nicotine replacement therapy options.",
                     "Try a certified quit-smoking programme such as the NHS Stop Smoking service.",
                     "Set a quit date and tell someone you trust to hold you accountable.",
                     "Replace the habit with something physical: a short walk or deep breathing exercises."]})

    if calc in ['frequently', 'always']:
        recs.append({"icon":"🍷","title":"Moderate Your Alcohol Intake",
            "steps":["Limit to 1 drink for women and 2 for men per day at most.",
                     "Alcohol adds significant empty calories, often more than a full meal.",
                     "Designate alcohol-free days each week to reset your habits.",
                     "Swap cocktails for sparkling water with a splash of juice."]})

    if scc == 'no':
        recs.append({"icon":"📊","title":"Start Tracking What You Eat",
            "steps":["Try MyFitnessPal or Cronometer for just one week.",
                     "Most people are surprised by how many calories their lighter meals contain.",
                     "You do not need to track forever — just until you develop a clear sense of portions.",
                     "Focus on protein and fibre intake, not just total calories."]})

    if caec in ['frequently', 'always']:
        recs.append({"icon":"🍎","title":"Bring Mindfulness to Snacking",
            "steps":["Before reaching for a snack, drink a glass of water and wait 10 minutes.",
                     "Prepare healthy snack portions in advance: nuts, fruit, or yoghurt.",
                     "Avoid eating in front of screens as it leads to significantly more consumption.",
                     "Keep unhealthy snacks out of the house entirely."]})

    if tue > 4:
        recs.append({"icon":"📱","title":"Break the Screen-Sitting Cycle",
            "steps":["Set a timer to stand and stretch for 5 minutes every hour.",
                     "Use the Pomodoro approach: 25 minutes of work, then a 5-minute movement break.",
                     "Walk while taking calls. Stretch while watching TV.",
                     "Limit recreational screen time to under 2 hours after work."]})

    if mtrans in ['Automobile', 'Motorbike']:
        recs.append({"icon":"🚴","title":"Add Movement to Your Commute",
            "steps":["Try cycling or walking for trips under 2 km.",
                     "Get off public transport one stop early and walk the rest.",
                     "Even parking further from your destination adds meaningful daily steps.",
                     "Active commuting is exercise you do not have to schedule separately."]})

    if ncp > 4:
        recs.append({"icon":"🍽️","title":"Simplify Your Meal Structure",
            "steps":["Aim for 3 balanced meals with at most 1 or 2 planned snacks.",
                     "Large meals spread across the day are easier to manage than frequent small ones.",
                     "Eating on a consistent schedule helps regulate hunger hormones.",
                     "Each main meal should include a source of protein, fibre, and healthy fat."]})

    return recs[:8]


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def results_page():
    return render_template('results.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')


# ── Predict ───────────────────────────────────────────────────────────────────
@app.route('/api/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({
            'success': False,
            'error': 'Models not loaded. Ensure all .pkl files are present in the root directory.'
        }), 500

    try:
        d = request.get_json()
        if not d:
            return jsonify({'success': False, 'error': 'No JSON data received.'}), 400

        # ── Unit conversions ─────────────────────────────────────────────────
        h = float(d.get('Height', 0))
        w = float(d.get('Weight', 0))
        if d.get('height_unit') == 'ft':
            h = round(h * 0.3048, 3)
        if d.get('weight_unit') == 'lbs':
            w = round(w * 0.453592, 2)

        if h <= 0 or w <= 0:
            return jsonify({'success': False, 'error': 'Height and weight must be greater than zero.'}), 400

        inp = {
            'Gender':                         d.get('Gender'),
            'Age':                            float(d.get('Age', 25)),
            'Height':                         round(h, 3),
            'Weight':                         round(w, 2),
            'family_history_with_overweight': d.get('family_history_with_overweight', 'no'),
            'FAVC':                           d.get('FAVC', 'no'),
            'FCVC':                           float(d.get('FCVC', 2)),
            'NCP':                            float(d.get('NCP', 3)),
            'CAEC':                           d.get('CAEC', 'sometimes'),
            'CH2O':                           float(d.get('CH2O', 2)),
            'CALC':                           d.get('CALC', 'no'),
            'SMOKE':                          d.get('SMOKE', 'no'),
            'SCC':                            d.get('SCC', 'no'),
            'FAF':                            float(d.get('FAF', 1)),
            'TUE':                            float(d.get('TUE', 1)),
            'MTRANS':                         d.get('MTRANS', 'Public_Transportation'),
        }

        df = pd.DataFrame([inp])
        df = df[metadata['feature_names']]  # enforce column order

        for col in cat_cols:
            if col in df.columns:
                df[col] = le_dict[col].transform(df[col].astype(str))

        X = scaler.transform(df)

        # ── Predict — suppress all xgboost deprecation warnings ─────────────
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            pred_idx  = int(model.predict(X)[0])
            pred_prob = model.predict_proba(X)[0]

        bmi  = round(w / (h ** 2), 1)
        meta = OB_META.get(pred_idx, OB_META[1])
        recs = personalized_recs(d)

        prob_dict = {}
        for i, cls in enumerate(tgt_enc.classes_):
            prob_dict[cls] = round(float(pred_prob[i]) * 100, 1)

        return jsonify({
            'success':         True,
            'prediction': {
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


# ── Error handlers ────────────────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Server error'}), 500


if __name__ == '__main__':
    app.run(
        debug=False,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000))
    )
