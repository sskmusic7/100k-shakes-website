# GitHub Setup Guide

## ✅ Current Status

Your project is now initialized as a Git repository, but **not yet pushed to GitHub**.

## 🚀 Deploy to GitHub

### Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **"+"** icon → **"New repository"**
3. Name it: `100k-shakes-website` (or your preferred name)
4. Choose **Public** or **Private**
5. **Don't** initialize with README (we already have files)
6. Click **"Create repository"**

### Step 2: Connect Local Repository to GitHub

After creating the repo, GitHub will show you commands. Use these:

```bash
# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/100k-shakes-website.git

# Or if you prefer SSH:
git remote add origin git@github.com:YOUR_USERNAME/100k-shakes-website.git
```

### Step 3: Commit and Push

```bash
# Stage all files
git add .

# Create initial commit
git commit -m "Initial commit: 100K Shakes website"

# Push to GitHub
git branch -M main
git push -u origin main
```

## 🌐 GitHub Pages Deployment (Free Hosting!)

GitHub Pages can host your static website for free!

### Option A: Automatic Deployment

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under **Source**, select **"Deploy from a branch"**
4. Choose branch: **main**
5. Choose folder: **/ (root)**
6. Click **Save**

Your site will be live at: `https://YOUR_USERNAME.github.io/100k-shakes-website/`

### Option B: Use GitHub Actions (Advanced)

Create `.github/workflows/deploy.yml` for automatic deployments.

## 📝 What's Included in Git

✅ All HTML/CSS/JavaScript files
✅ Configuration files (package.json, etc.)
✅ Documentation
✅ Image generation scripts
✅ Menu items JSON

❌ **Excluded** (via .gitignore):
- Generated images (too large)
- Node modules
- API keys
- Cache files
- Model weights

## 🔄 Future Updates

```bash
# After making changes:
git add .
git commit -m "Description of changes"
git push
```

## 🎯 Quick Commands

```bash
# Check status
git status

# See what's changed
git diff

# View commit history
git log

# Pull latest changes
git pull
```

## 🔒 Security Notes

- ✅ API keys are in `.gitignore` (won't be committed)
- ✅ Generated images excluded (too large)
- ✅ Environment files excluded

**Never commit:**
- API keys
- `.env` files
- Personal credentials

## 📚 GitHub Resources

- [GitHub Docs](https://docs.github.com)
- [GitHub Pages](https://pages.github.com)
- [Git Basics](https://git-scm.com/book)
