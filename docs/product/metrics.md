# Metrics — fable             Last read: 2026-06-29

> **Provisional (bootstrap).** No harness exists yet, so every Current reading is a true
> baseline of 0 / n-a. TARGET numbers and dates below are placeholders the owner confirms when
> `initial-assessment.md` is accepted; they firm up the timeline this file is dated against.
> A target with no number+date is not falsifiable — these are stated falsifiably but flagged
> provisional until acceptance.

## North-star
| Metric | Target (falsifiable) | Current | Read on | Trend |
|--------|----------------------|---------|---------|-------|
| **Defensible-evidence yield** — pre-registered causal contrasts answered with replicated, blinded, counterbalanced evidence | ≥ 1 primary contrast resolved (provisional) by 2026-10-31 (provisional) | 0 | 2026-06-29 | — |

## Input metrics (the levers that move the north-star)
| Metric | Target | Current | Read on |
|--------|--------|---------|---------|
| Run-validity rate — % runs completing schema-valid, zero hallucination, replayable | ≥ 95% (provisional) | 0% (no harness) | 2026-06-29 |
| Evaluator reliability — human-vs-blind-LLM-judge agreement (Cohen's κ) on calibration sample | ≥ 0.6 (provisional) | n/a | 2026-06-29 |
| Replication per condition — runs per family condition (seeded, counterbalanced) | ≥ 30, aim 50 (provisional) | 0 | 2026-06-29 |

## Guardrails (must NOT degrade)
| Metric | Floor / ceiling | Current | Read on |
|--------|-----------------|---------|---------|
| **World-state hallucination rate** — agent narration silently mutating world state | = 0 (hard ceiling; the core architectural invariant) | n/a | 2026-06-29 |
| Evaluator-blind compliance — evaluator never sees family-condition labels | = 100% | n/a | 2026-06-29 |
| Run reproducibility — % runs re-instantiable from a complete RunManifest | = 100% (manifest completeness) | n/a | 2026-06-29 |
| Cost per experiment batch | ≤ ~$50 (autonomous envelope; above = escalate) | n/a | 2026-06-29 |
