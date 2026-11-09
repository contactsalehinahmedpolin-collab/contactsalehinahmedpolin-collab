#!/usr/bin/env python3
"""
render_cards.py
Renders the complete luxury animated SVG card suite into cards/:
1. cards/hero.svg - Editorial Hero Card with name shine sweep and embedded typing ASCII portrait
2. cards/heatmap.svg - Sapphire-blue contribution graph with diagonal reveal
3. cards/activity.svg - 12-month activity bar chart with streak telemetry
4. cards/tile-growth.svg - 30-Day Profit Sprint & DTC Funnels (33.3% width)
5. cards/tile-sourcing.svg - Guangdong Factory-Direct Wedge (-45% COGS) (33.3% width)
6. cards/tile-swarms.svg - Autonomous AI Swarm Mesh (Claude + Grok + Codex) (33.3% width)
7. cards/repo-sapphire.svg - sapphire-brain showcase repo
8. cards/repo-neuroflex.svg - NeuroFlex DTC growth showcase
9. cards/repo-jinny.svg - Jinny Telegram Telemetry Control Room
10. cards/ai-mesh.svg - Full-width AI Swarm Telemetry & Connector HUD
"""
import datetime
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
DATA_FILE = os.path.join(ROOT, "data", "contributions.json")
OUT_DIR = os.path.join(ROOT, "cards")
PORTRAIT_SVG = os.path.join(ROOT, "polin-ascii.svg")

W = 880  # Standard GitHub README full column width
GAP = 12
BOTTOM = 14
COL = W / 3

# Dark Luxury Obsidian & Sapphire Color Palette
DARK_BG = "#0d1117"
DARK_CARD = "#111827"
DARK_BORDER = "#30363d"
DARK_BORDER_LIGHT = "#3b434d"
TEXT_PRIMARY = "#f0f6fc"
TEXT_SECONDARY = "#8b949e"
TEXT_MUTED = "#6e7681"

# Brand Accents
SAPPHIRE_BLUE = "#2f55ff"
SAPPHIRE_LIGHT = "#58a6ff"
CYAN_ACCENT = "#38bdf8"
EMERALD_GREEN = "#10b981"
GOLD_ACCENT = "#f59e0b"
PURPLE_ACCENT = "#a855f7"

SERIF = "Georgia, 'Times New Roman', serif"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Monaco, Consolas, monospace"

BASE_CSS = """
@keyframes rise { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: none; } }
@keyframes fade { from { opacity: 0; } to { opacity: 1; } }
@keyframes grow { from { transform: scaleY(0); } to { transform: scaleY(1); } }
@keyframes pop { 0% { opacity: 0; transform: scale(.4); } 70% { opacity: 1; transform: scale(1.15); } 100% { opacity: 1; transform: none; } }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: .25; } }
@keyframes nudge { 0%, 100% { transform: none; } 50% { transform: translateX(5px); } }
@keyframes tilein {
  0% { opacity: 0; transform: translateY(60px) scale(.85); }
  60% { opacity: 1; transform: translateY(-6px) scale(1.02); }
  100% { opacity: 1; transform: none; }
}
@keyframes shine-sweep {
  0% { transform: translateX(-400px); }
  25%, 100% { transform: translateX(500px); }
}
@keyframes ring { 0% { opacity: .7; transform: scale(.2); } 100% { opacity: 0; transform: scale(2.2); } }
@keyframes pulse-flow { 0% { stroke-dashoffset: 24; } 100% { stroke-dashoffset: 0; } }

.r { opacity: 0; animation: rise .8s cubic-bezier(.2,.7,.2,1) both; transform-box: fill-box; }
.f { opacity: 0; animation: fade .9s ease-out both; }
.g { transform-box: fill-box; transform-origin: bottom; transform: scaleY(0); animation: grow .8s cubic-bezier(.2,.7,.2,1) both; }
.p { opacity: 0; transform-box: fill-box; transform-origin: center; animation: pop .4s ease-out both; }
.live { animation: pulse 1.6s ease-in-out infinite; }
.n { transform-box: fill-box; animation: nudge 1.8s ease-in-out infinite; }
.ti { opacity: 0; transform-box: fill-box; transform-origin: 50% 60%; animation: tilein 1s cubic-bezier(.2,.8,.2,1) both; }
.rg { opacity: 0; transform-box: fill-box; transform-origin: center; animation: ring 1.2s ease-out both; }
.flow-line { stroke-dasharray: 6 6; animation: pulse-flow 1.2s linear infinite; }

@media (prefers-reduced-motion: reduce) {
  .r,.f,.g,.p,.live,.n,.ti,.rg,.flow-line { animation: none !important; opacity: 1 !important; transform: none !important; }
}
"""


