# Documentation map and authority

**Current after iteration 044 · D2026-10-26**

This map separates current decisions, preserved evidence and historical instructions. Relative links describe the extracted **Linear_A_Research_Current** package. The same front documents are maintained in Research Environment; detailed packet members are available in the portable package even when not present as loose documents.

## Current reading and working layer

| File | Purpose | Update rule |
| --- | --- | --- |
| [START_HERE](../START_HERE.md) | Brief orientation and reading order | Update with each research checkpoint |
| [CURRENT_STATE](CURRENT_STATE.md) | Effective conclusions, limits and current blockers | Reconcile with the completed report and state delta |
| [NEXT](../NEXT.md) | Human-readable decision brief for future work | Replace obsolete acquisition instructions explicitly |
| [RESEARCH_PROTOCOL](RESEARCH_PROTOCOL.md) | Mission, admission, source, exposure and review standard | Change deliberately and record provenance |
| [current_status.json](../registry/current_status.json) | Latest iteration, authority, counts and active status | Must agree with the current prose and registry |
| [research_queue.json](../registry/research_queue.json) | Conditional branch decisions and exact reopeners | Current operational queue; no automatic rotation |
| [ITERATION_BRIEF](../templates/ITERATION_BRIEF.md) | Reusable research intake and handoff | Fill for a new campaign; it is not a research result |
| [Review through044](../reviews/2026-10-26/REVIEW_THROUGH_044.md) | Current continuation review and preservation scope | Preserve dated review |
| [Review through042](../reviews/2026-10-25/REVIEW_THROUGH_042.md) | Earlier completed phase | Preserved unchanged |
| [Current phase report](../phases/2026-10-25/PHASE_REPORT.md) | C043/C044 result, source boundaries and stop | Completed continuation |
| [Prior phase report](../phases/2026-10-24/PHASE_REPORT.md) | C042 result and source boundaries | Preserved unchanged |
| [Review through 041](../reviews/2026-10-23/REVIEW_THROUGH_041.md) | Earlier audited documentation review | Preserved historical checkpoint |

## Scientific records and historical controls

| Record | What it controls | What it does not establish |
| --- | --- | --- |
| [Claims](../registry/claims.json) | Preserved claim objects and their IDs | Every legacy statement is not automatically accepted today |
| [Experiments](../registry/experiments.json) | Computation, source/access and feasibility records | The count is not the number of semantic experiments |
| [Sources](../registry/sources.json) | Source IDs, locators, acquisition levels and dependencies | A source entry is not proof that the whole publication was read |
| [Baseline dispositions](../baseline/CLAIM_DISPOSITIONS.json) | Current adjudication of the covered historical claims | Later source access and candidate selection |
| [History crosswalk](../baseline/HISTORY_CROSSWALK.json) | Older claims and the reports that narrowed them | A fresh revalidation of every original source |
| [Exposure ledger](../baseline/EXPOSURE_LEDGER.json) | Known exposure at the baseline | Absence from the ledger does not mean unseen |
| [DO_NOT_REUSE](DO_NOT_REUSE.md) | Accumulated warnings and exact scope limits | A research queue or a ban on genuinely new evidence |
| [HISTORY](HISTORY.md) and [CHANGELOG](CHANGELOG.md) | Append-only chronology and maintenance record | Present-tense guidance in old entries remains historical |

The frozen baseline has 12 files. Its report, queue, source inventory and publication note remain the 18 October snapshots. The specific findings of 038–044 supplement the scientific record; the current queue consolidates their operational consequences. Original editions and object evidence control observations. Recency alone does not decide a source conflict.

## Find the recent evidence

