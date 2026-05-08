import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import numpy as np
from typing import Tuple, Dict, Any

from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

from src.utils.logger import get_logger


logger = get_logger()


class HyperparameterTuningError(Exception):
    """Custom exception for hyperparameter tuning errors."""
    pass


# -----------------------------------
# PARAMETER GRID
# -----------------------------------
def get_param_grid() -> Dict[str, Any]:
    """
    Define hyperparameter grid for RandomForest.
    (Note: uses pipeline naming convention: model__param)
    """

    return {
        "model__n_estimators": [100, 150, 200],
        "model__max_depth": [6, 8, 10, None],
        "model__min_samples_split": [2, 5, 10],
        "model__min_samples_leaf": [1, 2, 4]
    }


# -----------------------------------
# RANDOM SEARCH (FAST)
# -----------------------------------
def randomized_search(
    pipeline: Pipeline,
    X,
    y,
    n_iter: int = 10,
    cv: int = 3,
    scoring: str = "f1",
    random_state: int = 42
) -> Tuple[Pipeline, Dict]:

    try:
        logger.info("Starting RandomizedSearchCV...")

        param_dist = get_param_grid()

        search = RandomizedSearchCV(
            estimator=pipeline,
            param_distributions=param_dist,
            n_iter=n_iter,
            cv=cv,
            scoring=scoring,
            n_jobs=-1,
            random_state=random_state,
            verbose=1
        )

        search.fit(X, y)

        logger.info(f"Best Params: {search.best_params_}")
        logger.info(f"Best Score: {search.best_score_}")

        return search.best_estimator_, search.best_params_

    except Exception as e:
        logger.error(f"Randomized search failed: {str(e)}")
        raise HyperparameterTuningError(str(e))


# -----------------------------------
# GRID SEARCH (EXHAUSTIVE)
# -----------------------------------
def grid_search(
    pipeline: Pipeline,
    X,
    y,
    cv: int = 3,
    scoring: str = "f1"
) -> Tuple[Pipeline, Dict]:

    try:
        logger.info("Starting GridSearchCV...")

        param_grid = get_param_grid()

        search = GridSearchCV(
            estimator=pipeline,
            param_grid=param_grid,
            cv=cv,
            scoring=scoring,
            n_jobs=-1,
            verbose=1
        )

        search.fit(X, y)

        logger.info(f"Best Params: {search.best_params_}")
        logger.info(f"Best Score: {search.best_score_}")

        return search.best_estimator_, search.best_params_

    except Exception as e:
        logger.error(f"Grid search failed: {str(e)}")
        raise HyperparameterTuningError(str(e))


# -----------------------------------
# MAIN TUNING PIPELINE
# -----------------------------------
def tune_model(
    pipeline: Pipeline,
    X,
    y,
    method: str = "random"
) -> Tuple[Pipeline, Dict]:
    """
    Main entry point for hyperparameter tuning.

    Args:
        pipeline: sklearn Pipeline (preprocessor + model)
        X, y: training data
        method: 'random' or 'grid'

    Returns:
        best_model, best_params
    """

    try:
        if method == "random":
            return randomized_search(pipeline, X, y)

        elif method == "grid":
            return grid_search(pipeline, X, y)

        else:
            raise ValueError("Invalid tuning method. Use 'random' or 'grid'.")

    except Exception as e:
        raise HyperparameterTuningError(f"Tuning pipeline failed: {str(e)}")