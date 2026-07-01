# Todo — visual-companion as a standalone skill + drop WebSockets

## Decision (recommended)
- **Standalone skill** `skills/visual-companion/`, not embedded in elenchus-build.
  Reusable across front ends, owns its own `scripts/`, dispatched by description.
- `elenchus-build` references it for **visual** frontend-design questions, pairing it
  with the `ui-ux-pro-max` skill (design intelligence) — user answers in the terminal.

## Tasks

### 1. Create the standalone skill
- [ ] `skills/visual-companion/SKILL.md` — from `visual-companion.md`, add YAML frontmatter
      (`name`, `description` telling Claude *when* to use it: visual questions inside an
      Elenchus/brainstorm flow), and rewrite the browser-interaction sections to say
      "user answers in the terminal" (no click-to-record selections).
- [ ] Move scripts into `skills/visual-companion/scripts/`
      (server.cjs, start-server.sh, frame-template.html, helper.js).
- [ ] Delete the root `visual-companion.md` and root `scripts/` after the move.

### 2. Remove WebSockets entirely (server-side)
- [ ] `server.cjs`: delete RFC-6455 block (encode/decode/accept-key, OPCODES, WS_MAGIC),
      `handleUpgrade`, `handleMessage`, `broadcast`, `clients`, and `server.on('upgrade')`.
- [ ] Add poll endpoint: `GET /poll` returns newest screen filename+mtime as JSON.
- [ ] Watcher keeps only `touchActivity` (idle timeout still works); drop `state/events`.

### 3. Remove WebSockets (client-side)
- [ ] `helper.js`: delete WS connect/sendEvent/click-capture. Replace with a poller
      hitting `/poll` ~every 1s, reload on change. Keep `toggleSelect` as *local*
      visual highlight only (no network send).

### 4. Template copy change
- [ ] `frame-template.html`: indicator-bar + header status instruct the user to
      **answer in the terminal**.

### 5. Wire into elenchus-build
- [ ] `skills/elenchus-build/SKILL.md`: note that a **visual** frontend-design question
      dispatches design to `ui-ux-pro-max` and renders through the `visual-companion`
      skill; user answers in the terminal.

### 6. Docs / sync
- [ ] Sync the new skill to `~/.claude/skills/` runtime (confirm before writing outside repo).

## Review

**Decisions taken:** standalone skill (not embedded); browser fully static (no click
capture); synced to runtime now.

**Changes made:**
1. **New skill `skills/visual-companion/`** — `SKILL.md` (frontmatter with when-to-use +
   ui-ux-pro-max pairing note; all interaction rewritten to "user answers in terminal";
   examples stripped of `onclick`/`data-choice`) + `scripts/` moved from repo root.
2. **`server.cjs`** — deleted the entire RFC-6455 block (OPCODES, WS_MAGIC,
   compute/encode/decodeFrame), `handleUpgrade`, `handleMessage`, `broadcast`, `clients`,
   the `server.on('upgrade')` listener, and the `state/events` writes. Added `GET /poll`
   returning `{file, mtime}` of the newest screen. Watcher now only logs + `touchActivity`
   (idle timeout intact). `module.exports = { startServer }`. Dropped unused `crypto`.
3. **`helper.js`** — replaced WS client with a ~1s poller against `/poll` that reloads on
   change; no click capture, no `toggleSelect`.
4. **`frame-template.html`** — header now "Elenchus — Visual Companion" / status "Answer in
   your terminal"; indicator bar tells the user to answer in the terminal.
5. **`elenchus-build/SKILL.md`** — added a handoff note under Macro clarification: visual
   frontend-design questions dispatch to `ui-ux-pro-max` + render through `visual-companion`,
   user answers in terminal.
6. **Sync** — `visual-companion/` and the edited `elenchus-build/SKILL.md` copied to
   `~/.claude/skills/`.

**Verified:** `node --check server.cjs` passes; live smoke test via `start-server.sh`
confirmed `/poll` transitions null→screen, the page injects the poll client + content, and
the terminal-answer copy renders. No WebSocket code remains.

**Note for user:** restart the session so Claude Code registers the new `visual-companion`
skill.

## Skill test (via /writing-skills)

Reference/technique skill → tested with 3 application + gap scenarios (subagents reading
the deployed SKILL.md, no access to this conversation). **All 3 passed.**

- **Application** (mixed visual + conceptual Qs): routed the layout Q → browser, the auth Q
  → terminal; launched server with the absolute `start-server.sh --project-dir` path; wrote
  a content fragment via Write (not heredoc) using `.split`/`.mockup`/`.pros-cons`; labelled
  options A/B; told the user the URL + auto-reload + "answer in the terminal"; obtained the
  answer only from the terminal; iterated with `-v2` filename; unloaded with `waiting.html`;
  stop-server at the end. Even added the `.gitignore` reminder.
- **Answer-collection trap**: correctly refused click-to-select — browser is display-only,
  answer is the terminal message, `/poll` is server→browser only, no events file invented.
- **Sync/reload gap**: accurately explained plain-HTTP `/poll` (~1s), no manual refresh, no
  WebSockets; cited exact skill lines and reasoned about the ~1s latency edge + liveness check.

**Verdict:** skill teaches the new answer-in-terminal / no-WebSocket model cleanly; no stale
click-capture mental model leaked through. No fixes required.

**Optional polish (not blocking):** skill is ~1505 words (>500 target, acceptable for a
reference skill); could add a short "Common Mistakes" section (e.g. "reading a nonexistent
events file", "using the browser for a conceptual question") for extra robustness.
</content>
