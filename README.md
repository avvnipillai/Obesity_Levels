# 🏥 HealthAlign - Obesity Prediction & Personalized Health Recommendations

A modern, AI-powered web application that predicts obesity risk and provides personalized, empathetic lifestyle and dietary recommendations based on machine learning analysis of the UCI Obesity Dataset.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3+-green)
![XGBoost](https://img.shields.io/badge/XGBoost-ML%20Model-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## ✨ Features

### 🎯 Comprehensive Health Assessment
- **Interactive Form** with 16 personalized health questions
- **Smart Toggles, Sliders, and Dropdowns** for intuitive input
- **Animated Weighing Scale** for visual engagement
- **Real-time Validation** and helpful error messages

### 🤖 AI-Powered Predictions
- **XGBoost Classification Model** trained on 6,278 real-world data points
- **7 Obesity Classifications** (Insufficient Weight to Obesity Type III)
- **Confidence Scores** showing prediction probability for each category
- **BMI Calculation** with health status interpretation

### 💡 Personalized Recommendations
- **10 Lifestyle Categories** analyzed for each user
- **Gentle, Empathetic Language** (never condescending)
- **Actionable Suggestions** based on user's specific inputs
- **Evidence-Based Advice** from legitimate health sources
- **Customized to Each User** - recommendations change based on their data

### 📊 Comprehensive EDA Analysis
- **8 Interactive Charts** showing health patterns
- **Statistical Insights** with data interpretation
- **Feature Importance Analysis** showing key health factors
- **Evidence-Based Findings** and recommendations

### 🎨 Modern User Interface
- **Responsive Design** (works on desktop, tablet, mobile)
- **Dark/Light Mode Toggle** with system preference detection
- **Glass-Morphism Effects** and smooth animations
- **Professional Typography** with sophisticated font choices
- **Gradient Color Schemes** for visual appeal

### 🌙 Dark Mode Support
- Automatic detection of system preference
- Manual toggle with persistent storage
- Optimized color schemes for both modes
- Smooth transitions

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git (for deployment)

### Local Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/obesity-prediction.git
cd obesity-prediction

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Open browser to http://localhost:5000
```

### Google Colab Training

1. Open [Google Colab](https://colab.research.google.com)
2. Copy contents of `google_colab_training.py`
3. Run the notebook to train models
4. Download all `.pkl` files
5. Place them in the project root directory

---

## 📁 Project Structure

```
obesity-prediction/
├── app.py                          # Flask application & API
├── requirements.txt                # Python dependencies
├── Procfile                        # Render deployment config
├── DEPLOYMENT_GUIDE.md             # Detailed setup guide
├── google_colab_training.py        # Model training script
├── templates/
│   ├── index.html                 # Assessment page
│   └── analysis.html              # EDA dashboard
├── static/
│   ├── css/
│   │   └── styles.css             # All styling & animations
│   └── js/
│       ├── theme.js               # Dark/light mode
│       ├── animations.js          # UI animations
│       ├── form.js                # Form handling
│       └── analysis.js            # Charts & analysis
├── [Model files: *.pkl]           # Pre-trained models
└── README.md                       # This file
```

---

## 🔧 Technology Stack

### Backend
- **Flask** - Web framework
- **XGBoost** - Machine learning model
- **Scikit-learn** - Preprocessing & scaling
- **Pandas/NumPy** - Data handling

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling with animations
- **JavaScript (ES6)** - Interactivity
- **Chart.js** - Data visualization

### Deployment
- **Render.com** - Free cloud hosting
- **Gunicorn** - WSGI server
- **GitHub** - Version control

---

## 📊 Model Details

### Training Data
- **Source**: UCI Machine Learning Repository - Obesity Dataset
- **Records**: 6,278 individuals
- **Features**: 16 input variables
- **Target**: 7 obesity classifications

### Architecture
- **Algorithm**: XGBoost Classifier
- **Training Split**: 80% train, 20% test
- **Validation**: Stratified K-Fold cross-validation
- **Performance**: ~95%+ accuracy

### Input Features
1. Gender (Male/Female)
2. Age (years)
3. Height (meters)
4. Weight (kilograms)
5. Family history of overweight (Yes/No)
6. High-caloric food consumption (Yes/No)
7. Vegetable consumption frequency
8. Number of main meals
9. Between-meal snacking (No/Sometimes/Frequently/Always)
10. Water consumption (liters/day)
11. Alcohol consumption (No/Sometimes/Frequently/Always)
12. Smoking (Yes/No)
13. Calorie monitoring (Yes/No)
14. Physical activity frequency (days/week)
15. Technology usage (hours/day)
16. Transportation mode (Walking/Public/Automobile/etc.)

### Output Classes
```
0 - Insufficient Weight (BMI < 18.5)
1 - Normal Weight (BMI 18.5-24.9)
2 - Overweight Level I (BMI 25-26.9)
3 - Overweight Level II (BMI 27-29.9)
4 - Obesity Type I (BMI 30-34.9)
5 - Obesity Type II (BMI 35-39.9)
6 - Obesity Type III (BMI ≥ 40)
```

---

## 🌐 Deployment

### Render.com (Recommended - Free Tier)

**Full instructions in `DEPLOYMENT_GUIDE.md`**

Quick steps:
1. Push code to GitHub
2. Connect GitHub to Render
3. Set up web service
4. Deploy

---

## 💡 Features in Detail

### Assessment Page
- **Animated Scale** - Visual weight display
- **16-Question Form** - Covers all health factors
- **Smart Input Types** - Sliders, toggles, dropdowns
- **Real-time Validation** - Helpful error messages
- **Results Display** - Color-coded risk assessment
- **Probability Chart** - Confidence for each obesity level
- **Personalized Recommendations** - 10 categories tailored to user

### Analysis Page
- **Obesity Distribution** - Population breakdown
- **BMI Analysis** - Weight status patterns
- **Age vs Weight** - Relationship visualization
- **Exercise Impact** - Physical activity correlation
- **Dietary Impact** - High-calorie food effects
- **Water Intake** - Hydration importance
- **Screen Time** - Technology usage effects
- **Feature Importance** - Key health factors
- **Key Findings** - Data insights
- **Evidence-Based Recommendations** - Health guidance

### Dark Mode
- Automatic system preference detection
- Manual toggle in header
- Persistent storage (localStorage)
- Smooth transitions
- Optimized readability for both modes

---

## 🎯 Recommendation Categories

The app provides personalized suggestions in these areas:

1. **High-Calorie Food Consumption** - Reduction strategies
2. **Vegetable Intake** - Increasing consumption
3. **Water Hydration** - Daily water intake targets
4. **Physical Activity** - Exercise recommendations
5. **Smoking Cessation** - Quit smoking resources
6. **Alcohol Moderation** - Consumption guidelines
7. **Calorie Monitoring** - Tracking methods
8. **Between-Meal Snacking** - Mindful eating
9. **Screen Time Reduction** - Activity increase
10. **Transportation Choices** - Active commuting

Each recommendation includes:
- ✓ Personalized title
- ✓ 3-5 actionable suggestions
- ✓ Gentle, encouraging tone
- ✓ Practical, implementable steps
- ✓ No medical jargon

---

## 📱 Responsive Design

- **Desktop** - Full-featured experience
- **Tablet** - Optimized layout
- **Mobile** - Touch-friendly interface
- **All Devices** - Consistent functionality

---

## 🔐 Privacy & Security

- ✓ No user data collection
- ✓ No authentication required
- ✓ No external tracking
- ✓ All processing server-side
- ✓ HTTPS support (Render provides SSL)
- ✓ No cookies for tracking

---

## ⚠️ Important Disclaimer

**This application is for educational and informational purposes only.**

It provides:
- ❌ NOT medical diagnosis
- ❌ NOT medical advice
- ❌ NOT treatment recommendations
- ❌ NOT substitute for healthcare provider

It provides:
- ✓ Informational assessment
- ✓ Educational insights
- ✓ Lifestyle suggestions
- ✓ Health awareness

**Always consult with a qualified healthcare provider for:**
- Medical diagnosis
- Treatment plans
- Personalized medical advice
- Specific health concerns

---

## 🛠️ Troubleshooting

### Issue: Models not loading
**Solution**: Verify all `.pkl` files are in root directory

### Issue: Slow page loads
**Solution**: Normal on free Render tier. Cold starts take 30 seconds.

### Issue: Form submission fails
**Solution**: Check browser console (F12). Verify model files exist.

### Issue: Dark mode not working
**Solution**: Clear localStorage and refresh page

---

## 📚 API Reference

### POST /api/predict

**Request Body:**
```json
{
  "Gender": "Male",
  "Age": 25,
  "Height": 1.75,
  "Weight": 80,
  "family_history_with_overweight": "no",
  "FAVC": "no",
  "FCVC": 2.5,
  "NCP": 3,
  "CAEC": "no",
  "CH2O": 2.5,
  "CALC": "no",
  "SMOKE": "no",
  "SCC": "yes",
  "FAF": 3,
  "TUE": 2,
  "MTRANS": "Public_Transportation"
}
```

**Response:**
```json
{
  "success": true,
  "prediction": {
    "index": 1,
    "name": "Normal Weight",
    "risk_level": "Healthy",
    "color": "green",
    "message": "Great! You're maintaining a healthy weight..."
  },
  "bmi": 26.1,
  "probabilities": {
    "Insufficient Weight": 0.01,
    "Normal Weight": 0.78,
    ...
  },
  "recommendations": [...]
}
```

---

## 📝 Recommendations Engine

Recommendations are generated based on:

1. **User Input Analysis** - Each answer is evaluated
2. **Evidence-Based Guidelines** - From reputable health sources
3. **Personalization** - Tailored to individual inputs
4. **Tone & Sensitivity** - Empathetic, non-judgmental language
5. **Actionability** - Practical, implementable steps

Sources include:
- WHO (World Health Organization)
- NIH (National Institutes of Health)
- CDC (Centers for Disease Control)
- Academic nutritionist recommendations
- Evidence-based health studies

---

## 📈 Future Enhancements

Potential additions:
- [ ] User accounts & progress tracking
- [ ] Meal planning integration
- [ ] Exercise program recommendations
- [ ] Mobile app version
- [ ] Multi-language support
- [ ] Doctor export feature
- [ ] Community features
- [ ] AI chatbot support

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- **UCI Machine Learning Repository** - Dataset
- **XGBoost Team** - ML framework
- **Flask Team** - Web framework
- **Chart.js Team** - Data visualization
- **Health Organizations** - Evidence-based guidelines

---

## 📧 Support

For issues or questions:

1. Check `DEPLOYMENT_GUIDE.md` for setup help
2. Review error logs in Render dashboard
3. Verify all project files are present
4. Test locally before deploying

---

## 🌟 Star This Project!

If you find this helpful, please star ⭐ this repository!

---

**Built with ❤️ for health awareness and education**


---

**Happy coding and stay healthy!** 🏃‍♂️💪
