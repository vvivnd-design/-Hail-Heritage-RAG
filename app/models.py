from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    top_k: Optional[int] = Field(default=None, ge=1, le=10)

class SourceItem(BaseModel):
    source: str
    chunk_id: str
    score: float
    text: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceItem]
    grounded: bool
    request_id: str

class IngestResponse(BaseModel):
    accepted: int
    quarantined: int
    chunks_indexed: int
    details: List[dict]
