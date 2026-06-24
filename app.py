import os
import joblib
import json
from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import traceback

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# ============================================================================
# LOAD TRAINED MODELS AND PREPROCESSORS
# ============================================================================

try:
    model = joblib.load('xgboost_model.pkl')
    scaler = joblib.load('scaler.pkl')
    label_encoders = joblib.load('label_encoders.pkl')
    target_encoder = joblib.load('target_encoder.pkl')
    categorical_cols = joblib.load('categorical_cols.pkl')
    numerical_cols = joblib.load('numerical_cols.pkl')
    metadata = joblib.load('model_metadata.pkl')
    print("✓ All models and preprocessors loaded successfully!")
except Exception as e:
    print(f"✗ Error loading models: {e}")
    print("Make sure all .pkl files are in the same directory as app.py")

# ============================================================================
# OBESITY CLASSIFICATIONS AND HEALTH RANGES
# ============================================================================

OBESITY_CLASSIFICATION = {
    0: {
        'name': 'Insufficient Weight',
        'risk_level': 'Low',
        'color': 'blue',
        'message': 'You have insufficient weight. Consider consulting a healthcare provider about healthy weight gain strategies.'
    },
    1: {
        'name': 'Normal Weight',
        'risk_level': 'Healthy',
        'color': 'green',
        'message': 'Great! You\'re maintaining a healthy weight. Continue with your current lifestyle habits.'
    },
    2: {
        'name': 'Overweight Level I',
        'risk_level': 'Moderate',
        'color': 'orange',
        'message': 'You\'re slightly overweight. Small lifestyle adjustments can help you reach a healthier weight.'
    },
    3: {
        'name': 'Overweight Level II',
        'risk_level': 'Moderate-High',
        'color': 'orange-red',
        'message': 'You\'re overweight. It\'s a good time to make meaningful changes to your diet and exercise routine.'
    },
    4: {
        'name': 'Obesity Type I',
        'risk_level': 'High',
        'color': 'red',
        'message': 'You have obesity Type I. Professional guidance from a healthcare provider is recommended.'
    },
    5: {
        'name': 'Obesity Type II',
        'risk_level': 'Very High',
        'color': 'dark-red',
        'message': 'You have obesity Type II. Please consult with a healthcare professional for personalized guidance.'
    },
    6: {
        'name': 'Obesity Type III',
        'risk_level': 'Critical',
        'color': 'dark-red',
        'message': 'You have obesity Type III. Professional medical consultation is strongly recommended.'
    }
}

# ============================================================================
# PERSONALIZED RECOMMENDATIONS
# ============================================================================

