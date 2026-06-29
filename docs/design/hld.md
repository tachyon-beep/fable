# fable — High-Level Design (HLD)

Owner: Claude (product-owner agent)  ·  Date: 2026-06-29  ·  Status: **v2 — design-review incorporated**
Derives from: `docs/text1.md` (proposal), `docs/text2.md` (critique), `docs/product/initial-assessment.md`
Requirements: Plainweave `plainweave:req:FABLE:0001..0022` (cited inline as REQ-FABLE-NNNN)

> **v2 (2026-06-29):** revised after the adversarial design-review pass. Two independent reviews
> (`docs/design/reviews/2026-06-29-determinism-review.md`,
> `…-solution-design-review.md`) drove the changes recorded in PDR-0005 (deterministic rule-based
> GM), PDR-0006 (reproducibility architecture), PDR-0007 (apparatus is first-class), PDR-0008
> (measurement defensibility). One budget-coupled decision (Stage-1 spend + world-policy factor) is
> escalated to the owner in PDR-0009 and is the only thing blocking full Stage-1 execution. Schemas
> (§5, now incl. config artifacts) are frozen first for Stage 0; everything else may still move.

---

## 1. Purpose & scope

fable is a generative-social-simulation **harness** plus the **experimental apparatus** that turns
it into evidence. Agents reason and converse in natural language; all consequential world change is
mediated by a structured world / Game-Master (GM) interface. The Stage-1 question:

> Under controlled moral stressors, do simulated children's later independent actions resemble
> their caregivers' **stated** values, their **enacted** values, or their **tribe's** norms?

This HLD covers **Stage 0** (the harness foundation) and **Stage 1** (the one-generation causal
experiment). Stage 2 (generational transmission, MCP wrapper, scale) is named where it affects
design seams but not detailed — it is gated behind a stable Stage 1.

## 2. Architectural principles (the invariants)

1. **No narration into reality (REQ-FABLE-0001).** World state changes *only* through a GM that
   validates a structured `AgentActionProposal`. Agent text is cognition and speech, never a
   world mutation. The guardrail is a measured hallucination rate of **zero**.
2. **Partial information (REQ-FABLE-0003, 0004).** Agents see only an `AgentObservationPacket`;
   the world holds objective truth, public facts, and per-agent private facts. Uncertainty and
   rumour are first-class.
3. **Harness-only privilege (REQ-FABLE-0005).** Setting values, modifying reputation, scoring, and
   reading hidden cards are never agent-reachable. Agents never see scores — so they cannot game
   the rubric.
4. **Provenance & replay (REQ-FABLE-0006, 0007).** Every event, proposal, resolution, and LLM
   request/response is recorded; a recorded run replays exactly from its transcript, and a
   `RunManifest` re-instantiates a comparable run.
5. **Measurement before realism (REQ-FABLE-0013, 0014, 0018).** The GM's "moral physics", the
   scene scheduler, and the evaluator are all potential hidden treatments; each is made explicit,
   versioned, and (for the evaluator) blind.

## 3. Component architecture

```
                         ┌──────────────────────────────────────────────┐
                         │                Run Controller                 │  REQ-0007
                         │  (loads RunManifest, drives the day loop)      │
                         └───────────────┬────────────────────────────────┘
                                         │
        ┌───────────────┬───────────────┼───────────────┬───────────────────┐
        ▼               ▼               ▼               ▼                   ▼
  Scene Scheduler   Agent Runtime   GM / Resolver   World State Store    Evaluator
   REQ-0012          REQ-0002/0003   REQ-0001/0013    REQ-0004            REQ-0018 (out-of-band)
        │               │               │               │
        │           Memory Store    World-Policy      Event Log /
        │           REQ-0003        Table (frozen)    Audit Ledger
        │           Family          REQ-0013          REQ-0006
        │           Reflection Eng.
        └─────────── REQ-0010/0011 ──┘
```

