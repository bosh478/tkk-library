#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

p = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/39[2022-08-29]最高检发布第三十九批指导性案例.md")
content = p.read_text(encoding='utf-8')

# Write results to file
output = Path("D:/AI agent/tkk-library/scripts/debug_output.txt")
results = []

results.append(f"File size: {len(content)}")
results.append(f"Content preview (first 500 chars): {content[:500]}")

# Find position of case number
search = '检例第158号'
pos = content.find(search)
results.append(f"'{search}' position: {pos}")

if pos >= 0:
    # Show surrounding context
    start = max(0, pos - 100)
    end = min(len(content), pos + 50)
    segment = content[start:end]
    results.append(f"Segment around position: (index {start} to {end})")
    results.append(repr(segment))

output.write_text('\n'.join(results), encoding='utf-8')
print("Done - wrote to debug_output.txt")