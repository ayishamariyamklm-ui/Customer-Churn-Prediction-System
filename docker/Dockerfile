# =========================================================
# CUSTOMER CHURN PREDICTION - DOCKERFILE
# =========================================================

FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p logs models artifacts reports outputs data/processed

EXPOSE 5000
EXPOSE 8000

CMD ["python", "scripts/run_app.py"]