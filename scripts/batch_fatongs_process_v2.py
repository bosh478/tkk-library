#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch process 上海一中法院 法通识 files to wiki/summaries/
Fixed encoding issues for Windows
"""
import os
import re
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')

SOURCE_DIR = Path(r"D:\AI agent\tkk-library\sources\微信公号资料\上海一中法院\上海一中法院-法通识-md")
TARGET_DIR = Path(r"D:\AI agent\tkk-library\wiki\summaries")

def extract_date_title(filename):
    """Extract date and title from filename like [2023-02-09]醉驾的10个常见法律问题法通识.md"""
    basename = os.path.basename(filename)
    # Pattern: [YYYY-MM-DD]Title法通识.md
    match = re.match(r'\[(\d{4}-\d{2}-\d{2})\](.+?)法通识\.md', basename)
    if match:
        date = match.group(1)
        title = match.group(2).strip()
        return date, title
    # Handle case where "法通识" might be part of title
    match = re.match(r'\[(\d{4}-\d{2}-\d{2})\](.+)\.md', basename)
    if match:
        date = match.group(1)
        title = match.group(2).strip()
        return date, title
    return None, None

def extract_title_from_content(content):
    """Extract title from first heading in content"""
    match = re.search(r'^#\s+(.+?)(?:\||\n)', content, re.MULTILINE)
    if match:
        title = match.group(1).strip().rstrip('|').strip()
        return title
    return None

def extract_key_points(content):
    """Extract meaningful key points from content"""
    points = []
    lines = content.split('\n')

    for line in lines:
        line = line.strip()
        # Skip headers, formatting lines, short lines
        if not line:
            continue
        if line.startswith('#'):
            continue
        if line.startswith('**') and line.endswith('**'):
            continue
        if line.startswith('文：') or line.startswith('值班编辑'):
            continue
        if line.startswith('http'):
            continue
        if '<' in line and '>' in line:
            continue

        # Clean markdown formatting
        clean = re.sub(r'\*\*', '', line)
        clean = re.sub(r'\[\d+\]', '', clean)
        clean = re.sub(r'^【.+?】', '', clean)  # Remove 【法条链接】 style markers
        clean = clean.strip()

        # Look for meaningful content lines (at least 15 chars)
        if len(clean) >= 15 and not clean.startswith('*') and '请点击' not in clean:
            points.append(clean)
            if len(points) >= 8:
                break

    return points[:5] if points else []

def determine_tags(title, content):
    """Determine tags based on title and content"""
    tags = []
    title_lower = title.lower() if title else ''

    # Category mapping
    if any(k in title_lower for k in ['劳动', '工伤', '女职工', '实习生', '培训', '仲裁']):
        tags.append('劳动与社会保障')
    if any(k in title_lower for k in ['借贷', '合同', '违约金', '中介', '租赁', '房产', '物业', '装修', '合伙', '赠与', '海外购物', '买房']):
        tags.append('合同与物权')
    if any(k in title_lower for k in ['醉驾', '交通', '事故', '名誉', '正当防卫', '毒品', '治安', '打架', '伤害']):
        tags.append('刑事与行政')
    if any(k in title_lower for k in ['抚养', '继承', '婚姻', '夫妻', '医美', '离婚']):
        tags.append('婚姻家庭')
    if any(k in title_lower for k in ['诉讼', '再审', '保全', '司法鉴定', '送达', '执行', '民商事']):
        tags.append('诉讼与仲裁')
    if any(k in title_lower for k in ['公司', '股东', '股权转让', '担保', '企业']):
        tags.append('公司商事')
    if any(k in title_lower for k in ['消费者', '旅游', '双十一', '网络直播', '网络', '消费']):
        tags.append('消费与互联网')

    # Add legal tag
    tags.append('法律通识')

    if not tags:
        tags.append('法律通识')

    return tags[:3]  # Limit to 3 tags

def process_file(filepath):
    """Process a single file and return the wiki content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

    # Extract date and title from filename
    date, title = extract_date_title(filepath)
    if not date or not title:
        print(f"Skipping invalid filename format: {filepath}")
        return None

    # Extract title from content heading
    content_title = extract_title_from_content(content)
    if content_title and len(content_title) > 5:
        title = content_title

    # Determine tags
    tags = determine_tags(title, content)

    # Generate key points
    points = extract_key_points(content)

    # Build frontmatter with proper escaping
    safe_title = title.replace('"', "'")

    frontmatter = f'''---
title: "{safe_title}"
type: summary
published: {date}
created: 2026-05-11
updated: 2026-05-11
tags: [{', '.join(tags)}]
source: sources/微信公号资料/上海一中法院/上海一中法院-法通识-md/{filepath.name}
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | 上海一中法院-法通识 |
| 类型 | 法律知识普及 |
| 发布日期 | {date} |
| 关键词 | {', '.join(tags)} |

## 核心要点

'''
    # Add key points
    for i, point in enumerate(points[:5], 1):
        frontmatter += f"{i}. {point}\n"

    return frontmatter, title, date

# Process all files
files = sorted(SOURCE_DIR.glob("*.md"))
print(f"Found {len(files)} files to process")

TARGET_DIR.mkdir(parents=True, exist_ok=True)

success_count = 0
error_files = []

for filepath in files:
    try:
        result = process_file(filepath)
        if result:
            frontmatter, title, date = result

            # Create target filename
            date_formatted = date.replace('-', '')
            # Clean title for filename - remove invalid chars
            safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
            safe_title = safe_title[:50]  # Limit length
            target_name = f"summary_{date_formatted}_上海一中法院_法通识_{safe_title}.md"
            target_path = TARGET_DIR / target_name

            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(frontmatter)

            print(f"Created: {target_name}")
            success_count += 1
    except Exception as e:
        print(f"Error processing {filepath.name}: {e}")
        error_files.append(str(filepath))

print(f"\nDone! Successfully processed {success_count}/{len(files)} files")
if error_files:
    print(f"Failed files: {len(error_files)}")