# C042: unit-free capacity comparison and its limits

2026-10-24. Comparative analyst. Status: completed finite model comparison, subject to lead adjudication. Source facts were supplied by the lead/source investigator; this analyst independently executed the model and checked its limits. No ancient object was independently examined by this analyst.

## Result

The two vessel inscriptions do not behave like full-capacity labels in one common volumetric unit at the published capacity values. With KN Zb27 read **107**, its approximately 34-litre carrier implies about **0.318 litres per written unit**. With ZA Zb3 read **32**, Stronk's 556-litre estimate implies **17.375 litres per written unit**. Those are consequences of the proposed model, not recovered Minoan units. The mismatch persists through all nine source-grounded historical reading combinations.

This is a **conditional physical constraint**, not a newly deciphered administrative action. It rejects the conjunction of common unit, full individual-carrier scope, and adequate source capacities. Partial filling, different units, or scope beyond one carrier can each remove the contradiction. The comparison does not choose among them. Olivier had already drawn attention to the smaller KN carrier bearing a larger numeral than ZA in 1992; that qualitative observation is not a project discovery. [1]

The concrete project improvement is to replace an unexamined frozen KN reading of 17 with an explicit source history—17, then 117, then an autopsy-based 107—and to state precisely what a capacity argument does and does not establish. The project scan found no earlier analysis of these exact capacities in its specified scope, but cannot establish genuinely unused evidence.

## Source-specific inputs

| Object / input | Value and status | Source and inspection control |
|---|---|---|
| KN Zb27 = HM5194 capacity | About 34 L | Christakis2010 p.51. The inspected article text supplies no capacity method or uncertainty. No invented error interval. [2] |
| KN numeral | 107 preferred | Del Freo2017 p.17 reports a 22 June2012 autopsy by Del Freo and Zurbach correcting117. This is reported physical examination, not a project autopsy. [3] |
| KN earlier readings | 117;17 | 117 in Olivier1992/Christakis2010;17 in earlier GORILA and the inherited frozen corpus. Historical sensitivity branches, not equally supported current readings. [1–3] |
| ZA Zb3 capacity | 556 L ±11%, or494.84–617.16 L | Stronk1972 pp.85–87, all three original pages inspected by lead. A geometric estimate using average inner radius and maximum wine-level height; not a performed filling measurement. The percentage is the author's tolerance, not a statistical confidence interval. [4] |
| ZA numeral | 32 preferred | Explicitly stated in Olivier1992 p.446's comparison; agrees with current inherited transcription. Original GORILA plate has not been inspected in this phase. [1] |
| ZA historical numbers | 22;21 |22 in Stronk1972; Best1982–83 pp.9–10 argues for21 against32 from damage/divider interpretation, and Stronk1982–83 p.27 conditionally accepts21. This is not a correction to32. Original Best pages were inspected by lead/challenger; no new project stroke adjudication was possible from the poor photograph. [4–5,7] |

Do not merge the unverified larger-capacity estimate cited by Younger, Notti2025's preview-only unit proposal, or a Linear B28.8-litre calibration into these inputs. A source-specific geometric estimate remains a source-specific estimate.

## Test and reproducibility

The frozen rule is `C042_ANALYSIS_RULE.md`, SHA256 `72ecdf4a19014190562b327dfecb88b93a5449c198fbfa60f37e3db568c167f0`. It was written after KN34/117/17 were supplied, but before this analyst received ZA capacity/numerals or the KN107 correction. This timing separates the rule from later values; it does not convert a source-led discovery into unused validation.

For a common positive volume unit *u*, full capacity requires

\[
V_{KN}=q_{KN}u,\qquad V_{ZA}=q_{ZA}u,
\qquad\frac{V_{KN}}{V_{ZA}}=\frac{q_{KN}}{q_{ZA}}.
\]

At the nominal values the two inferred units differ by a factor of about54.68 for107/32. Even using ZA's low source estimate, a full107-unit KN carrier would need about**1,655 L**, rather than about34 L. Its required capacity is at least**48.7 times** the published approximation. No credible probability is attached to that factor: KN's uncertainty is unspecified. The correct statement quantifies the necessary revision, rather than pretending a formal two-object interval test was available.

| KN numeral | ZA numeral | KN implied full unit, L | ZA implied full unit, L | Minimum KN capacity multiplier over34 L, using ZA's low estimate |
|---:|---:|---:|---:|---:|
| **107** | **32** | **0.318** | **17.375** | **48.7** |
|107|22|0.318|25.273|70.8|
|107|21|0.318|26.476|74.2|
|117|32|0.291|17.375|53.2|
|117|22|0.291|25.273|77.4|
|117|21|0.291|26.476|81.1|
|17|32|2.000|17.375|7.7|
|17|22|2.000|25.273|11.2|
|17|21|2.000|26.476|11.8|

The old17 reading weakens the mismatch but does not remove it. For the preferred107 and historical117 readings, the relation is already reversed at the ordinal level: the smaller carrier has the larger number. Olivier noticed this under117. [1]

### Post hoc geometry sensitivity

After the ratio test, the lead proposed a separate conservative envelope check; the challenger accepted its conditional form. Christakis reports a height of53cm. If the vessel is approximately axisymmetric and its maximum outer diameter is no greater than that height, as the published profile qualitatively suggests, an enclosing cylinder has volume

