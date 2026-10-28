"""Conditional arithmetic sanity check; no inference of ancient unit or meaning."""
import json
high_unit_g = 31200
expected_ninth_g = high_unit_g / 9
result = {
    "source": "Montecchi2024 pp184-185, reported values; no fresh measurement",
    "assumed_high_unit_g": high_unit_g,
    "ninth_g": expected_ninth_g,
    "reported_mass_comparisons": [
        {"mass_g": m, "difference_from_ninth_g": m-expected_ninth_g,
         "relative_difference_percent": 100*(m/expected_ninth_g-1)}
        for m in (3450,3511)
    ],
    "eleven_high_units_g": 11*high_unit_g,
    "scope": "Fit to a selected ninth is not semantic validation. Eleven literal high units on one stone is a restricted model, not the author's group-of-weights proposal."
}
print(json.dumps(result,indent=2))
