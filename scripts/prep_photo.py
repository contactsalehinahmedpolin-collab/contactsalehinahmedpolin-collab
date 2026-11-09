#!/usr/bin/env python3
"""
prep_photo.py
Prepares an input photo for clean monochrome ASCII conversion:
1. Removes background with rembg so subject is completely isolated
2. Bilateral filtering to smooth skin/paper texture while keeping edge lines sharp
3. Contrast-Limited Adaptive Equalization & tone stretching (subject only)
4. Difference-of-Gaussians edge enhancement for facial features & eyes
5. Composites onto pure white (luminance > threshold washes out to space glyphs)

Output: source-prepped.png -> consumed by make_ascii_svg.py.
Usage:
    python scripts/prep_photo.py [input_photo.jpg] [output.png]
"""
import os
import sys

try:
    import cv2
    import numpy as np
    from PIL import Image
    from rembg import remove
except ImportError as e:
    print(f"[!] Error: Missing required package: {e}", file=sys.stderr)
    print("    Run: pip install pillow numpy opencv-python-headless rembg", file=sys.stderr)
    sys.exit(1)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "source-photo.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "source-prepped.png")

LINE_WEIGHT = 0.65


def prep(image_path, out_path):
    print(f"[*] Isolating subject and prepping tones from {image_path}...")
    img = Image.open(image_path).convert("RGBA")
    cut = remove(img)
    rgb = np.array(cut.convert("RGB"))
    alpha = np.array(cut.split()[-1])
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

    # Smooth texture while preserving crisp contours
    smooth = gray
    for _ in range(3):
        smooth = cv2.bilateralFilter(smooth, 9, 45, 9)

    # Tone stretch subject only
    subj_mask = alpha > 120
    if np.any(subj_mask):
        lo, hi = np.percentile(smooth[subj_mask], [3, 92])
        tone = np.clip((smooth.astype(np.float32) - lo) / max(1e-4, (hi - lo)), 0, 1)
    else:
        tone = smooth.astype(np.float32) / 255.0

    # Feature line enhancement via Difference-of-Gaussians
    fine = cv2.GaussianBlur(smooth, (0, 0), 1.5).astype(np.float32)
    coarse = cv2.GaussianBlur(smooth, (0, 0), 6.0).astype(np.float32)
    lines = np.clip((coarse - fine) / 38.0, 0, 1)
    out = np.clip(tone - LINE_WEIGHT * lines, 0, 1) * 255.0

    # Composite onto pure white background
    mask = cv2.GaussianBlur(alpha.astype(np.float32) / 255.0, (0, 0), 1.0)
    out = out * mask + 255.0 * (1.0 - mask)

    # Center crop / pad to square
    ys, xs = np.where(alpha > 20)
    if len(xs) > 0 and len(ys) > 0:
        side = max(xs.max() - xs.min(), ys.max() - ys.min()) + 60
        cx, cy = (xs.min() + xs.max()) // 2, (ys.min() + ys.max()) // 2
        canvas = np.full((side, side), 255, np.uint8)
        x0, y0 = cx - side // 2, cy - side // 2
        sx0, sy0 = max(x0, 0), max(y0, 0)
        sx1, sy1 = min(x0 + side, out.shape[1]), min(y0 + side, out.shape[0])
        canvas[sy0 - y0:sy1 - y0, sx0 - x0:sx1 - x0] = out[sy0:sy1, sx0:sx1].astype(np.uint8)
    else:
        canvas = out.astype(np.uint8)

    Image.fromarray(canvas, mode="L").save(out_path)
    print(f"[✓] Saved contrast-enhanced prepped image to {out_path} ({canvas.shape[1]}x{canvas.shape[0]})")


if __name__ == "__main__":
    if not os.path.exists(INP):
        print(f"[!] Error: Input image {INP} does not exist.", file=sys.stderr)
        sys.exit(1)
    prep(INP, OUT)
