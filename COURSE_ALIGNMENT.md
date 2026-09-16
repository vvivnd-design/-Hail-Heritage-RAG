# Course Alignment and Submission Scope

## Hail Heritage RAG | راوي حائل الذكي

**Program:** Modern Data Engineering for Advanced AI Systems  
**Academy:** SDAIA Academy  
**Submission type:** Integrated local proof of concept

## Alignment with the course

The course capstone asks students to integrate modern data architecture, real-time data pipelines, vector databases, advanced RAG, data quality, and governance into one Python implementation.

This project demonstrates those areas as follows:

| Course area | Project implementation |
|---|---|
| Modern Data Architecture | Separated ingestion, quality, knowledge, AI, and API responsibilities |
| Real-Time / Event-Driven Pipelines | Local asynchronous Producer → Broker → Consumer demonstration |
| Vector Databases | Persistent ChromaDB collection using cosine similarity |
| Advanced RAG | Load → chunk → embed → store; query embedding → top-k retrieval → context → grounded generation |
| Data Quality | Completeness, supported-file-type, duplicate checks, and quarantine |
| Governance | Authorized-source rule, common PII-pattern redaction, and audit logging |
| Lineage / Traceability | Source, chunk ID, request ID, processing metadata, and audit events |
| Evaluation | Lightweight retrieval evaluation and abstention behavior |
| Architecture Integration | FastAPI exposes the integrated application |

## Relationship to the Day 3 RAG example

The Day 3 material defines RAG as Retrieve → Augment → Generate and separates the pipeline into indexing and querying. It also demonstrates a FastAPI-based application using embeddings, a vector database, PDF processing, and an LLM.

Hail Heritage RAG follows the same architectural learning objective but uses a different domain: authorized museum and visitor-center knowledge in the Hail Region.

## Scope and integrity

This repository is a local capstone proof of concept. Kafka, Redpanda, distributed vector databases, Lakehouse infrastructure, Kubernetes, and enterprise IAM/observability are documented as production evolution options; they are not represented as deployed components.

The included sample knowledge is project documentation for demonstration and is not represented as an official museum database.
