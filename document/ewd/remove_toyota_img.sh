#!/usr/bin/env bash
set -euo pipefail

mode="${1:-}"
if [[ "$mode" != "--dry-run" && "$mode" != "--apply" ]]; then
  echo "Usage: $0 --dry-run | --apply" >&2
  exit 2
fi

# Regex removes from the opening <img src="...fig-pos/" through wmode="transparent">
# across any number of characters/lines (non-greedy).
perl_expr='
  s{
    <img\s+src="https://techinfo\.toyota\.com/t3Portal/external/en/ewdappu/EM43B0U/ewd/contents/routing/fig-pos/"
    .*?
    wmode="transparent">\s*
  }{}gsx;
'

shopt -s nullglob
files=( *.html )

if (( ${#files[@]} == 0 )); then
  echo "No .html files found in the current directory."
  exit 0
fi

for f in "${files[@]}"; do
  grep -q 'ewd/contents/routing/fig-pos/' "$f" || continue

  tmp="$(mktemp)"
  perl -0777 -pe "$perl_expr" "$f" > "$tmp"

  if cmp -s -- "$f" "$tmp"; then
    rm -f -- "$tmp"
    continue
  fi

  if [[ "$mode" == "--dry-run" ]]; then
    echo "==== $f ===="
    diff -u --label "$f (original)" "$f" --label "$f (preview)" "$tmp" || true
    rm -f -- "$tmp"
    continue
  fi

  bak="${f}.bak"
  if [[ -e "$bak" ]]; then
    echo "SKIP: backup already exists: $bak"
    rm -f -- "$tmp"
    continue
  fi

  cp -p -- "$f" "$bak"
  mv -- "$tmp" "$f"
  echo "UPDATED: $f (backup: $bak)"
done
