import chromadb
from sentence_transformers import SentenceTransformer
from app.config import settings

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.chroma_dir)
        self.collection = self.client.get_or_create_collection(
            name=settings.collection_name, metadata={"hnsw:space": "cosine"}
        )
        self.model = SentenceTransformer(settings.embedding_model)

    def add_chunks(self, chunks: list[dict]) -> int:
        if not chunks: return 0
        texts = [c["text"] for c in chunks]
        embeddings = self.model.encode(texts, normalize_embeddings=True).tolist()
        self.collection.upsert(
            ids=[c["id"] for c in chunks],
            documents=texts,
            metadatas=[c["metadata"] for c in chunks],
            embeddings=embeddings,
        )
        return len(chunks)

    def search(self, query: str, top_k: int) -> list[dict]:
        q = self.model.encode([query], normalize_embeddings=True).tolist()
        r = self.collection.query(query_embeddings=q, n_results=top_k, include=["documents","metadatas","distances"])
        if not r["ids"] or not r["ids"][0]: return []
        return [
            {"chunk_id": cid, "text": doc, "metadata": meta, "score": max(0.0, 1.0-float(dist))}
            for cid, doc, meta, dist in zip(r["ids"][0], r["documents"][0], r["metadatas"][0], r["distances"][0])
        ]
