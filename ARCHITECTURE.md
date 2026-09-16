# Architecture

```text
Authorized PDF / TXT / MD
          |
          v
Ingestion -> Quality Gate ---- failure ----> Quarantine
          |
          v
PII Redaction + Audit Metadata
          |
          v
Recursive Chunking
          |
          v
Multilingual Embeddings
          |
          v
ChromaDB Vector Store
          ^
          |
User -> FastAPI -> Query Embedding -> Top-k Similarity Retrieval
                                      |
                               Confidence Threshold
                                /              \
                          sufficient         weak evidence
                              |                  |
                         Optional LLM          Abstain
                              |
                    Answer + Sources + Scores
                              |
                            Audit
```

## Architectural rationale

The submitted implementation is deliberately laptop-friendly and reproducible. It demonstrates the integrated architecture without claiming enterprise infrastructure that was not deployed.

## Production evolution

A production version can replace the local event simulation with Kafka or Redpanda, use a governed Lakehouse for durable storage, adopt Great Expectations or equivalent validation, move to Qdrant/Milvus or another distributed vector store, orchestrate with Airflow/Prefect, and deploy on Kubernetes with centralized observability and IAM.
