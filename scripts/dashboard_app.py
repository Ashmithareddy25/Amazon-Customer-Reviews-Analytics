import streamlit as st
import pandas as pd
import plotly.express as px
from textblob import TextBlob

# App title
st.set_page_config(page_title="Amazon Review Analytics", layout="wide")
st.title("📊 Amazon Customer Reviews Analytics Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_parquet("data/sample/amazon_reviews_cleaned.parquet")
    df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")
    return df

df = load_data()

# Compute sentiment if not already present
if "sentiment_score" not in df.columns:
    st.info("⚙️ Calculating sentiment scores, please wait...")
    df["sentiment_score"] = df["review_body"].astype(str).apply(lambda x: TextBlob(x).sentiment.polarity)
    df["sentiment"] = df["sentiment_score"].apply(lambda s: "Positive" if s > 0 else "Negative" if s < 0 else "Neutral")

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
categories = ["All"] + sorted(df["product_category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Select Product Category", categories)

if selected_category != "All":
    df = df[df["product_category"] == selected_category]

# Overview metrics
st.markdown("### 📈 Overview Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Average Rating", round(df["star_rating"].mean(), 2))
col2.metric("Total Reviews", len(df))
col3.metric("Verified Purchases (%)", round((df["verified_purchase"].value_counts(normalize=True).get('Y', 0)) * 100, 2))

# Visualization 1: Rating distribution
st.markdown("### ⭐ Rating Distribution")
fig_rating = px.histogram(
    df, x="star_rating", nbins=5, title="Distribution of Ratings", color="star_rating", color_continuous_scale="Blues"
)
st.plotly_chart(fig_rating, use_container_width=True)

# Visualization 2: Sentiment analysis
st.markdown("### 💬 Sentiment Distribution")
fig_sentiment = px.pie(df, names="sentiment", title="Overall Sentiment Distribution", hole=0.4)
st.plotly_chart(fig_sentiment, use_container_width=True)

# Visualization 3: Average Rating by Category
st.markdown("### 🏷️ Average Rating by Product Category")
avg_rating = (
    df.groupby("product_category")["star_rating"].mean().sort_values(ascending=False).head(10).reset_index()
)
fig_avg = px.bar(avg_rating, x="star_rating", y="product_category", orientation="h", title="Top 10 Categories by Avg Rating")
st.plotly_chart(fig_avg, use_container_width=True)

# Visualization 4: Review trend over time
st.markdown("### 📆 Monthly Review Trends")
monthly_trend = df.groupby(df["review_date"].dt.to_period("M")).size().reset_index(name="Review Count")
monthly_trend["review_date"] = monthly_trend["review_date"].astype(str)
fig_trend = px.line(monthly_trend, x="review_date", y="Review Count", title="Monthly Review Count Trend")
st.plotly_chart(fig_trend, use_container_width=True)

# Data preview
with st.expander("🧾 View Cleaned Data Sample"):
    st.dataframe(df.sample(10))
