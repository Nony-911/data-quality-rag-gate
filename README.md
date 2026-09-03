# data-quality-rag-gate
# 🛡️ Data Quality Gate for RAG Pipelines

An end-to-end Data Engineering pipeline enforcing Data Governance dimensions (Completeness, Accuracy, Validity) before feeding unverified data into Retrieval-Augmented Generation (RAG) knowledge bases.

> This project was made for **"Modern Data Engineering for AI Systems"** course provided by [SDAIA Academy](https://github.com/SDAIAAcademy).
---

## 📌 Architecture & Concepts
1. **Data Ingestion**: Processes raw user reviews and product evaluation metrics.
2. **Quality Gate Engine**: Validates inputs against core data quality dimensions:
   - **Completeness**: Ensures critical attributes (e.g., user email) are present.
   - **Accuracy**: Verifies ratings fall within permissible bounds (1 to 5).
   - **Validity**: Filters promotional spam and malicious web links.
3. **Quarantine Zone**: Isolates bad data with reason logging to protect downstream storage.
4. **Quality-Filtered RAG**: Feeds verified records into vector/text search retrieval
---

## 🚀 How to Run Locally

```bash
# Install dependencies
pip install pandas

# Execute the integrated pipeline
python app.py
