# Linear A — Iteration 14 Ambitious Research Plan

## Mission

Move beyond the current structural result:

> `KI-RO • ENTRY 1 ... KU-RO N` marks a differential / exception subset in personnel administration.

Iteration 14 should try to determine **what kind of differential** this is.

The target is not merely another plausible gloss. The target is to discriminate among:

- absent / missing personnel
- owing / owed-to personnel
- surplus / extra personnel
- exempt / released personnel
- assigned / transferred personnel
- another outstanding or reconciled status

A successful iteration should either:

1. **identify the polarity/cause of KI-RO independently**, or
2. establish a much tighter impossibility result showing exactly what evidence is still missing.

---

# Core strategy

Iteration 14 should operate as five coordinated evidence lanes rather than one linear investigation.

## Lane A — Build a complete KI-RO entity recurrence graph

### Goal
Find designations that occur:

- under KI-RO in one record, and
- outside KI-RO in another independently interpretable record.

This is the most direct route to learning what changes when an entity moves into the KI-RO subset.

### Actions

1. Extract every complete designation occurring:
   - directly under KI-RO,
   - in a KI-RO-bearing section,
   - in closely associated KU-RO totals.

2. Normalize readings conservatively:
   - exact form
   - uncertain signs
   - restored signs
   - possible variants
   - scribal/site provenance

3. Search every designation across the full available corpus.

4. For every recurrence, record:
   - document
   - section
   - position
   - commodity/personnel context
   - quantity
   - heading
   - scribe
   - findspot
   - whether KI-RO is present
   - whether the recurrence was used to discover the candidate

5. Rank recurrence pairs by leverage.

### Priority score

Highest-value candidate:

> same designation + same site/scribe/administrative family + KI-RO in one context + non-KI-RO in another + independently recognizable surrounding structure.

### Breakthrough test

If the same designation occurs in a normal roster and a KI-RO subset, ask:

> What independently observable state changed?

Do not translate until an observable difference selects one hypothesis over the others.

---

# Lane B — Reconstruct complete personnel roster families

## Goal

Determine whether a KI-RO list is a subset, complement, exception list, or unrelated roster relative to another list.

### Target families

Begin with:

- HT 88
- HT 94
- HT 117
- HT 87
- HT 7
- any tablets sharing their scribes, personnel ideograms, headings, or recurrent names

Then expand only when a documentary link exists.

### Actions

For every target tablet:

1. reconstruct the entire record from the best available edition;
2. preserve line order, dividers, damaged signs, joins, erasures, headings and totals;
3. classify sections without semantic assumptions:
   - main list
   - secondary list
   - KI-RO section
   - total
   - personnel ideogram section
   - commodity section
4. compare candidate rosters pairwise.

### Explicit models

For roster A and KI-RO list K, test:

- K ⊂ A
- K = A \ B
- K = B \ A
- K is a separate status class
- K is unrelated to A

### What would matter

If a KI-RO list consists entirely of names present in a larger independently dated or categorized roster, then KI-RO becomes a plausible **state-change marker** rather than a generic list heading.

If K equals a mathematically expected difference between two rosters, that would be especially powerful.

---

# Lane C — Numerical closure and polarity search

## Goal

Find one document family where KI-RO participates in a numerical relationship whose sign can be independently determined.

Iteration 13 showed that:

> `KI-RO = deficit`

is too narrow.

Iteration 14 should ask whether the sign can be recovered from *another quantity relation* rather than from English interpretation.

### Search targets

Look for documents containing some combination of:

- KI-RO
- KU-RO
- personnel ideograms
- repeated commodities
- explicit totals
- identical categories in two sections
- independently interpretable capacity/count constraints
- paired “before/after” or “expected/actual” structures

### Candidate equations

Do **not** assume any equation. Test whether the layout supports one of:

`Expected = Recorded + KI-RO`

`Recorded = Expected + KI-RO`

`Difference = |A - B|`

`Total = Main + KI-RO`

`Main = Total - KI-RO`

For each possible relationship:

