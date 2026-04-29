#!/usr/bin/env python3
"""Extract chapters from 法医病理司法鉴定实务 - SIMPLE VERSION."""

import re
import os

source_file = r"D:/AI agent/tkk-library/sources/证据质证/《法医病理司法鉴定实务》官大威 科学出版社 2025年.md"
output_dir = r"D:/AI agent/tkk-library/wiki/concepts/"

# Read source file
with open(source_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find all chapter headings - use simple string matching
chapter_headings = []
for i, line in enumerate(lines):
    stripped = line.strip()
    # Match ## 第X章 or # 第X章
    if stripped.startswith('## 第') and '章' in stripped:
        # Extract chapter name
        match = re.search(r'(第[一二三四五六七八九十〇零]+章)', stripped)
        if match:
            chapter_headings.append((i, match.group(1)))
    elif stripped.startswith('# 第') and '章' in stripped:
        match = re.search(r'(第[一二三四五六七八九十〇零]+章)', stripped)
        if match:
            chapter_headings.append((i, match.group(1)))

print(f"Found {len(chapter_headings)} chapters")

# Simple manual mapping for numbers 1-30
def cn_to_num(cn_str):
    """Convert Chinese chapter suffix to number (1-30)."""
    # Simple mapping for 1-30
    mapping = {
        '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
        '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
        '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15,
        '十六': 16, '十七': 17, '十八': 18, '十九': 19, '二十': 20,
        '二十一': 21, '二十二': 22, '二十三': 23, '二十四': 24, '二十五': 25,
        '二十六': 26, '二十七': 27, '二十八': 28, '二十九': 29, '三十': 30
    }
    return mapping.get(cn_str, 0)

# Test
print("\nChapters found:")
for idx, (ln, name) in enumerate(chapter_headings):
    chapter_num = cn_to_num(name[1:])  # Remove 第 prefix
    print(f"  {idx+1}. Line {ln+1}: {name} -> {chapter_num}")

# Extract content for each chapter
for idx in range(len(chapter_headings)):
    chapter_name = chapter_headings[idx][1]
    chapter_num = cn_to_num(chapter_name[1:])

    start_idx = chapter_headings[idx][0]
    if idx + 1 < len(chapter_headings):
        end_idx = chapter_headings[idx + 1][0]
    else:
        end_idx = len(lines)

    # Get content
    chapter_content = '\n'.join(lines[start_idx:end_idx])

    # Create frontmatter
    frontmatter = f"""---
title: 法医病理司法鉴定实务_第{chapter_num}章
type: concept
created: 2026-04-29
updated: 2026-04-29
tags: [法医病理, 司法鉴定, 证据质证, 第{chapter_num}章]
sources: [["《法医病理司法鉴定实务》官大威 科学出版社 2025年"]]
置信度: 〔确定〕意图保留度: 40%
---

# 一句话说明
法医病理司法鉴定实务第{chapter_num}章，系统阐述{chapter_name.replace('第', '').replace('章', '')}的理论与实践。

# 顿悟
法医病理鉴定的核心在于将医学理论与司法实践相结合，通过科学的检验方法为司法裁判提供客观证据。

"""

    # Combine and write
    full_content = frontmatter + chapter_content
    filename = f"concept_法医病理司法鉴定实务_第{chapter_num}章.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_content)

    print(f"Created: {filename}")

print(f"\nDone! Created {len(chapter_headings)} files")