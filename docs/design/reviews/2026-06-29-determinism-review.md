# Design Review — Determinism & Replay (2026-06-29)

Reviewer: `axiom-determinism-and-replay:determinism-reviewer` (background agent)
Subject: HLD draft (`docs/design/hld.md`) + `text1.md`/`text2.md` + assessment + REQ-FABLE-0001..0022
Verdict: **two-tier reproducibility framing is sound, but record-replay (REQ-0006) is NOT yet
achievable or testable as specified.** Re-instantiation (REQ-0007) is achievable but the
RunManifest is materially incomplete. Tally: 3 CRITICAL, 5 HIGH, 4 MEDIUM, 3 LOW, 2 INFO.

## CRITICAL
- **C1 — No divergence oracle.** "Replay exactly" is unfalsifiable: no state hash / per-step
  compare-point. The zero-hallucination provenance audit verifies *sourcing*, not replay
  equivalence — the HLD conflates them. → Add `state_hash` over folded world+memory state at each
  day/phase boundary and each `GMResolution`; replay asserts hash-equality. Channel 05.
- **C2 — Effects-substitution layer underspecified.** The load-bearing replay mechanism is one
  sentence. Missing: (1) the **key** mapping logged response→request at replay; (2) the **scope**
  (only "LLM I/O" named — embeddings, clock, env RNG, os.environ not declared as recorded
  effects); (3) replay lifecycle (read-only vs re-issuing side effects). Adversarial catch: a
  JSON-repair retry that re-calls the model is a *second uncaptured live call* during replay
  (interacts with REQ-0009). → One `Effects` interface as the sole choke point for ALL
  non-deterministic reads, keyed + recorded; store raw response bytes verbatim. Channels 06+10.
- **C3 — Evaluator is a third LLM surface that produces the primary DV and may be outside the
  transcript.** REQ-0018 (blind LLM) + REQ-0019 (primary DV = EvaluatorScore). If "out-of-band"
  bypasses the event log, world state replays exactly but the *headline number is
  non-reproducible*. → Bring evaluator I/O into the transcript; pin at temp=0 + provider seed;
  record per-call response. (Determinism-scoped only; bias is text2's lane.) Channels 06+10.

## HIGH
- **H1 — Day-loop concurrency/ordering undefined.** ~24 per-step LLM calls will be parallelized
  for throughput; applying/logging in completion order breaks JSONL order, RNG draw order, and
  ordinal keys. → Declare deterministic-parallel: fan out, join, **sort by agent_id**, apply+log
  in canonical order, never completion order. Canonical family/agent iteration order. Channel 07.
- **H2 — Single shared RNG, no sub-stream isolation.** Scene scheduling + world events share one
  draw sequence; values depend on interleaving. → Derive named sub-streams per component via
  domain separation (counter-based); pin the BitGenerator (e.g. numpy PCG64) and record it. Ch 03.
- **H3 — Q1 answered: pin the GM (and evaluator); keep agents stochastic.** GM is the
  deterministic "moral physics" spine, not a behavioural subject; a stochastic GM injects noise
  into the causal path (a re-instantiation confound — GM variance vs treatment effect). →
  **Split the determinism class by surface:** agents = stochastic-recorded; GM + evaluator =
  deterministic-as-possible (temp=0, seed, recorded). Channels 01+10.
- **H4 — RunManifest materially incomplete for re-instantiation (REQ-0007).** Add: (a) provider
  sampling **seed**; (b) **provider/endpoint identity** + `system_fingerprint` (OpenRouter routes
  one "model+version" to multiple backends/quantizations); (c) full sampling params (top_k,
  penalties, max_tokens, stop, logit_bias); (d) embeddings model+version+**dimension**; (e)
  runtime/library versions (python, pydantic, numpy RNG algo); (f) **content hashes** of the
  frozen event_schedule / world_policy / prompt_pack tables (an id string can be silently
  mutated); (g) `sim_version` = **git SHA + dirty flag**, not loose semver. Channels 02+11.
- **H5 — Environmental world-updates vs the REQUIRED `source_resolution_id`.** Step-1 world
  updates mutate state but aren't agent-action resolutions → either the "no orphan deltas"
  invariant fails or they need a synthetic source; and their "(seeded)" draws are an unlogged
  replay-relevant effect. → Add a **typed** delta source (`agent_resolution` |
  `system_resolution`); require *a* typed source; log environmental RNG as a recorded effect. Ch 06.

## MEDIUM
- **M1 — Canonical encoding unspecified.** Default JSON isn't canonical (key order, ensure_ascii,
  float repr, unicode). Severity is **conditional on the C2 keying choice**: hash-of-prompt key →
  CRITICAL; structural/ordinal key → LOW. → JCS (RFC 8785) for any hashed bytes; store raw
  responses verbatim; NFC for SQLite text. Channel 11.
