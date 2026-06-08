---
artifact: next-session-handoff
purpose: "Single entry point to resume the Elenchus build after a context clear."
read_first: true
---

# Next session — kickoff for building `elenchus-build`

**Status:** Elenchus v0.1 design is closed (`ready: true`). This session designed it by running
the council on itself. Next phase: implement the `elenchus-build` front end on the engine.

## Read these, in order
1. `docs/2026-06-02-elenchus-build-summary.md` — **the spec / source of truth.**
2. `docs/2026-06-01-elenchus-readiness-session.md` — the decision log (categories A–E, resolved).
3. `.claude/skills/elenchus-council/SKILL.md` + `.claude/agents/council-seat.md` — the engine (v0).
4. (Background) `docs/2026-06-01-elenchus-phase0-baseline.md`, `…-dogfood-architecture-critique.md`.

## ⚠️ Reconcile the engine with the refined spec (the committed engine is partly stale)

The engine was written before the design was refined. Before/while building the front end,
update `elenchus-council` to match the build summary:

1. **Conclusion gate.** Engine currently emits a READY/REFINE/NOT-READY *verdict*. Refined design:
   **the judge flags contradictions/gaps but does NOT certify readiness** — readiness is the
   user's self-declared call. Reframe the gate to "surface questions + flag contradictions," no
   readiness verdict.
2. **Round 2 semantics.** Engine does *all-pairs peer review* (seats critique each other's
   answers) — the dogfood found this the weakest, most expensive step. Refined flow: **R1 = seats
   generate Socratic questions from the premise; the user answers; R2 = seats stress-test the
   user's answers.** Replace all-pairs peer review with answer-stress-testing.
3. **What gets anonymized.** Shift from anonymizing seat *answers* to anonymizing the *questions*
   presented to the user (strip which seat asked).
4. **Checkpoint + resume.** Add (front end): markdown checkpoint file w/ frontmatter; **write
   state during the round**; resume = **scan-on-invoke** (skill Reads the file), not a
   SessionStart hook; never rely on SessionEnd (~1.5s).
5. **Context7 MCP.** Add to the seats' tools (currently Read/Grep/Glob/WebSearch/WebFetch) for
   up-to-date framework/API facts and a grounded study path.
6. **Scope (description/triggers).** In scope: readiness/study [primary] + benchmarking tools /
   weighing approaches [secondary]. **Out of scope:** over-engineering/flaw *verdicts* (one
   high-tier model handles those).
7. **Dispatch caveat.** The `council-seat` agent isn't dispatchable mid-session (agents register
   at startup) — document an install-then-restart step in the deployment notes.

## Validation harness (scaffold ready; baseline run pending)

`docs/validation/harness.md` formalizes the phase-0 scenarios into 6 re-runnable **fixtures**
(S1–S4 from the baseline + S5 sound-premise / no-manufactured-doubt + S6 degraded-dispatch),
each with scripted answers, scored against the **spec invariants** (I1–I10) — not the
committed engine. **The baseline run has not been executed yet.** Running it doubles as a check
on the reconciliation list above (the spec-invariant rubric will flag the stale READY verdict
and all-pairs Round 2). It also becomes the yardstick for the planned *relentless / adaptive*
redesign (hybrid pool→one-at-a-time questioning; recommended answers only AFTER the user
answers) — see the delta protocol in the harness.

**Kickoff line for the baseline run:**
> "Read docs/validation/harness.md and run the baseline: convene elenchus-council on fixtures
> S1–S6 with their scripted answers, fill the scorecard, and save it to
> docs/validation/runs/2026-06-02-baseline.md."

## Kickoff line for the fresh session
"Read docs/2026-06-02-next-session-handoff.md and build the elenchus-build front end."
