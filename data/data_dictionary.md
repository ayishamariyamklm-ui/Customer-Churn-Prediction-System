# Data Dictionary — Customer Churn Prediction

## 1. Dataset Overview

This data dictionary describes the fields used in the **Telco Customer Churn Prediction** project.

The dataset contains customer-level information for a telecom company, including demographic details, account information, subscribed services, billing details, and churn status.

The goal of the dataset is to predict whether a customer is likely to leave the service.

---

## 2. Dataset Location

data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv

Processed files may be stored in:

data/processed/
├── train.csv
├── test.csv
└── validation.csv

---

## 3. Target Variable

| Column  | Type        | Description                                     | Example Values |
| ------- | ----------- | ----------------------------------------------- | -------------- |
| `Churn` | Categorical | Indicates whether the customer left the company | `Yes`, `No`    |

During model training, the target variable is converted into binary format:

| Original Value | Encoded Value | Meaning                |
| -------------- | ------------: | ---------------------- |
| `No`           |           `0` | Customer did not churn |
| `Yes`          |           `1` | Customer churned       |

---

## 4. Feature Categories

The dataset features can be grouped into the following categories:

| Category                | Description                           |
| ----------------------- | ------------------------------------- |
| Customer Identification | Unique customer identifier            |
| Demographics            | Customer personal attributes          |
| Account Information     | Contract and billing details          |
| Telecom Services        | Subscribed phone/internet services    |
| Charges                 | Monthly and total billing information |
| Target                  | Churn outcome                         |

---

## 5. Full Data Dictionary

| Column Name        | Data Type                      | Category                | Description                                                  | Example Values                                                                             | Used in Model |
| ------------------ | ------------------------------ | ----------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------- |
| `customerID`       | String                         | Customer Identification | Unique customer identifier                                   | `7590-VHVEG`                                                                               | No            |
| `gender`           | Categorical                    | Demographics            | Customer gender                                              | `Male`, `Female`                                                                           | Yes           |
| `SeniorCitizen`    | Integer/Categorical            | Demographics            | Indicates whether the customer is a senior citizen           | `0`, `1`                                                                                   | Yes           |
| `Partner`          | Categorical                    | Demographics            | Indicates whether the customer has a partner                 | `Yes`, `No`                                                                                | Yes           |
| `Dependents`       | Categorical                    | Demographics            | Indicates whether the customer has dependents                | `Yes`, `No`                                                                                | Yes           |
| `tenure`           | Numeric                        | Account Information     | Number of months the customer has stayed with the company    | `1`, `24`, `72`                                                                            | Yes           |
| `PhoneService`     | Categorical                    | Telecom Services        | Indicates whether the customer has phone service             | `Yes`, `No`                                                                                | Yes           |
| `MultipleLines`    | Categorical                    | Telecom Services        | Indicates whether the customer has multiple phone lines      | `Yes`, `No`, `No phone service`                                                            | Yes           |
| `InternetService`  | Categorical                    | Telecom Services        | Type of internet service used by the customer                | `DSL`, `Fiber optic`, `No`                                                                 | Yes           |
| `OnlineSecurity`   | Categorical                    | Telecom Services        | Indicates whether the customer has online security service   | `Yes`, `No`, `No internet service`                                                         | Yes           |
| `OnlineBackup`     | Categorical                    | Telecom Services        | Indicates whether the customer has online backup service     | `Yes`, `No`, `No internet service`                                                         | Yes           |
| `DeviceProtection` | Categorical                    | Telecom Services        | Indicates whether the customer has device protection service | `Yes`, `No`, `No internet service`                                                         | Yes           |
| `TechSupport`      | Categorical                    | Telecom Services        | Indicates whether the customer has technical support service | `Yes`, `No`, `No internet service`                                                         | Yes           |
| `StreamingTV`      | Categorical                    | Telecom Services        | Indicates whether the customer has streaming TV service      | `Yes`, `No`, `No internet service`                                                         | Yes           |
| `StreamingMovies`  | Categorical                    | Telecom Services        | Indicates whether the customer has streaming movies service  | `Yes`, `No`, `No internet service`                                                         | Yes           |
| `Contract`         | Categorical                    | Account Information     | Customer contract type                                       | `Month-to-month`, `One year`, `Two year`                                                   | Yes           |
| `PaperlessBilling` | Categorical                    | Account Information     | Indicates whether customer uses paperless billing            | `Yes`, `No`                                                                                | Yes           |
| `PaymentMethod`    | Categorical                    | Account Information     | Customer payment method                                      | `Electronic check`, `Mailed check`, `Bank transfer (automatic)`, `Credit card (automatic)` | Yes           |
| `MonthlyCharges`   | Numeric                        | Charges                 | Amount charged to the customer each month                    | `29.85`, `70.70`, `99.65`                                                                  | Yes           |
| `TotalCharges`     | Numeric/Object before cleaning | Charges                 | Total amount charged to the customer                         | `29.85`, `1889.50`, `6844.50`                                                              | Yes           |
| `Churn`            | Categorical                    | Target                  | Indicates whether customer churned                           | `Yes`, `No`                                                                                | Target        |

