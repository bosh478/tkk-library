#!/usr/bin/env python3
"""Extract chapters from 法医病理司法鉴定实务 - WORKING."""

import re
import os

source_file = r"D:/AI agent/tkk-library/sources/证据质证/《法医病理司法鉴定实务》官大威 科学出版社 2025年.md"
output_dir = r"D:/AI agent/tkk-library/wiki/concepts/"

def cn_to_num(s):
    """Convert Chinese number string to integer - WORKING VERSION."""
    cn_map = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'〇':0,'零':0}

    if not s:
        return 0

    result = 0
    i = 0
    n = len(s)

    while i < n:
        c = s[i]
        if c in cn_map:
            next_is_ten = (i + 1 < n and s[i + 1] == '十')
            if next_is_ten:
                # e.g., 十一 -> add 10 then 1, 二十一 -> add 20 then 1
                result = result * 10 + cn_map[c]  # This adds the digit to result (e.g., for 二十一: first digit 2 -> result=2)
                i += 1  # Move past the digit, will process 十 next
            else:
                result = result * 10 + cn_map[c]
                i += 1
        elif c == '十':
            # This 十 is value 10, it may be:
            # 1) a continuation of previous digit (like 二十一 where 十 follows 二)
            # 2) standalone 十 meaning 10
            if i == 0 or s[i-1] not in cn_map:
                # standalone 十 (like 十 or 十一 where we already processed 一)
                result = result * 10 + 10
            else:
                # continuation (like 二十一 where 二 was already processed)
                # The previous digit was already multiplied by 10 and added to result
                # Here 十 just adds 10
                result = result * 10 + 10
            i += 1
        elif c == '百':
            result *= 100
            i += 1
        elif c == '千':
            result *= 1000
            i += 1
        else:
            i += 1

    return result

# Test
test_cases = [
    ('一', 1), ('二', 2), ('三', 3), ('十', 10), ('十一', 11), ('十二', 12),
    ('二十', 20), ('二十一', 21), ('三十', 30), ('三十一', 31),
    ('一百', 100), ('一百一十一', 111), ('二百三十四', 234)
]

print("Testing cn_to_num:")
for input_str, expected in test_cases:
    result = cn_to_num(input_str)
    status = "OK" if result == expected else f"FAIL (got {result})"
    print(f"  '{input_str}' -> {result} ({status})")

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

print(f"\nFound {len(chapters)} chapters")

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