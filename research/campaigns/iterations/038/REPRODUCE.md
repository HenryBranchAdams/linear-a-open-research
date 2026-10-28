# Reproduce campaign038 at its actual scope

The scientific comparison is qualitative. Read `evidence/EVIDENCE_RECORD.json`, the critical overlay, `analysis/RIVAL_COMPARISON.md`, and the independent review. No statistical program, model fit, random seed or held-out linguistic test was performed.

## Source replication

1. Open the exact original source URLs in REPORT.md/source registry. Read Andreadaki-Vlasaki and Hallager2007 pp13–15; inspect actual fig5, not a text screenshot placeholder. Figure7 is an auxiliary, partly cropped image in the acquisition record.
2. Compare the whole-group erasure notation, residual pair and first-mark proposal with DelFreo p100 and committee p586. Keep editorial grouping separate from an ancient divider.
3. Attempt to identify a diagnostic erasure/stamping intersection in the acquired plate. This team could not; reproduce that limit or document a new concrete observation. Do not recast the editors' timing assessment as the team's new observation.
4. Hold the physical observations fixed while assigning the designation to responsibility, a distinct counterparty, an account/category, or an earlier entry. Identify any acquired observation that changes under those assignments. The completed comparison found none.
5. Assess the conditional I<S<T physical exclusion separately from reference, motive and linguistic action.

This replication uses exposed evidence. It is not unused-outcome validation. A genuinely new observation requires an exposure record and, where appropriate, a dated protocol before inspection.

## Offline preservation check

Run from the extracted `Linear_A_Campaign_038` directory with Python3 and its standard library. The embedded exact baseline archive supplies the immutable corpus and inherited registries; no network or third-party dependency is required.

```python
from pathlib import Path
import hashlib, json, zipfile

root = Path('.')
with zipfile.ZipFile(root / 'history/Linear_A_Research_Baseline_2026-10-18.zip') as z:
    base = 'Linear_A_Baseline_2026-10-18/'
    blob = z.read(base + 'corpus/discovery_snapshot.json')
    old_claims = json.loads(z.read(base + 'registry/claims.json'))['claims']
    old_experiments = json.loads(z.read(base + 'registry/experiments.json'))
    old_sources = json.loads(z.read(base + 'registry/sources.json'))

index = json.loads(blob)
p = root / 'iterations/038'
raw = json.loads((p / 'evidence/raw_index_record.json').read_text())
overlay = json.loads((p / 'evidence/KHWc2123_critical_overlay.json').read_text())
claims = json.loads((root / 'registry/claims.json').read_text())['claims']
experiments = json.loads((root / 'registry/experiments.json').read_text())
sources = json.loads((root / 'registry/sources.json').read_text())

assert hashlib.sha256(blob).hexdigest() == '9b293509ab0ff928564c924e41f2c7da97e024ff28ac9b196e25cec638a2629b'
assert raw['record'] == overlay['raw_index_value'] == index['KHWc2123']
assert hashlib.sha256((p / 'evidence/KHWc2123_critical_overlay.json').read_bytes()).hexdigest() == '7cdab8ba2cc26ac18cf026a1ebc6cf3d50a8c0478aa790625d9e6b465fc34533'
assert claims[:80] == old_claims
assert experiments[:28] == old_experiments
assert sources[:92] == old_sources
assert (len(claims), len(experiments), len(sources)) == (82, 30, 100)
assert all(overlay['semantics'][k] is None for k in ('selected_referent', 'selected_role', 'selected_action'))
print('Preservation and representation checks passed; no semantic inference is tested.')
```

The lead executed these substantive comparisons and additional baseline-file equality, identifier-uniqueness and reviewed-document-hash checks. Actual output/environment is in `PRESERVATION_CHECK.json`. The challenger separately ran the raw/overlay check recorded in `agents/independent_challenger/OVERLAY_CHECK.json`.

## Capture and path scope

The archive includes authored observations, complete reasoning, acquisition/failure logs, review, critical overlays, exact raw-row extracts, current registries and the unchanged user-project baseline archive. Newly downloaded complete third-party publications, figure images, rendered pages and full tool-extracted source captures are not redistributed in this portable payload. `SOURCE_CAPTURE_MANIFEST.json` gives their exact working-tree paths, hashes, sizes and omission status; source ledgers supply URLs and inspection scope. Hashes identify acquired bytes, not proof of a reading.

Some agent logs preserve the absolute/relative workspace paths used during execution. The portable commands above resolve the same inputs from the embedded baseline. Existing historical registry paths keep their original archive scope; new C038 registry paths resolve from the campaign archive root.

`PACKAGE_MANIFEST.json` lists included files and hashes; it excludes itself to avoid a self-referential digest. A verified ZIP or matching checksum establishes preservation, never a translation.
