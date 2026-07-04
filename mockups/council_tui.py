#!/usr/bin/env python3
"""
Elenchus council — an animated terminal mockup in pure stdlib. No frameworks.

  python council_tui.py            # interactive, animated (needs a TTY)
  python council_tui.py --print    # emit one clean static frame (no color/animation)
  python council_tui.py --print > council-tui.txt

Keys (interactive):  [tab] cycle seat  [f] floor  [s] synthesis  [g] gate
                     type + [enter] answer   [q]/Ctrl-C  adjourn

Every framed line is padded to an exact 80-column grid using display-width-1
glyphs, so the borders hold in any terminal. ANSI color is used inline but is
stripped when measuring width, and disabled entirely for --print.
"""

import sys, os, re, math, time

# ── canvas ──────────────────────────────────────────────────────────────────
W = 80                 # total width
IN = W - 2             # inner width between the outer verticals
LW, RW = 33, 45        # left panel width, right panel width (+2 gap = 80)
GAP = "  "

# ── color (ANSI 256; no-ops when disabled) ──────────────────────────────────
USE_COLOR = True
ESC = "\x1b"
def sgr(*c):
    return (ESC + "[" + ";".join(str(x) for x in c) + "m") if USE_COLOR else ""
RESET  = sgr(0)
BOLD   = sgr(1)
def fg(n): return sgr(38, 5, n)

BORDER = fg(240)
DIM    = fg(244)
GOLD   = fg(178)   # opus
CYAN   = fg(80)    # sonnet
GREEN  = fg(114)   # haiku
MAG    = fg(176)   # chairman
RED    = fg(167)
YELLOW = fg(179)
SLATE  = fg(109)

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
def vlen(s):            # visible length, ignoring color escapes
    return len(ANSI_RE.sub("", s))
def vljust(s, w):       # left-justify by visible width
    return s + " " * max(0, w - vlen(s))
def vcenter(s, w):
    pad = max(0, w - vlen(s)); l = pad // 2
    return " " * l + s + " " * (pad - l)

# ── frame primitives ─────────────────────────────────────────────────────────
def bcol(s):  return BORDER + s + RESET
def top(l="╭", r="╮"):  return bcol(l + "─" * IN + r)
def bot(l="╰", r="╯"):  return bcol(l + "─" * IN + r)
def band(inner=""):     return bcol("│") + vljust(inner, IN) + bcol("│")
def hrule():            return bcol("│" + "─" * IN + "│")
def titled(title, w=W, l="┌", r="┐"):
    seg = f"{l}─ {title} "
    return bcol(seg + "─" * (w - vlen(seg) - 1) + r)

def lcell(inner):  return bcol("│") + vljust(inner, LW - 2) + bcol("│")
def rcell(inner):  return bcol("│") + vljust(inner, RW - 2) + bcol("│")
def rtitled(title):
    seg = f"┌─ {title} "
    return bcol(seg + "─" * (RW - vlen(seg) - 1) + "┐")
LBOT = bcol("└" + "─" * (LW - 2) + "┘")
RBOT = bcol("└" + "─" * (RW - 2) + "┘")

SPIN = "⣾⣽⣻⢿⡿⣟⣯⣷"

# ── seats model ──────────────────────────────────────────────────────────────
SEATS = [
    {"tag": "α", "model": "opus-4.8",  "posture": "relentless",      "base": 92, "amp": 4, "col": GOLD},
    {"tag": "β", "model": "sonnet-5",  "posture": "systems-skeptic", "base": 78, "amp": 7, "col": CYAN},
    {"tag": "γ", "model": "haiku-4.5", "posture": "latency-hawk",    "base": 85, "amp": 5, "col": GREEN},
]

def depth_pct(s, i, t):
    return max(0, min(99, int(s["base"] + s["amp"] * math.sin(t * 1.7 + i * 1.3))))

def depth_bar(pct, width=14, col=CYAN):
    full = round(pct / 100 * width)
    return col + "█" * full + RESET + DIM + "░" * (width - full) + RESET

