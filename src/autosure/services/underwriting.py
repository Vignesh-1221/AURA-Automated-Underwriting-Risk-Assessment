import pandas as pd
import numpy as np
from src.autosure.domain.schemas import InsuranceApplication
from src.autosure.rules.engine import RuleEngine
from src.autosure.interface.model_loader import ModelLoader

# CONFIG
MODEL_PATH = "models/saved/risk_model.pkl"

class UnderwritingService:
    def __init__(self):
        self.rule_engine = RuleEngine()
        # Load model via our new inference module
        self.ai_model = ModelLoader.load_model(MODEL_PATH)

    def _prepare_features(self, app: InsuranceApplication) -> pd.DataFrame:
        """Converts Domain Object to AI Model Input format."""
        age = (app.submission_date - app.dob).days // 365
        med_count = len(app.medical_conditions)
        
        data = {
            "age": [age],
            "weight_kg": [app.weight_kg],
            "height_cm": [app.height_cm],
            "annual_income": [app.annual_income],
            "total_debt": [app.total_debt],
            "credit_score": [app.credit_score if app.credit_score else 0],
            "gender": [app.gender],
            "policy_type": [app.policy_type],
            "coverage_amount": [app.coverage_amount],
            "medical_count": [med_count]
        }
        return pd.DataFrame(data)

    def evaluate_application(self, app: InsuranceApplication) -> dict:
        """
        Orchestrates the decision: Rules -> AI -> Final Verdict
        """
        # 1. Rule Engine
        rule_result = self.rule_engine.evaluate(app)
        
        if rule_result["status"] == "REJECT":
            return {
                "application_id": app.app_id,
                "status": "REJECT",
                "risk_source": "Rule Engine",
                "final_score": 100,
                "reasons": rule_result["reasons"]
            }

        # 2. AI Inference
        features = self._prepare_features(app)
        ai_risk_prob = self.ai_model.predict_proba(features)[0][1]
        ai_score = round(ai_risk_prob * 100, 2)

        # 3. Hybrid Logic
        rule_score = rule_result["rule_based_score"]
        final_risk_score = (0.4 * rule_score) + (0.6 * ai_score)
        
        decision = "ACCEPT"
        reasons = rule_result["reasons"]

        if final_risk_score > 75:
            decision = "REJECT"
            reasons.append(f"AI High Risk (Prob: {ai_score}%)")
        elif final_risk_score > 40:
            decision = "MANUAL_REVIEW"
            reasons.append(f"AI Moderate Risk (Prob: {ai_score}%)")
        else:
            reasons.append("AI Risk Assessment: Low")

        return {
            "application_id": app.app_id,
            "status": decision,
            "final_score": round(final_risk_score, 1),
            "breakdown": {"rule": rule_score, "ai": ai_score},
            "reasons": reasons
        }