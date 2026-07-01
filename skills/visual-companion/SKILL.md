---
name: visual-companion
description: >-
  Use to SHOW the user something in their browser during an Elenchus or
  brainstorming flow — UI mockups, wireframes, architecture diagrams, side-by-side
  visual comparisons, design polish — when the content itself is visual and the
  user would grasp it better by seeing than by reading. The user always ANSWERS in
  the terminal; the browser is display-only (no clicking, no selections recorded).
  Typically dispatched by elenchus-build for a visual frontend-design question,
  paired with ui-ux-pro-max for the design intelligence. NOT for text/tabular
  questions (requirements, tradeoff lists, A/B/C described in words) — those stay
  in the terminal.
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Visual Companion

Browser-based visual companion for showing mockups, diagrams, and options while the
user answers in the terminal. A server watches a directory for HTML files and serves
the newest one to the browser; the browser auto-reloads by polling. There is **no
bidirectional channel** — the user looks at the browser and types their answer in the
terminal.

## When to Use

Decide per-question, not per-session. The test: **would the user understand this
better by seeing it than reading it?**

**Use the browser** when the content itself is visual:

- **UI mockups** — wireframes, layouts, navigation structures, component designs
- **Architecture diagrams** — system components, data flow, relationship maps
- **Side-by-side visual comparisons** — two layouts, two color schemes, two directions
- **Design polish** — look and feel, spacing, visual hierarchy
- **Spatial relationships** — state machines, flowcharts, entity relationships as diagrams

**Stay in the terminal** when the content is text or tabular:

- **Requirements and scope questions** — "what does X mean?", "which features are in scope?"
- **Conceptual A/B/C choices** — picking between approaches described in words
- **Tradeoff lists** — pros/cons, comparison tables
- **Technical decisions** — API design, data modeling, architectural approach selection
- **Clarifying questions** — anything where the answer is words, not a visual preference

A question *about* a UI topic is not automatically a visual question. "What kind of
wizard do you want?" is conceptual — terminal. "Which of these wizard layouts feels
right?" is visual — browser.

## Pairing with ui-ux-pro-max (frontend design)

When an Elenchus front end (e.g. elenchus-build) reaches a **visual frontend-design**
question, dispatch the design thinking to the **`ui-ux-pro-max`** skill (styles,
palettes, font pairings, layout patterns), then render its options through this
companion so the user can *see* them. The user compares in the browser and answers in
the terminal.

## How It Works

The server watches `screen_dir` for HTML files and serves the newest one. You write
HTML there; the user sees it in their browser. The browser polls the server (`GET
/poll`) about once a second and reloads when you push a new screen — no refresh needed
from the user. There are **no selections and no browser events**: the user's answer is
always their **terminal message**.

**Content fragments vs full documents:** If your HTML file starts with `<!DOCTYPE` or
`<html`, the server serves it as-is (injecting only the poll script). Otherwise it wraps
your content in the frame template — header, CSS theme, and the "answer in the terminal"
indicator bar. **Write content fragments by default.** Only write full documents when
you need complete control over the page.

## Starting a Session

```bash
# Start server with persistence (mockups saved to project)
scripts/start-server.sh --project-dir /path/to/project

# Returns: {"type":"server-started","port":52341,"url":"http://localhost:52341",
#           "screen_dir":".../content","state_dir":".../state"}
```

Save `screen_dir` and `state_dir` from the response. Tell the user to open the URL.

**Finding connection info:** The server writes its startup JSON to `$STATE_DIR/server-info`.
If you launched it in the background and didn't capture stdout, read that file for the URL
and port. With `--project-dir`, check `<project>/.superpowers/brainstorm/` for the session dir.

**Note:** Pass the project root as `--project-dir` so mockups persist in
`.superpowers/brainstorm/` and survive server restarts. Without it, files go to `/tmp`
and get cleaned up. Remind the user to add `.superpowers/` to `.gitignore` if needed.

**Launching by platform:**

- **Claude Code (macOS/Linux):** default mode works — the script backgrounds the server.
- **Claude Code (Windows):** the script auto-foregrounds; set `run_in_background: true`
  on the Bash call, then read `$STATE_DIR/server-info` next turn for the URL/port.
- **Codex:** auto-detects `CODEX_CI` and foregrounds — run it normally.
- **Gemini CLI:** use `--foreground` and set `is_background: true` on your shell call.
- **Other reaping environments:** the server must survive across turns — use `--foreground`
  with your platform's background mechanism.

If the URL is unreachable from your browser (remote/containerized setups), bind a
non-loopback host:

```bash
scripts/start-server.sh --project-dir /path/to/project --host 0.0.0.0 --url-host localhost
```

`--url-host` controls the hostname printed in the returned URL JSON.

## The Loop

1. **Check the server is alive**, then **write HTML** to a new file in `screen_dir`:
   - Before each write, check `$STATE_DIR/server-info` exists. If it doesn't (or
     `$STATE_DIR/server-stopped` exists), the server shut down — restart it with
     `start-server.sh` first. It auto-exits after 30 minutes of inactivity.
   - Use semantic filenames: `platform.html`, `visual-style.html`, `layout.html`.
   - **Never reuse filenames** — each screen gets a fresh file. The server serves the
     newest by modification time, and the browser reloads to it on its next poll.
   - Use the Write tool — **never cat/heredoc** (dumps noise into the terminal).