---

## 6. Column-Level Details

### 6.1 customerID

| Attribute     | Description  |
| ------------- | ------------ |
| Column        | `customerID` |
| Type          | String       |
| Role          | Identifier   |
| Used in Model | No           |

- Description :

`customerID` is a unique identifier for each customer.

- Reason for Exclusion :

This column is removed during preprocessing because it does not provide predictive value. It is only used to identify customers.

### 6.2 gender

| Attribute     | Description  |
| ------------- | ------------ |
| Column        | `customerID` |
| Type          | String       |
| Role          | Identifier   |
| Used in Model | No           |


- Description :

Represents the gender of the customer.

### 6.3 SeniorCitizen

| Attribute     | Description           |
| ------------- | --------------------- |
| Column        | `SeniorCitizen`       |
| Type          | Integer / Categorical |
| Values        | `0`, `1`              |
| Used in Model | Yes                   |

- Description :

Indicates whether the customer is a senior citizen.

| Value | Meaning              |
| ----: | -------------------- |
|   `0` | Not a senior citizen |
|   `1` | Senior citizen       |

### 6.4 Partner

| Attribute     | Description |
| ------------- | ----------- |
| Column        | `Partner`   |
| Type          | Categorical |
| Values        | `Yes`, `No` |
| Used in Model | Yes         |

- Description :

Indicates whether the customer has a partner.

### 6.5 Dependents

| Attribute     | Description  |
| ------------- | ------------ |
| Column        | `Dependents` |
| Type          | Categorical  |
| Values        | `Yes`, `No`  |
| Used in Model | Yes          |

- Description :

Indicates whether the customer has dependents.

### 6.6 tenure

| Attribute     | Description |
| ------------- | ----------- |
| Column        | `tenure`    |
| Type          | Numeric     |
| Unit          | Months      |
| Used in Model | Yes         |

- Description :

Number of months the customer has stayed with the telecom company.

- Business Meaning :

Tenure is usually one of the strongest churn indicators. Customers with shorter tenure often have higher churn risk.

### 6.7 PhoneService

| Attribute     | Description    |
| ------------- | -------------- |
| Column        | `PhoneService` |
| Type          | Categorical    |
| Values        | `Yes`, `No`    |
| Used in Model | Yes            |

- Description :

Indicates whether the customer subscribes to phone service.

### 6.8 MultipleLines

| Attribute     | Description                     |
| ------------- | ------------------------------- |
| Column        | `MultipleLines`                 |
| Type          | Categorical                     |
| Values        | `Yes`, `No`, `No phone service` |
| Used in Model | Yes                             |

- Description :

Indicates whether the customer has multiple phone lines.

### 6.9 InternetService

| Attribute     | Description                |
| ------------- | -------------------------- |
| Column        | `InternetService`          |
| Type          | Categorical                |
| Values        | `DSL`, `Fiber optic`, `No` |
| Used in Model | Yes                        |

- Description :

Indicates the type of internet service used by the customer.

- Business Meaning :

Internet service type may influence churn because service quality, pricing, and customer expectations differ across service types.

### 6.10 OnlineSecurity

| Attribute     | Description                        |
| ------------- | ---------------------------------- |
| Column        | `OnlineSecurity`                   |
| Type          | Categorical                        |
| Values        | `Yes`, `No`, `No internet service` |
| Used in Model | Yes                                |

- Description :

Indicates whether the customer has online security service.

- Business Meaning :

Customers without online security may show higher churn risk if they feel the service package lacks value.

### 6.11 OnlineBackup

| Attribute     | Description                        |
| ------------- | ---------------------------------- |
| Column        | `OnlineBackup`                     |
| Type          | Categorical                        |
| Values        | `Yes`, `No`, `No internet service` |
| Used in Model | Yes                                |

- Description :

