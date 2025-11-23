# AURA: Automated Underwriting & Risk Assessment

AURA (Automated Underwriting & Risk Assessment) is an intelligent
decision-support platform designed to modernize and streamline insurance
underwriting. It combines deterministic business rules with
probabilistic machine learning to deliver transparent, fair, and
regulation-compliant decisions.

AURA uses a Hybrid Decision Architecture, blending:

-   Deterministic Business Rules -- for strict regulatory compliance and
    sanity checks\
-   Probabilistic Machine Learning -- for identifying non-linear risk
    patterns such as DTI ratios and lifestyle correlations

This ensures explainability without sacrificing predictive performance.

## Executive Summary

AURA is built around interpretability, auditability, and modular design.
The system evaluates insurance applications and returns:

-   ACCEPT
-   REJECT
-   MANUAL_REVIEW

Each decision is paired with explainability metadata so underwriters
understand why the decision was made.

## Key Features

### Hybrid Intelligence Engine

A weighted decision model blending: - 40% Business Rules - 60% AI Model
Output

### Real-Time Dashboard

A responsive SPA user interface.

### Microservices Architecture

FastAPI-based SOA.

### Fail-Safe Compliance

Automatic knockout rules.

### Explainable AI

Transparent reasoning metadata.

## Project Structure

    AURA/
    ├── data/
    ├── frontend/
    │   └── index.html
    ├── models/
    │   └── saved/
    │       └── risk_model.pkl
    ├── src/
    │   └── autosure/
    │       ├── domain/
    │       ├── inference/
    │       ├── interface/
    │       ├── rules/
    │       └── services/
    ├── tests/
    ├── datagen.py
    ├── train_model.py
    ├── run.py
    └── requirements.txt

## Installation & Setup

### 1. Install Dependencies

    pip install -r requirements.txt

### 2. Initialize System

    python datagen.py
    python train_model.py

### 3. Launch Backend

    python run.py

### 4. Open Dashboard

Open frontend/index.html.

## Architecture & Decision Logic

### Rule Layer (40%)

Compliance rules and knockout logic.

### AI Layer (60%)

Random Forest classifier.

### Decision Synthesis

Final Score = (Rule Score \* 0.4) + (AI Score \* 0.6)

### Risk Thresholds

  Score    Decision        Action
  -------- --------------- --------------
  0-40     ACCEPT          Auto-approve
  41-75    MANUAL_REVIEW   Human review
  76-100   REJECT          Decline

## API Docs

-   /docs (Swagger UI)
-   /redoc (Redoc)
