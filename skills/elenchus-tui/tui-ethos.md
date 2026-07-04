# TUI ethos — pure-ASCII terminal mockups that actually hold

Design rules for the `elenchus-tui` skill. No framework (curses/rich/blessed/textual) — the
deliverable is one runnable stdlib script anyone can read and run. No `ui-ux-pro-max` — it is
web/mobile-tuned and off-target for a fixed-cell terminal grid. The reference implementation
that already embodies all of this: **`mockups/council_tui.py`** (+ `mockups/council-tui.txt`).
Reuse its primitives; don't reinvent them.

## 1. The 80-column grid law

The mockup targets an **80-column** terminal (state it if you deviate). **Every framed line
is padded to the exact inner width by *visible* width**, not byte length — ANSI escapes and
wide glyphs must not count as cells. Build on a visible-width helper:

```python
import re
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
def vlen(s):            # visible length, ignoring color escapes
    return len(ANSI_RE.sub("", s))
def vljust(s, w):       # left-justify to an exact visible width
    return s + " " * max(0, w - vlen(s))
```

A row that overflows wraps into a second terminal line (broken border); a short *framed* row
leaves a ragged edge. So pad every cell through `vljust`/`vcenter`.

**Framed rows vs loose lines.** A **framed** row (one that starts/ends with a border glyph
`│ ╭ ╮ ╰ ╯ ┌ ┐ └ ┘ ├ ┤ ─`) must be **exactly 80** by visible width — a short one ragged-edges
the border. A **loose** line (a bare tagline, a `[key] …` footer, the input row) is *not*
framed and may be **any width ≤ 80** — it just must never exceed 80 (which would wrap). At
verify time: framed row ≠ 80 → FAILED; any row > 80 → FAILED; a loose row < 80 → fine.
(Confirmed on the reference: its tagline is 79 and its keybar 77 — both correct, not bugs.)

## 2. Width-1 glyph discipline (the trap the baseline fell into)

Box-drawing (`─│╭╮╰╯┌┐└┘├┤`) and block (`█░▓`) glyphs are width-1 in normal Western
terminals — but Unicode marks many decorative glyphs (`· → ↑ ↓ ✓ ✗ ◆ ◷ ⇄` …) **ambiguous
width**: 1 cell in a non-CJK terminal, 2 cells in a CJK/ambiguous-as-wide terminal. A design
built on them *passes its own width self-check* (same assumed model) yet shifts by two columns
elsewhere. **Don't ship that as a footnote caveat.** Either:

- **Own the assumption explicitly** — commit to width-1 (standard non-CJK terminal), keep the
  glyph set small and consistent, and *state that assumption in the mockup header and report*;
  the tmux capture is then the source of truth. **(default)** OR
- **Offer an ASCII-only fallback** glyph set (`+ - | > v * x`) toggled by a flag, for
  teammates on ambiguous-width terminals.

Measure with a display-width function that strips ANSI and counts East-Asian wide/ambiguous
correctly — never `len()`.

## 3. Flicker-free paint (why tmux beats a screenshot here)

An animated/navigable TUI must repaint without tearing. The reference `paint()` does three
things — reuse it verbatim:

```python
def paint(lines):
    out = ["\x1b[?2026h"]                 # 1) DEC-2026 synchronized output: buffer the whole
    for i, ln in enumerate(lines):        #    frame, swap atomically — no half-drawn screen
        out.append(f"\x1b[{i+1};1H")      # 2) absolute cursor per line (no trailing newline)
        out.append(ln); out.append("\x1b[K")  #    → the frame can never scroll; clear stale tail
    out.append("\x1b[J")                  # 3) erase anything below the frame
    out.append("\x1b[?2026l")             #    end synchronized update
    sys.stdout.write("".join(out)); sys.stdout.flush()
```

Absolute positioning + `\x1b[K` (not a full `\x1b[2J` erase every frame) is what removes the
blank-then-redraw flash.

**Flicker check ≠ byte-identical captures.** A live clock/spinner/animated bar *legitimately*
changes between captures — a raw `diff` would false-FAIL it (confirmed: the reference's clock
ticks `00:00→00:01` and depth bars breathe between two captures 0.6s apart). So the verifier
proves flicker-freedom two robust ways instead:

