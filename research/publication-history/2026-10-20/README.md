# Linear A, in the Open

An open, AI-assisted Linear A investigation by Henry Adams and contributors. This site explains the research for readers arriving without project history and preserves the evidence needed to challenge its conclusions.

## Research state

The 18 October 2026 baseline covers research through investigations 36–37. The mission remains open. Useful source corrections, numerical constraints and structural comparisons survive, while several earlier semantic and validation claims have been narrowed or withdrawn. The latest two branches are parked and no semantic experiment is active.

Start with [CURRENT_STATE.md](CURRENT_STATE.md), [the full public baseline](research/current/CURRENT_RESEARCH_BASELINE.md), [the current brief](research/current/CURRENT_RESEARCH_BRIEF.md) and [the source guide](research/current/SOURCE_GUIDE.md).

## Site

The opening page introduces the script and mission, shows retained findings, provides an HT34 reading-and-meaning demonstration, explains corrections and separates the evidence and access limits reached by investigations 36 and 37. The research page, methods/glossary, contribution brief and source release provide progressively deeper reading.

The original eight tasks are archived. Original prompt and input bytes are preserved. Historical discussions, submissions and release of existing claims remain available. New claims and renewals are closed; current ideas, sources and corrections use the existing reviewed contribution flow.

The site uses the existing Cloudflare Worker, managed ChatGPT sign-in and managed D1 database. No database migration is introduced by this revision. Private identity fields remain out of public responses and exports.

## Build and verification

Requires Node.js 24 and Python 3. Run `npm run build`, then `npm test`. In the managed Sites environment, preview with `sites-preview start` and this checkout's absolute path. The local preview uses an empty, transient coordination database and does not modify production records.

`scripts/build.mjs` packages the Worker, self-hosted image/font assets, public source release and eight archival input packets. The packets retain original prompts and inputs but are repackaged with the current-state notice; they are not byte-identical to original packets.

`src/editorial.js` contains the public narrative. `content/findings.json` stores current finding dispositions. `research/current/` contains the full public reference packet. `DESIGN.md` records the tasteskill v2 direction and validation approach.

Research prose is CC BY 4.0. Original datasets, publications, photos and fonts retain their stated licenses. See [LICENSES.md](LICENSES.md). The first site's root documents remain under research/publication-history/2026-10-02/ as historical records.
