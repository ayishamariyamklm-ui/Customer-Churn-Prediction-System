from flask import Flask, render_template, request, jsonify
import pandas as pd

from src.inference.predict_pipeline import run_prediction
from src.utils.logger import get_logger
from src.utils.exceptions import CustomException

logger = get_logger()

app = Flask(__name__)


# -----------------------------------
# HOME ROUTE
# -----------------------------------
@app.route("/", methods=["GET"])
def home():
    """
    Render homepage with input form
    """
    return render_template("index.html")


# -----------------------------------
# FORM PREDICTION (UI)
# -----------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    """
    Handle form submission and return prediction
    """

    try:
        data = request.form.to_dict()

        # Convert numeric fields
        numeric_fields = ["tenure", "MonthlyCharges", "TotalCharges"]

        for field in numeric_fields:
            if field in data:
                data[field] = float(data[field])

        logger.info(f"Received input: {data}")

        result = run_prediction(data)

        logger.info(f"Prediction result: {result}")

        return render_template(
            "index.html",
            prediction_text=f"Churn Prediction: {result['prediction']}",
            probability_text=f"Churn Probability: {result['churn_probability']}",
            risk_text=f"Risk Level: {result['churn_risk']}"
        )

    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")

        return render_template(
            "index.html",
            prediction_text="Error occurred during prediction",
            probability_text="",
            risk_text=""
        )


# -----------------------------------
# API ENDPOINT (JSON)
# -----------------------------------
@app.route("/api/predict", methods=["POST"])
def api_predict():
    """
    JSON API endpoint for predictions
    """

    try:
        data = request.get_json()

        if not data:
            raise CustomException("No JSON input provided")

        result = run_prediction(data)

        return jsonify({
            "status": "success",
            "data": result
        })

    except Exception as e:
        logger.error(f"API prediction failed: {str(e)}")

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


# -----------------------------------
# HEALTH CHECK
# -----------------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


# -----------------------------------
# ERROR HANDLER
# -----------------------------------
@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {str(e)}")

    return jsonify({
        "status": "error",
        "message": "Internal Server Error"
    }), 500