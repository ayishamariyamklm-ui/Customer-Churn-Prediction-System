import os
import json
import numpy as np
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)


class ModelEvaluationError(Exception):
    """Custom exception for evaluation errors."""
    pass


# -----------------------------------
# CORE METRICS
# -----------------------------------
def evaluate_model(model, X_test, y_test) -> dict:
    """
    Evaluate classification model.

    Returns:
        dict: evaluation metrics
    """

    try:
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]

        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall": recall_score(y_test, y_pred),
            "f1_score": f1_score(y_test, y_pred),
            "roc_auc": roc_auc_score(y_test, y_prob)
        }

        return metrics

    except Exception as e:
        raise ModelEvaluationError(f"Evaluation failed: {str(e)}")


# -----------------------------------
# CONFUSION MATRIX
# -----------------------------------
def get_confusion_matrix(model, X_test, y_test) -> np.ndarray:
    try:
        y_pred = model.predict(X_test)
        return confusion_matrix(y_test, y_pred)
    except Exception as e:
        raise ModelEvaluationError(f"Confusion matrix failed: {str(e)}")


# -----------------------------------
# CLASSIFICATION REPORT
# -----------------------------------
def get_classification_report(model, X_test, y_test) -> str:
    try:
        y_pred = model.predict(X_test)
        return classification_report(y_test, y_pred)
    except Exception as e:
        raise ModelEvaluationError(f"Report generation failed: {str(e)}")


# -----------------------------------
# SAVE METRICS
# -----------------------------------
def save_metrics(metrics: dict, path: str = "models/metrics.json"):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w") as f:
            json.dump(metrics, f, indent=4)

    except Exception as e:
        raise ModelEvaluationError(f"Saving metrics failed: {str(e)}")


# -----------------------------------
# SAVE ARTIFACTS (OPTIONAL)
# -----------------------------------
def save_confusion_matrix(cm: np.ndarray, path: str = "artifacts/confusion_matrix.csv"):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)

        df_cm = pd.DataFrame(cm)
        df_cm.to_csv(path, index=False)

    except Exception as e:
        raise ModelEvaluationError(f"Saving confusion matrix failed: {str(e)}")


# -----------------------------------
# FULL EVALUATION PIPELINE
# -----------------------------------
def full_evaluation(model, X_test, y_test):
    """
    Run full evaluation and save outputs.
    """

    metrics = evaluate_model(model, X_test, y_test)
    cm = get_confusion_matrix(model, X_test, y_test)
    report = get_classification_report(model, X_test, y_test)

    save_metrics(metrics)
    save_confusion_matrix(cm)

    return {
        "metrics": metrics,
        "confusion_matrix": cm,
        "classification_report": report
    }