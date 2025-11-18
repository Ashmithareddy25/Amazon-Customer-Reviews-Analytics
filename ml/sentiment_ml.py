import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import re

# -------------------------------
# LOAD DATA
# -------------------------------
df = pd.read_csv("data/processed/cleaned_reviews.csv")

# Keep only needed columns
df = df[['review_body', 'star_rating']].dropna()

# Create sentiment label
def label_sentiment(rating):
    if rating >= 4:
        return "positive"
    elif rating == 3:
        return "neutral"
    else:
        return "negative"

df["sentiment"] = df.star_rating.apply(label_sentiment)

# -------------------------------
# TEXT PREPROCESSING
# -------------------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z ]", "", text)
    return text

df["clean_review"] = df.review_body.apply(clean_text)

# -------------------------------
# TRAIN / TEST SPLIT
# -------------------------------
X = df["clean_review"]
y = df["sentiment"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------
# TF-IDF VECTORIZE
# -------------------------------
tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

# -------------------------------
# TRAIN LOGISTIC REGRESSION MODEL
# -------------------------------
model = LogisticRegression(max_iter=200)
model.fit(X_train_tfidf, y_train)

# -------------------------------
# EVALUATE MODEL
# -------------------------------
pred = model.predict(X_test_tfidf)

print("\nClassification Report:")
print(classification_report(y_test, pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, pred))
