# 🛡️ GitHub Rulesets Import Guide

This directory contains pre-configured GitHub rulesets that implement the branching strategy for NSAF.

## 📋 Ruleset Files

### 1. `github-ruleset-main-branch.json`
- **Protection Level**: Maximum (Owner Only)
- **Target**: `main` branch
- **Features**: 
  - Restricts all pushes (PR only)
  - Requires 1 review + code owner approval
  - Requires status checks
  - Prevents force pushes and deletions
  - Linear history required

### 2. `github-ruleset-release-branch.json`  
- **Protection Level**: High (Public Fork Target)
- **Target**: `release` branch
- **Features**:
  - Restricts direct pushes (PR only)
  - Requires 1 review
  - Requires status checks
  - Prevents force pushes and deletions
  - Admin can bypass via PR

### 3. `github-ruleset-dev-branch.json`
- **Protection Level**: Moderate (Development)
- **Target**: `dev` branch  
- **Features**:
  - Restricts direct pushes (PR only)
  - Requires 1 review
  - Basic status checks
  - Prevents force pushes and deletions
  - More flexible for development

## 🚀 How to Import Rulesets

### Step 1: Access Repository Settings
1. Go to your GitHub repository
2. Click **Settings** tab
3. Navigate to **Rules** in the left sidebar
4. Click **Rulesets**

### Step 2: Import Each Ruleset
1. Click **New ruleset** button
2. Select **Import a ruleset**
3. Upload one of the JSON files:
   - Start with `github-ruleset-main-branch.json`
   - Then `github-ruleset-release-branch.json`
   - Finally `github-ruleset-dev-branch.json`
4. Review the imported rules
5. Click **Create ruleset**

### Step 3: Verify Configuration
After importing all three rulesets, verify:
- [ ] Main branch has maximum protection
- [ ] Release branch allows PRs but blocks direct pushes
- [ ] Dev branch has moderate protection for development
- [ ] All branches prevent force pushes and deletions

## ⚙️ Alternative: Manual Configuration

If you prefer to configure manually instead of importing:

### Main Branch Rules:
```
Settings → Rules → Rulesets → New ruleset
├── Name: "Main Branch Protection"
├── Target: main
├── Rules:
│   ├── Restrict pushes ✅
│   ├── Require pull requests ✅ (1 review + code owner)
│   ├── Require status checks ✅
│   ├── Restrict force pushes ✅
│   ├── Restrict deletions ✅
│   └── Require linear history ✅
└── Bypass: None
```

### Release Branch Rules:
```
Settings → Rules → Rulesets → New ruleset  
├── Name: "Release Branch Protection"
├── Target: release
├── Rules:
│   ├── Restrict pushes ✅
│   ├── Require pull requests ✅ (1 review)
│   ├── Require status checks ✅
│   ├── Restrict force pushes ✅
│   └── Restrict deletions ✅
└── Bypass: Admin (via PR only)
```

### Dev Branch Rules:
```
Settings → Rules → Rulesets → New ruleset
├── Name: "Dev Branch Protection"  
├── Target: dev
├── Rules:
│   ├── Require pull requests ✅ (1 review)
│   ├── Require status checks ✅ (basic)
│   ├── Restrict force pushes ✅
│   └── Restrict deletions ✅
└── Bypass: Admin (via PR only)
```

## 🔍 Expected Behavior After Setup

### Main Branch (`main`):
- ❌ Direct pushes blocked for everyone (including admin)
- ✅ Only PRs from release branch allowed
- ✅ Requires your review + status checks
- ✅ Complete protection for production code

### Release Branch (`release`):
- ❌ Direct pushes blocked
- ✅ PRs from dev branch allowed
- ✅ Public can fork this branch
- ✅ Source for all releases and tags

### Dev Branch (`dev`):
- ❌ Direct pushes blocked  
- ✅ PRs from feature branches allowed
- ✅ Contributors target this branch
- ✅ Active development happens here

## 🧹 Cleanup Instructions

After importing the rulesets, you should delete these JSON files:

```bash
# Delete the ruleset files
rm github-ruleset-*.json
rm RULESET_IMPORT_GUIDE.md

# Commit the cleanup
git add .
git commit -m "🧹 Remove ruleset import files after GitHub configuration"
```

## 🎯 Verification Checklist

After importing and cleaning up:
- [ ] All three rulesets are active in GitHub
- [ ] Cannot push directly to main branch
- [ ] Cannot push directly to release branch  
- [ ] Cannot push directly to dev branch
- [ ] Can create PRs between branches
- [ ] Status checks are required
- [ ] JSON files have been deleted from repository

## 📞 Support

If you encounter issues with ruleset import:
1. Check that you have admin access to the repository
2. Ensure the JSON files are valid (they should be pre-validated)
3. Try importing one ruleset at a time
4. Verify branch names match your repository exactly

The rulesets are designed to work immediately after import with no additional configuration needed.
