# fable — Initial Assessment: Scope, Risks, Timeline & Execution Needs

Author: Claude (product-owner agent)  ·  Date: 2026-06-29  ·  Status: **draft for owner review**
Sources: `docs/text1.md` (design proposal), `docs/text2.md` (experimental-design critique)
Related: `vision.md`, `roadmap.md`, `metrics.md`, PDR-0001, PDR-0002

---

## 0. Executive summary

fable is a **generative-social-simulation harness** plus the **experimental apparatus** that
turns it into evidence. Agents reason and converse in natural language; every consequential
world change is mediated by a structured world / Game-Master (GM) interface — *agents may speak
freely but may not change the world by narration.* The product is finished when the harness
runs reproducibly **and** has produced an initial, defensible set of results answering one
sharp causal question:

> **Under controlled moral stressors, do simulated children's later independent actions
> resemble their caregivers' *stated* values, their *enacted* values, or their *tribe's* norms?**

The design (`text1.md`) is architecturally strong; the critique (`text2.md`) is right that it is
not yet a clean *experimental* design. This assessment adopts the critique's staging —
**Stage 0 (engineering pilot) → Stage 1 (one-generation causal experiment) → Stage 2
(generational transmission)** — and scopes Stage 1 and Stage 2 in full per the owner's request.

**Headline judgement.** Stage 0 + Stage 1 is a *medium* build (a focused single-language harness,
not a platform) carrying *high experimental-design risk* and *moderate cost risk*. The dominant
risks are not "can we write the code" — they are **(a)** keeping the world-state-hallucination
rate at zero, **(b)** an evaluator that doesn't grade its own normative priors (circularity),
**(c)** the GM and scheduler acting as hidden treatments, and **(d)** full-replication API spend
exceeding the autonomous envelope. Stage 2 is deferred and gated: it adds a *second model* (a
developmental summariser) that can silently become the real inheritance mechanism, so it is only
sound after Stage 1 is stable.

> **One escalation is baked into the plan.** Producing the initial results *is* the product, and
> that requires running the full replicated Stage-1 batch (≥30 runs). The arithmetic (24 agents ×
> ~12 events × 3 phases × multi-call scenes × ≥30 seeds) will almost certainly exceed the
> **~$50/batch autonomous spend envelope**. So the headline result cannot begin until the owner
> approves an experiment budget — I will bring a cost model and a batch plan for sign-off before
> any full run (R8, §5). Stage 0 (the harness + 12-agent pilot) is fully inside the envelope and
> needs no escalation.

---

## 1. Scope

### 1.1 In scope — the product

**Engineering (the harness).** A Python harness with versioned schemas at every boundary:
- **Run Controller** — drives a run from a `RunManifest` (seed, model, temperature, condition
  assignment, schedule id, world-policy id, evaluator + prompt-pack versions).
- **World State Store** — the authoritative physical/social/cultural/family state; public vs.
  hidden facts per event.
- **GM / Resolver** — validates proposed actions and decides outcomes against an explicit,
  pre-registered **world-policy table** (the "moral physics"), not ad-hoc.
- **Agent Runtime** — parents and children act only via a small structured action verb set
  (`observe, speak, ask, give, take, hide, accuse, defend, punish, forgive, trade, teach_child,
  family_reflect, council_vote, private_reflect, ritualise`); each agent sees only an
  **observation packet**, never full world state.
- **Memory Store** — subjective, per-agent retrieved memories (salience/recency).
- **Family Reflection Engine** — schedules the post-event household scene that produces the
  clean causal artefact: *event → public behaviour → parental explanation → child question →
  child memory*, across three inheritance channels (observed behaviour, explicit teaching,
  emotional framing).
- **Scene Scheduler** — fixed / randomised / contingent scenes, each **tagged by type** so
  analysis can separate agent effects from scheduler selection pressure.
- **Event Log / Audit Ledger** — append-only, event-sourced; records every LLM input/output so
  a run is **replayable from the recorded transcript**.
- **Evaluator** — three layers: rule-based event metrics (objective: who took medicine, who
  lied), a **blind** LLM classifier (blind to family-condition labels), and a **human audit
  sample** for calibration. Scores actions, speech, and reflections separately.

**Schemas to freeze first (versioned):** `AgentObservationPacket`, `AgentActionProposal`,
`GMResolution`, `WorldStateDelta`, `MemoryWrite`, `FamilyReflectionRecord`, `EvaluatorInput`,
`EvaluatorScore`, `RunManifest`.

