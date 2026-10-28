# HT24 fallback: establish what the total measures before rereading ME

Date: 2026-09-09. Status: **conditional identifiability result; no new reading, yield, or participant role established.**

The useful new result is a sharper acquisition rule. **Resolving ME? beside 6 alone cannot exclude a doubled unit if output yield remains unconstrained.** Conversely, if the 45 noduli could independently be tied to the *recto input* with a known one-unit denomination and complete count, downstream yield would be irrelevant to that exclusion. The next work must distinguish those two claims about the total; they are different experiments.

This extends iteration 9's calculation rather than claiming its arithmetic again. Inputs and uncertainty coding were read from `inputs/extracted/linear_a_round9/notes/anetaki.{md,json}`, `analysis/anetaki_textile_test.py`, and `RETURN_TO_CHATGPT.md`. The earlier inspection of GORILA photographs is inherited, not a new autopsy here.

## Context check

Del Freo places the noduli on the sill between Room 27 and Corridor 9, near the threshold of Room 26 where HT24 was identified. He reports one seal design, similar shapes and local clay. His proposed workshop is neither named in the tablet nor identified by a sealing; production-stage and receipt interpretations remain reconstructions. His approximately 50% preparation loss concerns a Mycenaean comparison, not a measured HT24 yield. [Del Freo 2020, pp.57 n.9, 59 n.30, 60–62](https://iris.cnr.it/retrieve/435c5e13-7821-4b55-aec2-2c07865e1652/prod_421681-doc_175687.pdf).

A fresh source check reached Militello's archaeological monograph. It describes an isolated tablet near the southern entrance, and unattached noduli rather than labels attached to surviving wool containers. The argument for an administrator rather than multiple outside sealers depends on expecting different seals from different contributors. That expectation does not exclude a single intermediary or a common institutional seal. It cannot independently assign one of the tablet's headings to the seal user. [Militello 2014, pp.262–263](https://www.academia.edu/113784761/Pietro_Militello_Fest%C3%B2s_e_Haghia_Triada_Rinvenimenti_minori_I_Materiale_per_la_tessitura_).

The newer StorAtlas project retains the spatial association: the tablet is placed on the 26/9 threshold and the noduli approximately two metres away on the Room 27 sill. The page draws on existing findspot research and provides no batch label, newly read ME, or measured yield. Its exact distance differs from Del Freo's approximately one metre, and one later sentence also shifts the room reference; do not convert these approximate summaries into precise coordinates. [StorAtlas, South-West Quarter, “Finds” and “Interpretation”](https://storatlas.weebly.com/south-west-quarter.html).

**Evidence decision:** retain HT24 plus the 45 noduli as a strong contextual association worth studying, but do not encode it as a physically joined, named, or independently mass-calibrated packet. Repetition of this interpretation across sources does not create independent observations of a 45-unit input total. The shared seal design has no demonstrated link to KU-*56-RI-JA, PA-SA-RI-JA, or the broken final heading.

## Executed extension: what additional observation would identify a multiplier?

Let:

- `B = 31½`, the inherited sum of surviving recto numerals;
- `S = 10` with only secure ME, or `S = 16` when accepting ME? beside 6;
- `m > 0`, a hypothetical ME multiplier;
- `x ≥ 0`, unpreserved *weighted* input;
- `R = 4½`, the conditional reverse total;
- `c > 0`, conversion to standard wool units (`c = 10` in the proposed model);
- `0 < y ≤ 1`, output/input yield under a no-additions model.

The balance is

\[
cR=y\left[B+(m-1)S+x\right].
\]

Even with the reading settled and `c = 10`, **every positive multiplier is algebraically compatible** when `x` has no upper bound and yield can approach zero. For any `m`, write `L = B + (m−1)S` and choose

\[
x=\max(0,45-L)+1,\qquad y=\frac{45}{L+x}.
\]

This constructs `x > 0`, `0 < y < 1`, and exactly 45 output units. The result is a proof of non-identification under the stated model, not a claim that every completion fits the damaged writing. Unknown token denomination or free conversion `c` introduces further ambiguity.

With a genuinely independent lower bound `y_min > 0`, the necessary bound becomes

\[
m\leq1+\frac{cR/y_{\min}-B}{S}.
\]

| New independent constraint | Consequence for doubled ME, accepting ME beside 6 |
|---|---|
| Better reading only; yield free | No exclusion by this arithmetic |
| Same output = 45; actual yield at least 95% | Excluded even before missing input: multiplier ceiling `1211/608 ≈ 1.9918` |
| Same output = 45; actual yield at least 90% | Lower bound allows doubled ME: ceiling `69/32 = 2.15625` |
| Same output = 45; yield at least `18/19` | Boundary case: doubled ME requires zero missing weighted input at equality; positive missing input would exclude it |
| Independent recto input = 45, however measured | Doubled ME excluded by the visible minimum alone; no downstream yield is needed |

The 95% and 90% values are experimental requirements, **not observed ancient yields**. A modern wool-processing experiment would constrain HT24 only after independently establishing the relevant initial and final material states and their comparability. The word “spun” cannot be assumed merely to make the needed yield bound convenient.

The input-token route requires all of: same batch; noduli count complete for that batch; one known standard-input unit per nodulus; no missing/returned/reused tokens; and the signs and quantities belonging to the counted input operation. “45 objects nearby” supplies none of those identifications on its own. Once an input total is established, this becomes an input inventory constraint and is no longer dependent on a lossless input/output equation.

The code constructs exact examples and computes the yield-bound ceilings for both reading scenarios. It deliberately does not count a feasible numerical completion as an epigraphic restoration.

## Mission decision and next acquisition

**Park HT24 as a numerical fallback until there is an independent input-total link or a comparable processing-stage/yield constraint.** A better photograph remains useful epigraphy, but by itself is not the highest-value discriminator for this branch. Search results retrieved no new secure ME reading or actual HT24 yield; this is a bounded search result, not a claim that no unpublished or inaccessible evidence exists.

For sentence roles, the decisive missing link is still a named participant tied to a particular operation. All current numbers can survive a swap among delivered amounts, planned allocations, stored holdings, and production targets. Even resolving `m` would classify an accounting modifier, not supply an action verb or a source/recipient opposition.

Recommended acquisitions, in order:

1. A complete second text with both marked and unmarked wool and an independently read total in the same units, preferably with no processing transition. This would estimate a multiplier without HT24's restored balance.
2. An independently documented correspondence between the 45 noduli and the recto input, including denomination and completeness. Reconsult original excavation notebooks and Hallager 2002 before treating later summaries as packet evidence.
3. Improved HT24 images with a blind sign assessment once either total constraint exists. Retain all damaged numeral boundaries, not only the ME adjunct.

Reproduce with `python iterations/010/notes/ht24_fallback/identifiability.py` from the research root. Results are in `notes/ht24_fallback/identifiability_results.json`; retrieval and dependency details are in `notes/ht24_fallback/sources.json` relative to this iteration. New analysis priority is unestablished.
