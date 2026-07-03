<!--
TEMPLATE (plan mode, plan-check round — REPLACES writing-plans' solo Self-Review).
The chairman composes:
  seat-base (engine) + THIS + tier adapter (engine) + the SPEC + the chairman's
  DRAFT PLAN (the one plan file under audit; if the spec was split, one dispatch
  per plan file) + "you are in the plan-check round (verify the plan against the spec)".
Inlined into each seat's dispatch prompt. This round audits the chairman's ARTIFACT
(the written plan) — it does not stress-test the author and does not issue a
build/readiness verdict. It is the council analogue of build mode's Round-3 spec-check.
-->

# Plan-check — verify the implementation plan against the spec (you see both)

You receive two things: the **approved spec** and the chairman's **draft
implementation plan** meant to execute it. Your job is a **coverage + executability
audit**, not a fresh critique of the design and not a sign-off. The design was
already settled upstream — do **not** re-open it. Check only whether *this plan*
faithfully and completely implements *this spec*, and whether an engineer with zero
prior context could execute it without hitting a gap.

Check, concretely:

- **Spec coverage.** Walk every requirement, constraint, and non-goal in the spec.
  Each requirement/constraint must map to a task that implements it; each non-goal
  must NOT be silently implemented. Name any requirement with no task.
- **Cross-task consistency.** Types, method signatures, and property names defined
  in an earlier task must match their uses in later tasks (a `clearLayers()` in Task
  3 but `clearFullLayers()` in Task 7 is a defect). If the spec was split into
  multiple plans, check the **shared contract/seam** holds across them — the same
  type isn't redefined divergently on each side.
- **Placeholders / hand-waving.** Flag any "TBD", "add error handling", "handle edge
  cases", "write tests for the above" (without the test), steps that say *what* but
  not *how*, or references to types/functions defined in no task.
- **Grounding.** Where a task leans on a framework/API fact, verify it against
  current docs (Context7 first, web second). Flag a task built on a stale or wrong
  API signature.

Do NOT re-argue the design, propose a different architecture, or add new feature
objections — that is not this round. Flag only gaps between the spec and the plan,
and defects inside the plan.

Return **exactly** this schema:

```
COVERED:
  - spec requirements / constraints that a named task implements correctly
GAPS:
  - spec requirement / constraint with NO task, or a non-goal that leaked in
    (name the specific spec item)
DEFECTS:
  - placeholder / type-signature inconsistency across tasks / step that shows
    what-not-how / undefined reference / stale API (name the specific task)
```
