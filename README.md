# 🛒 Amazon Customer Reviews Analytics (Spark)

Analyze **Amazon US product reviews** to uncover **sentiment trends**, **rating behavior**, and **helpfulness prediction** using **Apache Spark**.  
This project leverages Spark’s distributed processing to perform large-scale **ETL, NLP, and Machine Learning** on millions of real-world customer reviews.

---

## 📦 Dataset

**Dataset:** [Amazon US Customer Reviews Dataset (Kaggle)](https://www.kaggle.com/datasets/cynthiarempel/amazon-us-customer-reviews-dataset)  
*(Originally part of the AWS Open Data Registry)*

**Description:**  
Over **130 million product reviews** from verified Amazon customers across multiple categories — including text, ratings, timestamps, and metadata.

**Key Columns:**
- `review_id` → Unique identifier for each review  
- `product_id` → ASIN (Amazon Standard Identification Number)  
- `product_title` → Product name  
- `star_rating` → Rating from 1–5  
- `review_body` → Text review  
- `helpful_votes` → Votes marking a review as helpful  
- `product_category` → Product type (Electronics, Books, etc.)  
- `review_date` → Date of the review  

**Why This Dataset:**  
A **multi-million-row dataset** with both **textual** and **numerical** features — perfect for **parallelized ETL, joins, NLP, and ML pipelines** using Spark.

---

## 🎯 Project Goals

- Perform **Exploratory Data Analysis (EDA)** on reviews and ratings  
- Discover **sentiment trends** across product categories and years  
- Analyze **correlation between review length and rating**  
- Predict **helpful vs. non-helpful** reviews using **Spark MLlib**  
- Build **classification and regression models** for review analysis  
- Visualize **yearly trends**, **category insights**, and **sentiment distributions**


VIDEO RECORDING (Google Drive Link): https://drive.google.com/file/d/1wz9NxPkv3Lelz5qNbY1PaGAN-jZmxEpk/view?usp=sharing 
