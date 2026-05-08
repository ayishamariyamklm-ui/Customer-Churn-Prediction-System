import os
import json
import shutil
from datetime import datetime


class ModelRegistryError(Exception):
    """Custom exception for model registry errors."""
    pass


# -----------------------------------
# CREATE VERSIONED MODEL DIRECTORY
# -----------------------------------
def create_model_version_dir(base_path: str = "models/registry") -> str:
    """
    Create a new versioned directory for model artifacts.

    Returns:
        str: Path to version directory
    """

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        version_path = os.path.join(base_path, f"model_{timestamp}")

        os.makedirs(version_path, exist_ok=True)

        return version_path

    except Exception as e:
        raise ModelRegistryError(f"Failed to create version directory: {str(e)}")


# -----------------------------------
# SAVE MODEL WITH VERSIONING
# -----------------------------------
def register_model(
    model_path: str,
    metrics: dict,
    registry_path: str = "models/registry"
):
    """
    Register a trained model with metadata.

    Args:
        model_path: Path to trained model file
        metrics: Evaluation metrics dictionary
        registry_path: Base registry directory
    """

    try:
        if not os.path.exists(model_path):
            raise ModelRegistryError(f"Model file not found: {model_path}")

        # Create version folder
        version_dir = create_model_version_dir(registry_path)

        # Copy model file
        model_filename = os.path.basename(model_path)
        dest_model_path = os.path.join(version_dir, model_filename)

        shutil.copy2(model_path, dest_model_path)

        # Save metadata
        metadata = {
            "model_name": "churn_model",
            "version": os.path.basename(version_dir),
            "registered_at": datetime.now().isoformat(),
            "metrics": metrics
        }

        metadata_path = os.path.join(version_dir, "metadata.json")

        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=4)

        return version_dir

    except Exception as e:
        raise ModelRegistryError(f"Model registration failed: {str(e)}")


# -----------------------------------
# GET LATEST MODEL VERSION
# -----------------------------------
def get_latest_model(registry_path: str = "models/registry") -> str:
    """
    Get the latest registered model path.

    Returns:
        str: Path to latest model file
    """

    try:
        if not os.path.exists(registry_path):
            raise ModelRegistryError("Registry path does not exist")

        versions = [
            d for d in os.listdir(registry_path)
            if os.path.isdir(os.path.join(registry_path, d))
        ]

        if not versions:
            raise ModelRegistryError("No models found in registry")

        latest_version = sorted(versions)[-1]

        version_dir = os.path.join(registry_path, latest_version)

        # Find model file
        for file in os.listdir(version_dir):
            if file.endswith(".pkl") or file.endswith(".joblib"):
                return os.path.join(version_dir, file)

        raise ModelRegistryError("No model file found in latest version")

    except Exception as e:
        raise ModelRegistryError(f"Failed to get latest model: {str(e)}")


# -----------------------------------
# LIST ALL REGISTERED MODELS
# -----------------------------------
def list_models(registry_path: str = "models/registry"):
    """
    List all registered models with metadata.
    """

    try:
        if not os.path.exists(registry_path):
            return []

        models = []

        for version in os.listdir(registry_path):
            version_dir = os.path.join(registry_path, version)

            metadata_path = os.path.join(version_dir, "metadata.json")

            if os.path.exists(metadata_path):
                with open(metadata_path) as f:
                    metadata = json.load(f)
                    models.append(metadata)

        return models

    except Exception as e:
        raise ModelRegistryError(f"Failed to list models: {str(e)}")