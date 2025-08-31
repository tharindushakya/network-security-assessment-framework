# 🌳 Branching Strategy for NSAF

This document outlines the branching strategy and repository access control for the Network Security Assessment Framework.

## 📋 Branch Structure

### 🔒 **Main Branch** (`main`)
- **Purpose**: Production-ready, stable releases only
- **Access**: Private - Owner only
- **Protection**: Fully protected, no direct pushes
- **Contains**: Only thoroughly tested, stable code
- **Merge Policy**: Only from `release` branch via reviewed PRs

### 🚀 **Release Branch** (`release`)
- **Purpose**: **ONLY SOURCE FOR ALL RELEASES** - Public release candidates and stable versions
- **Access**: Public - Can be forked by anyone
- **Protection**: Protected from direct pushes
- **Contains**: Release-ready code, cleaned of development artifacts
- **Merge Policy**: From `dev` branch when ready for release
- **Release Policy**: ALL GitHub releases, tags, and packages are built ONLY from this branch

### 🛠️ **Dev Branch** (`dev`)
- **Purpose**: Active development and issue resolution
- **Access**: Public - Receives issues and contributions
- **Protection**: Moderate protection, requires reviews
- **Contains**: Latest development code, may include experimental features
- **Merge Policy**: Feature branches and issue fixes merge here

### 🌿 **Feature Branches**
- **Purpose**: Individual features and bug fixes
- **Naming**: `feature/feature-name` or `fix/issue-number`
- **Access**: Public - Contributors can create via forks
- **Lifecycle**: Created from `dev`, merged back to `dev`

## 🔄 Workflow Process

### For Contributors (External)
1. **Fork** the repository
2. **Clone** their fork locally
3. **Create feature branch** from `release` or `dev`
4. **Make changes** and commit
5. **Push** to their fork
6. **Create Pull Request** to `dev` branch
7. **Address review feedback**
8. **Merge** after approval

### For Maintainer (You)
1. **Review PRs** on `dev` branch
2. **Merge approved changes** to `dev`
3. **Test thoroughly** on `dev`
4. **Create PR** from `dev` to `release` when ready
5. **Clean release branch** (remove dev artifacts using release scripts)
6. **Tag release** on `release` branch - **THIS IS THE ONLY RELEASE SOURCE**
7. **All GitHub releases, packages, and Docker images are built from `release` branch only**
8. **Merge** `release` to `main` for archival

## 🛡️ Repository Access Control

### GitHub Repository Settings

1. **Repository Visibility**:
   - Set to **Public** to allow forks
   - Main branch protected via rules, not visibility

2. **Branch Protection Rules**:

   **Main Branch (`main`)**:
   - ✅ Restrict pushes to matching branches
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date
   - ✅ Require signed commits
   - ✅ Include administrators in restrictions
   - ✅ Allow only specific people to push (Owner only)

   **Release Branch (`release`)**:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date
   - ✅ Dismiss stale reviews when new commits are pushed

   **Dev Branch (`dev`)**:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass
   - ✅ Allow merge commits

3. **Issue Settings**:
   - ✅ Enable issues on the repository
   - ✅ Allow anyone to create issues
   - ✅ Use issue templates for structured reporting

4. **Fork Settings**:
   - ✅ Allow forking
   - ✅ Set `release` as the default branch for forks

## 🎯 Access Levels Summary

| Branch | Visibility | Fork Access | Issue Reports | Direct Push |
|--------|------------|-------------|---------------|-------------|
| `main` | Private* | No | No | Owner Only |
| `release` | Public | Yes | No | PR Only |
| `dev` | Public | Yes | Yes | PR Only |
| `feature/*` | Public | Yes | Yes | Fork Only |

*Main branch is protected via rules, not repo visibility

## 🔧 Setup Commands

### Initial Setup (Already Done)
```bash
# Create release branch
git checkout dev
git checkout -b release
git push -u origin release

# Set release as default branch for new clones/forks
# (Done via GitHub settings)
```

### For Contributors
```bash
# Fork on GitHub, then:
git clone https://github.com/[username]/network-security-assessment-framework.git
cd network-security-assessment-framework
git remote add upstream https://github.com/tharindushakya/network-security-assessment-framework.git

# Create feature branch
git checkout release
git checkout -b feature/my-feature

# Work and commit
git add .
git commit -m "Add new feature"
git push origin feature/my-feature

# Create PR to dev branch via GitHub
```

### Maintainer Workflow
```bash
# Review and merge PRs to dev
# When ready for release:
git checkout dev
git pull origin dev

# Create release PR
git checkout release
git merge dev
git push origin release

# Tag release
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# IMPORTANT: All releases are built from 'release' branch only
# GitHub Actions will automatically build packages from this branch

# Merge to main (via PR for audit trail)
git checkout main
git merge release
git push origin main
```

## 🎉 Benefits of This Strategy

1. **Public Collaboration**: Contributors can fork `release` branch
2. **Issue Management**: Issues go to `dev` branch for active development
3. **Stable Releases**: `release` branch always contains clean, stable code
4. **Private Main**: `main` branch serves as your private production archive
5. **Clear Workflow**: Defined path from development to production
6. **Quality Control**: Multiple review stages before reaching `main`
7. ****SINGLE SOURCE OF TRUTH**: ALL releases come exclusively from `release` branch**

## 📝 Notes

- Contributors should target `dev` branch for PRs
- Release branch gets cleaned of development artifacts before tagging
- Main branch serves as the authoritative production history
- **ALL GitHub releases, tags, packages, and Docker images are built ONLY from `release` branch**
- Use semantic versioning for all releases
- GitHub Actions workflows should run on all branches for CI/CD
- **Never create releases from `main` or `dev` branches - only from `release`**
