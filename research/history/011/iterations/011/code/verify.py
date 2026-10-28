#!/usr/bin/env python3
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[3]
ev = json.loads((ROOT/'iterations/011/results/category_compatibility.json').read_text())
claims = json.loads((ROOT/'registry/claims_delta.json').read_text())
assert ev['classes']['grain_specific_commodity']['O2'] == 'fails'
assert ev['decision']['project_label'] == 'entity/account/designation'
assert len(claims) == 4
assert any(c['id']=='LA-011-004' and c['disposition']=='not_achieved' for c in claims)
for rel in ['START_HERE.md','context/CURRENT_STATE.md','iterations/011/REPORT.md','iterations/011/notes/SARU_DOSSIER.md','iterations/011/notes/HT117_HT87.md','registry/sources_011.json']:
    assert (ROOT/rel).exists(), rel
print('Iteration 11 verification passed.')
print('Category constraint advanced; full action-and-role mission remains open.')
