---
name: finishing-implementation-elenchus
description: >-
  Use when a frontend feature has been implemented and you want to verify it actually
  works in the running browser against its spec/plan — then fix what doesn't —  before
  calling it done. Triggers: "verify my implementation works", "check the frontend
  against the spec", "did I actually build everything", "finish and verify this feature",
  "run the finishing pass". The post-execution stage of the Elenchus pipeline. NOT for
  stress-testing a build premise (elenchus-build), NOT for writing or verifying a plan
  (elenchus-plan), and NOT a code-style review.
allowed-tools: Agent, Read, Write, Edit, Grep, Glob, Bash, WebSearch, WebFetch, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# Finishing implementation (verify → fix loop)

The **post-execution** stage of the Elenchus pipeline
(`elenchus-build → brainstorming → elenchus-plan → execution → THIS`). After a frontend
feature is built, this runs a bounded **verify→fix loop**: report-only verifier subagents
drive the running app with **Playwright MCP** and report what passed / failed / needs a
human / is missing; the **chairman (this thread) implements the fixes** one by one; repeat.

**Separation of concerns is the whole design:**

- **Verifier subagents** (`finishing-verifier`, a no-Write sandbox) **only verify → report.**
  They drive the browser and return a fixed schema. They never touch code.
- **The chairman** reads the reports, reconciles them against the checklist, and
  **implements the fixes.** Verification and repair never live in the same agent.

Built with the `writing-skills` skill. It is **not** an anonymized council — verifiers
aren't debating a premise, they're observing a browser. (The two-verifier default gives
cross-checking, not Socratic dissent.)

## The loop

```
running app + spec/plan
  │
  ▼
[Precondition gate] confirm the app is running + its URL. NEVER start the dev server.
  │   If the port isn't open, ask the user to confirm the URL; require it before pass 1.
  ▼
[Derive checklist] one testable item per named feature (route/page/interaction +
  │   expected observable outcome). This is what every verifier checks.
  ▼
[Config gate — ONCE] propose {iterations (default 3), verifier structure (default two
  │   cross-checked: Sonnet + highest tier)}; user confirms/edits; then run unattended.
  ▼
[Fix-pass ×N] ── verify (dispatch configured verifiers, SEQUENTIALLY) ──► each drives the
  │              browser through the WHOLE checklist, returns PASSED/FAILED/NEEDS-HUMAN/
  │              MISSING + evidence ──► chairman MERGES (flag disagreements) + RECONCILES
  │              every item ──► chairman IMPLEMENTS fixes one by one (FAILED + MISSING)
  ▼
[Final confirm pass] one more verification, NO fixes — captures post-fix reality
  ▼
[Report] docs/elenchus/<slug>-finishing.md: per-item results across passes, the fixes the
        chairman made, verifier disagreements, and what remains NEEDS-HUMAN.
```

## Precondition gate (before anything)

- **The user runs the dev server; you never start it.** (Project convention.) Ask the user
  to confirm the URL. If the port isn't open, say so and ask for the right URL — do not
  launch a server, do not guess.
- A quick `Bash` reachability check (e.g. `curl -sI <url>`) is fine to confirm it's up. If
  it isn't reachable, stop and get a working URL first — a run against a dead URL produces
  only NEEDS-HUMAN.
- **Confirm the Playwright MCP is actually connected BEFORE dispatching** — run
  `claude mcp list` and check `playwright` shows `✔ Connected`, not `⏸ Pending approval`.
  A verifier dispatched while the server is pending gets **no `browser_*` tools** and can
  only return NEEDS-HUMAN (wasting the dispatch). If it's pending/missing, have the user
  approve it and install the browser (see Install) and **restart** — then dispatch.

## Derive the acceptance checklist

From the spec + plan, write **one testable item per named feature**: the route/page or
interaction, and the **expected observable outcome** in the browser. This is the contract
every verifier checks and the chairman reconciles against — so nothing is silently skipped.

## Configuration gate (once, then unattended)

Propose the run config and let the user edit it, **once**, after the checklist:

- **Iterations:** `N` fix-passes (default **3**) **plus one free final no-fix confirm pass**
  (a run does `N+1` verifications).
- **Verifier structure:** default **two independent, cross-checked** verifiers per pass —
  **Sonnet** and the **highest tier** (`model: fable`; `model: opus` fallback) — each drives
  the *full* checklist; the chairman merges. The user may change the count, the tiers, or
  drop to one. State the per-pass seat-call cost.

After the user confirms, run the loop to completion without further gates.

## Each fix-pass