2. **Tell the user what to expect, then end your turn:**
   - Remind them of the URL (every step, not just the first).
   - Give a brief text summary of what's on screen ("Showing 3 layout options for the home page").
   - Ask them to **answer in the terminal**: "Take a look and tell me what you think."

3. **On your next turn**, read the user's **terminal message** — that is the answer.
   There are no browser events to read; the browser is display-only.

4. **Iterate or advance** — if their feedback changes the current screen, write a new
   file (e.g. `layout-v2.html`). Move to the next question only once the current one is settled.

5. **Unload when returning to a text discussion** — when the next step doesn't need the
   browser, push a waiting screen to clear the stale content:

   ```html
   <!-- filename: waiting.html (or waiting-2.html, etc.) -->
   <div style="display:flex;align-items:center;justify-content:center;min-height:60vh">
     <p class="subtitle">Continuing in the terminal...</p>
   </div>
   ```

6. Repeat until done.

## Writing Content Fragments

Write just the content that goes inside the page. The server wraps it in the frame
template automatically (header, theme CSS, the terminal-answer indicator bar).

**Minimal example — two static options for the user to compare visually:**

```html
<h2>Which layout works better?</h2>
<p class="subtitle">Consider readability and visual hierarchy — tell me in the terminal</p>

<div class="options">
  <div class="option">
    <div class="letter">A</div>
    <div class="content"><h3>Single Column</h3><p>Clean, focused reading experience</p></div>
  </div>
  <div class="option">
    <div class="letter">B</div>
    <div class="content"><h3>Two Column</h3><p>Sidebar navigation with main content</p></div>
  </div>
</div>
```

No `<html>`, no CSS, no `<script>` needed — the server provides all of that. The options
are **display only** (label them A/B/… so the user can name their pick in the terminal);
don't add click handlers.

## CSS Classes Available

The frame template provides these classes for your content.

### Options (labelled A/B/C choices — display only)

```html
<div class="options">
  <div class="option">
    <div class="letter">A</div>
    <div class="content"><h3>Title</h3><p>Description</p></div>
  </div>
</div>
```

### Cards (visual designs)

```html
<div class="cards">
  <div class="card">
    <div class="card-image"><!-- mockup content --></div>
    <div class="card-body"><h3>Name</h3><p>Description</p></div>
  </div>
</div>
```

### Mockup container

```html
<div class="mockup">
  <div class="mockup-header">Preview: Dashboard Layout</div>
  <div class="mockup-body"><!-- your mockup HTML --></div>
</div>
```

### Split view (side-by-side)

```html
<div class="split">
  <div class="mockup"><!-- left --></div>
  <div class="mockup"><!-- right --></div>
</div>
```

### Pros/Cons

```html
<div class="pros-cons">
  <div class="pros"><h4>Pros</h4><ul><li>Benefit</li></ul></div>
  <div class="cons"><h4>Cons</h4><ul><li>Drawback</li></ul></div>
</div>
```

### Mock elements (wireframe building blocks)

```html
<div class="mock-nav">Logo | Home | About | Contact</div>
<div style="display: flex;">
  <div class="mock-sidebar">Navigation</div>
  <div class="mock-content">Main content area</div>
</div>
<button class="mock-button">Action Button</button>
<input class="mock-input" placeholder="Input field">
<div class="placeholder">Placeholder area</div>
```

### Typography and sections

- `h2` — page title · `h3` — section heading · `.subtitle` — secondary text
- `.section` — content block with bottom margin · `.label` — small uppercase label

## Design Tips

- **Scale fidelity to the question** — wireframes for layout, polish for polish questions.
- **State the question on each page** — "Which layout feels more professional?" not "Pick one" —
  and remind the user to answer in the terminal.
- **Iterate before advancing** — if feedback changes the current screen, write a new version.
- **2–4 options max** per screen; **label them A/B/…** so the user can name their pick.
- **Use real content when it matters** — for a photography portfolio, use actual images
  (Unsplash). Placeholder content obscures design issues.
- **Keep mockups simple** — focus on layout and structure, not pixel-perfect design.

## File Naming

- Semantic names: `platform.html`, `visual-style.html`, `layout.html`.
- Never reuse filenames — each screen is a new file.
- For iterations, append a version suffix: `layout-v2.html`, `layout-v3.html`.
- The server serves the newest file by modification time.

## Cleaning Up

```bash
scripts/stop-server.sh $SESSION_DIR
```

If the session used `--project-dir`, mockup files persist in `.superpowers/brainstorm/`
for later reference. Only `/tmp` sessions are deleted on stop.

## Reference

- Frame template (CSS reference): `scripts/frame-template.html`
- Poll client (browser-side): `scripts/helper.js`
- Server: `scripts/server.cjs` (plain HTTP + `/poll`; no WebSockets)
</content>
