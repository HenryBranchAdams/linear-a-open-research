"""Independent arithmetic reconstruction for C042 review.

Source values are conditional inputs, not remeasurements. ZA's 11% is the
published tolerance, not a probability distribution. KN's about 34 L has no
published interval in the inspected text. Historical numerals are sensitivity
branches and do not carry equal evidentiary status.
"""
from fractions import Fraction
import json
import math

kn = Fraction(34)
za = Fraction(556)
za_low = za * Fraction(89, 100)
za_high = za * Fraction(111, 100)
rows = []
for nk in (107, 117, 17):
    for nz in (32, 22, 21):
        rows.append({
            "KN_numeral": nk,
            "ZA_numeral": nz,
            "KN_implied_full_unit_L": float(kn / nk),
            "ZA_implied_full_unit_L": float(za / nz),
            "ZA_to_KN_implied_unit_ratio": float((za / nz) / (kn / nk)),
            "required_KN_capacity_at_ZA_lower_L": float(za_low * nk / nz),
            "ZA_fill_fraction_if_KN_full_same_unit": float((kn / nk) * nz / za),
            "ZA_fill_fraction_upper_at_ZA_lower": float((kn / nk) * nz / za_low),
        })

print(json.dumps({
    "status": "conditional deterministic calculation; no confidence intervals or new measurement",
    "ZA_source_tolerance_L": [float(za_low), float(za_high)],
    "rows": rows,
    "post_hoc_geometry": {
        "height_m": 0.53,
        "premises": "Approximately axisymmetric vessel; all horizontal outer diameters <= reported 53 cm height; published profile preserves shape",
        "outer_enclosing_cylinder_L": math.pi * (0.53 / 2) ** 2 * 0.53 * 1000,
        "warning": "Conditional upper bound, not measured internal capacity and not an independent second ancient observation",
    },
}, indent=2))