**Experiment (Stage 1).**
- Population: 2 tribes × 4 families × 3 members = **24 agents** (Parent A, Parent B, Child).
- **Neutral condition IDs** (no loaded labels in prompts): e.g. `C1_congruent_fairness`,
  `C2_stated_fairness_enacted_kin_bias`, `C3_two_parent_conflict`, `C4_survival_pragmatist`.
- **Counterbalance** family conditions across tribes (rotate across run blocks) so tribe culture
  is estimable separately from family treatment.
- Fixed 12-event moral arc + **held-out adolescent tests** with the same latent structure but
  novel surface (the rite of passage becomes a held-out test, not just drama).
- **Controls:** no-family-reflection arm; tribe-only arm; congruent vs. hypocritical parent arm.
- **Pre-registration:** primary dependent variable, the small set of primary contrasts, and the
  world-policy table are frozen *before* the full runs.
- **Replication:** ≥30 (aim 50) seeded runs; analysed with a mixed model (child action vector ~
  parent enacted/stated + tribe norm + scarcity + conflict + hypocrisy + run/family random effects).
- **Primary DV:** child independent-action similarity to caregiver *enacted* values on held-out
  dilemmas. Speech/reflection are secondary.
- Initial **6 value dimensions:** kin loyalty, tribal loyalty, truth/deception, mercy/punishment,
  authority/obedience, survival pragmatism.

**Deliverable for Stage 1:** the harness + a written results report answering the primary
question with the pre-registered contrasts, plus the full run dataset and replay logs.

### 1.2 In scope — Stage 2 (gated, deferred)
- **Child → parent transformation:** generate the next-generation parent profile from the
  child's accumulated memories/actions — tested against controls (human-written profile,
  LLM-generated, **no-memory**, and **direct-card-inheritance** upper bound) so the *summariser*
  is not mistaken for inheritance.
- Second child generation; **frozen** world policy + event schedule to isolate compounding drift.
- **MCP wrapper** of the stabilised world API (tools for consequential actions, resources for
  read-only state, prompts for scene templates); harness-only tools (`set_value`,
  `modify_reputation`, `score_my_values`, `read_parent_hidden_card`) never exposed to agents.
- Scale: 4-member families (sibling divergence), more value dimensions, **multi-model
  replication** as a blocking factor.

### 1.3 Explicitly out of scope (v1)
Full open-world simulation; pure-text world state; >2 tribes; many children per family at first;
elaborate council politics / mythology that can dominate family effects; live dashboards; any
real-world political/religious labels. (These are `vision.md` anti-goals or Later-sequencing.)

---

## 2. Architecture & technology choice

- **Language:** Python. Rationale: the docs specify "native Python/JSON first"; richest LLM SDKs;
  `pydantic` gives versioned, validating schemas cheaply; the experiment is API-bound, not
  CPU-bound, so Rust's advantages don't apply yet. (Re-evaluate only if run throughput becomes a
  bottleneck.)
- **Persistence:** event-sourced JSONL logs + a small embedded DB (SQLite) for queryable run
  state and the audit ledger. (axiom-embedded-database pack applies.)
