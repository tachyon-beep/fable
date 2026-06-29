# PDR-0007 — The experimental apparatus is first-class; the freeze set includes config artifacts

Date: 2026-06-29   Status: accepted   Author: Claude (product-owner agent)   Owner sign-off: within-strategy (architecture)
Related: HLD §3/§5/§10, REQ-FABLE-0014/0015/0016/0017/0020, solution-review C3

## Context
The solution review found the "evidence half" of the product under-engineered: the apparatus
requirements (neutral-ID prompt side 0014, counterbalancing 0015, held-out tests 0016, control arms
0017, replication+analysis 0020) traced only to §8 prose with no §3 component owner, and the config
artifacts the RunManifest references by id (world-policy table, condition/value cards, event arc,
held-out tests, six-dimension anchors, prompt pack) were excluded from the Stage-0 schema freeze —
freezing the envelope but not the contents.

## The call
1. Add two first-class components to the HLD:
   - **Experiment Orchestrator** — owns counterbalanced condition→tribe assignment across run blocks
     (0015), control-arm configuration (0017), held-out-test administration (0016), and batch
     execution; emits the per-run `RunManifest`.
   - **Analysis module** — owns the mixed-model analysis (0020) and the primary-DV computation
     (per PDR-0008).
2. **Extend the Stage-0 freeze set** beyond the nine I/O schemas to include versioned schemas for
   the config artifacts: world-policy table, condition/value cards, 12-event arc / scene schema,
   held-out-test set, six value-dimension anchors, and prompt pack. Each is **pinned by content
   hash** in the RunManifest (an id string alone can be silently mutated).

## Rationale
The product's definition of done is "harness PLUS the apparatus that turns it into evidence";
half the scope was un-architected. Reproducibility (REQ-0007) is only as strong as the artifacts
the manifest points at, so they must be versioned and hash-pinned, and that must happen before the
freeze — the freeze is the first irreversible commitment.

## Reversal trigger
Revisit if the orchestrator/analysis split proves artificial in build (e.g. analysis is better
owned by an offline notebook than a harness component) — restructure under a follow-on PDR, keeping
the content-hash pinning invariant.
