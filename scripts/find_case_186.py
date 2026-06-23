#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import re

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md")

# Find which file contains case 186
for f in SOURCE_DIR.glob("*.md"):
    content = f.read_text(encoding='utf-8')
    if '检例第186号' in content:
        print(f"Case 186 found in: {f.name}")
        pos = content.find('检例第186号')
        start = max(0, pos - 50)
        end = min(len(content), pos + 50)
        print(f"  Context: {repr(content[start:end])}")
        break
    # Also check for just the number
    if '186号' in content:
        print(f"Found '186号' in: {f.name}")

# Also check the file 44 for case 175 formatting
print("\n--- Case 175 in file 44 ---")
p44 = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/44[2023-06-13]最高人民检察院发布第四十四批指导性案例.md")
content44 = p44.read_text(encoding='utf-8')
pos44 = content44.find('检例第175号')
print(f"Position: {pos44}")
if pos44 >= 0:
    start = max(0, pos44 - 30)
    end = min(len(content44), pos44 + 50)
    print(f"Context: {repr(content44[start:end])}")