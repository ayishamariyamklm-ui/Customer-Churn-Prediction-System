import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder


class FeatureEngineeringError(Exception):
    pass


# -----------------------------------
# FEATURE CREATION
# -----------------------------------
def create_features(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df = df.copy()

        # Ensure numeric conversion (important for Telco dataset)
        if "TotalCharges" in df.columns:
            df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

        # Avg monthly charge
        if "TotalCharges" in df.columns and "tenure" in df.columns:
            df["AvgChargesPerMonth"] = df["TotalCharges"] / (df["tenure"] + 1)

        # Tenure groups
        if "tenure" in df.columns:
            df["TenureGroup"] = pd.cut(
                df["tenure"],
                bins=[0, 12, 24, 48, 60, 100],
                labels=["0-1yr", "1-2yr", "2-4yr", "4-5yr", "5+yr"]
            )

        # Service count
        service_cols = [
            "PhoneService", "MultipleLines", "InternetService",
            "OnlineSecurity", "OnlineBackup", "DeviceProtection",
            "TechSupport", "StreamingTV", "StreamingMovies"
        ]

        existing_services = [col for col in service_cols if col in df.columns]

        if existing_services:
            df["TotalServices"] = df[existing_services].apply(
                lambda x: sum(val != "No" for val in x), axis=1
            )

        return df

    except Exception as e:
        raise FeatureEngineeringError(f"Error in feature creation: {str(e)}")


# -----------------------------------
# PREPROCESSOR BUILDER
# -----------------------------------
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline


def build_preprocessor(df: pd.DataFrame) -> ColumnTransformer:
    try:
        df = df.copy()

        numeric_features = [
            col for col in df.select_dtypes(include=["int64", "float64"]).columns
            if col != "Churn"
        ]

        categorical_features = [
            col for col in df.select_dtypes(include=["object", "category"]).columns
            if col != "Churn"
        ]

        # ✅ NUMERIC PIPELINE
        numeric_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ])

        # ✅ CATEGORICAL PIPELINE
        categorical_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            ))
        ])

        # ✅ COMBINE
        preprocessor = ColumnTransformer([
            ("num", numeric_pipeline, numeric_features),
            ("cat", categorical_pipeline, categorical_features),
        ])

        return preprocessor

    except Exception as e:
        raise FeatureEngineeringError(f"Error building preprocessor: {str(e)}")


# -----------------------------------
# FULL FEATURE PIPELINE
# -----------------------------------
def feature_pipeline(df: pd.DataFrame):
    df = create_features(df)
    preprocessor = build_preprocessor(df)
    return df, preprocessor