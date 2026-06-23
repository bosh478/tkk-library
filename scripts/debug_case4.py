#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
p = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/39[2022-08-29]最高检发布第三十九批指导性案例.md")
content = p.read_text(encoding='utf-8')

# Find exact position
idx = content.find('检例第158号')
if idx >= 0:
    print(f"Found at index {idx}")
    start = max(0, idx - 80)
    end = min(len(content), idx + 200)
    segment = content[start:end]
    print(f"Segment (repr): {repr(segment)}")

    # Check what characters are around it
    # 17 chars before: **陈某某刑事申诉公开听证案
    # then newline
    # then ** （检例第158号）**
    print("\nLooking for case name pattern...")
    case_start = content.rfind('**', 0, idx)
    print(f"Case name start marker at: {case_start}")
    print(f"Case name: {repr(content[case_start:idx])}")

    # Find the newline before **
    newline_before = content.rfind('\n', 0, case_start)
    print(f"Newline before case name: {newline_before}")
    print(f"Case name line: {repr(content[newline_before+1:idx])}")