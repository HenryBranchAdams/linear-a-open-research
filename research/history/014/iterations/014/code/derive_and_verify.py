#!/usr/bin/env python3
from pathlib import Path
import json, collections, copy
ROOT=Path(__file__).resolve().parents[3]
corpus=json.loads((ROOT/'corpus/sigla_sequences_2026-09-07.json').read_text())
rec=json.loads((ROOT/'iterations/014/data/kiro_member_recurrences.json').read_text())
ht=json.loads((ROOT/'iterations/014/data/ht100_polarity.json').read_text())

# Exact recurrence re-derivation.
idx=collections.defaultdict(list)
for d in corpus['documents']:
    for s in d['sequences']:
        idx[s['form']].append(d['document_face'])
expected={r['form']:sorted(set(r['all_exact_documents'])) for r in rec}
for form,docs in expected.items():
    assert sorted(set(idx[form]))==docs,(form,sorted(set(idx[form])),docs)

# Key negative controls really recur outside KIRO discovery witnesses.
lookup={r['form']:r for r in rec}
for form in ['KU-*56-NU','PA-JA-RE','SA-RU','PA-TA-NE']:
    assert lookup[form]['external_document_count']>=1,form
assert lookup['KU-*56-NU']['external_document_count']>=3
assert lookup['PA-JA-RE']['external_document_count']>=3

# HT100 ambiguity is genuinely bifurcating.
sc={x['ambiguous_quantity']:x for x in ht['scenarios']}
assert sc[4]['include_matches'] and not sc[4]['exclude_matches']
assert sc[6]['exclude_matches'] and not sc[6]['include_matches']

# Failure injection: if 4/6 collapsed to one reading, ambiguity disappears; verifier detects that change.
def polarity_state(scenarios):
    incl=any(x['include_matches'] for x in scenarios)
    excl=any(x['exclude_matches'] for x in scenarios)
    return {'inclusive_possible':incl,'exclusive_possible':excl,'identified':incl ^ excl}
base=polarity_state(ht['scenarios'])
assert base=={'inclusive_possible':True,'exclusive_possible':True,'identified':False}
only4=polarity_state([sc[4]])
only6=polarity_state([sc[6]])
assert only4['identified'] and only4['inclusive_possible']
assert only6['identified'] and only6['exclusive_possible']

# Frozen source discrepancy check: HT122a contains PA-RI-NE, not exact PA-TA-NE.
ht122=next(d for d in corpus['documents'] if d['document_face']=='HT 122a')
forms=[s['form'] for s in ht122['sequences']]
assert 'PA-RI-NE' in forms and 'PA-TA-NE' not in forms

out={
 'corpus_documents':len(corpus['documents']),
 'exact_KIRO_faces':sum(1 for d in corpus['documents'] if 'KI-RO' in [s['form'] for s in d['sequences']]),
 'key_external_recurrence_counts':{f:lookup[f]['external_document_count'] for f in ['KU-*56-NU','PA-JA-RE','SA-RU','PA-TA-NE']},
 'ht100_polarity_state':base,
 'ht100_if_4':only4,
 'ht100_if_6':only6,
 'ht122_frozen_reading':'PA-RI-NE',
 'full_level4_breakthrough':False,
 'verification_scope':'Computation/source-state checks only; semantic synthesis remains interpretive.'
}
(ROOT/'iterations/014/results/verification.json').write_text(json.dumps(out,indent=2)+'\n')
print('Iteration 14 verification passed.')
print(json.dumps(out,indent=2))
