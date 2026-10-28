#!/usr/bin/env python3
"""Exact rational sensitivity comparison for C042; no external packages.

Inputs are publication-specific extractions. Outputs are model consequences,
not measured ancient units or amounts. Run from any working directory:
    python3 capacity_comparison.py
"""
from pathlib import Path
from fractions import Fraction
import csv
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "capacity_inputs.json"
raw = INPUT.read_bytes()
data = json.loads(raw)
rule = (ROOT / data["analysis_rule"]).read_bytes()
assert hashlib.sha256(rule).hexdigest() == data["analysis_rule_sha256"], "Frozen rule changed"

def ratio(value):
    return Fraction(str(value))

def output(value):
    return {"fraction": str(value), "decimal": float(value)}

kn = data["capacity_source_inputs"]["KNZb27"]
za = data["capacity_source_inputs"]["ZAZb3"]
v_kn = ratio(kn["litres_nominal"])
v_za = ratio(za["litres_nominal"])
lo_za, hi_za = ratio(za["lower"]), ratio(za["upper"])
assert 0 < lo_za <= v_za <= hi_za
assert lo_za == v_za * (1-ratio(za["relative_tolerance"]))
assert hi_za == v_za * (1+ratio(za["relative_tolerance"]))

rows = []
for branch_kn in data["reading_branches"]["KNZb27"]:
    for branch_za in data["reading_branches"]["ZAZb3"]:
        q_kn, q_za = branch_kn["q"], branch_za["q"]
        assert q_kn > 0 and q_za > 0
        u_kn, u_za = v_kn/q_kn, v_za/q_za
        u_za_low, u_za_high = lo_za/q_za, hi_za/q_za
        # If ZA is full at its published tolerance, KN's required full capacity.
        kn_required_low, kn_required, kn_required_high = q_kn*u_za_low, q_kn*u_za, q_kn*u_za_high
        # If KN is full at its nominal capacity, ZA's corresponding amount.
        za_if_kn_full = q_za*u_kn
        # Existence of partial-fill solutions is constructive: use <=min(V_i/q_i).
        u_partial_max_nominal = min(u_kn, u_za)
        u_partial_witness = u_partial_max_nominal/2
        f_kn_witness = q_kn*u_partial_witness/v_kn
        f_za_witness = q_za*u_partial_witness/v_za
        assert 0 < f_kn_witness <= 1 and 0 < f_za_witness <= 1
        assert q_za*u_partial_witness <= lo_za
        assert f_kn_witness/f_za_witness == u_za/u_kn
        rows.append({
            "KN_q": q_kn,
            "ZA_q": q_za,
            "KN_reading_status": branch_kn["status"],
            "ZA_reading_status": branch_za["status"],
            "KN_full_unit_L_nominal": output(u_kn),
            "ZA_full_unit_L_nominal": output(u_za),
            "ZA_full_unit_L_source_low": output(u_za_low),
            "ZA_full_unit_L_source_high": output(u_za_high),
            "nominal_full_units_equal": u_kn == u_za,
            "KN_nominal_unit_inside_ZA_source_interval": u_za_low <= u_kn <= u_za_high,
            "formal_two_object_interval_decision_available": False,
            "reason_formal_interval_unavailable": "KN reports about34L without an uncertainty interval.",
            "KN_capacity_required_L_if_ZA_full_low": output(kn_required_low),
            "KN_capacity_required_L_if_ZA_full_nominal": output(kn_required),
            "KN_capacity_required_L_if_ZA_full_high": output(kn_required_high),
            "KN_required_capacity_factor_minimum_vs_34L": output(kn_required_low/v_kn),
            "full_unit_ratio_ZA_to_KN_nominal": output(u_za/u_kn),
            "ZA_amount_L_if_KN_full_same_unit": output(za_if_kn_full),
            "ZA_fill_fraction_if_KN_full_nominal": output(za_if_kn_full/v_za),
            "ZA_fill_fraction_if_KN_full_low": output(za_if_kn_full/hi_za),
            "ZA_fill_fraction_if_KN_full_high": output(za_if_kn_full/lo_za),
            "partial_fill_feasible_nominal": True,
            "partial_fill_feasible_source_ZA_interval_and_nominal_KN": True,
            "positive_unit_upper_bound_partial_fill_L_nominal": output(u_partial_max_nominal),
            "partial_fill_constructive_witness_u_L": output(u_partial_witness),
            "partial_fill_constructive_witness_f_KN": output(f_kn_witness),
            "partial_fill_constructive_witness_f_ZA": output(f_za_witness),
            "fill_fraction_ratio_KN_to_ZA_common_unit_nominal": output(u_za/u_kn),
            "ordinal_inversion": (v_kn < lo_za and q_kn > q_za),
        })

