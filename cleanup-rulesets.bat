@echo off
REM 🧹 Cleanup Script for GitHub Ruleset Import Files (Windows)
REM Run this script AFTER you have successfully imported the rulesets to GitHub

echo 🧹 Cleaning up GitHub ruleset import files...
echo.

echo 📋 Files to be deleted:
dir github-ruleset-*.json RULESET_IMPORT_GUIDE.md cleanup-rulesets.* 2>nul

echo.
set /p confirm="❓ Have you successfully imported all rulesets to GitHub? (y/N): "

if /i "%confirm%"=="y" goto delete
if /i "%confirm%"=="yes" goto delete
goto cancel

:delete
echo 🗑️ Deleting ruleset import files...

REM Delete ruleset JSON files
del github-ruleset-*.json 2>nul

REM Delete import guide  
del RULESET_IMPORT_GUIDE.md 2>nul

REM Delete cleanup scripts
del cleanup-rulesets.sh 2>nul
del cleanup-rulesets.bat 2>nul

echo ✅ Cleanup complete!
echo 📝 Don't forget to commit the changes:
echo    git add .
echo    git commit -m "🧹 Remove ruleset import files after GitHub configuration"
goto end

:cancel
echo ❌ Cleanup cancelled. Import rulesets first, then run this script again.
echo.
echo 📖 Import instructions:
echo    1. Go to GitHub repository → Settings → Rules → Rulesets
echo    2. Click 'New ruleset' → 'Import a ruleset'
echo    3. Upload each JSON file (main, release, dev)
echo    4. Verify the rules are active
echo    5. Run this cleanup script again

:end
pause
