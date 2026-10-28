#!/usr/bin/env python3
from pathlib import Path
import json, collections, csv
ROOT=Path(__file__).resolve().parents[3]
corpus=json.loads((ROOT/'corpus/sigla_sequences_2026-09-07.json').read_text())
kiro_sets={
 'HT 88':['KU-*56-*56','KA-JU','KU-*56-NU','PA-JA-RE','SA-MA-RO','DA-TA-RE'],
 'HT 94b':['TU-MA','PA-TA-NE','DE-DI','KE-KI-RU','SA-RU'],
 'HT 117a':['U-SU','MI-TU','KU-RA-MU','MA-RU','KU-*56-NU','TU-JU-MA','U-DI-MI','MI-RU-TA-RA-RE','TE-*56-RE','NA-DA-RE'],
 'HT 1':['*79-SU','DI-DI-ZA-KE','KU-*56-NU','A-RA-NA-RE']}
occ=collections.defaultdict(list)
for d in corpus['documents']:
 for i,s in enumerate(d['sequences']): occ[s['form']].append({'document_face':d['document_face'],'sequence_index':i})
rows=[]
for form in sorted(set(sum(kiro_sets.values(),[]))):
 kd=sorted([d for d,v in kiro_sets.items() if form in v]); ad=sorted(set(x['document_face'] for x in occ[form])); ext=sorted(set(ad)-set(kd))
 rows.append({'form':form,'kiro_context_documents':kd,'all_exact_documents':ad,'external_exact_documents':ext,'exact_occurrence_count':len(occ[form]),'external_document_count':len(ext)})
(ROOT/'iterations/014/data/kiro_member_recurrences.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Rebuilt',len(rows),'KI-RO member recurrence records')
