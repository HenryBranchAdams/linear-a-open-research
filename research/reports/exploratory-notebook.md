# Linear A: reconstructing the activity behind the writing

**Date:** 12 September 2026  
**Status:** Post-iteration-16 exploratory notebook. This is not iteration 17, a revised accepted-claim register, a completed decipherment, or a claim to scholarly priority. Original research packages are unchanged.

## Working conjecture

Some of the administrative texts may be organized around **continuing responsibilities** rather than complete, explicitly narrated transactions. A designation identifies the person, household, workshop, office, location or account to which resources are attributed. The record then distinguishes what has been handled from what remains to be handled. The institution maintaining the record may be an implicit participant.

This is a hypothesis about document production. It does not identify a language family, translate a verb, prove that all labels are names, or imply modern double-entry bookkeeping. Its value would be in predicting details of the ancient records that a rival model does not predict.

## 1. A concrete exploratory pattern: HT118

The published paired values are:

| Designation | Main amount | KI amount | Sum | Difference |
|---|---:|---:|---:|---:|
| MA-DI | 15 | 10 | 25 | 5 |
| QA-QA-RU | 6 | 4 | 10 | 2 |
| A-RI-SU | 4 | 1 | 5 | 3 |

The INSCRIBE institutional catalogue transnumerates these values and describes the object as a pig record with a miscalculated sum. Its public record includes a 3D model. The catalogue and transcription were consulted; this notebook does not claim a new 3D surface examination. [S1, S2]

**Observation:** each paired sum is divisible by five. The paired differences do not exhibit the same regularity.

**Speculation:** perhaps the two recorded quantities partition round targets or batches—25, 10 and 5—rather than the first quantity already including the second. In a fulfillment interpretation, the records would mean 15 handled and 10 remaining against 25; 6 handled and 4 remaining against 10; 4 handled and 1 remaining against 5.

Those are hypothetical reconstructions, not translations. Allocation/unallocated stock, two categories within planned batches, and other accounting partitions can share the arithmetic. A model in which KI is contained within the main quantity remains arithmetically possible as well.

### Executed sanity check

`explore_ht118.py` enumerates all six assignments of the three KI values to the three main values. Exactly one assignment—the written pairing—makes all three sums divisible by five. The script also reports both addition and subtraction for moduli two through ten.

This is **not** a confirmatory significance test. Addition, five, the tablet and the selected paired rows were considered after inspection. One of six is not an adjusted p-value, Bayes factor, or probability that a quota interpretation is correct. Three rows are a small exploratory signal.

### Unresolved facts retained

RI-RU-MA has main quantity 10 but no written KI value; it is excluded, not supplied with zero. The main quantities total 35 although the written KU-RO is 30. The explicitly written KI quantities total 15; the final transcription retains `15[`. No sign or numeral is changed to repair the main discrepancy. Common units and row scope remain assumptions when adding the values. KI's connection with KI-RO remains an explicit lexical dependency. [S1–S3]

**Discriminating prediction:** in an independently linked record using the same commodity and account scope, the complete amount for QA-QA-RU would be ten under the additive-target model, rather than six under the inclusive-target model. That prediction should be frozen before a genuinely unexamined witness is evaluated. Previously exposed material can test consistency, not provide a fresh holdout.

## 2. KI-RO as the part still requiring attention

HT34's edited `100 / PA3 70 / KI-RO 30 [[7]]` supports a complementary quantity under the scope assumptions retained in the review. The seven is editorially marked erased; its proposed association with a pre-correction 37 is conditional. The subtraction argument already appears in the Younger commentary. [S3, S4]

A productive working paraphrase is **the part still to be accounted for**, rather than an invariant English debt word. This can generate two different document shapes: remaining quantities under individual accounts, or a list of accounts still requiring reconciliation. It might connect quantitative KI entries with KI-RO-headed lists of one-count designations without assuming those lists count absent people.

The stronger proposition is not that a flexible gloss can describe everything. It is that a specified administrative procedure could produce those two representations at different levels of detail. A successful model must predict which level is written and when. Stable, fully resolved accounts placed under KI-RO with no relevant residual would be evidence against this particular model.

