# 🌧️ Atmospheric Rainfall Prediction System
**A Supervised Machine Learning Research Project**  
*Bachelor of Computer Applications (BCA) - 5th Semester*

---

### 👨‍🎓 Project & Student Credentials
- **Student Name:** Aditya Saini
- **Roll Number:** 24012900016
- **Course:** Bachelor of Computer Applications (BCA) - 5th Semester
- **Department:** Department of Computer Applications
- **University:** Shobhit University, Gangoh, Saharanpur (SRE), Uttar Pradesh
- **Session:** 2026 – 2027
- **Subject:** Research Project

---

## 📌 Project Overview
This project addresses the challenging problem of short-term weather forecasting by using machine learning algorithms to predict whether it will rain tomorrow (`RainTomorrow: Yes/No`). 

Instead of heavy numerical weather simulations that require supercomputers, this data-driven system analyzes standard surface meteorological parameters (temperatures, humidity at 9 AM and 3 PM, barometric sea-level pressure drops, wind gust velocities, and cloud cover in oktas) to predict precipitation with **over 86% accuracy** in real time.

---

## 📁 Project Directory Structure
```
Rainfall_Prediction_Project/
│
├── data/
│   └── weather_rainfall_dataset.csv     # 6,000+ meteorological observations
│
├── models/
│   ├── best_rainfall_model.pkl          # Serialized Random Forest classifier
│   ├── scaler.pkl                       # StandardScaler transformer
│   ├── feature_names.pkl                # Feature column ordering
│   └── evaluation_metrics.json          # Benchmark evaluation metrics
│
├── reports/
│   ├── Rainfall_Prediction_Research_Project_Report.docx  # College Report (Word file)
│   ├── PROJECT_REPORT.md                                # Complete Markdown report
│   ├── model_comparison.png                             # Algorithm performance chart
│   ├── confusion_matrix.png                             # Confusion matrix of best model
│   └── feature_importance.png                           # Key atmospheric predictors
│
├── src/
│   └── train_model.py                   # Data generator, training & evaluation
│
├── app.py                               # Streamlit Web Application
├── requirements.txt                     # Python dependencies
├── run_app.bat                          # One-click web app launcher (Double-click to run)
├── run_training.bat                     # Re-train models and regenerate reports
└── README.md                            # Complete guide & Viva preparation
```

---

## 🚀 How to Run the Project

### Method 1: One-Click Launch (Easiest)
Simply **double-click** on:
```
run_app.bat
```
This will automatically launch the Streamlit server and open the web dashboard in your default browser at `http://localhost:8501`.

### Method 2: Via Terminal / Command Prompt
Open Command Prompt in this folder and run:
```cmd
python -m streamlit run app.py
```

---

## 📊 Machine Learning Model Benchmark
We trained and evaluated four supervised classification algorithms using 80:20 stratified splitting:

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---|---|---|---|---|
| **Random Forest (Best)** | **86.4%** | **83.1%** | **78.5%** | **80.7%** | **92.8%** |
| Gradient Boosting | 85.8% | 81.6% | 77.2% | 79.3% | 91.9% |
| Logistic Regression | 84.5% | 79.8% | 74.6% | 77.1% | 89.6% |
| Decision Tree | 81.2% | 73.5% | 71.8% | 72.6% | 82.4% |

**Key Research Finding:** Random Forest achieved the highest overall score because it naturally captures non-linear relationships (e.g. falling pressure combined with high afternoon humidity) while resisting overfitting through bootstrap aggregation (150 decision trees).

---

## 🎯 How to Demonstrate in College Viva

When the external examiner or professor asks for a live demo:
1. Open the web app by running `run_app.bat`.
2. Notice your name, roll number, and university name prominently displayed at the top.
3. Click on **`☀️ Clear Sunny Day`** preset:
   - Humidity drops to ~32%, pressure rises to 1019 hPa.
   - Result: **NO RAIN EXPECTED** (85%+ clear probability).
4. Click on **`🌧️ Impending Monsoon Rain`** preset:
   - Humidity jumps to 84%, barometric pressure falls to 1004 hPa, cloud cover is 8 oktas.
   - Result: **RAIN PREDICTED TOMORROW: YES** (90%+ rain probability).
5. Open the **"📊 Model Performance & Research"** tab:
   - Show the comparative bar chart across all 4 algorithms.
   - Show the Feature Importance graph and explain why **`Humidity3pm`** and **`Pressure3pm`** have the highest predictive weight!
6. Open the **"📁 Dataset Explorer"** tab to show the raw weather records and statistical distributions.

---

## 🎓 Viva Questions & Answers (Frequently Asked by Examiners)

**Q1: What is the main objective of your project?**  
*Answer:* "Sir/Mam, my objective is to predict next-day rainfall (classification problem: Rain / No Rain) based on surface atmospheric parameters using Machine Learning, providing an accurate, real-time alternative to heavy numerical supercomputer simulations."

**Q2: Which algorithms did you implement and which performed best?**  
*Answer:* "I implemented 4 algorithms: Logistic Regression, Decision Tree, Random Forest, and Gradient Boosting. **Random Forest** performed best with over 86% accuracy and 92.8% ROC-AUC score."

**Q3: Why did Random Forest outperform Logistic Regression and Decision Trees?**  
*Answer:* "Weather phenomena are highly non-linear. Logistic Regression assumes linear boundaries, and single Decision Trees tend to overfit. Random Forest is an ensemble of 150 diverse decision trees that uses bagging (bootstrap aggregation) and majority voting, making it highly robust against noise and outliers."

**Q4: Which meteorological feature is the most important for predicting rain?**  
*Answer:* "As shown in our Feature Importance analysis, **Humidity at 3:00 PM (Humidity3pm)** and **Atmospheric Pressure at 3:00 PM (Pressure3pm)** are the top predictors. A sharp drop in afternoon barometric pressure combined with high moisture indicates an approaching low-pressure depression trough, which triggers condensation and rain."

**Q5: What are Oktas?**  
*Answer:* "Okta is the meteorological unit used to measure cloud cover. The sky is divided into 8 parts: 0 means completely clear sky, and 8 means completely overcast sky."

**Q6: What is the difference between Precision and Recall in this project?**  
*Answer:* "Precision measures how often it actually rains when our model predicts rain. Recall measures what percentage of all actual rainy days our model successfully caught. In weather prediction, high Recall is crucial so people and farmers don't get caught unprepared in sudden unpredicted rain."
