# Design Review — Solution Design (2026-06-29)

Reviewer: `axiom-solution-architect:solution-design-reviewer` (background agent)
Subject: HLD draft + assessment (RAID) + REQ-FABLE-0001..0022 + text1/text2 + vision
Verdict: **NEEDS-WORK** (revise before Stage-0 schema freeze — not a redesign; the harness half is
strong, the evidence half is under-engineered). Tally: 4 CRITICAL, 3 HIGH, 5 MEDIUM, 3 LOW.
Severity lens: the project's own "blast radius on the evidence."

## CRITICAL (resolve before schema freeze)
- **C1 — GM contradiction: LLM or deterministic resolver?** §9 says "a capable model for
  **agents+GM**" (LLM, shared with agents); §3/§5/§6 describe a deterministic, seeded,
  policy-table resolver with "zero live LLM calls." Can't be both. Resolution determines Q1
  (determinism), R2 (an LLM GM sharing the agent model = actor and adjudicator share priors =
  circularity in *resolution*), and REQ-0001 (a rule-based resolver mechanically guarantees no
  narration-into-reality; an LLM resolver reintroduces story-soup). Structured `action_type`
  does NOT settle it — adjudicating `accuse`/`defend`/`hide`/contested `take` depends on free-text
  speech/target. → **Prefer a rule-based GM** (policy-table + seeded RNG, deterministic,
  replayable, no LLM). If NL adjudication is truly needed, isolate it as a named sub-component, a
  THIRD model family, pinned in the manifest.
- **C2 — Primary DV (REQ-0019) has no operational definition and no required owner.** Undefined:
  how the caregiver *enacted-value vector* is computed (which scores, which events, weighting), and
  the *similarity metric* (cosine? per-dim distance? rank corr?). Pre-registration (the natural
  owner) is only "recommended," so the headline estimand is unpinned. "Enacted values" is itself a
  noisy LLM-derived estimate → doubles measurement noise (feeds H2). → Add a pre-registered
  operational-definition artifact (aggregation rule + similarity metric + anchor→score mapping);
  make pre-registration a **requirement**, not a recommendation; anchor the primary DV on the
  **rule-based + human** layers, LLM judge corroborative only.
- **C3 — Experimental apparatus untraceable + excluded from the freeze gate.** REQ-0014 (prompt
  side), 0015, 0016, 0017, 0020 trace only to §8 prose — no §3 component. No analysis/stats
  component (0020), no batch/experiment orchestrator (0015/0017), no held-out-test administrator
  (0016). Worse: the config artifacts the RunManifest references by id (world-policy table,
  condition cards, event arc, held-out tests, six-dimension anchors, prompt pack) are NOT among
  the nine schemas being frozen — freezing the envelope, not the contents. → Add §3 components
  (Experiment Orchestrator; Analysis module); extend the Stage-0 freeze set to version those
  config artifacts; pin them by **content hash** in the manifest.
- **C4 — World-policy neutrality (Q4) unresolved; one frozen table conditions the whole horse-race.**
  Freezing makes the GM's "moral physics" explicit/reproducible but NOT neutral (text2 §6: "value
  inheritance may be adaptation to the GM's moral physics"). One physics shared by all families →
  if it rewards enacted-consistency or punishes hypocrisy/deception, it inflates the "enacted"
  channel and attenuates stated/tribe — the result becomes an artifact of the chosen table. →
  Either (a) include a 2-level world-policy factor in Stage 1 (benevolent vs harsh), or (b)
  pre-register the claim as explicitly *conditional on world_policy_id=X* + ship a world-policy
  rationale/assumptions deliverable. Decide before freezing 0013.

## HIGH
- **H1 — No cost model; $50/batch is decorative for Stage 1.** No per-call/run/batch arithmetic,
  no token caps, no prompt-caching of static context, no model-tiering specifics, no early-stop.
  Order-of-magnitude estimate: ~10³ calls/run → ~$15–20/run before eval; ≥30/condition × several
  arms → **~$2k–$6k, 1–2 orders over the envelope**. $50 realistically bounds only Stage-0 pilots.
  → Produce a cost-model artifact (Stage-0 exit deliverable); design cost controls (token caps,
  prompt caching, model tiering, evaluator batching); re-scope $50 as Stage-0/pilot, separate
  Stage-1 budget line.
- **H2 — Underpowered / non-independent samples.** "≥30 (aim 50)" is a round number, not a
  pre-registered minimum-detectable-effect from assumed variance/ICC. 8 families share one valley
  (shared events/rumours/council, cross-family contamination) → SUTVA/independence violated; the
  run may be the effective unit. → Derive run count from a pre-registered MDE + ICC; state the
  interference assumption; decide family-vs-run as the unit per contrast.
- **H3 — "Tribe norm" leg rests on n=2 hand-authored cultures.** Counterbalancing separates family
  from tribe, but the tribe-norm channel itself has 2 instances (1 df), confounded with everything
  that differs between River/Stone. → Treat tribe as a fixed 2-level *context*; pre-register
  tribe-norm convergence as **exploratory**; scope claims to "these two cultures."

## MEDIUM
- **M1 — RunManifest incomplete:** add distinct pinned `agent_model`, `gm_model`, `evaluator_model`
  (REQ-0018's "different family" must be enforceable), `embedding_model`. (Converges determinism H4.)
- **M2 — Zero-hallucination metric narrower than the construct:** the orphan-delta audit catches
  ungated *mutation*, not agent **speech** asserting a false world fact that others then believe via
  observation packets or that's written to memory as truth. → Add a provenance check: memory/
  observation facts trace to a logged `public_fact` or resolved delta, never raw speech-as-truth.
- **M3 — OpenRouter has no reliability/recovery design:** no rate-limit/retry/backoff, no
  resume-from-partial-transcript for an interrupted *live* run, no idempotency. (Converges
  determinism M4 snapshot/checkpoint.)
- **M4 — Two unquantified NFRs:** evaluator κ floor (set a number — it's the acceptance criterion)
  and replay-equivalence verification (per-step canonical state hash). (Converges determinism C1.)
- **M5 — Evaluator circularity over-relies on "different family":** frontier models share corpora/
  RLHF. → Primary DV on rule-based + human (LLM corroborative); add a judge-vs-human κ floor +
  same-vs-different-family sensitivity sub-study. (Ties C2.)

## LOW
- **L1** — Optional embeddings unrequired/unpinned (gold-plating + nondeterminism); defer or pin.
- **L2** — weft-suite (warpline/loomweave) heavy for a greenfield tree; keep deferred (wardline at
  the GM boundary is justified).
- **L3** — Q5 (SQLite at 50×) is trivial: shard per `run_id`; answer inline, don't list as a
  research question. (Conversely Q4 deserves the "blocking" status it lacks.)

## What the design does well (named)
Mechanical enforcement of REQ-0001 (required `source_resolution_id` + orphan audit); correct
record-replay vs re-instantiation distinction; strong requirement-backed descoping; defeated
label-leakage (neutral IDs + label-free EvaluatorInput); correctly-placed wardline boundary;
honest RAID register.

## Highest-leverage / risk
C1 (GM nature) is upstream of Q1+R2+the invariant. Highest blast-radius-on-evidence: C4
(world-policy) and C2 (primary-DV definition) — either renders the headline indefensible. Irreversible
risk: the schema freeze — extend the freeze set (C3) BEFORE it. Feasibility risk: H1 — Stage-1 is
plausibly 10–100× the autonomous envelope; the owner can't make the budget call without a cost model.
