import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
import joblib

DATA_PATH = "data/processed/cleaned_reviews.csv"
OUTPUT_DIR = "data/outputs"
MODEL_DIR = "ml/models"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

def main():
    print("📥 Loading data for product demand prediction...")
    
    df = pd.read_csv(
        DATA_PATH,
        usecols=["product_id", "review_date", "star_rating"],
        parse_dates=["review_date"],
        engine="python"
    )

    df["month"] = df["review_date"].dt.to_period("M")

    # monthly review count and avg rating
    monthly = df.groupby(["product_id", "month"]).agg(
        review_count=("star_rating", "count"),
        avg_rating=("star_rating", "mean")
    ).reset_index()

    # prepare features
    scaler = MinMaxScaler()
    monthly["review_norm"] = scaler.fit_transform(monthly[["review_count"]])
    monthly["rating_norm"] = scaler.fit_transform(monthly[["avg_rating"]])

    # future demand = weighted combination
    monthly["future_demand_score"] = (
        0.7 * monthly["review_norm"] +
        0.3 * monthly["rating_norm"]
    )

    # Train simple regression model to predict future demand
    X = monthly[["review_norm", "rating_norm"]]
    y = monthly["future_demand_score"]

    model = LinearRegression()
    model.fit(X, y)

    joblib.dump(model, os.path.join(MODEL_DIR, "product_demand_model.pkl"))
    joblib.dump(scaler, os.path.join(MODEL_DIR, "product_demand_scaler.pkl"))

    # Predict demand for next month
    monthly["predicted_next_month_demand"] = model.predict(X)

    top = monthly.groupby("product_id")["predicted_next_month_demand"].mean().sort_values(ascending=False).head(20)

    output = os.path.join(OUTPUT_DIR, "future_product_demand.csv")
    top.to_csv(output)
    
    print(f"\n📊 Top products predicted for future demand:")
    print(top)
    print(f"\n💾 Saved → {output}")

if __name__ == "__main__":
    main()
