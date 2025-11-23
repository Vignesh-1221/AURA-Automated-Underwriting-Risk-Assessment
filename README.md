AURA: Automated Underwriting & Risk Assessment

AURA (Automated Underwriting & Risk Assessment) is an intelligent decision-support platform designed to modernize and streamline insurance underwriting. It combines deterministic business rules with probabilistic machine learning to deliver transparent, fair, and regulation-compliant decisions.

AURA uses a Hybrid Decision Architecture, blending:

Deterministic Business Rules – for strict regulatory compliance and sanity checks

Probabilistic Machine Learning – for identifying non-linear risk patterns such as DTI ratios and lifestyle correlations

This ensures explainability without sacrificing predictive performance.

📋 Executive Summary

AURA is not a “black box” AI. It is built around interpretability, auditability, and modular design. The system evaluates insurance applications and returns:

ACCEPT

REJECT

MANUAL_REVIEW

Each decision is paired with explainability metadata so underwriters understand why the decision was made.

🚀 Key Features
🔹 Hybrid Intelligence Engine

A weighted decision model blending:

40% Business Rules

60% AI Model Output

Ensures responsible and balanced underwriting decisions.

🔹 Real-Time Dashboard

A responsive SPA user interface for visualizing:

Risk profiles

Feature contributions

Decision breakdowns

🔹 Microservices Architecture

Built using a clean, modular FastAPI-based SOA.

🔹 Fail-Safe Compliance

Knockout rules automatically reject:

Out-of-age applicants

High BMI

Medical exclusions

Fraud flags

🔹 Explainable AI (XAI)

Each decision includes a transparent reasoning summary:

Rule contribution

ML probability

Risk factors

📂 Project Structure
AURA/
├── data/                   # Synthetic training data storage
├── frontend/               # User Interface
│   └── index.html          # AURA Dashboard (HTML/Tailwind)
├── models/                 # Serialized ML models
│   └── saved/
│       └── risk_model.pkl  # Trained Random Forest Pipeline
├── src/
│   └── autosure/           # Core Application Logic
│       ├── domain/         # Pydantic Schemas (Data Contracts)
│       ├── inference/      # ML Model Loading & Prediction
│       ├── interface/      # FastAPI Routes & Endpoints
│       ├── rules/          # Deterministic Compliance Logic
│       └── services/       # Business Logic Orchestration
├── tests/                  # Unit & Integration Tests
├── datagen.py              # Synthetic Data Generator
├── train_model.py          # ML Training Pipeline
├── run.py                  # Application Entry Point
└── requirements.txt        # Dependencies

🛠️ Installation & Setup
Prerequisites

Python 3.9+

pip package manager

1. Install Dependencies
pip install -r requirements.txt

2. Initialize the System
Generate synthetic dataset:
python datagen.py

Train and save the ML model:
python train_model.py

3. Launch the Backend
python run.py


API will be available at:

http://127.0.0.1:8000

4. Open the Dashboard

Open:

frontend/index.html


in any modern browser to use the AURA Underwriting Dashboard.

🧠 Architecture & Decision Logic

AURA follows a linear processing pipeline:

1. Ingestion

Data received via REST API

Validated using Pydantic schemas

2. Rule-Based Layer (40%)

Performs:

Age validation (18–75)

BMI checks

Medical knockout flags

Compliance checks

If a knockout triggers → immediate rejection.

3. AI Layer (60%)

A Random Forest Classifier outputs:

Risk probability score (0–100%)

4. Decision Synthesis
Final Score = (Rule Score * 0.4) + (AI Score * 0.6)

Risk Thresholds
Score Range	Decision	Action
0 – 40	ACCEPT	Auto-approve
41 – 75	MANUAL_REVIEW	Human underwriter review needed
76 – 100	REJECT	Decline application
🔌 API Documentation

Swagger UI:

http://127.0.0.1:8000/docs


Redoc:

http://127.0.0.1:8000/redoc

🧪 Testing

Run all tests:

pytest tests/
