# KH Wc 2123: exact frozen-index and figure audit

Date: 2026-10-21. Supplementary task from lead; limited to this object's existing row, its provenance, and the newly obtained original fig.5. No additional candidate screened.

## Exact retained input

File: `baseline_packet/Linear_A_Baseline_2026-10-18/corpus/discovery_snapshot.json`.

SHA-256: `9b293509ab0ff928564c924e41f2c7da97e024ff28ac9b196e25cec638a2629b`.

This digest matches source-registry entry **R32-S6**, the inherited index from investigation21 and campaign22–31. Entry **I21_FROZEN** identifies the upstream as `https://github.com/mwenge/lineara.xyz`; R32-S6 explicitly calls it a discovery index, not an independent edition. The entire raw file remains unchanged.

The exact `KHWc2123` object is:

```json
{
  "support": "Roundel",
  "transliteratedWords": ["*810-PI-KA"],
  "words": ["𐝭𐘢𐘾"]
}
```

| Position | Codepoint | Installed Unicode 15.0.0 name | Index transliteration |
|---|---|---|---|
| 1 | U+1076D | UNASSIGNED | *810 |
| 2 | U+10622 | LINEAR A SIGN AB039 | PI |
| 3 | U+1063E | LINEAR A SIGN AB077 | KA |

“UNASSIGNED” describes the installed Unicode database's result; it is not a statement about a glyph's ancient identity or every later Unicode version. The execution output and exact row are preserved in `raw/KHWc2123_exact_index_audit.json`.

## Crosswalk: what is established and what is not

The baseline/source controls inspected contain no explicit `*810 → A373` alias record. They identify the digitized index's provenance but do not supply sign-by-sign normalization documentation. The current upstream README describes extraction from George Douros's tabulation, with edition images and Younger's commentary obtained separately. That is project-level provenance, not a target-specific reading authority.

The current upstream `ideograms.js` maps the literal U+1076D character to `*810`:

- https://github.com/mwenge/lineara.xyz/blob/master/ideograms.js
- Web retrieval `turn43view2`, content at displayed lines2180–2184.
- Upstream metadata/README: https://github.com/mwenge/lineara.xyz, `turn41view0`, displayed lines242–250.

These are current source-code observations; no upstream commit was recovered that independently pins the frozen snapshot's creation. They verify the application's character label but **do not establish `*810 = A373` as an editorial or palaeographic crosswalk**.

For this one object, matching the first indexed element to the edition's first mark is a reasonable **positional inference** because both precede AB39-77. It does not justify silently replacing `*810` throughout the corpus, or promoting A373 from one published reading branch into an adjudicated identity. Retain the index literal alongside the source branches.

## Consequential loss in the normalized row

The index represents one hyphenated token and contains no erasure brackets. Original p.13 and the fig.5 transcription instead represent the full sequence as erased and treat the first mark as separate from the syllabic pair. The comma/separation in the critical transcription is editorial; the photograph does not establish an ancient engraved divider there.

Therefore `*810-PI-KA` must not be used as:

- a secure complete three-syllable word;
- a secure unaltered current label at stamping;
- a secure instance of a known product logogram;
- an unused witness created by this campaign.

This is an overlay requirement. It does not require changing the immutable discovery data, and it does not recover a translation.

## Independent visual inspection: original fig.5

Source image supplied by the source investigator:

`../source_epigraphy/raw/AndreadakiVlasaki_Hallager2007_author_fig5.jpg`

I inspected its pixels through the image viewer. It contains obverse, reverse, edge, and impression photographs together with drawings. The printed transcription visibly places the first mark and PI-KA within one pair of erasure brackets. The first-mark drawing is much cleaner than the corresponding photographed traces. Finger-ridge patches, deformation, and surviving incision traces are visible, consistent with the source's account of handling and attempted smoothing.

I cannot identify a sufficiently clear crosscut in this image to independently establish erasure relative to the particular later seal impressions. I also cannot adjudicate the first mark as bird, tripod, or another reading from this plate alone. The seal drawing is identified in the source caption as composite; it is not an additional seal or independent impression event.

**Revised access status:** original fig.5 is now visually inspected. The earlier failed-screenshot record remains historically accurate but no longer describes the campaign's final image-access state.

## Consequential relabeling check

| Assignment changed | Effect on observed physical record |
|---|---|
| PI-KA as responsible operator → PI-KA as intended recipient | None established: either could appear in an erased designation before the present impressions. |
| PI-KA as individual → PI-KA as institution/account | None established: no independent person/category link is supplied. |
| First mark as bird-type product sign → tripod-type mark | Changes the proposed reading, but neither branch acquires an independently identified commodity or administrative relation. |
| Erased inscription has lost administrative force → same referent continues despite attempted removal | Both remain compatible; material alteration alone does not establish administrative cancellation. |

## Gate decision

**Unchanged: do not admit a semantic role/category test on this packet.** The additional work strengthens reading and representation control, and updates image access. It does not fix an inscription referent, prove administrative cancellation, or independently verify a decisive erasure–stamping microsequence.

The target was present in the frozen inherited index. Actual prior deliberate inspection of this exact row is not reconstructed; prior availability is established, and unused-witness status is not warranted.

## Minimal reproduction

Read only key `KHWc2123` from the named frozen JSON; compute the file's SHA-256; for the three characters in its `words[0]` print `ord`, hexadecimal codepoint, and `unicodedata.name`, retaining `unicodedata.unidata_version`. No corpus counts, model fit, or statistical test was performed. Compare the row with original printed p.13 and fig.5, not with a later flattened transcription.