\[
V_{outer}\leq\pi(0.53)^3/4\approx0.11693\ {\rm m}^3=116.93\ {\rm L}.
\]

Taper and wall thickness reduce internal capacity relative to that envelope. Even the weakest historical17/32 branch requires at least262.88L, about2.25 times this bound; preferred107/32 requires at least1,654.62L. Thus this added check also excludes common-unit full capacities across all branches **under the stated profile and height premises**, without relying on34L as an exact measurement. No project diameter measurement, formal uncertainty interval, or new capacity measurement is claimed. The calculation is post hoc source-led sensitivity, not part of the frozen rule. A strongly distorted profile, failure of approximate axisymmetry, or materially inaccurate height would defeat this particular bound. [2]

Run `python3 capacity_comparison.py` in this directory, or run it by absolute path from anywhere. It uses exact rational arithmetic for the entered decimal source values, checks the frozen rule hash, and writes `capacity_results.json` and `capacity_results.csv`. Machine precision does not increase the precision of the source measurements. `capacity_inputs_source_updates_1.json` preserves the provisional input statuses before Olivier's original comparison was inspected; `capacity_inputs.json` is the final source-status revision. The numerical results did not change in that status update.

## Surviving alternatives

**Partial filling in one common unit.** If the text records an amount in its carrier, rather than full capacity, the inequalities are

\[
0<u\leq\min(V_{KN}/q_{KN},V_{ZA}/q_{ZA}).
\]

They have solutions for any two positive capacities and numbers. For107/32, the nominal upper bound is34/107 L per unit. At that upper bound, KN is full and ZA contains about10.17 L, about1.83% of its estimated capacity. An even smaller unit leaves both partly filled. These are constructive demonstrations of model feasibility, not observations of ancient contents. An independent lower bound on the unit or a demonstrated minimum fill level would be needed to exclude this alternative.

**Equal filling fractions.** If both were filled to the same fraction of capacity, even below full, the same ratio equation applies and the mismatch remains. With unconstrained unequal fractions, however, the preferred source values merely require KN's fraction to be about54.68 times ZA's. No inspected source establishes actual filling fractions.

**Different units.** Assigning each object its own unit trivially fits the full-capacity hypothesis. The shared conventional VIN/AB131 designation does not independently prove identical unit size across place, date and accounting convention. A common unit is a declared premise of the test, not its result.

**Scope beyond the carrier.** A label may concern a group, cumulative amount, obligation, allocation, or other accounting scope. This physical test does not establish any of those scopes and cannot distinguish their administrative direction. The previously exposed ZA batch/ritual-event alternative remains live; it was not newly discovered here.

**Uncertain physical model.** The source capacities use different or unspecified methods. KN's completeness/restoration and ZA's idealized geometry must remain attached to their source reports. The large factor required does make a minor rounding explanation inadequate, but this calculation alone supplies no formal error bound on KN.

## Decision and next obtainable observation

Stop this numerical comparison. Additional fitted units cannot clarify the meaning. A source correction overlay is warranted for KN's reading, and the common-unit full-capacity interpretation should carry this explicit constraint. No participant role, transaction direction, content residue, or lexical meaning follows.

The most consequential obtainable observations would be: an independently grounded unit applicable to the exact KN inscription; physical use evidence establishing a fill level; a complete source reconstruction of each exact carrier's capacity; or an independently linked record that fixes the numeral's scope. Better photographs of the numerals would strengthen reading control. They would not themselves identify the written relationship.

## Sources and project evidence

1. J.-P. Olivier1992, *Rapport sur les textes en hiéroglyphique crétois, en linéaire A et en linéaire B*, Mykenaïka, BCH Supplement25,443–456, p.446. Institutional original: https://helios.eie.gr/helios/bitstream/10442/147/1/A03.003.0.pdf . Lead/source investigator inspected p.446 pixels; comparative analyst read its extracted text. Credit includes prior recognition of the ordinal inversion.
2. K.S. Christakis2010, *A wine offering to the Central Palace Sanctuary at Knossos: the evidence from KN Zb27*, BSA Studies18,49–55. Exact author-hosted URL and object/figure chain are in `capacity_inputs.json` and `../source_archaeology/C042_SOURCE_REPORT.md`.
3. M. Del Freo2017, *Rapport2011–2015 sur les textes en écriture hiéroglyphique crétoise, en linéaire A et en linéaire B*, Aegean ScriptsI,3–30, p.17. Exact author-hosted URL in `capacity_inputs.json`; source investigator's extraction controls the107 autopsy statement.
4. J.P. Stronk1972, *A Pithos from Epano Zakro*, TalantaIV,85–87. https://www.talanta.nl/wp-content/uploads/2014/10/Stronk-85-87.pdf .
5. J.P. Stronk1982–83, *Linear A Liquid Measure: A Contribution*, TalantaXIV–XV,27. https://www.talanta.nl/wp-content/uploads/2014/10/Stronk-27.pdf .
6. `C042_EXPOSURE_CHECK.json` and `check_exposure.py`:50 unique indexed historical reports read through the documented verifying history reader, current prose/registry scan, and exact inherited corpus rows. This scope excludes all raw acquisitions and protected initial-report bytes. Absence of a hit is not absence of exposure.
7. J.G.P. Best1982–83, *The Zakro Pithos Inscription, Again*, TalantaXIV–XV,9–16, specifically pp.9–10. https://www.talanta.nl/wp-content/uploads/2014/10/Best-9-16.pdf .
