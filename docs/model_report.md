# Model Report — Customer Churn Prediction

## 1. Report Overview

This report documents the modeling process for the Telco Customer Churn Prediction System.

It covers:

- Business objective
- Dataset summary
- Preprocessing
- Feature engineering
- Model training
- Model comparison
- Evaluation metrics
- Best model selection
- Business insights
- Limitations
- Future improvements

---

## 2. Business Objective

The objective is to predict which telecom customers are likely to churn.

The model helps the business:

- Identify high-risk customers
- Reduce revenue loss
- Prioritize retention campaigns
- Improve customer lifetime value
- Make data-driven customer decisions

---

## 3. Machine Learning Problem

This is a binary classification problem.

Target column:


Churn

Classes:

| Encoded Value | Meaning                 |
| ------------: | ----------------------- |
|           `0` | Customer will not churn |
|           `1` | Customer will churn     |


Original mapping:

No  → 0
Yes → 1

---

## 4. Dataset

Raw dataset:

data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv

Processed datasets:

data/processed/
├── train.csv
├── test.csv
└── validation.csv

Data dictionary:

data/data_dictionary.md

---

## 5. Feature Groups

 Numerical Features :

- tenure
- MonthlyCharges
- TotalCharges

Categorical Features :

- gender
- SeniorCitizen
- Partner
- Dependents
- PhoneService
- MultipleLines
- InternetService
- OnlineSecurity
- OnlineBackup
- DeviceProtection
- TechSupport
- StreamingTV
- StreamingMovies
- Contract
- PaperlessBilling
- PaymentMethod

---

## 6. Data Preprocessing

Preprocessing includes:

- Dropping customerID
- Converting TotalCharges to numeric
- Handling missing values
- Encoding target column
- Scaling numerical variables
- One-hot encoding categorical variables

Preprocessing is handled using a scikit-learn Pipeline and ColumnTransformer.

This ensures that training and inference use the same transformations.

---

## 7. Feature Engineering

Feature engineering may include:

| Feature              | Meaning                     |
| -------------------- | --------------------------- |
| `AvgChargesPerMonth` | Spending behavior           |
| `TenureGroup`        | Customer lifecycle segment  |
| `TotalServices`      | Customer service engagement |


Business interpretation:

- Short-tenure customers are more likely to churn
- Customers with more services may be more engaged
- High charges may increase churn risk
- Month-to-month contracts may increase churn risk

---

## 8. Models Trained

The project compares multiple models:

| Model                        | Purpose                      |
| ---------------------------- | ---------------------------- |
| Logistic Regression          | Baseline interpretable model |
| Random Forest Classifier     | Non-linear ensemble model    |
| Gradient Boosting Classifier | Strong tabular-data model    |

---

## 9. Training Pipeline

Main script:

scripts/train_pipeline.py

Run:

python scripts/train_pipeline.py

Training steps:

- Load data
- Clean data
- Split features and target
- Train-test split
- Build preprocessing pipeline
- Train candidate models
- Evaluate models
- Select best model
- Save model artifacts
- Save metrics
- Save plots

---

## 10. Evaluation Metrics

The model is evaluated using:

| Metric    | Meaning                                            | Business Relevance        |
| --------- | -------------------------------------------------- | ------------------------- |
| Accuracy  | Overall correct predictions                        | Basic performance         |
| Precision | Correct churn predictions among predicted churners | Avoids unnecessary offers |
| Recall    | Actual churners correctly detected                 | Reduces missed churn      |
| F1-score  | Balance of precision and recall                    | Useful for imbalance      |
| ROC-AUC   | Ability to separate churners and non-churners      | Main selection metric     |

---

## 11. Why Accuracy Is Not Enough

Churn datasets are often imbalanced.

A model can get high accuracy by predicting most customers as non-churn. That is not useful for business because the goal is to identify customers likely to leave.

Therefore, this project focuses on:

