#!/usr/bin/env python3
"""Fix GuideCase files with invalid title (':') by extracting case number as title"""
import re
from pathlib import Path

VAULT = Path("D:/AI agent/tkk-library")
TARGET_DIR = VAULT / "wiki/syntheses"
SOURCE_DIR = VAULT / "sources/2-案例库/公报案例"

def fix_title(fpath):
    """Fix title by extracting case number from filename or source"""
    try:
        content = fpath.read_text(encoding='utf-8')

        # Check if title is just ':'
        if not re.search(r'^title:\s*：\s*$', content, re.MULTILINE):
            return False

        # Extract case number from filename
        # GuideCase_(2015)民申字第1070号.md -> (2015)民申字第1070号
        fname = fpath.stem  # e.g., GuideCase_(2015)民申字第1070号
        case_num = fname.replace('GuideCase_', '')

        # Try to get better title from source file
        source_match = re.search(r'source:\s*"([^"]+)"', content)
        if source_match:
            src_path = VAULT / source_match.group(1).replace('/', '\\')
            if not src_path.exists():
                src_path = Path(str(src_path).replace('\\\\', '/'))
            if src_path.exists():
                src_content = src_path.read_text(encoding='utf-8')
                # Extract case number from first line
                first_line_match = re.search(r'^#\s*(.+)', src_content)
                if first_line_match:
                    title = first_line_match.group(1).strip()
                    # Remove case number prefix if present
                    title = re.sub(r'^[（(][^）)]*[）)]\s*', '', title)
                    if title and title != '：':
                        # Fix the content
                        content = re.sub(r'^title:\s*：\s*$', f'title: {title}', content, flags=re.MULTILINE)
                        # Also fix 问题意识 if it's just '：'
                        content = re.sub(r'^问题意识:\s*：\s*$', f'问题意识: {title}', content, flags=re.MULTILINE)
                        fpath.write_text(content, encoding='utf-8')
                        return True

        # Fallback: use case number as title
        if case_num:
            content = re.sub(r'^title:\s*：\s*$', f'title: {case_num}', content, flags=re.MULTILINE)
            content = re.sub(r'^问题意识:\s*：\s*$', f'问题意识: {case_num}', content, flags=re.MULTILINE)
            fpath.write_text(content, encoding='utf-8')
            return True

        return False
    except Exception as e:
        print(f"Error fixing {fpath.name}: {e}")
        return False

def main():
    fixed = 0
    for f in TARGET_DIR.glob("GuideCase_*.md"):
        if fix_title(f):
            fixed += 1
            print(f"Fixed: {f.name}")
    print(f"\nTotal fixed: {fixed}")

if __name__ == "__main__":
    main()
