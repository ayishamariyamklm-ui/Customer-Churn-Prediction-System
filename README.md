# Customer Churn Prediction System

## Project Overview

This project is an end-to-end machine learning system that predicts whether a telecom customer is likely to churn.

The project is designed as a job-ready data science portfolio project, not just a notebook experiment. It includes data preprocessing, feature engineering, model training, model evaluation, model persistence, prediction pipelines, a Flask web application, a FastAPI API, batch prediction, testing, documentation, Docker support, and CI/CD using GitHub Actions.

---

## Business Problem

Customer churn is one of the most important business problems in the telecom industry. When customers leave a service provider, the company loses recurring revenue and may also spend more money acquiring new customers.

The goal of this project is to help a telecom company identify high-risk customers before they churn, so the business can take proactive retention actions such as:

- Offering discounts or loyalty rewards
- Improving customer support
- Promoting long-term contracts
- Targeting customers with personalized retention campaigns

---

## Project Objective

The main objective is to build a production-style machine learning system that can:

- Predict customer churn
- Estimate churn probability
- Classify customers into risk levels
- Support both single and batch predictions
- Serve predictions through a web app and API
- Track model performance and artifacts

---

## Dataset

The project uses the Telco Customer Churn dataset.

Dataset file:


data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv

The dataset contains customer demographic, account, service, and billing information.

Example features include:

- Gender
- SeniorCitizen
- Partner
- Dependents
- Tenure
- PhoneService
- InternetService
- OnlineSecurity
- TechSupport
- Contract
- PaymentMethod
- MonthlyCharges
- TotalCharges
- Churn

Target column:

Churn

Target values:

- Yes = Customer churned
- No = Customer stayed

---

## GitHub Project Structure

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
│   │   ├── test.csv
│   │   ├── train.csv
│   │   └── validation.csv
│   └── data_dictionary.md
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_experiments.ipynb
│
├── src/
│   ├── __init__.py
│   │
│   ├── data/
│   │   ├── data_preprocessing.py
│   │   ├── data_validation.py
│   │   └── data_loader.py
│   │
│   ├── features/
│   │   ├── feature_engineering.py
│   │   └── feature_selection.py
│   │
│   ├── models/
│   │   ├── model_training.py
│   │   ├── model_evaluation.py
│   │   ├── model_registry.py
│   │   └── hyperparameter_tuning.py
│   │
│   ├── inference/
│   │   ├── model_inference.py
│   │   └── predict_pipeline.py
│   │
│   ├── utils/
│   │   ├── logger.py
│   │   ├── exceptions.py
│   │   └── helpers.py
│   │
├── models/
│   ├── best_model.pkl
│   ├── churn_model.pkl
│   ├── preprocessor.pkl
│   └── metrics.json
│
├── app/
│   ├── __init__.py
│   ├── web_app.py
│   ├── api.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── main.js
│
├── config/
│   ├── config.yaml
│   ├── paths.yaml
│   └── logging.yaml
│
├── scripts/
│   ├── _init_.py
│   ├── split_data.py
│   ├── train_pipeline.py
│   ├── evaluate_model.py
│   ├── run_app.py
│   └── batch_predict.py
│
├── tests/
│   ├── __init__.py
│   ├── test_data_preprocessing.py
│   ├── test_feature_engineering.py
│   ├── test_model_training.py
│   ├── test_inference.py
│   └── test_api.py
│
├── docs/
│   ├── architecture.md
│   ├── api_docs.md
│   ├── model_report.md
│   └── deployment_guide.md
│
├── logs/
│   ├── app.log
│   ├── error.log
│   ├── prediction.log
│   ├── preprocessing.log
│   └── training.log
│
├── artifacts/
│   ├── confusion_matrix.png
│   └── roc_curve.png
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
└── .github/
    └── workflows/
        └── ci.yml


---

## Architecture Summary

The system follows a modular machine learning architecture.

Raw Data
   ↓
Data Validation
   ↓
Data Preprocessing
   ↓
Feature Engineering
   ↓
Model Training
   ↓
Model Evaluation
   ↓
Model Artifact Saving
   ↓
Inference Pipeline
   ↓
Web App / REST API / Batch Prediction

---

## Main Components

### 1. Data Layer

Location:

src/data/

Responsibilities:

