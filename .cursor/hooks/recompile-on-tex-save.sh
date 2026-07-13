#!/usr/bin/env bash
# Cursor hook: recompile LaTeX after .tex edits (agent or Tab).
# Manual saves are handled by LaTeX Workshop onSave in book/.vscode/settings.json.
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
LOG="$ROOT/.cursor/hooks/tex-compile.log"
STAMP="$ROOT/.cursor/hooks/.tex-compile.stamp"
DEBOUNCE_SEC=2

input=$(cat)
file_path=$(printf '%s' "$input" | python3 -c 'import json,sys
try:
    print(json.load(sys.stdin).get("file_path",""))
except Exception:
    print("")')

[[ -n "$file_path" && "$file_path" == *.tex ]] || exit 0

if [[ "$file_path" != /* ]]; then
  file_path="$ROOT/$file_path"
fi

compile_script=""
if [[ "$file_path" == *"/books/short-reach-optics/"* ]]; then
  compile_script="$ROOT/books/short-reach-optics/compile.sh"
elif [[ "$file_path" == *"/parts/"* ]] || [[ "$(basename "$file_path")" == main*.tex ]]; then
  compile_script="$ROOT/compile.sh"
fi

[[ -n "$compile_script" && -x "$compile_script" ]] || exit 0

token=$(python3 -c 'import os,random,time; print(f"{os.getpid()}-{random.randrange(1_000_000)}-{time.time_ns()}")')
printf '%s' "$token" >"$STAMP"

(
  sleep "$DEBOUNCE_SEC"
  if [[ "$(cat "$STAMP" 2>/dev/null)" != "$token" ]]; then
    exit 0
  fi

  {
    echo "==> $(date -Iseconds) compile after ${file_path#$ROOT/}"
    (cd "$(dirname "$compile_script")" && ./"$(basename "$compile_script")")
    echo "==> $(date -Iseconds) done"
  } >>"$LOG" 2>&1
) &

exit 0
