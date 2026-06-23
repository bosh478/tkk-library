#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
p = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/39[2022-08-29]最高检发布第三十九批指导性案例.md")
content = p.read_text(encoding='utf-8')

import re
# Maybe the first ** on line 16 is NOT a markdown formatting marker
# Let's just look for the case name followed by newline and then ** （检例第158号）**
# The case name might not have ** at all in this pattern
pattern = r'陈某某刑事申诉公开听证案\r?\n\*\* （检例第158号）\*\*'
match = re.search(pattern, content)
print(f"Match found: {match is not None}")
if match:
    print(f"Full match: {repr(match.group())}")

# Let's also try: only opening ** on line 16
pattern2 = r'\*\*(.+?)\r?\n\*\* （检例第158号）\*\*'
match2 = re.search(pattern2, content)
print(f"\nPattern2 found: {match2 is not None}")
if match2:
    print(f"Full match: {repr(match2.group())}")
    print(f"Group 1: {repr(match2.group(1))}")