| Component | Responsibility | Key REQs |
|-----------|----------------|----------|
| **Run Controller** | Loads a `RunManifest`, seeds all non-LLM randomness, drives the day loop, owns the run lifecycle. | 0007, 0008 |
| **World State Store** | Authoritative physical / social / cultural / family state; objective vs public vs per-agent-private facts. Mutated *only* by applying a `WorldStateDelta` emitted from a `GMResolution`. | 0001, 0004 |
| **GM / Resolver** | **Deterministic, seeded, rule-based — no LLM** (PDR-0005). Validates `AgentActionProposal` at the trust boundary (REQ-0009); resolves outcomes by world-policy-table lookup + seeded RNG; **sole constructor** of `GMResolution` + `WorldStateDelta`. | 0001, 0009, 0013 |
| **Agent Runtime** | Builds the per-agent `AgentObservationPacket`, calls the LLM, parses a structured `AgentActionProposal`. Parents and children. Never sees full state or scores. | 0002, 0003, 0005 |
| **Memory Store** | Per-agent subjective memories with salience/recency; returns retrieved memories for the packet. Optional embeddings (local Ollama `nomic-embed-text`) for relevance ranking. | 0003 |
| **Family Reflection Engine** | After salient events, runs the household scene (after the public scene) yielding `FamilyReflectionRecord`; carries the three inheritance channels; never hands the child a value card. | 0010, 0011 |
| **Scene Scheduler** | Selects scenes; tags each fixed/randomised/contingent; logs contingent trigger rules. | 0012 |
| **Event Log / Audit Ledger** | Append-only, event-sourced JSONL + SQLite index; records all events and LLM I/O for exact replay. | 0006 |
| **Evaluator** | Three layers: rule-based metrics, **blind LLM classifier (different family, temp=0+seed, I/O recorded via the Effects boundary)**, human audit. Scores actions/speech/reflection separately on six dimensions; **primary DV anchored on rule-based + human**, LLM corroborative (PDR-0008). | 0018, 0019, 0021 |
| **Experiment Orchestrator** | Generates counterbalanced condition→tribe assignment across run blocks; configures control arms; administers held-out tests; executes batches; emits each `RunManifest`. | 0015, 0016, 0017 |
| **Analysis** | Mixed-model analysis (run + family random effects); computes the pre-registered primary DV. | 0019, 0020 |

## 4. Control flow — the simulated-day loop

Per `text1.md` step structure, with the critical ordering constraint that **family reflection
follows the public scene** (REQ-FABLE-0010) so we measure interpretation, not just instruction:

1. **World update** — scarcity, illness, rumours, resource changes (seeded).
2. **Observation packets** — each active agent gets its scoped packet (REQ-0003).
3. **Individual intention** — agents choose goals/actions.
4. **Scene scheduling** — scheduler picks scenes, tagged by type (REQ-0012).
5. **Public scenes** — market, council, conflict, work, ritual.
6. **World resolution** — GM validates + applies consequences via the policy table (REQ-0001/0013).
7. **Family scenes** — household reflection on salient events (REQ-0010/0011).
8. **Memory writing** — each agent stores subjective memories.
9. **Reflection** — agents privately update beliefs/lessons.
10. **Evaluation** — out-of-band scoring; agents never see results (REQ-0005/0018).

## 5. Data model — versioned schemas (REQ-FABLE-0008)

Frozen first for Stage 0. Versioned `pydantic` models; every instance validated at its boundary;
versions recorded in the `RunManifest`. **The freeze set is the nine I/O schemas PLUS the experiment
config artifacts** (world-policy table, condition/value cards, 12-event arc / scene schema,
held-out-test set, six value-dimension anchors, prompt pack), each pinned by **content hash** in the
manifest (PDR-0007) — freeze the contents, not just the envelope.

| Schema | Carries (sketch) |
|--------|------------------|
| `AgentObservationPacket` | agent_id, day, location, visible_events[], private_memories_retrieved[], available_actions[] |
| `AgentActionProposal` | action_type (∈ verb set), target?, object?, speech?, private_reasoning_summary? |
| `GMResolution` | action_id, accepted: bool, rejection_reason?, outcome, world_policy_id, resulting_delta_ref |
| `WorldStateDelta` | event_id, **typed source: `agent_resolution` \| `system_resolution`** (REQUIRED — no orphan deltas), changes[] |
| `MemoryWrite` | agent_id, text, salience, tags[], day, **provenance: public_fact/delta ref — never raw speech** |
| `FamilyReflectionRecord` | family_id, event_id, parent_explanations[], child_question, lesson, rule_change?, child_memory_ref |
| `EvaluatorInput` | observable record (action/speech/reflection) + ground truth; **no condition labels** |
| `EvaluatorScore` | per-dimension scores (6), layer (rule/llm/human), separate action/speech/reflection |
| `RunManifest` | run_id, sim_version (**git SHA + dirty**), seed + BitGenerator, distinct **agent_model / evaluator_model / embedding_model** (+ provider, system_fingerprint, full sampling params), event_schedule_id, world_policy_id, condition assignment, **content hashes of config artifacts**, evaluator_version, prompt_pack_version, schema_versions, runtime/lib versions |

