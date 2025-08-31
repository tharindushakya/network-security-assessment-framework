# Release Management for NSAF

This document outlines the release process and file exclusions for the Network Security Assessment Framework (NSAF).

## Release Exclusions

The following files and directories are automatically excluded from releases through `.gitignore`, `.gitattributes`, and `MANIFEST.in`:

### Summary and Documentation Files
- `PROJECT_COMPLETE.md` - Development completion summary
- `PROJECT_STRUCTURE.md` - Internal project structure documentation
- `SECURITY_REMEDIATION_SUMMARY.md` - Security fix summary
- `SECURITY_CONFIG.md` - Internal security configuration guide

### Test and Development Files
- `test_*.py` - All test files
- `*_test.py` - Test files with different naming conventions
- `demo*.py` - Demo and example scripts
- `test_installation.py` - Installation testing script
- `test_security_fixes.py` - Security validation script
- `pytest.ini` - Test configuration

### Security Scan Results
- `security_scan_*.json` - Bandit security scan results
- `bandit_*.json` - Security analysis outputs
- `*_scan_results_*.json` - Any scan result files
- `demo*_results_*.json` - Demo output files

### Development Artifacts
- `__pycache__/` - Python cache directories
- `*.pyc`, `*.pyo` - Compiled Python files
- `.pytest_cache/` - Test cache
- `.coverage`, `htmlcov/` - Coverage reports
- `.mypy_cache/` - Type checking cache

### IDE and OS Files
- `.vscode/` - VS Code settings
- `.idea/` - IntelliJ/PyCharm settings
- `.DS_Store` - macOS file system metadata
- `Thumbs.db` - Windows file system metadata
- `desktop.ini` - Windows folder settings

### Logs and Temporary Files
- `logs/` - Log directories
- `reports/` - Report output directories
- `*.log` - Log files
- `*.tmp`, `*.temp` - Temporary files

## Release Process

### Automated Release (Recommended)

1. **Create a release tag:**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

2. **GitHub Actions will automatically:**
   - Clean the repository by removing excluded files
   - Build Python packages (wheel and source distribution)
   - Create GitHub release with changelog
   - Upload release assets
   - Build and push Docker images
   - Optionally publish to PyPI (if token is configured)

### Manual Release Preparation

1. **Run the release preparation script:**
   ```bash
   python scripts/prepare_release.py --version v1.0.0
   ```

2. **Review changes and test:**
   ```bash
   # Verify the package builds correctly
   python -m build
   
   # Test installation
   pip install dist/nsaf-*.whl
   python -c "import nsaf; print('NSAF installed successfully')"
   ```

3. **Create release manually if needed:**
   ```bash
   # Create tag
   git tag -a v1.0.0 -m "Release version 1.0.0"
   
   # Push tag
   git push origin v1.0.0
   
   # Upload to PyPI
   twine upload dist/*
   ```

4. **Restore development files:**
   ```bash
   python scripts/prepare_release.py --restore
   ```

## Release Checklist

### Pre-Release
- [ ] Update version in `setup.py`
- [ ] Update `CHANGELOG.md` with new features and fixes
- [ ] Run full test suite
- [ ] Run security scan (Bandit)
- [ ] Update documentation if needed
- [ ] Review and clean up any temporary files

### Release
- [ ] Create and push version tag
- [ ] Verify GitHub Actions workflow completes successfully
- [ ] Test installation from PyPI/GitHub releases
- [ ] Test Docker image functionality
- [ ] Update release notes with any additional information

### Post-Release
- [ ] Announce release in appropriate channels
- [ ] Update any dependent projects
- [ ] Plan next release cycle
- [ ] Monitor for any issues or bug reports

## File Structure After Release

The release package will contain:
```
nsaf/
├── nsaf/               # Core package
│   ├── core/          # Scanner modules
│   ├── utils/         # Utility functions
│   └── templates/     # Report templates
├── docs/              # User documentation
├── examples/          # Usage examples
├── README.md          # Project overview
├── LICENSE            # License file
├── CHANGELOG.md       # Version history
├── CONTRIBUTING.md    # Contribution guidelines
├── SECURITY.md        # Security policy
├── requirements.txt   # Dependencies
└── setup.py          # Package configuration
```

## Notes

- The `.gitattributes` file uses `export-ignore` to exclude files from `git archive` commands
- The `MANIFEST.in` file controls what gets included in Python package distributions
- The GitHub Actions workflow automatically cleans the repository before building releases
- Development files are preserved in the repository but excluded from release packages
- Use the backup and restore functionality in the release preparation script for safety

## Troubleshooting

### Common Issues

1. **Files still appearing in release:**
   - Check `.gitattributes` has correct `export-ignore` entries
   - Verify `MANIFEST.in` excludes the files
   - Ensure GitHub Actions workflow cleans files before building

2. **Missing files in release:**
   - Check `MANIFEST.in` includes necessary files
   - Verify files are not accidentally excluded by patterns
   - Test build locally with `python -m build`

3. **Docker build fails:**
   - Ensure all required dependencies are in `requirements.txt`
   - Check that package builds successfully first
   - Verify Docker base image has necessary system packages