1. derive the equation from document structure;
2. calculate every feasible orientation;
3. identify which orientations are mathematically impossible;
4. separate mathematical exclusion from semantic interpretation.

### Breakthrough criterion

A high-value result would be:

> Only one sign/orientation of the KI-RO quantity is compatible with an independently fixed total.

That would give polarity without relying on a translation.

---

# Lane D — Physical and documentary linkage

## Goal

Find evidence that two records belong to the same administrative episode.

Text similarity alone has repeatedly proven insufficient.

### Evidence types

Search for:

- same scribe
- same findspot / room
- matching seal
- matching clay type / tablet class
- joining fragments
- sequential archival context
- same unusual heading
- same unusual roster packet
- same commodity combination
- same quantity signature

### Priority

A physically or archivally linked pair containing:

- one main roster
- one KI-RO list

would be vastly more informative than two merely similar texts.

### Rule

Physical linkage can establish **same administrative network or episode**.

It does not by itself establish:
- same person
- supplier/recipient direction
- lexical meaning

Those remain separate claims.

---

# Lane E — Cross-domain KI-RO operator model

## Goal

Use commodity records to infer the abstract operation of KI-RO, then test whether that operation predicts personnel behavior.

### Corpus

Revisit:

- HT 30
- HT 123
- every additional KI-RO commodity record

### Model classes

Test KI-RO as:

- negative residual
- positive residual
- unsigned difference
- exception category
- carried balance
- reconciliation entry
- unfulfilled amount
- overage
- transfer/outstanding quantity

### Critical discipline

Do not use personnel interpretations to choose the commodity model.

First derive the strongest commodity-side functional model.

Then ask whether that model independently predicts:

> what a one-count KI-RO personnel list should look like.

A model that explains both domains with fewer special assumptions deserves priority.

---

# Parallel control lane — Linear B and other deciphered accounting systems

## Goal

Use deciphered systems only to test structural reasoning.

Do not project Greek meanings into Linear A.

### Questions

In Linear B personnel/accounting tablets:

- can a category heading also be counted as an entry elsewhere?
- how are absent, owed, assigned, exempt, or transferred workers represented?
- what graphical/accounting structures distinguish:
  - main roster
  - deficit roster
  - surplus roster
  - transfer roster
  - exception roster?

### Valid use

If our proposed structural diagnostic would misclassify known Linear B examples, reject the diagnostic.

### Invalid use

“Linear B uses X for absence, therefore Linear A KI-RO means absence.”

Never make that inference.

---

# Computational work

Iteration 14 should build a real research graph rather than another flat sequence list.

## Entity graph

### Nodes

- designation
- tablet
- tablet face
- section
- heading
- commodity
- personnel ideogram
- scribe
- seal
- location
- quantity

### Edges

- appears-in
- governed-by
- totaled-by
- shares-scribe
- shares-seal
- shares-roster
- same-object
- possible-variant
- physically-linked

### Why

The key question is relational:

> Which KI-RO members recur elsewhere, and what changes around them?

A graph makes that query natural.

---

# Evidence ladder

Every candidate should receive one of five levels.

## Level 0 — spelling resemblance
No semantic value by itself.

## Level 1 — shared administrative context
Useful for discovery.

## Level 2 — independently classified domain
Example: personnel context anchored by VIR ideogram.

## Level 3 — independently identified relation
Example: the same designation demonstrably changes from main roster to exception subset.

## Level 4 — polarity/action identified
Example: arithmetic or documentary evidence proves that the exception is a shortfall rather than surplus.

## Level 5 — construction prediction
The proposed interpretation predicts an unused witness correctly.

Iteration 14 should aim for **Level 4**.

---

# Candidate triage

At the beginning of the run, generate a ranked table:

| Candidate | KI-RO witness | Non-KI-RO witness | Same scribe/site? | Independent domain anchor? | Numerical leverage? | Physical link? | Score |
|---|---|---|---|---|---|---|---|

Do not spend equal time on every candidate.

Investigate the top 3–5 only.

---