| Packet | Start | Decisive record | Comparison and continuation |
| --- | --- | --- | --- |
| Cord-function join,043 | [Report](../iterations/043/REPORT.md) | [Exact joins](../iterations/043/evidence/JOIN_FINAL.json) | [Review](../iterations/043/review/FINAL_REVIEW.md), [continuation](../iterations/043/CONTINUATION.md) |
| HT31 vessel class,044 | [Report](../iterations/044/REPORT.md) | [Overlay](../iterations/044/evidence/HT31_OVERLAY.json), [source packet](../iterations/044/evidence/SOURCE_PACKET.md) | [Review](../iterations/044/review/FINAL_REVIEW.md), [continuation](../iterations/044/CONTINUATION.md) |
| KH Wc2123, 038 | [Report](../iterations/038/REPORT.md) | [Critical overlay](../iterations/038/evidence/KHWc2123_critical_overlay.json) | [Rivals](../iterations/038/analysis/RIVAL_COMPARISON.md), [continuation](../iterations/038/CONTINUATION.md) |
| SI Zg1, 039 | [Report](../iterations/039/REPORT.md) | [Critical overlay](../iterations/039/evidence/SIZg1_critical_overlay.json) | [Rivals](../iterations/039/analysis/RIVAL_COMPARISON.md), [continuation](../iterations/039/CONTINUATION.md) |
| Akrotiri pair, 040 | [Report](../iterations/040/REPORT.md) | [Evidence record](../iterations/040/evidence/EVIDENCE_RECORD.json), [sources](../iterations/040/evidence/SOURCE_RECORDS.json) | [Rivals](../iterations/040/analysis/RIVAL_COMPARISON.md); apply 041 to old access tasks |
| KN Zb27 / ZA Zb3, 042 | [Report](../iterations/042/REPORT.md) | [Reading/object overlay](../iterations/042/evidence/READING_AND_OBJECT_OVERLAY.json), [sources](../iterations/042/evidence/SOURCE_RECORDS.json) | [Analysis](../iterations/042/analysis/C042_ANALYSIS.md), [continuation](../iterations/042/CONTINUATION.md) |
| Akrotiri catalogue/sample link, 041 | [Report](../iterations/041/REPORT.md) | [Catalogue overlay](../iterations/041/evidence/CATALOGUE_OVERLAY.json), [sources](../iterations/041/evidence/SOURCE_RECORDS.json) | [Join decision](../iterations/041/analysis/JOIN_DECISION.md), [continuation](../iterations/041/CONTINUATION.md) |

Each campaign also retains its source records, reviewer notes, adjudication and reproduction instructions. Full new third-party publications are not redistributed; their source URLs, hashes and access scope remain recorded.

## Supersessions that matter for the next team

| Earlier instruction or statement | Effective current disposition |
| --- | --- |
| Frozen baseline queue gives Flouda first conditional priority | Use [current queue](../registry/research_queue.json); conditional priorities depend on an actual changed evidence route |
| 038 screened SI Zg1 but did not investigate deeply | 039 evaluated its complete AB118 target argument |
| 040 obtained only 2019 Akrotiri metadata | 041 acquired the official complete volumes and inspected the relevant catalogue, plates and concordance |
| Original 2019 statement of isolated marks | Preserve separately from the later possible lost continuation; singleton status is not settled by choosing the convenient source |
| 2021 necessity of separate Akrotiri potter and inscriber | The later source removes that necessity; identity and separation are both unproved |
| Initial ritual “mission achieved” and unused-validation wording | Retired by baseline B-D01 |
| Iteration 13 personnel list; iteration 16 deficit breakthroughs; 18 fulfillment; 20 remainder | Read their later correction chains in the [historical audit](../reviews/2026-10-23/historical_research_audit.md) and baseline dispositions |
| Old files called CURRENT_STATE or old report “next steps” | Historical snapshots housed under their iterations; they do not replace the current front documents |

The [organization log](../reviews/2026-10-23/ORGANIZATION_LOG.json) records old paths, new paths and stable file identities. Historical citations retain their original paths; use the log to locate a moved loose artifact. The archives preserve original internal paths unchanged.

## Archive navigation and reproduction

The exact [C041 archive](../iterations/041/Linear_A_Campaign_041.zip) preserves C040, then C039, C038 and the baseline/history chain. Earlier archives remain nested to preserve their original bytes without repeatedly flattening duplicate copies.

The [archive navigation index](../registry/archive_navigation.json) resolves **31 unique archive roots and 60 report/atlas/baseline members**. It records the actual parent/member chain and hashes. These are navigation counts, not research achievements.

Use **python3 tools/read_history.py --list Iteration_21** to find a report and **python3 tools/read_history.py --read 23** to read the indexed iteration 21 report. The [history reader](../tools/read_history.py) verifies the archive chain and prints the preserved text without extracting or modifying it. A report's scientific meaning remains subject to later corrections.

