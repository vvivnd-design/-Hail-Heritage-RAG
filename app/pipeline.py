import json, shutil, uuid
from datetime import datetime, timezone
from pathlib import Path
from app.documents import load_document, recursive_chunk
from app.quality import validate_document
from app.audit import write_audit

RAW=Path("data/raw"); QUARANTINE=Path("data/quarantine"); PROCESSED=Path("data/processed")
for directory in (RAW, QUARANTINE, PROCESSED):
    directory.mkdir(parents=True, exist_ok=True)

def ingest_all(store):
    seen=set(); details=[]; accepted=quarantined=indexed=0
    for path in sorted(RAW.iterdir()):
        if not path.is_file() or path.name.startswith("."): continue
        report, clean = validate_document(path, load_document(path), seen)
        details.append(report.to_dict())
        if not report.valid:
            quarantined += 1
            shutil.copy2(path, QUARANTINE/path.name)
            write_audit({"event":"document_quarantined", **report.to_dict()})
            continue
        payload=[]
        for i,chunk in enumerate(recursive_chunk(clean)):
            payload.append({"id":f"{path.stem}-{i}-{uuid.uuid4().hex[:8]}",
                            "text":chunk,
                            "metadata":{"source":path.name,"chunk_index":i,
                                        "ingested_at":datetime.now(timezone.utc).isoformat(),
                                        "pii_redacted":report.pii_detected}})
        indexed += store.add_chunks(payload); accepted += 1
        (PROCESSED/f"{path.stem}.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8")
        write_audit({"event":"document_indexed","source":path.name,"chunks":len(payload)})
    return {"accepted":accepted,"quarantined":quarantined,"chunks_indexed":indexed,"details":details}
