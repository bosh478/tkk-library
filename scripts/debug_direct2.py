#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import re

p = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/39[2022-08-29]最高检发布第三十九批指导性案例.md")
content = p.read_text(encoding='utf-8')

# Pattern: **casename (only opening **) followed by ** （检例第X号）**
# Two ** on consecutive lines, each only has opening **
# We need to capture from first ** to just before second **
# But actually the case name is between the two ** on line 16

# Let's look for the pattern: **casename\n** （检例第X号）**
pattern = r'\*\*(.+?)\n\*\* （检例第158号）\*\*'
match = re.search(pattern, content)
print(f"Pattern match: {match}")
if match:
    print(f"Full match: {repr(match.group())}")
    print(f"Group 1: {repr(match.group(1))}")

# Try with newlines in the content
print(f"\nContent contains \\r\\n: {chr(13) in content[:1000]}")
print(f"Content contains \\n: {chr(10) in content[:1000]}")