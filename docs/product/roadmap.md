# Roadmap — fable            Updated: 2026-06-29 (PDR-0001)

> Sequencing, WSJF / cost-of-delay, and dated forecasts are produced by
> /axiom-program-management. This file records bets as INTENT, not a delivery
> schedule. Do not compute WSJF here; hand the committed bet over for sequencing.
> The dated, phased timeline lives in `initial-assessment.md` (the current deliverable),
> not in this file.

## Now  (committed, in-flight)
- **Initial assessment** — delivered (owner's first deliverable). · artifact: `initial-assessment.md`
- **Stage 0 — harness foundation** — structured world interface + rule-based GM + Effects
  boundary + event-sourced replayable logs + the no-narration invariant; prove agents are
  constrained and traces are clean. Design reviewed (HLD v2, PDR-0005..0008). · tracker:
  **fable-1c6ca715c5** (15 tasks) · metric: run-validity rate, world-state-hallucination rate (guardrail)

## Next (shaped, decreasing certainty)
- **Stage 1 — one-generation causal experiment** — 24 agents, power-derived replication, fixed
  12-event arc + held-out tests, counterbalanced conditions, 3-layer blind evaluator,
  pre-registered DV + world-policy table. Produces the **initial results**. Full batch gated by
  PDR-0009 (budget). · tracker: **fable-6a4b84af09** · metric: defensible-evidence yield, κ

## Later (directional bets, no order, no dates) · tracker: **fable-5026ddd67a**
- **Stage 2 — generational transmission** — child→parent transformation (with summariser-bias
  controls: human / LLM / no-memory / direct-inheritance arms), second generation, frozen world
  policy + event schedule.
- **MCP wrapper** — wrap the stabilised world API as MCP tools/resources/prompts.
- **Scale & richness** — sibling families (3→4 members), more value dimensions beyond the
  initial 6, multi-model replication as a blocking factor, dashboards and automated scoring.
