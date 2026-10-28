#!/usr/bin/env python3
from pathlib import Path
import json, copy

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE_PATH = ROOT / "iterations/012/data/evidence.json"

def derive(evidence):
    occ = evidence["occurrences"]
    secure_counted = [
        o for o in occ
        if o["normalized"] == "QI-TU-NE"
        and o["reading_status"] == "secure_for_structural_test"
        and o["position"] == "counted_entry"
        and o.get("quantity") == 1
    ]
    secure_heading = [
        o for o in occ
        if o["normalized"] == "QI-TU-NE"
        and o["reading_status"] == "secure_for_structural_test"
        and o["position"] in {"heading_component", "subheading"}
    ]
    di_docs = [
        o["document"] for o in secure_heading
        if any(str(x).startswith("DI-KI-SE 1") for x in o.get("entries_include", []))
    ]
    source_ids = {s for o in occ for s in o.get("source_ids", [])}
    return {
        "secure_counted_documents": [o["document"] for o in secure_counted],
        "secure_heading_documents": [o["document"] for o in secure_heading],
        "secure_cross_position": bool(secure_counted and secure_heading),
        "di_ki_se_under_qi_tu_ne_documents": di_docs,
        "replicated_di_relation": len(set(di_docs)) >= 2,
        "ht94_required_for_cross_position": "HT 94b" in {o["document"] for o in secure_counted + secure_heading},
        "source_coverage_nonempty": len(source_ids) > 0,
        "full_action_and_roles": False,
    }

def assert_baseline(result):
    assert result["secure_cross_position"] is True
    assert "HT 7b" in result["secure_counted_documents"]
    assert {"HT 87", "HT 117b"}.issubset(set(result["secure_heading_documents"]))
    assert result["replicated_di_relation"] is True
    assert result["ht94_required_for_cross_position"] is False
    assert result["source_coverage_nonempty"] is True
    assert result["full_action_and_roles"] is False

def failure_injection_tests(evidence):
    tests = {}

    # Removing the restored HT94 witness must NOT break the secure result.
    e = copy.deepcopy(evidence)
    e["occurrences"] = [o for o in e["occurrences"] if o["document"] != "HT 94b"]
    r = derive(e)
    tests["remove_ht94_result_survives"] = r["secure_cross_position"] and r["replicated_di_relation"]

    # Removing HT7 must break the secure count-vs-heading contrast.
    e = copy.deepcopy(evidence)
    e["occurrences"] = [o for o in e["occurrences"] if o["document"] != "HT 7b"]
    tests["remove_ht7_breaks_cross_position"] = not derive(e)["secure_cross_position"]

    # Downgrading HT7 reading must also break it.
    e = copy.deepcopy(evidence)
    for o in e["occurrences"]:
        if o["document"] == "HT 7b":
            o["reading_status"] = "uncertain"
    tests["uncertain_ht7_breaks_cross_position"] = not derive(e)["secure_cross_position"]

    # Removing DI-KI-SE from one heading witness must break replication.
    e = copy.deepcopy(evidence)
    for o in e["occurrences"]:
        if o["document"] == "HT 87":
            o["entries_include"] = [x for x in o.get("entries_include", []) if not str(x).startswith("DI-KI-SE")]
    tests["remove_one_di_breaks_replication"] = not derive(e)["replicated_di_relation"]

    # Removing all sources must be detected.
    e = copy.deepcopy(evidence)
    for o in e["occurrences"]:
        o["source_ids"] = []
    tests["missing_sources_detected"] = not derive(e)["source_coverage_nonempty"]

    assert all(tests.values()), tests
    return tests

def main():
    evidence = json.loads(EVIDENCE_PATH.read_text())
    result = derive(evidence)
    assert_baseline(result)
    tests = failure_injection_tests(evidence)

    out = {
        "derived_findings": result,
        "failure_injection_tests": tests,
        "note": "Structural/computational verification only. Semantic model preferences remain interpretive."
    }
    out_path = ROOT / "iterations/012/results/derived_findings.json"
    out_path.write_text(json.dumps(out, indent=2) + "\n")
    print("Iteration 12 structural verification passed.")
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
