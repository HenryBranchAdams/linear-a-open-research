# Linear A, in the Open

An open, AI-assisted Linear A investigation by Henry Adams and contributors. This site explains the research for readers arriving without project history and preserves the evidence needed to challenge its conclusions.

## Research state

Research is current through C044 (documentation D2026-10-26). The latest result is a graded local preference for HT31’s first vessel sign as a bronze-cauldron class; exclusive material denotation and action/participant roles remain open. C042’s numeral/capacity constraint and C043’s failed comparison gate are preserved. No semantic experiment is active and C045 has not been created.

Live site: https://linear-a-open-research.madebyhenry.chatgpt.site

Public repository: https://github.com/HenryBranchAdams/linear-a-open-research

Start with [CURRENT_STATE.md](CURRENT_STATE.md), [the full public baseline](research/current/CURRENT_RESEARCH_BASELINE.md), [the current brief](research/current/CURRENT_RESEARCH_BRIEF.md) and [the source guide](research/current/SOURCE_GUIDE.md).

## Site

The site uses a compact research-document layout with a contents index, current assessment, evidence/result/limitation table, source references and an optional HT34 reading-and-scope comparison. Typography, navigation, findings, methods and contribution pages follow the same restrained system. The research page, methods/glossary, contribution brief and source release provide progressively deeper reading.

The original eight tasks are archived. Original prompt and input bytes are preserved. Historical discussions, submissions and release of existing claims remain available. New claims and renewals are closed; source notes, corrections, reproductions, independent reviews and evidence proposals use the open contribution hub. Everyone can prepare a portable draft before choosing on-site submission or GitHub.

The site uses the existing Cloudflare Worker, managed ChatGPT sign-in and managed D1 database. An additive `contribution_records` table explicitly links new submissions with their discussion, provenance, reuse permission and related work. Existing research, submissions and discussions are preserved; old links are not guessed. Private identity fields remain out of public responses and exports. Public visibility inherits moderation of linked records and ancestors.

## Journal and collaboration

`/journal` offers readable notes from the reviewed C042–C044 record, each connected to its existing finding discussion. `/journal/feed.xml` is a public RSS feed of the editorial notes. Campaign documentation dates are labeled separately from publication dates. `/discussion` remains the open forum.

`/contribute` is an account-free draft workspace with local browser autosave, Markdown/JSON downloads and a prefilled GitHub issue route. Posting here requires sign-in and a public handle. `/contributions` lists new, explicitly linked public records with review status, evidence, replies and independent reviews. The site and GitHub are separate channels with explicit cross-links, not automatic synchronization.

Public reads use `/api/contributions`, `/api/contributions/export` and `/api/contributions/:id`; `/api/contributions/schema` describes the version 1 export envelope. List/export responses accept `type`, `status`, `q`, `related`, `limit` and `cursor`. Follow `nextCursor` until null to retrieve all pages. Public JSON allows cross-origin reads. It excludes hidden material and private authentication identities, respects each contribution’s reuse permission and does not relicense cited third-party sources. The existing `/api/export` remains steward-only.

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CONTRIBUTION_TEMPLATE.md](CONTRIBUTION_TEMPLATE.md).

## Build and verification

Requires Node.js 24 and Python 3. Run `python3 scripts/verify-public-research.py`, `npm run build`, then `npm test`. In the managed Sites environment, preview with `sites-preview start` and this checkout's absolute path. The local preview uses an empty, transient coordination database and does not modify production records.

`scripts/build.mjs` packages the Worker, self-hosted image/font assets, public source release and eight archival input packets. The packets retain original prompts and inputs but are repackaged with the current-state notice; they are not byte-identical to original packets.

`src/editorial.js` contains the public narrative. `content/findings.json` stores current finding dispositions. `research/current/` contains the full public reference packet. `DESIGN.md` records the current research-archive design and validation approach.

Research prose is CC BY 4.0. Original datasets, publications, photos and fonts retain their stated licenses. See [LICENSES.md](LICENSES.md). The first site's root documents remain under research/publication-history/2026-10-02/ as historical records.

## Public research projection

`research/campaigns/` preserves the authored record through C044. Its publication manifest pins original bytes and lists omitted nested archives and private metadata. Read [PUBLIC_RELEASE.md](research/campaigns/PUBLIC_RELEASE.md) for scope. The original complete-snapshot verifier needs those omitted archives; use the public verifier above for this checkout. Passing software checks does not establish ancient meanings.
