# =====================================================================
# Makefile for Amazon Customer Reviews Analytics Project
# This Makefile automates the end-to-end pipeline:
# - Data cleaning
# - Spark batch processing
# - Analytics queries
# - ML model execution
# - Product worthiness scoring
# - Streamlit dashboard launching
# - Cleanup of processed outputs
#
# Each target can be run individually using:
#       make <target>
#
# Example:
#       make data
#       make models
#       make dashboard
# =====================================================================

# Declare phony targets to avoid conflicts with real file names
.PHONY: all data analysis models worthiness dashboard clean

# -----------------------------------------------------------
# Run the ENTIRE workflow: data → analysis → ML models → worthiness
# This is the default action when running 'make' with no arguments.
# -----------------------------------------------------------
all: data analysis models worthiness

# -----------------------------------------------------------
# DATA PIPELINE
# 1. Run Python script to clean raw Amazon review data
# 2. Run Spark job to ingest processed data into distributed format
# -----------------------------------------------------------
data:
	python3 scripts/clean_data.py
	spark-submit spark_jobs/batch_ingest.py

# -----------------------------------------------------------
# ANALYTICS PIPELINE
# Executes Spark SQL queries or transformations to produce
# insights such as aggregations, summary statistics, and metrics.
# -----------------------------------------------------------
analysis:
	spark-submit spark_jobs/complex_queries.py

# -----------------------------------------------------------
# MACHINE LEARNING PIPELINE
# Runs Spark-based ML jobs:
#   - predict_rating.py : Predicts product star rating using ML
#   - predict_helpfulness.py : Predicts review helpfulness score
# Both jobs are executed using spark-submit
# -----------------------------------------------------------
models:
	spark-submit ml/predict_rating.py
	spark-submit ml/predict_helpfulness.py

# -----------------------------------------------------------
# WORTHINESS SCORE GENERATION
# Computes a product-level “worthiness score” using:
#   - Average rating
#   - Sentiment metrics
#   - Review factors
# -----------------------------------------------------------
worthiness:
	spark-submit scripts/product_worthiness.py

# -----------------------------------------------------------
# DASHBOARD SERVER
# Launches the Streamlit dashboard for real-time visualization.
# This opens the UI where users can explore:
#   - Ratings
#   - Sentiment
#   - ML predictions
#   - Product worthiness
# -----------------------------------------------------------
dashboard:
	streamlit run dashboard/app.py

# -----------------------------------------------------------
# CLEANUP
# Removes all processed datasets and ML model artifacts
# Useful when re-running pipelines from scratch
# -----------------------------------------------------------
clean:
	rm -rf data/processed/*
	rm -rf ml/models/*
