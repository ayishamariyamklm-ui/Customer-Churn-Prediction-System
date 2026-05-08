import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import yaml
sys.stdout.reconfigure(encoding='utf-8')
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging FIRST
from src.utils.logger import setup_logger, get_logger

setup_logger()
logger = get_logger()

# Import app AFTER logger setup
from app.web_app import app


# -----------------------------------
# LOAD CONFIG
# -----------------------------------
def load_config(config_path="config/config.yaml"):
    try:
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, "r") as f:
            return yaml.safe_load(f)

    except Exception as e:
        logger.error(f"Failed to load config: {str(e)}")
        raise


# -----------------------------------
# RUN APPLICATION
# -----------------------------------
def run():
    try:
        config = load_config()

        host = config["api"]["host"]
        port = config["api"]["port"]
        debug = config["api"]["debug"]

        logger.info(" Starting Customer Churn Web App...")
        logger.info(f"Host: {host}, Port: {port}, Debug: {debug}")

        app.run(host=host, port=port, debug=debug)

    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise


# -----------------------------------
# ENTRY POINT
# -----------------------------------
if __name__ == "__main__":
    run()