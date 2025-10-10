# Paper Risk Log and Strengthening Ideas

## Outstanding technical concerns

1. **Latent `FOLLOW` state in Agent A.** The initiator still switches into a `FOLLOW` state even though the helper `_handle_follow_message` function was removed earlier. It currently never fires because conversations terminate at the certificate ACK, yet the dormant branch is easy to trigger if we reintroduce YIELD-handshake behaviour. We should either excise the dead state or reimplement the handler so reviewers do not question the FSM completeness.
2. **Responder-MinCut Baseline behaviour.** The responder-led baseline finishes with 20.5% success because it only handles unreachable cases and sometimes emits empty separators. That is consistent with its design, but the paper needs to acknowledge the limitation explicitly; otherwise the confusion over “low success” will distract from the main claim.
3. **Tail cases for CertTalk bytes.** Five seeds show 1.6–2.0 KB transcripts. Each is a path-cert scenario with many reruns and one probe. We should characterise these outliers in the paper (e.g., explain that they correspond to near-ambiguous path/cut boundary instances) and, if possible, note that the byte budget still respects the 3 KB cap.
4. **Cut optimality gap.** About 235 cut certificates exceed the oracle minimum by one or more cells (max gap 10 on seed 623). The current digest is correct, but the narrative should admit that witness bits focus on soundness, not optimality.
5. **Compact schema parity.** Send-All now uses the same compact key map as CertTalk. We should document when this change happened and verify the paper tables reflect the 364 byte median rather than the earlier 466 byte figure to avoid accusations of unfair comparisons.

## Opportunities to strengthen the paper

1. **Add a “tail behaviour” subsection.** Summarise round/byte distributions, highlight the fast-path fraction (23.5% three-turn runs), and explain the probe rarity (0.5%). This gives readers confidence that efficiency is not just a median story.
2. **Clarify baseline intent.** Dedicate a paragraph that frames Responder-MinCut as a cut-only baseline meant for unreachable instances, perhaps reporting its performance conditioned on unreachable seeds (205/808 accepted). Pair this with a sentence on why Send-All and Greedy-Probe remain the principal comparators.
3. **Include an ablation table.** We already recorded the pre/post SCHEMA removal metrics. A compact table showing the evolution (3.1 KB → 947 B → 653 B → 468 B) would make the narrative of iterative improvements far more convincing.
4. **Document fairness knobs.** State explicitly that all systems share compact schema, CRC16, and identical limits. If we keep the option to shorten `signed_by` to `"B"`, mention the possible savings and whether we exercised them.
5. **Discuss correctness guarantees.** The current draft explains the oracle, but adding a short remark about zero oracle failures in the final sweep (1000/1000) reinforces the rigor claim.
6. **Expose planner invariants.** Tie the halo, failed digest sets, and witness bits back to the protocol analysis so the reader sees how each design choice prevents specific failure modes observed in early runs.
7. **Reference raw artefacts.** Link directly (relative paths) to `runs/20251009T201009Z_certtalk.jsonl` and the transcript gallery so reviewers can audit without hunting through the tree.

## Optional polish

- Consider pruning the empty top-level `agents/` directory and documenting the reason if we keep it. Little structural inconsistencies will distract program chairs.
- Before submission, regenerate `paper_source.txt` and the handoff bundle after any LaTeX edits to keep the artefact hash in sync with the final PDF.

