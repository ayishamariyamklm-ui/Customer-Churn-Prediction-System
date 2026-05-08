import os
import json
import pandas as pd
from typing import Dict, Any


class HelperError(Exception):
    """Custom exception for helper utilities."""
    pass


# -----------------------------------
# FORMAT OUTPUT
# -----------------------------------
def format_output(prediction: int, probability: float) -> Dict[str, Any]:
    """
    Format prediction output in a clean, API-friendly structure.
    """

    try:
        return {
            "prediction": int(prediction),
            "churn_probability": round(float(probability), 4),
            "churn_risk": get_risk_level(probability)
        }
    except Exception as e:
        raise HelperError(f"Output formatting failed: {str(e)}")


# -----------------------------------
# RISK LEVEL CLASSIFICATION
# -----------------------------------
def get_risk_level(probability: float) -> str:
    """
    Convert churn probability into business-friendly risk levels.
    """

    try:
        if probability >= 0.75:
            return "High Risk"
        elif probability >= 0.40:
            return "Medium Risk"
        else:
            return "Low Risk"
    except Exception as e:
        raise HelperError(f"Risk level calculation failed: {str(e)}")


# -----------------------------------
# LOAD JSON
# -----------------------------------
def load_json(path: str) -> Dict:
    """
    Load JSON file safely.
    """

    try:
        if not os.path.exists(path):
            raise HelperError(f"File not found: {path}")

        with open(path, "r") as f:
            return json.load(f)

    except Exception as e:
        raise HelperError(f"JSON loading failed: {str(e)}")


# -----------------------------------
# SAVE JSON
# -----------------------------------
def save_json(data: Dict, path: str):
    """
    Save dictionary as JSON file.
    """

    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    except Exception as e:
        raise HelperError(f"JSON saving failed: {str(e)}")


# -----------------------------------
# ENSURE DIRECTORY
# -----------------------------------
def ensure_dir(path: str):
    """
    Create directory if it doesn't exist.
    """

    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        raise HelperError(f"Directory creation failed: {str(e)}")


# -----------------------------------
# DATAFRAME SUMMARY (FOR DEBUGGING)
# -----------------------------------
def dataframe_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate quick summary of dataset.
    Useful for logging and debugging.
    """

    try:
        return {
            "shape": df.shape,
            "columns": list(df.columns),
            "missing_values": df.isnull().sum().to_dict(),
            "dtypes": df.dtypes.astype(str).to_dict()
        }
    except Exception as e:
        raise HelperError(f"Dataframe summary failed: {str(e)}")