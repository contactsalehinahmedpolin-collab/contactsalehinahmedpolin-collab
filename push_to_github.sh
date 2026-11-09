#!/usr/bin/env bash
set -e

REPO_NAME="contactsalehinahmedpolin-collab"
REMOTE_URL="https://github.com/${REPO_NAME}/${REPO_NAME}.git"

echo "============================================================"
echo "⚡ SAPPHIRE PROFILE ENGINE · GITHUB DEPLOYMENT RELAY"
echo "============================================================"
echo "Target Repo: https://github.com/${REPO_NAME}/${REPO_NAME}"
echo ""

# Ensure git remote is set
git remote remove origin 2>/dev/null || true
git remote add origin "$REMOTE_URL"

echo "[1/3] Compiling animated terminal SVG suite..."
"/Users/salehinahmed/Downloads/JINNY SL/.venv/bin/python3" scripts/build_all.py

echo ""
echo "[2/3] Staging and committing changes..."
git add .
git commit -m "feat(art): compile animated terminal suite (monochrome ASCII portrait, neofetch card, heatmap & swarm HUD)" 2>/dev/null || echo "Working tree clean, proceeding..."

echo ""
echo "[3/3] Pushing to GitHub (main branch)..."
git push -u origin main

echo ""
echo "🎉 DEPLOYMENT COMPLETE! View your animated profile at:"
echo "   👉 https://github.com/${REPO_NAME}"
echo "============================================================"
