"""Preserve the exposed index row and literal token matches; no semantic inference."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
source = ROOT / "corpus/discovery_snapshot.json"
raw = source.read_bytes()
rows = json.loads(raw)
token = "*410-VS"
matches = [key for key, row in rows.items() if token in row.get("transliteratedWords", [])]
result = {
    "snapshot_sha256": hashlib.sha256(raw).hexdigest(),
    "literal_token": token,
    "literal_token_document_matches": matches,
    "scope": "Frozen project discovery index, exact token only; not all-edition uniqueness or unused validation.",
    "target_id": "HT31",
    "target_raw_row": rows["HT31"],
    "normalization_performed": False,
}
print(json.dumps(result, ensure_ascii=False, indent=2))
