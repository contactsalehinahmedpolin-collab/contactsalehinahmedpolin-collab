#!/usr/bin/env python3
"""
render_heatmap_svg.py
Renders data/contributions.json (produced by fetch_contributions.py) as an
interactive, animated GitHub contribution calendar SVG:
- 53-week x 7-day grid of rounded colored cells
- Diagonal slide-down reveal animation (CSS keyframes with zero external JS)
- Terminal window chrome with glowing buttons
- Less -> More legend
- High-visibility stats telemetry footer

Output: contrib-heatmap.svg
Run by GitHub Actions or locally via build_all.py.
"""
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IN_PATH = os.path.join(HERE, "..", "data", "contributions.json")
OUT_PATH = os.path.join(HERE, "..", "contrib-heatmap.svg")

# GitHub Cyber-Green Palette (Empty -> Peak activity)
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

CELL = 12
GAP = 3
STEP = CELL + GAP
PAD = 24
LEFT_LABEL_W = 32
TOP_LABEL_H = 22
TITLEBAR_H = 34

BG = "#0a0e14"
BG2 = "#0e1624"
FRAME = "#21262d"
BORDER_HIGHLIGHT = "#30363d"
MUTED = "#7d8590"
TEXT = "#e6edf3"
ACCENT = "#58a6ff"
CYAN = "#38bdf8"
GREEN = "#39d353"
GOLD = "#f2cc60"

# Animation timing
COL_T = 0.016   # per-column delay
ROW_T = 0.040   # per-row delay
CELL_DUR = 0.40


def level_for(count):
    if count == 0:
        return 0
    if count <= 4:
        return 1
    if count <= 12:
        return 2
    if count <= 25:
        return 3
    if count <= 45:
        return 4
    return 5


def build_grid(days):
    if not days:
        return []
    first = datetime.date.fromisoformat(days[0]["date"])
    lead_pad = (first.weekday() + 1) % 7  # 0=Sunday
    grid = []
    col = [None] * lead_pad
    
    for d in days:
        date = datetime.date.fromisoformat(d["date"])
        weekday = (date.weekday() + 1) % 7
        while len(col) < weekday:
            col.append(None)
        col.append((d["date"], d["count"], level_for(d["count"])))
        if len(col) == 7:
            grid.append(col)
            col = []
            
    if col:
        while len(col) < 7:
            col.append(None)
        grid.append(col)
        
    return grid


