#!/usr/bin/env bash
# Build the HTML study-guide version of the book for GitHub Pages (Cayman theme).
# Requires: Python 3, pandoc >= 3.0
# Output lands in ../../docs/ (repo root) for GitHub Pages (main/docs).
set -euo pipefail
cd "$(dirname "$0")"

DOCS_DIR="../../docs"

echo "=== Building HTML study guide ==="

# Step 1: Pre-process LaTeX into a pandoc-friendly combined file
echo "[1/3] Pre-processing LaTeX..."
python3 build_html_preprocess.py

# Step 2: Convert to GitHub-Flavored Markdown via pandoc (Jekyll + Cayman renders it)
echo "[2/3] Running pandoc..."
pandoc .build/combined_for_html.tex \
  -f latex \
  -t gfm \
  --toc \
  --toc-depth=3 \
  --number-sections \
  --wrap=none \
  -o "${DOCS_DIR}/index.md"

# Add Jekyll front matter to the top of the file
TMPFILE=$(mktemp)
cat > "$TMPFILE" << 'EOF'
---
layout: default
title: "Short-Reach Optics for AI Compute"
---

EOF
cat "${DOCS_DIR}/index.md" >> "$TMPFILE"
mv "$TMPFILE" "${DOCS_DIR}/index.md"

# Step 3: Ensure config and nojekyll-free setup
echo "[3/3] Finalizing..."
# _config.yml should already exist; no .nojekyll needed (we want Jekyll)

echo "=== Done. Output in ${DOCS_DIR}/ ==="
echo "To deploy: commit docs/ and push to main. Enable GitHub Pages from Settings → Pages → main/docs."
