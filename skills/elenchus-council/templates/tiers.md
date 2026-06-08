<!--
TEMPLATE — not a registered agent. The chairman READS this when composing each
seat's dispatch prompt and applies the row for that seat's tier. One seat per
tier (Opus / Sonnet / Haiku) for decorrelation. Mode-agnostic.
-->

# Tier adapters — how the chairman tunes each seat

Three tiers per convene (top / strong-mid / fast-small). They are **decorrelated by
capability, not independent** — same vendor, same alignment regime. This is an
honest *same-vendor* council: better than one model, not truly independent. Do not
oversell it in synthesis.

The chairman assigns one seat per tier and **adapts the dispatch prompt per the row
below** before inlining `seat-base` + the round template. Tier↔angle assignment per
round is the chairman's call; rotating which tier gets the most load-bearing angle
across rounds is fine.

| Tier | Pin | Lean into | How to tune the prompt | Watch-out |
|---|---|---|---|---|
| **Opus** | `model: opus` | The most ambiguous, load-bearing angle; longest chains of reasoning; subtle contradictions. | Least hand-holding. Hand it the part of the premise that is hardest to ground and trust it to follow the thread. | Can over-elaborate — restate the compactness cap (bullets, not essays). |
| **Sonnet** | `model: sonnet` | Breadth — covering the obvious-but-important gaps reliably. | Balanced default. Give it the wide sweep so nothing routine slips through. | None notable; solid generalist. |
| **Haiku** | `model: haiku` | Fast, concrete, surface-level gaps and naming the un-named risk. | **Tighten and concretize.** Re-state explicitly, in its prompt: "ask questions, do not issue a verdict" and "pressure ≠ evidence." Keep the premise framing short; ask for fewer things at once. | **Caves more under authority / sunk-cost pressure (measured in this project).** In synthesis, report its softer take as **one** position — **never average toward it.** |

**Graceful degradation.** If a tier can't be reached, drop to two seats and **say so**
in the synthesis — never silently collapse two seats onto one model, and never run a
one-seat "council."