- Load raw dataset
- Validate required columns
- Clean missing and invalid values
- Convert data types
- Prepare data for modeling

Important files:

- src/data/data_loader.py
- src/data/data_preprocessing.py
- src/data/data_validation.py

### 2. Feature Engineering Layer

Location:

src/features/

Responsibilities:

- Create business-driven features
- Build preprocessing pipeline
- Encode categorical variables
- Scale numerical features
- Support feature selection

Important files:

- src/features/feature_engineering.py
- src/features/feature_selection.py

Example engineered features:

- Average charges per month
- Tenure group
- Total services used

### 3. Model Training Layer

Location:

- src/models/
- scripts/train_pipeline.py

Responsibilities:

- Train multiple machine learning models
- Compare model performance
- Select the best model
- Save trained model artifacts
- Save metrics

Models used:

- Logistic Regression
- Random Forest Classifier
- Gradient Boosting Classifier

Best model selection metric:

ROC-AUC

ROC-AUC is used because churn prediction is an imbalanced classification problem, and accuracy alone can be misleading.

### 4. Inference Layer

Location:

src/inference/

Responsibilities:

- Load trained model
- Accept customer input
- Generate prediction
- Generate churn probability
- Return business-friendly risk level

Important files:

- src/inference/model_inference.py
- src/inference/predict_pipeline.py

Example output:

{
  "prediction": 1,
  "churn_probability": 0.82,
  "churn_risk": "High Risk"
}

### 5. Application Layer

Location:

app/

The project includes two interfaces:

#### Flask Web App

File:

app/web_app.py

Purpose:

- Provides a simple browser-based interface
- Allows business users to enter customer details
- Displays churn prediction and risk level

#### FastAPI REST API

File:

app/api.py

Purpose:

- Provides API endpoints for system integration
- Supports single customer prediction
- Supports batch prediction

---

## Model Artifacts

After training, the following files are generated:

models/
├── best_model.pkl
├── churn_model.pkl
├── preprocessor.pkl
└── metrics.json

### churn_model.pkl

Contains the complete trained pipeline:

preprocessing + model

This is used for inference.

### best_model.pkl

A copy of the selected best-performing model.

### preprocessor.pkl

Stores the preprocessing object separately for inspection, debugging, or reuse.

### metrics.json

Stores model performance results, including:

- Best model name
- Selection metric
- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Cross-validation score

---

## Visual Artifacts

The project generates visual artifacts for model interpretation and evaluation.

artifacts/
├── confusion_matrix.png
└── roc_curve.png

### confusion_matrix.png

Shows how many customers were correctly or incorrectly classified as churn or non-churn.

### roc_curve.png

Shows the trade-off between true positive rate and false positive rate.

---

## Evaluation Metrics

The project evaluates models using:

| Metric    | Meaning                                            | Business Relevance                   |
| --------- | -------------------------------------------------- | ------------------------------------ |
| Accuracy  | Overall correct predictions                        | Basic performance indicator          |
| Precision | Correct churn predictions among predicted churners | Helps avoid wasting retention offers |
| Recall    | Actual churners correctly identified               | Important for reducing missed churn  |
| F1-score  | Balance of precision and recall                    | Useful for imbalanced data           |
| ROC-AUC   | Ability to separate churners from non-churners     | Main model selection metric          |

For churn prediction, recall is especially important because missing a customer who is likely to churn can result in lost revenue.

---

## Installation

### 1. Clone the repository

git clone https://github.com/ayishamariyamklm-ui/customer-churn-prediction.git
cd customer-churn-prediction

### 2. Create a virtual environment

Windows:

python -m venv venv
venv\Scripts\activate

Mac/Linux:

python -m venv venv
source venv/bin/activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Install project in editable mode

pip install -e .

#### Environment Variables

Create a .env file from .env.example:

cp .env.example .env

For Windows PowerShell:

copy .env.example .env

Example .env.example:

APP_ENV=development
DEBUG=True
APP_HOST=127.0.0.1
APP_PORT=5000
MODEL_PATH=models/churn_model.pkl
LOG_LEVEL=INFO

#### How to Run the Training Pipeline

Run this from the project root:

python scripts/train_pipeline.py

This will:

