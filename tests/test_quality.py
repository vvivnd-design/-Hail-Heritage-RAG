from pathlib import Path
from app.quality import validate_document, redact_pii
def test_redaction():
    out=redact_pii("test@example.com 0501234567")
    assert "[REDACTED_EMAIL]" in out and "[REDACTED_PHONE]" in out
def test_short_document_rejected():
    report,_=validate_document(Path("x.txt"),"قصير",set())
    assert report.valid is False