Indicates whether the customer has online backup service.

### 6.12 DeviceProtection

| Attribute     | Description                        |
| ------------- | ---------------------------------- |
| Column        | `DeviceProtection`                 |
| Type          | Categorical                        |
| Values        | `Yes`, `No`, `No internet service` |
| Used in Model | Yes                                |

- Description :

Indicates whether the customer has device protection service.

### 6.13 TechSupport

| Attribute     | Description                        |
| ------------- | ---------------------------------- |
| Column        | `TechSupport`                      |
| Type          | Categorical                        |
| Values        | `Yes`, `No`, `No internet service` |
| Used in Model | Yes                                |

- Description :

Indicates whether the customer has technical support.

- Business Meaning :

Lack of technical support can increase dissatisfaction and churn risk.

### 6.14 StreamingTV

| Attribute     | Description                        |
| ------------- | ---------------------------------- |
| Column        | `TechSupport`                      |
| Type          | Categorical                        |
| Values        | `Yes`, `No`, `No internet service` |
| Used in Model | Yes                                |

- Description :

Indicates whether the customer has streaming TV service.

### 6.15 StreamingMovies

| Attribute     | Description                        |
| ------------- | ---------------------------------- |
| Column        | `StreamingMovies`                  |
| Type          | Categorical                        |
| Values        | `Yes`, `No`, `No internet service` |
| Used in Model | Yes                                |

- Description :

Indicates whether the customer has streaming movie service.

### 6.16 Contract

| Attribute     | Description                              |
| ------------- | ---------------------------------------- |
| Column        | `Contract`                               |
| Type          | Categorical                              |
| Values        | `Month-to-month`, `One year`, `Two year` |
| Used in Model | Yes                                      |

- Description :

Indicates the customer's contract type.

- Business Meaning :

Contract type is usually a strong churn predictor.

| Contract Type    | Expected Churn Risk |
| ---------------- | ------------------- |
| `Month-to-month` | High                |
| `One year`       | Medium              |
| `Two year`       | Low                 |

Customers on month-to-month contracts can leave more easily, which often increases churn risk.

### 6.17 PaperlessBilling

| Attribute     | Description        |
| ------------- | ------------------ |
| Column        | `PaperlessBilling` |
| Type          | Categorical        |
| Values        | `Yes`, `No`        |
| Used in Model | Yes                |

- Description :

Indicates whether the customer uses paperless billing.

### 6.18 PaymentMethod

| Attribute     | Description                                                                                |
| ------------- | ------------------------------------------------------------------------------------------ |
| Column        | `PaymentMethod`                                                                            |
| Type          | Categorical                                                                                |
| Values        | `Electronic check`, `Mailed check`, `Bank transfer (automatic)`, `Credit card (automatic)` |
| Used in Model | Yes                                                                                        |

- Description :

Indicates the customer payment method.

- Business Meaning :

Payment method may relate to churn behavior. For example, some datasets show customers using electronic checks may have higher churn risk.

### 6.19 MonthlyCharges

| Attribute     | Description      |
| ------------- | ---------------- |
| Column        | `MonthlyCharges` |
| Type          | Numeric          |
| Unit          | Currency         |
| Used in Model | Yes              |

- Description :

Amount charged to the customer each month.

- Business Meaning :

Higher monthly charges may increase churn risk if the customer feels the service is expensive or not valuable enough.

### 6.20 TotalCharges

| Attribute     | Description                 |
| ------------- | --------------------------- |
| Column        | `TotalCharges`              |
| Type          | Numeric after preprocessing |
| Unit          | Currency                    |
| Used in Model | Yes                         |

- Description :

Total amount charged to the customer over their lifetime with the company.

- Data Quality Note

`TotalCharges` may appear as an object/string column in the raw dataset and must be converted to numeric during preprocessing.

`df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")`

---

## 7. Numerical Features

The main numerical features are:

| Feature          | Description                      |
| ---------------- | -------------------------------- |
| `tenure`         | Number of months customer stayed |
| `MonthlyCharges` | Monthly billing amount           |
| `TotalCharges`   | Total billing amount             |


These features are typically scaled using:

StandardScaler

---

## 8. Categorical Features

The categorical features are:

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

These are typically encoded using:

`OneHotEncoder`

with:

`handle_unknown="ignore"`

This prevents inference errors when unseen categories appear.

---

## 9. Features Excluded from Modeling

| Column       | Reason                               |
| ------------ | ------------------------------------ |
| `customerID` | Identifier only, no predictive value |

