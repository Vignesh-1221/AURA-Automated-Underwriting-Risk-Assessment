from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal
from datetime import date

# 1. ENUMS (Standardizing inputs)
GenderType = Literal['Male', 'Female', 'Other']
PolicyType = Literal['Term', 'Whole', 'Universal']

# 2. APPLICATION SCHEMA (The Input)
class InsuranceApplication(BaseModel):
    app_id: str = Field(..., description="Unique UUID for application")
    applicant_name: str
    dob: date
    gender: GenderType
    weight_kg: float = Field(..., gt=20, lt=300, description="Weight in KG")
    height_cm: float = Field(..., gt=50, lt=250, description="Height in CM")
    submission_date: date = Field(default_factory=date.today)
    # Financials
    annual_income: float = Field(..., gt=0)
    total_debt: float = Field(default=0.0)
    credit_score: Optional[int] = Field(None, ge=300, le=850)
    
    # Risk Factors
    is_smoker: bool
    medical_conditions: List[str] = [] # e.g. ["diabetes", "hypertension"]
    
    # Policy Request
    policy_type: PolicyType
    coverage_amount: float = Field(..., gt=1000)

    # COMPUTED PROPERTIES (Business Logic Helper)
    @property
    def bmi(self) -> float:
        height_m = self.height_cm / 100
        return round(self.weight_kg / (height_m ** 2), 2)
    
    @property
    def debt_to_income_ratio(self) -> float:
        if self.annual_income == 0: return 0.0
        return round(self.total_debt / self.annual_income, 2)

    # VALIDATION (Solves "Conflicting Info")
    @validator("coverage_amount")
    def check_coverage_limit(cls, v, values):
        # Example: Prevent someone with $10k income asking for $10M coverage
        income = values.get("annual_income", 0)
        if income > 0 and v > (income * 50): 
            raise ValueError(f"Coverage {v} exceeds 50x income limit.")
        return v

# 3. DECISION SCHEMA (The Output)
class UnderwritingDecision(BaseModel):
    application_id: str
    decision: Literal['ACCEPT', 'REJECT', 'MANUAL_REVIEW']
    risk_score: float = Field(..., ge=0, le=100)
    reasons: List[str] = []
    timestamp: date = Field(default_factory=date.today)