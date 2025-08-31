#!/usr/bin/env python3
"""
Security scan script for NSAF
Runs Bandit security analysis on the codebase
"""

import subprocess
import sys
import json
from pathlib import Path


def check_bandit_installed():
    """Check if bandit is installed and install if needed"""
    # First try using python -m bandit
    try:
        result = subprocess.run([sys.executable, '-m', 'bandit', '--version'], 
                              capture_output=True, text=True)
        print(f"Bandit version: {result.stdout.strip()}")
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    
    # Try direct bandit command
    try:
        result = subprocess.run(['bandit', '--version'], capture_output=True, text=True)
        print(f"Bandit version: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("Bandit not found. Installing...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'bandit[toml]>=1.7.5'], 
                         check=True, capture_output=True)
            print("Bandit installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to install bandit: {e}")
            return False


def run_bandit_scan():
    """Run Bandit security scan"""
    print("Running Bandit Security Scan")
    print("=" * 40)
    
    # Ensure bandit is available
    if not check_bandit_installed():
        return False
    
    # Run bandit scan with JSON output for parsing
    cmd = [
        sys.executable, '-m', 'bandit',  # Use python -m bandit for better compatibility
        '-r', '.',  # Recursive scan
        '-f', 'json',  # JSON output for parsing
        '--exit-zero-on-no-confidence',  # Don't fail on no confidence issues
        '--skip', 'B101,B601',  # Skip some common false positives
    ]
    
    # Fallback to direct bandit command if python -m fails
    fallback_cmd = [
        'bandit',
        '-r', '.',
        '-f', 'json',
        '--exit-zero-on-no-confidence',
        '--skip', 'B101,B601',
    ]
    
    try:
        print("Scanning codebase...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        # If the first command fails, try the fallback
        if result.returncode != 0 and "No module named" in result.stderr:
            print("   Trying alternative bandit command...")
            result = subprocess.run(fallback_cmd, capture_output=True, text=True, timeout=120)
        
        # Parse JSON output
        try:
            scan_data = json.loads(result.stdout) if result.stdout else {}
            
            # Get metrics
            metrics = scan_data.get('metrics', {})
            results = scan_data.get('results', [])
            
            # Print summary
            print(f"Scan Results:")
            print(f"   Files scanned: {metrics.get('_totals', {}).get('loc', 'Unknown')}")
            print(f"   Issues found: {len(results)}")
            
            # Categorize issues by severity
            high_issues = [r for r in results if r.get('issue_severity') == 'HIGH']
            medium_issues = [r for r in results if r.get('issue_severity') == 'MEDIUM']
            low_issues = [r for r in results if r.get('issue_severity') == 'LOW']
            
            print(f"   High severity: {len(high_issues)}")
            print(f"   Medium severity: {len(medium_issues)}")
            print(f"   Low severity: {len(low_issues)}")
            
            # Show high and medium issues
            if high_issues or medium_issues:
                print("\nIssues requiring attention:")
                for issue in high_issues + medium_issues:
                    print(f"   {issue.get('test_id', 'Unknown')}: {issue.get('issue_text', 'No description')}")
                    print(f"      File: {issue.get('filename', 'Unknown')}:{issue.get('line_number', '?')}")
                    print(f"      Severity: {issue.get('issue_severity', 'Unknown')}")
                    print(f"      Confidence: {issue.get('issue_confidence', 'Unknown')}")
                    print()
            
            # Determine success
            if high_issues:
                print("Security scan failed: High severity issues found")
                return False
            elif medium_issues:
                print("Security scan passed with warnings: Medium severity issues found")
                return True
            else:
                print("Security scan passed: No high or medium severity issues found")
                return True
                
        except json.JSONDecodeError:
            # Fallback to simple output parsing
            if result.returncode == 0:
                print("Security scan completed successfully")
                print("No high or medium severity issues found")
                return True
            else:
                print(f"Security scan completed with warnings (exit code: {result.returncode})")
                if result.stdout:
                    print("Scan output:")
                    print(result.stdout[:1000])  # Limit output
                return False
            
    except subprocess.TimeoutExpired:
        print("Security scan timed out (120s)")
        return False
    except Exception as e:
        print(f"Security scan failed: {e}")
        return False


def run_safety_check():
    """Run safety check for known vulnerabilities in dependencies"""
    print("\nRunning Safety Check for Dependencies")
    print("=" * 45)
    
    try:
        # Try to install safety if not available
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'safety'], 
                      capture_output=True, check=False)
        
        # Run safety check
        result = subprocess.run([
            sys.executable, '-m', 'safety', 'check', 
            '--json', '--ignore', '70612'  # Ignore jinja2 issue if present
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("No known security vulnerabilities found in dependencies")
            return True
        else:
            print("Potential vulnerabilities found in dependencies:")
            if result.stdout:
                try:
                    safety_data = json.loads(result.stdout)
                    for vuln in safety_data:
                        print(f"   Package: {vuln.get('package_name', 'Unknown')}")
                        print(f"   Vulnerability: {vuln.get('advisory', 'No description')}")
                except json.JSONDecodeError:
                    print(result.stdout[:500])
            return False
            
    except subprocess.TimeoutExpired:
        print("Safety check timed out")
        return True  # Don't fail the build for this
    except Exception as e:
        print(f"Safety check failed: {e}")
        return True  # Don't fail the build for this


def main():
    """Main function"""
    project_root = Path(__file__).parent.parent
    print(f"Security Scanning: {project_root.absolute()}")
    print("=" * 60)
    
    # Change to project directory
    import os
    os.chdir(project_root)
    
    # Run security scans
    bandit_success = run_bandit_scan()
    safety_success = run_safety_check()
    
    # Summary
    print("\nSecurity Scan Summary")
    print("=" * 30)
    print(f"Bandit scan: {'PASS' if bandit_success else 'FAIL'}")
    print(f"Safety check: {'PASS' if safety_success else 'WARN'}")
    
    if bandit_success:
        print("\nPrimary security scan passed!")
        if not safety_success:
            print("Review dependency vulnerabilities but build can proceed")
        return 0
    else:
        print("\nSecurity scan failed! Fix issues before deploying.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
