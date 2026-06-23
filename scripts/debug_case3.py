#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
p = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/39[2022-08-29]最高检发布第三十九批指导性案例.md")
content = p.read_text(encoding='utf-8')
lines = content.split('\n')
for i in range(14, 20):
    print(f"{i+1}: {repr(lines[i])}")

import re
# Try different patterns
patterns = [
    r'\*\* （检例第158号）\*\*',
    r'（检例第158号）',
    r'检例第158号',
]
for pat in patterns:
    matches = list(re.finditer(pat, content))
    print(f"\nPattern {repr(pat)}: {len(matches)} matches")