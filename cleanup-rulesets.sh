#!/bin/bash
# 🧹 Cleanup Script for GitHub Ruleset Import Files
# Run this script AFTER you have successfully imported the rulesets to GitHub

echo "🧹 Cleaning up GitHub ruleset import files..."

# List files to be deleted
echo "📋 Files to be deleted:"
ls -la github-ruleset-*.json RULESET_IMPORT_GUIDE.md cleanup-rulesets.sh 2>/dev/null || echo "Some files may already be deleted"

echo ""
read -p "❓ Have you successfully imported all rulesets to GitHub? (y/N): " confirm

if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
    echo "🗑️ Deleting ruleset import files..."
    
    # Delete ruleset JSON files
    rm -f github-ruleset-*.json
    
    # Delete import guide
    rm -f RULESET_IMPORT_GUIDE.md
    
    # Delete this cleanup script
    rm -f cleanup-rulesets.sh
    
    echo "✅ Cleanup complete!"
    echo "📝 Don't forget to commit the changes:"
    echo "   git add ."
    echo "   git commit -m '🧹 Remove ruleset import files after GitHub configuration'"
    
else
    echo "❌ Cleanup cancelled. Import rulesets first, then run this script again."
    echo ""
    echo "📖 Import instructions:"
    echo "   1. Go to GitHub repository → Settings → Rules → Rulesets"
    echo "   2. Click 'New ruleset' → 'Import a ruleset'"
    echo "   3. Upload each JSON file (main, release, dev)"
    echo "   4. Verify the rules are active"
    echo "   5. Run this cleanup script again"
fi
