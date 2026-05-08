import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import joblib
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from src.data.data_loader import load_data
from src.data.data_preprocessing import clean_data
from src.data.data_validation import validate_dataframe
from src.features.feature_engineering import create_features, build_preprocessor
from src.utils.logger import get_logger


logger = get_logger()


class ModelTrainingError(Exception):
    """Custom exception for model training errors."""
    pass


def train_model(
    data_path: str,
    model_output_path: str = "models/churn_model.pkl",
    test_size: float = 0.2,
    random_state: int = 42
):
    """
    Train churn prediction model.

    Steps:
    - Load data
    - Validate data
    - Clean + feature engineer
    - Split data
    - Train pipeline
    - Save model

    Returns:
        pipeline, X_test, y_test
    """

    try:
        # ---------------------------
        # LOAD DATA
        # ---------------------------
        logger.info("Loading data...")
        df = load_data(data_path)

        # ---------------------------
        # VALIDATE DATA
        # ---------------------------
        logger.info("Validating data...")
        validate_dataframe(df)

        # ---------------------------
        # CLEAN DATA
        # ---------------------------
        logger.info("Cleaning data...")
        df = clean_data(df)

        # ---------------------------
        # FEATURE ENGINEERING
        # ---------------------------
        logger.info("Creating features...")
        df = create_features(df)

        # ---------------------------
        # SPLIT FEATURES & TARGET
        # ---------------------------
        X = df.drop("Churn", axis=1)
        y = df["Churn"]

        # ---------------------------
        # PREPROCESSOR
        # ---------------------------
        logger.info("Building preprocessing pipeline...")
        preprocessor = build_preprocessor(df)

        # ---------------------------
        # MODEL
        # ---------------------------
        model = RandomForestClassifier(
            n_estimators=150,
            max_depth=8,
            random_state=random_state,
            n_jobs=-1
        )

        # ---------------------------
        # FULL PIPELINE
        # ---------------------------
        pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("model", model)
        ])

        # ---------------------------
        # TRAIN TEST SPLIT
        # ---------------------------
        logger.info("Splitting dataset...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=test_size,
            random_state=random_state,
            stratify=y
        )

        # ---------------------------
        # TRAIN MODEL
        # ---------------------------
        logger.info("Training model...")
        pipeline.fit(X_train, y_train)

        # ---------------------------
        # SAVE MODEL
        # ---------------------------
        os.makedirs(os.path.dirname(model_output_path), exist_ok=True)

        joblib.dump(pipeline, model_output_path)
        logger.info(f"Model saved at {model_output_path}")

        return pipeline, X_test, y_test

    except Exception as e:
        logger.error(f"Model training failed: {str(e)}")
        raise ModelTrainingError(str(e))


# -----------------------------------
# FEATURE IMPORTANCE (POST TRAINING)
# -----------------------------------
def get_feature_importance(pipeline, feature_names):
    """
    Extract feature importance from trained RandomForest model.
    """

    try:
        model = pipeline.named_steps["model"]

        importances = model.feature_importances_

        importance_df = pd.DataFrame({
            "feature": feature_names,
            "importance": importances
        }).sort_values(by="importance", ascending=False)

        return importance_df

    except Exception as e:
        raise ModelTrainingError(f"Feature importance extraction failed: {str(e)}")