#!/bin/bash
set -euo pipefail
[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0
cd "$CLAUDE_PROJECT_DIR"
# Claude reads a hook's stdout, not its stderr: send it warnings only
exec 3>&1 1>&2
warn() { echo "⚠️ $*" >&3; }

# Cloud's uv can't self-update: reinstall it at the pyproject.toml floor
uv_floor=$(sed -nE 's/^required-version *= *">= *([0-9.]+)".*/\1/p' pyproject.toml)
uv_now=$(uv --version | awk '{print $2}')
if [ -n "$uv_floor" ] && [ "$(printf '%s\n' "$uv_floor" "$uv_now" | sort -V | head -1)" != "$uv_floor" ]; then
  curl -LsSf "https://github.com/astral-sh/uv/releases/download/$uv_floor/uv-installer.sh" | UV_NO_MODIFY_PATH=1 sh \
    || warn "uv $uv_floor not installed; using $uv_now"
fi

{ uv sync && uv run pre-commit install; } || warn "uv sync or pre-commit install failed"

# Cloud doesn't install the repo's plugins
settings=.claude/settings.json
jq -r '.extraKnownMarketplaces // {} | .[].source.repo' "$settings" \
  | while read -r repo; do
    claude plugin marketplace add "$repo" --scope project || warn "marketplace not added: $repo"
  done
# Install all, so false ones are ready to enable; install writes true, so re-disable them
jq -r '.enabledPlugins // {} | to_entries[] | "\(.key) \(.value)"' "$settings" \
  | while read -r plugin enabled; do
    if ! claude plugin install "$plugin" --scope project; then
      warn "plugin not installed: $plugin"
    elif [ "$enabled" != true ]; then
      claude plugin disable "$plugin" --scope project || warn "plugin not disabled: $plugin"
    fi
  done

# The image has Chromium but not playwright-cli
command -v playwright-cli >/dev/null \
  || npm install -g @playwright/cli@latest \
  || warn "playwright-cli not installed"
