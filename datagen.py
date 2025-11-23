import pandas as pd
import numpy as np
import random
import uuid
from datetime import date, timedelta

# Configuration
NUM_SAMPLES = 1000
OUTPUT_PATH = "data/raw/training_data.csv"

def generate_synthetic_data():
    print(f"🏭 Generating {NUM_SAMPLES} synthetic applications...")
    
    data = []
    
    for _ in range(NUM_SAMPLES):
        # 1. Basic Demographics
        is_male = random.choice([True, False])
        gender = "Male" if is_male else "Female"
        
        # Age distribution (weighted towards 25-50)
        age = int(np.random.triangular(18, 35, 75))
        dob = date.today() - timedelta(days=age*365)
        
        # 2. Body Metrics (Correlated with Gender)
        if gender == "Male":
            height = np.random.normal(175, 7)
            weight = np.random.normal(85, 12)
        else:
            height = np.random.normal(162, 6)
            weight = np.random.normal(70, 10)
            
        # 3. Financials (Correlated with Age)
        # Older people generally earn more
        income_base = 30000 + (age * 1000)
        annual_income = abs(np.random.normal(income_base, 15000))
        
        # Debt is often higher for middle aged (mortgages)
        debt = abs(np.random.normal(annual_income * 0.5, annual_income * 0.2))
        
        # Credit Score (Random but skewed high)
        credit_score = min(850, max(300, int(np.random.normal(700, 100))))

        # 4. Risk Factors
        # Smoker probability higher for lower income/high stress (simplified logic)
        is_smoker = np.random.choice([True, False], p=[0.15, 0.85])
        
        # Medical Conditions
        conditions = []
        if random.random() < 0.1: conditions.append("Diabetes")
        if random.random() < 0.1: conditions.append("Hypertension")
        if random.random() < 0.01: conditions.append("Severe Heart Failure") # Rare knockout
        
        # 5. The "Ground Truth" (Did they actually default/claim?)
        # This is what the AI will try to predict.
        # We simulate 'risk' based on the variables above so the model has patterns to find.
        base_risk_prob = 0.1
        if is_smoker: base_risk_prob += 0.2
        if credit_score < 600: base_risk_prob += 0.3
        if (debt / annual_income) > 0.6: base_risk_prob += 0.2
        if age > 60: base_risk_prob += 0.15
        
        # Determine label: 1 = High Risk (Reject), 0 = Low Risk (Accept)
        # We add some randomness so the model isn't perfect (real world is messy)
        actual_risk_label = 1 if random.random() < base_risk_prob else 0

        row = {
            "app_id": str(uuid.uuid4())[:8],
            "applicant_name": f"Applicant_{random.randint(1000,9999)}",
            "dob": dob,
            "gender": gender,
            "weight_kg": round(weight, 1),
            "height_cm": round(height, 1),
            "annual_income": round(annual_income, 2),
            "total_debt": round(debt, 2),
            "credit_score": credit_score,
            "is_smoker": is_smoker,
            "medical_conditions": ",".join(conditions), # Save as string for CSV
            "policy_type": random.choice(["Term", "Whole", "Universal"]),
            "coverage_amount": round(annual_income * 10, -3), # Round to nearest 1000
            "target_risk": actual_risk_label # 1 = Risky, 0 = Safe
        }
        data.append(row)

    # Save
    df = pd.DataFrame(data)
    
    # Ensure directory exists
    import os
    os.makedirs("data/raw", exist_ok=True)
    
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Data saved to {OUTPUT_PATH}")
    print(df["target_risk"].value_counts(normalize=True))

if __name__ == "__main__":
    generate_synthetic_data()