# Pre-registered falsification tests

Before interpreting the strongest candidate, write down:

1. favored model;
2. strongest rival;
3. observation predicted by favored model;
4. observation predicted by rival;
5. what would falsify each.

Example:

> If KI-RO marks missing personnel, every KI-RO member should belong to an independently established expected roster but be absent from the recorded-present roster.

versus:

> If KI-RO marks additional personnel, members should appear outside the expected roster or increase the recorded count beyond the baseline.

Then inspect the validation evidence.

---

# Negative controls

Iteration 14 should explicitly search for:

- KI-RO entries that **do not** recur in expected rosters;
- normal roster entries that appear under KI-RO elsewhere;
- non-KI-RO sections with the same `ENTRY 1 ... KU-RO N` structure;
- commodity records that contradict a fixed polarity;
- similarly structured headings that clearly are not KI-RO.

These controls are essential because the pattern itself may be generic accounting syntax.

---

# Source audit requirements

For every decisive witness:

1. primary edition image if available;
2. normalized edition transcription;
3. modern transcription;
4. uncertainty ledger;
5. source dependence record.

No decisive claim should rest solely on:
- a reconstructed sign,
- a derivative corpus,
- or a modern translation.

---

# Iteration 14 stopping rules

Stop a branch when:

- its best result still depends only on spelling similarity;
- direction remains reversible after all available constraints;
- a necessary sign is restored but not visible;
- an equation requires a free parameter that can absorb any result;
- a historical interpretation is merely being rediscovered.

Do not keep producing increasingly polished English translations of an underdetermined structure.

---

# Breakthrough criteria

## Full breakthrough

Iteration 14 succeeds at the project mission if we can support something of the form:

> In construction X, designation A is independently shown to occupy role R under condition/action Y.

And:

- R is not inferred from Y,
- Y is not inferred from R,
- reversing the roles contradicts observed evidence,
- the construction is actually written rather than merely implied,
- at least one rival explanation is eliminated,
- and preferably the analysis predicts an unused witness.

## Major intermediate breakthrough

Also count as major progress if we establish:

> KI-RO has a fixed polarity or status class in personnel administration.

For example:

- negative shortfall,
- positive surplus,
- absent/missing,
- transferred,
- exempt,

provided the result is independently constrained.

---

# Deliverables

Iteration 14 should produce:

1. **KI-RO recurrence graph**
2. **full KI-RO occurrence inventory**
3. **top-candidate dossier**
4. **roster comparison matrices**
5. **numerical polarity tests**
6. **physical/documentary linkage table**
7. **commodity-domain operator model**
8. **Linear B diagnostic controls**
9. **prediction / exposure ledger**
10. **adversarial review**
11. **updated cumulative claim register**
12. **Iteration 14 report**
13. **reproducible research workspace**

---

# Recommended execution order

### Phase 1 — Discovery
Build the complete KI-RO recurrence graph and rank candidates.

### Phase 2 — Source audit
Primary-check only the highest-leverage recurrence pairs.

### Phase 3 — Roster reconstruction
Reconstruct the top linked personnel families.

### Phase 4 — Numerical polarity
Search for an independently fixed total or complement.

### Phase 5 — Cross-domain model
Determine whether commodity KI-RO predicts the personnel pattern.

### Phase 6 — Falsification
Run the strongest rival explanation against the same evidence.

### Phase 7 — Prediction
If a model survives, freeze a prediction before opening the best unused witness.

### Phase 8 — Consolidation
Update the structured research environment and clearly separate:
- established facts
- favored hypotheses
- rejected hypotheses
- unresolved dependencies

---

# Working hypothesis — explicitly provisional

The most productive hypothesis to challenge is:

> **KI-RO marks a reconciliatory difference between an expected administrative state and an observed/recorded state.**

In commodity accounts, that difference appears numerically.

In personnel accounts, it may appear as an enumerated subset of people.

If this is right, the next decipherment step is not translating KI-RO directly. It is identifying:

> **expected relative to what?**

That is the central question for Iteration 14.
