#!/usr/bin/env python3
"""
make_info_card.py
Renders a high-tech, neofetch-style terminal system card as an animated SVG:
- Title bar with macOS control buttons
- Animated line-by-line staggered fade and slide-in
- Tech stack, AI swarm connectors, supply chain highlights
- Terminal ANSI color palette bar
- Aligns side-by-side with polin-ascii.svg (Width: 490px, Height: 430px)

Output: neofetch-card.svg
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "neofetch-card.svg")

CANVAS_W = 490
CANVAS_H = 430
PAD = 20
TITLEBAR_H = 34

BG = "#0a0e14"
BG2 = "#0e1624"
FRAME = "#30363d"
TITLE_TEXT = "#7d8590"
TEXT = "#e6edf3"
MUTED = "#8b949e"
CYAN = "#38bdf8"
ACCENT = "#58a6ff"
GREEN = "#39d353"
GOLD = "#e3b341"
PURPLE = "#bc8cff"
PINK = "#f472b6"

# Neofetch data points
ROWS = [
    ("OS", "Sapphire OS v2.0 (Autonomous Revenue Engine)", GREEN),
    ("Host", "Guangdong Core x US DTC Infrastructure", TEXT),
    ("Kernel", "Polin-Brain / Antigravity AGY-2.4", CYAN),
    ("Role", "Founder @ Sapphire Lead · DTC Architect", GOLD),
    ("AI Swarms", "Claude 3.5 · Grok-2/X · Codex · Gemini", PURPLE),
    ("Connectors", "Telegram Relay · Shared Brain · Signals Radar", ACCENT),
    ("Sourcing", "Guangdong Direct Mesh (-40% Physical COGS)", PINK),
    ("Tech Stack", "Python, TypeScript, Next.js, Shell, FastAPIs", TEXT),
    ("Uptime", "24/7/365 (116+ sends · 10 Warmed Inboxes)", GREEN),
    ("Email", "contact.salehinahmedpolin@gmail.com", CYAN),
    ("Base", "Guangdong, China · Dhaka, Bangladesh", MUTED),
]

PALETTE_COLORS = ["#ff5f56", "#ffbd2e", "#27c93f", "#38bdf8", "#58a6ff", "#bc8cff", "#f472b6", "#e6edf3"]


def render():
    css = """
@keyframes slide-in {
  0%   { opacity: 0; transform: translateX(-14px); }
  100% { opacity: 1; transform: translateX(0); }
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.35; }
}
.line { opacity: 0; animation: slide-in 0.45s cubic-bezier(0.16, 1, 0.3, 1) both; }
.live-dot { animation: pulse-dot 1.8s infinite ease-in-out; }
""".strip()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
        f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">',
        f'<style>{css}</style>',
        '<defs>',
        f'<linearGradient id="infoBg" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0%" stop-color="{BG2}"/>',
        f'<stop offset="100%" stop-color="{BG}"/>',
        '</linearGradient>',
        '</defs>',
        f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="10" fill="url(#infoBg)"/>',
        f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="10" fill="none" stroke="{FRAME}" stroke-width="1"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}" stroke-width="1"/>',
    ]

    # macOS window buttons
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

    parts.append(
        f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" '
        f'text-anchor="middle">polin@sapphire: ~$ neofetch</text>'
    )
    
    # Pulse status icon
    parts.append(f'<circle class="live-dot" cx="{CANVAS_W - PAD - 72}" cy="{TITLEBAR_H/2}" r="4" fill="{GREEN}"/>')
    parts.append(f'<text x="{CANVAS_W - PAD}" y="{TITLEBAR_H/2 + 4}" fill="{GREEN}" font-size="11" text-anchor="end">ONLINE</text>')

    # Terminal Header
    cur_y = TITLEBAR_H + 24
    header_delay = 0.05
    parts.append(
        f'<g class="line" style="animation-delay:{header_delay:.2f}s">'
        f'<text x="{PAD}" y="{cur_y}" fill="{ACCENT}" font-size="14" font-weight="700">polin@sapphire-lead</text>'
        f'</g>'
    )
    cur_y += 14
    parts.append(
        f'<g class="line" style="animation-delay:{header_delay + 0.05:.2f}s">'
        f'<text x="{PAD}" y="{cur_y}" fill="{FRAME}" font-size="12">------------------------------------------------</text>'
        f'</g>'
    )

    # Info Rows
    cur_y += 20
    row_gap = 21
    for idx, (key, val, color) in enumerate(ROWS):
        delay = 0.12 + idx * 0.045
        label = f"{key}:".ljust(11)
        parts.append(
            f'<g class="line" style="animation-delay:{delay:.3f}s">'
            f'<text x="{PAD}" y="{cur_y}" font-size="11">'
            f'<tspan fill="{CYAN}" font-weight="600">{label}</tspan>'
            f'<tspan fill="{color}">{val}</tspan>'
            f'</text>'
            f'</g>'
        )
        cur_y += row_gap

    # Palette blocks
    cur_y += 6
    palette_delay = 0.12 + len(ROWS) * 0.045
    parts.append(f'<g class="line" style="animation-delay:{palette_delay:.3f}s">')
    parts.append(f'<text x="{PAD}" y="{cur_y + 11}" fill="{MUTED}" font-size="11">Palette:    </text>')
    
    block_start_x = PAD + 76
    for pi, pcol in enumerate(PALETTE_COLORS):
        bx = block_start_x + pi * 24
        parts.append(f'<rect x="{bx}" y="{cur_y}" width="20" height="13" rx="3" fill="{pcol}"/>')
    parts.append('</g>')

    # Terminal blinking cursor at bottom
    cur_y += 34
    prompt_y = cur_y
    parts.append(f'<line x1="{PAD}" y1="{prompt_y - 14}" x2="{CANVAS_W - PAD}" y2="{prompt_y - 14}" stroke="{FRAME}" stroke-width="1"/>')
    parts.append(
        f'<text x="{PAD}" y="{prompt_y + 4}" fill="{TITLE_TEXT}" font-size="11">'
        f'polin@sapphire:~$ <tspan fill="{GREEN}">ready --autonomous</tspan>'
        f'</text>'
    )
    parts.append(
        f'<rect x="{PAD + 205}" y="{prompt_y - 7}" width="7" height="13" fill="{GREEN}">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/>'
        f'</rect>'
    )

    parts.append("</svg>")
    svg = "".join(parts)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[✓] Rendered neofetch info card SVG ({CANVAS_W}x{CANVAS_H}) -> {OUT}")


if __name__ == "__main__":
    render()
