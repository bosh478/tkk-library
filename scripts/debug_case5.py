#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
p = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/39[2022-08-29]最高检发布第三十九批指导性案例.md")
content = p.read_text(encoding='utf-8')

# Find line 17 content directly
lines = content.split('\n')
print(f"Line 16: {repr(lines[15])}")
print(f"Line 17: {repr(lines[16])}")
print(f"Line 18: {repr(lines[17])}")

# Try to find the exact pattern
import re
# Pattern: **casename** then ** （检例第158号）**  (no closing ** on first line)
pat1 = r'\*\*(.+?)\s*\n\*\* （检例第158号）\*\*'
m1 = re.search(pat1, content)
print(f"\nPattern 1 match: {m1}")

# Maybe the first ** is actually just **
pat2 = r'\*\*陈某某刑事申诉公开听证案\s*\n\*\* （检例第158号）\*\*'
m2 = re.search(pat2, content)
print(f"Pattern 2 match: {m2}")

# Try different regex - maybe there's no closing ** on line 16
pat3 = r'\*\*(.+?)\n\*\* （检例第158号）\*\*'
m3 = re.search(pat3, content)
print(f"Pattern 3 match: {m3}")
if m3:
    print(f"  Groups: {m3.groups()}")