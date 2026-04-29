#!/usr/bin/env python3
"""Extract chapters from 法医病理司法鉴定实务 - FINAL VERSION."""

import re
import os

source_file = r"D:/AI agent/tkk-library/sources/证据质证/《法医病理司法鉴定实务》官大威 科学出版社 2025年.md"
output_dir = r"D:/AI agent/tkk-library/wiki/concepts/"

def cn_to_num(s):
    """Convert Chinese number string to integer."""
    result = 0
    for c in s:
        if c == '十':
            result = result * 10 + 10 if result > 0 else 10
        elif c == '一': result = result * 10 + 1
        elif c == '二': result = result * 10 + 2
        elif c == '三': result = result * 10 + 3
        elif c == '四': result = result * 10 + 4
        elif c == '五': result = result * 10 + 5
        elif c == '六': result = result * 10 + 6
        elif c == '七': result = result * 10 + 7
        elif c == '八': result = result * 10 + 8
        elif c == '九': result = result * 10 + 9
        elif c == '〇' or c == '零': result = result * 10 + 0
    return result

# Read source file
with open(source_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find all chapter headings
chapter_pattern = re.compile(r'^#{1,2}\s*(第[一二三四五六七八九十〇零]+章)')

chapters = []
for i, line in enumerate(lines):
    match = chapter_pattern.search(line.strip())
    if match:
        chapters.append((i, match.group(1)))

print(f"Found {len(chapters)} chapters")

# Extract content for each chapter
for idx in range(len(chapters)):
    chapter_name = chapters[idx][1]  # e.g., "第一章"
    chapter_num = cn_to_num(chapter_name[1:-1])  # e.g., "一章" -> 1

    start_idx = chapters[idx][0]
    if idx + 1 < len(chapters):
        end_idx = chapters[idx + 1][0]
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

print(f"\nDone! Created {len(chapters)} files")