#!/usr/bin/env python3
"""Batch process 上海二中院-至正开放麦 markdown files to wiki/summaries/"""

import re
import os
from pathlib import Path

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/上海二中院/上海二中院-至正开放麦-md/")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/summaries/")

# Get all .md files (excluding backup configs)
source_files = sorted([f for f in SOURCE_DIR.glob("*.md") if not f.name.endswith(".baiduyun.uploading.cfg")])

print(f"Found {len(source_files)} files to process")

def extract_date_title(filename):
    """Extract date and title from filename like '[2023-02-03]标题至正开放麦.md'"""
    name = filename.stem
    match = re.match(r'\[(\d{4}-\d{2}-\d{2})\](.+)', name)
    if match:
        date = match.group(1).replace('-', '')  # YYYYMMDD
        title_full = match.group(2).strip()
        title = title_full.replace('至正开放麦', '').strip()
        # Also remove court suffix if present (e.g., "马鞍山中院", "泰州中院", "上海财经大学", "复旦大学")
        for suffix in ['马鞍山中院', '泰州中院', '上海财经大学', '复旦大学']:
            if title.endswith(suffix):
                title = title[:-len(suffix)].strip()
        return date, title
    return None, name

def extract_key_points(content, min_points=5):
    """Extract at least min_points key points from content"""
    # Remove frontmatter if present
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            content = parts[2]

    lines = content.strip().split('\n')
    key_points = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            continue
        if len(line) < 15:
            continue

        # Clean up markdown formatting
        clean = re.sub(r'^\s*[-*+]\s*', '', line)
        clean = re.sub(r'^\s*\d+\.\s*', '', clean)
        clean = re.sub(r'\*\*(.+?)\*\*', r'\1', clean)
        clean = re.sub(r'\*(.+?)\*', r'\1', clean)
        clean = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean)  # Remove links

        if len(clean) > 15 and len(clean) < 300:
            key_points.append(clean)

        if len(key_points) >= min_points * 2:
            break

    # Deduplicate
    seen = set()
    unique_points = []
    for p in key_points:
        if p not in seen:
            seen.add(p)
            unique_points.append(p)

    return unique_points[:min_points]

def extract_excerpt(content, max_chars=500):
    """Extract a brief excerpt from content"""
    # Remove frontmatter if present
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            content = parts[2]

    paragraphs = content.strip().split('\n\n')
    excerpt_lines = []

    for p in paragraphs:
        p = p.strip()
        # Skip headers, short lines, and lines that are mostly markdown
        if p.startswith('#'):
            continue
        if len(p) < 50:
            continue
        # Skip if it's mostly a link or image
        if p.startswith('![') or p.startswith('[') and '](' in p:
            continue

        # Clean up the paragraph
        clean = re.sub(r'\*\*(.+?)\*\*', r'\1', p)
        clean = re.sub(r'\*(.+?)\*', r'\1', clean)
        clean = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean)

        excerpt_lines.append(clean)
        if sum(len(l) for l in excerpt_lines) > max_chars:
            break

    return '\n\n'.join(excerpt_lines)

def determine_tags(title, content):
    """Determine appropriate tags based on title and content"""
    tags = ["上海二中院", "至正开放麦", "普法"]

    title_lower = title.lower()
    content_lower = content.lower()

    if any(k in title_lower for k in ['公司法', '资本', '股权', '注销', '减资']):
        tags.append("公司商事")
    if any(k in title_lower for k in ['合同', '违约', '解除', '无效', '债务', '债权']):
        tags.append("民商事")
    if any(k in title_lower for k in ['刑法', '诈骗', '受贿', '行贿', '洗钱', '经营']):
        tags.append("刑事")
    if any(k in title_lower for k in ['劳动', '劳动关系', '竞业', '社保']):
        tags.append("劳动与社会保障")
    if any(k in title_lower for k in ['婚姻', '离婚', '抚养', '彩礼', '继承']):
        tags.append("婚姻家庭与继承")
    if any(k in title_lower for k in ['房屋', '租赁', '买房', '房产', '物业']):
        tags.append("建筑工程与房地产")
    if any(k in title_lower for k in ['行政', '处罚', '诉讼']):
        tags.append("行政诉讼")
    if any(k in title_lower for k in ['仲裁']):
        tags.append("诉讼与仲裁")
    if any(k in title_lower for k in ['消费', '网络', '电商', '平台']):
        tags.append("消费维权")
    if any(k in title_lower for k in ['执行', '查封', '保全']):
        tags.append("强制执行")

    return tags

def process_file(source_path):
    """Process a single source file and return target content"""
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = source_path.name
    date_str, title = extract_date_title(source_path)

    if not date_str:
        date_str = "20230101"
    if not title:
        title = filename.replace('.md', '')

    # Extract title from first # heading if exists
    h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if h1_match:
        title = h1_match.group(1).strip()

    key_points = extract_key_points(content)
    excerpt = extract_excerpt(content)
    tags = determine_tags(title, content)

    # Build frontmatter
    tags_str = ', '.join(tags)
    frontmatter = f"""---
title: {title}
type: summary
created: 2026-05-11
updated: 2026-05-11
tags: [{tags_str}]
source: [[{filename}]]
---"""

    # Build content sections
    key_points_section = "## 核心要点\n\n"
    for i, point in enumerate(key_points, 1):
        key_points_section += f"{i}. {point}\n"

    excerpt_section = "## 内容摘要\n\n" + excerpt if excerpt else "## 内容摘要\n\n（见正文）"

    result = f"""{frontmatter}

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{filename}]] |
| 类型 | 普法文章 |
| 发布日期 | {date_str} |
| 关键词 | {tags_str} |

{key_points_section}

{excerpt_section}

## 相关

- 详见 [[wiki/summaries/]] 上海二中院系列
"""

    return result

# Process all files
processed = 0
errors = 0

for source_file in source_files:
    try:
        date_str, title = extract_date_title(source_file)
        target_name = f"summary_{date_str}_上海二中院_至正开放麦_{title}.md"
        target_path = TARGET_DIR / target_name

        result_content = process_file(source_file)

        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(result_content)

        processed += 1
        if processed % 20 == 0:
            print(f"Processed {processed}/{len(source_files)} files...")

    except Exception as e:
        errors += 1
        print(f"Error processing {source_file.name}: {e}")

print(f"\nCompleted: {processed} files processed, {errors} errors")
print(f"Output directory: {TARGET_DIR}")