# Data Processing and Machine Learning

## Data Cleaning and Preprocessing
The following preprocessing steps are applied to the raw review data:
- Removal of missing and duplicate records
- Text normalization (lowercasing, punctuation removal)
- Tokenization and stop-word removal
- Sampling of large datasets to optimize training time

The cleaned dataset serves as a unified input for all modeling tasks.

## Feature Engineering
Unstructured review text is converted into numerical representations using:
- TF-IDF (Term Frequency–Inverse Document Frequency)

TF-IDF helps capture the importance of words while reducing the impact of commonly occurring but less informative terms.

## Machine Learning Models
The project includes multiple machine learning models addressing different analytical objectives.

### Model Summary

| Task | Model | Input Features | Output |
|----|----|----|----|
| Sentiment Analysis | Logistic Regression | TF-IDF vectors | Positive / Neutral / Negative |
| Rating Prediction | Linear Regression | TF-IDF vectors | Star Rating (1–5) |
| Topic Modeling | Latent Dirichlet Allocation (LDA) | Bag-of-Words | Review Topics |

Each model is trained independently and stored for reuse within the analytics dashboard.
