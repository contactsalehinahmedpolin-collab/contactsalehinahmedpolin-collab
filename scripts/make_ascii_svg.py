#!/usr/bin/env python3
"""
make_ascii_svg.py
Converts source-prepped.png into a high-contrast, clean monochrome ASCII art SVG
that "types" itself in like an authentic terminal session with a moving cursor,
then holds.

Width: ~390px (Pairs side-by-side with 490px info-card.svg to equal 880px total width).
Output: polin-ascii.svg
"""
import html
import os
import sys
from PIL import Image, ImageEnhance, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "source-prepped.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "polin-ascii.svg")

# Grid configuration: exactly 370px wide x 430px tall to sit side-by-side with 490x430 info card
COLS = int(os.environ.get("COLS", 64))
ROWS = int(os.environ.get("ROWS", 36))
CANVAS_W = 370
CANVAS_H = 430
PAD = 16
TITLEBAR_H = 34
STATUS_H = 36

ART_W = CANVAS_W - PAD * 2
ART_TOP = TITLEBAR_H + 8
STATUS_LINE_Y = CANVAS_H - STATUS_H
STATUS_Y = STATUS_LINE_Y + 22

ART_H = STATUS_LINE_Y - ART_TOP - 6
CELL_W = ART_W / COLS
CELL_H = ART_H / ROWS
RAMP = " .:-=+*#%@"  # Bright (sparse) -> Dark (dense)

CONTRAST = 1.22
BRIGHTNESS = 1.05
GAMMA = 1.08
WHITE_FLOOR = 0.88  # Luminance above this maps to space (clears background)

BG = "#0d1117"
BG2 = "#111827"
FRAME = "#30363d"
TITLE_TEXT = "#7d8590"
INK = "#e6edf3"
CURSOR = "#38bdf8"
ACCENT = "#58a6ff"

# Animation timing
ROW_DUR = 4.2 / ROWS
STAGGER = ROW_DUR


def generate_ascii_rows():
    if not os.path.exists(SRC):
        print(f"[!] Warning: {SRC} not found. Generating cyber avatar matrix...", file=sys.stderr)
        return None

    im = Image.open(SRC).convert("L")
    im = ImageEnhance.Brightness(im).enhance(BRIGHTNESS)
    im = ImageEnhance.Contrast(im).enhance(CONTRAST)
    im = im.resize((COLS, ROWS), Image.LANCZOS)
    px = im.load()

    rows_txt = []
    for y in range(ROWS):
        chars = []
        for x in range(COLS):
            lum = px[x, y] / 255.0
            lum = pow(lum, GAMMA)
            if lum >= WHITE_FLOOR:
                chars.append(" ")
                continue
            idx = int((1.0 - lum) * (len(RAMP) - 1) + 0.5)
            idx = max(0, min(len(RAMP) - 1, idx))
            chars.append(RAMP[idx])
        rows_txt.append("".join(chars))
    return rows_txt


def main():
    rows_txt = generate_ascii_rows()
    if not rows_txt:
        print("[!] Generating placeholder rows", file=sys.stderr)
        rows_txt = ["#" * COLS for _ in range(ROWS)]

    art_top = ART_TOP

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
        f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">',
        '<defs>',
        f'<linearGradient id="termBg" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0%" stop-color="{BG2}"/>',
        f'<stop offset="100%" stop-color="{BG}"/>',
        '</linearGradient>',
        '</defs>',
        f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="10" fill="url(#termBg)"/>',
        f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="10" fill="none" stroke="{FRAME}" stroke-width="1"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}" stroke-width="1"/>',
    ]

    # macOS window controls
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

    parts.append(
        f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" '
        f'text-anchor="middle">polin@sapphire: ~$ ./portrait.sh</text>'
    )

    # ASCII text rows with typing clip-path wipe animation
    font_size = CELL_H * 0.92
    for ry, line in enumerate(rows_txt):
        y = art_top + ry * CELL_H + CELL_H * 0.76
        row_y = art_top + ry * CELL_H
        delay = ry * STAGGER
        safe = html.escape(line)
        text = (
            f'<text xml:space="preserve" x="{PAD}" y="{y:.1f}" fill="{INK}" '
            f'font-size="{font_size:.1f}" textLength="{ART_W}" lengthAdjust="spacing">{safe}</text>'
        )

        parts.append(
            f'<clipPath id="row_{ry}">'
            f'<rect x="{PAD}" y="{row_y:.1f}" height="{CELL_H:.1f}" width="0">'
            f'<animate attributeName="width" from="0" to="{ART_W}" begin="{delay:.3f}s" '
            f'dur="{ROW_DUR:.2f}s" fill="freeze"/>'
            f'</rect>'
            f'</clipPath>'
        )
        parts.append(f'<g clip-path="url(#row_{ry})">{text}</g>')
        
        # Cursor traveling across the row
        parts.append(
            f'<rect y="{row_y:.1f}" width="{CELL_W*1.5:.1f}" height="{CELL_H-1:.1f}" fill="{CURSOR}" opacity="0">'
            f'<animate attributeName="x" from="{PAD}" to="{PAD+ART_W}" begin="{delay:.3f}s" '
            f'dur="{ROW_DUR:.2f}s" fill="freeze"/>'
            f'<set attributeName="opacity" to="0.85" begin="{delay:.3f}s"/>'
            f'<set attributeName="opacity" to="0" begin="{delay+ROW_DUR:.3f}s"/>'
            f'</rect>'
        )

    # Bottom status bar with persistent blinking cursor
    parts.append(f'<line x1="0" y1="{STATUS_LINE_Y:.1f}" x2="{CANVAS_W}" y2="{STATUS_LINE_Y:.1f}" stroke="{FRAME}"/>')
    
    status_prompt = 'polin@sapphire:~$ whoami <tspan fill="' + ACCENT + '" font-weight="600">Salehin Ahmed Polin</tspan>'
    parts.append(f'<text x="{PAD}" y="{STATUS_Y:.1f}" fill="{TITLE_TEXT}" font-size="11">{status_prompt}</text>')

    cursor_x = PAD + 258
    parts.append(
        f'<rect x="{cursor_x:.1f}" y="{STATUS_Y-11:.1f}" width="7" height="13" fill="{CURSOR}">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/>'
        f'</rect>'
    )

    parts.append("</svg>")
    svg = "".join(parts)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[✓] Rendered ASCII portrait SVG ({CANVAS_W}x{CANVAS_H}) -> {OUT}")


if __name__ == "__main__":
    main()
