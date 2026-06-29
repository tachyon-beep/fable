# PDR-0004 — Create public GitHub remote (owner-directed publish)

Date: 2026-06-29   Status: accepted   Author: Claude (product-owner agent)   Owner sign-off: yes (explicit instruction)
Supersedes: —   Related: vision.md (Authority grant — publish), PDR-0002, README.md

## Context
The owner instructed: "create and push to a remote repo, edit the text to say 'Autonomous Project
by Claude'." Publishing is within the granted authority (PDR-0002 lifted the default public-release
reservation), and the instruction was explicit. Before any world-visible push, the committed set
was scanned for secrets and the visibility/account choices were confirmed with the owner.

## Options considered
1. **Private remote** — pro: safer (not indexable); con: contradicts the showcase intent of the
   "Autonomous Project by Claude" label.
2. **Public remote** — pro: matches the showcase framing and the owner's choice; con: content can
   be cached/indexed even if later changed — so it required a pre-publish secret scan.
3. **Defer / ask more** — rejected: the instruction was explicit; only visibility + account needed
   confirming.

## The call
Created **https://github.com/tachyon-beep/fable** — **public**, owned by the active account
`tachyon-beep`, description "Autonomous Project by Claude". Added `README.md` carrying that label.
Pushed `main` (commits through `5f88e50`). Pre-publish checks: no literal secrets in the committed
tree (only env-var *names* and doc references to the *concept* of tokens); `.env` and `.mcp.json`
(which holds a real federation token) are gitignored and were not pushed.

## Rationale
The owner's instruction + the standing publish grant authorise this. Public matches the showcase
intent; the asymmetric risk of public exposure was mitigated by the secret scan and by confirming
visibility/account rather than guessing. Recording it as a PDR keeps the publish event in the
provenance trail.

## Reversal trigger
Flip the repo to private (or scrub history) immediately if a committed secret is ever discovered,
or if the owner signals the project should not be world-visible. Note: anything already pushed
public may persist in caches/indexes regardless — treat the secret-scan discipline as the real
control on every future push.
