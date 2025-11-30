#!/usr/bin/env bash
set -e

echo "=============================="
echo "Publishing Newsletter Site"
echo "=============================="

# 1. Check git status
echo "🔍 Checking git status..."
git status

echo
read -p "Continue with publishing? (y/n): " confirm
if [[ "$confirm" != "y" ]]; then
  echo "Publishing canceled."
  exit 1
fi

# 2. Build MkDocs site
echo
echo "Building MkDocs site..."
mkdocs build

# 3. Deploy to GitHub Pages
echo
echo "Deploying site to GitHub Pages (gh-pages)..."
ghp-import -n -p -f site

# 4. Commit source changes
echo
read -p "Enter git commit message: " commit_msg

git add .
git commit -m "$commit_msg"

# 5. Push source repo
echo
echo "Pushing source to GitHub..."
git push

echo
echo "DONE! Your site is now live."
echo "=============================="
