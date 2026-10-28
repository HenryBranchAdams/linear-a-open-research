#!/usr/bin/env python3
"""Offline reproduction and source-preserving ledger export. Python 3.10+.

Acquisition is intentionally separate. Branch JSON files contain manually
audited evidence, not data inferred from proposed English translations.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))

def write(path, obj):
    p = ROOT / path
    p.parent.mkdir(exist_ok=True, parents=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

for script in ['notes/identity_analysis.py', 'analysis/linear_b_check.py',
               'analysis/roundel_count_test.py', 'analysis/anetaki_textile_test.py']:
    subprocess.run([sys.executable, str(ROOT / script)], check=True, stdout=subprocess.DEVNULL)

sources, observations, claims, experiments = [], [], [], []
for branch in ['za9', 'linear_b', 'jar', 'identity', 'anetaki', 'roundels']:
    path = f'notes/{branch}.json'
    data = read(path)
    raw_sources = data.get('sources', [])
    if isinstance(raw_sources, dict):
        raw_sources = [dict(id=k, **v) for k, v in raw_sources.items()]
    for i, s in enumerate(raw_sources):
        sid = s.get('id', s.get('source_id', f'{branch}_source_{i+1}'))
        sources.append({'registry_id': f'{branch}:{sid}', 'source_id': sid,
                        'branch': branch, 'provenance_file': path,
                        'retrieved': s.get('retrieved', s.get('retrieval_date', data.get('retrieval_date', data.get('research_date', data.get('date', data.get('retrieved')))))),
                        'metadata': s})

    raw_obs = data.get('observations', [])
    if branch == 'identity':
        raw_obs = []
        for d in data['documents']:
            for row in d['rows']:
                raw_obs.append(dict(row, canonical_object_id=d['id'], aliases=[d.get('inventory')],
                                    source_id='YOUNGER_' + d['id'], context=d.get('genre'),
                                    published_scribe=d.get('scribe'), bibliographic_locator=d.get('gorila')))
    for i, o in enumerate(raw_obs):
        oid = o.get('id', o.get('row_id', f'observation_{i+1}'))
        obj = o.get('canonical_object_id', o.get('object_id', o.get('object', o.get('document', o.get('inscription')))))
        line = o.get('line', o.get('face_line', o.get('location')))
        if obj == 'KN V(4)831.4':
            obj, line = 'KN V(4)831', '.4'
        form = o.get('diplomatic_transcription', o.get('diplomatic', o.get('diplomatic_label', o.get('reading', o.get('reading_minimum')))))
        refs = o.get('sources', o.get('source_ids', o.get('source_id', o.get('source'))))
        if isinstance(refs, str): refs = [refs]
        observations.append({
            'evidence_id': f'{branch}:{oid}', 'branch': branch, 'canonical_object_id': obj,
            'object_matching_key': re.sub(r'\s+', '', obj) if isinstance(obj, str) else None,
            'aliases': o.get('aliases', [o['alias']] if o.get('alias') else []),
            'face': o.get('face'), 'line': line,
            'observation_text': o.get('observation'),
            'evidence_kind': o.get('kind', o.get('feature', o.get('type'))),
            'qualifications': o.get('qualifications', o.get('qualification')),
            'limitation': o.get('limitation', o.get('limitations')),
            'diplomatic_transcription': form,
            'normalized_search_form': o.get('normalized_search_form', o.get('normalized_target', o.get('normalized_search', o.get('normalized')))),
            'sign_uncertainty': o.get('sign_uncertainty', o.get('sign_level_uncertainty', o.get('target_sign_uncertainty', o.get('uncertainty', o.get('sign_or_boundary_uncertain', o.get('reading_qualifications')))))),
            'uncertainty_scope': 'target only' if 'target_sign_uncertainty' in o else 'see original record for scope',
            'other_uncertainty': o.get('other_uncertainty'),
            'target_complete': o.get('target_complete'),
            'missing_boundaries': o.get('missing_boundaries', o.get('word_boundaries', o.get('boundary_status', {'left':o.get('left_boundary', o.get('left_word_boundary')), 'right':o.get('right_boundary', o.get('right_word_boundary'))}))),
            'cross_face_continuation': o.get('cross_face_continuation'),
            'context': o.get('context', o.get('context_observed')),
            'bibliographic_locator': o.get('bibliographic_locator', o.get('locator', o.get('pages'))),
            'source_refs': refs,
            'proposed_analysis_separate': o.get('proposed_roles_separate'),
            'provenance_file': path,
            'original_record': o,
        })
    for i, c in enumerate(data.get('claims', data.get('claim_ledger', []))):
        claims.append({'ledger_id': f'{branch}:{c.get("id", i+1)}', 'provenance_file': path, **c})
    for i, e in enumerate(data.get('experiments', [])):
        experiments.append({'ledger_id': f'{branch}:{e.get("id", i+1)}', 'provenance_file': path, **e})
    if 'numeric_experiment' in data:
        experiments.append({'ledger_id': branch + ':numeric', 'provenance_file': path, **data['numeric_experiment']})

sources.extend(read('data/additional_sources.json'))
write('data/sources.json', sources)
write('data/observations.json', {'schema': 'round9-evidence-1',
      'conventions': 'Null means unestablished/not recorded, not absent. Original records preserve qualifications not expressible in common fields. Rows include alternative views and controls, not independent ancient witnesses.',
      'observations': observations})
write('data/claim_ledger.json', {'central_claims': read('data/central_claims.json'), 'branch_claims': claims})
write('data/experiment_ledger.json', {'cycles': read('data/research_cycles.json'), 'branch_experiments': experiments})

identity = read('notes/identity_results.json')
textile = read('results/anetaki_textile_test.json')
discovery = identity.get('sigla_discovery', {})
summary = {
    'iteration': 9,
    'inherited_analysis_reproduced': read('data/input_provenance.json')['round8_reproduced'],
    'original_sentence_goal_achieved': False,
    'new_Linear_A_action_identified': False,
    'same_referent_established_for_TA_NA_family': False,
    'ZA9_final_sign_independently_resolved': False,
    'ZA9_reading_status': read('notes/za9.json')['verdict'],
    'cross_site_face_overlap': identity['main_face_comparisons'],
    'whole_tablet_overlap': identity['whole_tablet_sensitivity'],
    'sigla_document_faces': discovery.get('document_faces_total'),
    'sigla_fetch_errors': discovery.get('fetch_errors'),
    'sigla_sequence_occurrences': discovery.get('indexed_sequence_occurrences'),
    'sigla_literal_A_TA_NA_TI_hits': discovery.get('literal_A_TA_NA_TI_hits'),
    'textile_lower_bound': textile['preserved_recto_numeric_lower_bound'],
    'textile_conditional_target': textile['conditional_common_batch_mass'],
    'textile_doubled_ME_sensitive_to_tentative_sign': textile['doubled_ME_sensitive_to_tentative_sign'],
    'evidence_rows_including_alternative_views': len(observations),
    'source_registry_rows_not_independent_sources': len(sources),
}
assert len({o['evidence_id'] for o in observations}) == len(observations)
assert not summary['original_sentence_goal_achieved']
assert read('notes/za9.json')['verdict'].startswith('unresolved')
write('results/summary.json', summary)
print(json.dumps(summary, ensure_ascii=False, indent=2))
