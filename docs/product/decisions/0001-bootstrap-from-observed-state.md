# PDR-0001 — Bootstrap the product workspace from observed state (reframed by owner)

Date: 2026-06-29   Status: accepted   Author: Claude (product-owner agent)   Owner sign-off: yes (reframe given in-session)
Supersedes: —   Related: vision.md, roadmap.md, metrics.md, PDR-0002

## Context
A fresh `/own-product` run found no workspace, no commits, and one placeholder tracker issue
(`fable-6b7a3c9248` "Future", P4, planning). The only direction signal was two documents in
`docs/`: `text1.md` (a design proposal for a hybrid LLM social simulation — 2 tribes × 4
families × 3 members, structured-action world interface, family-reflection mechanic, staged
v0→v1→v2) and `text2.md` (a sharp experimental-design critique reframing the work into Stage 0
pilot → Stage 1 one-generation causal experiment → Stage 2 generational). A bootstrap forces
a framing call now so the next session resumes from written state, not memory.

## Options considered
1. **Frame as a research instrument only** (Stage 0 "prove the harness" as the headline) —
   pro: matches the critique's caution; con: the owner wants a *finished product and results*,
   not just a validated pilot.
2. **Frame as product + results, staged Now/Next/Later** — pro: faithful to both docs and to
   the owner's explicit mandate ("turn the two documents into a finished product and initial
   set of results"); con: more scope to own.
3. **Do nothing / chat without writing** — rejected: bootstrap's entire purpose is durable state.

## The call
Option 2. The owner answered "Different framing" to the Stage-0-as-Now question and clarified
the mandate: fable is a product to be built and run to completion, yielding a finished harness
*and* an initial set of results. Now = the initial assessment (owner's first deliverable) +
Stage 0 harness foundation; Next = Stage 1 causal experiment (the initial results); Later =
Stage 2 generational transmission, MCP wrapper, scale. North-star = defensible-evidence yield.

## Rationale
The staging is the critique's own recommendation, so it is source-grounded rather than invented.
Making the north-star an *outcome* (defensible evidence) rather than "harness built" dodges the
build trap. The architectural invariant (no narration-into-reality) becomes the hard guardrail
because every downstream claim depends on it. Audience, the research-instrument purpose, and the
Now bet are explicitly tagged [INFERRED] in vision.md where they were reconstructed.

## Reversal trigger
Revisit this framing if: (a) the owner rejects or materially edits `initial-assessment.md`'s
scope; (b) the primary causal question changes; or (c) the architectural invariant proves
unenforceable in the Stage 0 pilot (hallucination rate cannot be driven to 0), which would
force a redesign of the world interface before any Stage 1 commitment.
