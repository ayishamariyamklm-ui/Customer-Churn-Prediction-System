import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import pandas as pd
from typing import Dict, List, Union

from src.inference.model_inference import predict_single, predict_batch
from src.utils.logger import get_logger
from src.utils.helpers import format_output
from src.utils.exceptions import CustomException


logger = get_logger()


EXPECTED_COLUMNS = [
    "tenure",
    "MonthlyCharges",
    "TotalCharges",
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
]


DEFAULT_VALUES = {
    "tenure": 0,
    "MonthlyCharges": 0.0,
    "TotalCharges": 0.0,
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "No",
    "Dependents": "No",
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "No",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Credit card (automatic)",
}


def align_input_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure prediction input contains all columns used during training.
    """

    df = df.copy()

    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = DEFAULT_VALUES[col]

    return df[EXPECTED_COLUMNS]


class PredictionPipeline:
    """
    High-level prediction pipeline.

    Responsibilities:
    - Validate and normalize input
    - Align input columns with training features
    - Call inference layer
    - Format output
    """

    def __init__(self):
        pass

    def _prepare_input(
        self,
        data: Union[Dict, List[Dict], pd.DataFrame]
    ) -> Union[Dict, pd.DataFrame]:

        try:
            if isinstance(data, dict):
                df = pd.DataFrame([data])
                df = align_input_features(df)
                return df.iloc[0].to_dict()

            elif isinstance(data, list):
                df = pd.DataFrame(data)
                return align_input_features(df)

            elif isinstance(data, pd.DataFrame):
                return align_input_features(data)

            else:
                raise CustomException(
                    "Invalid input format. Use dict, list of dicts, or DataFrame."
                )

        except Exception as e:
            logger.error(f"Input preparation failed: {str(e)}")
            raise CustomException(str(e))

    def predict(
        self,
        data: Union[Dict, List[Dict], pd.DataFrame]
    ) -> Union[Dict, List[Dict]]:

        try:
            prepared_data = self._prepare_input(data)

            if isinstance(prepared_data, dict):
                result = predict_single(prepared_data)

                return format_output(
                    result["prediction"],
                    result["churn_probability"]
                )

            else:
                results = predict_batch(prepared_data)

                formatted_results = [
                    format_output(
                        r["prediction"],
                        r["churn_probability"]
                    )
                    for r in results
                ]

                return formatted_results

        except Exception as e:
            logger.error(f"Prediction pipeline failed: {str(e)}")
            raise CustomException(str(e))


def run_prediction(
    data: Union[Dict, List[Dict], pd.DataFrame]
):
    """
    Simple function wrapper for quick usage.
    """

    pipeline = PredictionPipeline()
    return pipeline.predict(data)