RECOMMENDATIONS = {
    'high_caloric': {
        'yes': {
            'title': 'Reduce High-Calorie Foods',
            'suggestions': [
                'Start gradually replacing fried foods with baked or grilled alternatives',
                'Swap sugary drinks (soda, energy drinks) with water, herbal tea, or unsweetened beverages',
                'Try using low-fat or fat-free versions of dairy products',
                'When eating snacks, choose nuts, fruits, or yogurt instead of chips and candy',
                'Read food labels to be aware of calories and hidden sugars'
            ]
        },
        'no': {
            'title': 'Maintain Your Good Eating Habits',
            'suggestions': [
                'Keep avoiding high-calorie processed foods',
                'Continue making smart food choices that support your health',
                'Your awareness of nutrition is a great asset'
            ]
        }
    },
    'vegetable': {
        'low': {
            'title': 'Increase Vegetable Intake',
            'suggestions': [
                'Add vegetables to every meal: a handful of spinach in breakfast, veggies with lunch, salad with dinner',
                'Try adding frozen vegetables to meals - they\'re convenient and nutritious',
                'Experiment with different cooking methods: roasted, steamed, or raw',
                'Start with vegetables you already enjoy and branch out from there',
                'Aim for a variety of colors - different colors provide different nutrients'
            ]
        },
        'high': {
            'title': 'Great Job on Vegetable Consumption',
            'suggestions': [
                'You\'re doing great with vegetables',
                'Keep exploring new varieties to maintain interest and nutrition',
                'Consider growing your own vegetables if you have space'
            ]
        }
    },
    'water': {
        'low': {
            'title': 'Increase Water Intake',
            'suggestions': [
                'Start your day with a glass of water and keep a water bottle with you',
                'Drink water before, during, and after exercise',
                'Replace one sugary drink per day with water',
                'Add natural flavor with lemon, cucumber, or mint if plain water is boring',
                'Aim for at least 2-3 liters (8-10 glasses) daily, or more if you exercise'
            ]
        },
        'high': {
            'title': 'Excellent Water Consumption',
            'suggestions': [
                'You\'re staying well hydrated',
                'Keep up this excellent habit',
                'Proper hydration supports your overall health and metabolism'
            ]
        }
    },
    'exercise': {
        'low': {
            'title': 'Increase Physical Activity',
            'suggestions': [
                'Start small: a 15-20 minute walk daily can make a real difference',
                'Choose activities you enjoy - dancing, swimming, cycling, or sports are great options',
                'Try to move during your day: use stairs instead of elevators, park farther away',
                'Set a goal to increase activity gradually, don\'t rush into intense workouts',
                'Find a workout buddy for motivation and accountability'
            ]
        },
        'high': {
            'title': 'You\'re Very Active',
            'suggestions': [
                'Excellent work maintaining high physical activity levels',
                'Keep challenging yourself with new activities or increased intensity',
                'Your fitness habits are contributing positively to your health'
            ]
        }
    },
    'smoking': {
        'yes': {
            'title': 'Consider Quitting Smoking',
            'suggestions': [
                'Talk to your doctor about smoking cessation programs',
                'Try nicotine replacement therapy options like patches or gum',
                'Find a support group or online community for smokers trying to quit',
                'Replace the habit with something healthier like chewing gum or snacking on vegetables',
                'Quitting smoking will improve your weight and overall health'
            ]
        },
        'no': {
            'title': 'Great Choice - Keep Not Smoking',
            'suggestions': [
                'You\'re making a excellent decision for your health',
                'Avoiding smoking significantly reduces health risks',
                'Keep avoiding secondhand smoke when possible'
            ]
        }
    },
    'alcohol': {
        'yes': {
            'title': 'Moderate Your Alcohol Consumption',
            'suggestions': [
                'Limit to moderate amounts: up to 1 drink per day for women, 2 for men',
                'Be aware that alcoholic drinks contain empty calories',
                'Try alternating alcoholic drinks with water',
                'Choose lower-calorie options like light beer or wine spritzers',
                'Avoid binge drinking which can negatively impact weight and health'
            ]
        },
        'no': {
            'title': 'Good Decision on Alcohol',
            'suggestions': [
                'You\'re avoiding unnecessary calories from alcohol',
                'Keep maintaining this healthy choice',
                'Your abstinence is beneficial for your overall health'
            ]
        }
    },
    'monitor_calories': {
        'yes': {
            'title': 'Continue Monitoring Your Calories',
            'suggestions': [
                'You\'re already doing great by tracking your intake',
                'Try using a food journal or app to continue monitoring',
                'This awareness is key to maintaining a healthy weight',
                'Keep up this positive habit'
            ]
        },
        'no': {
            'title': 'Start Monitoring Your Calorie Intake',
            'suggestions': [
                'Use a food tracking app like MyFitnessPal or Cronometer',
                'Keep a simple food journal for a week to understand your eating patterns',
                'This doesn\'t mean obsessing, just becoming aware of what you eat',
                'Many people are surprised by their actual intake when they start tracking'
            ]
        }
    },
    'snacking': {
        'yes': {
            'title': 'Be Mindful of Between-Meal Snacking',
            'suggestions': [
                'Choose healthy snacks like fruits, nuts, yogurt, or vegetables',
                'Avoid keeping tempting snacks easily accessible',
                'Drink water first - sometimes thirst feels like hunger',
                'Set specific snack times rather than snacking continuously',
                'Practice portion control with pre-portioned snack containers'
            ]
        },
        'no': {
            'title': 'Excellent - Keep Avoiding Frequent Snacking',
            'suggestions': [
                'You\'re doing great by limiting between-meal eating',
                'Keep up this positive habit',
                'This contributes to better blood sugar levels and weight management'
            ]
        }
    },
    'tech_time': {
        'high': {
            'title': 'Reduce Screen Time and Increase Movement',
            'suggestions': [
                'Set a timer to take a 5-minute break from screens every hour',
                'Do some stretches or light exercises during breaks',
                'Try using a standing desk or adjustable workstation',
                'Walk around while taking phone calls or watching videos',
                'Plan outdoor activities that don\'t involve screens'
            ]
        },
        'low': {
            'title': 'Good Balance of Screen Time',
            'suggestions': [
                'You\'re maintaining a healthy balance with technology use',
                'Keep taking breaks from screens regularly',
                'Your activity level is supporting your health'
            ]
        }
    },
    'transport': {
        'sedentary': {
            'title': 'Choose More Active Transportation',
            'suggestions': [
                'Walk or cycle for short distances instead of driving',
                'Take public transport and walk to the station',
                'Park farther away to add more walking to your day',
                'If possible, combine transportation methods for more movement',
                'Active commuting adds exercise to your daily routine'
            ]
        },
        'active': {
            'title': 'Great Active Transportation Choices',
            'suggestions': [
                'You\'re getting extra activity through your transportation choices',
                'This contributes significantly to your daily exercise',
                'Keep using active transportation when possible'
            ]
        }
    },
    'meals_per_day': {
        'high': {
            'title': 'Consider Spreading Meals More Evenly',
            'suggestions': [
                'Eating fewer large meals can lead to overeating',
                'Try eating 3 balanced meals plus 1-2 healthy snacks',
                'Balanced meals with protein, vegetables, and whole grains keep you fuller',
                'Regular meal timing helps maintain stable blood sugar'
            ]
        },
        'normal': {
            'title': 'Good Meal Frequency',
            'suggestions': [
                'You\'re eating a reasonable number of meals per day',
                'Focus on making each meal nutritious and balanced',
                'Keep up this healthy eating pattern'
            ]
        }
    }
}

