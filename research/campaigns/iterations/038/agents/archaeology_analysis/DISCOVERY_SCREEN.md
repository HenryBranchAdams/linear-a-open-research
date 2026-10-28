# Archaeology investigator: bounded fallback discovery

Campaign: 038. Date: 2026-10-21. Investigator: `/root/archaeology_analysis`.

## Scope fixed by lead

Find one potentially new administrative writing–object–event packet outside Flouda/Phaistos and parked A588, HT86/95, morphology, accounting, and ritual branches. Permitted evidence routes were original publications of inscribed roundels/direct sealings with observed erasure, marking sequence, or attachment, or a securely joined document with a controlled operational contrast. Two search batches maximum, no full deep investigation before selection. Controls read: B2026-10-18 CLAIM_DISPOSITIONS, RESEARCH_QUEUE, EXPOSURE_LEDGER, and relevant DO_NOT_REUSE entries.

## Search actually executed

Batch 1, system2, three queries:

- `Minoan roundel inscription erasure seal impression KH Wc`
- `Linear A roundels marking sequence inscription sealing stylus Khania`
- `Minoan inscribed sealing reused erased inscription roundel object`

Batch 2, system1, three queries:

- `"KH Wc 2123" erased`
- `"New and unpublished Linear A and Linear B inscriptions from Khania" Hallager`
- `"roundel" "erased" "inscription" Khania`

Scope is search-result discovery, not a complete corpus census. Six queries were attempted. Exactly one finite object packet was developed for screening: KH Wc 2123 plus its original edition and the later sign-committee objection. Generic roundel descriptions were excluded because they lack object-specific event discrimination. Malia impression-count and ZA Wc 2 results were recognized as previously qualified branches and not reopened. Other tablets mentioned incidentally in the original article were not admitted as candidates.

## Packet: KH Wc 2123 / Khania Museum 2123

**Primary edition:** Maria Andreadaki-Vlasaki and Erik Hallager (2007), “New and unpublished Linear A and Linear B inscriptions from Khania,” *Proceedings of the Danish Institute at Athens* 5, 7–22; target pp.13–15, fig.5.

- Publisher metadata: https://tidsskrift.dk/pdia/article/view/19622
- Publisher PDF: https://tidsskrift.dk/pdia/article/download/19622/17243/44600
- Web retrieval reference: `turn8view0`; target edition text at PDF page index 8, printed p.13.

**Reading dependency:** “Resolutions of the Comité des signes,” meeting 22 September 2021, published in *Ariadne Supplement* 5 (2025), printed p.586.

- PDF: https://ejournals.lib.uoc.gr/Ariadne/article/download/1875/1784/3540
- Web retrieval reference: `turn6view1`, PDF page index 7.

### Source observations inspected at screening

The edition identifies the complete roundel by museum inventory and dates recovery to 2003 in Geometric leveling fill. It reports an attempted erasure before nine impressions from one seal, with nine fingerprint pairs. Its full transcription is erased: `[[A 373 , AB 39-77 (PI-KA)]]`. PI-KA is read confidently; the birdlike first sign and its ideographic status are proposed. [Edition p.13.]

The committee later deferred A373 because it lies on an erased surface and the photograph and drawing appear inconsistent. The expectation of an ideogram on a roundel was discussed, not established as independent identification. [Minutes p.586.]

### Access scope and correction

The complete primary PDF was accessible through the web retrieval tool, but only the target p.13 extracted text was deliberately inspected at this screening stage. Fig.5 and target pp.14–15 have **not yet been visually inspected**. The committee paragraph on p.586 was read. This is not an object autopsy or a complete article audit.

Initial discovery snippets could have suggested replacement of a sign group while retaining a new/older category sign. Original-source inspection corrected that possibility: the edition encloses the **entire** proposed transcription in erasure brackets. No replacement inscription is established by the inspected passage.

Direct local PDF acquisition via Python was attempted and failed because sandbox network access was denied (`Operation not permitted`); this is an implementation/access-route failure, not evidence that the sources are unavailable. No escalation attempted at screening. Failed acquisition manifest is in `raw/download_manifest.json`. A follow-up web `open` returned HTTP503 after the first successful text retrieval; preserve the successful inspection record and do not redescribe it as full access failure.

## Candidate admission record

| Field | Screening finding |
|---|---|
| Target | KH Wc2123, museum 2123, obverse erased inscription, especially AB39-77; nine rim impressions. |
| Decision potentially changed | Whether visible text and present impressions can be treated as one unchanged, contemporaneous administrative label-event relation. |
| Stable features | Exact object identity; published erasure; PI-KA survives according to edition. Physical phase inference needs figure inspection. |
| Consequential alternatives | First isolated mark A373 versus insufficiently identified traces; an attempted erasure can be cancellation, correction, or reuse. |
| Serious rival 1 | The visible written label was current and unchanged when present seal impressions were made. |
| Serious rival 2 | The visible label belongs to an earlier marking phase and was intentionally altered before stamping. |
| Observable difference | Compression/closure of inscription strokes by smoothing and spatial/physical relation to later impressions could support sequence 2. The source presently asserts this; images remain unchecked. |
| Independent relation | Stroke/smoothing/impression stratigraphy can be assessed without assigning a meaning to PI-KA or A373. |
| Semantic limit | Even a secure sequence does not distinguish responsible party, recipient, account, or commodity; deliberate erasure need not have successfully removed the text's administrative force. |
| Evidence route | Accessible original edition fig.5 and pp.13–15, checked against committee's photo/drawing objection. |
| Exposure | Absent from the relevant controls checked, but the exposure ledger is not exhaustive; prior project exposure UNKNOWN, not certified unseen. The source article was indexed in Younger's updates long before this campaign. |
| Method | Compare original prose/photo/drawing for exact phase evidence; keep lifecycle sequence separate from motive and role. No numerical test is warranted. |
| Stop | Failure to verify sequence; unresolved target reading; or absence of an independent role/category link after this finite packet. |

## Ranking recommendation

This packet has unusually explicit marking-order evidence and a complete object, but weak prospects for semantic discrimination. Recommend it only for a bounded physical/reading inquiry if no stronger packet is found. Do not admit a category-replacement semantic test: the assumed replacement is unsupported. No existing parked semantic claim is reopened by this screen.

The strongest surviving semantic alternatives would remain former or intended recipient, responsible party, institutional account, or object category. Any could be erased before a later stamping operation. A newly established material order would constrain the use of the text as evidence, rather than translate it.

## Next executable action if selected

Inspect the source's fig.5 and pp.13–15, identify which trace establishes erasure-before-stamping, and determine whether the later committee objection affects only A373 identification or also the phase argument. If no observable phase evidence can be independently checked, retain the edition's statement as reported, mark the visual verification limit, and stop.

## Completed follow-up

The lead subsequently assigned a bounded exact-index/figure audit. Fig.5 was obtained and visually inspected; its full-erasure transcription was confirmed, but a decisive erasure–stamping crosscut was not independently verified. The frozen index already contains `KHWc2123` as `*810-PI-KA` without erasure markers or separated first component. An explicit global `*810 → A373` mapping was not established. `RAW_INDEX_AUDIT.md` preserves the row, codepoints, provenance, current image-access status, and unchanged semantic gate decision. This follow-up adds no new candidate packet.
