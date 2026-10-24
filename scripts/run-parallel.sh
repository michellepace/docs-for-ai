#!/usr/bin/env bash
# Run each line of a file as its own `claude -p` session, several at once.
# Usage and caveats: scripts/run-parallel.sh --help
#
# Constraints:
#   1. `claude -p` reads stdin as prompt input, so it always gets </dev/null.
#   2. `claude -p` omits `--bare`: bare skips .claude/skills and bills the API.
set -uo pipefail

usage() {
  cat <<'EOF'
Run each line of a file as its own `claude -p` session, in parallel.

Usage: scripts/run-parallel.sh --effort <level> <prompt-file> [jobs]

  --effort <level>  low|medium|high|xhigh|max (all sessions)
  <prompt-file>     One prompt per line, blank lines skipped. Runs from the
                    repo root, so skills work: `/curate-doc uv <url>`
  [jobs]            Max concurrent sessions (default 7)

Output: `=== logs: <dir>`, then `[NN] exit=N  <prompt>` as each session
ends. NN numbers the non-blank lines; the full transcript is <dir>/NN.log.
exit=0 only means the session ended: check its log for the result.
Exits non-zero if any session failed.

Starts are staggered 2s so sessions editing the same file rarely clash.
If an edit is lost, rerun that prompt.

Example: scripts/run-parallel.sh --effort high prompts.txt 4
EOF
}

case "${1-}" in
  -h | --help)
    usage
    exit 0
    ;;
esac

if [ "${1-}" != --effort ] || [ $# -lt 3 ] || [ $# -gt 4 ]; then
  usage >&2
  exit 2
fi

effort=$2
prompt_file=$3
jobs=${4-7}

# claude only warns on an unknown level and runs at the default, so check here
case "$effort" in
  low | medium | high | xhigh | max) ;;
  *)
    printf 'error: effort must be one of low|medium|high|xhigh|max: %s\n' "$effort" >&2
    exit 2
    ;;
esac

[ -r "$prompt_file" ] || {
  printf 'error: cannot read prompt-file: %s\n' "$prompt_file" >&2
  exit 2
}
prompt_file=$(realpath "$prompt_file") # resolve before the cd below

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
printf '=== logs: %s  (effort: %s)\n' "$log_dir" "$effort"

# xargs -d '\n' passes each "NN <prompt>" line whole (by default it splits on
# spaces and chokes on quotes); the inner sh gets $log_dir as $0, $effort as
# $1, and that line as $2.
# shellcheck disable=SC2016 # single-quoted on purpose: the inner sh expands it
grep -v '^[[:space:]]*$' "$prompt_file" \
  | nl -w2 -n rz -s' ' \
  | while IFS= read -r line; do
    printf '%s\n' "$line"
    sleep 2 # start sessions 2s apart
  done \
  | xargs -d '\n' -n1 -P "$jobs" sh -c '
      n=${2%% *}
      prompt=${2#* }
      claude -p --effort "$1" "$prompt" </dev/null >"$0/$n.log" 2>&1
      status=$?
      printf "[%s] exit=%d  %s\n" "$n" "$status" "$prompt"
      exit "$status"
    ' "$log_dir" "$effort"
status=$?

printf '\n=== DONE: logs in %s\n' "$log_dir"
[ "$status" -eq 0 ] || printf '!!! at least one session failed\n'
exit "$status"
