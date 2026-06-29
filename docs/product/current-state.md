# Current State — fable        Checkpoint: 2026-06-29 (post-bootstrap, design in progress)

## The bet right now
Turn the two design docs into a finished product + initial results. Immediate work: requirements
+ HLD + adversarial design review → freeze schemas → build Stage 0. North-star: defensible-evidence yield.

## Published
- **Remote:** https://github.com/tachyon-beep/fable — **public**, "Autonomous Project by Claude"
  (PDR-0004). `main` tracks `origin/main`.

## In flight
- **Design review** — two specialist reviewers running in background against the HLD + requirements:
  determinism-and-replay reviewer, and solution-design reviewer. Findings to be synthesised → HLD
  revision before schema freeze.
- **HLD** — `docs/design/hld.md` drafted (pre-review), traces every component to REQ-FABLE IDs.

## Done this session
- Workspace bootstrap (vision/roadmap/metrics/current-state) + PDR-0001..0004.
- **Initial assessment** (`initial-assessment.md`) — the owner's first deliverable: scope, RAID
  risks, timeline (Stage 1+2), execution needs. Committed + public.
- **Requirements baselined in Plainweave:** `plainweave:req:FABLE:0001..0022` — all approved with
  acceptance criteria. 0001 = the no-narration invariant; 0002–0012 harness (Stage 0);
  0013–0021 experiment (Stage 1); 0022 cost control.
- **HLD** drafted with traceability + open design questions Q1–Q5.
- Public GitHub remote created + pushed; README = "Autonomous Project by Claude".

## Open questions / blocked-on-owner (none block Stage 0)
- **Stage-1 budget sign-off** — full replication (≥30 runs) will exceed ~$50/batch (REQ-0022);
  I bring a cost model before any full run.
- **Human calibration auditor** for evaluator κ (REQ-0018) — you or a delegate?
- **Pre-registration sign-off** (recommended) — freeze primary DV, contrasts, world-policy table.
- **Ratify [INFERRED] vision items** (audience, research-instrument purpose).

## Resources in hand
OpenRouter API (model choice mine; loomweave precedent `anthropic/claude-sonnet-4.6`); local Ollama
embeddings (`nomic-embed-text`, 768-dim) for memory retrieval; CUDA optional; full repo control;
weft suite (filigree backlog, plainweave requirements, wardline boundary, loomweave/warpline archaeology).

## Next session, start here
1. **Synthesise the two design-review reports** (background agents) → revise HLD + requirements;
   resolve any blocking item among Q1–Q5.
2. **Freeze the 9 boundary schemas** (HLD §5) as versioned pydantic models — the first Stage 0 code.
3. **Create Stage 0/1/2 tracker epics** in filigree; wire IDs into roadmap.md; consider a Plainweave
   baseline once requirements survive review.
4. Begin Stage 0 harness: World Store + GM/resolver + action interface + event log + minimal agent
   runtime + record-replay, against the REQ-0001 zero-hallucination exit gate.
5. Choose + pin the agent/GM vs. blind-evaluator model pair for RunManifest (REQ-0018).
