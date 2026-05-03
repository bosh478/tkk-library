#!/usr/bin/env python3
"""直接处理已知L5断链的修复脚本"""
import sys
import os
from pathlib import Path
import re

if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

WIKI_ROOT = Path("D:/AI agent/tkk-library/wiki")

# 手动定义已知的断链映射（从 retro_check_D6_index.py 输出整理）
KNOWN_FIXES = {
    # 公诉人出庭指南系列
    "公诉人出庭指南_第一编_公诉人出庭概述": "公诉人出庭概述",
    "公诉人出庭指南_第二编_出庭规范及程序问题应对": "公诉人出庭指南_第二编_出庭规范及程序问题应对",
    "公诉人出庭指南_第三编_常见罪名问题应对": "公诉人出庭指南_第三编_常见罪名问题应对",
    "公诉人出庭指南_第四编_庭审应对": "公诉人出庭指南_第四编_庭审应对",
    # 刑法释义书籍 - 这些书存在于concepts但wikilink格式不匹配
    "2024《刑法释义》王爱立 法律 2024年": "2024《刑法释义》王爱立 法律 2024年",
    "2024《刑法罪名精释》下 胡云腾 人民法院 2024年": "2024《刑法罪名精释》下 胡云腾 人民法院 2024年",
    "202507《刑事审判指导案例归类集成》法律出版社 2025年": "202507《刑事审判指导案例归类集成》法律出版社 2025年",
}

# 策略：提取关键词在 title_map 中查找
def build_title_map():
    title_map = {}
    for subdir in ["concepts", "entities", "summaries", "syntheses"]:
        dir_path = WIKI_ROOT / subdir
        if not dir_path.exists():
            continue
        for filepath in dir_path.glob("*.md"):
            try:
                content = filepath.read_text(encoding="utf-8")
            except:
                continue
            title_match = re.search(r'^---\n.*?title:\s*"?(.+?)"?\n', content, re.DOTALL)
            if title_match:
                title_map[title_match.group(1)] = filepath
    return title_map

def fix_file(filepath: Path, title_map: dict) -> int:
    try:
        content = filepath.read_text(encoding="utf-8")
    except:
        return 0

    original = content
    fixed = 0

    def replace_link(match):
        nonlocal fixed
        link = match.group(1)

        # 跳过已有链接
        if link.startswith("#") or "://" in link:
            return match.group(0)

        if link in title_map:
            return match.group(0)

        # 尝试匹配
        new_link = None

        # 策略1：精确后缀匹配（书名号链接匹配概念标题）
        for title in title_map:
            if title in link or link in title:
                new_link = title
                break

        # 策略2：主要关键词匹配（用于公诉人出庭指南等）
        if not new_link:
            keywords = [k for k in re.findall(r'[一-鿿]{2,}', link)]
            if keywords:
                for title in title_map:
                    # 检查最后一个关键词是否在title中
                    if keywords[-1] in title:
                        new_link = title
                        break

        if new_link and new_link != link:
            fixed += 1
            return f"[[{new_link}]]"
        elif new_link == link:
            fixed += 1
            return link
        else:
            # 无法修复，转为纯文本
            fixed += 1
            return link

    content = re.sub(r'\[\[([^\]]+)\]\]', replace_link, content)

    if content != original:
        try:
            filepath.write_text(content, encoding="utf-8")
        except:
            return 0

    return fixed

def main():
    title_map = build_title_map()
    print(f"title_map size: {len(title_map)}\n")

    total = 0
    for subdir in ["concepts", "entities", "summaries", "syntheses"]:
        dir_path = WIKI_ROOT / subdir
        if not dir_path.exists():
            continue
        subdir_fixed = 0
        for filepath in dir_path.glob("*.md"):
            f = fix_file(filepath, title_map)
            if f > 0:
                subdir_fixed += f
        print(f"  {subdir}: {subdir_fixed} fixes")
        total += subdir_fixed

    print(f"\nTotal: {total} links processed")

if __name__ == "__main__":
    main()