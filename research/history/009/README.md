# Linear A — iteration 9

Start with [RETURN_TO_CHATGPT.md](RETURN_TO_CHATGPT.md), then [REPORT.md](REPORT.md). The sentence goal is unmet; the package contains new source audits and executed constraints, not a claimed decipherment.

## Offline reproduction

Requirements: **Python 3.10 or newer; standard library only**. No installation, API key, fonts, browser, external repository, or network is needed.

From the extracted `linear_a_round9/` directory:

```sh
python3 analysis/run.py
python3 -m unittest discover -s tests -v
python3 analysis/verify_bundle.py
```

The first command reruns the contextual identity comparison, frozen Linear B checks, roundel proportionality test, and exact textile calculations, then regenerates the common evidence/source/claim/experiment ledgers and summary. The tests check source-reference integrity and preservation of decisive uncertainty. The verifier checks SHA-256 hashes, sizes, and file coverage against `MANIFEST.json`. All these operations are local. They verify data handling, numerical results, and package consistency; they do not certify readings or translations.

To recreate the archive and repeat clean-extraction verification:

```sh
python3 analysis/package.py
```

This creates `../linear_a_round9.zip` and a checksum sidecar. It extracts the archive into a fresh temporary directory, verifies the manifest, reruns analyses and tests, and verifies that all packaged bytes still match. It writes `results/package_verification.json`, rebuilds the archive, and repeats verification on that final archive.

## Files and data conventions

| Path | Contents |
|---|---|
| `REPORT.md`, `RETURN_TO_CHATGPT.md` | Full findings and concise handback |
| `notes/*.md` | Source-rich branch investigations and adversarial review |
| `notes/{za9,linear_b,jar,identity,anetaki,roundels}.json` | Frozen audited branch evidence; original schemas retained |
| `data/observations.json` | Common-schema observations, each retaining its full original record |
| `data/sources.json` | Source registry, locators, access metadata and dependencies |
| `data/claim_ledger.json` | Supported, rejected, conditional and unresolved claims |
| `data/experiment_ledger.json` | Five research cycles and branch experiments |
| `data/prediction_ledger.json` | Discriminating observations and remaining ambiguities |
| `data/sigla_sequence_inventory.json` | 802 document-face snapshot, 1,401 indexed sequences, page hashes and certainty classes |
| `data/input_provenance.json` | Handoff ZIP checksum and round 8 reproduction record |
| `analysis/`, `tests/` | Runnable calculations, integration checks and packaging |
| `results/`, `notes/identity_results.json` | Reproduced results; verification record |
| `MANIFEST.json` | Paths, sizes and SHA-256 hashes of all deliverable files except itself |

`null` means unestablished or unrecorded, not absence. A normalized search string is not a recovered complete word. Doubtful signs, missing boundaries, alternatives and joins remain in the source records. Common-schema `source_refs` resolve by `(branch, source_id)` in `data/sources.json`. The whitespace-normalized `object_matching_key` is only a matching aid; it does not resolve joins, old numbering, or identity. Aliases and the full original record remain authoritative for those questions.

The 115 exported observation rows include alternative editorial views, physical observations and controls, including 66 selected contextual rows. They are not 115 independent inscriptions. Likewise 802 SigLA pages are document faces, and 1,401 indexed sequences include fragments and face segments. The snapshot excludes most ritual texts and the modern four-sign THE Zb 6. Source-registry rows are not independent readings.

## Acquisition is separate

Offline results use frozen inputs. Original publication scans and full downloaded HTML are intentionally outside this archive. Relevant source URLs, page locators, retrieval information, access limitations and available checksums are preserved in the branch JSON and notes; online sources may change or become inaccessible.

Optional SigLA reacquisition uses the bundled standard-library script:

```sh
python3 notes/acquire_sigla_words.py /path/to/sigla_browse.html /path/to/new_cache /path/to/new_inventory.json
```

Save the live SigLA browse page first, then pass its local path. The script extracts all document-face links from that page and fetches their sequence views with six workers. It preserves page hashes and sequence certainty classes. It does not resolve damaged boundaries or certify complete words. A fresh network run will have a new acquisition timestamp and may reflect a changed corpus; it is not expected to reproduce the frozen snapshot byte for byte. Do not overwrite the frozen data if you want manifest verification to keep passing.

The selected contextual audit uses published transcriptions and explicit exclusions, not inferred `sender` or `recipient` fields from an explorer. No new test is described as blind: prior examples and predictions were already visible. No meaningful untouched semantic holdout was available; the work uses source checks, counterexamples and sensitivity analyses.

## Attribution and rights

The derived SigLA snapshot is attributed to **Ester Salgarella and Simon Castellan**, [SigLA](https://sigla.phis.me/), and is distributed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), as recorded in the data. It retains that license; the surrounding archive does not remove its terms. Ancient inscriptions, modern readings and hypotheses are credited individually. This package contains no source-publication PDFs, facsimile images, photographs or font files. Publication priority is not claimed for the new calculations.
