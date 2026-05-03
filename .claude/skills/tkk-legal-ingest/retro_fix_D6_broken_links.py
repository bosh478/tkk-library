#!/usr/bin/env python3
"""
retro_fix_D6_broken_links.py
修复 D6 断链问题：将失效的 [[wikilink]] 转为纯文本
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

def build_target_set() -> set:
    """构建所有有效的页面标题集合"""
    targets = set()
    for subdir in ["concepts", "entities", "summaries", "syntheses"]:
        dir_path = WIKI_ROOT / subdir
        if not dir_path.exists():
            continue
        for filepath in dir_path.glob("*.md"):
            try:
                content = filepath.read_text(encoding="utf-8")
            except:
                continue
            # 从 frontmatter 提取 title
            title_match = re.search(r'^---\n.*?title:\s*"?(.+?)"?\n', content, re.DOTALL)
            if title_match:
                targets.add(title_match.group(1))
            # 也添加文件名（去掉前缀和扩展名）
            name = filepath.stem
            for prefix in ["concept_", "entity_", "synthesis_", "summary_"]:
                if name.startswith(prefix):
                    name = name[len(prefix):]
                    break
            targets.add(name)
    return targets

def fix_file(filepath: Path, targets: set) -> int:
    """修复文件中的断链，返回修复数量"""
    try:
        content = filepath.read_text(encoding="utf-8")
    except:
        return 0

    original = content
    fixed_count = 0

    # 找到所有 wikilink
    def replace_wikilink(match):
        nonlocal fixed_count
        link = match.group(1)
        # 跳过头部锚点
        if link.startswith("#") or "://" in link or link.startswith("http"):
            return match.group(0)
        # 检查链接目标是否存在
        if link not in targets:
            fixed_count += 1
            return link  # 转为纯文本
        return match.group(0)

    content = re.sub(r'\[\[([^\]]+)\]\]', replace_wikilink, content)

    if content != original:
        try:
            filepath.write_text(content, encoding="utf-8")
        except:
            return 0

    return fixed_count

def main():
    print("正在构建目标页面集合...")
    targets = build_target_set()
    print(f"找到 {len(targets)} 个有效页面\n")

    total_fixed = 0

    for subdir in ["concepts", "entities", "summaries", "syntheses"]:
        dir_path = WIKI_ROOT / subdir
        if not dir_path.exists():
            continue
        subdir_fixed = 0
        for filepath in dir_path.glob("*.md"):
            fixed = fix_file(filepath, targets)
            if fixed > 0:
                subdir_fixed += fixed
        print(f"  {subdir}: 修复 {subdir_fixed} 处断链")
        total_fixed += subdir_fixed

    print(f"\n=== D6 断链修复报告 ===")
    print(f"总计修复: {total_fixed} 处断链")

if __name__ == "__main__":
    main()
