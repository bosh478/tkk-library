#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from pathlib import Path

file_path = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/39[2022-08-29]最高检发布第三十九批指导性案例.md")
content = file_path.read_text(encoding='utf-8')

# Write to file for debugging
with open("D:/AI agent/tkk-library/scripts/debug_result.txt", "w", encoding="utf-8") as f:
    f.write(f"Content length: {len(content)}\n")

    case_num = 158
    search_str = f"检例第{case_num}号"
    pos = content.find(search_str)
    f.write(f"'{search_str}' position: {pos}\n")

    if pos >= 0:
        start = max(0, pos - 30)
        end = min(len(content), pos + len(search_str) + 30)
        segment = content[start:end]
        f.write(f"Segment around position:\n")
        f.write(repr(segment))

        # Check what the actual character before '检' is
        f.write(f"\nCharacter at pos-1: {repr(content[pos-1])}\n")
        f.write(f"Character at pos-2: {repr(content[pos-2])}\n")
        f.write(f"Character at pos-3: {repr(content[pos-3])}\n")

print("Done - wrote to debug_result.txt")