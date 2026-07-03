<!--
TEMPLATE (plan mode, split-suggestion step — REPLACES writing-plans' solo Scope Check).
A SINGLE deep-tier dispatch (Fable; Opus fallback), run BEFORE any plan is written.
The chairman composes:
  seat-base (engine) + THIS + the Fable tier row (engine) + the SPEC
  + "you are producing an advisory split proposal; the chairman returns it to the
     user for approval — you do NOT decide and nothing is written on your say-so".
Inlined into the one seat's dispatch prompt.

WHY one deep seat, not the full council: this is a structural judgment that rewards
one long uninterrupted reasoning chain about the seam between subsystems — the Fable
tier's specialty — not breadth. It is NOT a critique round.

WHY this doesn't violate "no verdict": the seat PROPOSES; the USER disposes. A split
proposal handed back for approval is the engine's surface-don't-certify rule applied
to plan structure — the opposite of self-authorizing a split and writing files.
-->

# Split suggestion — should this spec become one plan or several? (advisory)

You receive the **approved spec**. Reason all the way to the bottom of one question:
**can this spec be implemented as one plan, or should it be split into multiple
independent plans** — each of which produces working, independently testable
software on its own?

This is a **suggestion for the user to approve**, not a decision and not a license
to split. You write nothing; the chairman returns your proposal to the user, who
makes the call. Do not hedge into uselessness, but do not overstate either — if one
plan is right, say one plan.

Reason about, at least:

- **Separable subsystems.** Does the spec name subsystems that own different
  concerns and fail in different ways? Could two engineers build them in parallel
  without stepping on each other?
- **The shared seam (the load-bearing part).** If they ARE separable, what is the
  contract between them — the data model, the API surface, the types both sides
  depend on? An "independent" split that lets each side invent the seam divergently
  is a false split that collides at integration. If a split is warranted, the seam
  almost always needs to be **pinned down first** (its own foundational plan, or a
  frozen contract both plans consume) before the parallel plans begin.
- **Testability of each proposed plan** on its own (e.g. each side mockable without
  the other). Mutual mockability is the real test of "independent" — apply it.
- **Cost of over-splitting.** Don't fragment a small cohesive spec into ceremony.

Return **exactly** this schema:

```
RECOMMENDATION: one plan | N plans (state N and name each)
SEAM:
  - if splitting: the shared contract/data-model/API both sides depend on, and
    whether it needs to be pinned down first (a foundational plan or frozen contract)
RATIONALE:
  - the reasoning: what makes the subsystems separable (or not), the mutual-mockability
    test result, and what each proposed plan delivers independently
RISK IF IGNORED:
  - what breaks if the spec is planned the other way (one big plan / a naive split)
```
