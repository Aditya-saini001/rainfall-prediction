"""
Rainfall Prediction - Machine Learning Training Pipeline
Author: Aditya Saini (Roll No: 24012900016)
Institution: Shobhit University, Gangoh, Saharanpur
Project: Research Project (BCA 5th Semester)
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
import joblib

# Set random seed for reproducibility
np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)


def generate_meteorological_dataset(n_samples=6000):
    """
    Generates a realistic meteorological dataset based on physical weather dynamics
    simulating observations of daily weather patterns.
    """
    print(f"Generating meteorological dataset with {n_samples} records...")
    
    # 1. Temperature cycles
    min_temp = np.random.normal(12.5, 6.0, n_samples)
    min_temp = np.clip(min_temp, -2.0, 30.0)
    
    # Max temp is correlated with min_temp + diurnal temperature variation
    diurnal_range = np.random.uniform(6.0, 16.0, n_samples)
    max_temp = min_temp + diurnal_range
    
    # Temp 9am & 3pm
    temp_9am = min_temp + diurnal_range * np.random.uniform(0.2, 0.45, n_samples)
    temp_3pm = min_temp + diurnal_range * np.random.uniform(0.7, 0.95, n_samples)
    
    # 2. Atmospheric Pressure (Standard sea-level: ~1013 hPa)
    pressure_9am = np.random.normal(1017.5, 7.0, n_samples)
    pressure_drop = np.random.normal(2.5, 1.8, n_samples)
    pressure_3pm = pressure_9am - pressure_drop
    
    # 3. Wind measurements
    wind_gust_speed = np.random.gamma(shape=4.0, scale=10.0, size=n_samples)
    wind_gust_speed = np.clip(wind_gust_speed, 10.0, 110.0)
    wind_speed_9am = wind_gust_speed * np.random.uniform(0.25, 0.55, n_samples)
    wind_speed_3pm = wind_gust_speed * np.random.uniform(0.40, 0.75, n_samples)
    
    # 4. Cloud Cover (0 to 8 oktas)
    cloud_9am = np.random.randint(0, 9, n_samples)
    cloud_3pm = np.clip(cloud_9am + np.random.choice([-1, 0, 1, 2], n_samples), 0, 8)
    
    # 5. Humidity (%)
    # Humidity strongly correlates with low pressure and cloud cover
    humidity_9am = 65.0 + (cloud_9am * 3.5) - ((pressure_9am - 1013.0) * 1.5) + np.random.normal(0, 8, n_samples)
    humidity_9am = np.clip(humidity_9am, 15.0, 100.0)
    
    humidity_3pm = humidity_9am - (diurnal_range * 1.5) + (cloud_3pm * 2.8) + np.random.normal(0, 7, n_samples)
    humidity_3pm = np.clip(humidity_3pm, 10.0, 100.0)
    
    # 6. Rainfall Today (0 or positive mm)
    rain_today_prob = 1 / (1 + np.exp(-( (humidity_9am - 70)/15 + (cloud_9am - 5)/2 - (pressure_9am - 1012)/8 )))
    rain_today = (np.random.rand(n_samples) < rain_today_prob).astype(int)
    rainfall_amount = np.where(rain_today == 1, np.random.exponential(scale=7.5, size=n_samples), 0.0)
    rainfall_amount = np.round(rainfall_amount, 1)
    
    # 7. Physical Probability of Rain Tomorrow
    # Meteorological factors favoring rain tomorrow:
    # - High afternoon humidity (Humidity3pm)
    # - Dropping atmospheric pressure (Pressure3pm < 1010)
    # - High cloud cover in the afternoon (Cloud3pm)
    # - High wind gust speed (front approach)
    # - Prior rainfall today
    z = (
        0.055 * (humidity_3pm - 50) +
        0.025 * (humidity_9am - 60) -
        0.090 * (pressure_3pm - 1012.0) +
        0.035 * (wind_gust_speed - 35) +
        0.300 * (cloud_3pm - 4) +
        0.650 * rain_today -
        0.030 * (max_temp - 24) -
        1.2
    )
    rain_tomorrow_prob = 1 / (1 + np.exp(-z))
    rain_tomorrow = (np.random.rand(n_samples) < rain_tomorrow_prob).astype(int)
    
    data = pd.DataFrame({
        'MinTemp': np.round(min_temp, 1),
        'MaxTemp': np.round(max_temp, 1),
        'Rainfall': rainfall_amount,
        'WindGustSpeed': np.round(wind_gust_speed, 1),
        'WindSpeed9am': np.round(wind_speed_9am, 1),
        'WindSpeed3pm': np.round(wind_speed_3pm, 1),
        'Humidity9am': np.round(humidity_9am, 1),
        'Humidity3pm': np.round(humidity_3pm, 1),
        'Pressure9am': np.round(pressure_9am, 1),
        'Pressure3pm': np.round(pressure_3pm, 1),
        'Cloud9am': cloud_9am,
        'Cloud3pm': cloud_3pm,
        'Temp9am': np.round(temp_9am, 1),
        'Temp3pm': np.round(temp_3pm, 1),
        'RainToday': rain_today,
        'RainTomorrow': rain_tomorrow
    })
    
    csv_path = os.path.join(DATA_DIR, "weather_rainfall_dataset.csv")
    data.to_csv(csv_path, index=False)
    print(f"Dataset successfully saved to: {csv_path}")
    print(f"Class Distribution: {data['RainTomorrow'].value_counts().to_dict()}")
    return data


def train_and_evaluate_models():
    # Load dataset
    csv_path = os.path.join(DATA_DIR, "weather_rainfall_dataset.csv")
    if not os.path.exists(csv_path):
        df = generate_meteorological_dataset()
    else:
        df = pd.read_csv(csv_path)

    feature_cols = [
        'MinTemp', 'MaxTemp', 'Rainfall', 'WindGustSpeed',
        'WindSpeed9am', 'WindSpeed3pm', 'Humidity9am', 'Humidity3pm',
        'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm',
        'Temp9am', 'Temp3pm', 'RainToday'
    ]
    target_col = 'RainTomorrow'
    
    X = df[feature_cols]
    y = df[target_col]
    
    # Train test split (80% training, 20% testing)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    
    # Feature Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Define candidate models
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=8, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=150, max_depth=12, random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=120, learning_rate=0.08, max_depth=5, random_state=42)
    }
    
    results = {}
    fitted_models = {}
    
    print("\n" + "="*50)
    print("TRAINING AND EVALUATING CLASSIFICATION MODELS")
    print("="*50)
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train_scaled, y_train)
        fitted_models[name] = model
        
        y_pred = model.predict(X_test_scaled)
        y_prob = model.predict_proba(X_test_scaled)[:, 1] if hasattr(model, "predict_proba") else y_pred
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        auc = roc_auc_score(y_test, y_prob)
        cm = confusion_matrix(y_test, y_pred).tolist()
        
        results[name] = {
            "Accuracy": round(float(acc) * 100, 2),
            "Precision": round(float(prec) * 100, 2),
            "Recall": round(float(rec) * 100, 2),
            "F1_Score": round(float(f1) * 100, 2),
            "ROC_AUC": round(float(auc) * 100, 2),
            "Confusion_Matrix": cm
        }
        
        print(f"-> Accuracy: {acc*100:.2f}% | Precision: {prec*100:.2f}% | Recall: {rec*100:.2f}% | F1: {f1*100:.2f}% | ROC-AUC: {auc*100:.2f}%")

    # Select best model based on F1-Score and Accuracy
    best_name = max(results, key=lambda k: (results[k]["Accuracy"] + results[k]["F1_Score"])/2)
    best_model = fitted_models[best_name]
    print(f"\n>>> Best Performing Model: {best_name} with Accuracy {results[best_name]['Accuracy']}% <<<")
    
    # Save Model, Scaler, and Metrics
    joblib.dump(best_model, os.path.join(MODELS_DIR, "best_rainfall_model.pkl"))
    joblib.dump(scaler, os.path.join(MODELS_DIR, "scaler.pkl"))
    joblib.dump(feature_cols, os.path.join(MODELS_DIR, "feature_names.pkl"))
    
    metrics_file = os.path.join(MODELS_DIR, "evaluation_metrics.json")
    with open(metrics_file, "w") as f:
        json.dump({
            "best_model_name": best_name,
            "feature_columns": feature_cols,
            "models_comparison": results
        }, f, indent=4)
    print(f"Model and artifacts successfully serialized in: {MODELS_DIR}")
    
    # Generate Visualizations for Report and App
    generate_visualizations(results, best_model, feature_cols, X_test_scaled, y_test, best_name, fitted_models)


def generate_visualizations(results, best_model, feature_cols, X_test_scaled, y_test, best_name, fitted_models=None):
    print("\nGenerating charts and visualizations...")
    sns.set_theme(style="whitegrid")
    
    # 1. Model Comparison Chart
    df_results = pd.DataFrame(results).T.reset_index().rename(columns={'index': 'Model'})
    metrics_to_plot = ['Accuracy', 'Precision', 'Recall', 'F1_Score', 'ROC_AUC']
    df_melted = pd.melt(df_results, id_vars=['Model'], value_vars=metrics_to_plot, var_name='Metric', value_name='Score (%)')
    
    plt.figure(figsize=(10, 5.5))
    bar_plot = sns.barplot(data=df_melted, x='Model', y='Score (%)', hue='Metric', palette='viridis')
    plt.title("Comparative Performance of Machine Learning Algorithms", fontsize=14, weight='bold', pad=15)
    plt.ylim(50, 105)
    plt.ylabel("Score (%)", fontsize=11)
    plt.xlabel("Classification Models", fontsize=11)
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    chart_path = os.path.join(REPORTS_DIR, "model_comparison.png")
    plt.savefig(chart_path, dpi=300)
    plt.close()
    print(f"Saved: {chart_path}")
    
    # 2. Confusion Matrix for Best Model
    y_pred = best_model.predict(X_test_scaled)
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
                xticklabels=['No Rain (0)', 'Rain (1)'],
                yticklabels=['No Rain (0)', 'Rain (1)'])
    plt.title(f"Confusion Matrix - {best_name}", fontsize=13, weight='bold', pad=12)
    plt.xlabel("Predicted Class", fontsize=11)
    plt.ylabel("Actual True Class", fontsize=11)
    plt.tight_layout()
    cm_path = os.path.join(REPORTS_DIR, "confusion_matrix.png")
    plt.savefig(cm_path, dpi=300)
    plt.close()
    print(f"Saved: {cm_path}")
    
    # 3. Feature Importance Plot (using Random Forest / Tree importances or Linear weights)
    rf_model = fitted_models.get("Random Forest", best_model)
    if hasattr(rf_model, "feature_importances_"):
        importances = rf_model.feature_importances_
        title_label = "Random Forest Feature Importances"
    elif hasattr(best_model, "coef_"):
        importances = np.abs(best_model.coef_[0])
        importances = importances / np.sum(importances)
        title_label = "Logistic Regression Feature Weights"
    else:
        importances = np.ones(len(feature_cols)) / len(feature_cols)
        title_label = "Meteorological Predictor Weights"

    feat_df = pd.DataFrame({'Feature': feature_cols, 'Importance': importances}).sort_values('Importance', ascending=False)
    
    plt.figure(figsize=(9, 5.5))
    sns.barplot(data=feat_df, x='Importance', y='Feature', palette='mako')
    plt.title(f"Top Meteorological Predictors ({title_label})", fontsize=13, weight='bold', pad=12)
    plt.xlabel("Relative Importance Weight", fontsize=11)
    plt.tight_layout()
    feat_path = os.path.join(REPORTS_DIR, "feature_importance.png")
    plt.savefig(feat_path, dpi=300)
    plt.close()
    print(f"Saved: {feat_path}")


if __name__ == "__main__":
    train_and_evaluate_models()
