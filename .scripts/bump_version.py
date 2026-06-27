#!/usr/bin/env python3
import sys
import os
import json
import re
import argparse
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description="Bump version in package.json and update CHANGELOG.md")
    parser.add_argument("bump_type", choices=["major", "minor", "patch", "current"], help="Type of version bump or current to update changelog only")
    parser.add_argument("--version", help="Directly set the target version")
    parser.add_argument("--message", "-m", help="Custom changelog release message")
    return parser.parse_args()

def increment_version(version_str, bump_type):
    parts = version_str.split('.')
    if len(parts) != 3:
        return version_str
    
    major, minor, patch = map(int, parts)
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
        
    return f"{major}.{minor}.{patch}"

def main():
    args = parse_args()
    
    pkg_path = "package.json"
    if not os.path.exists(pkg_path):
        print(f"Error: {pkg_path} not found.")
        sys.exit(1)
        
    with open(pkg_path, "r", encoding="utf-8") as f:
        pkg_data = json.load(f)
        
    current_version = pkg_data.get("version", "1.0.0")
    
    if args.version:
        new_version = args.version
    elif args.bump_type == "current":
        new_version = current_version
    else:
        new_version = increment_version(current_version, args.bump_type)
        
    print(f"Bumping version from {current_version} to {new_version}")
    
    # Save package.json
    pkg_data["version"] = new_version
    with open(pkg_path, "w", encoding="utf-8") as f:
        json.dump(pkg_data, f, indent=2)
        f.write("\n")
        
    # Update CHANGELOG.md
    changelog_path = "CHANGELOG.md"
    today = datetime.now().strftime("%Y-%m-%d")
    release_notes = args.message or "Release updates."
    
    new_entry = f"## [{new_version}] - {today}\n\n"
    if args.message:
        # If multiline, indent or format properly
        new_entry += f"{release_notes.strip()}\n\n"
    else:
        new_entry += f"- Minor bug fixes and improvements.\n\n"
        
    if os.path.exists(changelog_path):
        with open(changelog_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        if f"## [{new_version}]" in content:
            print(f"Changelog already contains an entry for version {new_version}. Skipping changelog update.")
        else:
            # Prepend under the first main title or at the top
            title_pattern = r"^(# Changelog\n*)"
            match = re.search(title_pattern, content, re.IGNORECASE)
            if match:
                inserted_content = content[:match.end()] + new_entry + content[match.end():]
            else:
                inserted_content = f"# Changelog\n\n{new_entry}{content}"
                
            with open(changelog_path, "w", encoding="utf-8") as f:
                f.write(inserted_content)
    else:
        # Create new changelog
        with open(changelog_path, "w", encoding="utf-8") as f:
            f.write(f"# Changelog\n\n{new_entry}")
            
    print("Version bump and changelog update complete.")

if __name__ == "__main__":
    main()
