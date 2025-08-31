# 🔧 GitHub Repository Configuration Guide

This guide explains how to configure your GitHub repository to implement the branching strategy with proper access controls.

## 📋 Repository Settings Checklist

### 1. General Repository Settings

**Repository Visibility:**
- ☑️ Set repository to **Public** (allows forking)
- ☑️ Enable Issues
- ☑️ Enable Projects
- ☑️ Enable Wiki (optional)
- ☑️ Enable Discussions (optional)

**Default Branch:**
- ☑️ Set `release` as the default branch for new clones/forks

### 2. Branch Protection Rules

#### Main Branch Protection (`main`)
```yaml
Protection Settings:
  - ☑️ Restrict pushes to matching branches
  - ☑️ Require pull request reviews before merging
    - Required reviewers: 1
    - Dismiss stale reviews: ☑️
    - Require review from code owners: ☑️
  - ☑️ Require status checks to pass before merging
    - Require branches to be up to date: ☑️
    - Status checks: CI/CD workflows
  - ☑️ Require signed commits
  - ☑️ Include administrators
  - ☑️ Restrict who can push to matching branches
    - People: [Your GitHub username only]
  - ☑️ Allow force pushes: ❌ (disabled)
  - ☑️ Allow deletions: ❌ (disabled)
```

#### Release Branch Protection (`release`)
```yaml
Protection Settings:
  - ☑️ Require pull request reviews before merging
    - Required reviewers: 1
    - Dismiss stale reviews: ☑️
  - ☑️ Require status checks to pass before merging
    - Require branches to be up to date: ☑️
    - Status checks: CI/CD workflows
  - ☑️ Include administrators
  - ☑️ Allow force pushes: ❌ (disabled)
  - ☑️ Allow deletions: ❌ (disabled)
```

#### Dev Branch Protection (`dev`)
```yaml
Protection Settings:
  - ☑️ Require pull request reviews before merging
    - Required reviewers: 1
  - ☑️ Require status checks to pass before merging
    - Status checks: CI/CD workflows
  - ☑️ Allow merge commits: ☑️
  - ☑️ Allow squash merging: ☑️
  - ☑️ Allow rebase merging: ☑️
```

### 3. Repository Access Settings

#### Collaborators & Teams
- **Owner**: Full access to all branches
- **External Contributors**: Fork and PR only

#### Issue Settings
- ☑️ Enable issues
- ☑️ Allow anyone to create issues
- ☑️ Use issue templates
- ☑️ Automatically delete head branches after PR merge

### 4. Actions & Workflows

#### Workflow Permissions
- ☑️ Read and write permissions for Actions
- ☑️ Allow GitHub Actions to create and approve pull requests

#### Secrets Configuration
- Add necessary secrets for CI/CD:
  - `PYPI_TOKEN` (for PyPI publishing)
  - `DOCKER_USERNAME` & `DOCKER_PASSWORD` (for Docker Hub)

## 🚀 Step-by-Step Configuration

### Step 1: Access Repository Settings
1. Go to your repository on GitHub
2. Click "Settings" tab
3. Navigate through the following sections:

### Step 2: Configure General Settings
```
Settings > General
├── Repository name: network-security-assessment-framework
├── Visibility: Public ☑️
├── Features:
│   ├── Issues: ☑️
│   ├── Projects: ☑️
│   └── Wiki: ☑️ (optional)
└── Default branch: release
```

### Step 3: Set Up Branch Protection
```
Settings > Branches
├── Add rule for "main"
│   └── Apply protection settings as listed above
├── Add rule for "release"
│   └── Apply protection settings as listed above
└── Add rule for "dev"
    └── Apply protection settings as listed above
```

### Step 4: Configure Access & Security
```
Settings > Manage access
├── Base permissions: Read
├── Collaborators: Add as needed
└── Teams: Configure if using organization

Settings > Security & analysis
├── Dependency alerts: ☑️
├── Security updates: ☑️
└── Code scanning: ☑️
```

### Step 5: Actions Configuration
```
Settings > Actions > General
├── Actions permissions: Allow all actions
├── Workflow permissions: Read and write
└── Allow Actions to create PRs: ☑️
```

## 🔄 Workflow Commands for You

### Setting Default Branch
```bash
# Set release as default branch (do this via GitHub UI)
# GitHub Settings > Branches > Default branch > Switch to release
```

### Managing Branch Protection
```bash
# You can also use GitHub CLI for automation
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":[]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1}'
```

## 📊 Branch Access Matrix

| Action | Main | Release | Dev | Feature/* |
|--------|------|---------|-----|-----------|
| Direct Push | Owner Only | PR Only | PR Only | Fork Only |
| Create PR to | From Release | From Dev | From Feature | N/A |
| Fork Access | No* | Yes | Yes | Yes |
| Issue Reports | No | No | Yes | Yes |
| Public Clone | No* | Yes | Yes | Yes |

*Protected via branch rules, not repo visibility

## 🎯 Verification Checklist

After configuration, verify:
- [ ] Can fork the repository
- [ ] Default branch for forks is `release`
- [ ] Cannot push directly to `main`
- [ ] Cannot push directly to `release` 
- [ ] Can create issues
- [ ] Can create PRs to `dev`
- [ ] CI/CD workflows run on all branches
- [ ] Branch protection rules are active

## 🚨 Important Notes

1. **Repository must be public** for external forks
2. **Main branch protection** prevents direct access while keeping repo public
3. **Release branch** serves as the public face of your project
4. **Contributors target dev branch** for all changes
5. **You maintain full control** over main branch merges

This configuration gives you:
- ✅ Public collaboration via forks
- ✅ Controlled access to main branch
- ✅ Clear workflow for contributors
- ✅ Professional development process
