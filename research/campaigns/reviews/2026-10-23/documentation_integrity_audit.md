# Documentation integrity audit through iteration 41

Reviewed 23 October 2026. This is an independent documentation and preservation audit, not a new research iteration or independent epigraphic examination.

## Verdict

The iteration 41 archive is internally coherent and passes its published preservation verifier. The latest loose status documents and registries match that archive. The main problem is navigability across historical scopes: some generic filenames and inherited paths describe much older snapshots, while the current decision relies on the frozen October 18 baseline plus four later campaigns. A reader can follow a stale instruction without realizing that the instruction was frozen for historical preservation.

The appropriate fix is a current navigation and operating layer with explicit historical scope. Preserve the original baseline and campaign archives. Do not repair historical records by silently changing their bytes.

## Inputs examined

- Latest portable archive extracted at `work/Linear_A_Campaign_041/`.
- Current loose files materialized at `inputs/Linear A/Research Environment/`.
- Original baseline extracted at `baseline_source/Linear_A_Baseline_2026-10-18/`.
- Read-only inspection of nested campaign archives inside `history/Linear_A_Campaign_040.zip`.

All relative research references below refer to the latest portable root unless prefixed `canonical loose` or explicitly scoped to an original historical archive.

## Verification performed

The published `verify041.py` was inspected before execution. It performs read-only file, JSON, hash and representation assertions; it does not fetch sources, mutate records or run scientific analyses. Running `python3 work/Linear_A_Campaign_041/verify041.py` passed.

| Check | Result | What it establishes |
| --- | --- | --- |
| Package manifest | All 147 listed files passed byte-size and SHA-256 checks; no duplicated manifest paths; only `PACKAGE_MANIFEST.json` itself is unlisted | Integrity of the packaged authored material and history |
| Registry counts | 85 claims, 36 experiment/access/feasibility records, 113 sources | Continuity counts, not semantic progress |
| Prior registry prefixes | All 84 claims, 34 experiment/access records and 109 sources from C040 unchanged | C041 additions did not rewrite inherited records |
| Baseline and corpus vs C040 | Byte-identical | Frozen material preserved |
| Baseline vs original October 18 archive | All 12 baseline files independently compared byte-for-byte and matched | C041 retained the original baseline, not merely a modified intermediate copy |
| Current loose vs C041 | All 14 overlapping current status, context and registry files matched byte-for-byte | No split between current loose files and the latest archived current layer at audit time |
| C038–041 claim links | All five appended claims' dependency identifiers and listed evidence paths resolve | Current claim-level references are usable within the extracted latest archive |
| C038–041 experiment outputs | All output paths checked resolve | Current campaign outputs are available |
| C041 catalogue/crosswalk fields | Published assertions passed: 1121→9384, 1122→9730, 17 positive-result ACV↔AKR rows, no exact target join, no never-sampled inference | Correct preservation of the represented result, not independent revalidation of ancient evidence |
| Historical archive | Exact C040 archive hash matches the fixed value in `verify041.py` | Preserved previous archive bytes |
| History policy | Context history/changelog/do-not-reuse append-only relative to C040; protocol unchanged | Preservation of recorded corrections |

The imported C041 archive itself is 25,246,276 bytes with SHA-256 `b8e03e1d5476f1702e060aca8be20b995afd5923851649dae92738744d53598e`.

The 14 loose matches were `NEXT.md`, `START_HERE.md`, the five `context/*.md` files, and all seven `registry/*.json` files.

## Concrete documentation hazards

### 1. The canonical root verifier is still an iteration 10 verifier

**Evidence:** `canonical loose verify.py` describes itself as reproducing iteration 010, assumes `iterations/010`, expects the 802-face/1,401-chunk index, and asserts exactly 44 claims. Current `registry/claims.json` contains 85 claims. It also executes iteration 10 scripts and writes `iterations/010/results/verification.json`.

**Consequence:** Running the generic root verifier against the current environment cannot establish current integrity and would fail its claim-count assertion even with otherwise intact current documentation. This is a scope mismatch, not evidence that C041 is corrupt. The audit did not run this mutating historical verifier against current loose records.

