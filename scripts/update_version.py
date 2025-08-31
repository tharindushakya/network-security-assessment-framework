#!/usr/bin/env python3
"""
Version updater script for NSAF setup.py
Safely updates the version string in setup.py
"""

import re
import sys
from pathlib import Path


def update_version(setup_file: str, new_version: str) -> bool:
    """
    Update the version in setup.py file.
    
    Args:
        setup_file: Path to setup.py file
        new_version: New version string
    
    Returns:
        True if successful, False otherwise
    """
    try:
        setup_path = Path(setup_file)
        if not setup_path.exists():
            print(f"Error: {setup_file} not found")
            return False
        
        # Read the current content
        content = setup_path.read_text(encoding='utf-8')
        
        # Update version using regex
        version_pattern = r'version\s*=\s*["\'][^"\']*["\']'
        new_version_string = f'version="{new_version}"'
        
        # Check if version exists
        if not re.search(version_pattern, content):
            print(f"Error: version field not found in {setup_file}")
            return False
        
        # Replace version
        updated_content = re.sub(version_pattern, new_version_string, content)
        
        # Write back to file
        setup_path.write_text(updated_content, encoding='utf-8')
        
        print(f"Successfully updated version to {new_version}")
        return True
        
    except Exception as e:
        print(f"Error updating version: {e}")
        return False


def get_current_version(setup_file: str) -> str:
    """Get current version from setup.py"""
    try:
        setup_path = Path(setup_file)
        content = setup_path.read_text(encoding='utf-8')
        
        match = re.search(r'version\s*=\s*["\']([^"\']*)["\']', content)
        if match:
            return match.group(1)
        return "unknown"
    except Exception:
        return "unknown"


def main():
    """Main function"""
    if len(sys.argv) != 3:
        print("Usage: python update_version.py <setup.py> <new_version>")
        print("Example: python update_version.py setup.py 1.2.3")
        sys.exit(1)
    
    setup_file = sys.argv[1]
    new_version = sys.argv[2]
    
    # Validate version format (basic)
    if not re.match(r'^\d+\.\d+\.\d+', new_version):
        print(f"Warning: Version '{new_version}' doesn't follow semantic versioning")
    
    # Show current version
    current_version = get_current_version(setup_file)
    print(f"Current version: {current_version}")
    print(f"New version: {new_version}")
    
    # Update version
    if update_version(setup_file, new_version):
        print("Version update completed successfully!")
        sys.exit(0)
    else:
        print("Version update failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
