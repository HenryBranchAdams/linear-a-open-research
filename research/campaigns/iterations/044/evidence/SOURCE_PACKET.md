# C044 source packet: HT31, ceramic production and the first vessel sign

Source investigator: `/root/linked_records`. Prepared 2026-10-25/26 UTC. This records observations and dependencies for lead adjudication. The frozen campaign decision is in `iterations/044/BRIEF.md` in the canonical project.

## What changed during inspection

The first reconnaissance found a ceramic tripod cooking-pot waster from the Haghia Triada kiln. That is a serious check on a generic inference from three supports to metal. Following the original citation chain revealed that the published argument is more specific: Duhoux acknowledges ceramic tripods and points to the **length and thinness of the supports**. Vandenabeele compares the complete combination of a rounded basin, upright handles and straight supports with an independently excavated bronze vessel. C044 must assess that stronger argument. It would misrepresent the literature to say that the ceramic waster alone refutes it.

## Source chain and access

| Source | Exact inspected evidence | Access and source dependence |
|---|---|---|
| Pietro Militello 2011, *La fornace da vasaio TM IB di Haghia Triada. Una riconsiderazione della tavoletta HT31*, Creta Antica12,273–288 | Selected text273–285; actual pixels274fig1,275–276,278,280,284 | Full16-page institutional PDF acquired. Figure1 reproduces GORILA; discussion follows Duhoux and Vandenabeele. It is not a new autopsy of HT31. |
| Dario Puglisi 2011, *La fornace da vasaio TM IB di Haghia Triada. Le ceramiche e il sistema di produzione, distribuzione e consumo*, Creta Antica12,199–271/272 | Public author HTML/OCR:200–205;213–215;222–225;253,255–256;269. Catalogue5.3/c.29a1 and context 5 are the exact targets | Full article text accessible through the indexed author page. Current directly fetched page has unavailable/login preview. Institutional PDF is explicitly private. No original figure8c/34 pixels acquired. Final page range disagreement remains bibliographic, not a specimen ambiguity. |
| Yves Duhoux 2000–2001, *Un inventaire linéaire A de vases: la tablette HT31*, Minos35–36,31–62 | Selected text31–43,59–60; decisive39–40, selected layout/reading33–37 | Full32-page publisher PDF acquired. Features and proportions depend on Vandenabeele's photographs. No independent object replication. |
| Frieda Vandenabeele 1974, *Les idéogrammes de vases sur les tablettes en linéaire A de Haghia Triada et Phaistos*, BCH98.1,5–21, DOI10.3406/bch.1974.2094 | Actual page images and text6,8–10,17–18,21. Fig1 whole tablet; fig2 HT31.1 photograph and drawing; fig21 bronze comparator | Full-PDF download returned403; explicitly linked public page-view images acquired. Published photographs by J.-P.Olivier; bronze photograph supplied by J.-Cl.Poursat. Local images are 710px page previews; not new physical examination. |

Local source identities and hashes are in `SOURCE_ACCESS_LEDGER.json`. Vandenabeele page-level URL/hash details are additionally preserved in `sources/Vandenabeele1974_acquisition.json`.

## Fixed identities and the independent observations

HT31 is the inscription target. Its first vessel is conventionally **A410VAS** in GORILA/Militello; **LA545 / VASd1** in the Raison–Pope/Duhoux notation. These sign-number namespaces are retained. A410 is not A411: Militello273 discusses A411 separately among Chania roundels.

Puglisi's **catalogue 5.3 = excavation c.29a1** is a ceramic fragment. Context5 denotes material from the firing-chamber area; c.29a is from around the first pillar, while c.30c is from cleaning the first eastern channel. Those boxes are not merged. The catalogue describes a wall with half a horizontal cord handle, cylindrical body and completely blackened cooking fabric. It classifies the object as a tripod cooking-pot waster. Neither legs nor a complete profile survive in the description. General overfiring criteria are discussed on213; the production attribution is the author's examination, not a new laboratory result. Fig8c is on215; the object photograph in fig34 is on256, still uninspected here.

Vandenabeele's bronze counterpart is **Malia, Quartier Mu, inventory 3068**, fig21. It is a distinct object, not an HT kiln product. The report places three bronze vessels below a small storeroom floor, discovered1969, dated no later thanMMII. The rounded basin, three upright semicircular handles and straight, square-section riveted supports are reported on9 and visible in the published photograph. HT31 is later. The comparison does not establish continuity of one administrative institution or one particular vessel.

## Morphology matrix

