#!/bin/bash
set -e

COPIED_URL="https://github.com/evilmartians/lefthook/tree/master/docs/mdbook"

COLLECTION_DIR="collections/lefthook"
DOWNLOAD_TEMP="collections/lefthook/download_temp"
CLONE_URL="https://github.com/evilmartians/lefthook.git"
DOCS_PATH="docs/mdbook"
BRANCH="master"

mkdir -p collections/lefthook/download_temp && cd collections/lefthook/download_temp
git init
git remote add origin https://github.com/evilmartians/lefthook.git
git config core.sparseCheckout true
echo "docs/mdbook/*" > .git/info/sparse-checkout
git pull origin master --depth=1
rsync -av --include='*/' --include='*.mdx' --include='*.md' --exclude='*' \
    docs/mdbook/ ../../../collections/lefthook/
cd ../../..
rm -rf collections/lefthook/download_temp
npx markdownlint-cli2 --fix "collections/lefthook/**/*.md"