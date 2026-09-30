#!/usr/bin/env bash
# Curate every URL in a file into a collection — one `claude -p` session per URL.
#
# Constraints:
#   1. `claude -p` reads stdin as prompt input, so it gets </dev/null and the
#      loop reads URLs on FD 3 — two guards against it eating the URL list.
#   2. `claude -p` omits `--bare`: bare skips .claude/commands and bills the API.
set -uo pipefail

usage() {
  cat <<'EOF'
Run `/curate-doc <collection> <url>` per URL in a file, one at a time.

Usage:
  scripts/curate-collection.sh <collection> <url-file>
  scripts/curate-collection.sh --help

Arguments:
  <collection>  Existing or new, e.g. uv.
  <url-file>    One URL per line; blank lines skipped.

Each URL runs in a fresh `claude -p` session, in file order; output streams to
stdout. A failed URL is reported and the run continues; exit status is non-zero
if any failed.

Example:
  scripts/curate-collection.sh uv urls.txt 2>&1 | tee curate-run.log
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

cd "$(dirname "$0")/.." || exit 1 # start claude here so this repo's .claude/ loads

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
