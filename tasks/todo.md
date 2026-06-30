# Add macro-clarification + custom seat roster to elenchus-build

## Goal
Before Round 1, the **chairman** (main thread) should:

1. **Ask macro clarifying questions one-by-one IN CHAT** to build a *macro vision* of
   the project, so the council seats — who are strong on architecture/tools/logic but
   **rarely touch frontend** — ask better-grounded questions covering more aspects.
   Topics: platform (web / mobile / desktop / CLI / multiplatform), frontend stack,
   backend & services, target users / scale, greenfield vs existing. Offer to dispatch
   **elenchus-study** when a framework choice is undecided (benchmark on community feedback).
2. **Propose a grounded seat roster** as a SEPARATE question after the clarifying ones:
   how many seats + which model mix + a **per-seat lens** (e.g. "2 opus on frontend
   because…, 4 sonnet on backend because…, 1 haiku verifying macro alignment / missing
   aspects…"). Reasoning must be grounded in the user's answers, not guessed. User
   approves or specifies manually.

Then dispatch that approved roster, injecting the macro vision into every seat's prompt.

## Key design decisions (pin down — confirm before I build)
- **Clarifying Q&A is in-chat, one question at a time** (not one markdown file per
  question). But it IS recorded into the existing checkpoint markdown, maintaining the
  "who asked / who answered" format — appended as each answer comes in, before any /clear.
- **Roster overrides the engine default.** Engine hardcodes "one seat per tier
  (opus/sonnet/haiku)." Build mode replaces that with the **user-approved roster**:
  variable seat count, any model mix, each seat carrying a **lens**. Honest-labeling
  (same-vendor, not truly independent) and graceful-degradation rules still apply.
- **Lens is injected at dispatch**, not baked into a new template. The chairman adds the
  seat's assigned lens + the macro vision to the composed Round-1 prompt. Round-1 template
  gets a short LENS/MACRO-CONTEXT note so seats stay inside their lens while holding the
  macro view. No engine round-schema changes.
- This is a **build-mode-only** change (study/gather keep their own pre-round flows).
  Engine SKILL.md gets one small note that a front end MAY supply a custom roster;
  the loop, anonymization, synthesis, gate are untouched.

## Decisions (confirmed with user)
- Roster: **propose freely + one-line cost note**, user trims.
- Decorrelation: **lenses decorrelate within a tier** (repeated tiers OK if lenses differ);
  honest-labeling note stays.

## Todo
- [x] Add `## Macro clarification (before Round 1)` to `elenchus-build/SKILL.md`
- [x] Add `## Seat roster (proposed, then approved)` section
- [x] Update `## Premise shaping` to hand into macro clarification (don't dispatch yet)
- [x] Update `templates/round-1-questions.md` with LENS + MACRO-CONTEXT injection note
- [x] Checkpoint frontmatter: `platform`, `macro:` block, `seats:` as `{model, lens}` list;
      Clarifying Q&A body section
- [x] Engine `elenchus-council/SKILL.md`: note that a front end MAY supply a custom roster
- [x] `## Common mistakes`: skipping clarification, fixed-3 without roster, question dump,
      duplicate tier w/o distinct lens
- [x] Mirror all edits to repo archive (verified in sync via diff)
- [x] **GREEN:** spot-test a frontend-lens seat — PASSED (see Review)

## Review — done

**What changed (build mode now runs a chairman-led pre-Round-1 phase):**
- **Macro clarification** — before dispatching, the chairman asks macro questions **one at a
  time in chat** (platform, frontend stack, backend/services, users/scale, greenfield),
  records each into the checkpoint's new *Clarifying Q&A* section as it lands, and **offers
  elenchus-study** when a framework is undecided. Purpose: give the seats a macro vision so
  they cover the **frontend they normally skip**, not just the backend.
- **Seat roster (proposed → approved)** — a separate step after clarification. The chairman
  proposes a grounded count + model mix + **per-seat lens** (frontend / backend slice /
  integrations / macro-alignment) with reasoning tied to the user's answers, propose-freely
  + one-line cost note. User approves or specifies. This **overrides the engine's fixed
  opus/sonnet/haiku trio**; repeated tiers are allowed when each carries a distinct lens.
- **Lens + macro context injected at dispatch** — Round-1 template gained a LENS/MACRO-CONTEXT
  note; no new round schema. Checkpoint frontmatter gained `platform`, a `macro:` block, and
  `seats:` as a `{model, lens}` roster list.
- **Engine** got one note: a front end MAY supply a custom roster overriding one-per-tier;
  loop/anonymization/synthesis/gate untouched.

**Files touched (global runtime + repo archive, verified in sync via diff):**
- `skills/elenchus-build/SKILL.md`
- `skills/elenchus-build/templates/round-1-questions.md`
- `skills/elenchus-council/SKILL.md`

**Testing (writing-skills GREEN):** dispatched one `council-seat` (opus, **frontend lens**,
multiplatform Flutter + Supabase offline premise). It asked frontend-specific Socratic
questions (conflict-resolution UI, draft/autosave survival, Flutter-web offline limits,
queued photo uploads), used the macro context to ground them, cited current docs
(PowerSync/Brick/Supabase Storage TUS), and issued no verdict. Behaves as intended.
A full multi-tier live convene still needs a fresh session (agents register at startup).

**Not committed** (commit-only-when-asked).
