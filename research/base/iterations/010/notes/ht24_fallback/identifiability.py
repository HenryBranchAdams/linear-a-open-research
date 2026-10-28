#!/usr/bin/env python3
"""HT24 identifiability conditions, extending (not repeating) round 9.

Numerical inputs are inherited from round9/notes/anetaki.json. This script
does not claim any yield, token denomination, or unpreserved amount is observed.
Only standard-library exact arithmetic is used. Run from any directory.
"""
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
B, R, C, N = F(63, 2), F(9, 2), F(10), F(45)
SCENARIOS = [('secure_ME_only', F(10)), ('accept_ME_by_six', F(16))]


def lower_bound(m, s):
    return B + (m - 1) * s


def compatible_witness(m, s):
    """Construct y in (0,1], x>0 satisfying y*(L+x)=C*R.

    x is an algebraic weighted missing amount. Positivity does not establish an
    epigraphically admissible restoration or archaeological likelihood.
    """
    low = lower_bound(m, s)
    missing = max(F(), C * R - low) + 1
    y = C * R / (low + missing)
    assert missing > 0 and 0 < y <= 1
    assert y * (low + missing) == C * R
    return {'m': str(m), 'weighted_missing': str(missing), 'yield': str(y),
            'physical_input': str(low + missing), 'output': str(C * R)}


out = {
    'experiment_id': 'R10-HT24-IDENTIFIABILITY',
    'kind': 'exact conditional identifiability analysis',
    'new_ancient_reading': False,
    'formula': 'c*R = y*(B + (m-1)*S + x)',
    'symbols': {'B': '63/2 inherited visible quantity lower bound',
                'R': '9/2 reverse total, conditional on fraction values and AB118?',
                'c': 'standard wool units per reverse accounting unit',
                'm': 'hypothetical ME multiplier',
                'S': 'accepted ME-marked visible subtotal',
                'x': 'unpreserved weighted input, nonnegative',
                'y': 'yield, 0<y<=1 under no additions'},
    'constructive_nonidentifiability': {},
    'bounded_yield_multiplier_ceilings': {},
    'input_token_link': {},
    'interpretation': [
        'Even a secure ME-by-six reading cannot bound m if yield can approach zero and missing input has no upper bound.',
        'Fixing yield alone is also insufficient if c can vary freely.',
        'An independently established same-batch input token count with known denomination bounds m without downstream yield.',
        'The report supplies the proof for all m>0; example countermodels below are illustrative, not ancient reconstructions.',
        'Numerical feasibility is a necessary screen, not sufficient evidence for a reading, restoration, or role assignment.'
    ]
}
for label, s in SCENARIOS:
    out['constructive_nonidentifiability'][label] = [
        compatible_witness(m, s) for m in [F(1,2), F(1), F(2), F(3), F(10)]
    ]
    out['bounded_yield_multiplier_ceilings'][label] = [
        {'yield_minimum': str(ymin),
         'm_ceiling': str(1 + (C * R / ymin - B) / s),
         'doubled_m_rejected_by_lower_bound': lower_bound(F(2), s) > C * R / ymin}
        for ymin in [F(1), F(99,100), F(19,20), F(18,19), F(9,10), F(1,2)]
    ]
    out['input_token_link'][label] = {
        'assumptions': '45 tokens independently tied to the recto input batch, each representing one standard wool unit, and count complete',
        'm_ceiling': str(1 + (N - B) / s),
        'yield_required': False,
        'doubled_m_rejected_by_lower_bound': lower_bound(F(2), s) > N,
        'unknown_token_denomination_removes_this_bound': True,
    }

(HERE / 'identifiability_results.json').write_text(
    json.dumps(out, indent=2, ensure_ascii=False) + '\n'
)
print(json.dumps(out, indent=2, ensure_ascii=False))
