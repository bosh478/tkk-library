#!/usr/bin/env python3
"""
Fix SPP Q&A wiki files - correct title duplication and source bracket issues
"""
import os
import re
from pathlib import Path

# VAULT_ROOT 多平台兼容（patched 2026-06-23）：
# 1. 优先 TKK_VAULT_ROOT 环境变量
# 2. Windows: "D:/AI agent/tkk-library"
# 3. Linux/WSL: /home/kangkang/tkk-library 等候选按存在性自动探测
_VAULT_CANDIDATES = [
    os.environ.get("TKK_VAULT_ROOT"),
    "D:/AI agent/tkk-library" if os.name == "nt" else None,
    "/home/kangkang/tkk-library",
    "/mnt/d/AI agent/tkk-library",
    "/mnt/c/Users/汤康康/tkk-library",
]
VAULT_ROOT = next(
    (Path(p) for p in _VAULT_CANDIDATES if p and Path(p).exists()),
    Path(os.environ.get("TKK_VAULT_ROOT", "D:/AI agent/tkk-library"))
)
TARGET_DIR = VAULT_ROOT / "wiki/summaries"

def fix_file(filepath):
    """Fix title duplication and source bracket issues in a single file"""
    content = filepath.read_text(encoding='utf-8')

    # Fix 1: Remove duplicate "最高检" prefix in title
    # Pattern: "最高检最高检" -> "最高检"
    content = content.replace('title: "最高检最高检', 'title: "最高检')

    # Fix 2: Fix triple brackets in source and table
    # Pattern: "[[[filename.md]]]" -> "[[filename.md]]"
    content = content.replace('[[[', '[[')
    content = content.replace(']]]', ']]')

    # Write back
    filepath.write_text(content, encoding='utf-8')
    return True

def main():
    files = list(TARGET_DIR.glob("summary_SPP_答记者问_*.md"))
    print(f"Total files to fix: {len(files)}")

    fixed = 0
    for f in files:
        try:
            fix_file(f)
            fixed += 1
        except Exception as e:
            print(f"Error fixing {f.name}: {e}")

    print(f"Fixed {fixed} files")

if __name__ == "__main__":
    main()