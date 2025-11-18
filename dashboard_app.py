import streamlit as st
import pandas as pd
import plotly.express as px
from textblob import TextBlob
import numpy as np

# -----------------------------------------------------------
# Page Config
# -----------------------------------------------------------
st.set_page_config(page_title="Amazon Product Worthiness Predictor", layout="wide")
st.title("📊 Amazon Product Worthiness & Review Insights Dashboard")

# -----------------------------------------------------------
# Load Data
# -----------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_parquet("data/sample/amazon_reviews_cleaned.parquet")
    df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")
    return df

df = load_data()

# -----------------------------------------------------------
# Sentiment Calculation
# -----------------------------------------------------------
if "sentiment_score" not in df.columns:
    st.info("⚙️ Calculating sentiment scores, please wait...")
    df["sentiment_score"] = df["review_body"].astype(str).apply(lambda x: TextBlob(x).sentiment.polarity)
    df["sentiment"] = df["sentiment_score"].apply(lambda s: "Positive" if s > 0 else "Negative" if s < 0 else "Neutral")

# -----------------------------------------------------------
# Sidebar: Category Selector
# -----------------------------------------------------------
st.sidebar.header("🔍 Filter Options")
categories = ["All"] + sorted(df["product_category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Select Product Category", categories)

if selected_category != "All":
    df = df[df["product_category"] == selected_category]

# -----------------------------------------------------------
# Product-level Aggregation & Worthiness
# -----------------------------------------------------------
st.markdown("### 💡 Product-Level Worthiness Analysis")

product_summary = (
    df.groupby("product_title")
    .agg(
        avg_rating=("star_rating", "mean"),
        review_count=("review_body", "count"),
        avg_sentiment=("sentiment_score", "mean"),
    )
    .reset_index()
)

# Normalize worthiness score (weighted mix of rating & sentiment)
product_summary["worthiness_score"] = (
    0.7 * (product_summary["avg_rating"] / 5) + 0.3 * ((product_summary["avg_sentiment"] + 1) / 2)
)
product_summary["worthiness_score"] = product_summary["worthiness_score"] * 100

# Top 5 best & worst products
top_products = product_summary.sort_values("worthiness_score", ascending=False).head(5)
low_products = product_summary.sort_values("worthiness_score", ascending=True).head(5)

# -----------------------------------------------------------
# Overview Metrics
# -----------------------------------------------------------
st.markdown("### 📈 Overview Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Average Rating", round(df["star_rating"].mean(), 2))
col2.metric("Total Reviews", len(df))
col3.metric("Average Worthiness (%)", round(product_summary["worthiness_score"].mean(), 2))

# -----------------------------------------------------------
# Visualization 1: Worthiness Distribution
# -----------------------------------------------------------
st.markdown("### 🏅 Product Worthiness Distribution")
fig_worthiness = px.scatter(
    product_summary,
    x="avg_rating",
    y="avg_sentiment",
    size="review_count",
    color="worthiness_score",
    hover_name="product_title",
    title="Relationship Between Rating, Sentiment & Worthiness",
    color_continuous_scale="Viridis",
)
st.plotly_chart(fig_worthiness, use_container_width=True)

# -----------------------------------------------------------
# Visualization 2: Top 5 Best and Worst Products
# -----------------------------------------------------------
st.markdown("### 🥇 Top 5 Best & 🚫 Worst Products")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 5 Best Products")
    fig_best = px.bar(
        top_products,
        x="worthiness_score",
        y="product_title",
        orientation="h",
        text="avg_rating",
        color="worthiness_score",
        color_continuous_scale="Greens",
        title="Top 5 Products by Worthiness",
    )
    st.plotly_chart(fig_best, use_container_width=True)
    st.dataframe(top_products[["product_title", "avg_rating", "avg_sentiment", "worthiness_score"]])

with col2:
    st.subheader("Bottom 5 Products")
    fig_worst = px.bar(
        low_products,
        x="worthiness_score",
        y="product_title",
        orientation="h",
        text="avg_rating",
        color="worthiness_score",
        color_continuous_scale="Reds",
        title="Lowest 5 Products by Worthiness",
    )
    st.plotly_chart(fig_worst, use_container_width=True)
    st.dataframe(low_products[["product_title", "avg_rating", "avg_sentiment", "worthiness_score"]])

# -----------------------------------------------------------
# Visualization 3: Category Trend (Optional)
# -----------------------------------------------------------
st.markdown("### 📆 Review Trend Over Time (Category-Level)")
monthly_trend = df.groupby(df["review_date"].dt.to_period("M")).size().reset_index(name="Review Count")
monthly_trend["review_date"] = monthly_trend["review_date"].astype(str)
fig_trend = px.line(
    monthly_trend,
    x="review_date",
    y="Review Count",
    title=f"Monthly Review Trend for {selected_category if selected_category != 'All' else 'All Categories'}",
)
st.plotly_chart(fig_trend, use_container_width=True)

# -----------------------------------------------------------
# Data Sample
# -----------------------------------------------------------
with st.expander("🧾 View Product Worthiness Data"):
    st.dataframe(product_summary.head(15))