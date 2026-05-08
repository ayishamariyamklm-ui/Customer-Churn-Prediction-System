from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Union

from src.inference.predict_pipeline import run_prediction
from src.utils.logger import get_logger
from src.utils.exceptions import CustomException


logger = get_logger()

app = FastAPI(
    title="Customer Churn Prediction API",
    description="Predict whether a customer will churn",
    version="1.0.0"
)


# -----------------------------------
# REQUEST SCHEMA
# -----------------------------------
class CustomerData(BaseModel):
    tenure: float = Field(..., example=5)
    MonthlyCharges: float = Field(..., example=70)
    TotalCharges: float = Field(..., example=350)

    # Optional categorical fields
    gender: str | None = None
    SeniorCitizen: int | None = None
    Partner: str | None = None
    Dependents: str | None = None
    PhoneService: str | None = None
    MultipleLines: str | None = None
    InternetService: str | None = None
    OnlineSecurity: str | None = None
    OnlineBackup: str | None = None
    DeviceProtection: str | None = None
    TechSupport: str | None = None
    StreamingTV: str | None = None
    StreamingMovies: str | None = None
    Contract: str | None = None
    PaperlessBilling: str | None = None
    PaymentMethod: str | None = None


# -----------------------------------
# ROOT ENDPOINT
# -----------------------------------
@app.get("/")
def root():
    return {
        "message": "Customer Churn Prediction API is running",
        "status": "success"
    }


# -----------------------------------
# HEALTH CHECK
# -----------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# -----------------------------------
# SINGLE PREDICTION
# -----------------------------------
@app.post("/predict")
def predict(data: CustomerData):
    """
    Predict churn for a single customer
    """

    try:
        input_data = data.dict()

        logger.info(f"Received input: {input_data}")

        result = run_prediction(input_data)

        logger.info(f"Prediction result: {result}")

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )


# -----------------------------------
# BATCH PREDICTION
# -----------------------------------
@app.post("/predict_batch")
def predict_batch(data: List[CustomerData]):
    """
    Predict churn for multiple customers
    """

    try:
        input_data = [item.dict() for item in data]

        logger.info(f"Received batch input: {len(input_data)} records")

        results = run_prediction(input_data)

        return {
            "status": "success",
            "count": len(results),
            "data": results
        }

    except Exception as e:
        logger.error(f"Batch prediction failed: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Batch prediction failed"
        )


# -----------------------------------
# ERROR HANDLER
# -----------------------------------
@app.exception_handler(CustomException)
def custom_exception_handler(request, exc: CustomException):
    return {
        "status": "error",
        "message": str(exc)
    }