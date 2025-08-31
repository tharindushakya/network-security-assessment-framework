#!/usr/bin/env python3
"""
Release content validator - Shows what files will be included/excluded in releases
"""

import os
import fnmatch
from pathlib import Path

class ReleaseValidator:
    def __init__(self, repo_path="."):
        self.repo_path = Path(repo_path).resolve()
        
        # Files explicitly excluded by .gitattributes export-ignore
        self.gitattributes_excludes = [
            "PROJECT_COMPLETE.md",
            "PROJECT_STRUCTURE.md", 
            "SECURITY_REMEDIATION_SUMMARY.md",
            "SECURITY_CONFIG.md",
            "test_*.py",
            "*_test.py",
            "demo*.py",
            "demo*.json",
            "test_installation.py",
            "test_security_fixes.py",
            "pytest.ini",
            "security_scan_*.json",
            "bandit_*.json",
            "*_scan_results_*.json",
            "logs/",
            "reports/",
            "*.log",
            ".venv/",
            "venv/",
            ".vscode/",
            ".idea/",
            ".DS_Store",
            "Thumbs.db",
            "desktop.ini"
        ]
        
        # Patterns from .gitignore for releases
        self.gitignore_patterns = [
            "__pycache__/",
            "*.pyc",
            "*.pyo", 
            "*$py.class",
            "build/",
            "dist/",
            "*.egg-info/",
            ".eggs/",
            "*.tmp",
            "*.temp",
            ".pytest_cache/",
            ".coverage",
            "htmlcov/",
            ".mypy_cache/",
            "*.bak",
            "*.backup",
            "cache/",
            ".cache/",
            "*.sample",
            "*.example",
            "sample_*",
            "example_*"
        ]

    def should_exclude(self, file_path):
        """Check if a file should be excluded from releases"""
        rel_path = file_path.relative_to(self.repo_path)
        path_str = str(rel_path)
        
        # Check gitattributes excludes
        for pattern in self.gitattributes_excludes:
            if fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(file_path.name, pattern):
                return True, f"gitattributes export-ignore: {pattern}"
        
        # Check gitignore patterns
        for pattern in self.gitignore_patterns:
            if fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(file_path.name, pattern):
                return True, f"gitignore pattern: {pattern}"
                
        # Check directory patterns
        for part in rel_path.parts:
            if part in ['__pycache__', '.pytest_cache', '.vscode', '.idea', 'logs', 'reports', '.venv', 'venv']:
                return True, f"excluded directory: {part}"
        
        return False, ""

    def analyze_repository(self):
        """Analyze what files will be included/excluded"""
        included_files = []
        excluded_files = []
        
        for file_path in self.repo_path.rglob("*"):
            if file_path.is_file():
                # Skip .git directory
                if '.git' in file_path.parts:
                    continue
                    
                excluded, reason = self.should_exclude(file_path)
                if excluded:
                    excluded_files.append((file_path, reason))
                else:
                    included_files.append(file_path)
        
        return included_files, excluded_files

    def print_analysis(self):
        """Print the release content analysis"""
        included, excluded = self.analyze_repository()
        
        print("🚀 NSAF Release Content Analysis")
        print("=" * 50)
        
        print(f"\n✅ Files INCLUDED in releases ({len(included)} files):")
        print("-" * 30)
        for file_path in sorted(included):
            rel_path = file_path.relative_to(self.repo_path)
            print(f"  ✓ {rel_path}")
        
        print(f"\n❌ Files EXCLUDED from releases ({len(excluded)} files):")
        print("-" * 30)
        excluded_by_category = {}
        for file_path, reason in excluded:
            rel_path = file_path.relative_to(self.repo_path)
            category = reason.split(":")[0]
            if category not in excluded_by_category:
                excluded_by_category[category] = []
            excluded_by_category[category].append((rel_path, reason))
        
        for category, files in excluded_by_category.items():
            print(f"\n  📁 {category.upper()}:")
            for rel_path, reason in sorted(files):
                print(f"    ✗ {rel_path} ({reason})")
        
        print(f"\n📊 Summary:")
        print(f"  • Total files analyzed: {len(included) + len(excluded)}")
        print(f"  • Files included in release: {len(included)}")
        print(f"  • Files excluded from release: {len(excluded)}")
        print(f"  • Exclusion rate: {(len(excluded)/(len(included)+len(excluded))*100):.1f}%")
        
        print(f"\n🎯 Release Package Contents:")
        print("  The release will contain only production-ready files:")
        print("  • Core nsaf package modules")
        print("  • Essential documentation (README, LICENSE, etc.)")
        print("  • User-facing examples and templates")
        print("  • Installation and configuration files")
        print("  • NO development, test, or summary files")

def main():
    validator = ReleaseValidator()
    validator.print_analysis()

if __name__ == "__main__":
    main()
