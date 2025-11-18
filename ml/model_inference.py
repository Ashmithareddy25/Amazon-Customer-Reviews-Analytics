import joblib
import re

# Load model + tfidf
model = joblib.load("models/sentiment_model.pkl")
tfidf = joblib.load("models/tfidf_vectorizer.pkl")

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z ]", "", text)
    return text

def predict_sentiment(review_text):
    clean = clean_text(review_text)
    vec = tfidf.transform([clean])
    pred = model.predict(vec)[0]
    return pred

if __name__ == "__main__":
    sample = "The product quality is amazing!"
    print("\nReview:", sample)
    print("Predicted Sentiment:", predict_sentiment(sample))