**Fix:** Make the current entry instructions name the current read-only verification command explicitly. Label the legacy root verifier as historical, preserve its bytes in an appropriate historical snapshot, and avoid presenting it as a general current verifier. A new current dispatcher should validate the current documentation layer separately from immutable C041, then run C041's verifier only inside the untouched C041 snapshot.

### 2. The canonical root manifest is dated September 9

**Evidence:** `canonical loose MANIFEST.json` is dated `2026-09-09` and records older hashes/sizes for `START_HERE.md`, context files and registry files. For example, it lists 2,742 bytes for START_HERE, whereas the current C041 START_HERE is 2,244 bytes.

**Consequence:** A generic manifest check produces expected mismatches for legitimately evolved current files. A future agent could misdiagnose preservation damage or overwrite current files with obsolete content.

**Fix:** Publish a clearly scoped current documentation manifest or current index, and identify the September 9 manifest as an iteration 10 snapshot. Do not recalculate its hashes and continue calling it the original manifest.

### 3. Frozen baseline operating priorities are no longer the complete current queue

**Evidence:** `baseline/BASELINE.json` records research through 36–37, counts 80/28/92, and identifies Flouda 2024 as the conditional first target. `baseline/RESEARCH_QUEUE.json` has 12 historical queue records. Current `NEXT.md` instead foregrounds the exact Akrotiri inventory/catalogue-to-specimen-to-analysis/use dependency and records that the 2019 volumes were acquired in C041.

**Consequence:** Reading a file named `BASELINE` or `RESEARCH_QUEUE` without its date and later addenda can restart an obsolete access search or miss the current exact dependency. The historical files are accurately labeled, but their machine-readable priorities are not themselves a current-state index.

**Fix:** Add one dated current state/queue index that reconciles B2026-10-18 with C038–C041 and explicitly lists the older queue as historical. Keep status and evidence level separate: no active semantic experiment; current exact dependency recorded; parked branches reopen only on named evidence changes.

### 4. The current claim registry envelope still says through 040

**Evidence:** `registry/claims.json` contains 85 claim objects including `LA-041-001`, but its `authority` string says “Cumulative claims through040; B2026-10-18 andC038/C039/C040 addenda control scope.” The current status page and record contents are through 041.

**Consequence:** A machine or reader using the registry envelope alone receives a stale authority boundary.

**Fix:** Correct the current envelope to include C041 while preserving all 85 claim objects exactly. Retain the old envelope in the immutable C041 archive and record this as metadata correction, not a new scientific claim.

### 5. One frozen baseline filename is an unresolved shorthand

**Evidence:** `baseline/BASELINE.json` sets `latest_campaign_decision.reopening_brief` to `EVIDENCE_PREREQUISITES.md`. No file of that name exists at the latest root or in the baseline directory. The available relevant file is `baseline/EVIDENCE_PREREQUISITES_36_37.md`.

**Consequence:** An automated continuation using the literal field cannot resolve the intended document.

**Fix:** Record an explicit compatibility alias/crosswalk in the current documentation index. Preserve the original JSON byte-for-byte.

### 6. Historical reproduction instructions require historical archive roots

**Evidence:** `iterations/039/REPRODUCE.md` says to run `verify039.py` from the archive root, but `verify039.py` is absent from the C041 root. It belongs to the original C039 archive. Similarly, inherited `registry/archives.json` paths `archive/linear_a_codex_round9_handoff.zip` and `archive/linear_a_round9.zip` do not exist at C041 root. `registry/sources.json` includes original local paths such as `data/discovery_snapshot.json`, whereas the current packaged frozen index is `corpus/discovery_snapshot.json`.

**Consequence:** A shallow existence checker produces false missing-file alarms. A reader can also attempt to reproduce an older iteration against a newer registry and corpus layout.

**Fix:** Provide a history locator describing which archive root owns each historical path, and distinguish immediately available current evidence paths from archive-member references. Do not globally rewrite all historical paths to the latest root.

