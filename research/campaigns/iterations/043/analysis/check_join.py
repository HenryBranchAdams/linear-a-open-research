"""Reproduce the finite C043 admission decision; no semantic model is fitted."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
rows = json.loads((ROOT / "evidence/JOIN_FINAL.json").read_text())["rows"]
unknown_negatives = [
    {**r, "inscription_status": "unknown"}
    if r["inscription_status"] == "explicit_catalogue_no_signs" else r
    for r in rows
]

def summarize(name, subset):
    readable = [r for r in subset if r["inscription_status"] == "readable_corpus_join"]
    classes = sorted({r["physical_function_author_report"] for r in readable})
    return {
        "branch": name,
        "selected_carriers": len(subset),
        "readable_carriers": [r["site"] + " " + r["inventory"] for r in readable],
        "readable_classes": classes,
        "cross_function_comparison_admitted": len(classes) > 1,
    }

result = {
    "purpose": "eligibility and sensitivity only; counts do not establish meaning",
    "branches": [
        summarize("all selected carriers", rows),
        summarize("HT only", [r for r in rows if r["site"] == "HT"]),
        summarize("catalogued complete only", [r for r in rows if r["source_fields"].get("Erhaltung") == ["komplett"]]),
        summarize("all catalogue negatives treated as unknown", unknown_negatives),
    ],
    "semantic_test_admitted": False,
    "reason": "No readable member of the reconstructed two-cord-end securing class.",
}
print(json.dumps(result, indent=2, ensure_ascii=False))
