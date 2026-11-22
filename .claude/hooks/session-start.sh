#!/bin/bash
# Cloud ignores enabledPlugins: install all; true/false still applies.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR"
settings=.claude/settings.json

# Platform uv can't self-update: reinstall at the pyproject.toml floor if below it
uv_floor=$(sed -nE 's/^required-version *= *">= *([0-9.]+)".*/\1/p' pyproject.toml)
uv_now=$(uv --version | awk '{print $2}')
if [ -n "$uv_floor" ] && [ "$(printf '%s\n' "$uv_floor" "$uv_now" | sort -V | head -1)" != "$uv_floor" ]; then
  curl -LsSf "https://astral.sh/uv/$uv_floor/install.sh" | UV_NO_MODIFY_PATH=1 sh \
    || echo "⚠️ uv $uv_floor not installed; using $uv_now" >&2
fi

uv sync
uv run pre-commit install

# Uses the platform's pre-installed Chromium; skill is vendored in .claude/skills
command -v playwright-cli >/dev/null \
  || npm install -g @playwright/cli@latest \
  || echo "⚠️ playwright-cli not installed" >&2

jq -r '.extraKnownMarketplaces[].source.repo' "$settings" \
  | while read -r repo; do
    claude plugin marketplace add "$repo" || echo "⚠️ marketplace not added: $repo" >&2
  done

jq -r '.enabledPlugins | keys[]' "$settings" \
  | while read -r plugin; do
    claude plugin install "$plugin" || echo "⚠️ plugin not installed: $plugin" >&2
  done
