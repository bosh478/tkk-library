#!/usr/bin/env python3
"""
retro_fix_L3_updated.py
修复 L3 updated 字段缺失问题
"""
import sys
import os
from pathlib import Path
import re
from datetime import datetime
# Force UTF-8 mode on Windows
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

WIKI_ROOT = Path("D:/AI agent/tkk-library/wiki")
TODAY = datetime.now().strftime("%Y-%m-%d")

def fix_file(filepath: Path) -> bool:
    """修复 updated 字段"""
    try:
        content = filepath.read_text(encoding="utf-8")
    except:
        return False

    if "updated:" in content:
        return False

    # 添加 updated 字段
    lines = content.split("\n")
    new_lines = []
    updated_added = False
    for line in lines:
        new_lines.append(line)
        if not updated_added and line.startswith("created:"):
            new_lines.append(f"updated: {TODAY}")
            updated_added = True

    if updated_added:
        new_content = "\n".join(new_lines)
        try:
            filepath.write_text(new_content, encoding="utf-8")
            return True
        except:
            return False
    return False

def main():
    fixed = 0
    for subdir in ["concepts", "entities", "summaries", "syntheses"]:
        dir_path = WIKI_ROOT / subdir
        if not dir_path.exists():
            continue
        for filepath in dir_path.glob("*.md"):
            if fix_file(filepath):
                fixed += 1

    print(f"已修复 {fixed} 个文件的 updated 字段")

if __name__ == "__main__":
    main()