The inspected preservation chain is C041 → exact C040 → exact C039. C039 contains C038 and a baseline archive; C038 contains its baseline archive. The baseline carries earlier bundles, including 010–020 and the 036–037 chain. Earlier bytes are not missing merely because the latest tree has only one immediate history ZIP. This audit did not resolve every historical provenance reference in every nested archive.

### 7. Current prose has a few abbreviated path references

**Evidence:** `NEXT.md` mentions `agents/SOURCE_ROUTE.md` in the Akrotiri section; the actual current path is `iterations/041/agents/SOURCE_ROUTE.md`. `context/CURRENT_STATE.md` mentions `041/CONTINUATION.md` and `CATALOGUE_OVERLAY.json` without complete paths.

**Consequence:** Human context supplies the intended location, but relative-link tooling and new agents can misresolve it.

**Fix:** Use explicit clickable relative links to files from each document's own directory in the new current layer. Check those links once after editing.

### 8. Public synchronization status is historical and separately scoped

**Evidence:** `baseline/PUBLIC_SYNC.md` explicitly records an October 18 observation and no publication. It describes a portal state through iteration 16 and an intended repository whose existence was not established in that review.

**Consequence:** This is not evidence of the site's present state or a current publication checklist. It cannot substantiate a claim that the public portal already reflects C041.

**Fix:** Keep the baseline record unchanged. A current support-work index should date any new public-surface observation and state whether synchronization was actually performed. Do not fold publication status into scientific progress.

## Recommended minimum current layer

A useful current documentation set can be small:

1. A start page with an ordered reading path, current archive and verification instructions.
2. A readable current-state synthesis with retained findings, major retired claims, what C038–C041 changed, and the unresolved semantic mission.
3. A current candidate queue with exact reopening evidence and stops, linked to the original baseline dispositions and recent evidence overlays.
4. A documentation map covering current, frozen baseline, append-only history, raw corpus, correction overlays and nested historical archives.
5. A continuation template requiring candidate, independent relation, grounded rivals, differing predictions, exposure record, finite scope, independent challenger and outcome class.
6. A current manifest/check result, explicitly separate from the immutable C041 verifier.

Do not increment the scientific iteration number, append scientific claims or create a semantic experiment solely for this organizational review. Counts should remain 85/36/113 unless actual new research is separately performed.

## Scope limits

This audit establishes preservation and documentation consistency, not validity of every older scientific result. It did not obtain publication PDFs, inspect ancient-object images, independently verify source transcriptions, reproduce all historical statistical analyses, test live contributor functionality, or contact anyone. The latest archive verification and current link checks are enough to identify and fix the concrete documentation issues above; expanding testing without a specific unresolved risk is unnecessary.

## Checks for the proposed new current documentation snapshot

The new snapshot should validate itself independently of immutable C041. Recommended read-only checks are:

- Every file in its current manifest exists and matches recorded size/hash; no duplicate manifest paths; coverage exceptions are explicit.
- The one preserved C041 ZIP matches the size/hash above.
- Current claim objects, source records and experiment/access records equal the C041 lists exactly, with 85/113/36 unique identifiers; a changed current claim-registry envelope is allowed and explicitly recorded.
- Every retained baseline and recent iteration member equals its C041 counterpart byte-for-byte.
- Frozen `corpus/discovery_snapshot.json` matches SHA-256 `9b293509ab0ff928564c924e41f2c7da97e024ff28ac9b196e25cec638a2629b` and contains 1,721 records.
- Current status metadata agrees on latest scientific iteration 41, unachieved action/participant mission, no active semantic experiment, and a documentation-only review.
- Current navigation links resolve relative to their document directories. Historical archive locators are checked with an archive-member resolver or are explicitly identified as archived scope, rather than treated as broken root-relative paths.
- Current claim source/dependency IDs and evidence links resolve.

Moving the old canonical `verify.py` to a historical folder preserves its source, but does not make it runnable there: it computes its root from `__file__` and expects the full iteration 010 layout. Label it preserved historical verifier source and direct actual historical reproduction to the original iteration 010 archive.
