#!/usr/bin/env python3
"""
retro_fix_L5_smart.py
智能修复 L5 断链问题
"""
import sys
import os
from pathlib import Path
import re
from datetime import datetime

if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

WIKI_ROOT = Path("D:/AI agent/tkk-library/wiki")

def build_target_map() -> dict:
    """构建所有有效的页面标题 -> 文件路径 映射"""
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
            name = filepath.stem
            for prefix in ["concept_", "entity_", "synthesis_", "summary_"]:
                if name.startswith(prefix):
                    name = name[len(prefix):]
                    break
            title_map[name] = filepath
    return title_map

def smart_fix_file(filepath: Path, title_map: dict) -> int:
    """智能修复文件中的断链"""
    try:
        content = filepath.read_text(encoding="utf-8")
    except:
        return 0

    original = content
    fixed_count = 0

    def replace_wikilink(match):
        nonlocal fixed_count
        link = match.group(1)

        if link.startswith("#") or "://" in link or link.startswith("http"):
            return match.group(0)

        if link in title_map:
            return match.group(0)

        # 智能修复策略
        new_link = None

        # 策略1: 去除书名号
        link_no_brackets = link.replace('《', '').replace('》', '')
        if link_no_brackets in title_map:
            new_link = link_no_brackets

        # 策略2: 尝试模糊匹配 - 链接是否包含标题，或标题包含链接
        if not new_link:
            for title in title_map:
                if title in link or link in title:
                    new_link = title
                    break

        # 策略3: 关键词包含匹配（至少2个关键词都在）
        if not new_link:
            keywords = [k for k in re.findall(r'[一-鿿]+', link) if len(k) >= 2]
            for title in title_map:
                if len(keywords) >= 2 and all(kw in title for kw in keywords[-3:]):
                    new_link = title
                    break

        # 策略4: 司法解释全书系列 - 不存在，跳过
        if not new_link and '司法解释全书' in link:
            new_link = link  # 转为纯文本

        # 策略5: 刑法分则章节引用书籍 - 书籍存在但章节不存在于wiki
        if not new_link and ('《刑法释义》' in link or '《刑法罪名精释》' in link):
            new_link = link  # 转为纯文本

        if new_link and new_link != link:
            fixed_count += 1
            return f"[[{new_link}]]"
        elif new_link == link:
            fixed_count += 1
            return link  # 转为纯文本

        return match.group(0)

        return match.group(0)

    content = re.sub(r'\[\[([^\]]+)\]\]', replace_wikilink, content)

    if content != original:
        try:
            filepath.write_text(content, encoding="utf-8")
        except:
            return 0

    return fixed_count

def main():
    print("正在构建目标页面映射...")
    title_map = build_target_map()
    print(f"找到 {len(title_map)} 个有效页面\n")

    total_fixed = 0
    for subdir in ["concepts", "entities", "summaries", "syntheses"]:
        dir_path = WIKI_ROOT / subdir
        if not dir_path.exists():
            continue
        subdir_fixed = 0
        for filepath in dir_path.glob("*.md"):
            fixed = smart_fix_file(filepath, title_map)
            if fixed > 0:
                subdir_fixed += fixed
        print(f"  {subdir}: 修复 {subdir_fixed} 处")
        total_fixed += subdir_fixed

    print(f"\n=== L5 智能修复完成 ===")
    print(f"总计修复: {total_fixed} 处")

if __name__ == "__main__":
    main()