import re, hashlib
from dataclasses import dataclass, asdict
from pathlib import Path

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
SA_PHONE_RE = re.compile(r"(?<!\d)(?:\+?966|0)?5\d{8}(?!\d)")
ID_RE = re.compile(r"(?<!\d)\d{10}(?!\d)")

@dataclass
class QualityReport:
    source: str
    valid: bool
    completeness: bool
    validity: bool
    uniqueness: bool
    pii_detected: bool
    reasons: list[str]
    def to_dict(self): return asdict(self)

def normalize_text(text: str) -> str:
    return " ".join(text.replace("\x00", " ").split())

def redact_pii(text: str) -> str:
    text = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    text = SA_PHONE_RE.sub("[REDACTED_PHONE]", text)
    return ID_RE.sub("[REDACTED_ID]", text)

def validate_document(path: Path, text: str, seen_hashes: set[str]):
    clean = normalize_text(text)
    reasons = []
    completeness = len(clean) >= 80
    if not completeness: reasons.append("Document is too short or empty.")
    validity = path.suffix.lower() in {".pdf", ".txt", ".md"}
    if not validity: reasons.append("Unsupported file type.")
    digest = hashlib.sha256(clean.encode("utf-8")).hexdigest()
    uniqueness = digest not in seen_hashes
    if uniqueness: seen_hashes.add(digest)
    else: reasons.append("Duplicate document content.")
    pii = bool(EMAIL_RE.search(clean) or SA_PHONE_RE.search(clean) or ID_RE.search(clean))
    return QualityReport(path.name, completeness and validity and uniqueness, completeness, validity, uniqueness, pii, reasons), redact_pii(clean)
