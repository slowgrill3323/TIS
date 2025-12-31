#!/usr/bin/env bash
set -euo pipefail

out="out.csv"
printf '"filename","title"\n' > "$out"

for f in *.html; do
  # If no .html files exist, zsh leaves the glob literal
  [[ "$f" == "*.html" ]] && break

  title="$(
    awk '
      BEGIN { IGNORECASE=1; RS="</td>"; ORS="" }
      {
        if ($0 ~ /<td[^>]*class="side"[^>]*>/ && $0 ~ /<b>[[:space:]]*Title:[[:space:]]*<\/b>/) {
          s=$0
          sub(/.*<b>[[:space:]]*Title:[[:space:]]*<\/b>/, "", s)
          gsub(/<[^>]*>/, "", s)
          gsub(/^[[:space:]]+|[[:space:]]+$/, "", s)
          print s
          exit
        }
      }
    ' "$f"
  )"

  [[ -z "$title" ]] && continue

  esc_f=${f//\"/\"\"}
  esc_t=${title//\"/\"\"}
  printf '"%s","%s"\n' "$esc_f" "$esc_t" >> "$out"
done
