import json
from datetime import datetime, timezone
from pathlib import Path
from app.config import AUDIT_LOG

LOG = Path(AUDIT_LOG)

def write_audit(event: dict):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        record = {"timestamp": datetime.now(timezone.utc).isoformat(), **event}
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
