#!/usr/bin/env python3
"""
build_all.py
One-command builder for the complete animated GitHub profile suite:
1. Fetches contribution statistics
2. Renders 53-week animated contribution heatmap SVG
3. Renders animated self-typing monochrome ASCII portrait SVG
4. Renders animated Neofetch system specifications card SVG
5. Renders animated Multi-Agent Swarm Telemetry HUD SVG
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PYTHON = sys.executable

SCRIPTS = [
    ("fetch_contributions.py", "Fetching GitHub contribution data"),
    ("render_heatmap_svg.py", "Generating animated contribution heatmap SVG"),
    ("make_ascii_svg.py", "Generating self-typing ASCII portrait SVG"),
    ("make_info_card.py", "Generating Neofetch system card SVG"),
    ("make_mesh_card.py", "Generating AI Swarm Telemetry HUD SVG"),
    ("make_systems_card.py", "Generating Systems Built & Production Card SVG"),
]


def run_pipeline():
    print("=" * 65)
    print("⚡ SAPPHIRE PROFILE ENGINE · FULL ART SUITE COMPILER")
    print("=" * 65)

    for script_name, desc in SCRIPTS:
        script_path = os.path.join(HERE, script_name)
        print(f"\n[+] {desc} ({script_name})...")
        res = subprocess.run([PYTHON, script_path], capture_output=True, text=True)
        if res.stdout:
            print(res.stdout.strip())
        if res.returncode != 0:
            print(f"[!] FAILED: {script_name}", file=sys.stderr)
            if res.stderr:
                print(res.stderr.strip(), file=sys.stderr)
            sys.exit(res.returncode)

    print("\n" + "=" * 65)
    print("🎉 ALL PROFILE ASSETS COMPILED SUCCESSFULLY!")
    print("=" * 65)

    root_dir = os.path.join(HERE, "..")
    svgs = [f for f in os.listdir(root_dir) if f.endswith(".svg")]
    for s in sorted(svgs):
        sp = os.path.join(root_dir, s)
        sz = os.path.getsize(sp)
        print(f"  • {s.ljust(24)} -> {sz / 1024:.1f} KB")


if __name__ == "__main__":
    run_pipeline()
