#!/usr/bin/env python3
"""
Batch process 上海一中法院 法通识 files to wiki/summaries/
"""
import os
import re
from pathlib import Path

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/上海一中法院/上海一中法院-法通识-md")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/summaries")

def extract_date_title(filename):
    """Extract date and title from filename like [2023-02-09]醉驾的10个常见法律问题法通识.md"""
    basename = os.path.basename(filename)
    match = re.match(r'\[(\d{4}-\d{2}-\d{2})\](.+)法通识\.md', basename)
    if match:
        date = match.group(1)
        title = match.group(2).strip()
        return date, title
    return None, None

def extract_content_points(content):
    """Extract key points from content, avoiding placeholders"""
    points = []
    lines = content.split('\n')

    # Look for numbered items, bullet points, or key statements
    for line in lines:
        line = line.strip()
        # Skip empty lines, headers, and formatting
        if not line or line.startswith('#') or line.startswith('**') or line.startswith('文：') or line.startswith('值班编辑'):
            continue
        # Clean markdown formatting
        line = re.sub(r'\*\*', '', line)
        line = re.sub(r'\[\d+\]', '', line)
        # Look for meaningful content lines (at least 20 chars)
        if len(line) >= 20 and not line.startswith('http') and '<' not in line:
            points.append(line)
            if len(points) >= 10:  # Get up to 10 points
                break

    return points[:5] if points else []  # Return at least 5

def determine_tags(title, content):
    """Determine tags based on title and content"""
    tags = []
    title_lower = title.lower()

    # Category mapping
    if any(k in title_lower for k in ['劳动', '工伤', '女职工', '实习生', '培训']):
        tags.append('劳动与社会保障')
    if any(k in title_lower for k in ['借贷', '合同', '违约金', '中介', '租赁', '房产', '物业', '装修', '合伙', '赠与', '海外购物']):
        tags.append('合同与物权')
    if any(k in title_lower for k in ['醉驾', '交通', '事故', '名誉', '正当防卫', '毒品', '治安']):
        tags.append('刑事与行政')
    if any(k in title_lower for k in ['抚养', '继承', '婚姻', '夫妻', '医美']):
        tags.append('婚姻家庭')
    if any(k in title_lower for k in ['仲裁', '诉讼', '再审', '保全', '司法鉴定', '送达', '执行']):
        tags.append('诉讼与仲裁')
    if any(k in title_lower for k in ['公司', '股东', '股权转让', '担保', '民商事']):
        tags.append('公司商事')
    if any(k in title_lower for k in ['消费者', '旅游', '双十一', '网络直播']):
        tags.append('消费与互联网')

    # Add legal tag
    tags.append('法律通识')

    # Ensure at least one tag
    if not tags:
        tags.append('法律通识')

    return tags

def process_file(filepath):
    """Process a single file and return the wiki content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract date and title from filename
    date, title = extract_date_title(filepath)
    if not date or not title:
        print(f"Skipping invalid filename format: {filepath}")
        return None

    # Extract first heading as title if present
    match = re.search(r'^#\s+(.+?)(?:\||\n)', content, re.MULTILINE)
    if match:
        title = match.group(1).strip().rstrip('|').strip()

    # Determine tags
    tags = determine_tags(title, content)

    # Generate key points
    points = extract_content_points(content)

    # Build frontmatter
    frontmatter = f"""---
title: {title}
type: summary
published: {date}
created: 2026-05-11
updated: 2026-05-11
tags: [{', '.join(tags)}]
source: sources/微信公号资料/上海一中法院/上海一中法院-法通识-md/{os.path.basename(filepath)}
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | 上海一中法院-法通识 |
| 类型 | 法律知识普及 |
| 发布日期 | {date} |
| 关键词 | {', '.join(tags)} |

## 核心要点

"""
    # Add key points
    for i, point in enumerate(points, 1):
        frontmatter += f"{i}. {point}\n"

    return frontmatter, title

# Process all files
files = sorted(SOURCE_DIR.glob("*.md"))
print(f"Found {len(files)} files to process")

for filepath in files:
    try:
        result = process_file(filepath)
        if result:
            frontmatter, title = result
            # Create target filename: summary_{YYYYMMDD}_上海一中法院_法通识_{Title}.md
            date, _ = extract_date_title(filepath)
            date_formatted = date.replace('-', '')
            safe_title = re.sub(r'[<>:"/\\|?*]', '', title)  # Remove invalid filename chars
            target_name = f"summary_{date_formatted}_上海一中法院_法通识_{safe_title}.md"
            target_path = TARGET_DIR / target_name

            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(frontmatter)

            print(f"Created: {target_name}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

print(f"\nDone! Processed {len(files)} files")