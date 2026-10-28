from pathlib import Path
import json,subprocess,re,hashlib
root=Path('/workspace/scratch/35b8eca9dd0b/project/Linear_A_Research_Current')
nav=json.loads((root/'registry/archive_navigation.json').read_text())
pattern=re.compile(r'KN\s*Zb\s*<?27>?|HM\s*5194|Z[AA]?\s*Zb\s*3\b|(?<!\d)5194(?!\d)|Christakis|\b34\s*(?:litres|liters|[lL]\b)',re.I)
seen=set(); records=[]
for i,r in enumerate(nav['reports']):
 if r['sha256'] in seen:continue
 seen.add(r['sha256'])
 p=subprocess.run(['python3',str(root/'tools/read_history.py'),'--read',str(i)],capture_output=True,text=True,check=True)
 lines=p.stdout.splitlines();matches=[]
 for j,line in enumerate(lines):
  if pattern.search(line):matches.append({'reader_output_line':j+1,'context':'\n'.join(lines[max(0,j-1):j+2])})
 records.append({'index':i,'archive_id':r['archive_id'],'member':r['member'],'sha256':r['sha256'],'matches':matches})
corpus=json.loads((root/'corpus/discovery_snapshot.json').read_text())
rows={k:v for k,v in corpus.items() if re.fullmatch(r'(?:KNZb<?27>?|ZAZb3)[a-z]?',k,re.I)}
result={'scope':'Text scan of unique indexed historical reports via the documented verifying reader; no full historical-source reinspection. Current prose/registries separately rg scanned. Does not include every raw acquisition or protected original initial report. Absence is no guarantee of no prior exposure.','pattern':pattern.pattern,'unique_reports_scanned':len(records),'reports_with_hits':[r for r in records if r['matches']],'all_reports_audited':records,'frozen_corpus_target_rows':rows}
out=Path('phase_work/comparative/C042_EXPOSURE_CHECK.json');out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='all_reports_audited'},ensure_ascii=False,indent=2))
