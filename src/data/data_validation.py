import pandas as pd


class DataValidationError(Exception):
    """Custom exception for data validation errors."""
    pass


def validate_dataframe(df: pd.DataFrame):
    """
    Perform full dataset validation.

    Checks:
    - Dataset not empty
    - Required columns present
    - Correct data types
    - No critical missing values
    - Valid target values
    """

    if df is None or df.empty:
        raise DataValidationError("Dataset is empty or not loaded properly.")

    # ---------------------------
    # REQUIRED COLUMNS
    # ---------------------------
    required_columns = [
        "customerID", "gender", "SeniorCitizen", "Partner", "Dependents",
        "tenure", "PhoneService", "MultipleLines", "InternetService",
        "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
        "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling",
        "PaymentMethod", "MonthlyCharges", "TotalCharges", "Churn"
    ]

    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise DataValidationError(f"Missing required columns: {missing_cols}")

    # ---------------------------
    # DATA TYPE CHECKS
    # ---------------------------
    if not pd.api.types.is_numeric_dtype(df["tenure"]):
        raise DataValidationError("Column 'tenure' must be numeric")

    if not pd.api.types.is_numeric_dtype(df["MonthlyCharges"]):
        raise DataValidationError("Column 'MonthlyCharges' must be numeric")

    # TotalCharges often comes as object → allow conversion later
    # So only check existence, not strict dtype here

    # ---------------------------
    # MISSING VALUES CHECK
    # ---------------------------
    critical_cols = ["tenure", "MonthlyCharges", "Churn"]

    for col in critical_cols:
        if df[col].isnull().sum() > 0:
            raise DataValidationError(f"Missing values found in critical column: {col}")

    # ---------------------------
    # TARGET VALIDATION
    # ---------------------------
    valid_targets = {"Yes", "No"}
    if not set(df["Churn"].unique()).issubset(valid_targets):
        raise DataValidationError("Invalid values found in 'Churn' column")

    # ---------------------------
    # CATEGORICAL VALUE CHECK (sample)
    # ---------------------------
    if "Contract" in df.columns:
        valid_contracts = {"Month-to-month", "One year", "Two year"}
        if not set(df["Contract"].unique()).issubset(valid_contracts):
            raise DataValidationError("Unexpected values in 'Contract' column")

    # ---------------------------
    # DUPLICATE CHECK
    # ---------------------------
    if df.duplicated().sum() > 0:
        raise DataValidationError("Duplicate rows found in dataset")

    return True


def validate_train_test_split(X, y):
    """
    Validate features and target after split.
    """

    if X.shape[0] != y.shape[0]:
        raise DataValidationError("Mismatch between X and y sizes")

    if X.empty or y.empty:
        raise DataValidationError("Train/Test split resulted in empty data")

    return True