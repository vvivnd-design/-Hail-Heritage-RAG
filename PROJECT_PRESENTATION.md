# 5-Minute Project Presentation | عرض المشروع

## 1. Problem | المشكلة
Knowledge about museums and visitor centers can be distributed across reports, surveys, policies, and documents. Manual search is slow, while a standalone LLM may answer without documentary evidence.

## 2. Solution | الحل
Hail Heritage RAG is an Arabic-first governed RAG application that validates authorized documents, redacts common PII patterns, creates multilingual embeddings, indexes chunks in a vector database, retrieves evidence, and returns grounded answers with source metadata.

## 3. Architecture
Documents -> Quality Gate -> Governance -> Chunking -> Embeddings -> Vector DB -> Retrieval -> LLM -> Evidence + Audit.

## 4. Course Alignment
Day 1: modern scalable data architecture.
Day 2: event-driven pipeline simulation.
Day 3: embeddings, vector database, similarity search, advanced RAG.
Day 4: data quality, governance, lineage/audit.
Day 5: integrated architecture, documentation, presentation, technical review.

## 5. Live Demo
1. Run `uvicorn app.main:app --reload`.
2. Open `/docs`.
3. POST `/ingest`.
4. POST `/query` with: `كيف تتعامل المنصة مع البيانات الشخصية؟`
5. Show answer, source, chunk ID, score, grounded flag, request ID.
6. Ask an unsupported question and show safe abstention.

## Closing
The value is not merely a chatbot. The project demonstrates a governed data pipeline that makes AI answers traceable to retrieved knowledge.
