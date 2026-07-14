#!/usr/bin/env bash
# Curate every URL in a file into a collection — one `claude -p` session per URL.
#
# Two non-obvious constraints, both learned the hard way:
#   1. `claude` gets </dev/null and the URL list is read on FD 3. Share stdin
#      with the loop and `claude -p` swallows the remaining URLs as piped input.
#   2. Never pass --bare. It skips discovery of .claude/commands, so the
#      /curate-doc slash command would not exist. Same reason we cd to the
#      repo root before invoking claude. NB: the headless docs say --bare
#      will become the default for -p in a future release.
set -uo pipefail

usage() {
  cat <<'EOF'
Curate a list of doc URLs into a collection, sequentially and in order.

Usage:
  scripts/curate-collection.sh <collection> <url-file>
  scripts/curate-collection.sh --help

Arguments:
  <collection>   Collection name, e.g. `uv`
  <url-file>     One source URL per line; blank lines skipped.

Runs `/curate-doc` once per URL in a fresh `claude -p` session, in file order.
A failed URL is reported and the run continues; exit status is non-zero if any
failed.

Example:
  scripts/curate-collection.sh uv uv.txt 2>&1 | tee curate-run.log
EOF
}

case "${1-}" in
  -h | --help)
    usage
    exit 0
    ;;
esac

if [ $# -ne 2 ]; then
  usage >&2
  exit 2
fi

collection=$1
url_file=$2

[ -r "$url_file" ] || {
  printf 'error: cannot read url-file: %s\n' "$url_file" >&2
  exit 2
}
url_file=$(realpath "$url_file") # resolve before the cd below

command -v claude >/dev/null || {
  printf 'error: claude not found on PATH\n' >&2
  exit 2
}

cd "$(dirname "$0")/.." || exit 1

n=0
failed=0
trap 'printf "\n!!! INTERRUPTED during [%d]\n" "$n"; exit 130' INT
while IFS= read -r url <&3 || [ -n "$url" ]; do
  [ -z "$url" ] && continue
  n=$((n + 1))
  printf '\n=== [%d] %s\n' "$n" "$url"
  claude -p "/curate-doc $collection $url" </dev/null \
    || {
      failed=$((failed + 1))
      printf '!!! FAILED [%d]: %s\n' "$n" "$url"
    }
done 3<"$url_file"

printf '\n=== DONE: %d URLs processed, %d failed\n' "$n" "$failed"
[ "$failed" -eq 0 ]
