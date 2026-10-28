#!/usr/bin/env python3
"""Offline context comparison, using only selected source-audited facts.

Run from any directory. The optional SigLA inventory adds a discovery audit.
"""
import json, re
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
e=json.loads((HERE/'identity.json').read_text())
docs={d['id']:d for d in e['documents']}
targets={'TA-NA-TI','TA-NA-TE','A-TA-NA-TE'}

def labels(doc, face=None, strict=True):
    out=set()
    for r in docs[doc]['rows']:
        s=r['normalized_search']
        if face and not r['line'].startswith(face+'.'): continue
        if len(s.split('-'))<2 or '+' in s: continue
        if strict and r['sign_or_boundary_uncertain']: continue
        if s in targets: continue
        out.add(s)
    return out

ti_faces=[('HT7','a'),('HT10','b'),('HT98','a')]
te_context=labels('ZA10','a')
face_results=[]
tablet_results=[]
for d,f in ti_faces:
    face_results.append({'ti_face':d+f,'te_face':'ZA10a','exact_shared_non_target_labels':sorted(labels(d,f)&te_context)})
    tablet_results.append({'ti_tablet':d,'te_tablet':'ZA10','exact_shared_non_target_labels':sorted(labels(d)&labels('ZA10'))})

target_rows=[dict(object_id=d['id'],site=d['site'],**r) for d in e['documents'] for r in d['rows'] if r['normalized_search'] in targets]
same_site_shared=sorted(labels('HT7','a')&labels('HT10','b'))
result={
 'method':'Retrospective exact shared non-target multi-sign label comparison. No fuzzy matching, p-value, or identity inference. Facts derived from selected complete contextual transcriptions. Damage-sensitive normalization separate.',
 'main_face_comparisons':face_results,
 'whole_tablet_sensitivity':tablet_results,
 'damaged_HT49_sensitivity':{'strict':sorted(labels('HT49','a')&te_context),'allow_doubtful_and_fragmentary':sorted(labels('HT49','a',False)&labels('ZA10','a',False))},
 'shared_non_target_labels_HT7a_HT10b':same_site_shared,
 'target_rows':target_rows,
 'conclusion':'In these audited witnesses, no exact co-label bridges the TA-NA-TI faces to ZA10a. SA-MA bridges HT10 and ZA10 only when opposite faces are aggregated. DA-RE bridges HT7a and HT10b, but has no identity certificate and no independently translated role.',
 'limits':['Co-occurrence identifies neither the same historical individual nor a role.','Zero overlap in sparse accounts is not a refutation of related forms.','Unknown commodities cannot be treated as identical.','The repeated spellings and contextual types do not establish an action.','HT98 fraction-only amount and HT10 fractional amount defeat a universal literal head-count interpretation, not a personal-account interpretation.']
}
inventory=ROOT/'data/sigla_sequence_inventory.json'
if inventory.exists():
    data=json.loads(inventory.read_text())
    hits=[]
    for d in data['documents']:
        for s in d.get('sequences',[]):
            if 'TA-NA' in s['form']:
                hits.append({'document_face':d['document_face'],'source':d['url'],**s})
    count_mismatches=[]
    checked=0
    for d in data['documents']:
        expected=re.search(r'/\s*(\d+) words?', d.get('metadata_text') or '')
        if expected:
            checked+=1
            if int(expected.group(1))!=len(d.get('sequences',[])):
                count_mismatches.append({'document_face':d['document_face'],'declared':int(expected.group(1)),'parsed':len(d.get('sequences',[]))})
    result['sigla_discovery']={'document_faces_total':len(data['documents']),'fetch_errors':sum(bool(d['error']) for d in data['documents']),'indexed_sequence_occurrences':sum(len(d.get('sequences',[])) for d in data['documents']),'metadata_word_count_checks':checked,'metadata_word_count_mismatches':count_mismatches,'ta_na_substring_hits':hits,'literal_A_TA_NA_TI_hits':[h for h in hits if h['form']=='A-TA-NA-TI'],'warning':'SigLA sequence chunks can be damaged or face segments. Absence is limited to this snapshot. This browse has no modern THE Zb6 pithos (Boulotis2008); its only THE IDs are THE7a/7b/8/9/10/11/12. Most ritual texts and some later editions are not covered.'}

(HERE/'identity_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
