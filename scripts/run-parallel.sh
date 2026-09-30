#!/usr/bin/env bash
# Run each line of a file as its own `claude -p` session, several at once.
# Usage and caveats: scripts/run-parallel.sh --help
#
# Constraints:
#   1. `claude -p` reads stdin as prompt input, so it always gets </dev/null.
#   2. `claude -p` omits `--bare`: bare skips .claude/commands and bills the API.
set -uo pipefail

usage() {
  cat <<'EOF'
Run each line of a file as a prompt in its own `claude -p` session, in parallel.

Usage:
  scripts/run-parallel.sh <command-file> [jobs]
  scripts/run-parallel.sh --help

Arguments:
  <command-file>  One prompt per line, e.g. `/curate-doc uv <url>`
  [jobs]          Sessions to run at once (default 7), started 2s apart.

Prints the log directory, then `[NN] exit=N  <prompt>` as each session ends;
its output is in <log-dir>/NN.log (NN = position among non-blank lines).
exit=0 only means the session ended; read its log to see if the prompt worked.

Sessions run concurrently, so prompts that edit the same file can overwrite
each other's edits.

Example:
  scripts/run-parallel.sh commands.txt 4
EOF
}

case "${1-}" in
  -h | --help)
    usage
    exit 0
    ;;
esac

if [ $# -lt 1 ] || [ $# -gt 2 ]; then
  usage >&2
  exit 2
fi

command_file=$1
jobs=${2-7}

[ -r "$command_file" ] || {
  printf 'error: cannot read command-file: %s\n' "$command_file" >&2
  exit 2
}
command_file=$(realpath "$command_file") # resolve before the cd below

case "$jobs" in
  '' | *[!0-9]* | 0)
    printf 'error: jobs must be a positive integer: %s\n' "$jobs" >&2
    exit 2
    ;;
esac

command -v claude >/dev/null || {
  printf 'error: claude not found on PATH\n' >&2
  exit 2
}

cd "$(dirname "$0")/.." || exit 1 # start claude here so this repo's .claude/ loads

log_dir=$(mktemp -d -t run-parallel-XXXXXX)
printf '=== logs: %s\n' "$log_dir"

# xargs -d '\n' passes each "NN <prompt>" line whole (by default it splits on
# spaces and chokes on quotes); the inner sh gets it as $1 and $log_dir as $0.
# shellcheck disable=SC2016 # single-quoted on purpose: the inner sh expands it
grep -v '^[[:space:]]*$' "$command_file" \
  | nl -w2 -n rz -s' ' \
  | while IFS= read -r line; do
    printf '%s\n' "$line"
    sleep 2 # start sessions 2s apart
  done \
  | xargs -d '\n' -n1 -P "$jobs" sh -c '
      n=${1%% *}
      prompt=${1#* }
      claude -p "$prompt" </dev/null >"$0/$n.log" 2>&1
      status=$?
      printf "[%s] exit=%d  %s\n" "$n" "$status" "$prompt"
      exit "$status"
    ' "$log_dir"
status=$?

printf '\n=== DONE: logs in %s\n' "$log_dir"
[ "$status" -eq 0 ] || printf '!!! at least one session failed\n'
exit "$status"
