import joblib
import re
import numpy as np
import pandas as pd
import scipy.sparse as sp
from sklearn.base import BaseEstimator

# ----------------------------
# CORRECT MODEL PATHS
# ----------------------------
SENTIMENT_MODEL = "models/sentiment_model.pkl"
TFIDF_MODEL = "models/tfidf_vectorizer.pkl"
RATING_MODEL = "models/rating_regression.pkl"


class LiveReviewAnalyzer:

    def __init__(self):
        print("📥 Loading models...")

        # Load models
        self.sentiment_model = joblib.load(SENTIMENT_MODEL)
        self.vectorizer = joblib.load(TFIDF_MODEL)
        self.rating_model = joblib.load(RATING_MODEL)

        # Try to get model expected feature count (scikit-learn stores it in n_features_in_)
        self.model_expected_features = getattr(self.rating_model, "n_features_in_", None)

        print("✅ All models loaded successfully!")
        if self.model_expected_features is not None:
            print(f"ℹ️ Rating model expects {self.model_expected_features} features as input.")
        else:
            print("⚠️ Could not read rating model expected feature count (n_features_in_).")

    # ----------------------------
    # TEXT CLEANING
    # ----------------------------
    def clean_text(self, text):
        text = str(text).lower()
        text = re.sub(r"[^a-zA-Z ]", "", text)
        return text

    # ----------------------------
    # HELPER: align TF-IDF vector to model expected size
    # ----------------------------
    def _align_vector_to_model(self, vec):
        """
        Ensure `vec` (sparse matrix, shape (1, n_features_vec)) has the same
        number of features as the trained rating model expects.

        If sizes match -> return vec unchanged.
        If vec has MORE features -> truncate rightmost columns (temporary workaround).
        If vec has FEWER features -> pad with zero columns on the right.
        NOTE: This is a compatibility workaround. The correct fix is to use the
        exact vectorizer used during training (or retrain the model with the
        current vectorizer).
        """
        if not sp.issparse(vec):
            vec = sp.csr_matrix(vec)

        n_vec = vec.shape[1]
        n_model = self.model_expected_features

        # If we can't determine model expected features, just return vec
        if n_model is None:
            print("ℹ️ Model expected feature count unknown. Skipping alignment.")
            return vec

        if n_vec == n_model:
            return vec

        print(f"⚠️ Feature mismatch detected: vectorizer -> {n_vec} features, "
              f"model -> {n_model} features.")

        if n_vec > n_model:
            # Truncate extra columns (keep first n_model features)
            print(f"⚠️ Truncating TF-IDF vector from {n_vec} -> {n_model} features (temporary).")
            # slicing columns on CSR sparse matrix works
            vec_aligned = vec[:, :n_model].tocsr()
            return vec_aligned

        # n_vec < n_model -> pad zeros to the right
        pad_cols = n_model - n_vec
        print(f"⚠️ Padding TF-IDF vector with {pad_cols} zero columns to match model (temporary).")
        zero_pad = sp.csr_matrix((1, pad_cols))
        vec_aligned = sp.hstack([vec, zero_pad], format="csr")
        return vec_aligned

    # ----------------------------
    # SENTIMENT PREDICTION
    # ----------------------------
    def predict_sentiment(self, review):
        clean = self.clean_text(review)
        vec = self.vectorizer.transform([clean])
        # No need to align for sentiment if it was trained with same vectorizer (assumed)
        pred = self.sentiment_model.predict(vec)[0]
        return pred

    # ----------------------------
    # RATING PREDICTION (1–5)
    # ----------------------------
    def predict_rating(self, review):
        clean = self.clean_text(review)
        vec = self.vectorizer.transform([clean])
        # Align feature count if needed (workaround)
        vec_aligned = self._align_vector_to_model(vec)
        rating = self.rating_model.predict(vec_aligned)[0]
        # Ensure numeric and nicely rounded
        return round(float(rating), 2)

    # ----------------------------
    # FULL ANALYSIS
    # ----------------------------
    def analyze_review(self, review):
        sentiment = self.predict_sentiment(review)
        rating = self.predict_rating(review)

        return {
            "review": review,
            "sentiment": sentiment,
            "predicted_rating": rating
        }


if __name__ == "__main__":
    analyzer = LiveReviewAnalyzer()

    print("\n🔍 Enter a review to analyze (type 'exit' to quit)\n")

    while True:
        try:
            review = input("Review: ")
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Exiting analyzer...")
            break

        if review.lower() in ["exit", "quit"]:
            print("👋 Exiting analyzer...")
            break

        try:
            result = analyzer.analyze_review(review)
            print("\n----------------------------")
            print(f"📝 Review: {result['review']}")
            print(f"💬 Sentiment: {result['sentiment']}")
            print(f"⭐ Predicted Rating: {result['predicted_rating']}")
            print("----------------------------\n")
        except Exception as e:
            print("🚨 Error during analysis:", str(e))
            print("Make sure you are loading the same TF-IDF vectorizer that was used during training.")
            print("As a diagnostic you can check:")
            try:
                n_vec = len(analyzer.vectorizer.get_feature_names_out())
                print(f" - Current vectorizer features: {n_vec}")
            except Exception:
                print(" - Could not read vectorizer feature names.")
            if analyzer.model_expected_features is not None:
                print(f" - Rating model expected features: {analyzer.model_expected_features}")
            break