Two mechanical guards enforce the no-narration invariant (REQ-0001; PDR-0008): (1) every
`WorldStateDelta` carries a typed source, the **GM is its sole constructor**, and the Stage-0 exit
audit is **content-aware** (a delta's changes ⊆ the changes its resolution sanctioned), not merely a
non-null pointer; (2) memory/observation facts must trace to a logged `public_fact` or a resolved
delta — never to raw agent speech treated as truth (closes the speech-channel contamination path).

## 6. Determinism & replay model (REQ-FABLE-0006, 0007) — see PDR-0006

Live LLM sampling is **not** bit-reproducible, so reproducibility is two distinct guarantees:
**record-replay** (a recorded run replays exactly from its transcript with zero live LLM calls) and
**re-instantiation** (the `RunManifest` launches a fresh *comparable* run). The v1 draft asserted
this without a mechanism; v2 specifies the architecture (PDR-0006):

1. **One `Effects` boundary** — the sole choke point for *all* non-deterministic reads: agent LLM
   calls, **evaluator** LLM calls, embeddings calls, environmental RNG draws, the clock, env reads,
   and any parse-repair/retry call. (The GM is deterministic — §3 — so it is not an LLM effect.) In
   replay it serves recorded responses and re-issues nothing live; an assertion enforces zero live
   recorded-kind calls.
2. **Structural effect key** `(run_id, day, phase, agent_id, call_purpose, attempt)` — decouples
   replay from concurrency and from JSON encoding (chosen over ordinal / hash-of-prompt keys).
3. **Per-step state-hash oracle** — a canonical hash over folded world+memory state at each
   day/phase boundary and each `GMResolution`; replay recomputes and asserts equality. This is what
   makes REQ-0006's "replay exactly" *testable* (a CI property), distinct from the REQ-0001
   provenance audit (which checks sourcing, not equivalence).
4. **Determinism class by surface** — agents = stochastic-recorded (the phenomenon); GM =
   deterministic rule-based (PDR-0005); evaluator = deterministic-as-possible (temp=0 + provider
   seed) and recorded, so the **primary result replays**.
5. **RNG sub-stream isolation** — one named, seed-derived sub-stream per stochastic component
   (scheduler, world-events, tie-breaks); pinned BitGenerator, recorded.
6. **Deterministic-parallel day loop** — agent calls may fan out for throughput, but are joined,
   **sorted by `agent_id`**, then applied and logged in canonical order — never completion order.
7. **Memory retrieval is a recorded effect** (logged retrieved IDs) — avoids the silent-corruption
   mode where a reordered ranking feeds the right response to a now-wrong prompt.
8. **Canonical encoding** — JCS (RFC 8785) for hashed bytes; raw LLM responses stored verbatim.

warpline tracks change-impact across schema edits; loomweave indexes the growing tree.

## 7. Family / inheritance mechanic (Stage 0 build, Stage 1 measurement)

The child is socialised, not programmed (REQ-FABLE-0011). Each family has a hidden value
configuration expressed operationally (REQ-0014), but the child's prompt contains only
**memories and observations** across three channels — observed behaviour, explicit teaching,
emotional framing. The Family Reflection Engine produces the clean causal artefact:

```
event → parent behaviour → parent explanation → child question → correction/reinforcement → child memory
```

This is the unit of analysis. `ritualise` lets a family turn an event into a durable rule/taboo —
value inheritance in narrative form.

## 8. Experimental apparatus (Stage 1)

- **Population:** 2 tribes × 4 families × 3 (Parent A, Parent B, Child) = 24 agents.
- **Conditions:** neutral IDs (REQ-0014), e.g. `C1_congruent_fairness`,
  `C2_stated_fairness_enacted_kin_bias`, `C3_two_parent_conflict`, `C4_survival_pragmatist`;
  **counterbalanced across tribes** over run blocks (REQ-0015).
- **Event arc:** fixed 12-event moral arc (harvest shortfall → outsider theft → secret aid →
  false rumour → collective punishment → medicine shortage → witnessed hypocrisy → cross-tribe
  friendship → sacred-site dispute → guilty family member → rival disaster → rite of passage).
- **Held-out tests (REQ-0016):** novel-surface dilemmas with the same latent structure, parents
  absent; the rite of passage is a held-out test, not just drama.
- **Controls (REQ-0017):** no-family-reflection, tribe-only, congruent-vs-hypocritical.
- **Evaluator (REQ-0018):** rule-based metrics + blind LLM (different family, recorded) + human
  audit; six dimensions with anchors (REQ-0021); actions/speech/reflection scored separately;
  **primary DV anchored on rule-based + human, LLM corroborative** (PDR-0008).
- **Primary DV (REQ-0019):** child independent-action similarity to caregiver **enacted** values on
  held-out dilemmas — with a **pre-registered operational definition** (enacted-vector aggregation +
  similarity metric). **Replication (REQ-0020):** count is **power-derived** (pre-registered MDE +
  ICC), not a round number; budget-coupled (PDR-0009).
- **Tribe** is a fixed 2-level *context* (River/Stone); tribe-norm convergence is **exploratory**,
  scoped to these two cultures (n=2) — no generalisation about "tribal enculturation" (PDR-0008).
- **Pre-registration is a gating requirement** (PDR-0008): primary DV, primary contrasts, and the
  world-policy table frozen before any full run. World-policy neutrality + Stage-1 budget are
  escalated to the owner (PDR-0009).

## 9. Technology

- **Python** + `pydantic` (versioned schemas), event-sourced **JSONL** logs + **SQLite** index.
- **LLM via OpenRouter**: a capable model for **agents**; the **GM is deterministic and uses no LLM**
  (PDR-0005); a **different model family** for the blind evaluator (REQ-0018), pinned temp=0+seed.
  Distinct `agent_model` / `evaluator_model` / `embedding_model` in the manifest. (Loomweave
  precedent: `anthropic/claude-sonnet-4.6`.)
- **Embeddings (optional):** local Ollama `nomic-embed-text` (768-dim) for memory relevance.
- **Compute:** API-bound; no GPU on the critical path (CUDA available as an option).
- **Trust boundary:** wardline scan of the GM/parse boundary clean of ERROR (REQ-0009).

## 10. Traceability (REQ → component)

REQ-0001/0013 → GM/Resolver + World Store · 0002 → Agent Runtime (action interface) ·
0003 → Agent Runtime + Memory Store · 0004 → World Store · 0005 → Agent Runtime / Evaluator
boundary · 0006 → Event Log + Effects boundary · 0007/0008 → Run Controller + schemas · 0009 → GM
boundary (wardline) · 0010/0011 → Family Reflection Engine · 0012 → Scene Scheduler ·
0014 → Agent Runtime + Experiment Orchestrator · 0015/0016/0017 → Experiment Orchestrator ·
0018/0019/0021 → Evaluator · 0019/0020 → Analysis · 0022 → Run Controller cost accounting.

## 11. Design questions — resolved in v2

- **Q1 (determinism):** RESOLVED — GM is deterministic/rule-based (PDR-0005); the evaluator is
  pinned (temp=0+seed) and recorded; determinism class splits by surface (PDR-0006).
- **Q2 (evaluator circularity):** primary DV anchored on rule-based + human (LLM corroborative); a
  different evaluator family + a judge-vs-human κ floor + a same-vs-different-family sensitivity
  sub-study bound it (PDR-0008).
- **Q3 (scheduler power):** scene typing (REQ-0012) + the no-family-reflection control (REQ-0017)
  quantify scheduler / family-scene contribution; contingent trigger rules are logged.
- **Q4 (world-policy neutrality):** **ESCALATED** to the owner (PDR-0009) — single conditional
  policy + rationale doc, or a 2-level world-policy factor; budget-coupled.
- **Q5 (scale):** RESOLVED — shard one SQLite store per `run_id` for the replicated batch.
