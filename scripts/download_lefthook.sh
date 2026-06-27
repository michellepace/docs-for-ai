#!/bin/bash
set -e

# Source: https://github.com/evilmartians/lefthook/tree/master/docs/mdbook

COLLECTION_DIR="collections/lefthook"
DOWNLOAD_TEMP="$COLLECTION_DIR/download_temp"
CLONE_URL="https://github.com/evilmartians/lefthook.git"
DOCS_PATH="docs/mdbook"
BRANCH="master"

mkdir -p "$DOWNLOAD_TEMP" && cd "$DOWNLOAD_TEMP"
git init
git remote add origin "$CLONE_URL"
git config core.sparseCheckout true
echo "$DOCS_PATH/*" >.git/info/sparse-checkout
git pull origin "$BRANCH" --depth=1
rsync -av --include='*/' --include='*.mdx' --include='*.md' --exclude='*' \
  "$DOCS_PATH/" "../../../$COLLECTION_DIR/"
cd ../../..
rm -rf "$DOWNLOAD_TEMP"
npx markdownlint-cli2 --fix "$COLLECTION_DIR/**/*.md"
