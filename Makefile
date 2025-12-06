# Makefile for Amazon Customer Reviews Analytics Project

.PHONY: all data analysis models worthiness dashboard clean

all: data analysis models worthiness

data:
	python3 scripts/clean_data.py
	spark-submit spark_jobs/batch_ingest.py

analysis:
	spark-submit spark_jobs/complex_queries.py

models:
	spark-submit ml/predict_rating.py
	spark-submit ml/predict_helpfulness.py

worthiness:
	spark-submit scripts/product_worthiness.py

dashboard:
	streamlit run dashboard/app.py

clean:
	rm -rf data/processed/*
	rm -rf ml/models/*
