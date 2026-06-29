# PDR-0003 — Owner extends scope to full repository control; provisions LLM + embeddings

Date: 2026-06-29   Status: accepted   Author: Claude (product-owner agent)   Owner sign-off: yes (explicit, in-session)
Supersedes: —   Related: vision.md (Authority grant), PDR-0002, initial-assessment.md

## Context
After confirming the initial grant (PDR-0002), the owner extended scope and provisioned resources
across several in-session messages: (1) "full and unrestricted control of the repository" —
explicitly including adding/changing/removing **system requirements** and maintaining the
**high-level design** derived from the two source docs; (2) authorization to copy the
`OPENROUTER_API_KEY` from `~/elspeth/.env`; (3) "choose your model of choice"; (4) a loomweave
**embeddings server** is available on the server when wanted.

## Options considered
1. **Keep the narrower grant; ask per-action** — pro: maximal caution; con: contradicts the
   owner's explicit, repeated widening and would stall an autonomous mandate.
2. **Record the extension: full in-repo authority + resource provisioning** — pro: matches the
   owner's governing instructions; keeps the genuinely irreversible/external edges reserved;
   captures provenance so the grant is inspectable. Con: broad authority, so it must be deliberate.

## The call
Option 2. The agent now has **full control of the repository** (create/edit/delete any file,
own the requirements and the HLD), **model-selection autonomy** over the harness, and a
**provisioned OpenRouter key** (copied into the gitignored `.env`; `.env` confirmed gitignored so
commit/push autonomy cannot leak it). The loomweave embeddings server is available for code
semantic search and as an option for the harness memory store's salience/relevance retrieval and
the evaluator's semantic classification. Reserved (escalate): spend > ~$50/batch; irreversible
data ops *outside* the repo working tree; obligations to external third parties beyond the
already-provisioned LLM API.

## Rationale
User instructions override defaults, and these were explicit and repeated. Full in-repo authority
is consistent with retaining the out-of-tree / external reservations because everything in-repo is
versioned and reversible via git — the audit trail the workspace depends on still holds. Recording
the model-choice autonomy here means the eventual model decision (a capable model for agents+GM, a
*different* family for the blind evaluator — R2 mitigation, now trivial via OpenRouter) is a
within-strategy call I own, to be frozen at Stage-1 pre-registration.

## Reversal trigger
Re-confirm at the monthly grant review (next: 2026-07-29), or immediately if the owner signals the
authority should narrow, or if a secret-leak near-miss occurs (e.g. `.env` ever becomes
un-ignored), which would force a credentials-handling revisit before the next commit.
