# Deployment Guide — Telco Customer Churn Prediction

## 1. Overview

This guide explains how to run and deploy the Telco Customer Churn Prediction project.

Supported modes:

- Local development
- Model training
- Flask web app
- FastAPI REST API
- Batch prediction
- Docker deployment
- Docker Compose
- GitHub Actions CI/CD

---

## 2. Prerequisites

Install:

- Python 3.10+
- pip
- Git
- Docker Desktop optional

Check versions:

- python --version
- pip --version
- git --version
- docker --version

---

## 3. Clone Repository

git clone https://github.com/your-username/customer-churn-prediction.git
cd customer-churn-prediction

---

## 4. Create Virtual Environment

Windows:

python -m venv venv
venv\Scripts\activate

Mac/Linux:

python -m venv venv
source venv/bin/activate

---

## 5. Install Dependencies

pip install -r requirements.txt
pip install -e .

---

## 6. Environment Setup

Create .env from .env.example.

Windows:

copy .env.example .env

Mac/Linux:

cp .env.example .env

Example:

APP_ENV=development
DEBUG=True
APP_HOST=127.0.0.1
APP_PORT=5000
DATA_PATH=data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv
MODEL_PATH=models/churn_model.pkl
METRICS_PATH=models/metrics.json
LOG_FILE=logs/app.log
LOG_LEVEL=INFO

Do not commit the real .env file.

---

## 7. Required Dataset

Make sure this file exists:

data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv

Without this file, training will fail.

---

## 8. Configuration

Config files:

config/
├── config.yaml
├── paths.yaml
└── logging.yaml

For local run:

api:
  host: "127.0.0.1"
  port: 5000
  debug: true

For Docker:

api:
  host: "0.0.0.0"
  port: 5000
  debug: true

---

## 9. Create Required Folders

Windows:

mkdir logs
mkdir models
mkdir artifacts
mkdir outputs
mkdir reports
mkdir data\processed

Mac/Linux:

mkdir -p logs models artifacts outputs reports data/processed

---

## 10. Train Model

Run:

python scripts/train_pipeline.py

This creates:

models/
├── best_model.pkl
├── churn_model.pkl
├── preprocessor.pkl
└── metrics.json

artifacts/
├── confusion_matrix.png
└── roc_curve.png

---

## 11. Run Flask Web App

Train the model first:

python scripts/train_pipeline.py

Run app:

python scripts/run_app.py

Open:

http://127.0.0.1:5000

---

## 12. Run FastAPI API

uvicorn app.api:app --reload

Open Swagger docs:

http://127.0.0.1:8000/docs

Health check:

curl http://127.0.0.1:8000/health

Expected response:

{
  "status": "ok"
}

---

## 13. FastAPI Prediction Example

curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "tenure": 12,
    "MonthlyCharges": 70.5,
    "TotalCharges": 846.0,
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "Yes",
    "StreamingMovies": "Yes",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check"
  }'

Example response:

{
  "status": "success",
  "data": {
    "prediction": 1,
    "churn_probability": 0.82,
    "churn_risk": "High Risk"
  }
}

---

## 14. Run Batch Prediction

python scripts/batch_predict.py data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv outputs/predictions.csv

Output:

outputs/predictions.csv

Generated columns:

- prediction
- churn_probability
- risk_level

---

## 15. Run Evaluation

python scripts/evaluate_model.py

Expected metrics:

- accuracy
- precision
- recall
- f1_score
- roc_auc
- classification report
- confusion matrix

---

## 16. Run Tests

pytest tests/ -v

Tests cover:

- Data preprocessing
- Feature engineering
- Model training
- Inference
- API endpoints

---

## 17. Docker Deployment

Docker files:

docker/
├── Dockerfile
└── docker-compose.yml

Build image:

docker build -f docker/Dockerfile -t telco-churn-app .

Run container:

docker run -p 5000:5000 telco-churn-app

Open:

http://127.0.0.1:5000

---

## 18. Docker Compose

Run:

docker compose -f docker/docker-compose.yml up --build

Stop:

docker compose -f docker/docker-compose.yml down

Open:

http://127.0.0.1:5000

---

## 19. GitHub Actions CI/CD

Workflow file:

.github/workflows/ci.yml

CI checks:

- Project structure
- Dependency installation
- Linting
- Unit tests

It runs on push or pull request.

---

## 20. Deployment Checklist

Before deployment:

[ ] Dataset exists in data/raw/
[ ] requirements.txt is complete
[ ] config.yaml has correct host and port
[ ] paths.yaml has correct paths
[ ] Model is trained
[ ] models/churn_model.pkl exists
[ ] models/preprocessor.pkl exists
[ ] models/metrics.json exists
[ ] Flask app runs
[ ] FastAPI app runs
[ ] Tests pass
[ ] Docker image builds
[ ] Docker container runs

---

## 21. Common Errors and Fixes

ModuleNotFoundError: No module named 'src'

Run from project root:

python scripts/run_app.py

Or install project:

pip install -e .
config/config.yaml not found

Run commands from the project root, not inside scripts/.

models/churn_model.pkl not found

Train the model:

python scripts/train_pipeline.py
docker command not found

Install Docker Desktop and restart terminal.

Docker app not opening

Use:

api:
  host: "0.0.0.0"
  port: 5000
  debug: true
Port already in use

Change port:

api:
  host: "127.0.0.1"
  port: 5050
  debug: true

Open:

http://127.0.0.1:5050

---

## 22. Production Notes

For real production:

- Disable debug mode
- Use Gunicorn or Uvicorn workers
- Add authentication
- Add HTTPS
- Add monitoring
- Add model versioning
- Add data drift detection
- Store models in cloud storage
- Use a database instead of CSV
- Add scheduled retraining

Production Flask command:

gunicorn app.web_app:app --bind 0.0.0.0:5000

Production FastAPI command:

uvicorn app.api:app --host 0.0.0.0 --port 8000

---

## 23. Quick Commands

- Install:

pip install -r requirements.txt
pip install -e .

- Train:

python scripts/train_pipeline.py

- Run Flask:

python scripts/run_app.py

- Run FastAPI:

uvicorn app.api:app --reload

- Batch predict:

python scripts/batch_predict.py data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv outputs/predictions.csv

- Test:

pytest tests/ -v

- Docker build:

docker build -f docker/Dockerfile -t telco-churn-app .

- Docker run:

docker run -p 5000:5000 telco-churn-app

- Docker Compose:

docker compose -f docker/docker-compose.yml up --build

---

## 24. Summary

This project supports:

- Local development
- Model training
- Flask web app
- FastAPI API
- Batch prediction
- Docker deployment
- Docker Compose
- CI/CD validation