- **No torn frame:** across several rapid captures, **every** capture is a *complete* frame —
  all four borders present, framed rows all their full width, no blank interior row that
  should hold content, no wrapped/continuation lines. A half-painted capture = tearing = FAILED.
- **Static cells hold:** compare captures with the **known-animated cells masked** (or verify a
  deliberately static state, e.g. the `--print` frame rendered in the pane) — the non-animated
  structure must be byte-identical. Drift there (a border that jumps, a row that reflows) = FAILED.

Reserve the raw byte-identical check for the `--print`/static path, where nothing should move.

## 4. Alt-screen + clean restore

Enter the alternate screen and hide the cursor on start; **always** restore on exit (even on
`Ctrl-C`) — a dirty restore is a FAILED at verify time:

```python
sys.stdout.write("\x1b[?1049h\x1b[?25l\x1b[2J")   # alt screen + hide cursor + clear once
# … loop …
finally:
    sys.stdout.write("\x1b[?25h\x1b[?1049l")       # show cursor + leave alt screen
```

## 5. Too-small guard

Check the terminal size each tick; if it's shorter/narrower than the frame, paint a
**front-loaded** "terminal too small — now WxH, need ≥80×N" notice instead of letting the
frame clip. Re-check each tick so it flips back to the full UI on resize. (Reference:
`too_small()` in `council_tui.py`.)

## 6. Named, navigable states + a `--print` snapshot path

- **Navigable:** one key per named breakpoint (e.g. `[f] floor [s] synthesis [g] gate`), so a
  viewer walks the states live. The verifier drives these keys and confirms each reaches the
  right state.
- **`--print <state>` / `--static`:** a non-interactive path that emits **one clean static
  frame per state with ANSI stripped** — this is what generates each `<breakpoint>.txt`
  deliverable and what the width check measures. Every breakpoint must be reachable both ways.

## 7. The shared tmux verify-harness (what a `tui-verifier` seat runs)

Every seat drives its **own private socket** at forced geometry with the status bar off, then
captures **twice, time-separated**, and measures visible width. The `tui-verifier` agent
carries the hard rules; this is the canonical shape (the chairman may run it too as a
generate-time sanity check, but the independent verdict comes from the seats):

```bash
SOCK="tui_<breakpoint>_<unique>"        # a PRIVATE server — never the default (live sessions!)
ROWS=44                                  # >= frame height
tmux -L "$SOCK" new-session -d -x 80 -y "$ROWS" "python3 <script> <reach-state-cmd>"
tmux -L "$SOCK" set -g status off
sleep 0.6; tmux -L "$SOCK" capture-pane -p > cap_a.txt   # capture the state
sleep 0.6; tmux -L "$SOCK" capture-pane -p > cap_b.txt   # again, time-separated

# FLICKER (robust to animation): both captures must be complete, untorn frames.
# A raw `diff cap_a cap_b` is only valid for a static (--print) state; for a live
# clock/spinner it false-fails, so instead confirm no torn frame + framed-row widths hold:
for f in cap_a.txt cap_b.txt; do
  awk '{ ln=$0; gsub(/\x1b\[[0-9;]*m/,"",ln); w=length(ln);
         if (w>80) { print FILENAME": OVERFLOW row "NR" ("w")"; bad=1 }         # wrap => FAILED
         if (ln ~ /^[│╭╮╰╯┌┐└┘├┤─]/ && w!=80) { print FILENAME": RAGGED framed row "NR" ("w")"; bad=1 } }
       END{ if(!bad) print FILENAME": frame ok (all framed rows 80, none overflow)" }' "$f"
done
tmux -L "$SOCK" kill-server                               # tear down ONLY your own socket
```

For a `--print`/static state you *may* add `diff cap_a.txt cap_b.txt` (nothing should move).
For a live state, don't — mask the animated cells or rely on the untorn-frame check above.

Hard rules that never bend: **always `-L <your-unique-socket>`** (never the default server),
**never bare `kill-server`**, **never** `ls`/`attach`/`kill` a session you didn't create,
force `-x 80 -y ROWS`, `status off`, capture twice, judge **framed** rows against 80 (loose
lines just must not overflow), tear down only your own socket. If you can't force the size or
launch the script → **NEEDS-HUMAN**, never a guessed PASS.
