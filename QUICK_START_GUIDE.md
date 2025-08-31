# NSAF - Network Security Assessment Framework

## Quick Start Guide

### Installation & Setup
```bash
# Clone repository
git clone https://github.com/yourusername/network-security-assessment-framework.git
cd network-security-assessment-framework

# Install dependencies
pip install -r requirements.txt

# Install NSAF package
pip install -e .
```

### Basic Usage
```bash
# CLI Interface
python nsaf_cli.py --target 192.168.1.1 --output-format html

# Python API
from nsaf import NetworkScanner, VulnerabilityScanner, ReportGenerator

scanner = NetworkScanner()
vuln_scanner = VulnerabilityScanner()
report_gen = ReportGenerator()

# Scan network
results = scanner.scan("192.168.1.0/24")
vulnerabilities = vuln_scanner.analyze(results)
report = report_gen.generate(vulnerabilities, format='html')
```

### GitHub Repository Setup

#### Branch Strategy
- **main**: Production releases (protected, private)
- **release**: Public fork target (protected) 
- **dev**: Development work (protected, accepts PRs)

#### GitHub Rulesets Import
1. Go to **Settings** → **Rules** → **Rulesets**
2. Import these files in order:
   - `github-ruleset-dev-branch.json` (moderate protection)
   - `github-ruleset-release-branch.json` (high protection)
   - `github-ruleset-main-branch.json` (maximum protection)
3. Verify each shows "Active" status
4. Delete ruleset JSON files after successful import

#### Repository Access
- **Main branch**: Owner only, maximum protection
- **Release branch**: Public forks, high protection
- **Dev branch**: Contributors, moderate protection

### Development Workflow
```bash
# Create feature branch from dev
git checkout dev
git pull origin dev
git checkout -b feature/your-feature

# Make changes and test
python -m pytest tests/

# Push and create PR to dev branch
git push origin feature/your-feature
# Create PR via GitHub UI targeting dev branch

# Release process (owner only)
# 1. Merge dev → release via PR
# 2. Create release from release branch
# 3. Merge release → main via PR (if needed)
```

### Key Features
- **Network Discovery**: Port scanning, service detection
- **Vulnerability Assessment**: Security analysis and scoring
- **Report Generation**: HTML, JSON, CSV formats
- **CLI Interface**: Command-line tool for automation
- **Python API**: Programmatic access for integration

### Security
- SSL/TLS verification enabled
- Input validation and sanitization  
- XSS protection in reports
- Secure file handling
- No hardcoded credentials

### Files You Need
- Core framework: `nsaf/` directory
- CLI tool: `nsaf_cli.py`
- Configuration: `requirements.txt`, `setup.py`, `MANIFEST.in`
- Documentation: `README.md`, `CHANGELOG.md`, `SECURITY.md`
- Testing: `tests/` directory, `pytest.ini`
- GitHub config: `.github/` workflows, `CONTRIBUTING.md`, `LICENSE`
- Rulesets: `github-ruleset-*.json` (temporary, delete after import)

### Support
- Issues: Use GitHub Issues on dev branch
- Security: See SECURITY.md for reporting
- Contributing: See CONTRIBUTING.md for guidelines

---
**Note**: This is a comprehensive security assessment tool. Use responsibly and only on networks you own or have permission to test.
