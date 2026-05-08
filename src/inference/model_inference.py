import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import joblib
import pandas as pd

from typing import Dict, List, Union

from src.utils.logger import get_logger
from src.utils.exceptions import CustomException

# Optional: if using model registry
try:
    from src.models.model_registry import get_latest_model
    REGISTRY_AVAILABLE = True
except ImportError:
    REGISTRY_AVAILABLE = False


logger = get_logger()


# -----------------------------------
# LOAD MODEL
# -----------------------------------
def load_model(model_path: str = "models/churn_model.pkl"):
    """
    Load trained model from disk or registry.
    """

    try:
        if REGISTRY_AVAILABLE and not os.path.exists(model_path):
            logger.info("Loading latest model from registry...")
            model_path = get_latest_model()

        if not os.path.exists(model_path):
            raise CustomException(f"Model not found at path: {model_path}")

        model = joblib.load(model_path)

        logger.info(f"Model loaded successfully from {model_path}")

        return model

    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise CustomException(str(e))


# -----------------------------------
# VALIDATE INPUT
# -----------------------------------
def validate_input(data: Dict):
    """
    Validate incoming prediction data.
    """

    required_fields = [
        "tenure",
        "MonthlyCharges",
        "TotalCharges"
    ]

    missing = [field for field in required_fields if field not in data]

    if missing:
        raise CustomException(f"Missing required fields: {missing}")


# -----------------------------------
# SINGLE PREDICTION
# -----------------------------------
def predict_single(data: Dict) -> Dict:
    """
    Predict churn for a single customer.

    Returns:
        dict with prediction and probability
    """

    try:
        validate_input(data)

        model = load_model()

        df = pd.DataFrame([data])

        pred = model.predict(df)[0]
        prob = model.predict_proba(df)[0][1]

        result = {
            "prediction": int(pred),
            "churn_probability": round(float(prob), 4)
        }

        return result

    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise CustomException(str(e))


# -----------------------------------
# BATCH PREDICTION
# -----------------------------------
def predict_batch(data: Union[List[Dict], pd.DataFrame]) -> List[Dict]:
    """
    Predict churn for multiple customers.
    """

    try:
        model = load_model()

        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, pd.DataFrame):
            df = data.copy()
        else:
            raise CustomException("Input must be list of dicts or DataFrame")

        preds = model.predict(df)
        probs = model.predict_proba(df)[:, 1]

        results = []

        for p, pr in zip(preds, probs):
            results.append({
                "prediction": int(p),
                "churn_probability": round(float(pr), 4)
            })

        return results

    except Exception as e:
        logger.error(f"Batch prediction failed: {str(e)}")
        raise CustomException(str(e))


# -----------------------------------
# GENERIC PREDICT (AUTO DETECT)
# -----------------------------------
def predict(data: Union[Dict, List[Dict], pd.DataFrame]):
    """
    Unified prediction function.
    """

    if isinstance(data, dict):
        return predict_single(data)

    return predict_batch(data)