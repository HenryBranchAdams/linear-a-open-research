# What Prinz's decipherment work teaches our Linear A project

Research note · 2 October 2026

## Assessment

There are useful, concrete lessons here. The strongest is to organize AI around a constrained reconstruction task, give it tools for the actual obstacle, and demand evidence that can distinguish a correct answer from an attractive one. His examples justify taking AI-assisted archival decipherment seriously. They do not yet demonstrate recovery of an unknown ancient language.

This review recovered Prinz's technical X thread, read his two WWI case studies, checked the relevant published ship-log transcription, and inspected two related public research repositories. The History Lab URL returned its title and description but did not expose the letter viewer or complete transcriptions through the available retrieval routes. Accordingly, this is a study of the documented approach, not a character-by-character certification of the 1593 letters. A further extraction attempt was blocked because the connected Firecrawl account had insufficient credits. No paid upgrade was made. Public verification code was identified but not executed.

## What his accounts actually establish

### The 1593 letters

Prinz says the cipher key was already available. Each ordinary symbol could represent two letters; missing spaces, hurried handwriting, historical French spelling, and special name/word symbols complicated reading. He describes an initial model pass, a second model for the unresolved remainder, and a custom app through which he helped inspect difficult signs. His percentage-complete figures are self-reported, not independently measured here. A follow-up says another researcher separately deciphered the letters, but that is not a substitute for comparing their readings and disagreements. [S1]

The methodological value is the division of labor: let the model handle broad reconstruction while making the residual visual uncertainty inspectable. The post does not disclose enough to reconstruct his exact prompts, app implementation, trial count, or validation protocol.

### The WWI examples

For RICHI-170, Prinz reports using a documented key outside its expected date range. The resulting German refers to a cruiser and a following allied squadron at Sevastopol, with one damaged or anomalous date character retained. [S2] The published HMS Canterbury log transcription records arrival on 24 November 1918 and an Allied Squadron on 26 November, corroborating those events. I checked those entries; I did not perform a fresh palaeographic reading of the scans. [S4]

For RICHI-240, he reports searching published keys and possible placements of twenty missing cipher symbols, scoring outputs for German patterns, then using historical evidence to complete ambiguous unit numbers. [S3] This distinction matters: historical information used to choose a completion contributes to that reconstruction; it cannot also count as an untouched test of the same completion.

A separate public repository explicitly credits Prinz's RICHI-170 key finding and describes reproducible decryption, error searches, and negative results. Its README strengthens the case that this is mechanically testable work, while leaving execution verification outstanding in this review. [S5]

## Why the transfer to Linear A needs care

The cipher examples have unusually powerful anchors: a known language, known or documented keys, and historical records close to the events. A candidate can be checked against a precise encoding rule. Even a many-to-one cipher can be checked for whether each proposed plaintext character is allowed by its recorded symbol.

Our project has a different set of anchors: recurring sign sequences, numerical relations, layouts, archaeological contexts, and qualified cross-script comparisons. Our recovered research still does not establish an independently supported action and participant-role construction. The review through iteration 16 retains the HT34 complementary-quantity result, the probable QA-QA-RU name comparison, and several administrative structures while identifying unresolved direction and scope. [P1]

Thus we should borrow the disciplined search and inspection workflow. We cannot transfer the ability to score a solution by how naturally it reads as French or German. In Linear A, rewarding fluent English risks selecting the model's narrative rather than the ancient text.

## Six practical changes worth adopting

The recommendations below are this review's proposals, not claims that Prinz already implements all of them.

### 1. Diagnose the obstacle before another research run

Assign each target one principal obstacle: sign identity, segmentation, relation between forms, numerical scope, semantic direction, or external corroboration. Then choose a tool that addresses it.

For ZA 9, if the decisive issue is the surviving stroke after A-TA-NA, more semantic speculation cannot supply the missing surface. A useful next result would be a better image or a discriminating sign comparison. If no new surface evidence is available, keep the alternatives live and move effort elsewhere.

### 2. Make a workbench for inspecting evidence

For each contested position, show the original photograph, edition drawing, sign crop, nearby secure comparison signs, competing readings, and the claims affected by the choice. Preserve edition, page, object, and image provenance.

Selecting TE rather than TI should immediately reveal which analyses change. An unreadable mark must remain selectable as unresolved. Avoid generative sharpening that invents strokes; retain the original pixels and label display transformations. A human or model judgment should record its basis, rather than silently overwriting the transcription.

The first workbench targets should be a small set of consequential ambiguities, not every sign in the corpus. ZA 9 and the critical state and scope of HT34/HT118 are candidates already identified by our audit. [P1, P3]

### 3. Search explicit alternatives and keep the cost of each visible

Represent a candidate as a bundle of choices: sign readings, boundaries, restorations, grammatical rules, and meaning assignments. Mark what is observed and what is supplied. Give arbitrary exceptions and unsupported restorations an explicit cost rather than allowing them to rescue a favored translation for free.

For IO Za 2 and IO Za 6, LA-H005 already records the recurring TA-NA…U-TI-NU frame and unresolved segmentation. [P2] Compare whole-form, compound, and affix analyses using the same retained witnesses. A useful outcome could be the elimination of one segmentation; it need not immediately identify a deity or verb.

### 4. Turn every promising rule into a prediction

