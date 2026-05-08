import pandas as pd
import numpy as np

from sklearn.feature_selection import SelectKBest, chi2
from sklearn.ensemble import RandomForestClassifier


class FeatureSelectionError(Exception):
    """Custom exception for feature selection errors."""
    pass


# -----------------------------------
# REMOVE HIGHLY CORRELATED FEATURES
# -----------------------------------
def remove_high_correlation(df: pd.DataFrame, threshold: float = 0.9) -> pd.DataFrame:
    """
    Remove highly correlated numerical features.

    Args:
        df (pd.DataFrame): Input dataframe
        threshold (float): Correlation threshold

    Returns:
        pd.DataFrame: Reduced dataframe
    """

    try:
        df = df.copy()

        numeric_df = df.select_dtypes(include=[np.number])

        corr_matrix = numeric_df.corr().abs()

        upper_triangle = corr_matrix.where(
            np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
        )

        drop_cols = [
            column for column in upper_triangle.columns
            if any(upper_triangle[column] > threshold)
        ]

        df.drop(columns=drop_cols, inplace=True, errors="ignore")

        return df

    except Exception as e:
        raise FeatureSelectionError(f"Correlation removal failed: {str(e)}")


# -----------------------------------
# STATISTICAL FEATURE SELECTION
# -----------------------------------
def select_k_best_features(X: pd.DataFrame, y: pd.Series, k: int = 10):
    """
    Select top K features using chi-square test.

    Note:
    - Works best with non-negative features (after encoding)
    """

    try:
        selector = SelectKBest(score_func=chi2, k=k)
        X_new = selector.fit_transform(X, y)

        selected_features = X.columns[selector.get_support()]

        return X_new, selected_features.tolist()

    except Exception as e:
        raise FeatureSelectionError(f"KBest selection failed: {str(e)}")


# -----------------------------------
# MODEL-BASED FEATURE IMPORTANCE
# -----------------------------------
def model_based_selection(X: pd.DataFrame, y: pd.Series, threshold: float = 0.01):
    """
    Select features based on RandomForest importance.

    Args:
        threshold: minimum importance to keep feature
    """

    try:
        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )

        model.fit(X, y)

        importances = model.feature_importances_

        feature_importance_df = pd.DataFrame({
            "feature": X.columns,
            "importance": importances
        }).sort_values(by="importance", ascending=False)

        selected_features = feature_importance_df[
            feature_importance_df["importance"] > threshold
        ]["feature"].tolist()

        return selected_features, feature_importance_df

    except Exception as e:
        raise FeatureSelectionError(f"Model-based selection failed: {str(e)}")


# -----------------------------------
# FULL FEATURE SELECTION PIPELINE
# -----------------------------------
def feature_selection_pipeline(X: pd.DataFrame, y: pd.Series):
    """
    Complete feature selection workflow:
    1. Remove correlated features
    2. Apply model-based selection
    """

    try:
        # Step 1: Remove correlation
        X_reduced = remove_high_correlation(X)

        # Step 2: Model-based selection
        selected_features, importance_df = model_based_selection(X_reduced, y)

        X_final = X_reduced[selected_features]

        return X_final, selected_features, importance_df

    except Exception as e:
        raise FeatureSelectionError(f"Feature selection pipeline failed: {str(e)}")