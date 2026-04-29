#!/usr/bin/env python3
"""Extract chapters from 法医病理司法鉴定实务 - WORKING VERSION."""

import re
import os

source_file = r"D:/AI agent/tkk-library/sources/证据质证/《法医病理司法鉴定实务》官大威 科学出版社 2025年.md"
output_dir = r"D:/AI agent/tkk-library/wiki/concepts/"

# Read source file
with open(source_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Map from Chinese chapter name to Arabic number (comprehensive mapping)
def cn_chapter_to_num(cn_name):
    """Convert Chinese chapter name (e.g., '第十一章') to Arabic number (11)."""
    # Extract the Chinese number part (between 第 and 章)
    cn_map = {
        '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
        '六': 6, '七': 7, '八': 8, '九': 9, '〇': 0, '零': 0
    }

    # Get the number part (e.g., '十一' from '第十一章')
    num_part = cn_name[1:-1]  # Remove 第 and 章

    # Convert Chinese to Arabic
    # "十一" -> 11, "二十一" -> 21, "十" -> 10, "一" -> 1

    result = 0
    for char in num_part:
        if char == '十':
            if result == 0:
                result = 10
            else:
                result = result * 10 + 10
        elif char == '百':
            result *= 100
        elif char == '千':
            result *= 1000
        elif char in cn_map:
            result = result * 10 + cn_map[char]

    return result

# Test
test_chapters = [
    ("第一章", 1), ("第二章", 2), ("第三章", 3), ("第四章", 4), ("第五章", 5),
    ("第六章", 6), ("第七章", 7), ("第八章", 8), ("第九章", 9), ("第十章", 10),
    ("第十一章", 11), ("第十二章", 12), ("第十三章", 13), ("第十四章", 14), ("第十五章", 15),
    ("第十六章", 16), ("第十七章", 17), ("第十八章", 18), ("第十九章", 19), ("第二十章", 20),
    ("第二十一章", 21), ("第二十二章", 22), ("第二十三章", 23), ("第二十四章", 24), ("第二十五章", 25),
    ("第二十六章", 26), ("第二十七章", 27), ("第二十八章", 28), ("第二十九章", 29), ("第三十章", 30)
]

print("Testing chapter conversion:")
for cn_name, expected in test_chapters:
    result = cn_chapter_to_num(cn_name)
    status = "OK" if result == expected else f"ERROR (got {result})"
    print(f"  {cn_name} -> {result} ({status})")