# Current State — fable        Checkpoint: 2026-06-29 (design review synthesised)

## The bet right now
Turn the two design docs into a finished product + initial results. Design is reviewed and revised;
the gate before building is the owner's **Stage-1 budget + world-policy decision** (PDR-0009).
North-star: defensible-evidence yield.

## Published
- **Remote:** https://github.com/tachyon-beep/fable — public, "Autonomous Project by Claude".

## Awaiting owner (the one thing blocking full Stage 1)
- **PDR-0009 (ESCALATION):** the full Stage-1 batch is plausibly **~$2k–$6k** (1–2 orders over the
  ~$50 envelope). Two coupled decisions are yours: (1) Stage-1 budget ceiling (sets replication
  count / statistical strength); (2) world-policy neutrality — single conditional policy + rationale
  doc (cheaper) vs a 2-level world-policy factor (~2× cost, stronger). My recommendation: phase it
  — Stage-0 pilot in-envelope, then a ~$50–150 calibration batch to replace estimates with measured
  cost/κ/variance, then a precise budget request. **Nothing full-Stage-1 runs until you sign off.**
- Also useful when convenient: a human evaluator-calibration auditor (κ sample); ratify the two
  `[INFERRED]` vision items.

## Done this session
- Workspace bootstrap + initial assessment (owner's first deliverable) — committed + public.
- **Requirements** REQ-FABLE-0001..0022 baselined in Plainweave (approved, with criteria).
- **HLD v2** (`docs/design/hld.md`) — derived from the docs, then **revised after two adversarial
  design reviews** (persisted under `docs/design/reviews/`).
- **Design decisions PDR-0005..0009:** rule-based deterministic GM; reproducibility architecture
  (one Effects boundary + structural keying + state-hash oracle + determinism-class-by-surface);
  apparatus is first-class (Experiment Orchestrator + Analysis + config artifacts in the freeze
  set); measurement defensibility (operationalised primary DV, pre-registration as a gate, DV
  anchored on rule-based+human, tribe as fixed context); cost/power escalation (PDR-0009).

## Next session, start here
1. **Reconcile the Plainweave requirements baseline to the PDRs** — add requirements for: Effects
   substitution boundary + structural keying; per-step state-hash oracle; determinism class by
   surface; extended RunManifest fields; pre-registration as a gate; content-hash pinning of config
   artifacts; speech-channel provenance guard; power-derived replication. Amend GM (deterministic),
   RunManifest (0007), replication (0020), cost (0022) where the decision refined them.
2. **Create Stage 0/1/2 tracker epics** in filigree; wire IDs into roadmap.md.
3. **Freeze the schema set** (9 I/O + config artifacts) as versioned pydantic models — first code.
4. Begin Stage 0 harness against the REQ-0001 content-aware zero-hallucination exit gate.
5. (Owner-gated) on PDR-0009 sign-off: calibration batch → measured cost model → Stage-1 plan.

## Resources in hand
OpenRouter (model choice mine; agents stochastic, evaluator a different family pinned temp=0; GM
uses no LLM); local Ollama embeddings optional; CUDA optional; full repo control; weft suite
(filigree backlog, plainweave requirements, wardline boundary, loomweave/warpline archaeology).
