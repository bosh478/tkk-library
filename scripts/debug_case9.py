#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
p = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/39[2022-08-29]最高检发布第三十九批指导性案例.md")
content = p.read_text(encoding='utf-8')

import re
# Pattern: **casename (no closing **) followed by newline then ** （检例第158号）**
# The opening ** on line 16 is NOT closed - it's just **casename
# Then line 17: ** （检例第158号）**
pattern = r'\*\*(.+?)\n\*\* （检例第158号）\*\*'
match = re.search(pattern, content)
print(f"Match found: {match is not None}")
if match:
    print(f"Full match: {repr(match.group())}")
    print(f"Group 1 (case name): {repr(match.group(1))}")