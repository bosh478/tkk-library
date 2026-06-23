#!/usr/bin/env python3
"""Fix source paths in GuideCase files - normalize slashes"""
from pathlib import Path

VAULT = Path("D:/AI agent/tkk-library")
TARGET_DIR = VAULT / "wiki/syntheses"

def fix_paths():
    count = 0
    for f in TARGET_DIR.glob("GuideCase_*.md"):
        try:
            content = f.read_text(encoding='utf-8')
            original = content

            # Fix source paths: normalize to forward slashes
            # Pattern: sources\2-案例库\公报案例\民事/... -> sources/2-案例库/公报案例/民事/...
            import re
            content = re.sub(r'source:\s*"sources[/\\]', 'source: "sources/', content)

            if content != original:
                f.write_text(content, encoding='utf-8')
                count += 1
        except Exception as e:
            print(f"Error: {f.name}: {e}")
    print(f"Fixed {count} files")

if __name__ == "__main__":
    fix_paths()