# ============================================================================
# ROUTE: HOME PAGE
# ============================================================================

@app.route('/')
def index():
    """Serve the main assessment page"""
    return render_template('index.html')

# ============================================================================
# ROUTE: ANALYSIS PAGE
# ============================================================================

@app.route('/analysis')
def analysis():
    """Serve the EDA analysis page"""
    return render_template('analysis.html')

# ============================================================================
# ROUTE: PREDICT OBESITY AND GENERATE RECOMMENDATIONS
# ============================================================================

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict obesity level based on user inputs.
    
    Expected JSON:
    {
        'Gender': 'Male/Female',
        'Age': 25,
        'Height': 1.75,
        'Weight': 80,
        'family_history_with_overweight': 'yes/no',
        'FAVC': 'yes/no',
        'FCVC': 2,
        'NCP': 3,
        'CAEC': 'no/sometimes/frequently/always',
        'CH2O': 2.5,
        'CALC': 'no/sometimes/frequently/always',
        'SMOKE': 'yes/no',
        'SCC': 'yes/no',
        'FAF': 3,
        'TUE': 2,
        'MTRANS': 'Automobile/Bike/Motorbike/Public_Transportation/Walking'
    }
    """
    try:
        data = request.get_json()
        
        # Prepare input data
        input_data = {
            'Gender': data.get('Gender'),
            'Age': float(data.get('Age')),
            'Height': float(data.get('Height')),
            'Weight': float(data.get('Weight')),
            'family_history_with_overweight': data.get('family_history_with_overweight'),
            'FAVC': data.get('FAVC'),
            'FCVC': float(data.get('FCVC')),
            'NCP': float(data.get('NCP')),
            'CAEC': data.get('CAEC'),
            'CH2O': float(data.get('CH2O')),
            'CALC': data.get('CALC'),
            'SMOKE': data.get('SMOKE'),
            'SCC': data.get('SCC'),
            'FAF': float(data.get('FAF')),
            'TUE': float(data.get('TUE')),
            'MTRANS': data.get('MTRANS')
        }
        
        # Create DataFrame with correct column order
        df_input = pd.DataFrame([input_data])
        df_input = df_input[metadata['feature_names']]
        
        # Encode categorical variables
        for col in categorical_cols:
            if col in df_input.columns:
                df_input[col] = label_encoders[col].transform(df_input[col].astype(str))
        
        # Scale features
        X_scaled = scaler.transform(df_input)
        
        # Make prediction
        prediction_idx = model.predict(X_scaled)[0]
        prediction_proba = model.predict_proba(X_scaled)[0]
        
        # Get obesity classification
        obesity_level = OBESITY_CLASSIFICATION[prediction_idx]
        obesity_name = obesity_level['name']
        
        # Generate personalized recommendations
        recommendations = generate_recommendations(data)
        
        # Calculate BMI
        height = float(data.get('Height'))
        weight = float(data.get('Weight'))
        bmi = weight / (height ** 2)
        
        return jsonify({
            'success': True,
            'prediction': {
                'index': int(prediction_idx),
                'name': obesity_name,
                'risk_level': obesity_level['risk_level'],
                'color': obesity_level['color'],
                'message': obesity_level['message']
            },
            'bmi': round(bmi, 2),
            'probabilities': {
                'Insufficient Weight': float(prediction_proba[0]),
                'Normal Weight': float(prediction_proba[1]),
                'Overweight Level I': float(prediction_proba[2]),
                'Overweight Level II': float(prediction_proba[3]),
                'Obesity Type I': float(prediction_proba[4]),
                'Obesity Type II': float(prediction_proba[5]),
                'Obesity Type III': float(prediction_proba[6])
            },
            'recommendations': recommendations
        })
        
    except Exception as e:
        print(f"Prediction error: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# ============================================================================
# HELPER FUNCTION: GENERATE PERSONALIZED RECOMMENDATIONS
# ============================================================================

def generate_recommendations(data):
    """Generate personalized lifestyle and diet recommendations"""
    
    recommendations = []
    
    # High caloric food recommendation
    if data.get('FAVC') == 'yes':
        recommendations.append(RECOMMENDATIONS['high_caloric']['yes'])
    else:
        recommendations.append(RECOMMENDATIONS['high_caloric']['no'])
    
    # Vegetable consumption recommendation
    fcvc = float(data.get('FCVC', 0))
    if fcvc < 2:
        recommendations.append(RECOMMENDATIONS['vegetable']['low'])
    else:
        recommendations.append(RECOMMENDATIONS['vegetable']['high'])
    
    # Water intake recommendation
    ch2o = float(data.get('CH2O', 0))
    if ch2o < 2:
        recommendations.append(RECOMMENDATIONS['water']['low'])
    else:
        recommendations.append(RECOMMENDATIONS['water']['high'])
    
    # Exercise recommendation
    faf = float(data.get('FAF', 0))
    if faf < 2:
        recommendations.append(RECOMMENDATIONS['exercise']['low'])
    else:
        recommendations.append(RECOMMENDATIONS['exercise']['high'])
    
    # Smoking recommendation
    if data.get('SMOKE') == 'yes':
        recommendations.append(RECOMMENDATIONS['smoking']['yes'])
    else:
        recommendations.append(RECOMMENDATIONS['smoking']['no'])
    
    # Alcohol recommendation
    if data.get('CALC') in ['frequently', 'always']:
        recommendations.append(RECOMMENDATIONS['alcohol']['yes'])
    else:
        recommendations.append(RECOMMENDATIONS['alcohol']['no'])
    
    # Calorie monitoring recommendation
    if data.get('SCC') == 'yes':
        recommendations.append(RECOMMENDATIONS['monitor_calories']['yes'])
    else:
        recommendations.append(RECOMMENDATIONS['monitor_calories']['no'])
    
    # Snacking recommendation
    caec = data.get('CAEC', 'no')
    if caec in ['frequently', 'always']:
        recommendations.append(RECOMMENDATIONS['snacking']['yes'])
    else:
        recommendations.append(RECOMMENDATIONS['snacking']['no'])
    
    # Tech time recommendation
    tue = float(data.get('TUE', 0))
    if tue > 4:
        recommendations.append(RECOMMENDATIONS['tech_time']['high'])
    else:
        recommendations.append(RECOMMENDATIONS['tech_time']['low'])
    
    # Transportation recommendation
    mtrans = data.get('MTRANS', 'Automobile')
    if mtrans in ['Automobile', 'Motorbike']:
        recommendations.append(RECOMMENDATIONS['transport']['sedentary'])
    else:
        recommendations.append(RECOMMENDATIONS['transport']['active'])
    
    # Meals per day recommendation
    ncp = float(data.get('NCP', 3))
    if ncp > 4:
        recommendations.append(RECOMMENDATIONS['meals_per_day']['high'])
    else:
        recommendations.append(RECOMMENDATIONS['meals_per_day']['normal'])
    
    return recommendations

# ============================================================================
# ROUTE: GET EDA DATA
# ============================================================================

@app.route('/api/eda-data')
def get_eda_data():
    """Return EDA analysis data"""
    try:
        eda_data = joblib.load('eda_data.pkl')
        return jsonify({
            'success': True,
            'data': eda_data
        })
    except:
        return jsonify({
            'success': False,
            'error': 'EDA data not found. Run the training script first.'
        }), 404

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == '__main__':
    # For local testing
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
