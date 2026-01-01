#!/usr/bin/env bash
set -euo pipefail

OUT="../URLs.csv"

find . -type f \( -iname '*.html' -o -iname '*.htm' -o -iname '*.css' \) -print0 |
while IFS= read -r -d '' f; do
  abs="$(cd "$(dirname "$f")" && pwd -P)/$(basename "$f")"

  grep -IohE \
    'https?://[^[:space:]"'"'"'<>]+|((\./|\../|/)?[A-Za-z0-9._-]+(/[A-Za-z0-9._-]+)+)(\?[^[:space:]"'"'"'<>]+)?(#[^[:space:]"'"'"'<>]+)?' \
    "$f" 2>/dev/null |
  awk -v file="$abs" '{
    url=$0
    gsub(/"/, "\"\"", url)
    f=file
    gsub(/"/, "\"\"", f)
    printf "\"%s\",\"%s\"\n", url, f
  }'
done | sort -u > "$OUT"
