#!/usr/bin/env python3
"""Batch ingest 188 files from 最高检高质效办好每一个案件 to wiki/summaries/"""

import os
import re
import glob
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-高质效办好每一个案件-md")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/summaries")
SOURCE_PREFIX = "sources/微信公号资料/最高人民检察院/最高检-高质效办好每一个案件-md"

def parse_source_filename(filename):
    """Extract date and title from source filename like '[2023-03-23]在高质效办好每一个案件中践行人民至上.md'"""
    basename = os.path.basename(filename)
    match = re.match(r'\[(\d{4}-\d{2}-\d{2})\](.+)\.md$', basename)
    if match:
        date_str = match.group(1).replace('-', '')  # 20230323
        title = match.group(2).strip()
        return date_str, title
    return None, None

def extract_title_and_content(filepath):
    """Extract title from first # heading and key points from content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    title = None
    body_lines = []

    for i, line in enumerate(lines):
        if title is None and line.startswith('#'):
            title = line.lstrip('#').strip()
        elif line.startswith('#') and i > 0:
            # Skip subsequent headings, keep content
            pass
        else:
            clean_line = line.strip()
            if clean_line and not clean_line.startswith(('来源：', '预览时', '阅读原文', '**')):
                body_lines.append(clean_line)

    # Extract key points - look for paragraphs that seem substantive
    key_points = []
    current_point = []

    for line in body_lines:
        # Stop at common endings
        if line.startswith('（作者为') or line.startswith('来源：') or line.startswith('编辑：'):
            continue
        if len(line) > 30:  # Only substantive lines
            current_point.append(line)
            if len(current_point) >= 3:
                key_points.append(' '.join(current_point))
                current_point = []
                if len(key_points) >= 6:  # Get at least 6 key points
                    break

    if not key_points and body_lines:
        # Fallback: take first substantive paragraphs
        for line in body_lines[:10]:
            if len(line) > 50 and line not in key_points:
                key_points.append(line)
                if len(key_points) >= 5:
                    break

    return title, key_points[:8]  # Return up to 8 key points

def create_summary_file(source_file, date_str, title):
    """Create summary file with frontmatter"""
    filename = os.path.basename(source_file)

    # Extract title from content if not from filename
    content_title, key_points = extract_title_and_content(source_file)

    if not title:
        title = content_title or filename

    # Create tags
    tags = ["检察工作", "高质效办案", "司法实践"]

    # Build frontmatter
    frontmatter = f"""---
title: {title}
type: summary
created: 2026-05-11
updated: 2026-05-11
tags: {tags}
source: {SOURCE_PREFIX}/{filename}
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{filename}]] |
| 类型 | 检察工作指导 |
| 发布日期 | {date_str[:4]}-{date_str[4:6]}-{date_str[6:8]} |
| 关键词 | 高质效办案 / 公平正义 / 检察履职 |

## ❓ 核心要点

"""
    for i, point in enumerate(key_points[:6], 1):
        # Clean up point
        clean_point = point.strip()
        if len(clean_point) > 200:
            clean_point = clean_point[:200] + "..."
        frontmatter += f"{i}. {clean_point}\n"

    frontmatter += "\n---\n"

    return frontmatter

def process_file(source_file):
    """Process a single file"""
    date_str, title = parse_source_filename(source_file)
    if not date_str:
        return None, f"Failed to parse: {source_file}"

    # Create target filename
    target_filename = f"summary_{date_str}_最高检_高质效办好每一个案件_{title}.md"
    target_path = TARGET_DIR / target_filename

    # Skip if exists
    if target_path.exists():
        return target_filename, "skipped (exists)"

    try:
        summary_content = create_summary_file(source_file, date_str, title)
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        return target_filename, "success"
    except Exception as e:
        return target_filename, f"error: {str(e)}"

def main():
    # Get all source files
    source_files = list(SOURCE_DIR.glob("*.md"))
    print(f"Found {len(source_files)} source files")

    results = []
    success_count = 0
    skipped_count = 0
    error_count = 0

    # Process in parallel batches
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(process_file, f): f for f in source_files}

        for future in as_completed(futures):
            result, status = future.result()
            if result:
                results.append((result, status))
                if status == "success":
                    success_count += 1
                elif "skipped" in status:
                    skipped_count += 1
                else:
                    error_count += 1

    print(f"\n=== Processing Complete ===")
    print(f"Total: {len(source_files)}")
    print(f"Success: {success_count}")
    print(f"Skipped (existed): {skipped_count}")
    print(f"Errors: {error_count}")

    if error_count > 0:
        print("\nErrors:")
        for r, s in results:
            if "error" in s:
                print(f"  {r}: {s}")

if __name__ == "__main__":
    main()