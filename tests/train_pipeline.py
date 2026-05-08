# =========================================================
# CUSTOMER CHURN PREDICTION - TRAINING PIPELINE
# =========================================================

import os
import yaml
import json
import logging
import warnings

import pandas as pd
import numpy as np
import joblib

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
    roc_curve,
    auc
)

warnings.filterwarnings("ignore")


# =========================================================
# LOAD CONFIGS
# =========================================================
def load_yaml(path: str):
    """
    Load YAML configuration file.
    """
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
logger = logging.getLogger("training_pipeline")


# =========================================================
# LOAD DATA
# =========================================================
def load_data(path: str) -> pd.DataFrame:
    """
    Load dataset from CSV.
    """
    logger.info(f"Loading data from: {path}")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found: {path}")

    df = pd.read_csv(path)

    logger.info(f"Dataset shape: {df.shape}")

    return df


# =========================================================
# PREPROCESSOR
# =========================================================
def build_preprocessor(numerical_features, categorical_features):
    """
    Build preprocessing pipeline for numeric and categorical features.
    """

    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_pipeline, numerical_features),
        ("cat", categorical_pipeline, categorical_features)
    ])

    return preprocessor


# =========================================================
# MODEL FACTORY
# =========================================================
def get_models():
    """
    Return candidate models for comparison.
    """

    return {
        "logistic_regression": LogisticRegression(
            max_iter=1000,
            random_state=42
        ),

        "random_forest": RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        ),

        "gradient_boosting": GradientBoostingClassifier(
            n_estimators=150,
            learning_rate=0.1,
            max_depth=3,
            random_state=42
        )
    }


# =========================================================
# EVALUATION
# =========================================================
def evaluate_model(model, X_test, y_test) -> dict:
    """
    Evaluate trained model.
    """

    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, preds),
        "precision": precision_score(y_test, preds),
        "recall": recall_score(y_test, preds),
        "f1": f1_score(y_test, preds),
        "roc_auc": roc_auc_score(y_test, probs)
    }

    logger.info(f"Evaluation metrics: {metrics}")
    logger.info("\n" + classification_report(y_test, preds))

    return metrics


# =========================================================
# FEATURE NAME EXTRACTION
# =========================================================
def get_feature_names_from_preprocessor(preprocessor):
    """
    Extract feature names after ColumnTransformer transformation.
    """

    feature_names = []

    for name, transformer, columns in preprocessor.transformers_:

        if name == "remainder":
            continue

        if hasattr(transformer, "named_steps"):
            last_step = list(transformer.named_steps.values())[-1]

            if hasattr(last_step, "get_feature_names_out"):
                names = last_step.get_feature_names_out(columns)
            else:
                names = columns

        elif hasattr(transformer, "get_feature_names_out"):
            names = transformer.get_feature_names_out(columns)

        else:
            names = columns

        feature_names.extend(names)

    return feature_names


# =========================================================
# SAVE FEATURE IMPORTANCE PLOT
# =========================================================
def save_feature_importance_plot(model_pipeline, output_path: str, top_n: int = 20):
    """
    Save feature importance plot for tree-based models.
    """

    try:
        preprocessor = model_pipeline.named_steps["preprocessor"]
        model = model_pipeline.named_steps["model"]

        if not hasattr(model, "feature_importances_"):
            logger.warning(
                "Feature importance plot skipped because selected model "
                "does not support feature_importances_."
            )
            return

        feature_names = get_feature_names_from_preprocessor(preprocessor)
        importances = model.feature_importances_

        importance_df = pd.DataFrame({
            "feature": feature_names,
            "importance": importances
        }).sort_values(by="importance", ascending=False).head(top_n)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        plt.figure(figsize=(12, 8))
        sns.barplot(
            data=importance_df,
            x="importance",
            y="feature"
        )
        plt.title("Top Feature Importances")
        plt.xlabel("Importance")
        plt.ylabel("Feature")
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        logger.info(f"Feature importance plot saved at: {output_path}")

    except Exception as e:
        logger.error(f"Failed to save feature importance plot: {str(e)}")


