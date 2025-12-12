# System Architecture and Data Pipeline

## High-Level Architecture
The project follows a modular and layered architecture where each stage of the pipeline performs a specific responsibility. This design improves scalability, clarity, and maintainability.

### Architecture Overview
![System Architecture](images/system_architecture.png)

> The diagram illustrates the flow from raw review data ingestion through Spark-based processing, machine learning models, and final visualization.

## Data Ingestion
The raw dataset consists of Amazon customer reviews stored in Parquet format. Due to cost constraints and limited access to real-time review APIs, the project adopts a batch ingestion strategy. File-based ingestion is also used to simulate streaming behavior.

## Processing Framework
Apache Spark is used for large-scale data processing. Spark enables efficient handling of large datasets and supports distributed transformations required for cleaning and feature engineering.

## Pipeline Workflow
1. Raw review data is loaded from Parquet files
2. Spark cleans and preprocesses the data
3. Cleaned data is stored in structured CSV format
4. Machine learning models consume the processed data
5. Analytical insights are visualized using Streamlit

This pipeline represents a complete analytical workflow rather than isolated exploratory analysis.
