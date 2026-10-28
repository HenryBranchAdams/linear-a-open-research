#!/usr/bin/env python3
"""Exploratory HT118 arithmetic, not a semantic decoder or a confirmatory test.

Run: python explore_ht118.py [output.json]
Only explicitly written paired quantities enter the pairing experiment. Missing KI
is not treated as zero. The final break marker and unmatched main total remain.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations
from pathlib import Path
import json
import sys

@dataclass(frozen=True)
class Row:
    designation: str
    main: int
    ki: int | None

ROWS = (
    Row('MA-DI', 15, 10),
    Row('QA-QA-RU', 6, 4),
    Row('A-RI-SU', 4, 1),
    Row('RI-RU-MA', 10, None),
)

def derive() -> dict:
    paired = tuple(r for r in ROWS if r.ki is not None)
    row_results = [
        {'designation': r.designation, 'main': r.main, 'KI': r.ki,
         'sum': r.main + r.ki, 'difference': r.main - r.ki,
         'KI_over_main': str(Fraction(r.ki, r.main))}
        for r in paired
    ]
    assignments = []
    for values in permutations(tuple(r.ki for r in paired)):
        sums = [r.main + k for r, k in zip(paired, values)]
        differences = [r.main - k for r, k in zip(paired, values)]
        assignments.append({
            'KI_assignment': values, 'sums': sums, 'differences': differences,
            'sum_multiple5_count': sum(x % 5 == 0 for x in sums),
            'difference_multiple5_count': sum(x % 5 == 0 for x in differences),
            'all_differences_nonnegative': all(x >= 0 for x in differences),
        })
    sensitivity = []
    for modulus in range(2, 11):
        sensitivity.append({
            'modulus': modulus,
            'observed_sum_divisibility': sum(r['sum'] % modulus == 0 for r in row_results),
            'observed_difference_divisibility': sum(r['difference'] % modulus == 0 for r in row_results),
            'assignments_all_sums_divisible': sum(all(s % modulus == 0 for s in p['sums']) for p in assignments),
            'assignments_all_differences_divisible': sum(all(s % modulus == 0 for s in p['differences']) for p in assignments),
        })
    main_total = sum(r.main for r in ROWS)
    ki_total = sum(r.ki for r in paired)
    return {
        'status': 'Post-iteration-16 speculation; not iteration 17 or a decipherment claim',
        'source': 'https://www.inscribercproject.com/Clay_tablet_HT_118.php',
        'transliteration_crosscheck': 'https://raw.githubusercontent.com/mwenge/lineara.xyz/master/commentary/HT118.html',
        'rows': row_results,
        'scope_and_anomalies': {
            'unpaired_row': {'designation': 'RI-RU-MA', 'main': 10, 'KI': None},
            'sum_main': main_total, 'written_KU_RO': 30,
            'main_mismatch': main_total - 30,
            'sum_explicit_KI': ki_total, 'written_final_KI': '15[',
            'final_break_preserved': True,
            'same_units_and_row_scope': 'required assumption for sums/differences',
        },
        'permutation_sanity_check': {
            'assignments': assignments,
            'all_sum_multiple5_assignments': sum(p['sum_multiple5_count'] == 3 for p in assignments),
            'assignment_count': len(assignments),
            'interpretation': '1 of 6 arrangements; NOT an adjusted p-value, Bayes factor, or probability of the hypothesis',
        },
        'post_hoc_modulus_sensitivity': sensitivity,
        'limitations': [
            'Tablet, three-row subset, addition and modulus five were considered after exposure.',
            'Round planned quotas/batches are a hypothesis, not an independently demonstrated practice for these rows.',
            'KI = KI-RO is a proposed lexical bridge, not established by this calculation.',
            'The numerical relation does not identify debt, physical flow direction, counterparty or historical persons.',
            'The main-column total remains unresolved. No numeral is emended to close it.',
            'No genuinely unseen ancient witness or publication-priority check is supplied.',
        ],
    }

def main() -> None:
    if len(sys.argv) > 2:
        raise SystemExit('Usage: python explore_ht118.py [output.json]')
    result = derive()
    # Internal arithmetic checks, deliberately not called semantic verification.
    assert [r['sum'] for r in result['rows']] == [25, 10, 5]
    assert result['scope_and_anomalies']['main_mismatch'] == 5
    assert result['scope_and_anomalies']['sum_explicit_KI'] == 15
    assert result['permutation_sanity_check']['assignment_count'] == 6
    assert result['permutation_sanity_check']['all_sum_multiple5_assignments'] == 1
    destination = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).with_name('ht118_exploration_reproducible.json')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(destination)

if __name__ == '__main__':
    main()
