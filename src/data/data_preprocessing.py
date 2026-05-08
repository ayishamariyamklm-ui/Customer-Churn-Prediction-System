import pandas as pd
import os
from sklearn.model_selection import train_test_split


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw telecom churn dataset.

    Steps:
    - Drop unnecessary columns
    - Fix data types
    - Handle missing values
    - Normalize categorical values
    """

    df = df.copy()

    # ---------------------------
    # DROP IRRELEVANT COLUMNS
    # ---------------------------
    if "customerID" in df.columns:
        df.drop("customerID", axis=1, inplace=True)

    # ---------------------------
    # FIX DATA TYPES
    # ---------------------------
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    # ---------------------------
    # HANDLE MISSING VALUES
    # ---------------------------
    if "TotalCharges" in df.columns:
        df["TotalCharges"].fillna(df["TotalCharges"].median(), inplace=True)

    # ---------------------------
    # STANDARDIZE CATEGORICAL VALUES
    # ---------------------------
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    # ---------------------------
    # TARGET COLUMN CLEANING
    # ---------------------------
    if "Churn" in df.columns:
        df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

    return df


def split_features_target(df: pd.DataFrame):
    """
    Split dataset into features and target.
    """

    if "Churn" not in df.columns:
        raise ValueError("Target column 'Churn' not found in dataset")

    X = df.drop("Churn", axis=1)
    y = df["Churn"]

    return X, y


def preprocess_pipeline(df: pd.DataFrame):
    """
    Full preprocessing pipeline:
    - Clean data
    - Split into X and y
    """

    df_clean = clean_data(df)
    X, y = split_features_target(df_clean)

    return X, y




def split_and_save_data(df: pd.DataFrame, output_dir="data/processed"):
    """
    Split dataset into train, validation, and test sets
    and save them as CSV files.
    """

    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Clean data
    df_clean = clean_data(df)

    # Step 2: Train (70%) and Temp (30%)
    train_df, temp_df = train_test_split(
        df_clean,
        test_size=0.3,
        random_state=42,
        stratify=df_clean["Churn"]
    )

    # Step 3: Validation (15%) and Test (15%)
    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.5,
        random_state=42,
        stratify=temp_df["Churn"]
    )

    # Step 4: Save datasets
    train_df.to_csv(f"{output_dir}/train.csv", index=False)
    val_df.to_csv(f"{output_dir}/validation.csv", index=False)
    test_df.to_csv(f"{output_dir}/test.csv", index=False)

    print("✅ Data split completed:")
    print(f"Train: {train_df.shape}")
    print(f"Validation: {val_df.shape}")
    print(f"Test: {test_df.shape}")