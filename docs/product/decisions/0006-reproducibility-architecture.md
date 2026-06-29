# PDR-0006 — Reproducibility architecture: one Effects boundary, structural keying, state-hash oracle, class-by-surface

Date: 2026-06-29   Status: accepted   Author: Claude (product-owner agent)   Owner sign-off: within-strategy (architecture)
Related: HLD §6, REQ-FABLE-0006/0007, determinism-review C1/C2/C3/H1/H2/H3/H4, solution-review M1/M4

## Context
The determinism review found that REQ-0006 ("replay exactly") was, as written, neither achievable
nor testable: the effects-substitution layer was one sentence, there was no oracle to prove a
replay reproduced recorded state, the day loop had no ordering/RNG discipline, the evaluator
(which produces the primary DV) might sit outside the transcript, and the RunManifest was
incomplete for re-instantiation. The dominant risk is *silent* divergence — a replay that succeeds
with no error but reconstructs a different world.

## The call
Adopt a single reproducibility architecture:
1. **One `Effects` boundary** — the sole choke point for ALL non-deterministic reads: agent LLM
   calls, the (deterministic) GM is exempt, **evaluator LLM calls**, embeddings calls,
   environmental RNG draws, the clock, env reads, and any parse-repair/retry LLM call. In replay
   mode it serves recorded responses and re-issues nothing live; an assertion enforces zero live
   calls of any recorded kind.
2. **Structural effect key** — `(run_id, day, phase, agent_id, call_purpose, attempt)`. Chosen over
   ordinal keys (fragile under concurrency) and hash-of-prompt keys (fragile under non-canonical
   encoding); decouples replay from both concurrency and encoding.
3. **Per-step state-hash divergence oracle** — a canonical hash over folded world+memory state at
   each day/phase boundary and each `GMResolution`; replay recomputes and asserts equality; first
   mismatch is the localization point. This makes REQ-0006 testable (CI property).
4. **Determinism class by surface** — agents = stochastic-recorded (the phenomenon); GM =
   deterministic rule-based (PDR-0005); evaluator = deterministic-as-possible (temp=0 + provider
   seed where available), and its I/O is recorded so the primary result replays.
5. **RNG sub-stream isolation** — one named, seed-derived sub-stream per stochastic component
   (scheduler, world-events, tie-breaks); pinned BitGenerator recorded in the manifest.
6. **Deterministic-parallel day loop** — agent calls may fan out for throughput but are joined,
   sorted by `agent_id`, then applied and logged in canonical order; never completion order.
7. **Extended RunManifest** — distinct pinned `agent_model`/`gm_model`/`evaluator_model`/
   `embedding_model` (+version, provider, `system_fingerprint`, full sampling params), seed,
   BitGenerator, content hashes of frozen config artifacts, runtime/library versions, and
   `sim_version` = git SHA + dirty flag. Memory retrieval is logged as a recorded effect.
8. **Canonical encoding** — JCS (RFC 8785) for hashed bytes; raw LLM responses stored verbatim.
9. **Per-run store sharding** — one SQLite store per `run_id` for the replicated batch (answers Q5).

## Rationale
This single architecture closes the determinism CRITICALs and HIGHs and the solution-review M1/M4
together; the structural key + state hash are the highest-leverage moves (they also force the
concurrency and RNG decisions). It is the axiom-determinism-and-replay Effects/compare-point pattern
applied to an LLM harness.

## Reversal trigger
Revisit a sub-decision if Stage-0 prototyping shows the structural key collides (e.g. multiple calls
share `(day,phase,agent,purpose)` — extend the tuple), or if per-step hashing proves too coarse to
localize a divergence (drop to per-resolution granularity).