def build_left(active, t):
    rows = [rtitled_left(), lcell("")]
    for i, s in enumerate(SEATS):
        hot = (i == active)
        dot = (s["col"] if hot else DIM) + "◆" + RESET
        name = (BOLD + s["col"] if hot else DIM) + f"seat {s['tag']}" + RESET
        model = (s["col"] if hot else DIM) + f"{s['model']:<9}" + RESET
        live = GREEN + "●" + RESET
        mark = ("  " + s["col"] + "◀" + RESET) if hot else ""
        rows.append(lcell(f"  {dot} {name}   {model} {live}{mark}"))
        rows.append(lcell(f"    depth {depth_bar(depth_pct(s, i, t), col=s['col'])}  {depth_pct(s, i, t):2d}%"))
        rows.append(lcell(f"    {DIM}posture: {s['posture']}{RESET}"))
        rows.append(lcell(""))
    spin = SPIN[int(t * 12) % len(SPIN)]
    rows.append(lcell(f"  {MAG}○ chairman{RESET} {DIM}·{RESET} {MAG}{spin} synth{RESET}"))
    rows.append(LBOT)
    return rows

def rtitled_left():
    seg = "┌─ SEATS "
    return bcol(seg + "─" * (LW - vlen(seg) - 1) + "┐")

# ── floor / synthesis / gate content (14 inner lines each) ───────────────────
def q(s):   return f'{DIM}"{s}{RESET}'
FLOOR = [
    "",
    f"  {GREEN}» seat γ{RESET}  {DIM}·  haiku{RESET}",
    f'    {DIM}"You claim CRDTs make merge{RESET}',
    f"    {DIM} conflicts impossible — but your{RESET}",
    f"    {DIM} cursor-sync is last-write-wins.{RESET}",
    f"    {DIM} Two offline carets collide:{RESET}",
    f'    {DIM} whose wins? Name the rule."{RESET}',
    "",
    f"  {GOLD}» seat α{RESET}  {DIM}·  opus{RESET}      {RED}┌─────────┐{RESET}",
    f'    {DIM}"Wrong bug. The real{RESET}  {RED}│ DISSENT │{RESET}',
    f"    {DIM} gap is presence GC —{RESET} {RED}└─────────┘{RESET}",
    f'    {DIM} 10k ghost sessions at 3 weeks."{RESET}',
    "",
    f"  {SLATE}seats clash → BOTH stand, no merge{RESET}",
]
SYNTH = [
    "",
    f"  {GREEN}CONVERGENCE{RESET}",
    f"    {DIM}· CRDT text layer is sound{RESET}",
    f"    {DIM}· offline-first is achievable{RESET}",
    "",
    f"  {YELLOW}SPLIT{RESET}  {DIM}(both preserved){RESET}",
    f"    {DIM}· {GOLD}α{DIM}: presence-GC is the risk{RESET}",
    f"    {DIM}· {GREEN}γ{DIM}: p99 latency is the risk{RESET}",
    f"    {SLATE}→ not merged. you weigh them.{RESET}",
    "",
    f"  {RED}OPEN{RESET}",
    f"    {DIM}· conflict rule undefined  (#1){RESET}",
    f"    {DIM}· statefulness contested   (#3){RESET}",
    "",
]
GATE = [
    "",
    f"  {RED}{BOLD}▓ GATE: CLOSED{RESET}",
    "",
    f"  {DIM}blockers before you proceed:{RESET}",
    f"    {RED}·{RESET} {DIM}#1 offline caret-resolution{RESET}",
    f"       {DIM}undefined  (α, β refuted){RESET}",
    f"    {RED}·{RESET} {DIM}#3 server statefulness{RESET}",
    f"       {DIM}contested  (β, γ){RESET}",
    "",
    f"  {GREEN}cleared:{RESET} {DIM}#4 latency (in test){RESET}",
    "",
    f"  {SLATE}the council won't open this —{RESET}",
    f"  {SLATE}only your answers do.{RESET}",
    "",
]
MODES = {"floor": ("FLOOR", FLOOR), "synthesis": ("SYNTHESIS", SYNTH), "gate": ("GATE", GATE)}

