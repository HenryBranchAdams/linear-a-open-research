#!/usr/bin/env python3
"""Reproduce iteration010 offline and verify portable evidence references.

This verifies files and computations, never a decipherment.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import hashlib
import io
import json
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
IT = ROOT / 'iterations/010'
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

checks = []
for item in json.loads((ROOT / 'registry/archives.json').read_text()):
    assert digest(ROOT / item['path']) == item['sha256'], item['path']
checks.append('Original archive hashes match')
corpus = json.loads((ROOT / 'corpus/sigla_sequences_2026-09-07.json').read_text())
assert len(corpus['documents']) == 802
assert sum(len(d['sequences']) for d in corpus['documents']) == 1401
assert len({d['document_face'] for d in corpus['documents']}) == 802
checks.append('802 unique indexed faces and 1401 chunks retained')

claims = json.loads((ROOT / 'registry/claims.json').read_text())['claims']
assert len(claims) == len({c['id'] for c in claims}) == 44
historical = json.loads((ROOT / 'registry/historical_claims.json').read_text())['claims']
refs = [p for c in historical for p in c['provenance']]
for ref in refs:
    parts = ref.split('!/')
    blob = (ROOT / parts[0]).read_bytes()
    for part in parts[1:]:
        with zipfile.ZipFile(io.BytesIO(blob)) as z:
            blob = z.read(part)
checks.append(f'{len(refs)} historical archive evidence references resolve')
sources = {s['id'] for s in json.loads((ROOT / 'registry/sources.json').read_text())}
candidates = json.loads((IT / 'data/candidates.json').read_text())
assert len(candidates) == 7 and len({c['id'] for c in candidates}) == 7
for c in candidates:
    assert set(c['sources']) <= sources
    assert (IT / c['detail']).is_file()
checks.append('44 unique claims and 7 source-linked candidate dossiers')

tracked = [IT / 'results/corpus_pairs.json', IT / 'results/packet_models.json',
           IT / 'notes/ht24_fallback/identifiability_results.json', IT / 'ATLAS.html']
before = {str(p.relative_to(ROOT)): digest(p) for p in tracked}
for script in ['code/corpus_pairs.py', 'code/packet_models.py',
               'notes/ht24_fallback/identifiability.py', 'code/build_atlas.py']:
    subprocess.run([sys.executable, str(IT / script)], check=True, stdout=subprocess.DEVNULL)
after = {str(p.relative_to(ROOT)): digest(p) for p in tracked}
assert before == after, 'Fresh reproduction changed a frozen output'
checks.append('Corpus, packet, HT24 and atlas outputs reproduce byte-for-byte')

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'a' and 'href' in a:
            self.links.append(a['href'])
parser = Links(); parser.feed((IT / 'ATLAS.html').read_text())
for ref in parser.links:
    u = urlparse(ref)
    if u.scheme or not u.path:
        continue
    assert (IT / unquote(u.path)).resolve().is_file(), ref
checks.append('Atlas local links resolve in the extracted workspace')
result = {'status': 'passed', 'checks': checks, 'output_hashes': after,
          'limits': 'No network required. Does not rerun historical iterations, certify readings, or establish translation.'}
(IT / 'results/verification.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
