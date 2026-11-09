#!/usr/bin/env python3
"""
make_systems_card.py
Renders the "Systems Built & Production Infrastructure" Terminal Card as an animated SVG:
- 6 Production Systems:
  1. SAPPHIRE SUPER BRAIN (Autonomous Multi-Agent Lead Scoring & State Machine)
  2. JINNY SL TELEGRAM BOT (Reactive Control Room & Webhook CRM Relay)
  3. OPENBOT CLUSTER (10-Node 24/7 Autonomous Brand OS)
  4. GUANGDONG SOURCING WEDGE (Factory-Direct Dongguan/Shenzhen Manufacturing)
  5. DTC PROFIT SPRINT (Direct-Response CRO, VSL Funnels & Retention Loops)
  6. TRI-SEARCH SEO/GEO/AEO (Knowledge Graph & AI Engine Dominance Radar)
- Animated staggered card fade-in & flowing status indicators
- Width: 860px, Height: 300px

Output: systems-card.svg
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "systems-card.svg")

CANVAS_W = 860
CANVAS_H = 300
PAD = 20
TITLEBAR_H = 34

BG = "#080c10"
BG2 = "#0d141f"
FRAME = "#21262d"
BORDER_HIGHLIGHT = "#30363d"
TITLE_TEXT = "#7d8590"
TEXT = "#e6edf3"
MUTED = "#8b949e"
CYAN = "#38bdf8"
ACCENT = "#58a6ff"
GREEN = "#39d353"
GOLD = "#e3b341"
PURPLE = "#bc8cff"
PINK = "#f472b6"


def render():
    css = """
