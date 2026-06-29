# PDR-0008 — Measurement defensibility: operationalise the primary DV, gate on pre-registration

Date: 2026-06-29   Status: accepted   Author: Claude (product-owner agent)   Owner sign-off: within-strategy (method)
Related: REQ-FABLE-0018/0019/0020/0021, solution-review C2/M5/H3/M2, text2.md

## Context
The solution review found the single most important measurement — the primary DV (REQ-0019) —
operationally undefined and unpinned (pre-registration was only "recommended"), the evaluator's
defensibility over-reliant on "different model family", the tribe-norm leg generalising from n=2
cultures, and the zero-hallucination metric blind to speech-channel contamination.

## The call
1. **Operationalise the primary DV** in a pre-registered artifact: the caregiver enacted-value
   vector aggregation rule (which scores, which events, weighting), the child action vector, the
   similarity metric, and the anchor→score mapping. The headline number must be computable as
   specified.
2. **Pre-registration is a gating REQUIREMENT, not a recommendation** — primary DV, primary
   contrasts, world-policy table, and replication target are frozen before any full Stage-1 run.
   (This will be added to the Plainweave requirements baseline.)
3. **Anchor the primary DV on the rule-based + human evaluator layers**; the blind LLM judge is
   **corroborative/secondary**. Add a judge-vs-human κ floor (a number, set at pre-registration)
   and a small same-family-vs-different-family sensitivity sub-study to bound circularity.
4. **Tribe is a fixed 2-level context, not a sampled factor.** Tribe-norm convergence claims are
   **exploratory** and scoped to "these two cultures" (River/Stone) — no generalisation about
   "tribal enculturation" from n=2.
5. **Broaden the zero-hallucination guard:** beyond the orphan-delta audit (gated mutation), add a
   provenance check that memory/observation facts trace to a logged `public_fact` or a resolved
   delta, never to raw agent speech treated as truth (the speech-channel contamination path).
6. **Replication count is derived, not assumed:** the ≥30/aim-50 placeholder is replaced by a
   pre-registered minimum-detectable-effect + assumed ICC/variance-component power analysis; the
   within-run interference (SUTVA) assumption is stated and the unit (family vs run) chosen per
   contrast. (The realised count is budget-coupled — see PDR-0009.)

## Rationale
"Defensible-evidence yield" is the north-star; an undefined estimand, an unpinned design, and an
LLM judging an LLM make it unreachable no matter how clean the engineering. These changes convert
the apparatus from "produces numbers" to "produces falsifiable, owned, pre-registered numbers."

## Reversal trigger
Revisit the rule-based/human anchoring if the human κ sample shows the rule-based layer fails to
capture a value dimension (then that dimension leans on human/LLM with a documented caveat); revisit
the power-derived count if the pilot's measured variance differs materially from the pre-registered
assumption.