def build_right(mode):
    title, body = MODES[mode]
    return [rtitled(title if False else title) if False else rtitled_right(title)] + [rcell(x) for x in body] + [RBOT]

def rtitled_right(title):
    seg = f"┌─ {title} "
    return bcol(seg + "─" * (RW - vlen(seg) - 1) + "┐")

# ── ledger (constant) ────────────────────────────────────────────────────────
def status_glyph(kind):
    return {
        "refuted":   RED + "✗ refuted" + RESET,
        "unproven":  YELLOW + "! unproven" + RESET,
        "contested": DIM + "~ contested" + RESET,
        "testing":   CYAN + "◷ testing" + RESET,
    }[kind]

LEDGER_ROWS = [
    ("1", "offline-first, zero conflicts", "refuted",   "α  β"),
    ("2", "presence scales for free",      "unproven",  "α"),
    ("3", "server stays stateless",        "contested", "β  γ"),
    ("4", "p99 < 50ms at 1k peers",        "testing",   "γ"),
]

def led_line(marker, claim, status, who):
    # fixed column starts (visible): marker@3, claim@6, status@37, who@50 —
    # measured with vljust so color-coded cells still align.
    s = vljust("   " + marker, 6)
    s = vljust(s, 6) + vljust(claim, 31)
    s += vljust(status, 13) + who
    return s

def build_ledger():
    out = [titled("CONTRADICTION LEDGER"), band("")]
    out.append(band(DIM + led_line("#", "claim", "status", "raised by") + RESET))
    out.append(band(DIM + led_line("─", "─" * 29, "─" * 10, "─" * 9) + RESET))
    for n, claim, kind, who in LEDGER_ROWS:
        out.append(band(led_line(n, claim, status_glyph(kind), DIM + who + RESET)))
    out.append(band(""))
    out.append(band(f"   {SLATE}▸ 2 unresolved{RESET}  {DIM}·  gate stays {RED}CLOSED{DIM} until you answer #1, #3{RESET}"))
    out.append(bot("└", "┘"))
    return out

# ── whole screen ─────────────────────────────────────────────────────────────
def render(active, mode, t, buf, caret, status):
    spin = SPIN[int(t * 12) % len(SPIN)]
    mm, ss = divmod(int(t), 60)
    lines = []
    lines.append(top())
    lines.append(band(f"  {GOLD}[=]{RESET}  {BOLD}ELENCHUS{RESET}  {DIM}·  council in session{RESET}"
                      f"      {DIM}premise: {SLATE}real-time-collab-editor{RESET}"))
    lines.append(hrule())
    lines.append(band(f"  {DIM}round 2 / 3  ·  stress-testing your answers    elapsed "
                      f"{CYAN}{mm:02d}:{ss:02d}{RESET}   {GREEN}{spin} live{RESET}"))
    lines.append(bot())
    lines.append("")

    left, right = build_left(active, t), build_right(mode)
    for a, b in zip(left, right):
        lines.append(a + GAP + b)
    lines.append("")

    lines.extend(build_ledger())
    lines.append("")
    tag = status if status else f"{DIM}the council never green-lights — it hands you the open questions. you decide.{RESET}"
    lines.append("  " + tag)
    lines.append("")

    lines.append(top())
    car = ("█" if caret else " ") if USE_COLOR else "_"
    lines.append(band(f"  {SLATE}›{RESET} {buf}{CYAN}{car}{RESET}"))
    lines.append(bot())
    lines.append(f"  {DIM}[tab] seat  [f] floor  [s] synthesis  [g] gate  "
                 f"[enter] answer  [q] adjourn{RESET}")
    return lines

