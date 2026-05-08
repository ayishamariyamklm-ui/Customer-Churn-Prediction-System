# API Documentation — Customer Churn Prediction

## 1. Overview

This document explains how to use the API layer of the Telco Customer Churn Prediction System.

The project supports two interfaces:

1. Flask Web App  
2. FastAPI REST API  

Both interfaces use the same prediction pipeline and trained model.

---

## 2. API Files


app/
├── web_app.py
├── api.py
├── templates/index.html
└── static/
    ├── css/style.css
    └── js/main.js

Prediction logic:

src/inference/
├── model_inference.py
└── predict_pipeline.py

Model artifact:

models/churn_model.pkl

---

## 3. API Architecture

Client / Browser
      ↓
Flask or FastAPI
      ↓
Prediction Pipeline
      ↓
Model Inference
      ↓
churn_model.pkl
      ↓
Prediction Response

---

## 4. Flask Web App

File:

app/web_app.py

Run:

python scripts/run_app.py

Open:

http://127.0.0.1:5000

If configured for port 8000:

http://127.0.0.1:8000

---

## 5. Flask Routes

| Route          | Method | Description              |
| -------------- | ------ | ------------------------ |
| `/`            | GET    | Loads prediction form    |
| `/predict`     | POST   | Handles form prediction  |
| `/api/predict` | POST   | JSON prediction endpoint |
| `/health`      | GET    | Health check             |

---

## 6. Flask Health Check

Endpoint:

GET /health

Response:

{
  "status": "ok"
}

---

## 7. Flask JSON Prediction

Endpoint:

POST /api/predict

Headers:

Content-Type: application/json

Example request:

{
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
}

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

## 8. FastAPI REST API

File:

app/api.py

Run:

uvicorn app.api:app --reload

Open API:

http://127.0.0.1:8000

Swagger docs:

http://127.0.0.1:8000/docs

ReDoc:

http://127.0.0.1:8000/redoc

---

## 9. FastAPI Endpoints

| Endpoint         | Method | Description                  |
| ---------------- | ------ | ---------------------------- |
| `/`              | GET    | API status                   |
| `/health`        | GET    | Health check                 |
| `/predict`       | POST   | Single customer prediction   |
| `/predict_batch` | POST   | Multiple customer prediction |

---

## 10. Root Endpoint

Endpoint:

GET /

Response:

{
  "message": "Customer Churn Prediction API is running",
  "status": "success"
}

----

## 11. Health Endpoint

Endpoint:

GET /health

Response:

{
  "status": "ok"
}

---

## 12. Single Prediction Endpoint

Endpoint:

POST /predict

Headers:

Content-Type: application/json

Example request:

{
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
}

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

## 13. Batch Prediction Endpoint

Endpoint:

POST /predict_batch

Example request:

[
  {
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
  },
  {
    "tenure": 36,
    "MonthlyCharges": 45.0,
    "TotalCharges": 1620.0,
    "gender": "Male",
    "SeniorCitizen": 0,
    "Partner": "No",
    "Dependents": "No",
    "PhoneService": "Yes",
    "MultipleLines": "Yes",
    "InternetService": "DSL",
    "OnlineSecurity": "Yes",
    "OnlineBackup": "Yes",
    "DeviceProtection": "Yes",
    "TechSupport": "Yes",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "Two year",
    "PaperlessBilling": "No",
    "PaymentMethod": "Credit card (automatic)"
  }
]

Example response:

{
  "status": "success",
  "count": 2,
  "data": [
    {
      "prediction": 1,
      "churn_probability": 0.82,
      "churn_risk": "High Risk"
    },
    {
      "prediction": 0,
      "churn_probability": 0.18,
      "churn_risk": "Low Risk"
    }
  ]
}

---

## 14. Input Fields

Expected complete input fields:

| Field              | Type    | Example            |
| ------------------ | ------- | ------------------ |
| `tenure`           | Number  | `12`               |
| `MonthlyCharges`   | Number  | `70.5`             |
| `TotalCharges`     | Number  | `846.0`            |
| `gender`           | String  | `Female`           |
| `SeniorCitizen`    | Integer | `0`                |
| `Partner`          | String  | `Yes`              |
| `Dependents`       | String  | `No`               |
| `PhoneService`     | String  | `Yes`              |
| `MultipleLines`    | String  | `No`               |
| `InternetService`  | String  | `Fiber optic`      |
| `OnlineSecurity`   | String  | `No`               |
| `OnlineBackup`     | String  | `Yes`              |
| `DeviceProtection` | String  | `No`               |
| `TechSupport`      | String  | `No`               |
| `StreamingTV`      | String  | `Yes`              |
| `StreamingMovies`  | String  | `Yes`              |
| `Contract`         | String  | `Month-to-month`   |
| `PaperlessBilling` | String  | `Yes`              |
| `PaymentMethod`    | String  | `Electronic check` |


Minimum numerical fields often validated:

- tenure
- MonthlyCharges
- TotalCharges

For best accuracy, provide all fields used during training.

---

## 15. Response Fields

| Field               | Meaning                             |
| ------------------- | ----------------------------------- |
| `prediction`        | `1` means churn, `0` means no churn |
| `churn_probability` | Probability of churn                |
| `churn_risk`        | Business risk category              |

Risk logic:

|    Probability | Risk Level  |
| -------------: | ----------- |
|       `< 0.40` | Low Risk    |
| `0.40 to 0.74` | Medium Risk |
|      `>= 0.75` | High Risk   |

---

## 16. cURL Example

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

---

## 17. Python Request Example

import requests

url = "http://127.0.0.1:8000/predict"

payload = {
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
}

response = requests.post(url, json=payload)

print(response.status_code)
print(response.json())

---

## 18. Model Requirement

Before using the API, train the model:

python scripts/train_pipeline.py

This should create:

models/churn_model.pkl

If this file does not exist, the API cannot generate predictions.

---

## 19. API Testing

Run:

pytest tests/test_api.py -v

Run all tests:

pytest tests/ -v

---

## 20. Docker API Usage

Run:

docker compose -f docker/docker-compose.yml up --build

Open Flask UI:

http://127.0.0.1:5000

For Docker, use this host in config/config.yaml:

api:
  host: "0.0.0.0"
  port: 5000
  debug: true

---

21. Summary

The API layer makes the churn model usable outside notebooks.

It supports:

- Flask web predictions
- FastAPI REST predictions
- Single prediction
- Batch prediction
- Health checks
- JSON responses
- Swagger documentation
- Docker-ready serving