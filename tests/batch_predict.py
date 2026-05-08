# =========================================================
# CUSTOMER CHURN - BATCH PREDICTION SCRIPT
# =========================================================

import os
import sys
import yaml
import logging
import pandas as pd
import joblib


# =========================================================
# LOAD CONFIGS
# =========================================================
def load_yaml(path):
    with open(path, "r") as file:
        return yaml.safe_load(file)


CONFIG = load_yaml("config/config.yaml")
PATHS = load_yaml("config/paths.yaml")


# =========================================================
# LOGGER
# =========================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("batch_predict")


# =========================================================
# LOAD MODEL
# =========================================================
def load_model(model_path):
    logger.info(f"Loading model from: {model_path}")
    model = joblib.load(model_path)
    return model


# =========================================================
# PREPROCESS INPUT
# =========================================================
def preprocess_input(df):
    target = CONFIG["data"]["target_column"]

    # Drop target if accidentally present
    if target in df.columns:
        df = df.drop(columns=[target])

    # Drop ID if exists
    if "customerID" in df.columns:
        df = df.drop(columns=["customerID"])

    # Convert numeric safely
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    return df


# =========================================================
# RISK CLASSIFICATION
# =========================================================
def classify_risk(prob):
    if prob >= 0.7:
        return "High Risk"
    elif prob >= 0.4:
        return "Medium Risk"
    else:
        return "Low Risk"


# =========================================================
# BATCH PREDICT
# =========================================================
def batch_predict(input_path, output_path):

    # Load model
    model = load_model(PATHS["models"]["trained_model"])

    # Load data
    logger.info(f"Reading input file: {input_path}")
    df = pd.read_csv(input_path)

    # Keep copy for output
    output_df = df.copy()

    # Preprocess
    df_processed = preprocess_input(df)

    # Predict
    logger.info("Running predictions...")
    predictions = model.predict(df_processed)
    probabilities = model.predict_proba(df_processed)[:, 1]

    # Append results
    output_df["prediction"] = predictions
    output_df["churn_probability"] = probabilities
    output_df["risk_level"] = [classify_risk(p) for p in probabilities]

    # Save output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    output_df.to_csv(output_path, index=False)

    logger.info(f"Batch predictions saved to: {output_path}")


# =========================================================
# CLI ENTRY
# =========================================================
if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: python scripts/batch_predict.py <input_csv> <output_csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    batch_predict(input_file, output_file)