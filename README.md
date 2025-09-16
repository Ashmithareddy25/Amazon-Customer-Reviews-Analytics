# 🏡 Airbnb Price & Demand Analytics (Spark)

Analyze Airbnb listings, calendar availability, and reviews to understand **pricing, demand seasonality, host behavior, and neighborhood patterns** using Apache Spark.

---

## 📦 Datasets

We are using **two sources**:

1. **Inside Airbnb (Official Open Data)** – multiple cities, updated regularly  
   👉 http://insideairbnb.com/get-the-data/  

   - `listings.csv` → host info, price, amenities, room type, reviews count  
   - `calendar.csv` → daily availability & price per listing  
   - `reviews.csv` → review text, rating, date  

2. **Kaggle Airbnb Open Data (cleaner versions for prototyping)**  
   - [Seattle Airbnb Open Data](https://www.kaggle.com/datasets/airbnb/seattle)  
   - [Boston Airbnb Open Data](https://www.kaggle.com/datasets/airbnb/boston)  

---

## 🎯 Project Goals

- Perform **Exploratory Data Analysis (EDA)** on listings, calendar, and reviews  
- Identify **price patterns and seasonality** across neighborhoods and room types  
- Train a **baseline ML model** (Spark MLlib) to predict nightly prices  
- (Optional) Explore **reviews text** for sentiment or rating prediction  

---


