# Vision — fable

> **Bootstrap note (2026-06-29).** This workspace was *reconstructed* from two design
> documents (`docs/text1.md`, a design proposal; `docs/text2.md`, an experimental-design
> critique), an empty git history, and a single placeholder tracker issue. Items tagged
> **[INFERRED]** were derived, not found, and are assumptions to confirm. The framing was
> revised by the owner this session (see PDR-0001) and the authority grant widened by the
> owner (see PDR-0002).

## Purpose
fable exists to **build a working generative-social-simulation harness and run it to produce
a defensible initial set of results on moral-value transmission.** Agents reason, argue,
teach, and reflect in natural language, but every consequential interaction with the world
passes through a structured world/Game-Master interface — agents may speak freely, but may
not change the world by narration. The change fable makes: it turns a vivid-but-unfalsifiable
"LLM society" into an instrument that yields *reproducible, blinded, counterbalanced* evidence
about whether simulated children inherit their caregivers' **stated** values, their **enacted**
values, or their **tribe's** norms.

## Who it serves
- **Primary:** the researcher-owner running value-transmission experiments — the person who
  needs the harness to exist *and* needs the results it produces. **[INFERRED]** The docs
  never name an audience; this is reconstructed from their content and the owner's mandate.
- **Secondary:** other social-simulation / LLM-agent researchers who could reuse the harness
  or build on the results. **[INFERRED]**
- **Explicitly not:** an entertainment game, an open-ended chatbot world, or a production
  multi-tenant service. fable is a research instrument first; engineering quality serves
  measurement, not a user-facing app.

## Anti-goals (what it refuses to be) — grounded in the source docs
- **A pure-text "story-soup" world.** World state changes only through validated structured
  actions resolved by the GM; narration never mutates reality. (`text1.md` core rule.)
- **A simulation agents can game.** Agents never see their own value scores or the evaluator;
  scoring is out-of-band and harness-only. (`text1.md` "what I would not do".)
- **A prompt-inheritance experiment in disguise.** A child is never handed the parent's value
  card directly; it must infer values from observed behaviour, explicit teaching, and emotional
  framing. (`text1.md`/`text2.md`.)
- **A morality play with real-world labels.** No real political, religious, or ethnic labels;
  tribes/families are neutral constructs to avoid confounds and sensitivity. (`text1.md`.)
- **A single elaborate "world" mistaken for evidence.** One impressive run is not a result;
  replication, counterbalancing, and held-out tests are non-negotiable for any causal claim.
  (`text2.md`.)

(Deferring MCP, intergenerational transmission, and extra value dimensions are *sequencing*
choices — see `roadmap.md` Later — not anti-goals.)

## Authority grant
Granted by: the repo owner (qacona@gmail.com)     Last reviewed: 2026-06-29
Review cadence: monthly, or on any vision/strategy/grant change
Provenance: PDR-0002 (owner widened the default grant) + PDR-0003 (owner extended to full
repository control and provisioned resources), both this session.

Autonomous within strategy — the agent MAY, without asking:
  prioritize the backlog, write PRDs, dispatch delivery to sub-agents, accept against
  criteria, reprioritize, kill a failing bet per metrics.md, **commit, push, and publish**
  within this project, **create / edit / delete any file in the repository** (including the
  system requirements and the high-level design this agent derives from `docs/` and maintains),
  **choose the LLM model(s)** the harness uses, and **run experiment batches costing up to
  ~$50 each**.

Escalate BEFORE acting — the agent MUST get owner sign-off for:
  changing this vision/strategy/grant itself; **any single experiment batch or paid action
  expected to exceed ~$50** (the spend clause); deleting data or any irreversible data
  operation **outside the project's own repository/working tree**; anything that obligates the
  owner to an external party (contracts, paid third-party services beyond the already-provisioned
  LLM API, regulators).
  (Taxonomy + rationale: product-ownership-operating-model.md. The default's public-release
  reservation is intentionally LIFTED — the owner granted publish + full in-repo autonomy.)