def svg(w, h, body, label, extra_css="", left=0, right=0, bottom=BOTTOM):
    if left:
        body = f'<g transform="translate({left:.3f} 0)">{body}</g>'
    full_w, full_h = w + left + right, h + bottom
    css = BASE_CSS + extra_css
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{full_w:.3f}" height="{full_h}" '
        f'viewBox="0 0 {full_w:.3f} {full_h}" role="img" aria-label="{html.escape(label)}">'
        f'<title>{html.escape(label)}</title>'
        f'<style>{css}</style>'
        f'{body}'
        f'</svg>'
    )


def write_card(filename, content):
    os.makedirs(OUT_DIR, exist_ok=True)
    filepath = os.path.join(OUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[✓] Rendered cards/{filename} ({len(content) / 1024:.1f} KB)")


def d(s):
    return f'style="animation-delay:{s:.2f}s"'


def wrap_text(text, max_chars):
    lines, current = [], ""
    for word in text.split():
        if current and len(current) + 1 + len(word) > max_chars:
            lines.append(current)
            current = word
        else:
            current = f"{current} {word}".strip()
    if current:
        lines.append(current)
    return lines


# -----------------------------------------------------------------------------
# 1. HERO CARD (Width: 880px, Height: 420px)
# -----------------------------------------------------------------------------
def render_hero():
    h = 420
    portrait_lines = []
    
    if os.path.exists(PORTRAIT_SVG):
        src = open(PORTRAIT_SVG, encoding="utf-8").read()
        rows = re.findall(r'<text xml:space="preserve"[^>]*\by="([\d.]+)"[^>]*>(.*?)</text>', src, re.S)
        for i, (y, txt) in enumerate(rows):
            portrait_lines.append(
                f'<text class="f" style="animation-delay:{0.20 + i * 0.016:.3f}s;animation-duration:.35s" '
                f'xml:space="preserve" x="20" y="{y}" fill="{CYAN_ACCENT}" font-size="6.3" '
                f'textLength="350" lengthAdjust="spacing">{txt}</text>'
            )

    body = f"""
<defs>
  <linearGradient id="heroGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#0a0e17"/>
    <stop offset="50%" stop-color="#111827"/>
    <stop offset="100%" stop-color="#0a0e14"/>
  </linearGradient>
  <linearGradient id="textShine" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="600" y2="0">
    <stop offset="0%" stop-color="{TEXT_PRIMARY}"/>
    <stop offset="40%" stop-color="{TEXT_PRIMARY}"/>
    <stop offset="50%" stop-color="{SAPPHIRE_LIGHT}"/>
    <stop offset="60%" stop-color="{TEXT_PRIMARY}"/>
    <stop offset="100%" stop-color="{TEXT_PRIMARY}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-600 0;600 0;600 0"
      keyTimes="0;.45;1" dur="6.5s" begin="1.5s" repeatCount="indefinite"/>
  </linearGradient>
  <filter id="glow">
    <feGaussianBlur stdDeviation="3" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>

<!-- Card Frame -->
<rect width="{W}" height="{h}" rx="16" fill="url(#heroGrad)" stroke="{DARK_BORDER}" stroke-width="1.5"/>

<!-- Top Status Badge -->
<g class="f" {d(0.05)}>
  <rect x="44" y="44" width="310" height="28" rx="14" fill="#161f38" stroke="#1d4ed8" stroke-width="1"/>
  <circle class="live" cx="58" cy="58" r="4.5" fill="{EMERALD_GREEN}"/>
  <text x="70" y="62" font-family="{MONO}" font-size="11" font-weight="600" letter-spacing="1" fill="{CYAN_ACCENT}">FOUNDER @ SAPPHIRE LEAD · 24/7 MESH</text>
</g>

<!-- Big Editorial Name with Animated Gradient Shine -->
<text class="r" {d(0.18)} x="42" y="152" font-family="{SERIF}" font-size="78" font-weight="700" letter-spacing="-1.5" fill="{TEXT_PRIMARY}">Salehin</text>
<text class="r" {d(0.32)} x="42" y="228" font-family="{SERIF}" font-style="italic" font-size="78" letter-spacing="-1.5" fill="url(#textShine)">Ahmed Polin</text>

<!-- Core Mission Statement -->
<g class="r" {d(0.50)}>
  <text x="44" y="274" font-family="{SANS}" font-size="16" font-weight="500" fill="{TEXT_PRIMARY}">Autonomous AI Swarms · US DTC Funnels · Guangdong Sourcing Wedge</text>
  <text x="44" y="302" font-family="{SANS}" font-size="14" fill="{TEXT_SECONDARY}">Slashing 30–50% off physical unit COGS in Guangdong to completely fund</text>
  <text x="44" y="324" font-family="{SANS}" font-size="14" fill="{TEXT_SECONDARY}">high-converting DTC growth engines, VSL checkout funnels &amp; retention loops.</text>
</g>

<!-- Footer Actions & Links -->
<g class="f" {d(0.72)}>
  <rect x="44" y="356" width="170" height="32" rx="8" fill="#1e293b" stroke="{DARK_BORDER_LIGHT}" stroke-width="1"/>
  <text x="60" y="377" font-family="{MONO}" font-size="12" font-weight="600" fill="{TEXT_PRIMARY}">salehinahmedpolin.com</text>
  <text class="n" x="222" y="377" font-family="{MONO}" font-size="13" fill="{SAPPHIRE_LIGHT}">↗</text>
  
  <text x="256" y="377" font-family="{MONO}" font-size="12" fill="{TEXT_MUTED}">|</text>
  <text x="274" y="377" font-family="{MONO}" font-size="12" fill="{TEXT_MUTED}">contact.salehinahmedpolin@gmail.com</text>
</g>

<!-- Right Side ASCII Portrait Terminal Box -->
<g transform="translate(485, 34)">
  <rect width="360" height="352" rx="12" fill="#090d14" stroke="{DARK_BORDER}" stroke-width="1.2"/>
  <line x1="0" y1="30" x2="360" y2="30" stroke="{DARK_BORDER}" stroke-width="1"/>
  <circle cx="16" cy="15" r="4" fill="#ff5f56"/>
  <circle cx="28" cy="15" r="4" fill="#ffbd2e"/>
  <circle cx="40" cy="15" r="4" fill="#27c93f"/>
  <text x="180" y="19" font-family="{MONO}" font-size="10" fill="{TEXT_MUTED}" text-anchor="middle">polin@sapphire: ~/avatar.sh</text>
  
  <g transform="translate(4, 18) scale(0.95)" font-family="{MONO}">
    {''.join(portrait_lines)}
  </g>
</g>
"""
    write_card("hero.svg", svg(W, h, body, "Salehin Ahmed Polin. Founder @ Sapphire Lead. Autonomous AI Swarms & DTC Growth Engineer."))


# -----------------------------------------------------------------------------
# 2. THREE BENTO TILES (Width: 285px each)
# -----------------------------------------------------------------------------
TILE_W, TILE_H = 880 / 3 - 8, 220

def render_tile(name, label, color, on_color, num, word, blurb, delay, pos):
    lines = wrap_text(blurb, 32)
    blurb_svg = "".join(
        f'<text class="r" {d(delay + 0.50 + i * 0.08)} x="22" y="{154 + i * 20}" font-family="{SANS}" '
        f'font-size="13.5" fill="{TEXT_SECONDARY}">{html.escape(l)}</text>'
        for i, l in enumerate(lines)
    )

    body = f"""
<defs>
  <clipPath id="card_{pos}"><rect width="{TILE_W}" height="{TILE_H}" rx="14"/></clipPath>
  <linearGradient id="tbg_{pos}" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#111827"/>
    <stop offset="100%" stop-color="#0a0e14"/>
  </linearGradient>
</defs>
<g class="ti" {d(delay)}>
  <g clip-path="url(#card_{pos})">
    <rect width="{TILE_W}" height="{TILE_H}" rx="14" fill="url(#tbg_{pos})" stroke="{DARK_BORDER}" stroke-width="1.2"/>
    <rect x="0" y="0" width="{TILE_W}" height="4" fill="{color}"/>
    <circle class="rg" {d(delay + 0.4)} cx="{TILE_W - 35}" cy="{TILE_H - 35}" r="50" fill="none" stroke="{color}" stroke-opacity=".3" stroke-width="2"/>
  </g>
  
  <!-- Category Tag -->
  <text class="r" {d(delay + 0.15)} x="22" y="38" font-family="{MONO}" font-size="11" font-weight="700" letter-spacing="1.2" fill="{color}">{label}</text>
  <text class="n" style="animation-delay:{delay + 1.2:.2f}s" x="{TILE_W - 28}" y="38" font-family="{MONO}" font-size="14" fill="{color}">→</text>

  <!-- Big Hero Metric -->
  <text class="r" {d(delay + 0.30)} x="20" y="104" font-family="{SERIF}" font-size="44" font-weight="700" fill="{TEXT_PRIMARY}">
    {num} <tspan font-style="italic" font-size="28" fill="{color}">{word}</tspan>
  </text>
  
  <line x1="22" y1="124" x2="{TILE_W - 22}" y2="124" stroke="{DARK_BORDER}" stroke-width="1"/>
  {blurb_svg}
</g>
"""
    write_card(f"{name}.svg", svg(TILE_W, TILE_H, body, f"{label}: {num} {word}. {blurb}",
                                 left=4 * pos, right=8 - 4 * pos))


# -----------------------------------------------------------------------------
# 3. LIVE CONTRIBUTION HEATMAP (Width: 880px, Height: 260px)
# -----------------------------------------------------------------------------
def render_heatmap(data):
    h = 260
    days = data.get("days", [])
    if not days:
        return

    first = datetime.date.fromisoformat(days[0]["date"])
    lead = (first.weekday() + 1) % 7
    cell, step, gx, gy = 12, 15, 46, 84
    
    # Sapphire Blue Heatmap Ramp
    BLUE_RAMP = ["#161f30", "#1e3a8a", "#2563eb", "#3b82f6", "#60a5fa", "#93c5fd"]
    
    cells, months, seen = [], [], set()
    for i, day in enumerate(days):
        k = i + lead
        cx, cy = gx + (k // 7) * step, gy + (k % 7) * step
        date = datetime.date.fromisoformat(day["date"])
        mkey = (date.year, date.month)
        if mkey not in seen and date.day <= 7:
            seen.add(mkey)
            months.append(
                f'<text class="f" {d(0.8 + len(months) * 0.04)} x="{cx}" y="{gy - 12}" '
                f'font-family="{MONO}" font-size="10" fill="{TEXT_MUTED}">{date.strftime("%b")}</text>'
            )
        lvl = day.get("level", 0)
        c = BLUE_RAMP[min(lvl, len(BLUE_RAMP) - 1)]
        delay = 0.5 + (k // 7) * 0.012 + (k % 7) * 0.03
        cells.append(
            f'<rect class="p" style="animation-delay:{delay:.3f}s" x="{cx}" y="{cy}" '
            f'width="{cell}" height="{cell}" rx="2.5" fill="{c}">'
            f'<title>{day["date"]}: {day["count"]} contributions</title></rect>'
        )

    # Weekday labels
    wlabels = []
    for wi, wname in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        y = gy + wi * step + 9
        wlabels.append(f'<text x="18" y="{y}" font-family="{MONO}" font-size="9" fill="{TEXT_MUTED}">{wname}</text>')

    # Legend
    leg_x = W - 180
    leg_y = gy + 7 * step + 18
    legend_svg = [f'<text x="{leg_x - 30}" y="{leg_y + 9}" font-family="{MONO}" font-size="10" fill="{TEXT_MUTED}">Less</text>']
    for li, lc in enumerate(BLUE_RAMP):
        legend_svg.append(f'<rect x="{leg_x + li * 14}" y="{leg_y}" width="11" height="11" rx="2" fill="{lc}"/>')
    legend_svg.append(f'<text x="{leg_x + len(BLUE_RAMP) * 14 + 8}" y="{leg_y + 9}" font-family="{MONO}" font-size="10" fill="{TEXT_MUTED}">More</text>')

    body = f"""
<rect width="{W}" height="{h}" rx="14" fill="{DARK_CARD}" stroke="{DARK_BORDER}" stroke-width="1.2"/>
<text class="f" {d(0.2)} x="46" y="44" font-family="{MONO}" font-size="11" font-weight="600" letter-spacing="1" fill="{CYAN_ACCENT}">LIVE CONTRIBUTION GRAPH · REFRESHED DAILY</text>
<text class="r" {d(0.35)} x="44" y="66" font-family="{SERIF}" font-size="28" font-weight="700" fill="{TEXT_PRIMARY}">
  {data.get("total_contributions", 0):,} <tspan font-style="italic" font-size="22" fill="{SAPPHIRE_LIGHT}">contributions in the last year</tspan>
</text>

{''.join(months)}
{''.join(wlabels)}
{''.join(cells)}
{''.join(legend_svg)}
"""
    write_card("heatmap.svg", svg(W, h, body, "Salehin Ahmed Polin Contribution Graph"))


# -----------------------------------------------------------------------------
# 4. ACTIVITY & 12-MONTH MONTHLY BAR CHART (Width: 880px, Height: 320px)
# -----------------------------------------------------------------------------
def render_activity(data):
    h = 320
    monthly_data = data.get("monthly", {})
    # Convert to sorted list of dicts
    sorted_months = sorted(monthly_data.keys())[-12:]
    monthly = [{"month": m, "total": monthly_data[m]} for m in sorted_months]
    
    if not monthly:
        return

    best = max(monthly, key=lambda m: m["total"])
    top = max(1, best["total"])
    x0, x1, base, maxh, gap = 46, 580, 260, 130, 10
    bw = (x1 - x0 - gap * (len(monthly) - 1)) / len(monthly)
    bars = []
    
    for i, m in enumerate(monthly):
        is_best = m is best
        bh = max(6, round(m["total"] / top * maxh))
        x = x0 + i * (bw + gap)
        fill = SAPPHIRE_LIGHT if is_best else (CYAN_ACCENT if i % 2 == 0 else "#2563eb")
        label = datetime.date.fromisoformat(m["month"] + "-01").strftime("%b")
        bars.append(
            f'<rect class="g" style="animation-delay:{0.8 + i * 0.05:.2f}s" x="{x:.1f}" y="{base - bh}" '
            f'width="{bw:.1f}" height="{bh}" rx="4" fill="{fill}"><title>{label}: {m["total"]:,}</title></rect>'
            f'<text class="f" style="animation-delay:{0.8 + i * 0.05:.2f}s" x="{x + bw / 2:.1f}" y="{base + 22}" '
            f'text-anchor="middle" font-family="{MONO}" font-size="11" fill="{TEXT_MUTED}">{label}</text>'
        )
        if is_best:
            bars.append(
                f'<text class="p" style="animation-delay:1.6s" x="{x + bw / 2:.1f}" y="{base - bh - 8}" '
                f'text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="600" fill="{SAPPHIRE_LIGHT}">{m["total"]:,}</text>'
            )

    cs = data.get("current_streak", 14)
    ls = data.get("longest_streak", 48)
    best_cnt = data.get("best_day", {}).get("count", 68)

    stats = [
        (f'{cs} <tspan font-style="italic" font-size="24">days</tspan>', f"current streak (longest: {ls}d)"),
        (f'{best_cnt} <tspan font-style="italic" font-size="24">commits</tspan>', "peak velocity day"),
        ("10 <tspan font-style='italic' font-size='24'>inboxes</tspan>", "warmed cold email mesh"),
    ]
    side = []
    for i, (big, small) in enumerate(stats):
        y = 96 + i * 78
        side.append(
            f'<g class="r" {d(1.1 + i * 0.15)}>'
            f'<text x="630" y="{y}" font-family="{SERIF}" font-size="36" font-weight="700" fill="{TEXT_PRIMARY}">{big}</text>'
            f'<text x="630" y="{y + 22}" font-family="{SANS}" font-size="12.5" fill="{TEXT_SECONDARY}">{small}</text>'
            f'</g>'
        )
        if i < 2:
            side.append(f'<line x1="630" y1="{y + 38}" x2="840" y2="{y + 38}" stroke="{DARK_BORDER}" stroke-width="1"/>')

    body = f"""
<rect width="{W}" height="{h}" rx="14" fill="{DARK_CARD}" stroke="{DARK_BORDER}" stroke-width="1.2"/>
<text class="f" {d(0.2)} x="46" y="44" font-family="{MONO}" font-size="11" font-weight="600" letter-spacing="1" fill="{CYAN_ACCENT}">ANNUAL ACTIVITY &amp; STREAK TELEMETRY</text>
<text class="r" {d(0.35)} x="44" y="80" font-family="{SERIF}" font-size="34" font-weight="700" fill="{TEXT_PRIMARY}">
  Monthly Output <tspan font-style="italic" font-size="26" fill="{SAPPHIRE_LIGHT}">Breakdown</tspan>
</text>
<line x1="600" y1="40" x2="600" y2="280" stroke="{DARK_BORDER}" stroke-width="1"/>
{''.join(bars)}
{''.join(side)}
"""
    write_card("activity.svg", svg(W, h, body, "Monthly contribution activity and streak telemetry"))


# -----------------------------------------------------------------------------
# 5. THREE SHOWCASE REPOSITORY CARDS (Width: 285px each)
# -----------------------------------------------------------------------------
REPO_W, REPO_H = 880 / 3 - 8, 180

def render_repo(name, title, desc, tag, color, pos):
    delay = 1.6 + pos * 0.12
    lines = wrap_text(desc, 32)
    desc_svg = "".join(
        f'<text class="r" {d(delay + 0.35 + i * 0.08)} x="20" y="{78 + i * 20}" font-family="{SANS}" '
        f'font-size="13" fill="{TEXT_SECONDARY}">{html.escape(l)}</text>'
        for i, l in enumerate(lines)
    )

    body = f"""
<rect width="{REPO_W}" height="{REPO_H}" rx="14" fill="{DARK_CARD}" stroke="{DARK_BORDER}" stroke-width="1.2"/>
<g class="r" {d(delay)}>
  <rect x="20" y="24" width="8" height="8" rx="2" fill="{color}"/>
  <text x="36" y="32" font-family="{SANS}" font-weight="700" font-size="16" fill="{TEXT_PRIMARY}">{html.escape(title)}</text>
  {desc_svg}
  <line x1="20" y1="{REPO_H - 36}" x2="{REPO_W - 20}" y2="{REPO_H - 36}" stroke="{DARK_BORDER}" stroke-width="1"/>
  <circle cx="26" cy="{REPO_H - 18}" r="3.5" fill="{color}"/>
  <text x="36" y="{REPO_H - 14}" font-family="{MONO}" font-size="10.5" font-weight="600" fill="{TEXT_MUTED}">{html.escape(tag)}</text>
  <text class="n" x="{REPO_W - 28}" y="{REPO_H - 14}" font-family="{MONO}" font-size="12" fill="{color}">↗</text>
</g>
"""
    write_card(f"repo-{name}.svg", svg(REPO_W, REPO_H, body, f"{title}: {desc}", left=4 * pos, right=8 - 4 * pos))


# -----------------------------------------------------------------------------
# 6. AUTONOMOUS AI SWARM & CONNECTORS HUD (Width: 880px, Height: 260px)
# -----------------------------------------------------------------------------
def render_ai_mesh():
    h = 260
    nodes = [
        {"name": "🧠 CLAUDE 3.5 SONNET", "tag": "STRATEGY & BRAIN", "desc": "Lead scoring, verified signals & sequence copywriting", "color": PURPLE_ACCENT, "stat": "Sync: Every 4h"},
        {"name": "⚡ GROK BOT (X / LIN)", "tag": "SIGNALS RADAR", "desc": "Executive profiling, trigger scans & social intelligence", "color": CYAN_ACCENT, "stat": "Radar: 24/7 Scan"},
        {"name": "🛠️ CODEX / AGY CORE", "tag": "EXECUTION ENGINE", "desc": "Telegram control room, tool runner & autonomous CRM", "color": EMERALD_GREEN, "stat": "Latency: < 200ms"},
        {"name": "🏭 GUANGDONG MESH", "tag": "SUPPLY CHAIN COGS", "desc": "Direct factory quotes, bottles & -45% COGS reduction", "color": GOLD_ACCENT, "stat": "Savings: 30-50%"},
    ]
    node_w = 196
    node_h = 136
    node_gap = (W - 40 - (node_w * 4)) / 3
    node_y = 68

    conn_lines = []
    conn_y = node_y + node_h / 2
    for i in range(3):
        x_start = 20 + (i + 1) * node_w + i * node_gap
        x_end = x_start + node_gap
        conn_lines.append(
            f'<line class="flow-line" x1="{x_start}" y1="{conn_y}" x2="{x_end}" y2="{conn_y}" '
            f'stroke="{SAPPHIRE_LIGHT}" stroke-width="2" opacity="0.6"/>'
        )

    node_cards = []
    for i, n in enumerate(nodes):
        nx = 20 + i * (node_w + node_gap)
        delay = 0.2 + i * 0.12
        desc_words = n["desc"].split()
        line1 = " ".join(desc_words[:4])
        line2 = " ".join(desc_words[4:])
        node_cards.append(
            f'<g class="r" {d(delay)}>'
            f'<rect x="{nx}" y="{node_y}" width="{node_w}" height="{node_h}" rx="10" fill="#0c1017" stroke="{DARK_BORDER}" stroke-width="1.2"/>'
            f'<rect x="{nx}" y="{node_y}" width="{node_w}" height="3.5" rx="2" fill="{n["color"]}"/>'
            f'<text x="{nx + 12}" y="{node_y + 24}" fill="{n["color"]}" font-family="{MONO}" font-size="10.5" font-weight="700">{n["name"]}</text>'
            f'<text x="{nx + 12}" y="{node_y + 40}" fill="{TEXT_MUTED}" font-family="{MONO}" font-size="8.5" letter-spacing="0.5">{n["tag"]}</text>'
            f'<text x="{nx + 12}" y="{node_y + 64}" fill="{TEXT_PRIMARY}" font-family="{SANS}" font-size="9.5">{line1}</text>'
            f'<text x="{nx + 12}" y="{node_y + 78}" fill="{TEXT_PRIMARY}" font-family="{SANS}" font-size="9.5">{line2}</text>'
            f'<line x1="{nx + 12}" y1="{node_y + 98}" x2="{nx + node_w - 12}" y2="{node_y + 98}" stroke="{DARK_BORDER}" stroke-width="1"/>'
            f'<circle cx="{nx + 18}" cy="{node_y + 115}" r="3.5" fill="{EMERALD_GREEN}"/>'
            f'<text x="{nx + 28}" y="{node_y + 118}" fill="{EMERALD_GREEN}" font-family="{MONO}" font-size="9" font-weight="600">{n["stat"]}</text>'
            f'</g>'
        )

    body = f"""
<rect width="{W}" height="{h}" rx="14" fill="{DARK_CARD}" stroke="{DARK_BORDER}" stroke-width="1.2"/>
<text class="f" {d(0.1)} x="20" y="36" font-family="{MONO}" font-size="11" font-weight="600" letter-spacing="1" fill="{CYAN_ACCENT}">AUTONOMOUS MULTI-AGENT SWARM MESH · 24/7 TELEMETRY</text>
<g class="f" {d(0.1)}>
  <circle class="live" cx="{W - 160}" cy="32" r="4.5" fill="{EMERALD_GREEN}"/>
  <text x="{W - 20}" y="36" font-family="{MONO}" font-size="11" font-weight="600" fill="{EMERALD_GREEN}" text-anchor="end">SWARM SYNCHRONIZED</text>
</g>

{''.join(conn_lines)}
{''.join(node_cards)}

<line x1="20" y1="{node_y + node_h + 16}" x2="{W - 20}" y2="{node_y + node_h + 16}" stroke="{DARK_BORDER}" stroke-width="1"/>
<text x="20" y="{node_y + node_h + 34}" font-family="{MONO}" font-size="10">
  <tspan fill="{TEXT_MUTED}">SHARED REPO: </tspan><tspan fill="{SAPPHIRE_LIGHT}">sapphire-brain</tspan>
  <tspan fill="{DARK_BORDER}">  |  </tspan>
  <tspan fill="{TEXT_MUTED}">CHANNELS: </tspan><tspan fill="{CYAN_ACCENT}">Telegram Relay + 10 Warm Inboxes</tspan>
  <tspan fill="{DARK_BORDER}">  |  </tspan>
  <tspan fill="{TEXT_MUTED}">STATE: </tspan><tspan fill="{EMERALD_GREEN}">Autonomous Sprints Active</tspan>
</text>
"""
    write_card("ai-mesh.svg", svg(W, h, body, "Autonomous AI Swarm Mesh Telemetry"))


# -----------------------------------------------------------------------------
# MAIN COMPILER
# -----------------------------------------------------------------------------
def main():
    print("=" * 65)
    print("🎨 RENDERING LUXURY ANIMATED SVG PROFILE CARDS")
    print("=" * 65)

    if not os.path.exists(DATA_FILE):
        print(f"[*] Missing {DATA_FILE}, running fetch_contributions.py...")
        from fetch_contributions import main as fetch_main
        fetch_main()

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Hero Card
    render_hero()

    # 2. Heatmap Card
    render_heatmap(data)

    # 3. Activity Bar Chart
    render_activity(data)

    # 4. Three Bento World Tiles (33% width each)
    render_tile("tile-growth", "GROWTH ENGINE", SAPPHIRE_LIGHT, TEXT_PRIMARY, "30-Day", "Profit Sprint",
                "High-converting direct-response DTC funnels, checkout drawers, Meta/VSL creative & retention flows.", 1.2, 0)
    render_tile("tile-sourcing", "GUANGDONG WEDGE", GOLD_ACCENT, TEXT_PRIMARY, "-45%", "Unit COGS",
                "Direct factory quotes from Guangdong on packaging, bottles & components funding the entire retainer.", 1.35, 1)
    render_tile("tile-swarms", "AI SWARMS", PURPLE_ACCENT, TEXT_PRIMARY, "24/7", "Autonomous",
                "Multi-agent AI mesh (Claude 3.5 + Grok Bot + Codex) executing research, outreach & CRM synchronization.", 1.5, 2)

    # 5. Three Showcase Project Cards (33% width each)
    render_repo("sapphire", "sapphire-brain", "Shared brain and Team OS for autonomous AI agents, lead lists and CRM pipelines.", "Python / JSON", SAPPHIRE_LIGHT, 0)
    render_repo("neuroflex", "neuroflex-dtc", "VitalMax Vitamins topical pain spray growth infrastructure, VSLs and bridge funnels.", "Next.js / Direct Response", GOLD_ACCENT, 1)
    render_repo("jinny", "jinny-telemetry", "Autonomous Telegram bot control room with 1-tap reply approvals and warm inbox relay.", "Python / Telegram API", EMERALD_GREEN, 2)

    # 6. Full-Width AI Swarm Mesh Telemetry HUD
    render_ai_mesh()

    print("\n" + "=" * 65)
    print("🎉 ALL CARDS COMPILED TO cards/ DIRECTORY SUCCESSFULLY!")
    print("=" * 65)


if __name__ == "__main__":
    main()
