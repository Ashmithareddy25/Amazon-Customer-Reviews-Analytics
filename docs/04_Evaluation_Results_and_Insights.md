# Evaluation Results and Analytical Insights

This section presents the quantitative evaluation of machine learning models used in the project along with the key analytical insights derived from customer review data.

---

## 📊 Sentiment Classification Evaluation

The sentiment analysis model was evaluated using a held-out test dataset and standard classification metrics.

### Model Used
- Logistic Regression
- TF-IDF feature representation

### Performance Metrics

| Metric | Value |
|------|-------|
| Accuracy | ~85% |
| Precision (Weighted Avg) | ~82% |
| Recall (Weighted Avg) | ~85% |
| F1-score (Weighted Avg) | ~82% |

The model performs particularly well in identifying **positive sentiment**, which aligns with the natural distribution of customer reviews where positive feedback is more frequent.

<p align="center">
  <img src="images/confusion_matrix.png" alt="Sentiment Confusion Matrix" width="600"/>
</p>

**Insight:**  
The confusion matrix shows strong classification for positive reviews, while neutral sentiment remains harder to classify due to overlap in language usage.

---

## 📈 Rating Prediction Evaluation

The rating prediction model estimates star ratings directly from review text.

### Model Used
- Linear Regression
- TF-IDF features

### Regression Metrics

| Metric | Value |
|------|-------|
| Mean Squared Error (MSE) | ~0.95 |
| R² Score | ~0.41 |

**Insight:**  
The results indicate a meaningful relationship between review text and numerical ratings. While textual sentiment alone cannot perfectly predict ratings, the model captures significant variance in customer scoring behavior.

---

## 🏷️ Topic Modeling Insights

Latent Dirichlet Allocation (LDA) was used to uncover hidden topics across customer reviews.

### Key Topics Identified
- Product quality and durability
- Ease of use and installation
- Shipping experience and delivery speed
- Pricing and value for money
- Customer satisfaction and complaints

<p align="center">
  <img src="images/lda_topics.png" alt="LDA Topics" width="600"/>
</p>

**Insight:**  
Topic modeling enables summarization of thousands of reviews into interpretable themes, helping businesses identify common strengths and recurring issues without manual review.

---

## 🔍 Overall Analytical Insights

- Customer sentiment is predominantly positive across categories
- Text-based features are effective for sentiment and rating prediction
- Topic modeling provides high-level summaries of customer concerns
- Combining NLP, ML, and visualization creates actionable business insights