The leading rivals are reserve stock, categorical exceptions, exclusions or exemptions, and bookkeeping partitions unrelated to completion. The operation and the economic event must remain separate.

## 3. Counted labels need not count the named individuals

QI-TU-NE occurs as a counted item and as a heading/subheading, repeatedly associated with DI-KI-SE. SA-RU recurs across commodity contexts. These were surviving findings, not secure lexical translations, in the cumulative review. [S3]

A household, office or workshop can be one unit in an organizational list and the heading for many resource entries elsewhere. A personal name can likewise head an account with quantities greater than one or fractional quantities; the numeral may count goods or labor time rather than people.

Thus neither `LABEL 1` proves a personal name nor `LABEL 20` disproves one. The decisive question is **what the numeral counts in that context**.

This also suggests that stable institutional or household identity may sometimes be a better target than the same historical individual. A designation's continuity of responsibility can survive changes of representative or seal. That possibility requires testing rather than assuming every name is an institution.

## 4. Repeated rosters may describe schedules and allocations, not one event

The audited HT86/95 packet preserves five exact recurring labels independently of the proposed Q-form equation. HT86a has 20 for five labels and 10 for its Q entry; HT95b has 10 for the corresponding six positions. However, headings, commodity signs and composites differ, and the two faces of a tablet are not independent transactions by default. [S5]

A roster with changing amounts can be generated by repeated allocations, different commodities, differentiated entitlements, planned and completed stages, or inventories at different moments. There is no need to make every ratio a unit conversion or every spelling contrast an inflection.

The prediction of an allocation-template model would concern recurring amount tiers and exceptions across a linked administrative series, not a global scaling factor selected to accommodate a favorite identity equation. The current table is a discovery clue, not proof of any such series.

## 5. The unwritten participant may be the recordkeeper

A hypothetical note `X: 6; balance 4` is ambiguous to an outsider. In a storeroom whose staff share the same task, the direction might be obvious without writing it. The object type, custody, heading or route of a receipt may supply information we are trying to locate in a word ending.

This suggests reconstructing **document grammar** before demanding ordinary sentence grammar. Layout can distinguish a heading from an entry, one quantity category from another, and a subtotal from a row. That structure is not automatically the syntax of the spoken language.

If every proposed resource-flow arrow can be reversed without changing the observations, direction is not identifiable from those observations alone. But a well-supported network known up to reversal is still useful. A genuinely asymmetric physical or documentary anchor could orient a linked portion of the network. Orientation must not be propagated into unrelated document types merely for convenience.

## 6. Seals as acts of control, not name tags

Earlier research found shared-seal connections but could not equate the seal user, named designation and participant role. [S3]

The new question is functional: what does applying this seal accomplish? Preventing unnoticed opening, certifying a count, authorizing release and acknowledging custody are different actions. They predict different relations between the seal, the inscription and the holder of the document.

Administrative media should therefore be modeled as possible instruments of authorization or accountability, not only as containers of words. This does not revive the rejected rules that one seal identifies one person or one impression universally equals one commodity unit.

## 7. Revisions can reveal a procedure

Published scholarship describes erasures and reuse on Linear A clay tablets. [S6] A revision could correct a calculation, update an ongoing account, or recycle an unrelated record. These must be distinguished.

A potentially high-value pattern would be independently ordered changes in which an increase in one quantity is matched by a decrease in another while a reference stays fixed. That would constrain a complementary operation more strongly than a single static equality. Conversely, changing only a subtotal to fit unchanged entries would suggest recalculation rather than movement of goods.

HT34's erased seven does not itself establish that seven units were physically delivered. HT118's five-unit discrepancy does not justify inventing a lost transaction. Ordinary mistakes remain a rival; hypotheses about intermediate states need physical sequencing evidence.

## 8. Ritual inscriptions may make something enduring, not narrate the rite

The libation formula occurs on objects used in cultic contexts, including votive stone vessels. [S6] An inscription on such an object could be a dedication, claim of belonging, invocation, enduring commemoration or instruction. It need not transcribe what somebody said while pouring.

Possible, deliberately untranslated frameworks include `X dedicates this to Y`, `this belongs to Y`, and `may Y favor X`. The object itself can supply the referent of “this.” A fixed expression shared across objects may be a ritual formula rather than an identifiable deity's name.

