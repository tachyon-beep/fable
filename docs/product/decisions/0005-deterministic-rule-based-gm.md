# PDR-0005 — The Game-Master is a deterministic, rule-based resolver (not an LLM)

Date: 2026-06-29   Status: accepted   Author: Claude (product-owner agent)   Owner sign-off: within-strategy (architecture)
Related: HLD §3/§6/§9, REQ-FABLE-0001/0013, solution-review C1, determinism-review H3

## Context
Both design reviews independently flagged the GM. The HLD contradicted itself: §9 said "a capable
model for agents+GM" (an LLM sharing the agent model) while §3/§5/§6 described a deterministic,
seeded, policy-table resolver with "zero live LLM calls." This had to be settled before the schema
freeze because it drives the determinism contract (Q1), the circularity risk (R2), and the
no-narration invariant (REQ-0001).

## Options considered
1. **LLM GM sharing the agent model** — pro: flexible natural-language adjudication; con: the actor
   and the adjudicator of consequences share normative priors (circularity in *resolution*, not
   just scoring), reintroduces "story soup", and breaks the deterministic-replay claim.
2. **LLM GM, distinct third model family, pinned** — pro: keeps NL flexibility, reduces shared
   priors; con: still stochastic; still a hidden treatment; more cost; more determinism burden.
3. **Deterministic, rule-based, seeded GM** (policy-table lookup + seeded RNG; no LLM) — pro:
   mechanically guarantees REQ-0001, defeats GM-as-hidden-treatment (R3), removes a circularity
   vector, and largely dissolves the determinism question for the GM surface; con: action
   adjudication must be expressible as rules over the structured proposal + world state.

## The call
Option 3. The GM is a **deterministic, seeded, rule-based resolver** that validates a structured
`AgentActionProposal` and resolves outcomes via the versioned world-policy table. No LLM in the GM
by default. Free-text `speech`/`private_reasoning_summary` are recorded and may inform *agents'*
perception, but never the *resolution function* — resolution keys only on structured fields +
world state + policy table. If a future action class genuinely needs natural-language adjudication,
it is isolated as a named, separately-modeled (third family), manifest-pinned sub-component —
deferred unless proven necessary.

## Rationale
This is the principled choice both reviewers recommended: it makes the headline invariant
mechanical, keeps the "moral physics" explicit and reproducible, and means the GM surface is
deterministic-by-construction (see PDR-0006's determinism-class split). It also fixes the §9 error.

## Reversal trigger
Revisit if Stage-0 prototyping shows a material fraction of action outcomes cannot be adjudicated by
rules over structured fields + world state without arbitrary/unfair resolutions — in which case the
isolated NL-adjudicator sub-component is introduced under its own PDR with the third-family pinning.
