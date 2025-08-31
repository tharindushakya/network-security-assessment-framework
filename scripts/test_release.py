#!/usr/bin/env python3
"""
Test script to validate release workflow components
"""

import sys
import subprocess
from pathlib import Path


def run_command(cmd: str, description: str) -> bool:
    """Run a command and return success status"""
    print(f"\n🔍 {description}")
    print(f"Running: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ Success")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Failed (exit code: {result.returncode})")
            if result.stderr.strip():
                print(f"Error: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"❌ Timeout (30s)")
        return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


def main():
    """Test release workflow components"""
    print("🚀 NSAF Release Workflow Validation")
    print("=" * 50)
    
    # Change to project directory
    project_dir = Path(__file__).parent.parent
    print(f"Project directory: {project_dir.absolute()}")
    
    # Test components
    tests = [
        ("python scripts/update_version.py setup.py 1.0.1", "Test version updater"),
        ("python scripts/update_version.py setup.py 1.0.0", "Revert version"),
        ("python -c \"import nsaf; print('NSAF import successful')\"", "Test NSAF import"),
        ("python scripts/security_scan.py", "Run security scan"),
        ("python -m build --help", "Check build tool availability"),
    ]
    
    results = []
    for cmd, desc in tests:
        success = run_command(cmd, desc)
        results.append((desc, success))
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 30)
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for desc, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {desc}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Release workflow should work correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please review before releasing.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
