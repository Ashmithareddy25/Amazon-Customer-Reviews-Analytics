import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import re
import joblib

print("\n📥 Loading dataset...")

# FIX FOR PARSER ERROR + ENCODING
df = pd.read_csv("data/processed/cleaned_reviews.csv", 
                 engine="python", 
                 encoding="utf-8", 
                 on_bad_lines="skip")

# Keep needed columns
df = df[['review_body', 'star_rating']].dropna()

# Label sentiment
def label_sentiment(rating):
    if rating >= 4:
        return "positive"
    elif rating == 3:
        return "neutral"
    else:
        return "negative"

df["sentiment"] = df.star_rating.apply(label_sentiment)

# TEXT CLEANING
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z ]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["clean_review"] = df.review_body.apply(clean_text)

# 🚀 REDUCE DATASET SIZE (important)
df = df.sample(50000, random_state=42)   # Use 50k rows only (FAST & ACCURATE)

print(f"Using {len(df)} rows for training...\n")

# SPLIT
X = df["clean_review"]
y = df["sentiment"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# TF-IDF
tfidf = TfidfVectorizer(stop_words="english", max_features=5000)
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

# MODEL
model = LogisticRegression(max_iter=300, n_jobs=-1)
model.fit(X_train_tfidf, y_train)

# PREDICT
pred = model.predict(X_test_tfidf)

print("\n📊 Classification Report:")
print(classification_report(y_test, pred))

print("\n🎯 Accuracy:", accuracy_score(y_test, pred))

print("\n🔁 Confusion Matrix:")
print(confusion_matrix(y_test, pred))

# SAVE MODEL
joblib.dump(model, "models/sentiment_model.pkl")
joblib.dump(tfidf, "models/tfidf_vectorizer.pkl")

print("\n💾 Model Saved Successfully in /models/")