geometry = data.get("posthoc_geometry_sensitivity")
geometry_result = None
if geometry:
    height_m = float(ratio(geometry["KN_height_cm_reported"])/100)
    bound_litres = math.pi * height_m**3/4 * 1000
    geometry_rows = []
    for row in rows:
        required = row["KN_capacity_required_L_if_ZA_full_low"]["decimal"]
        geometry_rows.append({
            "KN_q": row["KN_q"],
            "ZA_q": row["ZA_q"],
            "required_KN_capacity_low_L": required,
            "required_capacity_to_conditional_envelope_ratio": required/bound_litres,
            "exceeds_conditional_envelope": required > bound_litres,
            "minimum_height_cm_for_D_equals_H_envelope_to_hold_required_capacity": 100*(4*required/(1000*math.pi))**(1/3)
        })
    geometry_result = {
        "status": geometry["status"],
        "height_m": height_m,
        "conditional_external_cylinder_bound_L": bound_litres,
        "assumptions": geometry["assumptions"],
        "limitation": geometry["limitation"],
        "comparisons": geometry_rows
    }

result = {
    "input_sha256": hashlib.sha256(raw).hexdigest(),
    "analysis_rule_sha256": data["analysis_rule_sha256"],
    "model_status": {
        "M1_same_unit_full_capacity": "Every nominal reading branch mismatches; no formal two-object tolerance test since KN has no error bounds. Required capacity adjustments quantified.",
        "M2_same_unit_partial_fill": "Feasible for every branch; unconstrained sufficiently small positive common units exist.",
        "M3_scope_beyond_carrier": "Not identified; many beyond-carrier scopes survive but are not established.",
        "M4_different_units_full_capacity": "Feasible by assigning each source-derived V/q its own unit; independent unit equivalence needed.",
        "M5_same_unit_same_fill_fraction": "Same ratio incompatibility as M1. Variable fill fractions survive."
    },
    "interpretation_limits": [
        "Output precision is computational only; input capacities remain approximations.",
        "Source tolerance is not a statistical confidence interval.",
        "Historical readings are sensitivity branches, not equal-weight alternatives to autopsy107.",
        "Common AB131/VIN notation does not by itself prove common unit size.",
        "No quantity, capacity or fit identifies inscription action, owner, maker, supplier or recipient.",
        "No p-value or replication claim is warranted."
    ],
    "comparisons": rows,
    "posthoc_geometry_sensitivity": geometry_result
}
(ROOT / "capacity_results.json").write_text(json.dumps(result, indent=2, ensure_ascii=False)+"\n")
fields = ["KN_q", "ZA_q", "KN_full_unit_L_nominal", "ZA_full_unit_L_nominal", "ZA_full_unit_L_source_low", "ZA_full_unit_L_source_high", "KN_capacity_required_L_if_ZA_full_low", "KN_required_capacity_factor_minimum_vs_34L", "full_unit_ratio_ZA_to_KN_nominal", "ZA_fill_fraction_if_KN_full_nominal", "ordinal_inversion"]
with (ROOT / "capacity_results.csv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    for row in rows:
        writer.writerow({key: row[key]["decimal"] if isinstance(row[key],dict) else row[key] for key in fields})
print(f"Wrote {len(rows)} source-status-preserving scenarios to capacity_results.json and capacity_results.csv")
for row in rows:
    print(f"KN{row['KN_q']}/ZA{row['ZA_q']}: KN full unit={row['KN_full_unit_L_nominal']['decimal']:.6f} L; ZA full unit={row['ZA_full_unit_L_nominal']['decimal']:.6f} L; minimum KN capacity factor={row['KN_required_capacity_factor_minimum_vs_34L']['decimal']:.3f}; partial-fill feasible")
if geometry_result:
    minimum = min(x["required_capacity_to_conditional_envelope_ratio"] for x in geometry_result["comparisons"])
    print(f"Post hoc conditional geometric envelope={bound_litres:.3f} L; weakest required-capacity/envelope ratio={minimum:.3f}")