# =========================================================
# SAVE CONFUSION MATRIX PLOT
# =========================================================
def save_confusion_matrix_plot(model_pipeline, X_test, y_test, output_path: str):
    """
    Save confusion matrix heatmap.
    """

    try:
        preds = model_pipeline.predict(X_test)
        cm = confusion_matrix(y_test, preds)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        plt.figure(figsize=(6, 5))
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=["No Churn", "Churn"],
            yticklabels=["No Churn", "Churn"]
        )
        plt.title("Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        logger.info(f"Confusion matrix plot saved at: {output_path}")

    except Exception as e:
        logger.error(f"Failed to save confusion matrix plot: {str(e)}")


# =========================================================
# SAVE ROC CURVE
# =========================================================
def save_roc_curve_plot(model_pipeline, X_test, y_test, output_path: str):
    """
    Save ROC curve plot.
    """

    try:
        probs = model_pipeline.predict_proba(X_test)[:, 1]

        fpr, tpr, _ = roc_curve(y_test, probs)
        roc_auc = auc(fpr, tpr)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        plt.figure(figsize=(7, 5))
        plt.plot(fpr, tpr, label=f"ROC-AUC = {roc_auc:.3f}")
        plt.plot([0, 1], [0, 1], linestyle="--")
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("ROC Curve")
        plt.legend(loc="lower right")
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        logger.info(f"ROC curve plot saved at: {output_path}")

    except Exception as e:
        logger.error(f"Failed to save ROC curve plot: {str(e)}")


# =========================================================
# SAVE SHAP SUMMARY PLOT
# =========================================================
def save_shap_summary_plot(model_pipeline, X_sample, output_path: str, max_samples: int = 300):
    """
    Save SHAP summary plot for tree-based models.
    """

    try:
        import shap

        preprocessor = model_pipeline.named_steps["preprocessor"]
        model = model_pipeline.named_steps["model"]

        supported_tree_models = [
            "RandomForestClassifier",
            "GradientBoostingClassifier"
        ]

        if model.__class__.__name__ not in supported_tree_models:
            logger.warning(
                "SHAP summary skipped because selected model is not tree-based."
            )
            return

        X_sample = X_sample.copy().head(max_samples)

        X_transformed = preprocessor.transform(X_sample)

        if hasattr(X_transformed, "toarray"):
            X_transformed = X_transformed.toarray()

        feature_names = get_feature_names_from_preprocessor(preprocessor)

        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_transformed)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        plt.figure()

        if isinstance(shap_values, list):
            shap.summary_plot(
                shap_values[1],
                X_transformed,
                feature_names=feature_names,
                show=False
            )
        else:
            shap.summary_plot(
                shap_values,
                X_transformed,
                feature_names=feature_names,
                show=False
            )

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        logger.info(f"SHAP summary plot saved at: {output_path}")

    except ImportError:
        logger.warning(
            "SHAP is not installed. Install it using: pip install shap"
        )

    except Exception as e:
        logger.error(f"Failed to save SHAP summary plot: {str(e)}")


# =========================================================
# SAVE METRICS JSON
# =========================================================
def save_metrics_json(
    results: dict,
    best_name: str,
    best_score: float,
    X_train,
    X_test,
    X,
    output_path: str
):
    """
    Save training metrics and model comparison as JSON.
    """

    final_metrics = {
        "best_model": best_name,
        "selection_metric": "roc_auc",
        "best_score": float(best_score),
        "models": {},
        "dataset": {
            "train_size": int(X_train.shape[0]),
            "test_size": int(X_test.shape[0]),
            "total_features": int(X.shape[1])
        },
        "notes": {
            "business_priority": "recall",
            "reason": "Missing churn customers is more costly than false positives",
            "class_imbalance_handling": "stratified train-test split"
        }
    }

    for name, data in results.items():
        final_metrics["models"][name] = {
            "accuracy": float(data["metrics"]["accuracy"]),
            "precision": float(data["metrics"]["precision"]),
            "recall": float(data["metrics"]["recall"]),
            "f1_score": float(data["metrics"]["f1"]),
            "roc_auc": float(data["metrics"]["roc_auc"]),
            "cv_score": float(data["cv_score"])
        }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(final_metrics, f, indent=4)

    logger.info(f"Metrics JSON saved at: {output_path}")