def render(data):
    days = data.get("days", [])
    if not days:
        print("[!] No days data found in contributions.json", file=sys.stderr)
        return

    grid = build_grid(days)
    n_cols = len(grid)
    art_w = n_cols * STEP
    art_h = 7 * STEP

    # Extract month labels
    month_labels = []
    seen_months = set()
    for ci, column in enumerate(grid):
        for cell in column:
            if cell is None:
                continue
            date = datetime.date.fromisoformat(cell[0])
            key = (date.year, date.month)
            if key not in seen_months and date.day <= 7:
                seen_months.add(key)
                month_labels.append((ci, date.strftime("%b")))
            break

    canvas_w = PAD + LEFT_LABEL_W + art_w + PAD
    stats_h = 72
    canvas_h = TITLEBAR_H + TOP_LABEL_H + art_h + stats_h + PAD

    css = f"""
@keyframes cell-in {{
  0%   {{ opacity: 0; transform: translateY(-6px); }}
  100% {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes pulse-dot {{
  0%, 100% {{ opacity: 1; transform: scale(1); }}
  50% {{ opacity: 0.4; transform: scale(0.9); }}
}}
.c {{ opacity: 0; animation: cell-in {CELL_DUR:.2f}s cubic-bezier(0.16, 1, 0.3, 1) both; }}
.live-dot {{ animation: pulse-dot 2s infinite ease-in-out; transform-box: fill-box; transform-origin: center; }}
""".strip()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" '
        f'viewBox="0 0 {canvas_w} {canvas_h}" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">',
        f'<style>{css}</style>',
        '<defs>',
        f'<linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0%" stop-color="{BG2}"/>',
        f'<stop offset="100%" stop-color="{BG}"/>',
        '</linearGradient>',
        '</defs>',
        f'<rect width="{canvas_w}" height="{canvas_h}" rx="10" fill="url(#bgGrad)"/>',
        f'<rect x="0.5" y="0.5" width="{canvas_w-1}" height="{canvas_h-1}" rx="10" '
        f'fill="none" stroke="{BORDER_HIGHLIGHT}" stroke-width="1"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{canvas_w}" y2="{TITLEBAR_H}" stroke="{BORDER_HIGHLIGHT}" stroke-width="1"/>',
    ]

    # macOS window controls
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

    parts.append(
        f'<text x="{canvas_w/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
        f'text-anchor="middle">polin@github: ~/contributions --graph --live</text>'
    )
    
    # Live status badge in top right
    parts.append(f'<circle class="live-dot" cx="{canvas_w - PAD - 55}" cy="{TITLEBAR_H/2}" r="4" fill="{GREEN}"/>')
    parts.append(f'<text x="{canvas_w - PAD}" y="{TITLEBAR_H/2 + 4}" fill="{GREEN}" font-size="11" text-anchor="end">LIVE</text>')

    grid_top = TITLEBAR_H + TOP_LABEL_H
    grid_left = PAD + LEFT_LABEL_W

    # Month headers
    for ci, label in month_labels:
        x = grid_left + ci * STEP
        parts.append(f'<text x="{x}" y="{TITLEBAR_H + 16}" fill="{MUTED}" font-size="10">{label}</text>')

    # Day labels
    for wi, wname in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        y = grid_top + wi * STEP + CELL * 0.78
        parts.append(f'<text x="{PAD}" y="{y:.1f}" fill="{MUTED}" font-size="9">{wname}</text>')

    # Calendar Cells
    for ci, column in enumerate(grid):
        gx = grid_left + ci * STEP
        for ri, cell in enumerate(column):
            if cell is None:
                continue
            date_s, count, lvl = cell
            gy = grid_top + ri * STEP
            delay = ci * COL_T + ri * ROW_T
            plural = "s" if count != 1 else ""
            parts.append(
                f'<rect class="c" x="{gx}" y="{gy}" width="{CELL}" height="{CELL}" rx="2.5" '
                f'fill="{PALETTE[lvl]}" style="animation-delay:{delay:.3f}s">'
                f'<title>{date_s}: {count} contribution{plural}</title></rect>'
            )

    # Legend: Less [][][][][] More
    leg_y = grid_top + art_h + 10
    leg_x = canvas_w - PAD - (len(PALETTE) * (CELL + 2) + 65)
    parts.append(f'<text x="{leg_x}" y="{leg_y + CELL*0.75:.1f}" fill="{MUTED}" font-size="10" text-anchor="end">Less</text>')
    for li, colr in enumerate(PALETTE):
        lx = leg_x + 8 + li * (CELL + 2)
        parts.append(f'<rect x="{lx}" y="{leg_y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{colr}"/>')
    parts.append(f'<text x="{leg_x + 12 + len(PALETTE) * (CELL + 2)}" y="{leg_y + CELL*0.75:.1f}" fill="{MUTED}" font-size="10">More</text>')

    # Telemetry Stats Footer
    total = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)
    best_day = data.get("best_day", {})
    best_count = best_day.get("count", 0)

    sep_y = leg_y + CELL + 14
    parts.append(f'<line x1="{PAD}" y1="{sep_y}" x2="{canvas_w - PAD}" y2="{sep_y}" stroke="{FRAME}" stroke-width="1"/>')

    stats_y1 = sep_y + 24
    col_w = (canvas_w - PAD * 2) / 4

    stats_items = [
        ("TOTAL COMMITS", f"{total:,}", CYAN),
        ("CURRENT STREAK", f"{current_streak} days", GREEN),
        ("LONGEST STREAK", f"{longest_streak} days", GOLD),
        ("PEAK VELOCITY", f"{best_count} / day", ACCENT),
    ]

    for si, (label, val, color) in enumerate(stats_items):
        sx = PAD + si * col_w
        parts.append(f'<text x="{sx}" y="{stats_y1}" fill="{MUTED}" font-size="9" letter-spacing="0.5">{label}</text>')
        parts.append(f'<text x="{sx}" y="{stats_y1 + 18}" fill="{color}" font-size="14" font-weight="600">{val}</text>')

    parts.append("</svg>")
    svg = "".join(parts)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[✓] Rendered heatmap SVG ({canvas_w}x{canvas_h}) -> {OUT_PATH}")


def main():
    if not os.path.exists(IN_PATH):
        print(f"[!] {IN_PATH} not found. Running fetch_contributions.py first...", file=sys.stderr)
        from fetch_contributions import main as fetch_main
        fetch_main()

    with open(IN_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    render(data)


if __name__ == "__main__":
    main()
