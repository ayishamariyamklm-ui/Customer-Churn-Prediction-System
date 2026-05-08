import os
import logging
import logging.config
import yaml


class LoggerError(Exception):
    """Custom exception for logger errors."""
    pass


def setup_logger(config_path: str = "config/logging.yaml"):
    """
    Setup logging configuration from YAML file.
    """

    try:
        if not os.path.exists(config_path):
            raise LoggerError(f"Logging config not found at: {config_path}")

        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        # Ensure logs directory exists
        log_file = config.get("handlers", {}).get("file", {}).get("filename", "logs/app.log")
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        logging.config.dictConfig(config)

    except Exception as e:
        raise LoggerError(f"Failed to setup logger: {str(e)}")


def get_logger(name: str = "churn_app") -> logging.Logger:
    """
    Get a configured logger instance.

    Ensures logger is initialized only once.
    """

    logger = logging.getLogger(name)

    if not logger.handlers:
        # Fallback basic config if setup_logger wasn't called
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    return logger