#!/bin/bash
# ------------------------------------------
# git-clean-rebase.sh
# Safely sync local main branch with origin/main
# Handles rename/delete conflicts automatically.
# ------------------------------------------

set -e

echo "🔍 Checking branch..."
branch=$(git rev-parse --abbrev-ref HEAD)
if [ "$branch" != "main" ]; then
  echo "⚠️  You are on branch '$branch'. This script is for 'main'."
  read -p "Continue anyway? (y/n): " yn
  [ "$yn" != "y" ] && exit 0
fi

echo "🧹 Stashing local uncommitted changes (if any)..."
git stash push -m "pre-rebase-$(date +%s)" || true

echo "📥 Fetching latest remote changes..."
git fetch origin main

echo "🔄 Rebasing local changes on top of origin/main..."
git rebase origin/main || {
  echo "⚠️  Conflict detected — resolving automatically if possible..."
  # keep local tasks.yml, delete outdated ones if exist
  [ -f tasks.yml ] && git add tasks.yml || true
  [ -f .github/workflows/tasks.yml ] && git rm .github/workflows/tasks.yml || true
  git rebase --continue || {
    echo "❌ Manual resolution required. Run 'git status' to see conflicts."
    exit 1
  }
}

echo "🚀 Pushing updates to remote..."
git push --force-with-lease origin main

echo "✅ Rebase complete and pushed successfully!"
echo "📦 If you stashed changes, run 'git stash pop' to restore them."

