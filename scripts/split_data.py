"""
=========================================================
CUSTOMER CHURN PREDICTION - DATA SPLITTING SCRIPT
=========================================================

Purpose:
- Load raw dataset
- Clean data using preprocessing module
- Split into train / validation / test
- Save processed datasets

Output:
data/processed/
    ├── train.csv
    ├── validation.csv
    └── test.csv
=========================================================
"""


import logging
import pandas as pd
from sklearn.model_selection import train_test_split
import yaml

import sys
import os

# Absolute project root path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from src.data.data_preprocessing import clean_data

# ---------------------------------------------------------
# LOAD PATH CONFIG
# ---------------------------------------------------------
def load_paths(config_path="config/paths.yaml"):
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


# ---------------------------------------------------------
# SETUP LOGGING
# ---------------------------------------------------------
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )


# ---------------------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------------------
def main():
    setup_logging()

    # Load config
    PATHS = load_paths()

    raw_path = PATHS["data"]["raw"]
    processed_paths = PATHS["data"]["processed"]

    train_path = processed_paths["train"]
    val_path = processed_paths["validation"]
    test_path = processed_paths["test"]

    logging.info(f"Loading raw data from: {raw_path}")

    # Load dataset
    df = pd.read_csv(raw_path)

    logging.info(f"Raw data shape: {df.shape}")

    # Clean data
    df = clean_data(df)

    logging.info("Data cleaning completed")

    # -----------------------------------------------------
    # SPLIT DATA
    # -----------------------------------------------------
    train_df, temp_df = train_test_split(
        df,
        test_size=0.3,
        random_state=42,
        stratify=df["Churn"]
    )

    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.5,
        random_state=42,
        stratify=temp_df["Churn"]
    )

    logging.info(f"Train shape: {train_df.shape}")
    logging.info(f"Validation shape: {val_df.shape}")
    logging.info(f"Test shape: {test_df.shape}")

    # -----------------------------------------------------
    # SAVE FILES
    # -----------------------------------------------------
    os.makedirs(os.path.dirname(train_path), exist_ok=True)

    train_df.to_csv(train_path, index=False)
    val_df.to_csv(val_path, index=False)
    test_df.to_csv(test_path, index=False)

    logging.info("✅ Data split and saved successfully!")


# ---------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------
if __name__ == "__main__":
    main()