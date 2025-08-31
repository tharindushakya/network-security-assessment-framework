# GitHub Ruleset Import Guide - FIXED VERSION

## Overview
This guide helps you import the NSAF branch protection rulesets into your GitHub repository. The rulesets have been **completely fixed** based on GitHub's official documentation.

## ✅ Issues Fixed
- **Removed invalid actor configurations** - No bypass_actors specified  
- **Simplified branch references** - Using "main", "release", "dev" instead of "refs/heads/..."
- **Removed unsupported parameters** - Cleaned up rule parameters for compatibility
- **Removed description fields** - GitHub import only accepts specific fields
- **Simplified rule structure** - Following GitHub's documented format exactly

## Available Rulesets

### 1. Main Branch Protection (`github-ruleset-main-branch.json`)
**Purpose**: Maximum protection for main branch
**Rules**: 
- Prevents branch deletion (`deletion`)
- Prevents force pushes (`non_fast_forward`)
- Requires pull requests with 1 approval (`pull_request`)
- Requires linear history (`required_linear_history`)

### 2. Release Branch Protection (`github-ruleset-release-branch.json`)  
**Purpose**: Protection for release branch (public fork target)
**Rules**:
- Prevents branch deletion (`deletion`)
- Prevents force pushes (`non_fast_forward`)
- Requires pull requests with 1 approval (`pull_request`)

### 3. Dev Branch Protection (`github-ruleset-dev-branch.json`)
**Purpose**: Basic protection for development branch
**Rules**:
- Requires pull requests with 1 approval (`pull_request`)

## Import Instructions

### Step 1: Access Repository Settings
1. Go to your GitHub repository: `https://github.com/yourusername/your-repo`
2. Click **Settings** tab
3. In the left sidebar, scroll to **Code and automation**
4. Click **Rules** → **Rulesets**

### Step 2: Import Each Ruleset
1. Click **New ruleset** → **Import a ruleset**
2. Click **Choose file** and select one of the JSON files
3. Review the imported configuration preview
4. Click **Create ruleset**

### Step 3: Recommended Import Order
Import in this order to avoid conflicts:
1. `github-ruleset-dev-branch.json` (least restrictive)
2. `github-ruleset-release-branch.json` 
3. `github-ruleset-main-branch.json` (most restrictive)

### Step 4: Verify Each Import
After importing each ruleset:
- [ ] Ruleset appears in the **Rulesets** list
- [ ] **Status** shows as "Active" 
- [ ] **Target** shows correct branch name
- [ ] **Rules** count matches expected number

## What Changed (Technical Details)

### Before (Caused Errors)
```json
{
  "name": "Example",
  "description": "This caused errors",
  "conditions": {
    "ref_name": {
      "include": ["refs/heads/main"]  // ❌ Too verbose
    }
  },
  "rules": [
    {
      "type": "deletion",
      "parameters": {
        "restricted_deletions": true  // ❌ Unsupported
      }
    }
  ],
  "bypass_actors": [
    {
      "actor_id": null,  // ❌ Invalid actor
      "actor_type": "RepositoryRole"
    }
  ]
}
```

### After (Works Correctly)
```json
{
  "name": "Example",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": {
      "include": ["main"]  // ✅ Simple branch name
    }
  },
  "rules": [
    {
      "type": "deletion"  // ✅ No parameters needed
    }
  ]
  // ✅ No bypass_actors (GitHub auto-configures)
}
```

## Testing the Import

### 1. Test Branch Protection
After import, test that protection works:

```bash
# This should FAIL (protected)
git push origin main

# This should WORK (via PR)
git checkout -b test-branch
git push origin test-branch
# Then create PR via GitHub UI
```

### 2. Verify in GitHub UI
1. Go to **Settings** → **Branches**
2. You should see "Branch protection rules" referencing your rulesets
3. Try to delete a protected branch (should be prevented)

## Post-Import Customization

After successful import, you can enhance via GitHub UI:

### Add Status Checks
1. Go to imported ruleset in **Settings** → **Rules** → **Rulesets**
2. Click **Edit** on the ruleset
3. Add **Required status checks** rule
4. Specify your CI workflow names

### Configure Bypass Permissions  
1. Edit the ruleset
2. Scroll to **Bypass permissions**
3. Add specific users, teams, or apps
4. Choose bypass mode (always/pull_request)

## Cleanup After Import

### Remove Temporary Files
After successful import, clean up:

```bash
# Windows PowerShell
cd "d:\Projects\Github\Network Security Assessment Framework"
Remove-Item github-ruleset-*.json
git add .
git commit -m "Remove temporary ruleset files after successful import"
git push origin dev

# Or use the cleanup script
.\cleanup-rulesets.bat
```

```bash
# Linux/Mac
cd "/path/to/Network Security Assessment Framework"  
rm github-ruleset-*.json
git add .
git commit -m "Remove temporary ruleset files after successful import"
git push origin dev

# Or use the cleanup script
./cleanup-rulesets.sh
```

## Troubleshooting

### Still Getting "Invalid Actor" Error?
If you still see this error:
1. Make sure you're using the **fixed** JSON files (the ones without `bypass_actors`)
2. Try importing to a test repository first
3. Verify you have **admin** permissions on the repository

### Import Button Grayed Out?
- You need **admin** access to the repository
- Repository must not be archived
- Check if organization policies restrict ruleset creation

### Ruleset Not Working?
1. Check **enforcement** is set to "active" 
2. Verify branch names match exactly (case-sensitive)
3. Look for conflicting branch protection rules

## Advanced Tips

### Rule Layering
From GitHub docs: "If multiple rulesets target the same branch, rules aggregate and the most restrictive applies."

### Organization Rulesets
For GitHub Enterprise: You can create organization-wide rulesets that apply to multiple repositories.

### Monitoring
- Check **Settings** → **Rules** → **Insights** for rule violations
- Use repository audit logs to track protection events

## Success Indicators

You'll know the import worked when:
- ✅ All 3 rulesets show "Active" status
- ✅ Direct pushes to `main` and `release` branches are blocked  
- ✅ PRs are required for all protected branches
- ✅ Force pushes are prevented on protected branches

## Need Help?

1. **Check JSON syntax**: Use [jsonlint.com](https://jsonlint.com) to validate files
2. **GitHub Support**: Contact GitHub if you have Enterprise/Team plan
3. **Test Environment**: Try importing to a test repository first
4. **Repository Permissions**: Ensure you have admin access

---

**Note**: These ruleset files are temporary and should be deleted after successful import. The actual branch protection will be managed through GitHub's UI after import.
