from pathlib import Path
from pypdf import PdfReader

def load_document(path: Path) -> str:
    if path.suffix.lower() in {".txt", ".md"}:
        return path.read_text(encoding="utf-8", errors="ignore")
    if path.suffix.lower() == ".pdf":
        return "\n".join((p.extract_text() or "") for p in PdfReader(str(path)).pages)
    return ""

def recursive_chunk(text: str, chunk_size: int = 900, overlap: int = 120) -> list[str]:
    paragraphs = [p.strip() for p in text.splitlines() if p.strip()]
    chunks, current = [], ""
    for p in paragraphs:
        candidate = f"{current}\n{p}".strip()
        if len(candidate) <= chunk_size:
            current = candidate
            continue
        if current: chunks.append(current)
        if len(p) <= chunk_size:
            current = p
        else:
            step = max(1, chunk_size - overlap)
            chunks.extend(p[i:i+chunk_size] for i in range(0, len(p), step))
            current = ""
    if current: chunks.append(current)
    return [c for c in chunks if len(c) >= 40]
