<!--
TEMPLATE (build mode, Round 2). The chairman composes:
  seat-base (engine) + THIS + tier adapter (engine) + the premise + the author's
  answers to the Round 1 questions + "you are in round 2".
Inlined into each seat's dispatch prompt.
-->

# Round 2 — stress-test the author's answers (you see their answers)

You receive the author's own answers to the Round 1 questions. Test whether they
**hold**: do they contradict each other, assert something without grounding,
hand-wave the part that matters, or quietly skip the question? An **"I don't know" is
not something to attack** — flag it plainly as a learning point. Do not re-litigate
questions the answers genuinely resolved. Where an answer leans on a framework/API
fact, verify it against current docs (Context7 first, web second).

Return **exactly** this schema:

```
HOLDS UP:
  - answers that are grounded and internally consistent
DOESN'T HOLD:
  - answer X contradicts Y / asserts Z without grounding / hand-waves W (be specific)
STILL OPEN:
  - questions the answers didn't actually resolve, incl. any "I don't know"
```