- **M2 — `source_resolution_id` enforced at pointer level, not content level.** A delta could cite
  a valid resolution yet mutate fields it never sanctioned. → Make the audit content-aware (delta
  changes ⊆ resolution-sanctioned changes); GM is the *sole* delta constructor. Channel 05.
- **M3 — Memory retrieval recompute-vs-log undecided = the silent-corruption mode.** Ordinal key +
  recomputed retrieval: a ranking reorder (FP/thread/tie-break) changes the prompt but the ordinal
  still feeds the "right" response to a now-wrong prompt → **replay succeeds with no error and
  reconstructs a different world.** → Log retrieved memory IDs as a recorded effect (preferred);
  else pin OMP threads + deterministic tie-break on memory_id *and* add the C1 state hash. Ch 08/06.
- **M4 — No snapshot/checkpoint; RNG *state* not capturable.** Replay is whole-transcript-from-t0
  only; a crashed long run can't resume; bisection needs a checkpoint. A seed alone can't resume
  mid-run — need RNG internal state. → Optional per-day snapshot (state + all RNG states + effect
  cursor); cheap given event-sourcing. Channel 04.

## LOW / INFO
- **L1** — Re-instantiation has a shelf life: OpenRouter model retirement kills it (record-replay
  unaffected). Capture `system_fingerprint`; long-horizon may need a local open-weight (CUDA) option.
- **L2** — Forbid implicit-seed fallback (fail closed); pin + record the RNG algorithm/version.
- **L3** — Cross-process SQLite contention for the 50× batch → **shard one store per run_id**
  (answers HLD Q5); never share a writable SQLite file across concurrent runs.
- **INFO-1** — GPU embeddings + recomputed retrieval stacks atomic-reduction + BLAS FP
  non-determinism (neutralized if retrieval is a logged effect, M3).
- **INFO-2** — Confirm `run_id`/timestamps are descriptive metadata only — never inputs to RNG,
  effect keys, or state hashes.

## Cross-channel guidance (the spine)
1. **Choose the effect key FIRST — recommend STRUCTURAL `(day, phase, agent_id, call_purpose)`** —
   it decouples replay from both concurrency (H1) and encoding (M1) fragility.
2. **One Effects boundary or none** — it must cover agent + GM + **evaluator** + embeddings +
   environmental RNG + clock + any parse-repair call. Partial coverage passes on a dev box, leaks
   in the batch.
3. **Silent corruption > crashes** — C1 + H1 + M3 compose into a no-error wrong-world replay.
4. **Provenance ≠ replay-soundness** — REQ-0001 audit and REQ-0006 equivalence need different
   mechanisms (content-aware audit vs state-hash compare-point).
5. **Determinism class splits by surface** — agents stochastic-recorded; GM + evaluator deterministic.

## Recommended fix sequence
(1) Structural effect key (C2). (2) Divergence oracle / state hash (C1) — makes the class testable.
(3) Evaluator + embeddings + env RNG into the Effects boundary (C3, H5, M3). (4) Concurrency
strategy + RNG sub-stream isolation (H1, H2). (5) Split determinism class; pin GM + evaluator (H3).
(6) Extend RunManifest (H4). (7) Canonical encoding + remaining low/info.

**Highest-leverage single move:** define one `Effects` substitution boundary (structural key) +
per-step state hash — partially/fully closes C1, C2, C3, M1, M3, INFO-2 and forces H1/H2.
