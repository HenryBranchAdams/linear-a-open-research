#!/usr/bin/env python3
"""Offline conditional HT24 tests; no lexical or grammatical translation inferred.

Run from any directory. Reads source-qualified data, uses exact rationals,
and writes deterministic results beside the delivered evidence.
"""
import json
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'notes/anetaki.json').read_text())
p = data['numeric_experiment']
base = sum(map(F, p['preserved_numeric_lower_bounds']), F())
j, e, ratio = F(p['J']), F(p['E']), F(p['wool_per_AB118'])
verso = sum(F(a['integer']) + a['J_count'] * j + a['E_count'] * e for a in p['verso_entries'])
target = verso * ratio
scenarios = []
for s in p['ME_scenarios']:
    me_units = F(s['secure_or_accepted_ME_subtotal'])
    other = base - me_units
    # This is a necessary condition only: missing quantities consume residual mass.
    scenarios.append({
        'scenario': s['id'],
        'ME_bound': str((target - other) / me_units),
        'condition': 'ME multiplier must be <= bound only under lossless common-batch equivalence and nonnegative remaining mass',
        'candidate_multipliers': [
            {'m': str(m), 'preserved_lower_bound': str(other + me_units*m),
             'remaining_mass': str(target - other - me_units*m),
             'negative_residual_rejects': target - other - me_units*m < 0}
            for m in (F(1,2), F(1), F(2))
        ]
    })

receipt_quantities = [F(p['fractional_recto_entry'])] + [
    ratio * (F(a['integer']) + a['J_count']*j + a['E_count']*e) for a in p['verso_entries']
]
accepted_me_doubled_min = F(scenarios[1]['candidate_multipliers'][-1]['preserved_lower_bound'])
max_yield = target / accepted_me_doubled_min
result = {
    'experiment_id': 'ANETAKI-TEXTILE-1',
    'status': 'conditional arithmetic constraints, not decipherment',
    'preserved_recto_numeric_lower_bound': str(base),
    'conditional_verso_total': str(verso),
    'conditional_common_batch_mass': str(target),
    'all_unpreserved_mass_if_ME_multiplier_one': str(target-base),
    'preserved_mean': str(base/4),
    'six_entry_naive_mean_imputation': str((base/4)*6),
    'ME_scenarios': scenarios,
    'lossless_balance_required_for_negative_residual_rejection': True,
    'yield_sensitivity': {
        'model': 'Output = yield * (input lower bound + missing input); no additions or conversion differences',
        'ME_multiplier': '2',
        'reading': 'accept tentative ME beside6',
        'input_lower_bound': str(accepted_me_doubled_min),
        'output_assumed': str(target),
        'maximum_yield_at_lower_bound': str(max_yield),
        'minimum_loss_fraction_at_lower_bound': str(1-max_yield),
        'minimum_loss_percent_at_lower_bound': float(100*(1-max_yield)),
        'qualification': 'No observed yield. Positive missing input requires more loss. This alternative relaxes one-standard-input-unit per nodulus if45noduli are retained as an output-related total.'
    },
    'one_unit_nodulus_allocation': [
        {'quantity':str(q),'whole_unit_allocation_possible':q.denominator==1} for q in receipt_quantities
    ],
    'doubled_ME_sensitive_to_tentative_sign':
        scenarios[0]['candidate_multipliers'][-1]['negative_residual_rejects'] !=
        scenarios[1]['candidate_multipliers'][-1]['negative_residual_rejects'],
    'interpretation': 'An unqualified exclusion of a distinct ME unit does not follow. The doubled-unit rejection changes with tentativeME and depends on lossless equivalence. If input-output processing is allowed, a yield at most18/19 at the surviving lower bound removes that contradiction. No actual yield or translation is inferred. Existing fractional-token objection is reproduced, not new.',
}
assert base == F(63,2)
assert verso == F(9,2)
assert target == 45
assert result['doubled_ME_sensitive_to_tentative_sign']
assert max_yield == F(18,19)
assert result['one_unit_nodulus_allocation'][0]['whole_unit_allocation_possible'] is False
out = ROOT / 'results/anetaki_textile_test.json'
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
print(json.dumps(result, indent=2, ensure_ascii=False))
