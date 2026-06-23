#!/usr/bin/env python3
"""
Ingest 180 最高法_凡人小事 files from sources to wiki/summaries/
Naming: summary_{YYYYMMDD}_最高法_凡人小事_{Title}.md
"""
import os
import re
from pathlib import Path

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民法院/最高法-凡人小事-md")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/summaries")

def extract_title(content):
    """Extract title from first # heading"""
    match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ""

def extract_date_from_filename(filename):
    """Extract date from filename like [2024-02-28]..."""
    match = re.search(r'\[(\d{4}-\d{2}-\d{2})\]', filename)
    if match:
        return match.group(1).replace('-', '')
    return ""

def extract_key_points(content):
    """Extract 5+ key points from content"""
    lines = content.split('\n')
    key_points = []

    for line in lines:
        # Skip metadata lines
        if line.startswith('#') or line.startswith('**') or line.startswith('来源：') or \
           line.startswith('作者：') or line.startswith('责任编辑') or \
           line.startswith('预览时标签') or line.startswith('* * *') or \
           line.startswith('__') or '编辑：' in line or '摄影：' in line or \
           '电子邮箱' in line or '联系电话' in line or '新媒体编辑' in line:
            continue
        line = line.strip()
        if line and len(line) > 10:
            line = re.sub(r'\*\*(.*?)\*\*', r'\1', line)
            key_points.append(line)
            if len(key_points) >= 5:
                break

    return key_points[:6]

def sanitize_for_filename(title):
    """Sanitize title part for filename - remove brackets and special chars"""
    # Remove [2024-xx-xx] prefix that may be in title
    title = re.sub(r'^\[.*?\]\s*', '', title)
    # Remove brackets and special punctuation
    title = re.sub(r'[（），、。！？：""''【】《》（）]', '', title)
    title = re.sub(r'\s+', '_', title.strip())
    # Truncate long titles
    if len(title) > 30:
        title = title[:30]
    return title

def process_file(src_path):
    """Process a single file"""
    filename = src_path.name
    date_str = extract_date_from_filename(filename)

    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()

    title = extract_title(content)
    if not title:
        title = filename

    key_points = extract_key_points(content)

    # Sanitize title for filename
    title_for_file = sanitize_for_filename(title)
    target_filename = f"summary_{date_str}_最高法_凡人小事_{title_for_file}.md"

    # Build frontmatter
    date_formatted = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"

    frontmatter = f"""---
title: {title}
type: summary
created: 2026-05-11
updated: 2026-05-11
tags: [司法为民, 基层法官, 凡人小事]
source: sources/微信公号资料/最高人民法院/最高法-凡人小事-md/{filename}
related: []
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[最高法-凡人小事-md/{filename}]] |
| 类型 | 法官故事 / 司法为民 |
| 发布日期 | {date_formatted} |
| 关键词 | 基层法官 / 司法为民 / 凡人小事 |
| 核心要点 | {len(key_points)} 条要点（见下方） |

## ❓ 关键信息

"""

    for i, point in enumerate(key_points, 1):
        frontmatter += f"{i}. {point}\n"

    return target_filename, frontmatter

def main():
    source_files = list(SOURCE_DIR.glob("*.md"))
    total = len(source_files)
    print(f"Found {total} source files")

    success_count = 0
    error_count = 0
    errors = []

    for i, src_path in enumerate(source_files, 1):
        try:
            target_filename, content = process_file(src_path)
            target_path = TARGET_DIR / target_filename

            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content)

            success_count += 1
            if success_count % 30 == 0:
                print(f"  Processed {success_count}/{total}")

        except Exception as e:
            error_count += 1
            errors.append(f"{src_path.name}: {str(e)}")
            print(f"  ERROR: {src_path.name}: {e}")

    print(f"\nCompleted: {success_count} success, {error_count} errors")
    if errors:
        for e in errors[:5]:
            print(f"  {e}")

if __name__ == "__main__":
    main()