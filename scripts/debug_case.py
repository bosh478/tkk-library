#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Debug: check actual content around case 158"""

from pathlib import Path

p = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/39[2022-08-29]最高检发布第三十九批指导性案例.md")
content = p.read_text(encoding='utf-8')
lines = content.split('\n')

print("Lines 14-22:")
for i in range(14, min(22, len(lines))):
    print(f"{i+1}: {repr(lines[i])}")

print("\nSearching for '检例第158' context...")
idx = content.find('检例第158')
if idx >= 0:
    print(f"Found at index {idx}")
    start = max(0, idx - 50)
    end = min(len(content), idx + 100)
    print(repr(content[start:end]))