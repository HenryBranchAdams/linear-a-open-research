# Contributing

You can help with one source, one correction, one reproducible check or one well-supported objection. You do not need a complete decipherment theory or permission to download the public materials, fork the repository or investigate independently within their licenses.

Start at the [contribution hub](https://linear-a-open-research.madebyhenry.chatgpt.site/contribute), browse [public contributions](https://linear-a-open-research.madebyhenry.chatgpt.site/contributions), or use [the portable template](CONTRIBUTION_TEMPLATE.md). Read [CURRENT_STATE.md](CURRENT_STATE.md) before relying on an earlier finding.

To follow the work, read the [research journal](https://linear-a-open-research.madebyhenry.chatgpt.site/journal). Each entry explains a result, a useful failure or an open question and links to the evidence and public discussion. Reading and following the investigation do not require contributing.

## Choose a useful contribution

| Type | What to bring | What it can establish |
| --- | --- | --- |
| Source | An exact citation, object identifier, figure or legitimate access route; state what you inspected. | Better source access or a traceable observation. Access alone does not establish a meaning. |
| Correction | The precise passage, data row or claim; the problem; supporting evidence; a proposed correction. | A bounded repair. Keep unaffected observations and uncertainty intact. |
| Reproduction | The input version, commands or method, actual outputs and any differences. | Whether an earlier calculation or procedure reproduces. Reusing exposed evidence is not new linguistic validation. |
| Independent review | A link to the contribution or claim, what you checked, the strongest objection and what survives it. | An attributed challenge or assessment. Explain the limits of your independence. |
| Candidate evidence | The exact target, serious alternatives, a separating observation, finite checking route, prior exposure and stopping condition. | A proposal for bounded investigation. It does not automatically admit a semantic experiment. |

For a source or correction, complete the fields relevant to that small task. A new semantic proposal needs at least two serious interpretations and evidence that can distinguish them without assuming the preferred meaning. Explain what would change your assessment, not just what supports it.

## Work where you prefer

The site, GitHub and independent forks are valid places to prepare research. You may use any research method or agent within an explicit budget. Do not infer authorization for spending, correspondence or external publication from a research prompt.

- **Prepare a draft without an account.** The [hub](https://linear-a-open-research.madebyhenry.chatgpt.site/contribute) exposes the contribution fields before sign-in and can download a Markdown or JSON draft. A downloaded draft is your copy; it is not a published submission.
- **Submit on the site.** ChatGPT sign-in and a chosen public handle are required to post. Contributions are public and begin as unreviewed. The submitted record has a stable URL, linked discussion and a visible project-review disposition.
- **Contribute on GitHub.** Open a [research issue](https://github.com/HenryBranchAdams/linear-a-open-research/issues/new?template=research.yml), or fork the [repository](https://github.com/HenryBranchAdams/linear-a-open-research) and propose a focused pull request. Cite the baseline or commit you used and link the relevant site contribution when one exists.
- **Publish an independent research branch.** Preserve attribution, source licenses, input versions and the distinction between your conclusions and this project's reviewed record. Link your result in a contribution so others can inspect and challenge it.

There is no automatic two-way synchronization between GitHub and the live site. Site submissions and discussions live in the coordination database; the repository carries the maintained research record and software. Cross-link the original work to retain its provenance. A repository merge or promotion into the reviewed record is explicit.

## Make your work inspectable

Give the contribution a descriptive title. Identify the exact target and sources; separate observations from readings, restorations, assumptions and interpretations. Report the method or commands actually used, limitations and serious rivals, prior exposure, agent assistance and preferred credit. Use “unknown” where information is missing.

For a review or follow-up, link the original contribution. State whether you produced the original analysis, used its outputs or encountered its conclusion before checking it. Different authors, models or publications do not by themselves make the underlying evidence independent. A public review can support, challenge or narrow an interpretation; it does not silently change the project's accepted findings.

Public contribution pages show the submitted evidence, current project-review status, rationale and reviewed-record reference when supplied. Accepted and negative-result dispositions require a reviewed-record reference. Source fidelity, uncertainty, substantive rivals, outcome exposure and independent evidence govern review. Project review is not external academic peer review.

The public index covers contributions with an explicit submission-to-discussion link. Older discussions and submissions remain in their existing locations; no historical link is guessed from matching text.

## Reuse and independent snapshots

The anonymous read endpoints are:

- `/api/contributions`: a paginated public contribution list.
- `/api/contributions/export`: a paginated JSON snapshot using the same public visibility rules.

Exports identify format version 1 and retain public attribution, evidence, provenance and review information. Follow the response's pagination links or cursor to retrieve additional pages; a single page is not necessarily a complete snapshot. Hidden contributions and private authentication identifiers are excluded. The steward's administrative export remains separate.

Record the export time and original contribution URLs when keeping a snapshot or mirror. Public records may later be corrected or hidden; a snapshot describes what was visible at collection time, not an immutable endorsement. Preserve each contribution's reuse terms and third-party exclusions.

Choose the reuse terms for **your original contribution text** when submitting:

| Selection | Meaning |
| --- | --- |
| `CC-BY-4.0` | Others may reuse your original text under Creative Commons Attribution 4.0, with attribution. |
| `CC0-1.0` | You dedicate your original text under the CC0 1.0 terms. |
| `UNSPECIFIED` | No additional reuse license is granted. Public visibility and export do not imply permission to relicense or republish it. |

These selections do not change the rights in quoted scholarship, linked images, datasets or other people's work. They do not retroactively license older submissions. Credit original authors and image makers; link restricted plates and publications. SigLA-derived material retains its recorded CC BY-NC-SA 4.0 conditions. See [LICENSES.md](LICENSES.md) for the project's existing rights and exclusions. Share only material you are entitled to make public, and leave private contact details out of public fields.

## Current research boundaries

Research is through campaign 044, with documentation D2026-10-26. C043 and C044 are complete. No candidate or semantic experiment is active; C045 is available and has not been created. The frozen B2026-10-18 baseline plus C038–C044 remains the scientific authority.

The immediate source target is Duhoux 2003's complete ceramic comparison, especially §4.1.2, following C044's graded local vessel-class preference. Exact cross-material use or a feature-matched ceramic counterpart could change that result. Exclusive bronze denotation, an action and participant roles remain unresolved. The complete chapter and original target Puglisi figures remain uninspected; complete Flouda 2024 remains an inherited access dependency. Prepared evidence requests are unsent.

A legitimate complete copy or changed access route can enable bounded source evaluation. Read [the current brief](research/current/CURRENT_RESEARCH_BRIEF.md) for exact reopening and stopping conditions, and [the source guide](research/current/SOURCE_GUIDE.md) for inspection limits. Submission does not create a campaign, reserve a task or authorize an experiment.

The eight original missions remain archived. Their original prompts, inputs and identifiers are preserved. New lead, replication and external claims and renewals are closed. Existing contributors may release historical claims, submit results or discuss them. Independent reproduction reports are welcome as contributions without reopening a historical claim.

## Verify a software or data change

Run `python3 scripts/verify-public-research.py`, `npm run build`, then `npm test`. Report which checks you actually ran and which inputs were unavailable. The original full-snapshot verifier requires omitted archives and private inventories; the public verifier checks this repository's curated projection. Passing software checks does not establish ancient meanings.