# =========================================================
# MAIN PIPELINE
# =========================================================
def main():

    # -------------------------
    # Load Data
    # -------------------------
    df = load_data(PATHS["data"]["raw"])

    target = CONFIG["data"]["target_column"]

    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found in dataset.")

    # -------------------------
    # Basic Cleaning
    # -------------------------
    if "customerID" in df.columns:
        df.drop("customerID", axis=1, inplace=True)

    df[target] = df[target].map({"Yes": 1, "No": 0})

    if df[target].isnull().sum() > 0:
        raise ValueError("Target column contains invalid values after mapping.")

    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    # -------------------------
    # Features
    # Supports both numeric_features and numerical_features
    # -------------------------
    numerical_features = CONFIG["features"].get(
        "numeric_features",
        CONFIG["features"].get("numerical_features")
    )

    categorical_features = CONFIG["features"]["categorical_features"]

    if numerical_features is None:
        raise KeyError(
            "Numerical features not found. Use either "
            "'numeric_features' or 'numerical_features' in config.yaml."
        )

    X = df.drop(columns=[target])
    y = df[target]

    # -------------------------
    # Train-Test Split
    # -------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=CONFIG["data"]["test_size"],
        random_state=CONFIG["data"]["random_state"],
        stratify=y
    )

    logger.info(f"Train shape: {X_train.shape}")
    logger.info(f"Test shape: {X_test.shape}")

    # -------------------------
    # Preprocessor
    # -------------------------
    preprocessor = build_preprocessor(
        numerical_features,
        categorical_features
    )

    # -------------------------
    # Train Models
    # -------------------------
    models = get_models()

    best_model = None
    best_score = -1
    best_name = None
    results = {}

    for name, model in models.items():

        logger.info(f"Training model: {name}")

        pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("model", model)
        ])

        pipeline.fit(X_train, y_train)

        cv_scores = cross_val_score(
            pipeline,
            X_train,
            y_train,
            cv=5,
            scoring="roc_auc"
        )

        cv_score = np.mean(cv_scores)

        logger.info(f"{name} CV ROC-AUC: {cv_score:.4f}")

        metrics = evaluate_model(pipeline, X_test, y_test)

        results[name] = {
            "metrics": metrics,
            "cv_score": float(cv_score)
        }

        if metrics["roc_auc"] > best_score:
            best_score = metrics["roc_auc"]
            best_model = pipeline
            best_name = name

    logger.info(f"Best Model: {best_name} | ROC-AUC: {best_score:.4f}")

    if best_model is None:
        raise RuntimeError("No best model was selected. Training failed.")

    # -------------------------
    # Save Model Artifacts
    # -------------------------
    models_dir = PATHS["models"].get(
        "dir",
        PATHS["models"].get("model_dir", "models")
    )

    os.makedirs(models_dir, exist_ok=True)

    model_path = PATHS["models"]["trained_model"]
    preprocessor_path = PATHS["models"]["preprocessor"]
    metrics_path = PATHS["models"].get(
        "metrics",
        os.path.join(models_dir, "metrics.json")
    )

    joblib.dump(best_model, model_path)
    joblib.dump(best_model.named_steps["preprocessor"], preprocessor_path)

    logger.info(f"Model saved at: {model_path}")
    logger.info(f"Preprocessor saved at: {preprocessor_path}")

    # Also save best_model.pkl if configured
    if "best_model" in PATHS["models"]:
        joblib.dump(best_model, PATHS["models"]["best_model"])
        logger.info(f"Best model copy saved at: {PATHS['models']['best_model']}")

    # -------------------------
    # Save Metrics JSON
    # -------------------------
    save_metrics_json(
        results=results,
        best_name=best_name,
        best_score=best_score,
        X_train=X_train,
        X_test=X_test,
        X=X,
        output_path=metrics_path
    )

    # -------------------------
    # Save Visualization Artifacts
    # -------------------------
    save_feature_importance_plot(
        best_model,
        PATHS["artifacts"]["feature_importance"]
    )

    save_confusion_matrix_plot(
        best_model,
        X_test,
        y_test,
        PATHS["artifacts"]["confusion_matrix"]
    )

    if "roc_curve" in PATHS["artifacts"]:
        save_roc_curve_plot(
            best_model,
            X_test,
            y_test,
            PATHS["artifacts"]["roc_curve"]
        )

    save_shap_summary_plot(
        best_model,
        X_test,
        PATHS["artifacts"]["shap_summary"]
    )

    logger.info("Training pipeline completed successfully.")


# =========================================================
# ENTRY POINT
# =========================================================
if __name__ == "__main__":
    main()