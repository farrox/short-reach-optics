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
  xelatex -interaction=nonstopmode -synctex=1 -output-directory="$BUILD" main.tex
}

# Passes 1--2 may exit non-zero on unresolved cross-refs; keep going.
run_xelatex || true
run_xelatex || true
# Final pass is strict: do not swallow the exit code.
run_xelatex

# Atomic replace: viewer always sees a complete PDF.
if [[ ! -f "$BUILD/main.pdf" ]]; then
  echo "compile.sh: FAIL missing $BUILD/main.pdf" >&2
  exit 1
fi
mv -f "$BUILD/main.pdf" main.pdf.tmp
mv -f main.pdf.tmp main.pdf
if [[ -f "$BUILD/main.synctex.gz" ]]; then
  mv -f "$BUILD/main.synctex.gz" main.synctex.gz
fi
cp -f "$BUILD/main.log" main.log

LOG="$BUILD/main.log"
fail=0
if grep -q 'LaTeX Error' "$LOG"; then
  echo "compile.sh: FAIL LaTeX Error in $LOG" >&2
  fail=1
fi
if grep -Eqi 'Fatal error|Emergency stop|Undefined control sequence' "$LOG"; then
  echo "compile.sh: FAIL fatal / undefined control sequence in $LOG" >&2
  fail=1
fi
if grep -Eq 'undefined references|multiply-defined' "$LOG"; then
  echo "compile.sh: FAIL undefined or multiply-defined references in $LOG" >&2
  fail=1
fi
if [[ ! -f main.pdf ]]; then
  echo "compile.sh: FAIL missing main.pdf" >&2
  fail=1
fi
if [[ "$fail" -ne 0 ]]; then
  exit 1
fi

echo "==> $(pwd)/main.pdf"

if [[ -n "${CHECK_OVERFULL:-}" ]]; then
  ./check_overfull.sh "$BUILD/main.log"
fi
