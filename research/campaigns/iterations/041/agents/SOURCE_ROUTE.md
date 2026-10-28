# C041 source route — Nikolakopoulou2019, Akrotiri9384 /9730

**Investigator:** `/root/source_route` · **Date:** 2026-10-23 · **Disposition:** new full-source access achieved; catalogue/object controls improved; no sample-to-target binding recovered in the inspected concordance.

## Actual access change

Both complete volumes were recovered from the **publisher's openly linked PDF collection**. This changes the C040 state, which had not inspected the underlying catalogue/fabric study. It is not a new host for the already-read2025 paper, nor a new ancient witness.

- **C041-S01:** Irene Nikolakopoulou2019, *Akrotiri, Thera: Middle Bronze Age Pottery and Stratigraphy*, I, BAE318. [Publisher PDF](https://www.archetai.gr/images/pdfs/bae/BAE_318.pdf).561PDFpages;73,120,857bytes; SHA256`0ccd138b1b2fd2885f22516573e08ab373cf338c5bdc28d7256ffe64ccc50b52`.
- **C041-S02:** same work, II, BAE319. [Publisher PDF](https://www.archetai.gr/images/pdfs/bae/BAE_319.pdf).633PDFpages;36,676,561bytes; SHA256`3a9a22ab23de0e939a6e3153907300948c45effcee20942af973a3981b34ee73`.

Exact publisher link provenance: the public [BAE collection page](https://www.archetai.gr/index.php?id=19&lang=&p=content&section=1) contains explicit HTML anchors `../../../../images/pdfs/bae/BAE_318.pdf` and `../../../../images/pdfs/bae/BAE_319.pdf`. Its HTML is retained as `raw/source_route/publisher_catalogue.html`; no systematic guessing of hidden file IDs was used. Search independently surfaced319;318was followed from the actual publisher anchor. Normal HTTPS transfers succeeded without credentials or bypass. Generic web extraction rejected319because its36.7MBsize exceeded that tool's limit, which was a tool limit rather than a publisher denial.

Local files and extracted text are under `raw/source_route/`. Both volumes have a cover ahead of normal pagination: for the target pages, **printedpage+1 = one-basedPDFpage**. Acquisition does not imply exhaustive reading of1,194pages.

## Exact source controls recovered

| Control | Primary locator | Result and limitation |
| --- | --- | --- |
| Carrier concordance | II258, entries1121/1122; II609concordance | **1121=AIN9384**, ceramicgroups67N039–044; **1122=AIN9730**, group67N044; both67N,PhaseC. This crosswalk is independent of the marks. |
| Original photographs | II259, pl121 | Overall vessels and mark closeups explicitly linked to1121and1122. Same objects as C040's2021/2025figures, not additional witnesses. |
| Profiles/preservation | II543, plLVII |1121has substantial restored full profile;1122preserves upper fragment, with hypothetical/missing outline shown by broken lines. These drawings do not establish its total capacity. |
| Coarse form | I203, G10 | Hole-mouthed jar; incurving rim, piriform body, opposing raised handles. The catalogue groups both despite differing measurements/preservation. |
| Dimensions | II258 |9384height29.5cm; rimouter15.6/inner15.1cm; restoredbase11cm.9730preservedheight15cm; rim14.5cm; rimthickness0.9cm. Its rimmeasurement is not explicitly labelled inner/outer. No second capacity measure is present. |
| Mark descriptions | I203; II258 |1121trident between handles;1122rectanglewithopposingarcs at handlelevel. Code-independent graphic contrast retained. |
| Reading qualification | I220 |2019treats1121's trident as partly preserved and possible AB9/AB27comparisons as vulnerable;1122is identified withAB164. Later2021/2025read1121asAB81. Preserve history and uncertainty rather than silently rewriting2019or treating each suggestion as equally secure. |
| Completeness classification | I220 versus Michailidou2025printed13 |2019describes isolated pictorial marks, excluding a longer inscription;2025allows a lost following sign at9384's restored join. This source difference must remain explicit. |

The numerical measurements refine C040's rounded same-size description. They do **not** show a matched two-vessel volume comparison; differing inner/outer conventions also prevent a clean new test of equal mouth size. This is a control correction, not evidence for a contents reading.

## Hilditch fabric inquiry

Target chapter: J. Hilditch, “Fabrics and Technology: Phases B–C,” I377–470. I378states that93catalogued whole/reconstructed vessels were macroscopically grouped. That fact alone does not bind a fabric sample to either target.

**Consequential table checked as actual pixels:** Table3.23, I458–461(one-basedPDF459–462), concordance of sample numbers, contexts, macro/microgroups, firing, shapes, surface treatment and catalogue numbers. All four printed table pages were rendered at200dpi and visually inspected; OCR was used only as a secondary locator. No visible catalogue-cell1121or1122was recovered. The table includes67Ncontext material and other catalogue numbers, but sharedcontext or a generic hole-mouthed-jar entry cannot substitute for the target crosswalk. In particular, sample105's67NStr12hole-mouthedjar row explicitly points to catalogue**1196**, not1121or1122; this near-match was rejected as a targetjoin.

The printed table itself jumps from sample119to128across pp459–460 and repeats185across pp460–461. These are visible publication boundaries, not missing `pdftotext` rows. Preserve the gap; it prevents a broad statement that no target could ever have been sampled. Blank catalogue cells likewise do not prove absence of a target among unnamed samples.

**Bounded macroscopic check:** I379–396group-description text was searched for9384/9730and1121/1122; no directtargetidentifier was recovered. Actual pixels were inspected for I379's method/template, I380Table3.13, I383groupdescription, I396summary, I397–399macro-photographs, I400Table3.14and I401–402summary/microscopic-sampling transition. Table3.13contains counts by fabricgroup/pillarpit, not individual targetassignments; Table3.14likewise aggregates provenance by pit/phase. Photographic examples on397–399lack targetinventorylabels. These inspected materials do not supply a targetjoin.

The complete chapter remains available for future defined source comparisons. This report does not claim every caption, image or sample has been exhaustively adjudicated. In particular, a completed laboratory-record crosswalk would need an exact independent path from sampleID to catalogue1121/1122or AIN9384/9730. The preserved published data still allow the narrower conclusion: **no direct fabric-sample binding for this pair was recovered in the specified inspected packet**.

## Other routes actually checked

1. [Publisher volumeI metadata](https://www.archetai.gr/index.php?id=65&lang=&p=content&section=8): title, series and ISBN only; no full-text link on that individual page. It led through the publisher's series collection to explicit PDFs.
2. [Author's Academia books listing](https://culture.academia.edu/IRENENIKOLAKOPOULOU/Books) and [record38811739](https://www.academia.edu/38811739/Akrotiri_Thera_MBA_pottery_and_stratigraphy_Vols_I_II_The_Archaeological_Society_at_Athens_Library_Series_Nos_318_319): rendered title/frontmatter/contents for both volumes; not relied on as fullbookaccess.
3. [ResearchGate record334965534](https://www.researchgate.net/publication/334965534_Akrotiri_Thera_Middle_Bronze_Age_Pottery_and_Stratigraphy_Volume_I_Stratigraphy_Ceramic_Typology_and_Technology_Weaving_Equipment): author-uploaded material, but inspected rendering contains frontmatter plus the501–504loomweight section rather than targetcatalogue/fabrics. Itsdownloadlink returned404through the web tool. Do not count the “PDF Available” title as fullaccess.
4. UvADARE Hilditch metadata reappeared in discovery; C040alreadychecked it. It was not counted as a newroute.

Six search queries were executed, followed by dependent link/endpoint inspection:

- `"Nikolakopoulou" "2019" "Middle Bronze Age Pottery" pdf`
- `"Akrotiri Thera" "9384" "9730"`
- `"Akrotiri" "Hilditch" "377" "470"`
- `"Hilditch" "Phases B-C" pdf`
- `"9786185047429" pdf OR download`
- `"Akrotiri" "9384" "9730" -site:edabyt.gr`

Discoveryrefs: `turn69search1`(publishermetadata), `turn70view0`(samepage), `turn72view2`(publishercollection), `turn75search1`(official319PDF), `turn78view0`(toolsizefailure). Rawdownloadbytes and actualpublisherHTML, rather than searchsnippets, support the access result.

## Stop and continuation

The bounded source task achieved lawful full access and the exact catalogue/preservation controls. It did not recover an independent contents or exact production-group assignment for both marks. No further general acquisition is needed on this route. Continue only with a specified table/record capable of yielding the missing sample-to-inventory binding, or an exact use/contents record for these carriers.

No correspondence, sign-in, publication or semantic promotion was performed. The action/participant mission remains unmet by this source task.
