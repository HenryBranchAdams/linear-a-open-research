#!/usr/bin/env python3
"""Summarize frozen public-corpus queries without silently healing broken words.

Run from any working directory. No network or third-party packages are required.
This reproduces bookkeeping and a stated conditional comparison, not decipherment.
"""
import json
from pathlib import Path


def run():
    root = Path(__file__).resolve().parents[1]
    ledger = json.loads((root / "notes" / "linear_b.json").read_text())
    query_summary = []
    for query in ledger["queries"]:
        rows = query["rows"]
        query_summary.append({
            "query": query["query"],
            "mode": query["match_mode"],
            "reported_rows": query["reported_hits"],
            "stored_rows": len(rows),
            "unique_objects": len({r["object_internal_id"] for r in rows}),
            "unique_tokens": len({r["token_internal_id"] for r in rows}),
            "distinct_raw_forms": sorted({r["raw_form"] for r in rows}),
        })

    observed = {o["id"]: o for o in ledger["observations"]}
    tanat = [observed["LB01"], observed["LB05"]]
    # Read completeness from the occurrence-level critical audit, not API matching.
    intact = [o["normalized_target"] for o in tanat if o["target_complete"]]
    broken = [o["diplomatic"] for o in tanat if not o["target_complete"]]
    controls = [{
        "pair": f'{c["la"]} / {c["lb"]}',
        "LA_final_vowel": c["la"][-1],
        "LB_final_vowel": c["lb"][-1],
        "status": c["cross_script_identity"],
    } for c in ledger["controls"]]
    ortho = ledger["conditional_orthography"]
    return {
        "queries": query_summary,
        "complete_target_comparanda": intact,
        "incomplete_target_comparanda": broken,
        "selected_correspondence_controls": controls,
        "ordinary_o_stem_case_contrast": {
            "assumption": ortho["assumption"],
            "nominative_expected_final": ortho["nominative_expected_written_final"],
            "dative_expected_final": ortho["dative_expected_written_final"],
            "Uf311_final_matches_expected_dative": (
                ortho["observed_Uf_final"] == ortho["dative_expected_written_final"]
            ),
            "authority": ortho["source_id"],
            "limitation": ortho["limitation"],
        },
        "interpretive_scope": "Supports a Linear B person-related designation; establishes no Linear A sentence, role, or cross-form referent identity.",
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
