import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Input and output paths
SAMPLE_PATH = "data/sample/amazon_reviews_sample.parquet"
FIG_DIR = "reports/figures"
os.makedirs(FIG_DIR, exist_ok=True)

# Load the sample dataset
print("📂 Loading sample dataset...")
df = pd.read_parquet(SAMPLE_PATH)
print(f"✅ Loaded {len(df):,} rows and {len(df.columns)} columns.\n")

# Convert review_date if available
if "review_date" in df.columns:
    df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")

# ---------------------------
# 1️⃣ Rating Distribution
# ---------------------------
plt.figure(figsize=(8, 5))
sns.countplot(x="star_rating", data=df, palette="viridis", order=sorted(df["star_rating"].unique()))
plt.title("Distribution of Star Ratings")
plt.xlabel("Star Rating")
plt.ylabel("Number of Reviews")
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/1_rating_distribution.png", dpi=150)
plt.close()

# ---------------------------
# 2️⃣ Average Rating by Category
# ---------------------------
if "product_category" in df.columns:
    avg_rating = (
        df.groupby("product_category")["star_rating"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )
    plt.figure(figsize=(10, 6))
    sns.barplot(x=avg_rating.values, y=avg_rating.index, palette="coolwarm")
    plt.title("Top 10 Product Categories by Average Rating")
    plt.xlabel("Average Rating")
    plt.ylabel("Product Category")
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/2_avg_rating_by_category.png", dpi=150)
    plt.close()

# ---------------------------
# 3️⃣ Review Count by Year
# ---------------------------
if "review_date" in df.columns:
    df["year"] = df["review_date"].dt.year
    year_count = df["year"].value_counts().sort_index()
    plt.figure(figsize=(10, 5))
    sns.lineplot(x=year_count.index, y=year_count.values, marker="o", color="orange")
    plt.title("Number of Reviews per Year")
    plt.xlabel("Year")
    plt.ylabel("Review Count")
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/3_reviews_per_year.png", dpi=150)
    plt.close()

# ---------------------------
# 4️⃣ Verified vs Unverified Purchases
# ---------------------------
if "verified_purchase" in df.columns:
    verified_counts = df["verified_purchase"].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(
        verified_counts.values,
        labels=["Verified", "Unverified"],
        autopct="%1.1f%%",
        startangle=90,
        colors=["#4CAF50", "#F44336"]
    )
    plt.title("Verified vs Unverified Purchases")
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/4_verified_vs_unverified.png", dpi=150)
    plt.close()

# ---------------------------
# 5️⃣ Top 10 Most Reviewed Products
# ---------------------------
if "product_title" in df.columns:
    top_products = df["product_title"].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_products.values, y=top_products.index, palette="Blues_r")
    plt.title("Top 10 Most Reviewed Products")
    plt.xlabel("Number of Reviews")
    plt.ylabel("Product Title")
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/5_top_products.png", dpi=150)
    plt.close()

print("✅ All visualizations saved in reports/figures/")
import matplotlib.pyplot as plt
from PIL import Image

img = Image.open("reports/figures/1_rating_distribution.png")
plt.imshow(img)
plt.axis("off")
plt.show()