The early unnumbered recheck and nextstep runs remain unnumbered; do not invent iterations 1 and 2. Protected original Deep Research reports are identified in the frozen baseline source/crosswalk records and are not edited or copied into a substitute authority.

### Known historical path traps

| Historical reference | Correct interpretation |
| --- | --- |
| Generic original verify.py and MANIFEST.json | Iteration 010 artifacts; now preserved under [archive/010_environment](../archive/010_environment/README.md) |
| BASELINE.json reopening_brief = EVIDENCE_PREREQUISITES.md | Frozen shorthand; consult [baseline/EVIDENCE_PREREQUISITES_36_37.md](../baseline/EVIDENCE_PREREQUISITES_36_37.md) |
| verify039.py or verify041.py in an old REPRODUCE file | Run only inside that exact original campaign snapshot; do not run against edited front documents |
| registry/archives.json local paths | Original iteration 010 inventory and original archive-root scope; use the current navigation index for nested history |
| corpus/sigla_sequences_2026-09-07.json | Historical export with 802-face/1,401-chunk scope; not an alias for the 1,721-record [discovery snapshot](../corpus/discovery_snapshot.json) |
| ZIP path followed by !/ | A member inside an archive, not an ordinary filesystem path |
| C041 PACKAGE_MANIFEST.json | Original checkpoint manifest inside the preserved ZIP; current package uses [MANIFEST.json](../MANIFEST.json) |

The current [verify.py](../verify.py) validates the extracted current package, its links, immutable evidence, unchanged inherited scientific prefixes and appended C043/C044 records. It does not validate source interpretations, ancient readings, assays or meanings. Download the complete current ZIP before running it; downloading one script into an incomplete directory is not a package verification.

## Publication status

Read-only Sites metadata observed on 23 October reports **Linear A, in the Open**, version **3**, active, last updated **20 October 2026**, with no listed site automations. The URL is [linear-a-open-research.madebyhenry.chatgpt.site](https://linear-a-open-research.madebyhenry.chatgpt.site).

Rendered site content was not inspected in this review. The site is not certified as synchronized with this current checkpoint, and no publication or deployment occurred. The [18 October PUBLIC_SYNC note](../baseline/PUBLIC_SYNC.md) retains its historical version-1 observation; it is superseded for current metadata, not silently rewritten.

The intended external GitHub project repository was not verified in this review. A failed scoped search is not proof that it does not exist. The current deliverable and research records do not depend on an assumed repository.

## Maintenance rule

After substantive research, update the current front documents and status/queue together, preserve the completed campaign, append history/changelog and refresh the current package. Leave frozen sources and historical claims intact; add a scoped correction when needed. A documentation-only change gets a documentation revision and review entry, not a new research iteration.

The through-041 verifier is pinned inside the [exact D2026-10-23 package](../archive/D2026-10-23/Linear_A_Research_Current_through_041.zip). Run it only inside that snapshot. The current verifier is scoped to044 and uses [explicit expectations](../registry/verification_expectations.json), fixed old snapshot hashes and unchanged inherited scientific prefixes. The exact [through042 snapshot](../archive/D2026-10-25/Linear_A_Research_Current_through_042.zip) also preserves its own verifier and the 87/37/121 inherited registry objects. The C042-only [campaign archive](../iterations/042/Linear_A_Campaign_042.zip) preserves its analysis and review. The31-archive/60-report historical index remains unchanged; its current_campaigns metadata points to042–044. Future checkpoints must extend expectations deliberately.


## C043/C044 result and evidence navigation

The [continuation charter](../phases/2026-10-25/PHASE_CHARTER.md), [decisions](../phases/2026-10-25/DECISION_LOG.md), [candidate comparison](../phases/2026-10-25/CANDIDATE_COMPARISON.md), [access ledger](../phases/2026-10-25/ACQUISITION_LEDGER.md) and [exposure record](../phases/2026-10-25/EXPOSURE_AND_DEPENDENCE.json) define this phase. C044’s graded category preference must always retain its unconfirmed material-extension qualification. The [unsent request](../iterations/044/CONTINUATION_EVIDENCE_REQUEST.md) identifies the outstanding primary pages. Source working paths in agent ledgers identify acquisitions; they do not imply that full third-party publications are embedded.
