# =========================================================
# CUSTOMER CHURN PREDICTION - MODEL EVALUATION PIPELINE
# =========================================================

import os
import yaml
import json
import joblib
import logging
import pandas as pd
import numpy as np

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
    roc_curve
)

import matplotlib.pyplot as plt


# =========================================================
# CONFIG LOADING
# =========================================================
def load_yaml(path):
    with open(path, "r") as file:
        return yaml.safe_load(file)


CONFIG = load_yaml("config/config.yaml")
PATHS = load_yaml("config/paths.yaml")


# =========================================================
# LOGGER SETUP
# =========================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("evaluate_model")


# =========================================================
# LOAD DATA
# =========================================================
def load_data(path):
    logger.info(f"Loading data from: {path}")
    return pd.read_csv(path)


# =========================================================
# LOAD MODEL
# =========================================================
def load_model(path):
    logger.info(f"Loading model from: {path}")
    return joblib.load(path)


# =========================================================
# EVALUATION METRICS
# =========================================================
def evaluate(y_true, y_pred, y_proba=None):

    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, pos_label=1),
        "recall": recall_score(y_true, y_pred, pos_label=1),
        "f1_score": f1_score(y_true, y_pred, pos_label=1)
    }

    if y_proba is not None:
        metrics["roc_auc"] = roc_auc_score(y_true, y_proba)

    return metrics


# =========================================================
# PLOT CONFUSION MATRIX
# =========================================================
def plot_confusion_matrix(cm, save_path):

    plt.figure()
    plt.imshow(cm, interpolation="nearest")
    plt.title("Confusion Matrix")
    plt.colorbar()

    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    plt.savefig(save_path)
    plt.close()

    logger.info(f"Confusion matrix saved at: {save_path}")


# =========================================================
# PLOT ROC CURVE
# =========================================================
def plot_roc_curve(y_true, y_proba, save_path):

    fpr, tpr, _ = roc_curve(y_true, y_proba)

    plt.figure()
    plt.plot(fpr, tpr, label="ROC Curve")
    plt.plot([0, 1], [0, 1], linestyle="--")

    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend()

    plt.savefig(save_path)
    plt.close()

    logger.info(f"ROC curve saved at: {save_path}")


# =========================================================
# MAIN EVALUATION PIPELINE
# =========================================================
def main():

    # -------------------------
    # Load test data
    # -------------------------
    test_path = PATHS["data"]["processed"]["test"]
    df = load_data(test_path)

    target = CONFIG["data"]["target_column"]

    X_test = df.drop(columns=[target])
    y_test = df[target]

    # -------------------------
    # Load trained model
    # -------------------------
    model_path = PATHS["models"]["trained_model"]
    model = load_model(model_path)

    # -------------------------
    # Predictions
    # -------------------------
    logger.info("Running predictions...")
    y_pred = model.predict(X_test)

    y_proba = None
    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_test)[:, 1]

    # -------------------------
    # Metrics
    # -------------------------
    logger.info("Calculating metrics...")
    metrics = evaluate(y_test, y_pred, y_proba)

    logger.info(f"Evaluation Metrics: {metrics}")
    logger.info("\n" + classification_report(y_test, y_pred))

    # -------------------------
    # Save metrics
    # -------------------------
    metrics_path = PATHS["reports"]["metrics"] + "evaluation_metrics.json"
    os.makedirs(os.path.dirname(metrics_path), exist_ok=True)

    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=4)

    logger.info(f"Metrics saved at: {metrics_path}")

    # -------------------------
    # Confusion Matrix
    # -------------------------
    cm = confusion_matrix(y_test, y_pred)
    cm_path = PATHS["reports"]["confusion_matrix"]

    os.makedirs(os.path.dirname(cm_path), exist_ok=True)
    plot_confusion_matrix(cm, cm_path)

    # -------------------------
    # ROC Curve
    # -------------------------
    if y_proba is not None:
        roc_path = PATHS["reports"]["roc_curve"]
        plot_roc_curve(y_test, y_proba, roc_path)

    logger.info("Model evaluation completed successfully.")


# =========================================================
# ENTRY POINT
# =========================================================
if __name__ == "__main__":
    main()