1. **Verify — dispatch the configured verifiers, ONE AT A TIME (sequential).** The Playwright
   MCP drives a **single browser session per server** — running verifiers in parallel makes
   them fight over tabs/navigation and produces false results. So dispatch verifier A, wait,
   then verifier B. Each is `subagent_type: finishing-verifier`, pinned to its tier
   (`model: sonnet` / `model: fable`), and its prompt carries **the app URL + the full
   checklist**. The agent enforces the hard rules (observe the browser, NEEDS-HUMAN when it
   can't, report-only, the schema). Have each verifier start from a fresh `browser_navigate`
   (and `browser_close` between seats) so state doesn't bleed.
2. **Merge + reconcile.** Combine the verifiers' reports. **Every checklist item must appear**
   — a dropped item is itself a reported gap, not an omission. Where the two verifiers
   **disagree** on an item (one PASSED, one FAILED), **flag it** and treat it as not-yet-passing;
   never silently pick one.
3. **Fix (chairman only).** For each **FAILED** and **MISSING** item, formulate and implement
   the fix **one by one** — real edits, following the codebase's patterns. **NEEDS-HUMAN**
   items are surfaced to the user, never faked or auto-passed. Keep changes minimal and
   scoped to the failing item.

Loop to the next pass to confirm the fixes and catch regressions, up to `N`.

## Final confirm pass + report

- After the last fix-pass, run **one more verification with no fixing** to capture the true
  post-fix state.
- **Gitignore `docs/elenchus/` first** (append the line, create `.gitignore` if absent),
  then write the run report to `docs/elenchus/<slug>-finishing.md`: each checklist item's
  result across passes, the fixes the chairman implemented, any verifier disagreements, and
  everything still **NEEDS-HUMAN**. Surface failures plainly — **no silent skips.**
- **No approval verdict.** The skill reports what works, what it fixed, and what a human must
  still check. It does not declare the feature "done" — that's the user's call.

## Dispatch notes

- Verifier agent = `finishing-verifier` (Read/Grep/Glob + Context7 + Playwright browser tools,
  **no Write/Edit, no recursion** — report-only by construction). It reaches the Playwright MCP
  the same session-scoped way seats reach Context7 (wired in the repo-root `.mcp.json`).
- **Named-agent fallback + restart.** A freshly-installed `finishing-verifier.md` isn't
  dispatchable until Claude Code restarts (agents register at session start). If
  `subagent_type: finishing-verifier` errors "agent type not found," fall back to
  `subagent_type: general-purpose` with the finishing-verifier instructions **inlined**, and
  tell the user to restart so the sandbox (and its no-Write guarantee) applies next run.
- **Graceful degradation.** If the highest tier can't be reached, run the remaining verifier
  and **say so** in the report. Never silently collapse two verifiers onto one model.

## Common mistakes (from baseline testing)

- **Reading the source and issuing a PASS/FAIL as if browser-verified.** The #1 baseline
  failure — agents confidently substitute code-reading for observation. Verifiers MUST drive
  the browser; when they can't, the answer is **NEEDS-HUMAN**, not an asserted verdict.
- **Free-form findings instead of the fixed schema.** Baseline runs used ad-hoc labels
  ("BROKEN", "NEEDS WORK") the chairman can't reconcile. Enforce `PASSED/FAILED/NEEDS-HUMAN/
  MISSING` per item.
- **Burying "couldn't verify" in a footnote** instead of marking each affected item NEEDS-HUMAN.
- **Running the two verifiers in parallel** — they contend over the one browser session and
  produce false results. Sequential only.
- **Letting a verifier fix code**, or letting the chairman skip fixing and just hand back a
  report. Verifiers report; the chairman fixes. Both halves are required.
- **Starting the dev server yourself.** The user runs it; you ask for the URL.
- **Silently dropping a checklist item** the verifier didn't mention — reconcile every item.

## Rationalization table (excuse → reality)

| The excuse | The reality |
|---|---|
| "The source clearly shows this works, mark it PASSED." | Reading code is not observing the app. Drive the browser, or mark NEEDS-HUMAN. |
| "The server's down but the code is right, so it PASSES." | You didn't observe it → NEEDS-HUMAN. Never assert a verdict you couldn't see. |
| "I'll write my findings however reads best." | The chairman reconciles a fixed schema. Off-schema output loses items. |
| "Both verifiers mostly agree, ship it." | A single item disagreement is a not-yet-passing item. Flag it, don't average. |
| "Run both verifiers at once to save time." | One browser session — parallel verifiers corrupt each other. Sequential. |
| "The verifier can just fix the small stuff." | Verifiers are report-only (no Write). Only the chairman fixes. |

## Red flags — stop if you catch yourself

- About to mark an item PASSED/FAILED without having driven the browser for it.
- About to dispatch two verifiers in parallel against one app.
- About to let a verifier edit code, or to end without the chairman fixing FAILED/MISSING.
- About to start the dev server instead of asking for the URL.
- About to declare the feature "done" — that's the user's call; you report + fix + surface.

## Install / sync

- Skill: `skills/finishing-implementation-elenchus/` (archive) → sync to
  `~/.claude/skills/finishing-implementation-elenchus/` (runtime).
- Agent: `agents/finishing-verifier.md` (canonical) → mirror to `.claude/agents/`; **restart**
  before the first dispatch or use the named-agent fallback.
- Playwright MCP: wired in the repo-root `.mcp.json` (`npx @playwright/mcp@latest`), the same
  project-scope pattern as Context7. Ships no secrets. To reuse an existing logged-in session,
  add `--storage-state <path>` to its args.
- **First-run MCP prerequisites (one-time).** A project-scoped MCP server is **pending approval**
  until the user approves it — verify with `claude mcp list`. Approve the `playwright` server
  (via the `/mcp` command or by restarting `claude` and accepting the project-server prompt),
  and install the browser binary once with `npx playwright install chromium`. MCP servers
  connect at session start, so **restart** after approving. Until `playwright` shows
  `✔ Connected`, verifier seats have no browser tools and every item comes back NEEDS-HUMAN.
