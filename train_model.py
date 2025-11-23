import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
from datetime import date

# CONFIG
DATA_PATH = "data/raw/training_data.csv"
MODEL_PATH = "models/saved/risk_model.pkl"

def load_and_prep_data():
    """
    Loads CSV and performs feature engineering that MUST happen before the pipeline.
    """
    print("⏳ Loading data...")
    df = pd.read_csv(DATA_PATH)
    
    # 1. Feature Engineering: Convert DOB to Age
    # (The model doesn't understand dates, it understands numbers)
    df['dob'] = pd.to_datetime(df['dob'])
    df['age'] = (pd.Timestamp.now() - df['dob']).dt.days // 365
    
    # 2. Feature Engineering: Count Medical Conditions
    # We treat an empty string as 0 conditions
    df['medical_count'] = df['medical_conditions'].fillna("").apply(lambda x: len(x.split(",")) if x else 0)
    
    # 3. Drop columns we don't need for training
    # (app_id is random noise, DOB is replaced by age, target_risk is label)
    X = df.drop(columns=["app_id", "applicant_name", "dob", "medical_conditions", "target_risk"])
    y = df["target_risk"]
    
    return train_test_split(X, y, test_size=0.2, random_state=42)

def build_pipeline():
    """
    Creates a robust ML pipeline.
    """
    # 1. Define which columns are Numbers and which are Categories
    numeric_features = ["age", "weight_kg", "height_cm", "annual_income", "total_debt", "credit_score", "coverage_amount", "medical_count"]
    categorical_features = ["gender", "policy_type"] # We handle boolean 'is_smoker' as numeric/bool automatically usually
    
    # 2. Create Transformers
    # StandardScaler: Makes income (30000) and age (50) comparable
    numeric_transformer = StandardScaler()
    
    # OneHotEncoder: Converts "Male/Female" to [0, 1] vectors
    categorical_transformer = OneHotEncoder(handle_unknown="ignore")
    
    # 3. Combine them
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )
    
    # 4. Create the Full Pipeline (Preprocessor + Classifier)
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    return pipeline

if __name__ == "__main__":
    # A. Load
    X_train, X_test, y_train, y_test = load_and_prep_data()
    
    # B. Build
    model_pipeline = build_pipeline()
    
    # C. Train
    print("🧠 Training Random Forest Model...")
    model_pipeline.fit(X_train, y_train)
    
    # D. Evaluate
    print("📉 Evaluating...")
    preds = model_pipeline.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, preds):.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, preds))
    
    # E. Save
    # We save the WHOLE pipeline, not just the model.
    # This means we don't have to manually normalize data in production!
    import os
    os.makedirs("models/saved", exist_ok=True)
    joblib.dump(model_pipeline, MODEL_PATH)
    print(f"✅ Model saved to {MODEL_PATH}")