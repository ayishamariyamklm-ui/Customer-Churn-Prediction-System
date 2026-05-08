import os
import pandas as pd

from src.utils.logger import get_logger

logger = get_logger()


class DataLoaderError(Exception):
    """Custom exception for data loading errors."""
    pass


def load_csv(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame with validation.

    Args:
        file_path (str): Path to CSV file

    Returns:
        pd.DataFrame: Loaded dataset
    """

    try:
        if not os.path.exists(file_path):
            raise DataLoaderError(f"File not found: {file_path}")

        if not file_path.endswith(".csv"):
            raise DataLoaderError("Only CSV files are supported")

        logger.info(f"Loading data from {file_path}")

        df = pd.read_csv(file_path)

        if df.empty:
            raise DataLoaderError("Loaded dataset is empty")

        logger.info(f"Data loaded successfully with shape: {df.shape}")

        return df

    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise DataLoaderError(str(e))


def load_data(file_path: str) -> pd.DataFrame:
    """
    Wrapper function for loading data.
    Allows future extension (DB, API, etc.)
    """

    return load_csv(file_path)


def save_processed_data(df: pd.DataFrame, output_path: str):
    """
    Save processed dataset to disk.

    Args:
        df (pd.DataFrame): Processed data
        output_path (str): Save location
    """

    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        df.to_csv(output_path, index=False)

        logger.info(f"Processed data saved to {output_path}")

    except Exception as e:
        logger.error(f"Error saving data: {str(e)}")
        raise DataLoaderError(str(e))