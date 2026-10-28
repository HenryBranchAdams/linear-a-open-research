# PH Wg 45: bounded original-source access screen

Date: 2026-10-24. Classification: access work and candidate admission review; no numbered semantic campaign.

## Question and route

The phase-stop review identified PH Wg 45/HM 1535 as a remaining original-source opportunity. The exact missing observation is whether the original entry, reverse/substrate image or description establishes what was sealed and the inscription's stage, with a physical or written counterpart capable of distinguishing a referent. Modern catalogue classification as a direct sealing does not by itself establish that relationship.

The lead supplied a concrete official GORILA II page-image route from the inherited source registry. Existing records link printed p. 90 to selector 150 but another section has a different offset, so **selector 156 was a proposed route to printed p. 96, not an already verified page identity**. The instructed finite sequence was to try selector 156 and use 158 only if the acquired printed label required an offset correction.

## Actual access result

| Route | Result | Inspection level |
|---|---|---|
| Official detail page with `sp=156` | Direct HTTP 503 Service Unavailable | No page text, target label or pixels acquired |
| Official `_156.jpg` images endpoint | Web tool inaccessible; direct request HTTP 503 Service Unavailable | No image acquired |
| Selector 158 | Not requested | No acquired label justified an offset correction |
| Hallager 1996 II p. 7 | Lead reports one exact title/publication lookup found only publisher sale/catalogue material | No original page acquired or inspected by this reviewer |

The detail and image calls were ordinary public HTTP requests without login, payment or bypass. Their exact URLs and errors are saved in `ph_source_screen/access_ledger.json`. The web retrieval failure is `turn103view0`. Multiple retrieval mechanisms for this page remain one source dependency.

## Decision

No original pixels were obtained and no archaeological conclusion follows from the access failure. **Do not admit a second deep campaign from this packet now.** The direct current acquisition route has been tested within the declared bound and is blocked. This result justifies retaining the exact packet in the continuation queue while closing the present phase; it does not prove that the pages are globally unobtainable or that they lack useful evidence.

The next action is to recover an actual copy of the target GORILA II entry/plate and Hallager's target direct-sealing entry when a working route or supplied copy appears. First verify the printed label and inventory crosswalk, then inspect the reverse and any target-specific substrate/stage statement. PH Wg 36/HM 1534 remains a separate object. If the recovered packet only confirms direct attachment or timing without a discriminating written relationship, close at source/object control. A matched counterpart or otherwise diagnostic relation would warrant a fresh admission decision.

The phase-stop decision is recorded in `PHASE_STOP_REVIEW.md`. No messages requesting source copies were sent.