Before inspecting the evaluation material, record what the rule predicts: a sign, a quantity, a distribution across positions, or a relation between entries. Compare it with simple competing rules.

Split by ancient object or genuinely independent document group. Two faces of one tablet, two editions of one inscription, or near-duplicate formulae cannot casually be treated as independent tests. Previously reviewed material is a consistency check, not a fresh holdout. Model pretraining exposure is another reason to prefer executable constraints and genuinely new observations over verbal recall.

For grammar, the closest counterpart of checking a cipher is whether the same frozen rule accounts for all secure signs and predicts another occurrence without added exceptions. That will usually be weaker than exact cryptographic validation, but stronger than a plausible English sentence.

### 5. Give historical context two different jobs

Context can generate a hypothesis or test one. Record which it did. If a ritual setting suggested an offering interpretation, the ritual setting is not independent confirmation of that interpretation.

A useful test for Schümann's proposal would ask whether his sign assignments and grammatical rules, fixed in advance, work on other complete inscriptions. Keep reconstructed I-DA-MA-TE separate from surviving signs, and compare readings with alternative ritual functions. Our earlier correspondence identified this audit as a gap; this note does not perform that audit.

### 6. Calibrate the whole workflow on problems with recoverable answers

Use a small benchmark of edited Linear B records and synthetic account systems. Hide selected information, inject declared ambiguities, and measure recovery of structure, quantities, and roles separately. Include cases deliberately lacking enough evidence, where abstention is the correct result.

Renaming signs does not remove every clue or eliminate training contamination. Synthetic examples are useful for testing the software; known-language controls are useful for checking practical behavior. Neither demonstrates Linear A decipherment. Their purpose is to detect a procedure that produces confident stories even when the answer cannot be identified.

## Recommended next experiment

The highest-value adoption is a small, source-linked comparison workbench plus a frozen prediction test. Begin with the known IO Za 2/IO Za 6 structural comparison, because it connects directly to the newly raised interpretation. Do not start by fitting an entire English prayer.

Deliverables for that experiment:

1. An aligned transcription preserving damage, word dividers, face boundaries, and editorial disagreements.
2. A table of alternative segmentations and their explicit assumptions.
3. A rule inventory showing which observations each candidate explains and which it leaves unresolved.
4. A declared evaluation set, with previous exposure and source dependencies recorded.
5. Results against simple rivals and suitable shuffled controls; a failed prediction remains a result.

Success would be one reproducible constraint that favors an analysis over a real competitor. Establishing action or deity meaning would require additional independent evidence. The workbench and experiment are recommendations from this review, not completed implementations.

## Relation to our existing work

We already have claim registers, counterexamples, source audits, and executable analyses. The opportunity is to connect those controls more tightly to visual evidence and to make model exploration produce testable candidate rules. The iteration-16 review also found that passing tests did not necessarily validate the intended assumption: changing the erasure status left the calculation unchanged. [P1] Any new workbench should propagate source-state changes through the analysis, rather than merely display a reassuring validation label.

A related research repository documents archival discovery, explicit prior-art corrections, small solvers, and matched controls. It is a separate project; I did not establish that its owner is the person Prinz mentioned on X. It is useful as an additional example of reporting unresolved cases and distinguishing newly decoded material from old solutions found in print. [S6]

## Sources and scope

- **S1 — Prinz's technical thread**, 2 October 2026: https://x.com/deredleritt3r/status/2106067484084166835 . Retrieved with its surrounding thread, including the follow-up at https://x.com/deredleritt3r/status/2106088561715851415 . Primary account of his process; completeness claims not independently audited.
- **S2 — Prinz, RICHI-170 case study**, 17 September 2026: https://www.prinzai.com/p/gpt-6-astra-solves-a-wwi-german-radio . Primary public explanation; complete original model transcript not inspected.
- **S3 — Prinz, RICHI-240 case study**, 19 September 2026: https://www.prinzai.com/p/another-wwi-german-radio-cipher-falls . Primary public explanation of missing-symbol search and context-assisted reconstruction.
- **S4 — HMS Canterbury log transcription**, November 1918 entries: https://www.naval-history.net/OWShips-WW1-06-HMS_Canterbury.htm . Edited transcription linked to original log scans; checked 24 and 26 November.
- **S5 — 0wwafa/adfgvx-1918**: https://github.com/0wwafa/adfgvx-1918 . README inspected; source code not executed here. Independent author's verification claim, not this review's replication.
- **S6 — dbourdeau/cyphersolver**: https://github.com/dbourdeau/cyphersolver . README and indexed target descriptions inspected; separate research project, not attributed to Prinz.
- **Access-limited site — History Lab**: https://prinzai.com/history-lab/ . Title and description accessible; full letter viewer unavailable through retrieval in this run.
- **P1 — Project, Linear_A_Review_Through_Iteration_16.md**, 12 September 2026. Read earlier in this conversation. Critical cumulative review; not an independent ancient witness.
- **P2 — Project, registry/historical_claims.json**, LA-H005. Inspected earlier in this conversation. Explicit IO Za 2 / IO Za 6 comparison and unresolved segmentation.
- **P3 — Project, round-9 REPORT.md**. Read earlier in this conversation. Source-critical ZA 9 audit and alternatives.

No research-register dispositions or historical transcriptions were changed by this methodological review.
