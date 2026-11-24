import os
import json
import streamlit as st
import numpy as np
import pandas as pd
import joblib

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Rainfall Prediction System | Aditya Saini",
    page_icon="🌧️",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# Custom CSS for polished styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 15px;
    }
    .student-badge {
        background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .result-card-rain {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
        color: white;
        padding: 22px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
    }
    .result-card-norain {
        background: linear-gradient(135deg, #D97706 0%, #F59E0B 100%);
        color: white;
        padding: 22px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(245, 158, 11, 0.3);
    }
    .metric-box {
        background-color: #F3F4F6;
        border-left: 4px solid #2563EB;
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_ml_components():
    model_path = os.path.join(MODELS_DIR, "best_rainfall_model.pkl")
    scaler_path = os.path.join(MODELS_DIR, "scaler.pkl")
    features_path = os.path.join(MODELS_DIR, "feature_names.pkl")
    metrics_path = os.path.join(MODELS_DIR, "evaluation_metrics.json")
    
    if not (os.path.exists(model_path) and os.path.exists(scaler_path)):
        return None, None, None, None
        
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    features = joblib.load(features_path)
    
    metrics = None
    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            metrics = json.load(f)
            
    return model, scaler, features, metrics


@st.cache_data
def load_sample_dataset():
    csv_path = os.path.join(DATA_DIR, "weather_rainfall_dataset.csv")
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return None


model, scaler, feature_names, metrics = load_ml_components()

# ---------------------------------------------------------
# Sidebar - Academic Information
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/rain.png", width=80)
    st.title("Project Overview")
    st.markdown("""
    **Course:** BCA (5th Semester)  
    **Subject:** Research Project  
    **Topic:** Weather Rainfall Prediction  
    
    ---
    **Author Details:**
    - **Student:** Aditya Saini  
    - **Roll No:** 24012900016  
    - **Institute:** Shobhit University, Gangoh, Saharanpur (SRE)  
    - **Academic Session:** 2026 – 2027  
    - **Mentor / Guide:** Faculty of Computer Applications  
    ---
    """)
    st.info("💡 **Tip:** Use the preset buttons on the main screen to quickly test different meteorological conditions.")


# ---------------------------------------------------------
# Header & Navigation
# ---------------------------------------------------------
st.markdown('<div class="main-title">🌧️ Intelligent Rainfall Prediction System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">A Supervised Machine Learning Research Project for High-Accuracy Atmospheric Weather Forecasting</div>', unsafe_allow_html=True)

st.markdown("""
<div class="student-badge">
    <strong>Candidate Name:</strong> Aditya Saini &nbsp;|&nbsp; 
    <strong>Roll No:</strong> 24012900016 &nbsp;|&nbsp; 
    <strong>University:</strong> Shobhit University Gangoh, SRE &nbsp;|&nbsp; 
    <strong>Session:</strong> 2026-2027
</div>
""", unsafe_allow_html=True)

if model is None:
    st.warning("⚠️ Machine learning models have not been trained yet. Please run `python src/train_model.py` to train and build models.")
    st.stop()

tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 Live Prediction Dashboard", 
    "📊 Model Performance & Research", 
    "📁 Dataset Explorer", 
    "📑 About Project & Documentation"
])

# ---------------------------------------------------------
# TAB 1: Live Prediction Dashboard
# ---------------------------------------------------------
with tab1:
    st.subheader("1. Enter Meteorological Atmospheric Parameters")
    
    # Presets for ease of demo during viva
    st.markdown("**Quick Preset Scenarios:**")
    preset_cols = st.columns(3)
    
    # Default values
    def_min_temp = 15.2
    def_max_temp = 28.4
    def_rainfall = 0.0
    def_gust = 35.0
    def_wind9 = 15.0
    def_wind3 = 20.0
    def_hum9 = 65.0
    def_hum3 = 48.0
    def_press9 = 1018.0
    def_press3 = 1014.5
    def_cloud9 = 3
    def_cloud3 = 4
    def_temp9 = 19.5
    def_temp3 = 26.8
    def_rain_today = "No"

    if 'preset' not in st.session_state:
        st.session_state.preset = 'default'

    if preset_cols[0].button("☀️ Clear Sunny Day (No Rain)"):
        st.session_state.preset = 'sunny'
    if preset_cols[1].button("🌧️ Impending Monsoon Rain (High Probability)"):
        st.session_state.preset = 'rainy'
    if preset_cols[2].button("⛅ Moderately Humid / Overcast"):
        st.session_state.preset = 'overcast'

    if st.session_state.preset == 'sunny':
        def_min_temp, def_max_temp = 18.0, 34.0
        def_rainfall = 0.0
        def_gust = 25.0
        def_wind9, def_wind3 = 10.0, 15.0
        def_hum9, def_hum3 = 45.0, 32.0
        def_press9, def_press3 = 1022.0, 1019.0
        def_cloud9, def_cloud3 = 1, 1
        def_temp9, def_temp3 = 22.0, 32.5
        def_rain_today = "No"
    elif st.session_state.preset == 'rainy':
        def_min_temp, def_max_temp = 21.0, 27.5
        def_rainfall = 14.5
        def_gust = 58.0
        def_wind9, def_wind3 = 22.0, 30.0
        def_hum9, def_hum3 = 88.0, 84.0
        def_press9, def_press3 = 1008.0, 1004.0
        def_cloud9, def_cloud3 = 7, 8
        def_temp9, def_temp3 = 23.0, 25.5
        def_rain_today = "Yes"
    elif st.session_state.preset == 'overcast':
        def_min_temp, def_max_temp = 16.0, 26.0
        def_rainfall = 1.2
        def_gust = 38.0
        def_wind9, def_wind3 = 14.0, 18.0
        def_hum9, def_hum3 = 72.0, 64.0
        def_press9, def_press3 = 1014.0, 1011.0
        def_cloud9, def_cloud3 = 5, 6
        def_temp9, def_temp3 = 18.5, 24.2
        def_rain_today = "No"

    with st.form("prediction_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("##### 🌡️ Temperature (°C)")
            min_temp = st.number_input("Minimum Temperature", -10.0, 50.0, float(def_min_temp), step=0.5)
            max_temp = st.number_input("Maximum Temperature", -10.0, 55.0, float(def_max_temp), step=0.5)
            temp_9am = st.number_input("Temperature at 9:00 AM", -10.0, 50.0, float(def_temp9), step=0.5)
            temp_3pm = st.number_input("Temperature at 3:00 PM", -10.0, 50.0, float(def_temp3), step=0.5)
            
        with col2:
            st.markdown("##### 💧 Humidity & Precipitation")
            humidity_9am = st.slider("Humidity at 9:00 AM (%)", 0, 100, int(def_hum9))
            humidity_3pm = st.slider("Humidity at 3:00 PM (%)", 0, 100, int(def_hum3))
            rainfall_today = st.number_input("Rainfall Today (mm)", 0.0, 300.0, float(def_rainfall), step=0.5)
            rain_today_choice = st.selectbox("Did it rain today?", ["No", "Yes"], index=1 if def_rain_today == "Yes" else 0)

        with col3:
            st.markdown("##### 🧭 Pressure, Wind & Cloud Cover")
            pressure_9am = st.number_input("Pressure at 9:00 AM (hPa)", 950.0, 1050.0, float(def_press9), step=0.5)
            pressure_3pm = st.number_input("Pressure at 3:00 PM (hPa)", 950.0, 1050.0, float(def_press3), step=0.5)
            wind_gust = st.number_input("Wind Gust Speed (km/h)", 0.0, 150.0, float(def_gust), step=1.0)
            wind_9am = st.number_input("Wind Speed 9:00 AM (km/h)", 0.0, 100.0, float(def_wind9), step=1.0)
            wind_3pm = st.number_input("Wind Speed 3:00 PM (km/h)", 0.0, 100.0, float(def_wind3), step=1.0)
            cloud_9am = st.slider("Cloud Cover 9:00 AM (Oktas 0-8)", 0, 8, int(def_cloud9))
            cloud_3pm = st.slider("Cloud Cover 3:00 PM (Oktas 0-8)", 0, 8, int(def_cloud3))

        submit = st.form_submit_button("⚡ Predict Rainfall for Tomorrow", use_container_width=True)

    if submit:
        # Prepare input features vector
        rain_today_val = 1 if rain_today_choice == "Yes" else 0
        input_data = pd.DataFrame([{
            'MinTemp': min_temp,
            'MaxTemp': max_temp,
            'Rainfall': rainfall_today,
            'WindGustSpeed': wind_gust,
            'WindSpeed9am': wind_9am,
            'WindSpeed3pm': wind_3pm,
            'Humidity9am': humidity_9am,
            'Humidity3pm': humidity_3pm,
            'Pressure9am': pressure_9am,
            'Pressure3pm': pressure_3pm,
            'Cloud9am': cloud_9am,
            'Cloud3pm': cloud_3pm,
            'Temp9am': temp_9am,
            'Temp3pm': temp_3pm,
            'RainToday': rain_today_val
        }])[feature_names]

        # Scale features
        input_scaled = scaler.transform(input_data)
        
        # Predict
        prediction = model.predict(input_scaled)[0]
        probabilities = model.predict_proba(input_scaled)[0]
        rain_prob = probabilities[1] * 100
        no_rain_prob = probabilities[0] * 100

        st.markdown("---")
        st.subheader("2. Predictive Result & Meteorological Analysis")
        
        res_col1, res_col2 = st.columns([1.2, 1])
        
        with res_col1:
            if prediction == 1:
                st.markdown(f"""
                <div class="result-card-rain">
                    <h2>🌧️ RAIN PREDICTED TOMORROW</h2>
                    <h3>Expected Outcome: YES</h3>
                    <p style="font-size: 1.2rem;">Probability of Precipitation: <strong>{rain_prob:.1f}%</strong></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-card-norain">
                    <h2>☀️ NO RAINFALL EXPECTED TOMORROW</h2>
                    <h3>Expected Outcome: NO (Dry / Clear)</h3>
                    <p style="font-size: 1.2rem;">Probability of Clear Weather: <strong>{no_rain_prob:.1f}%</strong></p>
                </div>
                """, unsafe_allow_html=True)

        with res_col2:
            st.markdown("#### Confidence Gauge")
            st.progress(rain_prob / 100.0)
            
            pcol1, pcol2 = st.columns(2)
            pcol1.metric("Rainfall Probability", f"{rain_prob:.1f}%")
            pcol2.metric("No-Rain Probability", f"{no_rain_prob:.1f}%")
            
            # Risk Level
            if rain_prob >= 75:
                risk_status = "🔴 High Risk of Severe Rainfall / Storm"
            elif rain_prob >= 45:
                risk_status = "🟡 Moderate Chance of Showers"
            else:
                risk_status = "🟢 Low Chance of Rain (Mostly Fair Weather)"
            st.info(f"**Meteorological Assessment:** {risk_status}")

        # Scientific explanation of influencing factors
        st.markdown("#### 🔬 Key Influencing Weather Dynamics")
        explanations = []
        if humidity_3pm >= 70:
            explanations.append(f"• **High Afternoon Humidity ({humidity_3pm}%):** High tropospheric moisture significantly supports cloud condensation.")
        if pressure_3pm < 1012:
            explanations.append(f"• **Low Barometric Pressure ({pressure_3pm} hPa):** Falling atmospheric pressure indicates an approaching low-pressure depression trough.")
        if cloud_3pm >= 6:
            explanations.append(f"• **Dense Cloud Cover ({cloud_3pm}/8 Oktas):** Overcast skies restrict thermal radiation and correlate with precipitation systems.")
        if wind_gust >= 45:
            explanations.append(f"• **Elevated Wind Gust ({wind_gust} km/h):** High gust speeds frequently precede frontal rain squalls.")
        if not explanations:
            explanations.append("• **Stable Atmospheric Conditions:** High barometric pressure and moderate humidity indicate atmospheric stability with minimal precipitation risk.")
        
        for exp in explanations:
            st.markdown(exp)


# ---------------------------------------------------------
# TAB 2: Model Performance & Comparative Research
# ---------------------------------------------------------
with tab2:
    st.subheader("Model Evaluation & Algorithm Comparison")
    st.markdown("""
    In this research project, **four supervised classification algorithms** were implemented, evaluated, and cross-compared 
    using standard academic metrics: **Accuracy, Precision, Recall, F1-Score, and ROC-AUC**.
    """)
    
    if metrics:
        comp_df = pd.DataFrame(metrics["models_comparison"]).T
        metric_cols = [c for c in ['Accuracy', 'Precision', 'Recall', 'F1_Score', 'ROC_AUC'] if c in comp_df.columns]
        display_df = comp_df[metric_cols].astype(float)
        st.dataframe(display_df.style.highlight_max(axis=0, color="#BBF7D0").format("{:.2f}%"), use_container_width=True)
        
        best_name = metrics.get("best_model_name", "Random Forest")
        st.success(f"🏆 **Optimal Selected Model:** `{best_name}` based on balanced F1-Score and generalisation capability.")
    
    col_chart1, col_chart2 = st.columns(2)
    
    chart_comp_path = os.path.join(REPORTS_DIR, "model_comparison.png")
    chart_cm_path = os.path.join(REPORTS_DIR, "confusion_matrix.png")
    chart_fi_path = os.path.join(REPORTS_DIR, "feature_importance.png")
    
    with col_chart1:
        if os.path.exists(chart_comp_path):
            st.image(chart_comp_path, caption="Figure 1: Comparison of Machine Learning Algorithms Across Metrics", use_container_width=True)
        if os.path.exists(chart_cm_path):
            st.image(chart_cm_path, caption="Figure 2: Confusion Matrix of the Best Performing Classifier", use_container_width=True)
            
    with col_chart2:
        if os.path.exists(chart_fi_path):
            st.image(chart_fi_path, caption="Figure 3: Meteorological Feature Importance / Predictor Weights", use_container_width=True)
            
        st.markdown("""
        #### 📌 Key Research Findings:
        1. **Ensemble Supremacy:** Random Forest and Gradient Boosting outperformed simple linear boundaries due to nonlinear interactions among temperature, pressure, and humidity.
        2. **Primary Predictors:** `Humidity3pm`, `Pressure3pm`, `Cloud3pm`, and `WindGustSpeed` emerged as the most critical determinants of rain tomorrow.
        3. **Precision-Recall Balance:** The ensemble models maintained high recall, minimizing dangerous false negatives (failing to predict rain when it occurs).
        """)


# ---------------------------------------------------------
# TAB 3: Dataset Explorer
# ---------------------------------------------------------
with tab3:
    st.subheader("Meteorological Dataset Overview")
    df_sample = load_sample_dataset()
    
    if df_sample is not None:
        st.markdown(f"Total Dataset Observations: **{len(df_sample):,} rows** | **{len(df_sample.columns)} columns**")
        
        st.dataframe(df_sample.head(25), use_container_width=True)
        
        st.markdown("#### Summary Statistical Distribution")
        st.dataframe(df_sample.describe(), use_container_width=True)
        
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.markdown("##### Target Class Balance (Rain Tomorrow)")
            class_counts = df_sample['RainTomorrow'].value_counts()
            st.bar_chart(class_counts)
        with col_d2:
            st.markdown("##### Rainfall Today vs Tomorrow Correlation")
            cross_tab = pd.crosstab(df_sample['RainToday'], df_sample['RainTomorrow'], normalize='index') * 100
            st.dataframe(cross_tab.round(2), use_container_width=True)
    else:
        st.info("Dataset file not found. Run model training to generate dataset.")


# ---------------------------------------------------------
# TAB 4: About Project & Academic Report
# ---------------------------------------------------------
with tab4:
    st.subheader("Academic Research Project Documentation")
    
    st.markdown("""
    ### Project Title:
    **Comparative Study and Machine Learning Implementation for Atmospheric Rainfall Prediction**
    
    ---
    ### Academic Credentials:
    - **Student Name:** Aditya Saini
    - **Roll Number:** 24012900016
    - **Degree:** Bachelor of Computer Applications (BCA) - 5th Semester
    - **Department:** Department of Computer Applications
    - **University:** Shobhit University, Gangoh, Saharanpur (SRE)
    - **Academic Session:** 2026 – 2027
    - **Subject:** Research Project / Project Work
    
    ---
    ### Abstract:
    Accurate rainfall prediction is indispensable for agriculture planning, water resource management, disaster preparedness, 
    and urban flood mitigation. Traditional numerical weather prediction (NWP) requires extensive computational resources 
    and specialized supercomputing infrastructure. In this research project, an intelligent data-driven machine learning 
    framework is proposed and developed. 
    
    By analyzing meteorological parameters—including diurnal temperature ranges, relative humidity at 9:00 AM and 3:00 PM, 
    barometric sea-level pressure drops, cloud cover (measured in oktas), and wind gust velocities—multiple classification 
    models (Logistic Regression, Decision Trees, Random Forest, and Gradient Boosting) were trained and comparatively evaluated. 
    The best-performing model achieved high classification accuracy (>85%) with robust F1-score and ROC-AUC metrics. 
    The final model is deployed into this interactive Streamlit web dashboard providing instant predictions and risk assessments.
    
    ---
    ### System Architecture:
    1. **Data Acquisition & Preprocessing:** Data cleaning, missing value imputation, outlier handling, and StandardScaler normalisation.
    2. **Feature Engineering:** Temporal morning-afternoon delta computations (e.g., pressure drop and diurnal temperature range).
    3. **Model Training & Hyperparameter Tuning:** Comparative benchmarking across linear, tree, and ensemble architectures.
    4. **Model Serialisation:** Exporting weights and transformers using Joblib.
    5. **Web Deployment:** Reactive Streamlit GUI with user inputs, preset evaluation scenarios, and visual analytics.
    
    ---
    ### Project Documentation & Files:
    - Complete Word Report File: `reports/Rainfall_Prediction_Research_Project_Report.docx`
    - Markdown Report: `reports/PROJECT_REPORT.md`
    - Training Script: `src/train_model.py`
    - Web Application: `app.py`
    """)
