"""Verify the public research projection and its declared reproducible outputs.

This deliberately does not claim the complete snapshot's nested-archive checks,
source autopsies, assays, material identification or ancient semantic validation.
"""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / 'research/campaigns'
manifest = json.loads((RESEARCH / 'PUBLISHED_FILES.json').read_text())
assert manifest['research_through'] == '044'
expected = {entry['path'] for entry in manifest['files']}
actual = {p.relative_to(RESEARCH).as_posix() for p in RESEARCH.rglob('*') if p.is_file()}
assert actual == expected | {'PUBLISHED_FILES.json', 'PUBLIC_RELEASE.md'}, 'Unexpected public projection membership'
for entry in manifest['files']:
    data = (RESEARCH / entry['path']).read_bytes()
    assert len(data) == entry['size_bytes'], entry['path']
    assert hashlib.sha256(data).hexdigest() == entry['sha256'], entry['path']
    assert not re.search(rb'libfile_|oai-library://|library_file_id', data), entry['path']

# Every relative link in the newly authored current packet must resolve in the
# release. Original archival documents keep their historical relative links.
for filename in ['CURRENT_STATE.md', 'START_HERE.md', 'research/current/CURRENT_RESEARCH_BASELINE.md',
                 'research/current/CURRENT_RESEARCH_BRIEF.md', 'research/current/SOURCE_GUIDE.md']:
    file = ROOT / filename
    for target in re.findall(r'\]\(([^)]+)\)', file.read_text()):
        if re.match(r'[a-z]+:|#|/', target):
            continue
        assert (file.parent / target.split('#')[0]).exists(), (filename, target)

def run_json(script):
    result = subprocess.run([sys.executable, str(script)], check=True, capture_output=True, text=True)
    return json.loads(result.stdout)

assert run_json(RESEARCH / 'iterations/043/analysis/check_join.py') == json.loads(
    (RESEARCH / 'iterations/043/analysis/result.json').read_text()), 'C043 eligibility output changed'
assert run_json(RESEARCH / 'iterations/044/analysis/extract_target.py') == json.loads(
    (RESEARCH / 'iterations/044/analysis/target_index_result.json').read_text()), 'C044 index output changed'

# C042 writes outputs; run it in an isolated copy so published evidence bytes
# and their manifest remain untouched even if its implementation changes.
analysis = RESEARCH / 'iterations/042/analysis'
with tempfile.TemporaryDirectory(prefix='linear-a-c042-') as temporary:
    copied = Path(temporary) / 'analysis'
    shutil.copytree(analysis, copied)
    subprocess.run([sys.executable, str(copied / 'capacity_comparison.py')], check=True, capture_output=True, text=True)
    for name in ['capacity_results.json', 'capacity_results.csv']:
        assert (copied / name).read_bytes() == (analysis / name).read_bytes(), 'C042 output changed: ' + name

print(json.dumps({'status': 'passed', 'research_through': '044',
                  'published_files_checked': len(expected), 'relative_links': 'passed',
                  'reproduced': ['C042 capacity JSON/CSV (nine reading branches)', 'C043 eligibility JSON', 'C044 literal-index JSON'],
                  'scope': 'Integrity and reproducible outputs; no ancient-meaning validation.'}, indent=2))
