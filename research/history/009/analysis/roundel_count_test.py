#!/usr/bin/env python3
"""Test a common impression/commodity conversion against published intervals.

Run from any directory. No external dependencies or network.
This excludes a quantitative generalization; it does not translate any word.
Fraction signs remain unvalued: only 0 < f < 1 is assumed in the strict test.
"""
from pathlib import Path
from fractions import Fraction
import json

ROOT = Path(__file__).resolve().parents[1]
ledger = json.loads((ROOT / "notes" / "roundels.json").read_text())
obs = {r["id"]: r for r in ledger["observations"]}

integer_anchors = []
for key in ("R12", "R13"):
    r = obs[key]
    scale = Fraction(r["seal_impressions_options"][0], r["face_quantity"]["integer"])
    integer_anchors.append({"inscription": r["inscription"], "impressions_per_face_unit": str(scale)})
forced_scales = {a["impressions_per_face_unit"] for a in integer_anchors}
assert len(forced_scales) == 1
fixed_scale = Fraction(next(iter(forced_scales)))

fraction_results = []
for key in ("R14", "R15"):
    r = obs[key]
    integer = r["face_quantity"]["integer"]
    tests = []
    for impressions in r["seal_impressions_options"]:
        # Under common scale k, equality s=k*(n+f) forces f=s/k-n.
        required_f = Fraction(impressions, 1) / fixed_scale - integer
        tests.append({"seal_impressions": impressions,
                      "required_fraction": str(required_f),
                      "valid_positive_proper_fraction": 0 < required_f < 1})
    fraction_results.append({"inscription": r["inscription"], "fraction_sign": r["face_quantity"]["fraction_sign"],
                             "period_scope": r["period_scope"], "alternatives": tests,
                             "compatible_with_fixed_scale": any(x["valid_positive_proper_fraction"] for x in tests)})

result = {
    "model": "One common proportionality: seal impressions = k * additive face commodity quantity",
    "assumptions": ["Integer face quantities have comparable counting semantics",
                    "Fraction signs are additive positive proper fractions, not multipliers",
                    "Reported seal-count alternatives are exhaustive within this test"],
    "integer_anchors": integer_anchors,
    "forced_k": str(fixed_scale),
    "fraction_cases": fraction_results,
    "neopalatial_common_scale_survives_reported_malia_counts": fraction_results[0]["compatible_with_fixed_scale"],
    "za_wc2_sensitivity": [{"impressions": s, "face_quantity": 2, "matches_forced_scale": s == fixed_scale * 2} for s in [2,4]],
    "meaning": "GO and HT fix k=1; MA's reported 1/2 impressions require negative fraction values. PH, outside chapter scope, would require fraction1 rather than a proper fraction.",
    "limits": "Unknown/unrecorded Malia impressions, nonadditive reading, or different ration/commodity measures can evade this narrow model. The animal counts retain local evidential value. No direction or verb is inferred.",
    "source_observation_ids": ["R04","R05","R06","R12","R13","R14","R15"]
}
out = ROOT / "results" / "roundel_count_test.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
