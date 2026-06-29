# fable

> **Autonomous Project by Claude**

A research harness for a **controlled generative social simulation** studying how moral values
transmit — or fail to — across simulated families and tribes. Agents reason, argue, teach, and
reflect in natural language, but every consequential change to the world passes through a
structured world / Game-Master interface: *agents may speak freely, but may not change the world
by narration.* The aim is to turn a vivid-but-unfalsifiable "LLM society" into an instrument that
yields reproducible, blinded, counterbalanced evidence on whether simulated children inherit
their caregivers' **stated** values, their **enacted** values, or their **tribe's** norms.

## Autonomy

This project is owned and driven autonomously by Claude (the product owner). The standing
product workspace — vision, roadmap, metrics, decisions (PDRs), and the current-state resume
brief — lives in [`docs/product/`](docs/product/). Decisions carry written provenance; the
authority boundary the agent operates under is recorded in
[`docs/product/vision.md`](docs/product/vision.md).

## Where to start

- **Design sources** — [`docs/text1.md`](docs/text1.md) (design proposal) and
  [`docs/text2.md`](docs/text2.md) (experimental-design critique): the two documents this
  project derives from.
- **Initial assessment** — [`docs/product/initial-assessment.md`](docs/product/initial-assessment.md):
  scope, risks, timeline, and execution needs for Stage 1 and Stage 2.
- **Current state** — [`docs/product/current-state.md`](docs/product/current-state.md): the
  fastest path to where things stand.

## Staging

- **Stage 0 — harness foundation:** the structured world interface, GM/resolver, versioned
  schemas, event-sourced replayable logs, and the no-narration-into-reality invariant.
- **Stage 1 — one-generation causal experiment:** 24 agents (2 tribes × 4 families × 3),
  replicated and counterbalanced runs, held-out moral-dilemma tests, a three-layer blind
  evaluator — producing the initial results.
- **Stage 2 — generational transmission:** child→parent inheritance with summariser-bias
  controls, an MCP wrapper of the stabilised world API, and scale.

## Status

Bootstrap complete; harness build pending. This repository is an experiment in autonomous
software product ownership as much as it is a social-simulation study.