- Load raw data
- Clean and preprocess data
- Train multiple models
- Select the best model using ROC-AUC
- Save model artifacts
- Save metrics
- Generate evaluation plots

Expected output:

models/
├── best_model.pkl
├── churn_model.pkl
├── preprocessor.pkl
└── metrics.json

artifacts/
├── confusion_matrix.png
└── roc_curve.png

#### How to Run the Flask Web App

Make sure the model has already been trained:

python scripts/train_pipeline.py

Then run:

python scripts/run_app.py

Open in browser:

http://127.0.0.1:5000

If your config uses port 8000, open:

http://127.0.0.1:8000

#### How to Run the FastAPI API

Run:

uvicorn app.api:app --reload

Open API docs:

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/health

---

## API Usage

### Single Prediction Endpoint

POST /predict

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

### How to Run Batch Prediction

Batch prediction is useful when a business wants churn scores for many customers at once.

Command:

python scripts/batch_predict.py data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv outputs/predictions.csv

Output file:

outputs/batch_predictions.csv

The output contains the original customer data plus:

- prediction
- churn_probability
- risk_level

### How to Run Tests

Run all tests:

pytest tests/ -v

The tests cover:

- Data preprocessing
- Feature engineering
- Model training
- Inference
- API endpoints

---

## Docker Usage

This project includes Docker support for reproducible deployment.

### Build Docker Image

Run from the project root:

docker build -f docker/Dockerfile -t telco-churn-app .

### Run Docker Container

docker run -p 5000:5000 telco-churn-app

Open:

http://127.0.0.1:5000

### Run with Docker Compose

docker compose -f docker/docker-compose.yml up --build

Stop containers:

docker compose -f docker/docker-compose.yml down

Important:

Inside Docker, the app host should be:

api:
  host: "0.0.0.0"

Do not use:

host: "127.0.0.1"

inside Docker.

---

## CI/CD with GitHub Actions

The project includes a GitHub Actions workflow:

.github/workflows/ci.yml

The CI pipeline runs automatically on push or pull request.

It checks:

- Project structure
- Dependency installation
- Code linting
- Unit tests

This helps catch errors before code is merged.

---

## Configuration

Configuration files are stored in:

config/
├── config.yaml
├── paths.yaml
└── logging.yaml

### config.yaml

Stores:

- Data settings
- Feature lists
- Model parameters
- Training settings
- API settings
- Business thresholds

### paths.yaml

Stores all project file paths.

### logging.yaml

Stores logging configuration.

This makes the project configurable and avoids hardcoding paths in Python files.

---

## Logs

Logs are stored in:

logs/
├── app.log
├── error.log
├── prediction.log
├── preprocessing.log
└── training.log

Logging helps track:

- Training progress
- Prediction requests
- Errors
- Application behavior

---

## Notebooks

The project includes three main notebooks:

- notebooks/01_eda.ipynb
- notebooks/02_feature_engineering.ipynb
- notebooks/03_model_experiments.ipynb

### 01_eda.ipynb

Explores the dataset and identifies churn patterns.

### 02_feature_engineering.ipynb

Creates and analyzes new business-driven features.

### 03_model_experiments.ipynb

Compares multiple models and explains model selection.

---

## Business Insights

Key churn drivers identified in this project include:

- Customers with short tenure are more likely to churn
- Month-to-month contract customers have higher churn risk
- High monthly charges are associated with higher churn
- Customers without tech support or online security show higher churn
- Long-term contracts reduce churn risk

---

## Business Recommendations

Based on the churn prediction system, the telecom company can:

- Target high-risk customers with retention offers
- Promote annual or two-year contracts
- Offer support upgrades to customers without tech support
- Monitor new customers during their first year
- Prioritize high-value customers with high churn probability

---

## Technical Highlights

This project demonstrates:

- Modular Python project structure
- Clean separation of concerns
- Config-driven ML pipeline
- Data preprocessing and validation
- Feature engineering
- Multiple model comparison
- Model evaluation using business-relevant metrics
- Model serialization using joblib
- Web application using Flask
- REST API using FastAPI
- Batch prediction
- Docker support
- CI/CD using GitHub Actions
- Unit testing with pytest
- Documentation for architecture, API, model report, and deployment

---

## Author

Ayisha Mariyam
Data Scientist | Machine Learning | Analytics
