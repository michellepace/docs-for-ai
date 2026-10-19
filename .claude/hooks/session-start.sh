#!/bin/bash
# Cloud ignores enabledPlugins: install all; true/false still applies.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR"
settings=.claude/settings.json

uv sync
uv run pre-commit install

jq -r '.extraKnownMarketplaces[].source.repo' "$settings" \
  | while read -r repo; do
    claude plugin marketplace add "$repo" || echo "⚠️ marketplace not added: $repo" >&2
  done

jq -r '.enabledPlugins | keys[]' "$settings" \
  | while read -r plugin; do
    claude plugin install "$plugin" || echo "⚠️ plugin not installed: $plugin" >&2
  done
