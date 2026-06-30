# 🏥 HealthAlign - Obesity Prediction & Personalized Health Recommendations

A modern,web application that predicts obesity risk and provides personalized, empathetic lifestyle and dietary recommendations based on machine learning analysis of the UCI Obesity Dataset.

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

