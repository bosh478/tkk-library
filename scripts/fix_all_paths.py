#!/usr/bin/env python3
"""Fix all paths in GuideCase files - normalize ALL slashes to forward slashes"""
from pathlib import Path

VAULT = Path("D:/AI agent/tkk-library")
TARGET_DIR = VAULT / "wiki/syntheses"

def fix_paths():
    count = 0
    for f in TARGET_DIR.glob("GuideCase_*.md"):
        try:
            content = f.read_text(encoding='utf-8')
            original = content

            # Replace ALL backslashes with forward slashes in the entire file
            content = content.replace('\\', '/')

            if content != original:
                f.write_text(content, encoding='utf-8')
                count += 1
        except Exception as e:
            print(f"Error: {f.name}: {e}")
    print(f"Fixed {count} files")

if __name__ == "__main__":
    fix_paths()
