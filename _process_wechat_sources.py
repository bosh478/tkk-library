#!/usr/bin/env python3
"""
处理 sources/微信公号资料/ 下的四类文件，生成 wiki summaries
"""
import os
import re
import json
from pathlib import Path

VAULT_ROOT = Path("D:/AI agent/tkk-library")
SOURCES_DIR = VAULT_ROOT / "sources" / "微信公号资料"
SUMMARIES_DIR = VAULT_ROOT / "wiki" / "summaries"

def extract_frontmatter(content):
    """从markdown内容提取frontmatter"""
    lines = content.split('\n')
    frontmatter = {}
    in_frontmatter = False
    content_start = 0

    for i, line in enumerate(lines):
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
            else:
                content_start = i + 1
                break
        elif in_frontmatter and ':' in line:
            key, val = line.split(':', 1)
            frontmatter[key.strip()] = val.strip().strip('"').strip("'")

    body = '\n'.join(lines[content_start:])
    return frontmatter, body

def extract_title(content, filename):
    """从内容提取标题"""
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            return line.lstrip('#').strip()
        if line.startswith('【') and '】' in line:
            match = re.search(r'【(.+?)】', line)
            if match:
                return match.group(1)
    # fallback
    return filename.replace('.md', '')

def extract_date_from_filename(filename):
    """从文件名提取日期"""
    match = re.search(r'\[?(\d{4}-\d{2}-\d{2})\]?', filename)
    if match:
        return match.group(1)
    return ""

def create_summary(source_path, dest_path, title, category, tags):
    """创建summary文件"""
    if dest_path.exists():
        return False, "already exists"

    content = f"""---
title: {title}
type: summary
created: 2026-04-15
updated: 2026-04-15
tags: [{tags}]
category: {category}
source: [[{source_path.name}]]
---

## 关键要点

（待补充具体内容）

## 相关链接
- [[{source_path.name}]]
"""

    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return True, "created"

def process_zhida_xing_anli():
    """处理最高检-指导性案例-md"""
    source_dir = SOURCES_DIR / "最高检-指导性案例-md"
    count = 0
    for f in sorted(source_dir.glob("*.md")):
        frontmatter, body = extract_frontmatter(f.read_text(encoding='utf-8'))
        title = extract_title(body, f.name)
        dest_name = f"SPP_GuideCase_{f.stem}.md"
        dest = SUMMARIES_DIR / dest_name
        success, msg = create_summary(f, dest, title, "刑事", "最高检,指导性案例")
        if success:
            count += 1
        elif msg == "already exists":
            count += 1  # count anyway
    return count

def process_jian_da_wang():
    """处理最高检-检答网集萃-md"""
    source_dir = SOURCES_DIR / "最高检-检答网集萃-md"
    count = 0
    for f in sorted(source_dir.glob("*.md")):
        frontmatter, body = extract_frontmatter(f.read_text(encoding='utf-8'))
        title = extract_title(body, f.name)
        date = extract_date_from_filename(f.name)
        dest_name = f"SPP_JianDaWang_{date}_{f.stem}.md"
        dest = SUMMARIES_DIR / dest_name
        success, msg = create_summary(f, dest, title, "刑事", "最高检,检答网")
        if success:
            count += 1
        elif msg == "already exists":
            count += 1
    return count

def process_ruku_anli():
    """处理最高法-入库案例选介-md"""
    source_dir = SOURCES_DIR / "最高法-入库案例选介-md"
    count = 0
    for f in sorted(source_dir.glob("*.md")):
        frontmatter, body = extract_frontmatter(f.read_text(encoding='utf-8'))
        title = extract_title(body, f.name)
        date = extract_date_from_filename(f.name)
        dest_name = f"Court_RukuAnli_{date}_{f.stem}.md"
        dest = SUMMARIES_DIR / dest_name
        success, msg = create_summary(f, dest, title, "民商事", "最高法,人民法院案例库")
        if success:
            count += 1
        elif msg == "already exists":
            count += 1
    return count

def process_fada_wang():
    """处理最高法-法答网精选答问-md"""
    source_dir = SOURCES_DIR / "最高法-法答网精选答问-md"
    count = 0
    for f in sorted(source_dir.glob("*.md")):
        frontmatter, body = extract_frontmatter(f.read_text(encoding='utf-8'))
        title = extract_title(body, f.name)
        dest_name = f"Court_FaDaWang_{f.stem}.md"
        dest = SUMMARIES_DIR / dest_name
        success, msg = create_summary(f, dest, title, "民商事", "最高法,法答网")
        if success:
            count += 1
        elif msg == "already exists":
            count += 1
    return count

if __name__ == "__main__":
    print("=== 开始处理微信公号资料 ===\n")

    print("1. 处理最高检-指导性案例...")
    c1 = process_zhida_xing_anli()
    print(f"   完成: {c1} 个文件\n")

    print("2. 处理最高检-检答网集萃...")
    c2 = process_jian_da_wang()
    print(f"   完成: {c2} 个文件\n")

    print("3. 处理最高法-入库案例选介...")
    c3 = process_ruku_anli()
    print(f"   完成: {c3} 个文件\n")

    print("4. 处理最高法-法答网精选答问...")
    c4 = process_fada_wang()
    print(f"   完成: {c4} 个文件\n")

    total = c1 + c2 + c3 + c4
    print(f"=== 总计创建 {total} 个 summaries ===")

    # 列出当前summaries数量
    current = len(list(SUMMARIES_DIR.glob("*.md")))
    print(f"wiki/summaries/ 当前文件数: {current}")
