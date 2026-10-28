# Iteration 010 adversarial review

Reviewed 2026-09-09: `code/corpus_pairs.py`, `results/corpus_pairs.json`, `notes/corpus_pairs.md`, `code/packet_models.py`, `data/packet_quantities.json`, `results/packet_models.json`, `notes/documentary_links.md`, and their source metadata. I also independently inspected the saved GORILA I p.135 and p.155 images. This is a review of the edition and analysis, not object autopsy or a new literature search.

**Verdict: no blocking calculation defect found.** The results can support a descriptive candidate atlas and rejection of a tightly specified quantity model. They do not establish a participant identity, an operation, or grammatical roles. Most safeguards below are already stated in the technical notes and must survive compression into the atlas and handback.

## Material findings and required wording

### AR-01 — Define the negative result at the actual filter and matching scope

**Risk:** “Searched 802 inscriptions and found no long variants” would overstate the experiment. The source has 802 indexed faces but only 220 nonempty phonetic face contexts; the most inclusive audit has 250. All layers omit broken/uncertain sequences, one-sign items and KU-RO/KI-RO. The inventory also has known genre and acquisition limitations. The narrow variant function tests only initial A addition/deletion and terminal-sign substitutions, requires a non-target exact associate, and excludes same-object pairs. The Q forms differ in two positions, so they are not eligible for that narrow function; a separate broad packet screen recovers them.

**Required wording:** “No exclusive terminal-only variant pair with forms of at least three signs and an exact non-target associate was found on separate faces of separate objects among the retained sequences in this snapshot.” An initial-A result needs the same scope qualifier. The broader screen is exhaustive only within records already passing its three-associate threshold. Do not call either a global absence of linguistic alternation or linked referents.

**Current status:** `corpus_pairs.md` states these scope limits and exposes all filter counts. Preserve them in the user-facing summary, at least as a compact note.

### AR-02 — “Independent associates” means target-independent strings, not independent events

**Risk:** The field name `independent_associates` removes the candidate strings before counting shared strings. It does not establish statistical independence, independent ancient testimony, or names rather than commodity vocabulary. Five other strings make the Q comparison worth testing but do not uniquely identify its referent. Sum-of-rarity weights are not likelihood ratios.

**Required wording:** Use “five other repeated labels” or “target-independent roster support.” Describe the score only as a ranking aid. The common-commodity/quality and related-but-distinct-account rivals in `documentary_links.md` must remain live.

**Current status:** Code method strings and notes already disallow significance and identity inference.

### AR-03 — Strengthen the ratio rejection by testing one HT86a section separately

**Finding:** HT86a has two sections with different headings and grain composites. Pooling their six rows requires a stronger uniformity assumption than necessary. The mismatch already occurs within the first section:

| HT86a first-section label | HT86a quantity | HT95b proposed counterpart quantity | Ratio |
|---|---:|---:|---:|
| KU-NI-SU | 20 | 10 | 2 |
| SA-RU | 20 | 10 | 2 |
| DI-DE-RU | 20 | 10 | 2 |
| QA-RA2-WA / QE-RA2-U, hypothetical equivalence | 10 | 10 | 1 |

Thus the counterexample survives removal of DA-ME and MI-NU-TE and does not require a common conversion across the two different HT86a grain composites. It also survives the DA-ME/DA-ZA indexing discrepancy. This is a narrower and stronger diagnostic than the pooled presentation.

**Required wording:** “Within HT86a's first section, the three exact counterpart labels have a 2:1 numeral ratio to HT95b, while the proposed Q counterpart has 1:1. A single scale factor for equivalent quantities does not fit that alignment.” This still assumes the Q forms align and that the compared amounts are equivalent quantities; HT95b has no explicit grain logogram. Do not infer that the Q forms are unrelated, that quantities changed between observed dates, or that an input/output balance failed.

**Related wording correction:** The Q item and its three first-section companions change from A-KA-RU to the A-DU context in this comparison. DA-ME and MI-NU-TE are already under A-DU on HT86a. Avoid implying that all five companions changed heading together.

**Fix verified:** Root added `section_1_sensitivity` to the code and regenerated results. The three exact ratios are 2 and the hypothetical Q ratio is 1; the restricted model returns false. The output explicitly retains the missing HT95b unit and common-event assumptions.

### AR-04 — The computed sums are numeral sums, not established physical totals

**Risk:** `computed_totals_not_written_totals` gives 110, 67 and 60. Although the key rejects written-total status, the values can still be mistaken for comparable grain stocks. HT86a pools different grain composites; HT95b lacks an explicit commodity sign. Those sums cannot establish a mass difference or account balance without further assumptions.

**Required wording:** “Sums of transcribed numerals, without a demonstrated common commodity/unit.” Keep them out of headline comparisons unless this distinction is visible. No arithmetic error was found in the sums themselves.

**Fix verified:** Root renamed the result key to `numeral_sums_not_written_or_commensurable_totals` in code and regenerated output.

### AR-05 — Preserve witness and acquisition levels

**Risk:** Face-level results can be mistaken for replications: HT95a/b are one tablet, HT86b includes erased/palimpsest evidence, and HT9a/b are one object. Grouped objects combine information that may belong to different headings or writing episodes. Similarly, HT87/117 and the AT125 cross-media link have been read in scholarship but were not newly verified on their original plates in the documentary subtask.

**Required wording:** “Two tablets, with face and writing-state distinctions retained” for the HT86/95 case. Label the HT87/117 and seal link as published leads with the acquisition levels supplied by `documentary_links.md`. A common seal does not identify a named writer, sender, or recipient.

**Current status:** Same-object face pairs are excluded from rankings, explicit KH79/KH79+89 grouping is handled, and notes describe the remaining limitations. `651 catalog-object groups` is properly labelled a computational grouping, not an independently verified census of ancient objects.

## Checks completed

- Source SHA-256 agrees with the result metadata; all 802 source face names are unique.
- Recomputed all six face/object and filtering combinations in memory without rewriting another agent's files. Ranked pair rows and variant rows exactly match the stored JSON; same-object face pairs are absent from ranked results.
- Verified the known explicit joined-fragment alias is grouped in the output rather than counted as a separate object. No additional demonstrated duplicated ancient witness was found in the reviewed candidate set; this is not a complete epigraphic join audit.
- Independently read the printed normalized quantities on GORILA I pp.135 and 155. They support the transcribed row numbers used in the packet calculation. The printed DA-ME sign comparison supports treating the frozen DA-ZA as an unresolved database discrepancy rather than usable morphology. The damaged isolated preceding sign remains distinct.
- Exact ratios are 2 for the five equal-label pairs, and 1 for the hypothetical Q pair. Prediction 20 versus observed 10 and residual −10 are correct under the stated mapping.
- The HT95a-minus-b control values are correctly 0, 0, 0, 0, −3 and +10. Their mixed signs alone say nothing about transfer direction or date order.
- Leave-one-label-out repetition is correctly described as internal consistency; the labels all instantiate the same 20/10 pattern and do not create an independent prediction test.

No p-value, chance probability, name identification, or grammatical-role conclusion should be added. The appropriate research gain is a better qualified candidate and a narrower rejected conjunction, with the source-conflict correction compounded into the research environment.
