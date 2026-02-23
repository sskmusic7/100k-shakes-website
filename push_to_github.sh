#!/bin/bash
# Quick script to push to GitHub

echo "🚀 100K Shakes - GitHub Push Script"
echo "===================================="
echo ""

# Check if remote exists
if git remote | grep -q origin; then
    echo "✓ GitHub remote already configured"
    git remote -v
else
    echo "⚠ No GitHub remote configured yet"
    echo ""
    echo "To set up GitHub:"
    echo "1. Create a new repository at: https://github.com/new"
    echo "2. Don't initialize with README"
    echo "3. Copy the repository URL"
    echo "4. Run: git remote add origin YOUR_REPO_URL"
    echo "5. Then run this script again"
    echo ""
    read -p "Do you have a GitHub repo URL? (y/n): " has_repo
    
    if [ "$has_repo" = "y" ]; then
        read -p "Enter your GitHub repo URL: " repo_url
        git remote add origin "$repo_url"
        echo "✓ Remote added: $repo_url"
    else
        echo "Please create a GitHub repo first, then run this script again"
        exit 1
    fi
fi

echo ""
echo "Pushing to GitHub..."
echo ""

# Set main branch
git branch -M main

# Push
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "To enable GitHub Pages (free hosting):"
    echo "1. Go to your repo on GitHub"
    echo "2. Settings → Pages"
    echo "3. Source: main branch"
    echo "4. Your site will be live at: https://YOUR_USERNAME.github.io/REPO_NAME/"
else
    echo ""
    echo "❌ Push failed. Check your GitHub credentials and try again."
fi
