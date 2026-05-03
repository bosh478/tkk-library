#!/usr/bin/env python3
"""
retro_fix_D5_naming.py
修复 D5 命名规范问题：统一前缀格式
"""
import sys
import os
from pathlib import Path
import re
# Force UTF-8 mode on Windows
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

WIKI_ROOT = Path("D:/AI agent/tkk-library/wiki")

def fix_file(filepath: Path, subdir: str) -> bool:
    """修复命名，返回是否修改"""
    expected_prefix = {
        "concepts": "concept_",
        "entities": "entity_",
        "summaries": "summary_",
        "syntheses": "synthesis_"
    }.get(subdir, "")

    if not expected_prefix:
        return False

    # 检查是否需要修复
    if filepath.name.startswith(expected_prefix):
        return False

    # 新文件名
    new_name = expected_prefix + filepath.name
    new_path = filepath.parent / new_name

    # 如果目标文件已存在，跳过
    if new_path.exists():
        return False

    try:
        filepath.rename(new_path)
        return True
    except:
        return False

def main():
    fixed = 0
    skipped = 0
    errors = 0

    for subdir in ["concepts", "entities", "summaries", "syntheses"]:
        dir_path = WIKI_ROOT / subdir
        if not dir_path.exists():
            continue

        expected_prefix = {
            "concepts": "concept_",
            "entities": "entity_",
            "summaries": "summary_",
            "syntheses": "synthesis_"
        }.get(subdir, "")

        for filepath in list(dir_path.glob("*.md")):
            if filepath.name.startswith(expected_prefix):
                skipped += 1
                continue

            result = fix_file(filepath, subdir)
            if result:
                fixed += 1
                print(f"  [+] {subdir}/{filepath.name} -> {filepath.parent / (expected_prefix + filepath.name)}")
            else:
                errors += 1

    print(f"\n=== D5 命名修复报告 ===")
    print(f"已修复: {fixed} 个")
    print(f"跳过: {skipped} 个")
    print(f"错误: {errors} 个")

if __name__ == "__main__":
    main()
