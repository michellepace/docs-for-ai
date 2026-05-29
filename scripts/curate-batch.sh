#!/usr/bin/env bash
#
# Batch-curate URLs into a collection, one isolated `claude -p` run per URL.
# Each URL is processed in its own fresh Claude Code process
#
# Usage:
#   ./curate-batch.sh <collection> <file>   # urls from <file> into <collection>
#
set -uo pipefail

COLLECTION="${1:-}"
URL_FILE="${2:-}"
MODEL="claude-opus-4-8"
ALLOWED='Bash(find *),Bash(printf *),Bash(uv run scripts/curate_doc.py *),Bash(uv run scripts/update_index_descriptions.py *),Read,Write'

if [ -z "$COLLECTION" ] || [ -z "$URL_FILE" ]; then
  echo "❌ usage: $0 <collection> <file>" >&2
  exit 1
fi

if [ ! -f "$URL_FILE" ]; then
  echo "❌ url file not found: $URL_FILE" >&2
  exit 1
fi

pass=0
fail=0
results=()

i=0
while IFS= read -r url <&3 || [ -n "$url" ]; do
  url="${url#"${url%%[![:space:]]*}"}"   # ltrim
  url="${url%"${url##*[![:space:]]}"}"    # rtrim
  [ -z "$url" ] && continue
  case "$url" in \#*) continue ;; esac    # skip comment lines

  i=$((i+1))
  echo "=== [$i] curating: $url ==="

  # Run one isolated curation
  out=$(claude -p "/curate-doc $COLLECTION $url" \
    --model "$MODEL" \
    --allowedTools "$ALLOWED" \
    --permission-mode acceptEdits </dev/null 2>&1)
  code=$?
  printf '%s\n' "$out"

  # Decide PASS/FAIL
  if [ "$code" -ne 0 ] || printf '%s' "$out" | grep -q "❌ Error:"; then
    fail=$((fail+1))
    results+=("FAIL  [$i] $url  (exit=$code)")
    echo "--- ❌ FAIL [$i]: $url"
  else
    pass=$((pass+1))
    results+=("PASS  [$i] $url")
    echo "--- ✅ PASS [$i]: $url"
  fi
  echo
done 3< "$URL_FILE"

echo "======================================================"
echo "Summary: $pass passed, $fail failed, $i total"
echo "------------------------------------------------------"
for line in "${results[@]}"; do
  echo "  $line"
done
echo "======================================================"

# Non-zero overall exit if anything failed
[ "$fail" -eq 0 ]
