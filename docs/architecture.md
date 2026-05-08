# Architecture — Customer Churn Prediction System

## 1. Project Overview

The Customer Churn Prediction System is an end-to-end machine learning project designed to predict whether a telecom customer is likely to leave the company.

It includes:

- Data loading
- Data validation
- Data preprocessing
- Feature engineering
- Model training
- Model evaluation
- Model artifact generation
- Flask web application
- FastAPI REST API
- Batch prediction
- Testing
- Logging
- Docker support
- CI/CD with GitHub Actions

The goal is to show practical data science, machine learning engineering, and deployment skills.

---

## 2. Business Problem

Customer churn is a major business problem in the telecom industry. When a customer leaves, the company loses recurring revenue and may need to spend additional money to acquire a replacement customer.

This project helps the business identify customers who are likely to churn so that retention teams can take proactive actions.

Examples of retention actions:

- Offer loyalty discounts
- Improve customer support
- Promote long-term contracts
- Provide service upgrades
- Target high-risk customers with retention campaigns

---

## 3. System Objective

The system predicts:

- Whether a customer will churn
- The probability of churn
- The customer risk level

Example output:


{
  "prediction": 1,
  "churn_probability": 0.82,
  "churn_risk": "High Risk"
}

---

## 4. High-Level Architecture

Raw Telco Dataset
        ↓
Data Loading
        ↓
Data Validation
        ↓
Data Preprocessing
        ↓
Feature Engineering
        ↓
Train/Test Split
        ↓
Model Training
        ↓
Model Evaluation
        ↓
Best Model Selection
        ↓
Model Artifacts
        ↓
Inference Pipeline
        ↓
Flask Web App / FastAPI API / Batch Prediction
        ↓
Business Decision

---

## 5. Repository Structure

customer-churn-prediction/
│
├── README.md
├── requirements.txt
├── setup.py
├── .gitignore
├── .env.example
│
├── data/
│   ├── raw/
│   │   └── WA_Fn-UseC_-Telco-Customer-Churn.csv
│   ├── processed/
│   │   ├── train.csv
│   │   ├── test.csv
│   │   └── validation.csv
│   └── data_dictionary.md
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_experiments.ipynb
│
├── outputs/
│   └── predictions.csv
│
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   ├── inference/
│   └── utils/
│
├── models/
│   ├── best_model.pkl
│   ├── churn_model.pkl
│   ├── preprocessor.pkl
│   └── metrics.json
│
├── app/
│   ├── web_app.py
│   ├── api.py
│   ├── templates/
│   └── static/
│
├── config/
│   ├── config.yaml
│   ├── paths.yaml
│   └── logging.yaml
│
├── scripts/
│   ├── split_data.py
│   ├── train_pipeline.py
│   ├── evaluate_model.py
│   ├── run_app.py
│   └── batch_predict.py
│
├── tests/
├── docs/
├── logs/
├── artifacts/
├── docker/
└── .github/

---

## 6. Main Components

### 6.1 Data Layer

Location:

src/data/

Files:

- data_loader.py
- data_preprocessing.py
- data_validation.py

Responsibilities:

- Load raw CSV data
- Validate required columns
- Check missing values
- Convert data types
- Clean the dataset
- Prepare data for feature engineering

Important preprocessing steps:

- Drop customerID
- Convert TotalCharges to numeric
- Convert Churn into binary format
- Handle missing values

### 6.2 Feature Engineering Layer

Location:

src/features/

Files:

- feature_engineering.py
- feature_selection.py

Responsibilities:

- Create useful business-driven features
- Build preprocessing pipeline
- Encode categorical variables
- Scale numerical variables
- Support feature selection

Possible engineered features:

| Feature              | Purpose                      |
| -------------------- | ---------------------------- |
| `AvgChargesPerMonth` | Captures spending behavior   |
| `TenureGroup`        | Captures customer lifecycle  |
| `TotalServices`      | Captures customer engagement |

### 6.3 Model Layer

Location:

src/models/

Files:

- model_training.py
- model_evaluation.py
- model_registry.py
- hyperparameter_tuning.py

Responsibilities:

- Train machine learning models
- Evaluate model performance
- Compare different algorithms
- Save trained artifacts
- Track metrics
- Support future model versioning

Models used:

- Logistic Regression
- Random Forest Classifier
- Gradient Boosting Classifier

