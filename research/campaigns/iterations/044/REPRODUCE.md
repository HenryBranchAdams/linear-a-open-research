# Reproduce C044's corpus control and inspect its inference

From the extracted **complete current project** root:

```bash
python3 iterations/044/analysis/extract_target.py
```

Compare the printed JSON with `iterations/044/analysis/target_index_result.json`. This uses the unchanged `corpus/discovery_snapshot.json`, preserves HT31 exactly and lists literal `*410-VS` matches. It is not a critical-edition census or unused validation. The C044-only archive preserves the authored findings and row overlay; the complete current package supplies the frozen corpus needed for this index check.

The material comparison is qualitative. Read [the feature/source packet](evidence/SOURCE_PACKET.md), [critical overlay](evidence/HT31_OVERLAY.json), [inference branches](analysis/INFERENCE.md), [ceramic challenge](evidence/MATERIAL_RIVAL.md) and [independent review](review/FINAL_REVIEW.md). Their exact primary-source locators distinguish actually inspected pixels from reported examination and unavailable figures. No numerical similarity score or material-impossibility calculation was executed.

The original brief and reviewer criteria are retained with hashes. Later source-led refinements are in [the decision log](DECISION_LOG.md). The source chain is not independent replication, and the result is a graded preference with material extension unconfirmed.
