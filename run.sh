#!/bin/bash
set -e

echo "====================================================="
echo " AMAZON CUSTOMER REVIEWS ANALYTICS - FULL PIPELINE"
echo "====================================================="

echo ""
echo "📌 STEP 1 — Running Data Cleaning..."
python3 scripts/data_cleaning.py
echo "✔ Data cleaning completed."
echo ""

echo "📌 STEP 2 — Running Spark Batch Ingestion..."
spark-submit scripts/spark_ingestion.py
echo "✔ Spark ingestion completed."
echo ""

echo "📌 STEP 3 — Running Spark Streaming (10 batches)..."
python3 scripts/spark_streaming.py --batches 10
echo "✔ Streaming simulation completed."
echo ""

echo "📌 STEP 4 — Generating EDA Visuals..."
python3 scripts/eda_visuals.py   # EDA loads cleaned CSV
echo "✔ EDA visuals generated."
echo ""

echo "📌 STEP 5 — Training Sentiment Classification Model..."
python3 ml/sentiment_ml.py
echo "✔ Sentiment model trained."
echo ""

echo "📌 STEP 6 — Training Rating Prediction Model..."
python3 ml/rating_regression.py
echo "✔ Rating prediction model trained."
echo ""

echo "📌 STEP 7 — Training Product Demand Prediction Model..."
python3 ml/product_demand_predictor.py
echo "✔ Product demand model trained."
echo ""

echo "📌 STEP 8 — Running Review Forecasting Model..."
python3 ml/review_forecast.py
echo "✔ Review forecasting completed."
echo ""

echo "📌 STEP 9 — Running Topic Modeling..."
python3 ml/topic_modeling.py
echo "✔ Topic modeling completed."
echo ""

echo "📌 STEP 10 — Launching Streamlit Dashboard..."
streamlit run dashboard_app.py --server.headless true
echo ""

echo "====================================================="
echo "🚀 PIPELINE EXECUTION COMPLETE"
echo "Dashboard is running... Press CTRL+C to stop."
echo "====================================================="
