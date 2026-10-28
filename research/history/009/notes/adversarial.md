# Independent adversarial review — iteration 9

Review date: 2026-09-07 UTC. The reviewer did not author the HT24 or identity analyses. This is an independent review within the same project, not an external epigraphical peer review.

## Scope actually completed

- Read and reran `analysis/anetaki_textile_test.py` against `notes/anetaki.json`.
- Independently recalculated its central inequalities using exact fractions, without importing the implementation.
- Opened the locally retrieved primary PDF, Del Freo (2020), *Wool Working at Hagia Triada*, pp.55–63; visually inspected its p.55 drawing/transcription including the grey uncertainty indicators. The file has 13 PDF pages; article p.55 is PDF page 5. [Institutional PDF](https://openportal.ispc.cnr.it/data/2020/421681/2020_421681.published.pdf).
- Read and reran `notes/identity_analysis.py` against `notes/identity.json`. Inspected the selected context rows and exact-set comparison logic. This is not a fresh autopsy of HT7/10/98/49/ZA10.

## Verdict on the HT24 arithmetic

**The central sensitivity result is mathematically correct under its stated fixed-45 model.**

Let S=6+10+9½+6=31½, T=10(1¾+1¾+1)=45, and M be the subtotal assumed to carry ME. If unmarked quantities use unit 1, ME-marked quantities use a positive multiplier m, and all missing contributions are nonnegative, the necessary condition is:

`(S−M)+mM ≤ T`.

| ME assignment | M | Unmarked subtotal | Maximum multiplier | Minimum at m=2 | Residual from45 |
|---|---:|---:|---:|---:|---:|
| Secure10 only, other entries taken unmarked in this countermodel | 10 | 21½ | 47/20 | 41½ | 3½ |
| Also accept ME? beside6 | 16 | 15½ | 59/32 | 47½ | −2½ |
| Hypothetically restore ME on all four preserved numerical groups | 31½ | 0 | 10/7 | 63 | −18 |

The values and verdicts match the runnable analysis. The target excludes a doubled multiplier only in the latter two scenarios. This is a useful sensitivity result about an inference, not a probability estimate or a translated sign.

### Damaged numeral lower bounds

The primary transcription gives `]6`, `10[`, `]9 J`, and `6`. Under the conventional additive, nonnegative interpretation of their numeral/fraction marks, 6,10,9½,6 are valid lower bounds: a damaged extension can add, not subtract. This requires accepting the surviving identifications and J=½. It does not mean the original four values are known exactly. In particular, the residual13½ at m=1 can include extensions of partially preserved amounts as well as quantities of the two lost entries.

The source supports the grey uncertainty recorded for ME beside6; the secure ME next to10 is not grey. Thus the toggle is tied to a real published uncertainty rather than invented for the calculation. The third numerical entry lacks its commodity sign, so assigning it to the same commodity remains a reconstruction, explicitly proposed in Del Freo p.55.

The label “secure ME only” must always be described as a countermodel taking the other positions unmarked, not as observed absence of ME in the breaks. For multipliers below1, its computed minimum is only a minimum within that assignment; it is not a universal minimum over all possible hidden ME placements.

### Positive residual is weaker than a viable inscription

A positive residual means these inequalities do not reject a model. It does not prove suitable marks fit the remaining space, or establish that the missing entries had the required values. For illustration, the numbers6,10,9½,6,3,½ sum to45 after doubling only the second amount. This is a **mathematical completion**, not proposed restorations of HT24. No such quantities were newly read.

## Strongest counterargument: the equal-mass premise

**“Same batch” alone does not justify equating the two recorded masses.** If the recto records an input and the verso a processed output, material can be removed, added, or counted under a different accounting convention. The test therefore also requires no unaccounted processing loss/addition and compatible measures on the two sides. Del Freo himself discusses the potential importance of processing losses on p.61, while favoring already-spun wool for his reconstruction. His footnote49 on p.62 explicitly argues that spun-to-woven work produces few scraps, and allows that scraps might have been returned. This supports his chosen reconstruction but does not make equal mass an independent observation. The paper's historical argument is qualified, not a claim of an absolute arithmetic exclusion of every different unit (p.58).

A simple countermodel demonstrates the consequence. If the input/output mass ratio were11/10, the input allowance would be49½ for an output45. The tentative-ME doubled model's preserved minimum47½ would then leave2, instead of exceeding the allowance. This is a chosen sensitivity example, **not evidence that HT24 had a10% ratio difference**. The necessary ratio for the preserved47½ alone is at least19/18; accounting for positive lost quantities could require more. The 45 noduli could independently strengthen a fixed input amount only if their unit value and association with this precise batch are separately established. Those links remain interpretive.

Accordingly, a better photograph of the doubtful ME can change the verdict **within the fixed45 model**. It cannot by itself decide whether ME names a unit. The report should make this qualification explicit in the next-test statement and data assumptions.

## Other findings and limits

- The exact 45 amount is conditional on the accepted AB118 reading, proposed J/E values, 10:1 conversion and common accounting relationship. It is not an inscribed total on the recto.
- The “preserved mean” is a mean of numerical lower bounds, not a mean of four completely preserved original amounts. The189/4 six-entry imputation result is correct arithmetic; it should only illustrate that literal mean imputation does not yield45 exactly.
- The fractional-nodulus objection reproduces Del Freo p.59 and Hallager, whom he cites. It is not new here. For `]9J`, a missing integer extension does not eliminate the fractional remainder, but the code's displayed19/2 is a representative lower bound, not the certain original quantity. Other unknown conventions could change that argument.
- Three scenarios selected after reading the text are not a blind holdout or a statistical test. The code appropriately makes no p-value or linguistic likelihood claim.

## Identity analysis review

Both face-level and whole-tablet set intersections reproduce. Among the selected strict non-target multisign labels, the TA-NA-TI faces share no exact label with ZA10a. Whole-tablet aggregation adds SA-MA between HT10 and ZA10. DA-RE occurs with TA-NA-TI on HT7a and HT10b. The code excludes target labels, single signs, composites and damaged/doubtful labels from strict sets, and retains the damaged HT49 alternative separately.

This shows that **this particular exact-associate test did not establish identity**. It does not supply evidence that the designations are different: sparse records, different sites, unrecorded associates, short-name homonyms, and imperfect chronological overlap could readily produce the result. Conversely, even the shared DA-RE does not certify that either label names the same historical person. The output's cautions appropriately preserve these limits.

HT10b's TA-NA-TI amount includes E and HT98a's includes J E. That is evidence against treating every such numerical expression as a literal count of complete people. It does not exclude a personal-account name, a fractional allocation to people, or another person-related category. The code's limited wording is correct.

A provenance issue was reported before editing: `notes/identity.json` originally recorded2026-09-08, although the actual UTC date checked during review was2026-09-07. The root agent was asked to correct dates. No input data were edited by this reviewer.

## Reproduction

From the extracted `linear_a_round9/` directory:

```bash
python analysis/anetaki_textile_test.py
python notes/identity_analysis.py
```

The mathematical audit can also be repeated independently:

```python
from fractions import Fraction as F
q = [F(6), F(10), F(19, 2), F(6)]
T = 10 * (F(7, 4) + F(7, 4) + 1)
for marked in [(1,), (1, 3), (0, 1, 2, 3)]:
    fixed = sum(x for i, x in enumerate(q) if i not in marked)
    M = sum(q[i] for i in marked)
    print((T-fixed)/M, fixed+2*M, T-fixed-2*M)
```

Expected rows: `47/20 83/2 7/2`; `59/32 95/2 -5/2`; `10/7 63 -18`.

**Final review conclusion:** no numerical error found in the central tests. The report can retain the sensitivity result with the explicit equal-mass qualification. Neither the arithmetic nor the context intersections independently identify an action or participant role.

## Consolidated machine-ledger audit

A subsequent bounded audit inspected `analysis/run.py` and the generated observations, sources, claim and experiment ledgers. At that audit snapshot they contained115 observation rows and56 source-registry rows. Every observation source reference resolved by its `(branch, source_id)` pair; every branch claim's evidence/support/counterevidence reference resolved to an observation or source in that branch. No duplicate evidence IDs or registry IDs were found. Referenced result/note files existed. Provenance dates in the identity branch had been corrected to2026-09-07.

The original records retain uncertainty and physical observations, so no source evidence was found irretrievably lost. The following exposed-schema issues were sent to the root agent for correction before packaging:

- `linear_b:LB01` exports an empty `sign_uncertainty` list scoped to TA-NA-TO, while its diplomatic text includes a damaged upper label. Export explicit target scope and the separate other-uncertainty list to prevent consumers reading the empty list as a whole-inscription certainty flag.
- `LB05`'s explicit right divider is stored as `right_word_boundary`; include it in the common boundary mapping.
- Add `observation_text`, evidence kind/feature, qualifications and limitations. Several physical-context and publication-history rows otherwise appear content-empty in the common fields, despite informative original records.
- Separate `.4` from the roundel branch's `KN V(4)831.4` object IDs and expose a canonical key/aliases for spacing variants such as HT24/HT24 with a space. None of the current row counts should be interpreted as a count of independent inscriptions.
- Include source-local `pages` as a bibliographic-locator fallback, where applicable. Source-level acquisition dates can be inherited from the audited branch date only if that is documented; absence of a source-local date is not a later retrieval.

These are export clarity/provenance improvements. They do not change the substantive reading or arithmetic verdicts. This audit did not edit concurrent reports or source inputs.