# ── static print path ────────────────────────────────────────────────────────
def print_static():
    # Colors are baked into module constants at import, so strip escapes from the
    # rendered frame to emit clean, alignment-verifiable text.
    frame = "\n".join(render(active=0, mode="floor", t=252, buf="", caret=False, status=""))
    sys.stdout.write(ANSI_RE.sub("", frame) + "\n")

# ── flicker-free paint ───────────────────────────────────────────────────────
# 1) DEC mode 2026 = synchronized output: the terminal buffers the whole frame
#    and swaps it in atomically, so you never see a half-drawn screen.
# 2) absolute cursor positioning per line (no trailing newline) → the frame can
#    never scroll, even if the window is shorter than the frame.
# 3) clear-to-EOL (\x1b[K) per line instead of a full-screen erase → the screen
#    is never momentarily blank. All are no-ops on terminals that don't grok them.
def paint(lines):
    out = ["\x1b[?2026h"]                       # begin synchronized update
    for i, ln in enumerate(lines):
        out.append(f"\x1b[{i + 1};1H")          # go to row i+1, col 1
        out.append(ln)
        out.append("\x1b[K")                    # erase any stale tail on this row
    out.append("\x1b[J")                         # erase anything below the frame
    out.append("\x1b[?2026l")                    # end synchronized update
    sys.stdout.write("".join(out))
    sys.stdout.flush()

def too_small(cols, rows, need_h):
    # Shown when the window is shorter/narrower than the 80xN frame. Without this
    # the frame would clip (rows past the bottom clamp onto the last line). Info
    # is front-loaded so it stays visible even in a tiny pane; the loop re-checks
    # each tick, so it flips back to the full UI the moment you resize.
    return [
        "",
        f"  {BOLD}ELENCHUS{RESET} council TUI",
        "",
        f"  {YELLOW}terminal too small{RESET}",
        f"  now {cols}x{rows}   need >= {W}x{need_h}",
        "",
        f"  {DIM}resize the window / zoom out —{RESET}",
        f"  {DIM}it repaints automatically.  [q] quit{RESET}",
    ]

# ── interactive path ─────────────────────────────────────────────────────────
def run():
    import termios, tty, select
    if not sys.stdin.isatty():
        print_static(); return
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    start = time.time()
    active, mode, buf, status, status_until = 0, "floor", "", "", 0.0
    try:
        tty.setcbreak(fd)
        sys.stdout.write("\x1b[?1049h\x1b[?25l\x1b[2J")   # alt screen + hide cursor + clear once
        while True:
            t = time.time() - start
            caret = int(t * 2) % 2 == 0
            if status and t > status_until:
                status = ""
            frame = render(active, mode, t, buf, caret, status)
            try:
                cols, rows = os.get_terminal_size(sys.stdout.fileno())
            except OSError:
                cols, rows = W, len(frame)
            paint(frame if (rows >= len(frame) and cols >= W) else too_small(cols, rows, len(frame)))
            r, _, _ = select.select([sys.stdin], [], [], 0.1)
            if not r:
                continue
            ch = sys.stdin.read(1)
            if ch in ("q", "\x03", "\x04"):
                break
            elif ch == "\t":
                active = (active + 1) % len(SEATS)
            elif ch == "f":
                mode = "floor"
            elif ch == "s":
                mode = "synthesis"
            elif ch == "g":
                mode = "gate"
            elif ch in ("\r", "\n"):
                if buf.strip():
                    short = buf.strip()[:34]
                    status = GREEN + "✓ recorded — seats will stress-test: " + RESET + DIM + short + RESET
                    status_until = t + 3.5
                    buf = ""
            elif ch in ("\x7f", "\b"):
                buf = buf[:-1]
            elif ch.isprintable() and len(buf) < 60:
                buf += ch
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[?25h\x1b[?1049l")           # show cursor + leave alt screen
        sys.stdout.flush()
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

if __name__ == "__main__":
    if "--print" in sys.argv or "--static" in sys.argv:
        print_static()
    else:
        run()