### 6.4 Inference Layer

Location:

src/inference/

Files:

- model_inference.py
- predict_pipeline.py

Responsibilities:

- Load trained model
- Accept input data
- Run prediction
- Generate churn probability
- Return business-friendly output

### 6.5 Application Layer

Location:

app/

Files:

- web_app.py
- api.py
- templates/index.html
- static/css/style.css
- static/js/main.js

Responsibilities:

- Provide Flask web interface
- Provide FastAPI REST API
- Accept customer inputs
- Display or return churn predictions

### 6.6 Configuration Layer

Location:

config/

Files:

- config.yaml
- paths.yaml
- logging.yaml

Responsibilities:

- Store model parameters
- Store feature lists
- Store data paths
- Store artifact paths
- Store API settings
- Store logging settings

This avoids hardcoding and improves maintainability.

---

## 7. Training Pipeline Flow

Main script:

scripts/train_pipeline.py

Run command:

python scripts/train_pipeline.py

Training flow:

- Load config
- Load dataset
- Clean data
- Prepare X and y
- Split train/test data
- Build preprocessing pipeline
- Train candidate models
- Evaluate each model
- Select best model using ROC-AUC
- Save churn_model.pkl
- Save best_model.pkl
- Save preprocessor.pkl
- Save metrics.json
- Save visual artifacts

---

## 8. Model Artifacts

Generated files:

models/
├── best_model.pkl
├── churn_model.pkl
├── preprocessor.pkl
└── metrics.json
churn_model.pkl

Contains the complete pipeline:

#### Preprocessing + Trained model

This is used for inference.

#### best_model.pkl

Stores a copy of the selected best model.

#### preprocessor.pkl

Stores preprocessing separately for debugging and inspection.

#### metrics.json

Stores model comparison results and performance metrics.

---

## 9. Visual Artifacts

Generated files:

artifacts/
├── confusion_matrix.png
└── roc_curve.png

### confusion_matrix.png

Shows correct and incorrect churn predictions.

### roc_curve.png

Shows model classification ability across thresholds.

---

## 10. API and Web App Flow

User / Client
     ↓
Flask Web App or FastAPI API
     ↓
Prediction Pipeline
     ↓
Model Inference
     ↓
churn_model.pkl
     ↓
Prediction + Probability + Risk Level

---

## - 11. Batch Prediction Flow

Main script:

scripts/batch_predict.py

Run command:

python scripts/batch_predict.py data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv outputs/predictions.csv

Flow:

Input CSV
   ↓
Load model
   ↓
Generate predictions
   ↓
Add prediction columns
   ↓
Save outputs/predictions.csv

Output columns:

- prediction
- churn_probability
- risk_level

---

## 12. Testing Architecture

Location:

tests/

Test files:

- test_data_preprocessing.py
- test_feature_engineering.py
- test_model_training.py
- test_inference.py
- test_api.py

Run:

pytest tests/ -v

Tests cover:

- Data preprocessing
- Feature engineering
- Model training
- Inference
- API endpoints

---

## 13. Docker Architecture

Docker files:

docker/
├── Dockerfile
└── docker-compose.yml

Docker provides a reproducible environment for running the project.

Run:

docker compose -f docker/docker-compose.yml up --build

---

## 14. CI/CD Architecture

CI workflow:

.github/workflows/ci.yml

GitHub Actions checks:

- Project structure
- Dependency installation
- Code linting
- Unit tests

This improves reliability and shows production readiness.

---

## 15. Key Design Decisions

- Why use sklearn Pipeline?

The pipeline keeps preprocessing and model training together, preventing training-serving mismatch.

- Why use ROC-AUC?

Churn is usually imbalanced. ROC-AUC evaluates how well the model separates churners from non-churners.

- Why use recall as a business priority?

Missing an actual churn customer can lead to revenue loss. Recall helps identify more churn customers.

- Why save both full model and preprocessor?

The full pipeline is used for prediction. The separate preprocessor helps with debugging, feature inspection, and future experiments.

---

## 16. Summary

This architecture demonstrates a complete machine learning system with:

- Modular source code
- Config-driven design
- Reusable training pipeline
- Saved model artifacts
- Web app and API serving
- Batch prediction
- Testing
- Logging
- Docker support
- CI/CD automation