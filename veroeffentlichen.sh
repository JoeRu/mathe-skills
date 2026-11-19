#!/usr/bin/env sh
# Veröffentlicht den Ordner mathe-skills/ aus dem privaten Repository ins öffentliche
# Repository (Remote "public"): ein Commit je Lauf, aufgesetzt auf public/main.
# Aufruf im Wurzelordner des privaten Repos:  sh mathe-skills/veroeffentlichen.sh
set -eu
cd "$(git rev-parse --show-toplevel)"
python3 mathe-skills/build.py --nur-pruefen
git fetch -q public main
VERSION=$(python3 -c "import json;print(json.load(open('mathe-skills/.claude-plugin/plugin.json'))['version'])")
TREE=$(git rev-parse "HEAD:mathe-skills")
if [ "$TREE" = "$(git rev-parse public/main^{tree})" ]; then
  echo "public/main ist bereits auf diesem Stand ($VERSION)."; exit 0
fi
COMMIT=$(git commit-tree "$TREE" -p public/main -m "mathe-skills $VERSION

Stand aus dem privaten Repository, Commit $(git rev-parse --short HEAD).")
git push public "$COMMIT:refs/heads/main"
echo "veröffentlicht: mathe-skills $VERSION -> public/main ($(echo "$COMMIT" | cut -c1-7))"