A productive comparison would hold the sanctuary and object type as constant as possible and examine which slots vary with independently recognizable individuals, workshops or events. Variation by context should be separated from damage and scribal spelling.

## 9. Reopen morphology through recurring relations, not wishful restoration

Earlier failures concerned particular supposedly complete contrasts and weak identity bridges; they do not prove the absence of morphology. [S3]

A repeated alternation across several roots, tied to independently defined document positions and surviving hand/site controls, could support morphology before each historical referent is known. In ritual texts, coordinated changes in two separated slots could identify agreement or another grammatical dependency.

The point is not to assign `-NA`, `-ME` or any other ending a meaning now. It is to look for multiple constraints that converge on a rule. Broken tails must not be counted as optional suffixes. A formulaic register also cannot establish the default word order of the whole language by itself.

## 10. Visual combinations and approximate sound values

Salgarella's combinatory approach emphasizes that the construction of composite Linear A signs can itself carry information. [S7] Consequently, a feature treated as an affix in a flattened transcription might instead be a graphic qualifier or accounting adjunct.

Keep sign identity, spatial combination and approximate phonetic transcription as separate layers. Structural comparisons do not require choosing a language family first. Conversely, a tempting sound resemblance should not supply the accounting role that the context lacks.

## Synthesis

The leading conjecture is a small family of responsibility records: a recurring designation, an amount dealt with in the relevant way, an amount left in another status, and summaries at different levels. HT118's rounded paired sums provide one concrete exploratory reason to investigate this model. HT34 supplies a complementary-quantity constraint. The roster and seal findings suggest where social continuity and authorization might be encoded.

This account is not forced by the evidence. Its value lies in its sharper next question: **does a related record identify ten as the complete quantity behind QA-QA-RU's six and four, and does independent context distinguish what happened to the six?**

The first successful construction need not translate every word. It should make a prediction about another ancient writer's choice that its strongest rival would not make.

## Source record

- **S1 — INSCRIBE, University of Bologna, HT118 catalogue and model page:** https://www.inscribercproject.com/Clay_tablet_HT_118.php. Consultation in this brainstorm verified catalogue/transnumeration, not a new 3D reading. References GORILA I pp.200–201, Attili 1971 and Montecchi 2019.
- **S2 — Younger editorial commentary mirror, HT118:** https://raw.githubusercontent.com/mwenge/lineara.xyz/master/commentary/HT118.html. Transliterations and the previously noted main-total discrepancy.
- **S3 — Project:** `Linear_A_Review_Through_Iteration_16.md`, 12 September 2026, especially sections 1–3 and 5. This is an internal review, not an independent ancient witness.
- **S4 — Younger editorial commentary mirror, HT34:** https://raw.githubusercontent.com/mwenge/lineara.xyz/master/commentary/HT34.html. Edited erasure and pre-existing subtraction interpretation.
- **S5 — Project:** `Research Environment/iterations/010/notes/documentary_links.md`, especially the audited HT86/95 table and source-dependence notes. The earlier audit inspected GORILA I pp.134–135 and154–155; this brainstorm reused that audit rather than claiming a fresh plate reading.
- **S6 — Ester Salgarella, “Linear A,” accepted Oxford Classical Dictionary manuscript:** https://www.repository.cam.ac.uk/bitstreams/f6fd5b2a-3c52-4edd-856e-def4e71eb8db/download. Administrative reuse, document types, phonetic approximation and non-administrative supports. Relevant pages were read, including screenshots of PDF pages8 and10. Historical details above are distinct from this notebook's proposed workflows.
- **S7 — Ester Salgarella, “Mix and Match: A Combinatory (Re-)classification of Linear A Signs,” TALANTA54(2022), repository abstract:** https://www.repository.cam.ac.uk/items/d1c8c2dd-ee5b-4e61-9524-2c0eb5280eff. Only the repository abstract is relied upon here, not an unexamined full article.

## Reproduction

Run `python explore_ht118.py` with Python3.10 or newer. Only the standard library is needed. The output is `ht118_exploration_reproducible.json`. Its assertions check arithmetic, not translations. No ancient readings are modified and no missing quantity is inferred as zero.