- Recall
- F1-score
- ROC-AUC

---

## 12. Best Model Selection

The best model is selected using:

ROC-AUC

Reason:

ROC-AUC evaluates how well the model separates churn customers from non-churn customers across different thresholds.

This is better than relying only on accuracy.

---

## 13. Model Metrics

Metrics are saved automatically in:

models/metrics.json

Example structure:

{
  "best_model": "random_forest",
  "selection_metric": "roc_auc",
  "best_score": 0.86,
  "models": {
    "logistic_regression": {
      "accuracy": 0.80,
      "precision": 0.68,
      "recall": 0.73,
      "f1_score": 0.70,
      "roc_auc": 0.84,
      "cv_score": 0.83
    },
    "random_forest": {
      "accuracy": 0.82,
      "precision": 0.74,
      "recall": 0.76,
      "f1_score": 0.75,
      "roc_auc": 0.86,
      "cv_score": 0.85
    }
  }
}

Actual values are generated by running the training pipeline.

---

## 14. Model Artifacts

Generated artifacts:

models/
├── best_model.pkl
├── churn_model.pkl
├── preprocessor.pkl
└── metrics.json
churn_model.pkl

Full prediction pipeline:

- Preprocessor + Trained model

Used for inference.

- best_model.pkl

Copy of the best selected model.

- preprocessor.pkl

Stores preprocessing separately for debugging and inspection.

- metrics.json

Stores model comparison results.

---

## 15. Visual Artifacts

Generated files:

artifacts/
├── confusion_matrix.png
└── roc_curve.png
Confusion Matrix

Shows:

- True positives
- True negatives
- False positives
- False negatives

In churn prediction, false negatives are especially costly because they represent customers who churned but were missed by the model.

ROC Curve

Shows how well the model separates churners from non-churners.

---

## 16. Business Insights

Common churn drivers:

Short customer tenure
Month-to-month contracts
High monthly charges
Lack of tech support
Lack of online security
Electronic check payment method
Low service engagement

---

## 17. Business Recommendations

Recommended actions:

| Customer Segment          | Action                      |
| ------------------------- | --------------------------- |
| High churn probability    | Priority retention campaign |
| Medium churn probability  | Engagement offer            |
| New customers             | Early onboarding support    |
| Month-to-month contracts  | Offer annual plan discount  |
| Customers without support | Promote support bundles     |

---

## 18. Risk Level Strategy

| Churn Probability | Risk Level  | Suggested Action             |
| ----------------: | ----------- | ---------------------------- |
|          `< 0.40` | Low Risk    | No immediate action          |
|    `0.40 to 0.74` | Medium Risk | Monitor and offer engagement |
|         `>= 0.75` | High Risk   | Immediate retention action   |

---

## 19. Example Prediction

{
  "prediction": 1,
  "churn_probability": 0.82,
  "churn_risk": "High Risk"
}

Business interpretation:

The customer is likely to churn and should be prioritized for retention.

---

## 20. Business Impact Example

Assume:

Total customers = 10,000
At-risk customers = 2,500
Average monthly revenue per customer = ₹1,500

If retention actions reduce churn by 10%:

Retained customers = 250
Monthly revenue protected = ₹375,000
Annual revenue protected = ₹4,500,000

---

## 21. Deployment Usage

Train model
python scripts/train_pipeline.py
Run Flask app
python scripts/run_app.py
Run FastAPI
uvicorn app.api:app --reload
Batch prediction
python scripts/batch_predict.py data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv outputs/predictions.csv

---

## 22. Testing

Run:

pytest tests/ -v

Tests cover:

- Preprocessing
- Feature engineering
- Model training
- Inference
- API endpoints

---

## 26. Summary

This model report shows that the project includes:

- Business problem framing
- Clean preprocessing
- Feature engineering
- Multiple model comparison
- Evaluation with business-relevant metrics
- Model artifact saving
- Inference deployment
- Testing and documentation