<!--
TEMPLATE — not a registered agent. The chairman READS this when composing each
seat's dispatch prompt and applies the row for that seat's tier. One seat per
tier (Fable / Opus / Sonnet / Haiku) for decorrelation. Mode-agnostic.
-->

# Tier adapters — how the chairman tunes each seat

Four tiers per convene (deep-reasoning / top / strong-mid / fast-small). They are **decorrelated by
capability, not independent** — same vendor, same alignment regime. This is an
honest *same-vendor* council: better than one model, not truly independent. Do not
oversell it in synthesis.

The chairman assigns one seat per tier and **adapts the dispatch prompt per the row
below** before inlining `seat-base` + the round template. Tier↔angle assignment per
round is the chairman's call; rotating which tier gets the most load-bearing angle
across rounds is fine.

| Tier | Pin | Lean into | How to tune the prompt | Watch-out |
|---|---|---|---|---|
| **Fable** | `model: fable` | The **single hardest** angle that needs the **longest uninterrupted reasoning chain** — deep multi-step problems where depth beats breadth: a load-bearing assumption whose failure only shows several inferential steps down, a subtle interaction between distant parts of the premise. | **Give it one thing, not many.** Hand it the deepest problem in the premise and ask it to reason all the way to the bottom — no compactness pressure on the *thinking*, only on the write-up (bullets in the schema, but the chain behind them should be exhaustive). Do not fan its attention across breadth; that is Sonnet's job. | Slowest and most expensive seat — reserve it for the one angle that actually rewards depth; don't spend it on routine gaps. Can over-elaborate the write-up — restate the compactness cap on **output**, not on reasoning. |
| **Opus** | `model: opus` | The most **ambiguous, load-bearing** angle; subtle contradictions in the framing. Where Fable goes *deep* on one thread, Opus catches the *ambiguity* others gloss. | Least hand-holding. Hand it the part of the premise that is hardest to ground and trust it to follow the thread. | Can over-elaborate — restate the compactness cap (bullets, not essays). |
| **Sonnet** | `model: sonnet` | Breadth — covering the obvious-but-important gaps reliably. | Balanced default. Give it the wide sweep so nothing routine slips through. | None notable; solid generalist. |
| **Haiku** | `model: haiku` | Fast, concrete, surface-level gaps and naming the un-named risk. | **Tighten and concretize.** Re-state explicitly, in its prompt: "ask questions, do not issue a verdict" and "pressure ≠ evidence." Keep the premise framing short; ask for fewer things at once. | **Caves more under authority / sunk-cost pressure (measured in this project).** In synthesis, report its softer take as **one** position — **never average toward it.** |

**Concrete models the pins target (current generation).** The `model:` pins are aliases;
each resolves to the latest in its family — **Fable 5** (`claude-fable-5`), **Opus 4.8**
(`claude-opus-4-8`), **Sonnet 5** (`claude-sonnet-5`), **Haiku 4.5**
(`claude-haiku-4-5`). The Sonnet seat defaults to **Sonnet 5**. If you need to pin a seat
to an exact build, dispatch it with the full model ID instead of the alias.

**Graceful degradation.** If a tier can't be reached, drop that seat and run the
remaining ones — and **say so** in the synthesis. Never silently collapse two seats onto
one model, and never run a one-seat "council." (Fable is the most likely to be
unavailable or slow; falling back to the Opus/Sonnet/Haiku three is a valid degraded run
as long as it's named as such.)
