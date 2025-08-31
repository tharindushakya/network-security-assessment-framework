#!/usr/bin/env python3
"""
Security scanner script for NSAF.
Runs various security checks and generates reports.
"""

import subprocess
import sys
import json
from pathlib import Path


def run_bandit_scan():
    """Run Bandit security scanner."""
    print("🔍 Running Bandit security scan...")
    
    try:
        result = subprocess.run([
            "bandit", 
            "-r", "nsaf/",
            "-f", "json",
            "-o", "security_scan_results.json",
            "--configfile", ".bandit"
        ], capture_output=True, text=True, check=False)
        
        if result.returncode == 0:
            print("✅ Bandit scan completed successfully - No issues found")
        elif result.returncode == 1:
            print("⚠️  Bandit scan completed with findings")
            with open("security_scan_results.json", "r") as f:
                results = json.load(f)
                total_issues = len(results.get("results", []))
                print(f"Found {total_issues} security issues")
        else:
            print(f"❌ Bandit scan failed: {result.stderr}")
            
    except FileNotFoundError:
        print("❌ Bandit not found. Install with: pip install bandit")
        return False
    
    return True


def run_safety_scan():
    """Run Safety vulnerability scanner for dependencies."""
    print("🔍 Running Safety dependency scan...")
    
    try:
        result = subprocess.run([
            "safety", "check", 
            "--json",
            "--output", "dependency_scan_results.json"
        ], capture_output=True, text=True, check=False)
        
        if result.returncode == 0:
            print("✅ Safety scan completed - No vulnerable dependencies found")
        else:
            print("⚠️  Safety scan found vulnerable dependencies")
            
    except FileNotFoundError:
        print("❌ Safety not found. Install with: pip install safety")
        return False
    
    return True


def generate_security_report():
    """Generate combined security report."""
    print("📋 Generating security report...")
    
    report = {
        "scan_date": str(Path().resolve()),
        "bandit_results": {},
        "safety_results": {},
        "summary": {}
    }
    
    # Load Bandit results
    bandit_file = Path("security_scan_results.json")
    if bandit_file.exists():
        with open(bandit_file) as f:
            report["bandit_results"] = json.load(f)
    
    # Load Safety results  
    safety_file = Path("dependency_scan_results.json")
    if safety_file.exists():
        with open(safety_file) as f:
            report["safety_results"] = json.load(f)
    
    # Generate summary
    bandit_issues = len(report["bandit_results"].get("results", []))
    safety_issues = len(report["safety_results"]) if isinstance(report["safety_results"], list) else 0
    
    report["summary"] = {
        "total_issues": bandit_issues + safety_issues,
        "bandit_issues": bandit_issues,
        "safety_issues": safety_issues,
        "status": "PASS" if (bandit_issues + safety_issues) == 0 else "REVIEW_REQUIRED"
    }
    
    # Save combined report
    with open("combined_security_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"📄 Security report saved to combined_security_report.json")
    print(f"📊 Summary: {report['summary']}")


def main():
    """Main security scanning function."""
    print("🛡️  NSAF Security Scanner")
    print("=" * 50)
    
    success = True
    
    # Run security scans
    success &= run_bandit_scan()
    success &= run_safety_scan()
    
    # Generate report
    generate_security_report()
    
    if success:
        print("\n✅ Security scanning completed successfully")
        return 0
    else:
        print("\n❌ Some security scans failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
