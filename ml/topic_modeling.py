import os
import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# --------------------
# CONFIG
# --------------------
DATA_PATH = "data/processed/cleaned_reviews.csv"
OUTPUT_DIR = "data/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --------------------
# CLEAN TEXT
# --------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z ]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# --------------------
# MAIN
# --------------------
def main():
    print("📥 Loading review data...")
    df = pd.read_csv(
        DATA_PATH,
        usecols=["review_body"],
        nrows=50000,
        engine="python"
    )

    df["clean"] = df["review_body"].astype(str).apply(clean_text)

    print("🔤 Vectorizing text...")
    vectorizer = CountVectorizer(
        stop_words="english",
        max_features=8000
    )
    X = vectorizer.fit_transform(df["clean"])

    print("🧠 Training LDA Topic Model...")
    lda = LatentDirichletAllocation(
        n_components=6,  # number of topics
        random_state=42,
        learning_method='batch'
    )
    lda.fit(X)

    # Save important words per topic
    print("\n📜 TOPICS DISCOVERED:\n")
    feature_names = vectorizer.get_feature_names_out()

    topics = {}
    for idx, topic in enumerate(lda.components_):
        top_words = [feature_names[i] for i in topic.argsort()[-20:]]
        topics[f"Topic {idx+1}"] = top_words
        print(f"Topic {idx+1}: {top_words}")

    # Save to CSV
    topic_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in topics.items()]))
    output_path = os.path.join(OUTPUT_DIR, "lda_topics.csv")
    topic_df.to_csv(output_path, index=False)

    print(f"\n💾 Saved topic model output → {output_path}")


if __name__ == "__main__":
    main()

