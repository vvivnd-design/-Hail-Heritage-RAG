import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

AUDIT_LOG = os.getenv("AUDIT_LOG", "logs/audit.jsonl")

@dataclass(frozen=True)
class Settings:
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    openrouter_model: str = os.getenv("OPENROUTER_MODEL", "qwen/qwen3-coder:free")
    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    )
    chroma_dir: str = os.getenv("CHROMA_DIR", "storage/chroma")
    collection_name: str = os.getenv("COLLECTION_NAME", "hail_heritage")
    top_k: int = int(os.getenv("TOP_K", "5"))
    min_retrieval_score: float = float(os.getenv("MIN_RETRIEVAL_SCORE", "0.20"))

settings = Settings()