---

## 10. Data Cleaning Rules

| Rule                          | Description                           |
| ----------------------------- | ------------------------------------- |
| Drop `customerID`             | Remove non-predictive identifier      |
| Convert `TotalCharges`        | Convert from string/object to numeric |
| Handle missing `TotalCharges` | Fill using median                     |
| Strip categorical values      | Remove accidental spaces              |
| Encode `Churn`                | Convert `Yes/No` to `1/0`             |

---

## 11. Data Validation Rules

The validation process should check:

| Check                     | Purpose                                    |
| ------------------------- | ------------------------------------------ |
| Dataset is not empty      | Prevent training on empty file             |
| Required columns exist    | Ensure schema consistency                  |
| Target column exists      | Required for supervised learning           |
| Target values are valid   | Must contain only `Yes/No` before encoding |
| Numeric columns are valid | Prevent training errors                    |
| Duplicate rows checked    | Improve data quality                       |

---

## 12. Expected Raw Schema

Expected raw columns:

- customerID
- gender
- SeniorCitizen
- Partner
- Dependents
- tenure
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
- MonthlyCharges
- TotalCharges
- Churn

---

## 13. Expected Model Input Schema

After dropping customerID and separating target, the model expects:

- gender
- SeniorCitizen
- Partner
- Dependents
- tenure
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
- MonthlyCharges
- TotalCharges

---

## 14. Example Raw Record

{
  "customerID": "7590-VHVEG",
  "gender": "Female",
  "SeniorCitizen": 0,
  "Partner": "Yes",
  "Dependents": "No",
  "tenure": 1,
  "PhoneService": "No",
  "MultipleLines": "No phone service",
  "InternetService": "DSL",
  "OnlineSecurity": "No",
  "OnlineBackup": "Yes",
  "DeviceProtection": "No",
  "TechSupport": "No",
  "StreamingTV": "No",
  "StreamingMovies": "No",
  "Contract": "Month-to-month",
  "PaperlessBilling": "Yes",
  "PaymentMethod": "Electronic check",
  "MonthlyCharges": 29.85,
  "TotalCharges": "29.85",
  "Churn": "No"
}

---

## 15. Example Model Input

{
  "gender": "Female",
  "SeniorCitizen": 0,
  "Partner": "Yes",
  "Dependents": "No",
  "tenure": 1,
  "PhoneService": "No",
  "MultipleLines": "No phone service",
  "InternetService": "DSL",
  "OnlineSecurity": "No",
  "OnlineBackup": "Yes",
  "DeviceProtection": "No",
  "TechSupport": "No",
  "StreamingTV": "No",
  "StreamingMovies": "No",
  "Contract": "Month-to-month",
  "PaperlessBilling": "Yes",
  "PaymentMethod": "Electronic check",
  "MonthlyCharges": 29.85,
  "TotalCharges": 29.85
}

---


## 16. Example Model Output

{
  "prediction": 0,
  "churn_probability": 0.21,
  "churn_risk": "Low Risk"
}

---

## 17. Business Interpretation of Key Features

| Feature           | Business Interpretation                                 |
| ----------------- | ------------------------------------------------------- |
| `tenure`          | Short tenure often means higher churn risk              |
| `Contract`        | Month-to-month contracts usually have higher churn risk |
| `MonthlyCharges`  | Higher charges may increase churn risk                  |
| `TechSupport`     | Lack of support may increase dissatisfaction            |
| `OnlineSecurity`  | Additional services may improve customer stickiness     |
| `InternetService` | Service type may affect customer experience             |
| `PaymentMethod`   | Some payment methods may correlate with churn behavior  |
| `TotalCharges`    | Indicates lifetime value and customer history           |

----

## 18. Feature Engineering Possibilities

The following engineered features can improve model understanding:

| Feature              | Formula / Logic               | Meaning                    |
| -------------------- | ----------------------------- | -------------------------- |
| `AvgChargesPerMonth` | `TotalCharges / (tenure + 1)` | Average spending behavior  |
| `TenureGroup`        | Bin tenure into groups        | Customer lifecycle segment |
| `TotalServices`      | Count subscribed services     | Customer engagement level  |

---

## 19. Data Leakage Considerations

To avoid data leakage:

- Do not use future information in training
- Do not include customer identifiers as features
- Fit preprocessing only on training data
- Use scikit-learn pipelines for preprocessing and modeling
- Avoid manually preprocessing test data using full dataset statistics

---
