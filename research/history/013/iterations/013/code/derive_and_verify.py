#!/usr/bin/env python3
from pathlib import Path
import json, copy

ROOT = Path(__file__).resolve().parents[3]
E = json.loads((ROOT/"iterations/013/data/evidence.json").read_text())

def derive(e):
    pure = e["construction"]["secure_personnel_witnesses"]
    totals = []
    for w in pure:
        n = sum(int(x.rsplit(" ", 1)[1]) for x in w["entries"])
        totals.append({
            "document": w["document"],
            "computed": n,
            "written": w["ku_ro_total"],
            "matches": n == w["ku_ro_total"]
        })
    return {
        "pure_witness_count": len(pure),
        "all_personnel_totals_match": all(t["matches"] for t in totals),
        "totals": totals,
        "cross_domain_control_count": len(e["cross_domain_controls"]),
        "fixed_negative_sign_supported": e["sign_test"]["deficit_missing"]["status"] == "identified",
        "functional_core": e["sign_test"]["differential_exception_balance"]["status"],
        "full_action_and_roles": e["mission_result"]["full_action_and_roles"]
    }

def assert_baseline(r):
    assert r["pure_witness_count"] >= 2
    assert r["all_personnel_totals_match"]
    assert r["cross_domain_control_count"] >= 2
    assert not r["fixed_negative_sign_supported"]
    assert r["functional_core"] == "best_supported_functional_core"
    assert not r["full_action_and_roles"]

def failure_tests(e):
    tests = {}
    x = copy.deepcopy(e)
    x["construction"]["secure_personnel_witnesses"][0]["ku_ro_total"] = 7
    tests["wrong_ht88_total_detected"] = not derive(x)["all_personnel_totals_match"]

    x = copy.deepcopy(e)
    x["construction"]["secure_personnel_witnesses"] = x["construction"]["secure_personnel_witnesses"][:1]
    tests["single_witness_is_not_replication"] = derive(x)["pure_witness_count"] < 2

    x = copy.deepcopy(e)
    x["cross_domain_controls"] = []
    tests["loss_of_cross_domain_controls_detected"] = derive(x)["cross_domain_control_count"] == 0

    assert all(tests.values()), tests
    return tests

r = derive(E)
assert_baseline(r)
tests = failure_tests(E)
out = {
    "derived": r,
    "failure_injection_tests": tests,
    "scope_note": "Verifier proves replication/arithmetic only. The differential/exception functional gloss remains an evidence synthesis, not machine-derived lexical decipherment."
}
(ROOT/"iterations/013/results/verification.json").write_text(json.dumps(out, indent=2)+"\n")
print("Iteration 13 verification passed.")
print(json.dumps(out, indent=2))
