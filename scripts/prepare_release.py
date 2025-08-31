#!/usr/bin/env python3
"""
Release preparation script for NSAF
Cleans up development files and prepares the repository for release
"""

import os
import shutil
import glob
import argparse
from pathlib import Path

class ReleasePrep:
    def __init__(self, repo_path="."):
        self.repo_path = Path(repo_path).resolve()
        self.backup_dir = self.repo_path / ".release_backup"
        
    def create_backup(self):
        """Create backup of files that will be removed"""
        if self.backup_dir.exists():
            shutil.rmtree(self.backup_dir)
        self.backup_dir.mkdir()
        print(f"Created backup directory: {self.backup_dir}")

    def backup_file(self, file_path):
        """Backup a single file"""
        if file_path.exists():
            backup_path = self.backup_dir / file_path.name
            shutil.copy2(file_path, backup_path)
            print(f"Backed up: {file_path.name}")

    def remove_summary_files(self):
        """Remove project summary and analysis files"""
        summary_files = [
            "PROJECT_COMPLETE.md",
            "PROJECT_STRUCTURE.md", 
            "SECURITY_REMEDIATION_SUMMARY.md",
            "SECURITY_CONFIG.md"
        ]
        
        print("\n📄 Removing summary files:")
        for file_name in summary_files:
            file_path = self.repo_path / file_name
            if file_path.exists():
                self.backup_file(file_path)
                file_path.unlink()
                print(f"Removed: {file_name}")

    def remove_test_files(self):
        """Remove test and demo files"""
        print("\n🧪 Removing test and demo files:")
        
        # Test files
        test_patterns = [
            "test_*.py",
            "*_test.py", 
            "demo*.py",
            "test_installation.py",
            "test_security_fixes.py"
        ]
        
        for pattern in test_patterns:
            for file_path in self.repo_path.glob(pattern):
                self.backup_file(file_path)
                file_path.unlink()
                print(f"Removed: {file_path.name}")

        # Test configuration
        pytest_ini = self.repo_path / "pytest.ini"
        if pytest_ini.exists():
            self.backup_file(pytest_ini)
            pytest_ini.unlink()
            print("Removed: pytest.ini")

    def remove_scan_results(self):
        """Remove security scan results and demo outputs"""
        print("\n🔍 Removing scan results and demo outputs:")
        
        scan_patterns = [
            "security_scan_*.json",
            "bandit_*.json",
            "*_scan_results_*.json",
            "demo*_results_*.json",
            "*_results_*.json"
        ]
        
        for pattern in scan_patterns:
            for file_path in self.repo_path.glob(pattern):
                self.backup_file(file_path)
                file_path.unlink()
                print(f"Removed: {file_path.name}")

    def remove_dev_artifacts(self):
        """Remove development artifacts and temporary files"""
        print("\n🛠️ Removing development artifacts:")
        
        # Remove cache directories
        cache_dirs = [
            "__pycache__",
            ".pytest_cache",
            ".coverage",
            "htmlcov",
            ".mypy_cache"
        ]
        
        for cache_dir in cache_dirs:
            for dir_path in self.repo_path.rglob(cache_dir):
                if dir_path.is_dir():
                    shutil.rmtree(dir_path)
                    print(f"Removed directory: {dir_path}")

        # Remove temporary files
        temp_patterns = [
            "*.pyc",
            "*.pyo", 
            "*.log",
            "*.tmp",
            "*.temp"
        ]
        
        for pattern in temp_patterns:
            for file_path in self.repo_path.rglob(pattern):
                if file_path.is_file():
                    file_path.unlink()
                    print(f"Removed: {file_path}")

    def clean_empty_dirs(self):
        """Remove empty directories"""
        print("\n📁 Cleaning empty directories:")
        
        for dir_path in sorted(self.repo_path.rglob("*"), reverse=True):
            if dir_path.is_dir() and not any(dir_path.iterdir()):
                # Don't remove git or important directories
                if not any(part.startswith('.git') for part in dir_path.parts):
                    if dir_path.name not in ['nsaf', 'tests', 'docs', 'examples']:
                        dir_path.rmdir()
                        print(f"Removed empty directory: {dir_path}")

    def prepare_release(self, version=None):
        """Main release preparation process"""
        print("🚀 Preparing NSAF for release...")
        print(f"Repository path: {self.repo_path}")
        
        if version:
            print(f"Target version: {version}")
        
        self.create_backup()
        self.remove_summary_files()
        self.remove_test_files()
        self.remove_scan_results()
        self.remove_dev_artifacts()
        self.clean_empty_dirs()
        
        print("\n✅ Release preparation complete!")
        print(f"Backup created at: {self.backup_dir}")
        print("\nNext steps:")
        print("1. Review the changes")
        print("2. Run tests to ensure functionality")
        print("3. Create release tag and package")
        print("4. Restore files from backup if needed")

    def restore_backup(self):
        """Restore files from backup"""
        if not self.backup_dir.exists():
            print("No backup found to restore")
            return
            
        print("🔄 Restoring files from backup...")
        for backup_file in self.backup_dir.iterdir():
            if backup_file.is_file():
                restore_path = self.repo_path / backup_file.name
                shutil.copy2(backup_file, restore_path)
                print(f"Restored: {backup_file.name}")
        
        print("✅ Files restored from backup")

def main():
    parser = argparse.ArgumentParser(description="Prepare NSAF repository for release")
    parser.add_argument("--version", help="Target release version")
    parser.add_argument("--restore", action="store_true", help="Restore files from backup")
    parser.add_argument("--repo-path", default=".", help="Path to repository (default: current directory)")
    
    args = parser.parse_args()
    
    prep = ReleasePrep(args.repo_path)
    
    if args.restore:
        prep.restore_backup()
    else:
        prep.prepare_release(args.version)

if __name__ == "__main__":
    main()
