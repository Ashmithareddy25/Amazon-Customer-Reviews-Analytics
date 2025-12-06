#!/bin/bash
set -e

echo "Running data cleaning..."
python3 scripts/clean_data.py

echo "Running Spark batch ingestion..."
spark-submit spark_jobs/batch_ingest.py

echo "Running analytics and complex queries..."
spark-submit spark_jobs/complex_queries.py

echo "Training star rating classification model..."
spark-submit ml/predict_rating.py

echo "Training helpfulness regression model..."
spark-submit ml/predict_helpfulness.py

echo "Computing product worthiness scores..."
spark-submit scripts/product_worthiness.py

echo "Launching Streamlit dashboard..."
streamlit run dashboard/app.py
