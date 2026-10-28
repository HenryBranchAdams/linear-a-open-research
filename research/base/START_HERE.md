# Linear A research workspace

**Current result:** iteration10 is complete. We have stronger linked-record candidates and explicit rival tests, but no independently supported action-and-role sentence.

Start with [the candidate-pair atlas](iterations/010/ATLAS.html), then [current state](context/CURRENT_STATE.md). This workspace is the cumulative continuation point; the original historical bundles remain unchanged.

| Location | Purpose |
|---|---|
| `context/CURRENT_STATE.md` | What is established, blocked and worth doing next |
| `context/HISTORY.md` | Recovered trajectory through iteration9, including rounds3–5 |
| `context/DO_NOT_REUSE.md` | Rejected or unsupported shortcuts and repeat-work warnings |
| `context/RESEARCH_PROTOCOL.md` | Evidence standards and update procedure |
| `registry/claims.json` | Authoritative cumulative claim register:44 records with evidence and qualifications |
| `registry/experiments.json` | Executed iteration10 experiments, results and limitations |
| `registry/sources.json` | Source access levels, citations and corpus license |
| `corpus/` | Immutable SigLA acquisition; overlays live in experiments |
| `iterations/010/` | Atlas, code, data, full results, source audit and adversarial review |
| `archive/` | Original round9 and handoff bundles with earlier history |
| `verify.py` | Offline deterministic reproduction and integrity checks |

## Resume without reconstructing the project

1. Read current state, forbidden shortcuts and the latest atlas.
2. Choose a missing observation that would distinguish actual rival explanations; check the claims and history before repeating an experiment.
3. Add the next numbered iteration. Keep raw evidence, transformations, results and interpretations separate.
4. Append experiment and claim records; preserve stable IDs and earlier evidence. Update current state and this entry point when the run ends.
5. Run `python3 verify.py` and save the structured workspace plus an updated archive checkpoint.

The archive syntax `outer.zip!/member.zip!/file` identifies preserved nested members. `context/HISTORY.md` maps them. The September8 review is separately available among the existing project materials; its missing-archive limitation has now been addressed by recovery, not by retroactively changing that report.

## Reproduce

Python3 standard library only. Extract the accompanying workspace ZIP, enter `linear_a_research`, and run:

```sh
python3 verify.py
```

This regenerates the fresh numerical and corpus analyses and checks retained evidence references. It does not rerun all earlier iterations or certify any translation. Full scholarly PDFs are not redistributed; source locators and selected inspected edition pages are retained.
