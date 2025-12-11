# 🛒 Amazon Customer Reviews Analytics  
## A Complete End-to-End Big Data, NLP, and Machine Learning Pipeline Using Apache Spark

---

## 📘 Project Overview

This project implements a complete big data analytics pipeline to process, analyze, and model Amazon customer reviews. Using Apache Spark, PySpark MLlib, and Python, the system ingests raw review data, performs scalable transformations, extracts sentiment and topics from text, predicts ratings and helpfulness, and generates analytical insights. The pipeline also simulates real-time ingestion using file-based streaming and produces structured output files for visualization or further analysis.

---

## 🎯 Key Objectives

- Build an end-to-end scalable data pipeline for Amazon customer reviews  
- Clean, preprocess, and transform raw review data for analytics and machine learning  
- Perform Spark SQL analytics to extract category-wise insights, trends, and patterns  
- Engineer features for NLP and machine learning readiness  
- Train machine learning models for sentiment classification, rating prediction, helpfulness prediction, and topic modeling  
- Generate a Product Worthiness Score combining sentiment, rating, helpfulness, recency, and verified purchase behavior  
- Simulate real-time review ingestion using file-based streaming  
- Produce clean output datasets and results consumable by dashboards  

---

## 📦 Dataset Description

The project uses a structured Parquet dataset containing more than **50,000+ Amazon product reviews**.
**Dataset:** [Amazon US Customer Reviews Dataset (Kaggle)](https://www.kaggle.com/datasets/cynthiarempel/amazon-us-customer-reviews-dataset)  
*(Originally part of the AWS Open Data Registry)*

### **Dataset Fields**
- `review_id` – Unique identifier  
- `product_id` – ASIN of product  
- `product_title`  
- `review_body` – Text review  
- `star_rating` – Rating (1–5)  
- `review_date`  
- `verified_purchase`  
- `helpful_votes` / `total_votes`  
- `product_category`

---
🎯 3. Features & Goals

Primary objectives of this project:

✅ Clean and preprocess Amazon reviews
✅ Visualize rating distributions
✅ Conduct sentiment analysis to classify reviews as positive/negative
✅ Extract common themes and keywords from the text
✅ Build simple ML/NLP models for sentiment prediction
✅ Provide clear visual insights and dashboards
---

### **🏗️ Architecture**

```bash
                  Raw Data (Parquet)
                            │
                            ▼
                Data Cleaning & Preprocessing
                            │
                            ▼
                 Spark Batch Ingestion (ETL)
                            │
                            ▼
                  Spark SQL + EDA Analytics
                            │
                            ▼
                    Feature Engineering
                            │
                            ▼
               Machine Learning (MLlib + Python)
        ┌─────────────────────────────────────────────┐
        │ Logistic Regression – Sentiment             │
        │ Linear Regression – Rating Prediction       │
        │ RandomForest – Helpfulness Prediction       │
        │ LDA Topic Modeling – Theme Extraction       │
        └─────────────────────────────────────────────┘
                            │
                            ▼
                 Output (CSV/Parquet predictions)
                            │
                            ▼
                    Optional Streaming Layer
                            │
                            ▼
                External Dashboard (Streamlit)
```
---


### **📂 Repository Structure**

```bash

Amazon-Customer-Reviews-Analytics/
│
├── data/
│   ├── raw/                  # Original dataset
│   ├── cleaned/              # Cleaned data files
│   ├── stream_input/         # Files used for streaming simulation
│   ├── output_csv/           # Batch pipeline output
│   └── output_parquet/       # Parquet output for downstream use
│
├── scripts/
│   ├── ingestion.py          # Spark data ingestion pipeline
│   ├── data_cleaning.py      # Cleaning and preprocessing
│   ├── preprocessing.py      # NLP + feature engineering
│   ├── stream_pipeline.py    # File-based streaming logic
│   └── utils.py              # Helper utilities
│
├── ml/
│   ├── live_review_analyzer.py      # Live review scoring / sentiment
│   ├── model_inference.py           # Load models and run inference
│   ├── product_demand_predictor.py  # Demand/helpfulness forecast
│   ├── rating_regression.py         # Rating prediction model (regression)
│   ├── review_forecast.py           # Review volume forecasting
│   ├── sentiment_ml.py              # Sentiment classification (ML)
│   └── topic_modeling.py            # LDA topic modeling
│   └── __models__/                  # Stored models and vectorizers
│
├── models/                   # Additional trained model assets
├── notebooks/                # EDA and experimentation notebooks
├── reports/                  # PDF documentation and project reports
│
├── dashboard_app.py          # Streamlit dashboard (optional)
├── run.sh                    # End-to-end execution script
├── Makefile                  # Automation commands
├── README.md
└── LICENSE

```

---


## 🔧 Prerequisites

### **Software Requirements**
```bash
Python 3.8+
Apache Spark 3.x
Java 8+
pip / virtualenv
```

### **Python Libraries**
```bash
pyspark
pandas
numpy
scikit-learn
nltk
joblib
```

---

## 🔄 End-to-End Pipeline Details

### **1. Dataset Ingestion**
- Loads Parquet dataset using Spark Structured APIs  
- Reads data into Spark DataFrames for distributed processing  
- Converts and stores intermediate data in efficient columnar Parquet format  

### **2. Data Cleaning**
- Removes duplicates using `review_id`  
- Drops rows missing key fields  
- Normalizes text (lowercasing, removing symbols, trimming whitespace)  
- Converts `verified_purchase` to a binary flag  
- Parses `review_date` into proper date format  

### **3. Feature Engineering**
- Creates `review_length`, `helpfulness_ratio`, `verified_flag`  
- Extracts `year` and `month` from `review_date`  
- Computes sentiment using rule-based polarity functions  
- Performs NLP feature extraction:  
  - Tokenization  
  - Stopwords removal  
  - TF-IDF vectorization  

### **4. Spark SQL Analytics**
- Computes product category–level insights  
- Identifies top products by review count, helpfulness, and verified ratios  
- Analyzes rating distribution patterns  
- Extracts monthly sentiment and rating trends  
- Identifies highly helpful reviews  

### **5. Machine Learning Models**

#### **Sentiment Classification (Logistic Regression)**
- Predicts Positive / Neutral / Negative sentiment  
- Uses TF-IDF text vectors + numeric features  

#### **Rating Prediction (Linear Regression)**
- Predicts expected star rating from review text  

#### **Helpfulness Prediction (RandomForestRegressor)**
- Predicts `helpful_votes` using metadata + text features  

#### **Topic Modeling (LDA)**
- Extracts dominant themes from reviews  
- Helps uncover common customer concerns  

#### **Rule-Based Sentiment**
- Keyword-based polarity scoring  
- Used as a simple baseline model  

### **6. Evaluation Metrics**
- Accuracy  
- Precision  
- Recall  
- F1-score  
- Confusion Matrix  
- MSE / RMSE  
- R²  

### **7. Streaming Component**
- Uses file-based streaming simulation  
- Automatically processes new review files placed in `stream_input/`  
- Produces incremental outputs for near–real-time updates  

---

## 📊 Main Insights From the Pipeline
- Reviews are heavily skewed toward 4–5 star ratings  
- Verified purchases provide more trustworthy and positive ratings  
- Helpful votes follow a skewed long-tail distribution  
- Longer reviews generally receive more helpful votes  
- Seasonal patterns and category-specific behaviors emerge  
- Sentiment correlates strongly with star ratings  
- LDA Topic Modeling highlights themes such as quality, delivery, and price  

---
## 🛠️ Execution Setup

### 1. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Run Full End-to-End Pipeline
```bash
bash run.sh
```

### 4. Run Individual Components
**Ingestion**
```bash
python scripts/ingestion.py
```
**Cleaning**
```bash
python scripts/data_cleaning.py
```
**Feature Engineering**
```bash
python scripts/preprocessing.py
```

**ML Models**
- **Sentiment Classification – Logistic Regression**
```bash
python ml/sentiment_ml.py
```
- **Linear Regression – Rating Prediction**
```bash
python ml/rating_regression.py
```
- **Helpfulness Prediction – RandomForestRegressor**
```bash
python ml/product_demand_predictor.py
```

- **Topic Modeling – LDA**
```bash
python ml/topic_modeling.py
```

---
---

# 🚀 Deployment & Scalability
This project is designed for both **local execution** and **production-scale deployment**, ensuring flexibility for development, analytics, and large-scale distributed processing.

### 🌐 Local Execution (Development Mode)
Ideal for experimentation, academic use, and lightweight workloads:
- Spark runs in `local[*]` mode
- Streamlit dashboard available on localhost
- ML models loaded directly from `.pkl` files
- Streaming simulated using file-based batch ingestion

### ☁️ Cluster Deployment (Distributed Mode)
For processing millions of reviews at scale, the pipeline seamlessly extends to:
- **AWS EMR**
- **Databricks**
- **Google Cloud Dataproc**
- **Kubernetes + Spark Operator**

**Benefits of cluster deployment:**
- Distributed TF-IDF vectorization
- Distributed model training using PySpark MLlib
- Fast execution of Spark SQL analytic workloads
- Fault tolerance, checkpointing & scalability

### 🐳 Containerization (Optional Production Setup)
You may containerize the entire system using:
- Docker for the Streamlit dashboard
- Dockerized Spark images for batch/stream processing
- A FastAPI microservice for model inference

---

# ⚡ Performance Optimizations
The pipeline includes several optimizations for handling large-scale text analytics efficiently.

### 🔹 1. Parquet-Based Storage
- Highly compressed columnar format  
- Enables predicate pushdown  
- Faster for Spark analytics  

### 🔹 2. Spark Caching for Hot DataFrames
Used during iterative:
- SQL queries  
- NLP processing  
- ML model fitting  

### 🔹 3. Vectorized NLP Transformations
- Reuse TF-IDF vectorizer stored in joblib
- Avoid recomputing token mappings
- Ensures faster ML inference

### 🔹 4. Streaming Micro-Batch Architecture
- Processes incremental review files  
- Suitable for near real-time dashboards  
- Lightweight checkpoint-based fault recovery  

### 🔹 5. Hybrid ML Models
- Fast rule-based sentiment scoring for baseline
- More accurate ML-based models for production

---

# 🛡️ Data Quality & Validation
To maintain clean and reliable analytics, the pipeline enforces multiple data validation rules.

### 📌 Schema Validation
Ensures all required columns:
- `review_id`
- `product_id`
- `review_body`
- `star_rating`
- `verified_purchase`
- `review_date`

### 📌 Text Quality Validation
- Removes non-English characters  
- Removes repeated symbols  
- Enforces minimum review length  

### 📌 Missing Value Handling
- Drops unusable records
- Converts `verified_purchase` to binary flags
- Parses and standardizes `review_date`

### 📌 Outlier Detection
Flags anomalies such as:
- Extremely long reviews
- Repetitive spam-like text
- Abnormal rating patterns

---

# 🔐 Security & Compliance
While the dataset is fully public, the project follows standard data-handling best practices.

### 🔒 No Personal Identifiable Information
Amazon customer review datasets do not contain:
- Names  
- Emails  
- Addresses  
- Payment data  
- Sensitive personal content  

### 📦 Safe File Handling
- All processed data stored locally under `data/`
- No cloud uploads unless explicitly configured
- Checkpoints isolated inside pipeline directories

### 🧪 Model Safety
The ML models:
- Do not store any user-specific data  
- Only operate on review text and metadata  
- Are safe to deploy or share  

---

# 🔮 Future Enhancements
To further strengthen and expand this project, the following improvements can be added:

### 🧠 Advanced NLP Models
- Transformer-based sentiment analysis (BERT, DistilBERT)
- Summarization of long reviews
- Named Entity Recognition (NER) for extracting product attributes

### 📈 Enhanced Forecasting
- LSTM/RNN models for review volume forecasting  
- Prophet-based seasonal analysis  
- Category-level anomaly detection  

### 🗂️ Metadata Enrichment
- Integrate product metadata (price, brand)
- Cross-reference ASIN with external APIs (Amazon Product API)

### ⚡ Real-Time Streaming
- Upgrade to Kafka-based ingestion  
- Integrate Spark Structured Streaming on clusters  
- Build a real-time ML inference API  

### 📊 Dashboard Upgrades
- User-based filtering  
- Time-range comparisons  
- Multi-product comparison matrix  
- Recommendation engine integration  

---

### ✔️ Summary

This project implements a complete end-to-end big data pipeline built on Apache Spark with integrated NLP and machine learning modules. It automates data ingestion, cleaning, preprocessing, feature engineering, analytics, and model training for Amazon reviews at scale. The system produces structured outputs, generates meaningful insights, and supports simulated real-time updates, enabling deeper understanding of customer behavior and product performance.

---

[**VIDEO RECORDING** ](https://drive.google.com/file/d/1wz9NxPkv3Lelz5qNbY1PaGAN-jZmxEpk/view?usp=sharing)

