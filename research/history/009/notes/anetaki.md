# Anetaki pivot: a new textile context, then a conditional accounting test

The newly available material supplies a cloth-associated **KA** adjunct, not an identifiable giver or verb. I retrieved the primary Anetaki overview, visually inspected its principal object photograph, followed its textile connection into a newer study, and executed an uncertainty-sensitive test of HT24. The sentence goal remains unmet on this branch.

## What the new inscriptions actually provide

**KN Zg57**, an ivory ring, and **KN Zg58**, an associated handle, are separate inscription carriers. The ring has no reported numerals; the handle has numerals and fractions, and the editors distinguish their hands. The ring's faceC includes **AB54+77**, conventionally cloth+KA. An **A+KA** composite occurs with A above KA on the ring and below KA on the handle. This is variation in graphic layout, not an attested reversal of a spoken word. Full sign-group transcriptions are absent from the preliminary publication. The damaged hide adjunct on faceD has **KA/QE/KO** alternatives, so it cannot be counted as secure hide+KA. [Kanta et al., pp34,39-41](https://ejournals.lib.uoc.gr/Ariadne/article/view/1841).

Nosch and Weilhartner connect the cloth+KA to two competing possibilities: a technical designation associated with purple, or the **A/JA+KA** composites known in textile contexts. This is a published comparison, not a new decipherment. The broader evidence makes a textile interpretation worth testing but does not identify the modifier's meaning. [The Common Thread, pp129-131](https://www.academia.edu/145903263/The_Common_Thread_Textiles_and_Wool_Logograms_in_Linear_A).

| Witness | Published expression | Separate context |
|---|---|---|
| KN Zg57 C | AB54+77 | Textile logogram with KA endogram |
| HT24 b.2 | JA+KA *118 1 | Other face contains wool-associated signs |
| HT38 .2-3 | KA+A *118 3 | Adjacent textile logograms; mixed inventory |

The common *118 following both composites helps constrain their administrative category. It does not establish that they denote the same commodity, still less the same person. [Del Freo2020, p58 n18](https://openportal.ispc.cnr.it/data/2020/421681/2020_421681.published.pdf); [HT38 edition derivative](https://raw.githubusercontent.com/mwenge/lineara.xyz/master/commentary/HT38.html).

## Executed test: does HT24 rule out a different ME unit?

Del Freo discusses **ME** as commodity quality or processing stage, partly because of a proposed wool-unit balance. I checked the original p55 uncertainty coding: **ME beside6 is doubtful**, as is ME in the broken fourth-line entry. The secure ME-marked quantity is **10[**. The recoverable numerical marks sum to31½; several boundaries are broken. The reverse gives1¾+1¾+1 under the proposed fraction values; with a10:1 conversion this corresponds to45. This balance, associated with45 nearby noduli, remains conditional. Del Freo already identifies fractional quantities as a difficulty for a direct unit-token allocation. [Original publication, pp55-59](https://openportal.ispc.cnr.it/data/2020/421681/2020_421681.published.pdf).

Del Freo's wording is qualified: a different unit is difficult to interpret, and quality or processing seems more likely (p58). I test the stronger, often tempting inference that the arithmetic *excludes* a different unit; this is not an assertion that the author made an absolute claim. **The fixed45-input model requires lossless equivalence, no additions and unchanged conversions; merely sharing a batch does not establish those conditions.** My test treats ME as a hypothetical multiplier and asks whether even the surviving amounts exceed45. It preserves the difference between secure, tentative and restored ME occurrences.

| Reading scenario | If ME multiplies by2: minimum mass | Verdict under lossless45-total assumption |
|---|---:|---|
| Only the secure10 is ME-marked | 41½ | Numerically possible;3½ remains |
| Include ME? beside6 | 47½ | Exceeds45 before missing entries |
| Restore ME throughout | 63 | Exceeds45 |

This is a concrete sensitivity result: **the doubled-unit rejection depends on the tentative sign and on lossless equivalence**. It does not follow merely from the proposed total. A half-unit interpretation also survives these lower-bound tests; positive residuals establish numerical compatibility only, not epigraphically valid restorations or historical plausibility. The exact maximum multipliers are47/20,59/32 and10/7 respectively. They are necessary bounds under the lossless model, not estimates of ME's meaning.

A separate executed test allows processing: `output = yield × input`. With47½ minimum input and45 output, yield could be at most **18/19**; at the surviving lower bound, loss of **1/19 ≈5.263%** removes the contradiction. Positive missing input requires more loss. This is an algebraic alternative, not observed ancient wastage. It also loosens a direct assignment of45 noduli to45 standard *input* units. Del Freo's discussion of substantial raw-wool preparation loss concerns his Mycenaean comparison (p61), while p62 n49 distinguishes spun-to-woven scraps and possible return of scraps. Neither provides an actual yield for HT24. [Del Freo2020, pp61-62 n49](https://openportal.ispc.cnr.it/data/2020/421681/2020_421681.published.pdf).

I then inspected the actual [GORILA I p42 photograph/drawing](https://cefael.efa.gr/detail.php?site_id=1&actionID=page&serie_id=EtCret&volume_number=21&issue_number=1&sp=78&max_image_size=1) and [p43 apparatus](https://cefael.efa.gr/detail.php?site_id=1&actionID=page&serie_id=EtCret&volume_number=21&issue_number=1&sp=79&max_image_size=1). The available scan is150dpi. The doubtful adjunct lies at damaged surface; the partial drawn strokes do not license upgrading ME?. The6 has six drawn strokes, while10 approaches a damaged right-hand zone. SigLA calls the entire composite A561 certain, but that coarse encoding does not negate GORILA's component-level uncertainty. No new reading resulted; the test stays conditional.

For the ordinary multiplier1, unpreserved quantities and numeral extensions together must contribute13½. They should not be allocated automatically to only the two fully lost entries. Simple mean imputation yields47¼, so45 is not recovered by arithmetic averaging alone.

## Consequences and next discriminant

We have gained a stronger commodity context for **KA** and an exact condition on one attempted **ME** interpretation. We have not recovered a source, recipient or action. Both a receipt account and a stock/production schedule can preserve the same numbers. The proposed suppliers and workshop relationship in the literature are contextual reconstructions.

The smallest immediate discriminator is improved imagery of **HT24a ME? beside6**, together with an independently constrained total. For the broader Anetaki route, we need the full sign-group edition and all-face plates before treating ring/handle association as parallel wording. Searches for the final publication located forthcoming references, not an inspected final edition. Publication priority is not claimed for this calculation; the45-unit and fractional-nodulus arguments are already published.

Reproduce with `python analysis/anetaki_textile_test.py`. Inputs and dependencies: `notes/anetaki.json`; exact results: `results/anetaki_textile_test.json`. Only Python's standard library is required.
