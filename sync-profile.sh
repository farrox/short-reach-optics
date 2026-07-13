#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
PROFILE_REPO="${PROFILE_REPO:-$HOME/Developer/farrox}"
SOURCE="$ROOT/PROFILE_README.md"

if [[ ! -f "$SOURCE" ]]; then
  echo "Missing $SOURCE" >&2
  exit 1
fi

if [[ ! -d "$PROFILE_REPO/.git" ]]; then
  git clone git@github.com:farrox/farrox.git "$PROFILE_REPO"
fi

# Skip the setup comment on line 1; write the rest to README.md
tail -n +2 "$SOURCE" > "$PROFILE_REPO/README.md"

cd "$PROFILE_REPO"
if git diff --quiet README.md; then
  echo "Profile README already up to date."
  exit 0
fi

git add README.md
git commit -m "Sync profile README from short-reach-optics source."
git push origin main
echo "Pushed profile README to github.com/farrox/farrox"
