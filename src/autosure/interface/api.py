from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.autosure.domain.schemas import InsuranceApplication
from src.autosure.services.underwriting import UnderwritingService

app = FastAPI(title="AutoSure Underwriting API", version="1.0")

# --- ADD THIS BLOCK ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for demo purposes)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],
)
# ----------------------

# Initialize Service once on startup
service = UnderwritingService()

@app.get("/")
def health_check():
    return {"status": "active", "system": "AutoSure v1"}

@app.post("/predict")
def predict_risk(application: InsuranceApplication):
    """
    Endpoint to process new insurance applications.
    """
    try:
        result = service.evaluate_application(application)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))