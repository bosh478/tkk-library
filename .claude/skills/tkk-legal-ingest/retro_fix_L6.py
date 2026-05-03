#!/usr/bin/env python3
"""
retro_fix_L6.py
修复 L6 风格问题：添加 FAQ 和 ## 相关 区域
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

FAQ_TEMPLATE = """
## ❓ 常见问题

> 问：本页涉及的核心问题是什么？
> 答：（待补充）

> 问：实践中应注意哪些要点？
> 答：（待补充）
"""

RELATED_TEMPLATE = """
## 相关

（相关页面链接待补充）
"""

def fix_summaries_faq(filepath: Path) -> bool:
    """为 summaries 添加 FAQ"""
    try:
        content = filepath.read_text(encoding="utf-8")
    except:
        return False

    if "## ❓ 常见问题" in content:
        return False

    # 在文档概览后添加 FAQ
    if "## 📋 文档概览" in content:
        content = content.replace("## 📋 文档概览", "## 📋 文档概览\n\n## ❓ 常见问题\n\n> 问：本页涉及的核心问题是什么？\n> 答：（待补充）\n\n> 问：实践中应注意哪些要点？\n> 答：（待补充）")
    elif "## " in content:
        # 在第一个 ## 标题后添加
        match = re.search(r'(## [^\n]+\n)', content)
        if match:
            pos = match.end()
            content = content[:pos] + "\n## ❓ 常见问题\n\n> 问：本页涉及的核心问题是什么？\n> 答：（待补充）\n\n> 问：实践中应注意哪些要点？\n> 答：（待补充）" + content[pos:]

    try:
        filepath.write_text(content, encoding="utf-8")
        return True
    except:
        return False

def fix_concepts_related(filepath: Path) -> bool:
    """为 concepts 添加 ## 相关 区域"""
    try:
        content = filepath.read_text(encoding="utf-8")
    except:
        return False

    if "## 相关" in content:
        return False

    content += "\n## 相关\n\n（相关法条和概念待补充）\n"

    try:
        filepath.write_text(content, encoding="utf-8")
        return True
    except:
        return False

def main():
    summaries_fixed = 0
    concepts_fixed = 0

    # 处理 summaries
    summaries_dir = WIKI_ROOT / "summaries"
    if summaries_dir.exists():
        for filepath in summaries_dir.glob("*.md"):
            if fix_summaries_faq(filepath):
                summaries_fixed += 1

    # 处理 concepts
    concepts_dir = WIKI_ROOT / "concepts"
    if concepts_dir.exists():
        for filepath in concepts_dir.glob("*.md"):
            if fix_concepts_related(filepath):
                concepts_fixed += 1

    print(f"=== L6 风格修复报告 ===")
    print(f"summaries 添加 FAQ: {summaries_fixed} 个")
    print(f"concepts 添加 ## 相关: {concepts_fixed} 个")

if __name__ == "__main__":
    main()
