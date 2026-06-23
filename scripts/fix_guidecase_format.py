#!/usr/bin/env python3
"""
Fix GuideCase file format issues:
1. Remove '#' prefix from title
2. Fix source path to relative path (sources/...)
3. Remove乱码 characters from tags
"""
import re
from pathlib import Path

VAULT = Path("D:/AI agent/tkk-library")
TARGET_DIR = VAULT / "wiki/syntheses"

def fix_file(filepath):
    """Fix format issues in a GuideCase file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # 1. Fix title: remove '# ' prefix
        content = re.sub(r'^title:\s*#\s+(.+)$', r'title: \1', content, flags=re.MULTILINE)

        # 2. Fix source path: D:\AI agent\tkk-library\sources\... -> sources/...
        content = re.sub(
            r'source:\s*"D:\\AI agent\\tkk-library\\',
            'source: "',
            content
        )
        content = re.sub(
            r'source:\s*"D:/AI agent/tkk-library/',
            'source: "',
            content
        )
        # 将反斜杠替换为正斜杠
        content = re.sub(
            r'(source:\s*"[^"]*)\\([^"]*")',
            r'\1/\2',
            content
        )

        # 3. Fix tags: remove \x07 and other乱码
        content = re.sub(r"\\x07|\\x[0-9a-f]{2}", "", content)
        content = content.replace('\x07', '')

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

def main():
    files = list(TARGET_DIR.glob("GuideCase_*.md"))
    fixed = 0
    for f in files:
        if fix_file(f):
            fixed += 1
            print(f"Fixed: {f.name}")
    print(f"\nTotal fixed: {fixed}/{len(files)}")

if __name__ == "__main__":
    main()
