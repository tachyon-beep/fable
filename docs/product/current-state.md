# Current State — fable        Checkpoint: 2026-06-29 (Stage 0 build started)

## The bet right now
Build the Stage 0 harness (tracker epic **fable-1c6ca715c5**). Design is reviewed + frozen
(HLD v2, PDR-0005..0008). Full Stage-1 execution is gated by the owner's budget decision (PDR-0009).
North-star: defensible-evidence yield.

## Published / built
- **Remote:** https://github.com/tachyon-beep/fable (public). Latest commit `35ddc00`.
- **Code (Stage 0 foundations):** `uv` project (src layout, strict mypy, ruff, pytest). Boundary
  schemas — `FableModel` base, `ActionType` verb set + `AgentActionProposal` (REQ-0002),
  `Change`/`GMResolution`/`WorldStateDelta` with typed source + mandatory `source_resolution_id`
  (REQ-0001). **Content-aware zero-hallucination audit** (`fable.audit`, REQ-0001/PDR-0008):
  orphan + unsanctioned-change detection, 12 tests green, ruff+mypy clean, wardline exit 0.

## Awaiting owner (does NOT block Stage 0)
- **PDR-0009 (ESCALATION):** Stage-1 full batch ≈ $2k–$6k. Need a budget ceiling + world-policy
  choice (single conditional vs 2-level factor). Recommended: pilot → ~$50–150 calibration batch →
  precise budget request. Nothing full-Stage-1 runs until signed off.
- Human evaluator-calibration auditor (κ); ratify the two `[INFERRED]` vision items.

## Stage 0 task status (epic fable-1c6ca715c5, 15 tasks)
- ✅ Project scaffold + tooling (fable-a69c7725d2) — closed.
- ◐ Freeze 9 I/O schemas (fable-28d369e68d) — 3 of 9 done (action, resolution, delta). Remaining:
  AgentObservationPacket, MemoryWrite, FamilyReflectionRecord, EvaluatorInput, EvaluatorScore, RunManifest.
- ◐ Content-aware audit (fable-c59e57eb84) — delta-audit done + tested; speech-channel provenance
  guard pending (needs memory/observation schemas).
- ☐ Config-artifact schemas, Effects boundary, event log, world store, rule-based GM, state-hash
  oracle/replay, agent runtime, memory store, family reflection, scheduler, run controller, pilot.

## Next session, start here
1. Finish the remaining 6 I/O schemas + config-artifact schemas (content-hash pinned) — TDD.
2. Effects boundary (structural keying, record/replay) + event log (JSONL+SQLite, JCS for hashes).
3. World store + **rule-based GM** — **annotate wardline trust boundaries** here (REQ-0009; the
   taint gate is currently INERT, noted on task fable-cf421e38b8) so the gate actually enforces.
4. State-hash divergence oracle + replay loop; then agent runtime, memory, reflection, scheduler,
   run controller; then the 12-agent pilot vs the zero-hallucination exit gate.
5. **Reconcile the Plainweave requirements baseline to PDR-0005..0009** (new reqs: Effects boundary,
   state-hash, determinism-class, RunManifest fields, pre-registration gate, content-hash pinning,
   speech-channel provenance, power-derived replication) — still outstanding from the design synthesis.
6. (Owner-gated) on PDR-0009 sign-off: calibration batch → measured cost model → Stage-1 plan.

## Resources in hand
OpenRouter (model choice mine; agents stochastic, evaluator different-family temp=0, GM no-LLM);
local Ollama embeddings optional; CUDA optional; full repo control; weft suite. Build: `uv run pytest`,
`.venv/bin/ruff check src tests`, `.venv/bin/mypy`, `wardline scan . --fail-on ERROR`.
