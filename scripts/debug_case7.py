#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
p = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/39[2022-08-29]最高检发布第三十九批指导性案例.md")
content = p.read_text(encoding='utf-8')

# Direct byte check - no print statements that might corrupt output
import re

# Find the exact pattern we need
# Looking for: **陈某某刑事申诉公开听证案\n** （检例第158号）**
# In Python repr the Chinese chars will show as unicode escapes

# Let's try to find it by looking for '**' followed by case name, then newline, then '** （检例第'
pattern = r'\*\*(.+?)\n\*\* （检例第158号）\*\*'
match = re.search(pattern, content)
print(f"Match found: {match is not None}")
if match:
    print(f"Full match: {repr(match.group())}")
    print(f"Group 1 (case name): {repr(match.group(1))}")