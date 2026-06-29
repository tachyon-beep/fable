# fable — High-Level Design (HLD)

Owner: Claude (product-owner agent)  ·  Date: 2026-06-29  ·  Status: **draft, pre design-review**
Derives from: `docs/text1.md` (proposal), `docs/text2.md` (critique), `docs/product/initial-assessment.md`
Requirements: Plainweave `plainweave:req:FABLE:0001..0022` (cited inline as REQ-FABLE-NNNN)

> This HLD is maintained by the autonomous owner and will be revised after the adversarial
> design-review pass (determinism-and-replay, solution-design, program/QA). Schemas (§5) are the
> first thing frozen for Stage 0; everything else may still move.

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
| **GM / Resolver** | Validates `AgentActionProposal` against the verb set and world rules; resolves outcomes against the frozen **world-policy table**; emits `GMResolution` + `WorldStateDelta`. The trust boundary (REQ-0009). | 0001, 0009, 0013 |
| **Agent Runtime** | Builds the per-agent `AgentObservationPacket`, calls the LLM, parses a structured `AgentActionProposal`. Parents and children. Never sees full state or scores. | 0002, 0003, 0005 |
| **Memory Store** | Per-agent subjective memories with salience/recency; returns retrieved memories for the packet. Optional embeddings (local Ollama `nomic-embed-text`) for relevance ranking. | 0003 |
| **Family Reflection Engine** | After salient events, runs the household scene (after the public scene) yielding `FamilyReflectionRecord`; carries the three inheritance channels; never hands the child a value card. | 0010, 0011 |
| **Scene Scheduler** | Selects scenes; tags each fixed/randomised/contingent; logs contingent trigger rules. | 0012 |
| **Event Log / Audit Ledger** | Append-only, event-sourced JSONL + SQLite index; records all events and LLM I/O for exact replay. | 0006 |
| **Evaluator** | Out-of-band, three layers: rule-based metrics, blind LLM classifier (different model family), human audit sample. Scores actions/speech/reflection separately on six dimensions. | 0018, 0019, 0021 |

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

## 5. Data model — the nine versioned boundary schemas (REQ-FABLE-0008)

Frozen first for Stage 0. Implemented as versioned `pydantic` models; every instance validated at
its boundary; schema versions recorded in the `RunManifest`.

| Schema | Carries (sketch) |
|--------|------------------|
| `AgentObservationPacket` | agent_id, day, location, visible_events[], private_memories_retrieved[], available_actions[] |
| `AgentActionProposal` | action_type (∈ verb set), target?, object?, speech?, private_reasoning_summary? |
| `GMResolution` | action_id, accepted: bool, rejection_reason?, outcome, world_policy_id, resulting_delta_ref |
| `WorldStateDelta` | event_id, source_resolution_id (REQUIRED — no orphan deltas), changes[] |
| `MemoryWrite` | agent_id, text, salience, tags[], day |
| `FamilyReflectionRecord` | family_id, event_id, parent_explanations[], child_question, lesson, rule_change?, child_memory_ref |
| `EvaluatorInput` | observable record (action/speech/reflection) + ground truth; **no condition labels** |
| `EvaluatorScore` | per-dimension scores (6), layer (rule/llm/human), separate action/speech/reflection |
| `RunManifest` | run_id, sim_version, model+version, temp/top_p, seed, event_schedule_id, world_policy_id, condition assignment, evaluator_version, prompt_pack_version, schema_versions |

The **`WorldStateDelta.source_resolution_id` is mandatory** — this is how the zero-hallucination
guardrail (REQ-0001) is enforced mechanically: a log audit asserting every delta has a resolving
action is the Stage-0 exit gate.

## 6. Determinism & replay model (REQ-FABLE-0006, 0007)

Live LLM sampling is **not** bit-reproducible, so reproducibility is two distinct guarantees:

- **Record-replay** — every LLM prompt/response and every GM resolution is in the event log;
  replaying a recorded run reads effects from the transcript and performs **zero live LLM calls**,
  reproducing identical state. (This is the axiom-determinism-and-replay "effects substitution"
  pattern.)
- **Re-instantiation** — the `RunManifest` captures everything needed to launch a fresh,
  *comparable* run (seed for all non-LLM randomness, model+version, temperature, conditions,
  schedule/policy/prompt-pack versions). It does not promise identical text — it promises a
  same-conditions replication.

All non-LLM randomness (scene sampling, world events) draws from a single seeded RNG recorded in
the manifest. warpline tracks change-impact across schema edits; loomweave indexes the growing tree.

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
- **Evaluator (REQ-0018):** rule-based metrics + blind LLM (different model family) + human audit;
  six value dimensions with anchors (REQ-0021); actions/speech/reflection scored separately.
- **Primary DV (REQ-0019):** child independent-action similarity to caregiver **enacted** values
  on held-out dilemmas. **Replication (REQ-0020):** ≥30 (aim 50) seeded runs/condition; mixed model.
- **Pre-registration:** primary DV, primary contrasts, and world-policy table frozen before full
  runs. Full-batch spend (REQ-0022) is the escalation gate to the owner.

## 9. Technology

- **Python** + `pydantic` (versioned schemas), event-sourced **JSONL** logs + **SQLite** index.
- **LLM via OpenRouter**: a capable model for agents+GM; a **different model family** for the
  blind evaluator (REQ-0018) — frozen per `RunManifest`. (Loomweave precedent: `anthropic/claude-sonnet-4.6`.)
- **Embeddings (optional):** local Ollama `nomic-embed-text` (768-dim) for memory relevance.
- **Compute:** API-bound; no GPU on the critical path (CUDA available as an option).
- **Trust boundary:** wardline scan of the GM/parse boundary clean of ERROR (REQ-0009).

## 10. Traceability (REQ → component)

REQ-0001/0013 → GM/Resolver + World Store · 0002 → Agent Runtime (action interface) ·
0003 → Agent Runtime + Memory Store · 0004 → World Store · 0005 → Agent Runtime / Evaluator
boundary · 0006 → Event Log · 0007/0008 → Run Controller + schemas · 0009 → GM boundary
(wardline) · 0010/0011 → Family Reflection Engine · 0012 → Scene Scheduler · 0014–0021 →
Experimental apparatus · 0022 → Run Controller cost accounting.

## 11. Open design questions (for the review pass)

- **Q1 (determinism):** is full transcript record-replay sufficient, or do we also need to pin
  provider-side determinism knobs (seed/temperature=0 for the GM specifically)?
- **Q2 (evaluator circularity):** which concrete model pair minimises shared normative priors
  while keeping cost in envelope?
- **Q3 (scheduler power):** how do we quantify scheduler selection pressure so it doesn't inflate
  the family-reflection effect (beyond the no-reflection control)?
- **Q4 (world-policy neutrality):** how do we choose a *defensible* default world-policy table that
  doesn't pre-bake a moral theory — and how do we report its assumptions?
- **Q5 (scale):** SQLite is fine for one run; is it fine for 50× replicated runs, or do we shard
  per-run stores?