- **Embeddings / memory retrieval:** the Memory Store returns salient/relevant memories per
  observation packet; the owner-provisioned loomweave **embeddings server** can power that
  relevance ranking (and the evaluator's semantic classification) instead of a hand-rolled scorer.
- **Compute:** the critical path is **API-bound — no GPU required**. **CUDA cores are available**
  (subject to being free) as an *option* if local embeddings, local open-weight models (to cut
  high-volume call cost), or local multi-model replication later prove worthwhile — not a dependency.
- **Determinism / replay (critical nuance):** live LLM sampling is *not* bit-reproducible. So
  "reproducibility" means two distinct, achievable guarantees: **(1) record-replay** — every LLM
  prompt/response and every GM resolution is logged, so a *recorded* run replays exactly from its
  transcript; **(2) re-instantiation** — the `RunManifest` captures everything needed to launch a
  fresh *comparable* run (seed for all non-LLM randomness, model+version, temperature, condition
  assignment, schedule + policy + prompt-pack versions). The axiom-determinism-and-replay pack and
  the warpline tooling are directly in play here.
- **Trust boundary:** LLM output is *external input* crossing into structured world actions — a
  wardline trust-boundary concern. Action proposals are validated/sanitised at the boundary (the
  GM), never trusted into the sink (the world store).

---

## 3. Risk register (RAID)

Severity = impact if unmitigated × likelihood. Validity risks are rated by *blast radius on the
evidence*, per the critique.

| # | Risk | Sev | Mitigation | Owner gate? |
|---|------|-----|------------|-------------|
| R1 | **World-state hallucination** — agent narration silently treated as real, corrupting every downstream claim | **High** | Hard invariant: state changes only via validated `GMResolution`; Stage 0 success gate = 0 hallucinations across the pilot; automated log-audit asserting no `WorldStateDelta` lacks a resolved action | — |
| R2 | **Evaluator circularity** — same normative priors drive agents, GM, and judge | **High** | 3-layer evaluator; **different model** for the blind judge than for agents/GM; rule-based objective metrics as the spine; human audit sample for κ calibration; judge blind to condition labels | needs human auditor |
| R3 | **GM as hidden treatment** — the resolver quietly teaches a moral theory (mercy pays, deception is caught) | **High** | Pre-register an explicit **world-policy table** (consequence distribution per action class) before runs; later treat "world harshness" as a deliberate factor | freeze before runs |
| R4 | **Scheduler bias** — over-sampling drama / over-crediting family reflection | Med | Tag every scene fixed/random/contingent; log trigger rules; the no-family-reflection control quantifies the family-scene effect | — |
| R5 | **Confounded tribe × family** — culture vs. family treatment inseparable | **High** | Counterbalance family conditions across tribes over run blocks; estimate tribe effect separately | freeze design before runs |
| R6 | **Underpowered / non-independent samples** — 8 families in one valley ≠ 8 independent observations | **High** | Replication is mandatory (≥30, aim 50 seeds); run-seed = replication unit, family = unit-within-run; mixed-model analysis | — |
| R7 | **Loaded family labels leak into prompts/eval** — model performs hypocrisy instead of developing it | Med | Neutral operational condition IDs; evocative names kept out of prompts and evaluator inputs | — |
| R8 | **API spend overrun** — 24 agents × ~12 events × 3 phases × ≥30 runs of multi-call scenes can exceed the ~$50/batch envelope | **High** | Cost-model before full runs; batch sizing; cheaper model for high-volume non-critical calls; **full Stage-1 replication likely exceeds $50/batch → escalate** | **yes — spend clause** |
| R9 | **Replay nuance misunderstood** — expecting bit-reproducibility from live LLM calls | Med | Document record-replay vs. re-instantiation explicitly (§2); enforce RunManifest completeness as a guardrail | — |
| R10 | **Stage-2 summariser becomes the real mechanism** — child→parent compression dictates "inheritance" | **High (Stage 2)** | Defer to Stage 2; gate behind summariser-bias control arms (human / LLM / no-memory / direct-card) | freeze before Stage 2 |
| R11 | **Scope creep** — mythology, council politics, dashboards, extra dimensions pulled into v1 | Med | `vision.md` anti-goals + Later-band discipline; 6 value dimensions cap; PDR any expansion | — |
| R12 | **Tooling friction** — the weft suite (loomweave/warpline/legis/wardline/filigree) is heavy for a young codebase | Low | Adopt incrementally: filigree for backlog now; wardline at the LLM→action boundary; loomweave/warpline once the tree has mass | — |

**Assumptions:** capable LLM API access exists (✓ OpenRouter provisioned); the owner (or a
delegate) can provide a human calibration-audit sample; local compute suffices (no GPU on the
critical path — inference is API-side; CUDA available as an option).
**Dependencies:** model choice + budget ceiling (owner); human auditor (owner/delegate);
pre-registration sign-off (owner, optional but recommended).
**Issues (open now):** exact provider/model per role undecided; total budget undecided.

---

## 4. Timeline (Stage 1 and Stage 2)

This is an **agent-driven** build (me + dispatched specialist sub-agents; owner assists with
checkpoints/context), so the schedule is expressed as **phased milestones with effort bands and
the uncertainties that actually drive wall-clock** — not date-theatre. The dominant schedule
drivers are: run cadence, evaluator calibration loops, and owner-review/escalation turnaround.
Calendar dates are **provisional** and firm up on acceptance.

| Phase | Milestone (exit artifact) | Effort band | Key dependency / gate |
|-------|---------------------------|-------------|------------------------|
| **A. Assess** (now) | This assessment accepted; framing ratified; tracker epics created | S | owner review |
| **B. Stage 0 — harness foundation** | Frozen schemas; world store + GM/resolver + action interface + event log + minimal agent runtime + record-replay; **12-agent pilot with 0 hallucinations, schema-valid replayable logs** | **L** | R1 gate must pass before Stage 1 |
| **C. Stage 1 — experiment build** | Scene scheduler (tagged); world-policy table; neutral family conditions + counterbalancing; held-out test set; 3-layer evaluator + calibration harness; RunManifest; pre-registration doc | **L** | R2/R3/R5 frozen; human auditor lined up |
| **D. Stage 1 — execute & analyse** | Pilot batch → evaluator κ ≥ target → **full replicated runs (≥30)** → mixed-model analysis → **initial results report** | **M–L** | **R8 spend escalation**; calibration loop |
| **E. Stage 2 — generational + MCP + scale** | child→parent with control arms; 2nd generation; MCP wrapper; scale levers | **L–XL** | only after Stage 1 stable (R10) |

Effort bands: S ≈ a short focused session; M ≈ a few sessions; L ≈ a substantial multi-session
chunk; XL ≈ the largest. **Critical path:** A → B (R1 gate) → C (design freeze) → D (the spend
escalation + calibration are the two most likely stalls) → results. Stage 2 (E) is off the
critical path to the *initial results* and begins after D is accepted.

**Provisional calendar anchors** (revise on acceptance): Stage 0 pilot green by ~mid-July 2026;
first Stage-1 results by ~end-Oct 2026; Stage 2 entry only after that. These are intent, not a
commitment — `/axiom-program-management` owns any dated forecast.

---

## 5. What I need to execute

**From the owner (project decisions / inputs):**
1. **Model + API access — RESOLVED this session.** The owner provisioned an **OpenRouter** key
   (copied into the gitignored `.env`) and delegated model choice to me. OpenRouter reaching many
   model families makes the R2 mitigation cheap: a capable model for agents+GM and a **different**
   family for the blind evaluator, frozen at Stage-1 pre-registration and pinned in each
   `RunManifest`. A loomweave **embeddings server** is also available (see §2). No further owner
   action needed here.
2. **Total experiment budget** and the ceiling above the ~$50/batch envelope. The **full Stage-1
   replication will almost certainly exceed $50/batch** — I will produce a cost model and bring the
   batch plan back for sign-off (R8) before spending.
3. **A human calibration auditor** (you or a delegate) for the evaluator κ sample — a hard Stage-1
   dependency (R2). Small annotation task on a subset of traces.
4. **Pre-registration sign-off** (recommended): freeze primary DV, primary contrasts, and the
   world-policy table before full runs — a methodological gate that makes the results defensible.
5. **Ratify the [INFERRED] vision items** (audience, research-instrument purpose) — quick confirm.

**From the owner (operational / continuity — the support you offered):**
- **Checkpoint cadence.** I run `/product-checkpoint` at the end of each working session (and
  before any escalation) to commit the workspace; you've offered to assist with checkpoint
  management. Proposed default: checkpoint at each phase boundary (A→B→C→D→E) and on any stall.
- **Sub-agent fan-out vs. solo.** I work solo on linear engineering and the product calls;
  I **fan out to specialist sub-agents** for (a) the pre-build adversarial design review
  (determinism-and-replay, solution-design, program/QA), (b) parallelisable build chunks (schema
  set vs. evaluator vs. scheduler), and (c) independent verification of results. You manage
  context/handoff between independent agents per your offer.
- **Stall recovery.** If a turn stalls, the durable workspace (`docs/product/` + tracker) is the
  recovery point — any session resumes cold from `current-state.md`. Your offer to intervene on
  stalls is the backstop; checkpoints keep the blast radius of a stall to one phase.
- **Tooling-evaluation angle.** Noted that I may be interviewed on tooling challenges; R12 tracks
  weft-suite friction and I'll log concrete pain points as they arise.

**Already in hand (no action needed):** Python toolchain; **OpenRouter API access** (multi-model);
loomweave **embeddings server**; **CUDA** as an option; full repository control + model-choice
autonomy (PDR-0003); the weft suite (filigree for the backlog, wardline for the LLM→action trust
boundary, loomweave/warpline for code archaeology and change-impact as the tree grows, legis for
git/CI governance); the specialist agent roster (determinism-reviewer, solution-design-reviewer,
program/QA reviewers, embedded-database architect) which I will dispatch to pressure-test the
design before building. Storage for logs is negligible.

---

## 6. Recommendation & immediate next steps

Proceed on the staged plan. The architecture is sound; the work that determines success is
**experimental-design discipline**, not raw coding. Concretely, on acceptance:

1. Create Stage 0/1/2 tracker epics (filigree) and wire IDs into `roadmap.md`.
2. Dispatch a short adversarial design-review pass (determinism-and-replay + solution-design +
   program/QA reviewers) against this assessment and the schema set, then revise.
3. Freeze the 9 schemas and begin Stage 0 — schemas first, then GM/resolver, then the 12-agent
   pilot against the R1 (zero-hallucination) gate.
4. Bring the Stage-1 cost model + batch plan back for the spend escalation before any full run.

**Open escalations to the owner:** model/budget decision (R8), human auditor availability (R2),
and pre-registration sign-off. None block starting Stage 0; all block starting Stage 1 execution.