@keyframes node-fade {
  0%   { opacity: 0; transform: translateY(10px); }
  100% { opacity: 1; transform: translateY(0); }
}
@keyframes live-ping {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.3; transform: scale(0.85); }
}
.system-card {
  opacity: 0;
  animation: node-fade 0.5s cubic-bezier(0.16, 1, 0.3, 1) both;
}
.live-glow {
  animation: live-ping 1.8s ease-in-out infinite;
  transform-box: fill-box;
  transform-origin: center;
}
""".strip()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
        f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">',
        f'<style>{css}</style>',
        '<defs>',
        f'<linearGradient id="sysBg" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0%" stop-color="{BG2}"/>',
        f'<stop offset="100%" stop-color="{BG}"/>',
        '</linearGradient>',
        f'<linearGradient id="tileGrad" x1="0" y1="0" x2="1" y2="1">',
        f'<stop offset="0%" stop-color="#141a24"/>',
        f'<stop offset="100%" stop-color="#0a0e14"/>',
        '</linearGradient>',
        '</defs>',
        f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="10" fill="url(#sysBg)"/>',
        f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="10" fill="none" stroke="{BORDER_HIGHLIGHT}" stroke-width="1"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{BORDER_HIGHLIGHT}" stroke-width="1"/>',
    ]

    # macOS window buttons
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

    parts.append(
        f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" '
        f'text-anchor="middle">polin@sapphire: ~/systems_built --status=active</text>'
    )

    # Live Status Badge
    parts.append(f'<circle class="live-glow" cx="{CANVAS_W - PAD - 170}" cy="{TITLEBAR_H/2}" r="4.5" fill="{GREEN}"/>')
    parts.append(f'<text x="{CANVAS_W - PAD}" y="{TITLEBAR_H/2 + 4}" fill="{GREEN}" font-size="11" font-weight="600" text-anchor="end">6 ENGINES OPERATIONAL</text>')

    systems = [
        {
            "name": "🧠 SAPPHIRE BRAIN",
            "tag": "MULTI-AGENT OS",
            "desc": "Autonomous lead scoring, ICP queue & state machine",
            "stat": "105+ Leads • Every 4h Sync",
            "color": PURPLE,
            "delay": 0.08,
        },
        {
            "name": "⚡ JINNY SL TELEGRAM",
            "tag": "BOT CONTROL ROOM",
            "desc": "Realtime command center, CRM webhooks & relays",
            "stat": "10 Inboxes • 116+ Sends Live",
            "color": CYAN,
            "delay": 0.14,
        },
        {
            "name": "🤖 OPENBOT CLUSTER",
            "tag": "10-NODE AGENTS",
            "desc": "Money Maker, Intel, Art Machine & Revenue Engine",
            "stat": "24/7 Asynchronous Mesh",
            "color": GREEN,
            "delay": 0.20,
        },
        {
            "name": "🏭 GUANGDONG WEDGE",
            "tag": "SUPPLY CHAIN COGS",
            "desc": "Factory-direct sourcing across Shenzhen & Dongguan",
            "stat": "30% - 50% COGS Slashed",
            "color": GOLD,
            "delay": 0.26,
        },
        {
            "name": "📈 DTC PROFIT SPRINT",
            "tag": "D2C REVENUE ENGINE",
            "desc": "Direct-response funnels, mobile drawers & VSLs",
            "stat": "60+ Stores Audited",
            "color": PINK,
            "delay": 0.32,
        },
        {
            "name": "🎯 TRI-SEARCH ENGINE",
            "tag": "SEO / GEO / AEO",
            "desc": "Entity Knowledge Graph & AI Engine Pos-0 Dominance",
            "stat": "Google • Perplexity • GPT",
            "color": ACCENT,
            "delay": 0.38,
        },
    ]

    cols = 3
    rows = 2
    gap_x = 14
    gap_y = 12
    card_w = (CANVAS_W - PAD * 2 - (cols - 1) * gap_x) / cols
    card_h = (CANVAS_H - TITLEBAR_H - 18 - (rows - 1) * gap_y - 12) / rows
    start_y = TITLEBAR_H + 16

    for idx, sys_item in enumerate(systems):
        r = idx // cols
        c = idx % cols
        x = PAD + c * (card_w + gap_x)
        y = start_y + r * (card_h + gap_y)

        parts.append(
            f'<g class="system-card" style="animation-delay:{sys_item["delay"]:.2f}s">'
            f'<rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" rx="7" '
            f'fill="url(#tileGrad)" stroke="{FRAME}" stroke-width="1.2"/>'
            f'<rect x="{x}" y="{y}" width="{card_w}" height="3" rx="1.5" fill="{sys_item["color"]}"/>'
        )

        # Header: Name + Tag
        parts.append(
            f'<text x="{x + 12}" y="{y + 22}" fill="{TEXT}" font-size="12" font-weight="700">'
            f'{sys_item["name"]}</text>'
        )
        badge_w = len(sys_item["tag"]) * 6 + 12
        parts.append(
            f'<rect x="{x + card_w - badge_w - 10}" y="{y + 11}" width="{badge_w}" height="16" rx="4" '
            f'fill="{sys_item["color"]}18" stroke="{sys_item["color"]}55" stroke-width="0.8"/>'
            f'<text x="{x + card_w - badge_w/2 - 10}" y="{y + 22}" fill="{sys_item["color"]}" font-size="9" '
            f'font-weight="600" text-anchor="middle">{sys_item["tag"]}</text>'
        )

        # Description
        parts.append(
            f'<text x="{x + 12}" y="{y + 45}" fill="{MUTED}" font-size="10.5">'
            f'{sys_item["desc"]}</text>'
        )

        # Metric / Status Footer
        parts.append(
            f'<line x1="{x + 12}" y1="{y + card_h - 26}" x2="{x + card_w - 12}" y2="{y + card_h - 26}" '
            f'stroke="{FRAME}" stroke-width="0.8"/>'
            f'<circle cx="{x + 16}" cy="{y + card_h - 13}" r="3" fill="{sys_item["color"]}"/>'
            f'<text x="{x + 26}" y="{y + card_h - 10}" fill="{sys_item["color"]}" font-size="10" font-weight="600">'
            f'{sys_item["stat"]}</text>'
            f'</g>'
        )

    parts.append("</svg>")
    svg = "".join(parts)

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[✓] Rendered Systems Built Card SVG ({CANVAS_W}x{CANVAS_H}) -> {OUT}")


if __name__ == "__main__":
    render()
