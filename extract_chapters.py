#!/usr/bin/env python3
"""Extract chapters from 法医病理司法鉴定实务 into separate files."""

import re

source_file = r"D:/AI agent/tkk-library/sources/证据质证/《法医病理司法鉴定实务》官大威 科学出版社 2025年.md"
output_dir = r"D:/AI agent/tkk-library/wiki/concepts/"

# Read source file
with open(source_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find all chapter headings (## 第X章 or # 第X章)
chapter_pattern = re.compile(r'^#{1,2}\s*第[一二三四五六七八九十〇零0-9]+章')

chapters = []
for i, line in enumerate(lines):
    if chapter_pattern.match(line.strip()):
        chapters.append((i + 1, line.strip()))  # line number (1-based), heading

print(f"Found {len(chapters)} chapter headings")
for idx, (ln, heading) in enumerate(chapters):
    print(f"  {idx+1}. Line {ln}: {heading}")

# Extract chapters
chapter_data = []
for idx in range(len(chapters)):
    start_line = chapters[idx][0]  # 1-based line number
    if idx + 1 < len(chapters):
        end_line = chapters[idx + 1][0] - 1
    else:
        end_line = len(lines)

    content = ''.join(lines[start_line - 1:end_line])  # Convert to 0-based indexing
    chapter_data.append((chapters[idx][1], content))

print(f"\nExtracted {len(chapter_data)} chapters")

# Create output files
import os
os.makedirs(output_dir, exist_ok=True)

for idx, (heading, content) in enumerate(chapter_data):
    # Extract chapter number from heading
    # e.g., "## 第一章 绪论" -> "第一章"
    # e.g., "# 第三章 死亡的法医学鉴定理论" -> "第三章"
    match = re.search(r'第[一二三四五六七八九十〇零0-9]+章', heading)
    if match:
        chapter_num = match.group()
        # Convert Chinese number to Arabic
        cn_to_arab = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'〇':0,'零':0,'十':10}
        # Handle 十单独的情况
        if chapter_num == '十':
            arab_num = 10
        elif chapter_num.startswith('十'):
            # 十几
            arab_num = 10 + cn_to_arab.get(chapter_num[1], 0)
        else:
            arab_num = 0
            for c in chapter_num:
                if c in cn_to_arab:
                    arab_num = arab_num * 10 + cn_to_arab[c]
                elif c.isdigit():
                    arab_num = arab_num * 10 + int(c)

        filename = f"concept_法医病理司法鉴定实务_第{arab_num}章.md"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Created: {filename} ({len(content)} chars)")

print(f"\nDone! Created {len(chapter_data)} files in {output_dir}")