#!/usr/bin/env python3
"""
make_mesh_card.py
Renders the Autonomous Multi-Agent Swarm & Connectors Telemetry HUD SVG:
- Connectors: Grok Bot, Claude 3.5, Codex / Antigravity, Telegram Control Room, Guangdong Sourcing
- Animated flowing data pulses along connector lines
- Realtime telemetry status and node operational metrics
- Full-width terminal HUD (Width: 880px, Height: 270px)

Output: ai-mesh-card.svg
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "ai-mesh-card.svg")

CANVAS_W = 880
CANVAS_H = 270
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
@keyframes pulse-flow {
  0% { stroke-dashoffset: 24; }
  100% { stroke-dashoffset: 0; }
}
@keyframes node-fade {
  0%   { opacity: 0; transform: translateY(8px); }
  100% { opacity: 1; transform: translateY(0); }
}
@keyframes live-ping {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.3; transform: scale(0.85); }
}
.flow-line {
  stroke-dasharray: 6 6;
  animation: pulse-flow 1.2s linear infinite;
}
.node-card {
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
        f'<linearGradient id="meshBg" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0%" stop-color="{BG2}"/>',
        f'<stop offset="100%" stop-color="{BG}"/>',
        '</linearGradient>',
        f'<linearGradient id="nodeGrad" x1="0" y1="0" x2="1" y2="1">',
        f'<stop offset="0%" stop-color="#161b22"/>',
        f'<stop offset="100%" stop-color="#0d1117"/>',
        '</linearGradient>',
        '</defs>',
        f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="10" fill="url(#meshBg)"/>',
        f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="10" fill="none" stroke="{BORDER_HIGHLIGHT}" stroke-width="1"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{BORDER_HIGHLIGHT}" stroke-width="1"/>',
    ]

    # macOS window buttons
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

    parts.append(
        f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" '
        f'text-anchor="middle">polin@sapphire: ~/ai_mesh --telemetry --watch</text>'
    )

    # Live Status Badge
    parts.append(f'<circle class="live-glow" cx="{CANVAS_W - PAD - 150}" cy="{TITLEBAR_H/2}" r="4.5" fill="{GREEN}"/>')
    parts.append(f'<text x="{CANVAS_W - PAD}" y="{TITLEBAR_H/2 + 4}" fill="{GREEN}" font-size="11" font-weight="600" text-anchor="end">SWARM MESH ACTIVE</text>')

    # Four Swarm Nodes
    nodes = [
        {
            "name": "🧠 CLAUDE 3.5 SONNET",
            "tag": "STRATEGY & BRAIN",
            "desc": "Lead scoring, verified signals & sequence copywriting",
            "stat": "Sync: Every 4h",
            "color": PURPLE,
            "delay": 0.1,
        },
        {
            "name": "⚡ GROK BOT (X / LIN)",
            "tag": "SIGNALS RADAR",
            "desc": "Executive profiling, real-time trigger scans & intelligence",
            "stat": "Radar: 24/7 Scan",
            "color": CYAN,
            "delay": 0.2,
        },
        {
            "name": "🛠️ CODEX / AGY CORE",
            "tag": "EXECUTION ENGINE",
            "desc": "Telegram control room, tool orchestration & autonomous tasks",
            "stat": "Latency: < 200ms",
            "color": GREEN,
            "delay": 0.3,
        },
        {
            "name": "🏭 GUANGDONG MESH",
            "tag": "SUPPLY CHAIN COGS",
            "desc": "Factory-direct sourcing wedge & packaging margin expansion",
            "stat": "Savings: 30-50%",
            "color": GOLD,
            "delay": 0.4,
        },
    ]

    node_w = 196
    node_h = 136
    node_gap = (CANVAS_W - PAD * 2 - (node_w * 4)) / 3
    node_y = TITLEBAR_H + 20

    # Animated Flow Lines connecting nodes horizontally
    conn_y = node_y + node_h / 2
    for i in range(3):
        x_start = PAD + (i + 1) * node_w + i * node_gap
        x_end = x_start + node_gap
        parts.append(
            f'<line class="flow-line" x1="{x_start}" y1="{conn_y}" x2="{x_end}" y2="{conn_y}" '
            f'stroke="{ACCENT}" stroke-width="2" opacity="0.6"/>'
        )

    # Render Node Cards
    for i, n in enumerate(nodes):
        nx = PAD + i * (node_w + node_gap)
        parts.append(
            f'<g class="node-card" style="animation-delay:{n["delay"]:.2f}s">'
            f'<rect x="{nx}" y="{node_y}" width="{node_w}" height="{node_h}" rx="8" '
            f'fill="url(#nodeGrad)" stroke="{FRAME}" stroke-width="1.2"/>'
            f'<rect x="{nx}" y="{node_y}" width="{node_w}" height="4" rx="2" fill="{n["color"]}"/>'
        )
        
        # Node Header
        parts.append(
            f'<text x="{nx + 12}" y="{node_y + 24}" fill="{n["color"]}" font-size="11" font-weight="700">{n["name"]}</text>'
            f'<text x="{nx + 12}" y="{node_y + 40}" fill="{MUTED}" font-size="9" letter-spacing="0.5">{n["tag"]}</text>'
        )

        # Node Description (Wrapped lines)
        desc_words = n["desc"].split()
        line1 = " ".join(desc_words[:4])
        line2 = " ".join(desc_words[4:])
        parts.append(
            f'<text x="{nx + 12}" y="{node_y + 64}" fill="{TEXT}" font-size="9.5">{line1}</text>'
            f'<text x="{nx + 12}" y="{node_y + 78}" fill="{TEXT}" font-size="9.5">{line2}</text>'
        )

        # Node Status Footer inside box
        parts.append(
            f'<line x1="{nx + 12}" y1="{node_y + 98}" x2="{nx + node_w - 12}" y2="{node_y + 98}" stroke="{FRAME}" stroke-width="1"/>'
            f'<circle cx="{nx + 18}" cy="{node_y + 115}" r="3.5" fill="{GREEN}"/>'
            f'<text x="{nx + 28}" y="{node_y + 118}" fill="{GREEN}" font-size="9" font-weight="600">{n["stat"]}</text>'
        )
        parts.append('</g>')

    # Bottom Telemetry Summary Ticker
    footer_y = node_y + node_h + 36
    parts.append(f'<line x1="{PAD}" y1="{node_y + node_h + 16}" x2="{CANVAS_W - PAD}" y2="{node_y + node_h + 16}" stroke="{FRAME}" stroke-width="1"/>')
    parts.append(
        f'<text x="{PAD}" y="{footer_y}" font-size="10">'
        f'<tspan fill="{MUTED}">ARCHITECTURE: </tspan>'
        f'<tspan fill="{ACCENT}">Shared-Brain Swarm (sapphire-brain)</tspan>'
        f'<tspan fill="{FRAME}">  |  </tspan>'
        f'<tspan fill="{MUTED}">CHANNELS: </tspan>'
        f'<tspan fill="{CYAN}">Telegram + 10 Warm Inboxes</tspan>'
        f'<tspan fill="{FRAME}">  |  </tspan>'
        f'<tspan fill="{MUTED}">STATUS: </tspan>'
        f'<tspan fill="{GREEN}">2 Autonomous Sprints Active</tspan>'
        f'</text>'
    )

    parts.append("</svg>")
    svg = "".join(parts)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[✓] Rendered AI Mesh Telemetry SVG ({CANVAS_W}x{CANVAS_H}) -> {OUT}")


if __name__ == "__main__":
    render()
