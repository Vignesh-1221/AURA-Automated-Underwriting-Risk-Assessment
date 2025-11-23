from typing import List, Dict, Tuple
from src.autosure.domain.schemas import InsuranceApplication

class RuleEngine:
    """
    Deterministic rules for underwriting.
    Layer 1: Knockout Rules (Instant Reject)
    Layer 2: Risk Loading (Add percentage points to risk)
    Layer 3: Referral Rules (Manual Review needed)
    """

    def __init__(self):
        self.base_risk = 20  # Base probability of risk

    def _check_knockout_rules(self, app: InsuranceApplication) -> List[str]:
        """Returns a list of reasons for immediate rejection."""
        reasons = []
        
        # Rule 1: Age Limits (18-75)
        # --- FIXED LINE BELOW ---
        today = app.submission_date 
        # ------------------------
        
        age = (today - app.dob).days // 365
        if age < 18 or age > 75:
            reasons.append(f"Applicant age {age} is outside acceptable range (18-75).")

        # Rule 2: BMI Extremes
        if app.bmi > 40:
            reasons.append(f"BMI {app.bmi} exceeds automatic acceptance limit.")
        
        # Rule 3: Major Medical Conditions
        uninsurable_conditions = ["terminal illness", "severe heart failure"]
        for condition in app.medical_conditions:
            if condition.lower() in uninsurable_conditions:
                reasons.append(f"Uninsurable medical condition found: {condition}")

        return reasons

    def _calculate_risk_modifiers(self, app: InsuranceApplication) -> Tuple[int, List[str]]:
        """Calculates additional risk score based on rules."""
        score_increase = 0
        reasons = []

        # Smoker Penalty (+30 risk)
        if app.is_smoker:
            score_increase += 30
            reasons.append("Applicant is a smoker (+30 risk).")

        # High Debt Ratio Penalty (+15 risk)
        if app.debt_to_income_ratio > 0.60:
            score_increase += 15
            reasons.append(f"High debt-to-income ratio: {app.debt_to_income_ratio} (+15 risk).")

        # Credit Score Penalty
        if app.credit_score and app.credit_score < 600:
            score_increase += 20
            reasons.append("Low credit score (+20 risk).")
        
        return score_increase, reasons

    def evaluate(self, app: InsuranceApplication) -> Dict:
        """
        Main entry point for the Rule Engine.
        """
        # 1. Check Knockouts first
        knockouts = self._check_knockout_rules(app)
        if knockouts:
            return {
                "status": "REJECT",
                "score": 100,
                "reasons": knockouts
            }

        # 2. Calculate Risk Modifiers
        risk_mod, risk_reasons = self._calculate_risk_modifiers(app)
        
        # 3. Return Payload for the AI Model to consume later
        return {
            "status": "PROCEED", # Passed hard rules, ready for AI model
            "rule_based_score": self.base_risk + risk_mod,
            "reasons": risk_reasons
        }