#!/usr/bin/env python3
"""Exact retrospective diagnostic; quantities never infer action or identity."""
from fractions import Fraction
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parents[1]
source = HERE / 'data/packet_quantities.json'
data = json.loads(source.read_text())
facts = data['facts']
tables = {k: {r['label']: Fraction(r['quantity']) for r in v['rows']} for k, v in facts.items()}
left, right = tables['HT86a'], tables['HT95b']
shared = sorted(left.keys() & right.keys())
ratios = {k: left[k] / right[k] for k in shared}
values = set(ratios.values())
k = next(iter(values)) if len(values) == 1 else None
ql, qr = data['hypothetical_pair']['left'], data['hypothetical_pair']['right']
control = {n: tables['HT95a'][n] - tables['HT95b'][n] for n in sorted(tables['HT95a'].keys() & tables['HT95b'].keys())}
out = {
    'experiment_id': data['experiment_id'],
    'input_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'shared_exact_labels': shared,
    'exact_ratios_HT86a_over_HT95b': {w: str(v) for w, v in ratios.items()},
    'common_ratio_on_exact_labels': str(k) if k is not None else None,
    'retrospective_leave_one_exact_label_out': [
        {'excluded_label': w, 'training_ratios': sorted(set(str(ratios[v]) for v in shared if v != w)),
         'observed_ratio': str(ratios[w]), 'status': 'internal consistency only; repeated 20/10 is not independent predictive evidence'}
        for w in shared
    ],
    'extend_mapping_to_published_Q_pair': {
        'left_form': ql, 'right_form': qr,
        'observed_left_quantity': str(left[ql]), 'observed_right_quantity': str(right[qr]),
        'observed_ratio': str(left[ql] / right[qr]),
        'predicted_left_if_same_mapping_and_common_ratio': str(k * right[qr]) if k is not None else None,
        'residual_observed_minus_predicted': str(left[ql] - k * right[qr]) if k is not None else None,
        'universal_scale_model_fits': k is not None and left[ql] == k * right[qr],
        'interpretation': 'Reject only the conjunction of mapped Q identity plus one constant conversion of equivalent quantities; not the linguistic relationship.'
    },
    'section_1_sensitivity': {
        'independent_exact_labels': ['KU-NI-SU', 'SA-RU', 'DI-DE-RU'],
        'ratios': {w: str(ratios[w]) for w in ['KU-NI-SU', 'SA-RU', 'DI-DE-RU']},
        'Q_pair_ratio': str(left[ql] / right[qr]),
        'universal_scale_model_fits': all(ratios[w] == left[ql] / right[qr] for w in ['KU-NI-SU', 'SA-RU', 'DI-DE-RU']),
        'interpretation': 'Mismatch survives within HT86a section1 alone, avoiding its section2 grain composite. HT95b units and common event still unestablished.'
    },
    'inherited_HT95_faces_control': {
        'differences_a_minus_b': {w: str(v) for w, v in control.items()},
        'both_positive_and_negative': any(v > 0 for v in control.values()) and any(v < 0 for v in control.values()),
        'new_project_finding': False
    },
    'numeral_sums_not_written_or_commensurable_totals': {name: str(sum(t.values())) for name, t in tables.items()},
    'mission': 'Neither quantities nor repeated labels identify an action expression or direction of transfer.'
}
(HERE / 'results/packet_models.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
