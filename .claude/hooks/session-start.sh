#!/bin/bash
# Cloud only: local sessions exit at once.
# Warnings use stdout: Claude never sees a hook's stderr.
set -euo pipefail
[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0
cd "$CLAUDE_PROJECT_DIR"

# Bring cloud's uv up to the pyproject.toml floor
uv_floor=$(sed -nE 's/^required-version *= *">= *([0-9.]+)".*/\1/p' pyproject.toml)
uv_now=$(uv --version | awk '{print $2}')
if [ -n "$uv_floor" ] && [ "$(printf '%s\n' "$uv_floor" "$uv_now" | sort -V | head -1)" != "$uv_floor" ]; then
  curl -LsSf "https://github.com/astral-sh/uv/releases/download/$uv_floor/uv-installer.sh" | UV_NO_MODIFY_PATH=1 sh \
    || echo "⚠️ uv $uv_floor not installed; using $uv_now"
fi

uv sync && uv run pre-commit install || echo "⚠️ uv sync or pre-commit install failed"

# Uses the platform's pre-installed Chromium; skill is vendored in .claude/skills
command -v playwright-cli >/dev/null \
  || npm install -g @playwright/cli@latest \
  || echo "⚠️ playwright-cli not installed"

# Add the project's marketplaces and plugins, enabled or disabled as configured
settings=.claude/settings.json
jq -r '.extraKnownMarketplaces // {} | .[].source.repo' "$settings" \
  | while read -r repo; do
    claude plugin marketplace add "$repo" --scope project || echo "⚠️ marketplace not added: $repo"
  done
jq -r '.enabledPlugins // {} | to_entries[] | "\(.key) \(.value)"' "$settings" \
  | while read -r plugin enabled; do
    if ! claude plugin install "$plugin" --scope project; then
      echo "⚠️ plugin not installed: $plugin"
    elif [ "$enabled" != true ]; then
      claude plugin disable "$plugin" --scope project || echo "⚠️ plugin not disabled: $plugin"
    fi
  done
