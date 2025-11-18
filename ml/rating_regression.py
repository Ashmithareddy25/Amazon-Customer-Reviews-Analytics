import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

# ----------------------------------------
# LOAD DATA
# ----------------------------------------
print("📥 Loading cleaned reviews...")

df = pd.read_csv(
    "data/processed/cleaned_reviews.csv",
    usecols=["review_body", "star_rating"],   # only needed columns
    nrows=50000,                              # load 50k rows
    engine="python"
)

print(f"✔ Loaded {len(df)} rows")

# ----------------------------------------
# CLEANING
# ----------------------------------------
df.dropna(inplace=True)

def clean_text(text):
    text = str(text).lower()
    return re.sub(r"[^a-zA-Z ]", " ", text)

df["clean_review"] = df["review_body"].apply(clean_text)

# ----------------------------------------
# SPLIT DATA
# ----------------------------------------
X = df["clean_review"]
y = df["star_rating"]

print("✂ Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ----------------------------------------
# TF-IDF VECTORIZATION
# ----------------------------------------
print("🔤 Vectorizing text...")
tfidf = TfidfVectorizer(stop_words="english", max_features=4000)

X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

# ----------------------------------------
# TRAIN MODEL
# ----------------------------------------
print("🤖 Training Linear Regression model...")
model = LinearRegression()
model.fit(X_train_tfidf, y_train)

# ----------------------------------------
# EVALUATION
# ----------------------------------------
print("📊 Evaluating model...")

pred = model.predict(X_test_tfidf)

mse = mean_squared_error(y_test, pred)
r2 = r2_score(y_test, pred)

print(f"\n🎯 Mean Squared Error (MSE): {mse:.4f}")
print(f"📈 R² Score: {r2:.4f}")

# ----------------------------------------
# SAVE TO EXISTING 'models/' FOLDER
# ----------------------------------------
print("💾 Saving model into models/ folder...")

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/rating_regression.pkl")
joblib.dump(tfidf, "models/rating_vectorizer.pkl")

print("✅ Model + Vectorizer saved successfully to models/")
