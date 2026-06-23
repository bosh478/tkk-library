#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import re

p = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/39[2022-08-29]最高检发布第三十九批指导性案例.md")
content = p.read_text(encoding='utf-8')

# Find where ** （检例第158号）** is located
search_str = '** （检例第158号）**'
pos = content.find(search_str)
print(f"'{search_str}' position: {pos}")

if pos >= 0:
    # Context around this position
    start = max(0, pos - 30)
    end = min(len(content), pos + len(search_str) + 10)
    segment = content[start:end]
    print(f"Segment (repr): {repr(segment)}")
    print(f"Segment (print): {segment}")

    # The case name should be in the line before
    before = content[:pos]
    last_newline = before.rfind('\n')
    line_before = before[last_newline+1:]
    print(f"\nLine before header: {repr(line_before)}")
    print(f"Line before header (print): {line_before}")