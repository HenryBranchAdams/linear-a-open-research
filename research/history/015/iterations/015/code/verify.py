#!/usr/bin/env python3
from pathlib import Path
import json, copy

ROOT = Path(__file__).resolve().parents[3]
E = json.loads((ROOT/"iterations/015/data/ht100_adjudication.json").read_text())

def arithmetic():
    if4 = 58+4+12+2+5+16
    if6_excluding_ki = 58+6+12+5+16
    if6_including_ki = 58+6+12+2+5+16
    if4_excluding_ki = 58+4+12+5+16
    return {
        "if4_including_ki": if4,
        "if4_excluding_ki": if4_excluding_ki,
        "if6_excluding_ki": if6_excluding_ki,
        "if6_including_ki": if6_including_ki
    }

A = arithmetic()
assert A["if4_including_ki"] == 97
assert A["if6_excluding_ki"] == 97
assert A["if4_excluding_ki"] == 95
assert A["if6_including_ki"] == 99

readings = {x["source"]: x for x in E["source_readings"]}
assert readings["GORILA I"]["reading"] is None
assert readings["Uchitel"]["reading"] == 4
assert readings["CTLA"]["reading"] == 6
assert readings["current lineara.xyz / Younger-derived transcription"]["reading"] is None
assert readings["current AIgent structured corpus (Linear A Explorer / GORILA source)"]["reading"] is None

assert E["adjudication"]["secure_reading"] is None
assert not E["adjudication"]["four_secure"]
assert not E["adjudication"]["six_secure"]
assert E["polarity_result"]["ki_polarity_from_ht100"] == "not_identifiable"

# Failure injection: either claimed secure value must contradict the source-critical state.
def source_critical_ok(e):
    return (
        e["adjudication"]["secure_reading"] is None
        and readings["GORILA I"]["reading"] is None
    )

e4 = copy.deepcopy(E)
e4["adjudication"]["secure_reading"] = 4
e6 = copy.deepcopy(E)
e6["adjudication"]["secure_reading"] = 6

tests = {
    "claiming_4_secure_fails": not source_critical_ok(e4),
    "claiming_6_secure_fails": not source_critical_ok(e6),
    "baseline_unresolved_passes": source_critical_ok(E)
}
assert all(tests.values())

out = {
    "arithmetic": A,
    "source_critical_adjudication": "unresolved",
    "ki_polarity": "not_identifiable_from_HT100",
    "failure_injection_tests": tests,
    "note": "Arithmetic is deterministic; epigraphic status is encoded from the audited source hierarchy and is not a machine-vision reading."
}
(ROOT/"iterations/015/results/verification.json").write_text(json.dumps(out, indent=2)+"\n")
print("Iteration 15 HT100 verification passed.")
print(json.dumps(out, indent=2))
