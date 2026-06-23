#!/usr/bin/env python3
"""Batch process 上海高院-办案心法 md files to wiki summaries"""

import re
import os
from pathlib import Path

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/上海高院/上海高院-办案心法-md/")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/summaries/")
TARGET_DIR.mkdir(parents=True, exist_ok=True)

def extract_title(content):
    """Extract title from first # line, remove suffix and date prefix"""
    match = re.search(r'^#\s*(.+?)(?:丨办案心法)?\s*$', content, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        # Remove date prefix like [2022-06-20]
        title = re.sub(r'^\[[\d-]+\]', '', title).strip()
        return title
    return None

def extract_author(content):
    """Extract author info"""
    # Look for pattern like "作者：白云" or "作者:白云"
    match = re.search(r'作者[：:]\s*(\S+)', content)
    if match:
        return match.group(1)
    # Look for author name after introducing text
    match = re.search(r'上海市.{0,6}法院.{0,20}法官[——](\S+)', content)
    if match:
        return match.group(1)
    return None

def extract_core_points(content):
    """Extract core points from content"""
    # Remove front matter and footer
    lines = content.split('\n')
    core_lines = []
    capture = False

    for line in lines:
        # Skip header/footer lines
        if '办案心法' in line or '学习更多' in line or '责任编辑' in line:
            continue
        if line.strip().startswith('来源丨') or line.strip().startswith('声明'):
            continue
        if line.strip().startswith('预览时标签'):
            continue
        if line.strip().startswith('__'):
            continue

        # Capture substantive content
        if capture or (line.strip() and not line.startswith('#')):
            capture = True
            stripped = line.strip()
            if stripped and len(stripped) > 10:
                core_lines.append(stripped)

    return '\n'.join(core_lines[:100])  # Limit to first 100 substantive lines

def extract_tags(content, title):
    """Extract tags from content"""
    tags = ['办案心法', '上海市高级人民法院']

    # Extract topic from content
    topic_match = re.search(r'#(.+?)#', content)
    if topic_match:
        tags.append(topic_match.group(1))

    return tags

def extract_related(content):
    """Extract related concept links"""
    related = []

    # Check for legal topics mentioned
    if '家事纠纷' in content or '离婚' in content:
        related.append('[[concept_家事纠纷调解]]')
    if '刑事' in content or '证人' in content or '被告人' in content:
        related.append('[[concept_刑事审判]]')
    if '行政' in content:
        related.append('[[concept_行政诉讼]]')

    # Default related
    if not related:
        related.append('[[concept_诉讼调解]]')

    return related

def create_summary(filename, content):
    """Create a summary wiki page"""
    title = extract_title(content)
    if not title:
        title = filename.stem

    author = extract_author(content)
    core_points = extract_core_points(content)
    tags = extract_tags(content, title)
    related = extract_related(content)

    # Extract date from filename
    date_match = re.search(r'\[(\d{4}-\d{2}-\d{2})\]', filename.name)
    created_date = date_match.group(1) if date_match else '2026-05-11'

    # Create frontmatter
    frontmatter = f'''---
title: {title}
type: summary
category: 诉讼与仲裁
published: {created_date}
created: 2026-05-11
updated: 2026-05-11
tags: [{', '.join(tags)}]
source: [[{filename.name}]]
related: [{', '.join(related)}]
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{filename.name}]] |
| 类型 | 法院办案指导 |
| 发布日期 | {created_date} |
| 关键词 | {', '.join(tags)} |
| 作者 | {author or '上海市高级人民法院'} |

## 核心要点

{core_points[:3000] if core_points else '（内容见正文）'}
'''

    return frontmatter

def process_file(filepath):
    """Process a single file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract clean title for filename
    title = extract_title(content)
    if not title:
        title = filepath.stem

    # Clean title for filename
    clean_title = re.sub(r'^\[[\d-]+\]', '', filepath.stem)
    clean_title = clean_title.replace('丨办案心法', '')
    clean_title = clean_title.strip()

    # Create output filename
    output_name = f"summary_上海市高院_办案心法_{clean_title}.md"
    output_path = TARGET_DIR / output_name

    # Create summary
    summary = create_summary(filepath, content)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(summary)

    return output_name

def main():
    files = list(SOURCE_DIR.glob("*.md"))
    print(f"Found {len(files)} files to process")

    for i, filepath in enumerate(files, 1):
        try:
            result = process_file(filepath)
            print(f"[{i}/{len(files)}] Created: {result}")
        except Exception as e:
            print(f"[{i}/{len(files)}] ERROR: {filepath.name}: {e}")

    print(f"\nDone! Created {len(files)} summary files")

if __name__ == "__main__":
    main()