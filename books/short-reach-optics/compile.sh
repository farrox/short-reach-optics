#!/usr/bin/env bash
# XeLaTeX (required: tufte-latex, fontspec, Alegreya Sans TTFs in ./fonts/).
# Builds into .build/ and atomically replaces main.pdf only when finished, so the
# PDF viewer never reads a half-written file.
set -euo pipefail
cd "$(dirname "$0")"

BUILD=".build"
LOCK="$BUILD/compile.lock"
mkdir -p "$BUILD"

# Portable lock (macOS has no flock in PATH).
if ! mkdir "$LOCK" 2>/dev/null; then
  echo "==> compile already running, skipping"
  exit 0
fi
trap 'rmdir "$LOCK" 2>/dev/null || true' EXIT

run_xelatex() {
  # XeLaTeX often exits non-zero when the log only has warnings (undefined
  # refs on early passes). Keep going so passes 2--3 can resolve them.
  xelatex -interaction=nonstopmode -synctex=1 -output-directory="$BUILD" main.tex \
    || true
}

run_xelatex
run_xelatex
run_xelatex

# Atomic replace: viewer always sees a complete PDF.
mv -f "$BUILD/main.pdf" main.pdf.tmp
mv -f main.pdf.tmp main.pdf
if [[ -f "$BUILD/main.synctex.gz" ]]; then
  mv -f "$BUILD/main.synctex.gz" main.synctex.gz
fi

echo "==> $(pwd)/main.pdf"

if [[ -n "${CHECK_OVERFULL:-}" ]]; then
  ./check_overfull.sh "$BUILD/main.log"
fi
