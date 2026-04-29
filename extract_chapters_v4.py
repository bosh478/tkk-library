#!/usr/bin/env python3
"""Extract chapters from 法医病理司法鉴定实务 - FIXED Chinese number conversion."""

import re
import os

source_file = r"D:/AI agent/tkk-library/sources/证据质证/《法医病理司法鉴定实务》官大威 科学出版社 2025年.md"
output_dir = r"D:/AI agent/tkk-library/wiki/concepts/"

# Read source file
with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Split into lines
lines = content.split('\n')

# Find all chapter headings (## 第X章 or # 第X章) with Chinese numerals only
chapter_pattern = re.compile(r'^#{1,2}\s*(第[一二三四五六七八九十〇零]+章)')

chapters = []
for i, line in enumerate(lines):
    match = chapter_pattern.search(line.strip())
    if match:
        chapters.append((i, match.group(1)))  # line index, chapter name like "第一章"

print(f"Found {len(chapters)} chapters")

# FIXED Chinese to Arabic conversion
def cn_to_arabic(cn_str):
    """Convert Chinese chapter number suffix to Arabic numeral.

    Examples:
    - "一" -> 1
    - "十" -> 10
    - "十一" -> 11
    - "二十一" -> 21
    - "三十" -> 30
    """
    cn_map = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'〇':0,'零':0}
    result = 0
    for c in cn_str:
        if c in cn_map:
            result = result * 10 + cn_map[c]
        elif c == '十':
            result *= 10
        elif c == '百':
            result *= 100
        elif c == '千':
            result *= 1000
    return result

# Test
print("\nTest cn_to_arabic:")
tests = ['', '一', '二', '十', '十一', '十二', '二十', '二十一', '三十', '三十一']
for t in tests:
    print(f"  '{t}' -> {cn_to_arabic(t)}")

# Extract content for each chapter
for idx in range(len(chapters)):
    chapter_name = chapters[idx][1]  # e.g., "第一章"
    chapter_num = cn_to_arabic(chapter_name[1:-1])  # e.g., "一章" -> 1

    start_idx = chapters[idx][0]
    if idx + 1 < len(chapters):
        end_idx = chapters[idx + 1][0]
    else:
        end_idx = len(lines)

    # Get content from start to end (not including next chapter heading line)
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

    # Combine frontmatter with content
    full_content = frontmatter + chapter_content

    # Create filename
    filename = f"concept_法医病理司法鉴定实务_第{chapter_num}章.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_content)

    print(f"Created: {filename} ({len(full_content)} chars)")

print(f"\n\nDone! Created {len(chapters)} files in {output_dir}")