| Feature | HT31.1: photograph and published drawing | Malia3068 bronze: photograph/report | Puglisi5.3 ceramic: catalogue only |
|---|---|---|---|
| Body | Shallow, curved basin | Rounded basin | Cylindrical surviving wall; no complete profile |
| Handles | Two upright loops above rim | Three upright semicircular loops | Half horizontal cord handle |
| Supports | Three long, narrow incised strokes below basin | Three long, straight supports | Not preserved in catalogue description |
| Material cue | No direct surface/material observation from the pictogram | Physical bronze vessel, reported identification | Cooking clay, reported overfired/waster |
| Relation to kiln | No exact joined batch | None asserted | Exact kiln-context catalogue identity |

The matrix discriminates a specific morphological match from membership in the broad class of tripod vessels. A schematic line's width is not a measurement of an ancient vessel's leg cross-section. Conversely, schematic rendering does not make the complete combination of features irrelevant. No statistical score or unrecorded tolerance is imposed.

## Reading, segmentation and scope alternatives

Militello275–276 preserves the following consequential uncertainties:

- **PU-KO scope:** part of the heading with I-TI-SA, or a descriptor of the following tripod. The suggested bronze gloss is conditional on the second segmentation and on the material inference; it supplies no independent confirmation of either.
- **Rows3–4:** SA-JA-MA has a following numeral, but KI-DE-MA-…'s following numeral and the section's uniform vessel semantics are less secure. Treat row4 as uncertain, not a guaranteed inventory item or subheading.
- **Ligatures:** vessel names and vessel characteristics remain alternatives. Militello does not accept a rigid parallelism as sufficient to exclude descriptive terms.
- **Damaged amounts:** the first vessel's number is lost; the surviving5 after the lacuna is not automatically its count. SA-JA-MA30/20 and row5 vestigia are retained as reading alternatives. No integer-fit inference was run.
- **Source notation:** Militello's transcription275 gives KI-DE-MA-A323-NA, while prose276 prints A326. Neither is silently normalized into a settled reading. The present test does not depend on that sequence.

Duhoux33 reports that the supposed sign above/between the tripod's handles is absent in an enlargement shown to him by Olivier: two tiny stones explain the earlier reading. This is a reported high-magnification observation; the present710px page image cannot independently resolve the tiny marks. The first vessel therefore supplies no secure ligature functioning as an independent material label. Duhoux35 likewise allows both PU-KO scopes.

`HT31_RAW_ROW_OVERLAY.json` preserves the frozen row without normalization. Its initial transliteration is **TI-SA**, paired with **𐝫𐘠𐘞**; the editions' **I-TI-SA** is recorded separately. `*410-VS` occurs only in HT31 under an exact-token scan of this 1,721-record snapshot, a statement about this encoding only. The overlay retains all damage, PA₃ versus *56 conventions, vessel-number namespaces and the A323/A326 discrepancy. The reproducible extraction is `audit_ht31_snapshot.py`; no canonical corpus bytes were changed.

## Exact event relation and administrative interpretation

Militello274–275 assigns HT31 approximately to the1903 Room59 group, via inventories and excavation diaries. It is not a findspot in the kiln, an attached production tag, a named consignment, or a physically joined counterpart. Puglisi's kiln deposits also include collapse, redeposition and dump material; ceramic production evidence need not be one firing load. The studies support contemporary local production and morphological comparisons, but their proposed order, issue, receipt or banquet relationships require additional inferential links.

The lead may assess a local material/type preference for A410 from the independent bronze comparator. Extending that preference to the whole document requires the explicit premise that every listed item is the product of the same ceramic installation. A broader acquisition/allocation list could incorporate ceramic products and a bronze vessel. It need not be a warehouse census, and no flow direction or participant role follows.

## Access closure and next useful observation

The exact missing target is **Puglisi 2011 printed215fig8c,255catalogue 5.3,256fig34**, preferably the original PDF or a supplied scan, and any complete same-class ceramic form used in reconstructing5.3. No message was sent. A generic second tripod does not change the comparison: the useful ceramic evidence would preserve the upright loops, rounded basin and long thin supports in combination. A directly joined kiln/dispatch/account record would change the administrative comparison more than additional quantity fits.

## Source URLs

- Militello: https://www.iris.unict.it/retrieve/dfe4d227-4871-bb0a-e053-d805fe0a78d9/Creta%20Antica%2012,2011%2009%20MILITELLO.pdf
- Puglisi public author text: https://www.academia.edu/504733/La_fornace_da_vasaio_TM_IB_di_Haghia_Triada_Le_ceramiche_e_il_sistema_di_produzione_distribuzione_e_consumo
- Puglisi restricted institutional record: https://www.iris.unict.it/handle/20.500.11769/560369
- Duhoux: https://revistas.usal.es/dos/index.php/0544-3733/article/download/16424/17038/56788
- Vandenabeele: https://www.persee.fr/doc/bch_0007-4217_1974_num_98_1_2094
