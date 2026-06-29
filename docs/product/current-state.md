# Current State — fable        Checkpoint: 2026-06-29 (bootstrap, pre-commit)

## The bet right now
Produce the **initial assessment** (scope / risks / timeline for Stage 1 + Stage 2 + execution
needs) — the owner's first and only requested deliverable — then derive the **high-level design**
and stand up the Stage 0 harness foundation. North-star it serves: defensible-evidence yield.

## Published
- **Remote:** https://github.com/tachyon-beep/fable — **public**, "Autonomous Project by Claude"
  (PDR-0004). `main` tracks `origin/main`. README carries the label.

## In flight
- **Initial assessment** — written + committed → `docs/product/initial-assessment.md` (draft for
  owner review). Owner deliverable; gates the build. Folds in the operational/continuity support
  the owner offered.
- **Workspace bootstrap** — vision/roadmap/metrics/current-state + PDR-0001 (framing),
  PDR-0002 (grant), PDR-0003 (scope extension + resources), PDR-0004 (public release) committed
  (genesis `91b875d`, README `5f88e50`, pushed to origin).

## Open questions / blocked-on-owner
- **Confirm the reconstructed framing** in `vision.md` (audience, research-instrument purpose) —
  tagged [INFERRED]; owner reframed the Now bet in-session but the full vision is not yet ratified.
- **Stage-1 spend escalation (the one baked-in gate):** full replication (≥30 runs) will likely
  exceed the ~$50/batch envelope → I will bring a cost model + batch plan for sign-off before any
  full run. Does NOT block Stage 0.
- **Human calibration auditor** for the evaluator κ sample — a hard Stage-1 dependency; confirm
  who (owner or delegate).
- **Pre-registration sign-off** (recommended): freeze primary DV, contrasts, world-policy table
  before full runs.

## Resolved this session
- **Authority:** full repository control + commit/push/publish + model-choice autonomy +
  ~$50/batch spend envelope (PDR-0002, PDR-0003). Reserved: spend > $50/batch, out-of-tree
  irreversible data ops, external-party obligations.
- **Resources:** OpenRouter API key copied into the gitignored `.env`; loomweave embeddings
  server available; CUDA available as an option. Model choice delegated to me.
- **Ownership extended:** I now own the system requirements and the high-level design derived
  from `docs/text1.md` + `docs/text2.md`.

## Last checkpoint did
- Bootstrapped the workspace; reconstructed framing from the two source docs.
- Wrote the five artifacts + PDR-0001/0002/0003; produced the initial assessment.
- Confirmed + recorded the owner-widened/extended grant; provisioned LLM + embeddings access.

## Next session, start here
1. Get owner acceptance / edits on the assessment + the [INFERRED] vision items.
2. **Derive the high-level design** (`docs/design/hld.md`) from the two docs — now an owned
   artifact — and the system requirements; this is the first Stage-0 step.
3. Create Stage 0/1/2 tracker epics (filigree) and wire IDs into `roadmap.md`.
4. Dispatch the adversarial design-review pass (determinism-and-replay + solution-design +
   program/QA) against the HLD + the 9 schemas, then freeze schemas and begin Stage 0.
5. Choose + pin the model pair (agents+GM vs. blind evaluator) for `RunManifest`.
