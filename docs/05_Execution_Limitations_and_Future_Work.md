# Execution, Limitations, and Future Enhancements

This section describes the execution environment, design decisions, limitations of the current implementation, and potential future improvements.

---

## 🖥️ Execution Environment

The project was developed and executed locally using the following technologies:

| Component | Technology |
|--------|------------|
| Programming Language | Python |
| Big Data Processing | Apache Spark |
| Machine Learning | Scikit-learn |
| NLP | TF-IDF, LDA |
| Visualization | Streamlit |
| Operating System | Local Machine |

All execution steps, scripts, and dependencies are documented in the repository to ensure reproducibility.

---

## 🔁 Batch Processing vs Real-Time Streaming

Real-time streaming ingestion was initially explored. However, the following constraints influenced the final design:

- No freely available real-time Amazon review APIs
- Cloud-based streaming services (AWS, Kafka, etc.) incur high costs
- Budget constraints prevented continuous live ingestion

Based on instructor guidance, **batch processing with file-based streaming simulation** was adopted as a practical and acceptable alternative.

This approach still demonstrates:
- Incremental data ingestion
- Scalable processing logic
- Near-real-time analytical workflows

---

## ⚠️ Project Limitations

While the project meets its objectives, the following limitations are acknowledged:

- Lack of true real-time data ingestion
- Use of sampled datasets for faster experimentation
- Classical ML models instead of deep learning approaches
- Local execution instead of full cloud deployment

These limitations were necessary trade-offs to balance feasibility, cost, and academic scope.

---

## 🚀 Future Enhancements

The project can be extended in several directions:

| Area | Potential Improvement |
|----|------------------------|
| Data Ingestion | Integration with real-time APIs |
| Modeling | Transformer-based NLP models |
| Deployment | Cloud hosting on AWS or GCP |
| Automation | Continuous model retraining |
| Monitoring | Model performance tracking |

---

## ✅ Final Remarks

Despite practical constraints, the project successfully demonstrates an end-to-end analytics pipeline that goes beyond basic exploratory analysis. The system integrates scalable data processing, machine learning, evaluation metrics, and interactive visualization, making it applicable to real-world e-commerce analytics scenarios.
