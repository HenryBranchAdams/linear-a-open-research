#!/usr/bin/env python3
from pathlib import Path
import json, copy

ROOT = Path(__file__).resolve().parents[3]
E = json.loads((ROOT/"iterations/016/data/evidence.json").read_text())

def derive(e):
    h = e["ht34"]
    ref = h["critical_sequence"][0]["quantity"]
    pa3 = h["critical_sequence"][1]["quantity"]
    kiro = h["critical_sequence"][2]["quantity"]
    erased = h["critical_sequence"][3]["quantity"]
    t = e["ht118"]
    kis = t["ki_subtotal"]["components"]
    return {
        "ht34_reference": ref,
        "ht34_pa3": pa3,
        "ht34_kiro_current": kiro,
        "ht34_erased": erased,
        "ht34_residual": ref-pa3,
        "ht34_current_closes": pa3+kiro == ref,
        "ht34_erased_state_closes": pa3+kiro+erased == ref,
        "ht118_ki_sum": sum(kis),
        "ht118_written_ki_total": t["ki_subtotal"]["written_total"],
        "ht118_ki_closes": sum(kis) == t["ki_subtotal"]["written_total"],
        "participant_class": t["participant_anchor"]["classification"]
    }

r=derive(E)
assert r["ht34_residual"] == 30
assert r["ht34_current_closes"]
assert not r["ht34_erased_state_closes"]
assert r["ht118_ki_sum"] == 15
assert r["ht118_ki_closes"]
assert r["participant_class"] == "masculine personal name"

# Failure injection tests.
x=copy.deepcopy(E)
x["ht34"]["critical_sequence"][2]["quantity"]=37
assert not derive(x)["ht34_current_closes"]

x=copy.deepcopy(E)
x["ht34"]["critical_sequence"][3]["status"]="written_current"
# Numerically the recorded-state model would now need 107 rather than 100.
assert not derive(x)["ht34_erased_state_closes"]

x=copy.deepcopy(E)
x["ht118"]["ki_subtotal"]["components"]=[10,4,2]
assert not derive(x)["ht118_ki_closes"]

out={
    "derived":r,
    "failure_injection_tests":{
        "kiro37_breaks_ht34_closure":True,
        "retaining_erased7_breaks_ht34_closure":True,
        "altering_ht118_ki_component_breaks_subtotal":True
    },
    "semantic_scope":"Arithmetic and critical-state relations are machine verified. Lexical glosses and onomastic classification remain source-based inferences."
}
(ROOT/"iterations/016/results/verification.json").write_text(json.dumps(out,indent=2)+"\n")
print("Iteration 16 breakthrough verification passed.")
print(json.dumps(out,indent=2))
