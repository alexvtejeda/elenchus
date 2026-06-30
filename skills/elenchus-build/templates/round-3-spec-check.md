<!--
TEMPLATE (build mode, Round 3 — spec check). The chairman composes:
  seat-base (engine) + THIS + tier adapter (engine) + the full session record
  (premise, Round 1 questions, the author's answers, the Round 2 stress-test result,
  resolved decisions, preserved dissents, open questions, study path) + the chairman's
  DRAFT spec + "you are in round 3 (spec verification)".
Inlined into each seat's dispatch prompt. This round audits the chairman's ARTIFACT —
it does not stress-test the author and does not issue a readiness verdict.
-->

# Round 3 — verify the spec draft against the session record (you see both)

You receive two things: the **session record** (the premise, the questions, the
author's answers, what held and didn't hold under stress-test, the decisions that got
settled, the dissents that were preserved, the open questions, and the study path) and
the chairman's **draft spec** meant to pin all of that down for the brainstorming stage.

Your job is a **fidelity audit**, not a fresh critique and not a sign-off. Check that the
draft is a faithful, complete record of what this session actually established:

- **Every settled decision** in the record appears in the spec, with the reasoning that
  survived stress-test — not flattened to a bare assertion.
- **Every open question and every "I don't know"** is carried forward as still-open, not
  silently dropped or quietly resolved.
- **Every preserved dissent** stays a dissent in the spec — both positions and the
  condition under which each wins. A split smoothed into "agreed" is a defect.
- **No invented certainty:** the spec must not state as decided anything the session left
  open, nor overstate how grounded a framework/API choice is.

Do NOT re-open questions the session resolved, and do NOT add new objections — that is
not this round. Flag only gaps between the record and the draft.

Return **exactly** this schema:

```
CAPTURED FAITHFULLY:
  - decisions / answers / constraints the spec records accurately and completely
MISSING:
  - decision / answer / constraint / open question / dissent in the record that the
    spec dropped or under-states (name the specific item)
MISREPRESENTED:
  - where the spec states something the session did not settle, smooths a preserved
    dissent into agreement, or overstates certainty (quote the spec line, cite the record)
```
