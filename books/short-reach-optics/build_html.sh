#!/usr/bin/env bash
# Build the HTML study-guide version of the book for GitHub Pages (Cayman theme).
# Requires: Python 3, pandoc >= 3.0
# Output lands in ../../docs/ (repo root) for GitHub Pages (main/docs).
set -euo pipefail
cd "$(dirname "$0")"

DOCS_DIR="../../docs"

echo "=== Building HTML study guide ==="

# Step 1: Pre-process LaTeX into a pandoc-friendly combined file
echo "[1/4] Pre-processing LaTeX..."
python3 build_html_preprocess.py

# Step 2: Split the combined .tex into per-chapter files and convert each
echo "[2/4] Splitting into chapters and converting..."
python3 -c "
import re, subprocess, os

DOCS = '${DOCS_DIR}'
TEX = '.build/combined_for_html.tex'

with open(TEX) as f:
    content = f.read()

# Extract preamble and body
begin = content.find(r'\begin{document}')
end = content.find(r'\end{document}')
preamble = content[:begin]
body = content[begin+len(r'\begin{document}'):end]

# Split body by \chapter or \chapter*
# Each chunk starts with \chapter... 
chunks = re.split(r'(?=\\\\chapter(?:\*?)\\{)', body)

# First chunk is anything before the first chapter (copyright, preface etc)
# Chapters are the rest
chapters = []
front_matter = chunks[0] if chunks else ''

for i, chunk in enumerate(chunks):
    # Find the chapter title
    m = re.match(r'\\\\chapter\*?\\{([^}]+)\\}', chunk)
    if m:
        title = m.group(1)
        chapters.append((title, chunk))
    elif i == 0 and chunk.strip():
        # front matter before first chapter
        chapters.insert(0, ('Preface', chunk))

print(f'  Found {len(chapters)} chapters')
"

# Actually, let's use a simpler approach: pandoc with --split-level won't work for GFM.
# Instead, split the Markdown output by H1 headings.

echo "[2/4] Converting full document to Markdown..."
pandoc .build/combined_for_html.tex \
  -f latex \
  -t markdown-raw_html \
  --toc \
  --toc-depth=2 \
  --number-sections \
  --wrap=none \
  --markdown-headings=atx \
  -o .build/full_book.md 2>/dev/null || true

echo "[3/4] Splitting into per-chapter pages..."
python3 build_html_split.py "${DOCS_DIR}"

echo "[4/4] Done."
echo "=== Output in ${DOCS_DIR}/ ==="
echo "To deploy: commit and push. Enable GitHub Pages from Settings → Pages → main/docs."
