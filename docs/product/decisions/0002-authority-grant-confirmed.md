# PDR-0002 — Authority grant confirmed and widened by owner

Date: 2026-06-29   Status: accepted   Author: Claude (product-owner agent)   Owner sign-off: yes (explicit, in-session)
Supersedes: —   Related: vision.md (Authority grant), PDR-0001

## Context
Bootstrap requires a confirmed authority grant before the agent acts autonomously. The agent
proposed the default grant (autonomous within strategy; escalate vision/grant change, public
release, depended-on-feature deprecation, pricing, data deletion, external parties) via a
structured question, and asked for a per-batch LLM-API spend envelope.

## Options considered
1. **Default grant, publish reserved** — the structured answer chosen ("Adopt default grant");
   escalate every public release/announcement. Pro: conservative; con: contradicts the owner's
   later, explicit free-text grant of publish autonomy.
2. **Owner-widened grant: full autonomy incl. commit/push/publish** — pro: matches the owner's
   governing instruction ("full autonomy including when to commit, when to push and when to
   publish"); con: removes a normally-reserved gate, so it must be recorded deliberately.

## The call
Option 2. The owner's free-text mandate is the later and more specific statement and explicitly
names publish, so it governs: the agent is autonomous on commit, push, and publish within this
project. Spend is bounded by the owner's structured answer: **~$50 per experiment batch**
autonomous; above that, escalate (the spend clause survives — it was answered specifically and
not overridden by the free-text). Irreversible data ops outside the working tree and obligations
to external third parties remain reserved.

## Rationale
User instructions take precedence over defaults; widening a grant is the owner's prerogative and
here it was made explicitly and in-session, satisfying the operating model's rule that a grant
change is owner-gated. Recording it as a PDR (not a silent vision.md edit) preserves the
provenance the workspace exists to keep. The two specific reservations retained (out-of-tree
data deletion, external-party obligations) are the genuinely irreversible/outward edges the
owner did not address, so they default to escalate.

## Reversal trigger
Re-confirm at the monthly grant review (next: 2026-07-29) or immediately if the owner signals
the publish/commit autonomy should narrow, or if a near-miss occurs (e.g. an experiment batch
trends toward the $50 ceiling unexpectedly), prompting a spend-envelope revisit.
