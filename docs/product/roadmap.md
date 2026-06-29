# Roadmap — fable            Updated: 2026-06-29 (PDR-0001)

> Sequencing, WSJF / cost-of-delay, and dated forecasts are produced by
> /axiom-program-management. This file records bets as INTENT, not a delivery
> schedule. Do not compute WSJF here; hand the committed bet over for sequencing.
> The dated, phased timeline lives in `initial-assessment.md` (the current deliverable),
> not in this file.

## Now  (committed, in-flight)
- **Initial assessment** — the owner's first and only requested deliverable: scope, risks,
  and timeline for Stage 1 *and* Stage 2, plus execution needs. · artifact: `initial-assessment.md`
  · metric: unblocks everything (gate before build)
- **Stage 0 — harness foundation** — the structured world interface + GM/resolver +
  event-sourced, schema-valid logs + the no-narration-into-reality invariant; prove agents
  are constrained and traces are clean. Begins on assessment acceptance. · tracker: epics TBD
  · metric: run-validity rate, world-state-hallucination rate (guardrail)

## Next (shaped, decreasing certainty)
- **Stage 1 — one-generation causal experiment** — 24 agents (2 tribes × 4 families × 3),
  ≥30–50 replicated runs, fixed 12-event arc + held-out adolescent tests, family-condition
  counterbalanced across tribes, 3-layer blind evaluator, pre-registered world-policy table
  and primary contrasts. Produces the **initial results**. · metric: defensible-evidence yield,
  evaluator reliability (κ)

## Later (directional bets, no order, no dates)
- **Stage 2 — generational transmission** — child→parent transformation (with summariser-bias
  controls: human / LLM / no-memory / direct-inheritance arms), second generation, frozen world
  policy + event schedule.
- **MCP wrapper** — wrap the stabilised world API as MCP tools/resources/prompts.
- **Scale & richness** — sibling families (3→4 members), more value dimensions beyond the
  initial 6, multi-model replication as a blocking factor, dashboards and automated scoring.
