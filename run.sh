#!/bin/bash
set -e

echo "Running data cleaning..."
python3 scripts/data_cleaning.py

echo "Running Spark ingestion..."
spark-submit scripts/spark_ingestion.py

echo "Running Streaming (10 batches)..."
python3 scripts/spark_streaming.py --batches 10

echo "Running EDA visuals..."
python3 scripts/eda_visuals.py  # EDA now loads cleaned CSV, so this will work

echo "Training Sentiment Classification Model..."
python3 ml/sentiment_ml.py

echo "Training Rating Prediction Model..."
python3 ml/rating_regression.py

echo "Training Product Demand Prediction Model..."
python3 ml/product_demand_predictor.py

echo "Running Review Forecasting Model..."
python3 ml/review_forecast.py

echo "Running Topic Modeling..."
python3 ml/topic_modeling.py

echo "Launching Streamlit dashboard..."
streamlit run dashboard_app.py --server.headless true
