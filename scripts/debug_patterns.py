#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import re

p = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/39[2022-08-29]最高检发布第三十九批指导性案例.md")
content = p.read_text(encoding='utf-8')

# Test the pattern with only opening **
pattern = r'\*\*(.+?)\n\*\* （检例第158号）\*\*'
match = re.search(pattern, content)
print(f'Match: {match}')

# Try simpler pattern - just capture until newline
pattern2 = r'\*\*(.+?)\n'
match2 = re.search(pattern2, content)
print(f'Pattern2 match: {match2}')
if match2:
    captured = match2.group(1)
    print(f'  Captured: {repr(captured)}')
    print(f'  Length: {len(captured)}')

# Maybe the issue is that .+? is matching too much or too little
# Let's try a character class that excludes **
pattern3 = r'\*\*([^*]+)\n'
match3 = re.search(pattern3, content)
print(f'Pattern3 match: {match3}')
if match3:
    print(f'  Captured: {repr(match3.group(1))}')