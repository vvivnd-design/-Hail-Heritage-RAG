import uuid
from fastapi import FastAPI
from app.models import QueryRequest, QueryResponse, SourceItem, IngestResponse
from app.vector_store import VectorStore
from app.pipeline import ingest_all
from app.llm import generate_answer
from app.config import settings
from app.audit import write_audit

app=FastAPI(title="Hail Heritage RAG",version="1.0.0",
            description="Governed Arabic-first RAG application for museum and visitor-center knowledge.")
_store=None
def get_store():
    global _store
    if _store is None: _store=VectorStore()
    return _store

@app.get("/health")
def health(): return {"status":"ok","service":"hail-heritage-rag"}

@app.post("/ingest",response_model=IngestResponse)
def ingest(): return ingest_all(get_store())

@app.post("/query",response_model=QueryResponse)
def query(req: QueryRequest):
    request_id=str(uuid.uuid4())
    hits=get_store().search(req.question, req.top_k or settings.top_k)
    usable=[h for h in hits if h["score"] >= settings.min_retrieval_score]
    answer=generate_answer(req.question,usable)
    sources=[SourceItem(source=h["metadata"].get("source","unknown"),
                        chunk_id=h["chunk_id"],score=round(h["score"],4),text=h["text"][:700]) for h in usable]
    write_audit({"event":"query","request_id":request_id,"question":req.question,
                 "retrieved":len(sources),"grounded":bool(usable),"sources":[s.source for s in sources]})
    return QueryResponse(answer=answer,sources=sources,grounded=bool(usable),request_id=request_id)
