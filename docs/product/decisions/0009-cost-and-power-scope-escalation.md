# PDR-0009 — Cost & experimental-power scope (ESCALATION — owner-gated)

Date: 2026-06-29   Status: **proposed — awaiting owner**   Author: Claude (product-owner agent)   Owner sign-off: **REQUIRED (spend clause)**
Related: REQ-FABLE-0020/0022, solution-review H1/H2/C4, vision.md (spend clause), initial-assessment R8

## Context
The solution review quantified the escalation that was qualitatively baked into the plan: the
~$50/batch autonomous envelope realistically bounds only Stage-0 pilots. A full Stage-1 run is
order ~10^3 LLM calls/run before evaluation (~$15–20/run at ~$0.01/call), and replication is
≥30 *per condition* across several arms (baseline + no-reflection + tribe-only + any world-policy
variant), plausibly **120–300 runs → ~$2k–$6k**, i.e. 1–2 orders of magnitude over the envelope.
Two experimental-power decisions are coupled to this budget and are the owner's to make, because
they trade evidential strength against spend.

## The decisions requiring the owner
1. **Stage-1 budget ceiling.** What total spend is authorised for the first Stage-1 results? This
   directly sets the realised replication count (PDR-0008 power analysis) and therefore the
   statistical strength of the headline claim.
2. **World-policy neutrality (review C4).** Either (a) **include a 2-level world-policy factor**
   (benevolent-reciprocity vs harsh-scarcity) so policy-sensitivity is estimable — roughly *doubles*
   run count and cost but materially strengthens defensibility; or (b) **pre-register the first
   claim as conditional on a single `world_policy_id`** + ship a world-policy rationale document —
   cheaper, but the headline is explicitly conditional on one chosen "moral physics."

## Recommendation (for the owner to confirm or adjust)
Phase the spend: (i) Stage-0 pilot within the ~$50 envelope (no escalation needed); (ii) a small
**calibration batch** (~$50–150, single arm, ~10 runs) to measure real per-run cost + evaluator κ +
variance — this *replaces* the order-of-magnitude estimate with measured numbers; (iii) bring a
**precise cost model + a Stage-1 budget request** back to the owner before the full batch, defaulting
to option (b) (single pre-registered policy + rationale doc) for the *first* results, with the
2-level world-policy factor (option a) as a funded sensitivity extension if the budget allows.

## Reversal trigger / status
This PDR stays **proposed** until the owner sets a Stage-1 budget ceiling and chooses (a) vs (b).
Cost-control mechanisms (token caps, prompt-caching of static world/system context, model tiering
for high-volume non-critical calls, evaluator batching) are designed into the harness regardless and
a measured cost model is a Stage-0 exit deliverable. No full Stage-1 batch runs until this is accepted.
