#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Debug: find exact byte pattern for case 158"""

from pathlib import Path

p = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/39[2022-08-29]最高检发布第三十九批指导性案例.md")
content = p.read_text(encoding='utf-8')

# Find pattern: ** （检例第158号）**
import re
matches = list(re.finditer(r'\*\* （检例第158号）\*\*', content))
print(f"Found {len(matches)} matches for pattern")
for m in matches:
    print(f"  Position {m.start()}: {repr(m.group())}")

# Also check for casename before it
before = content[matches[0].start()-100:matches[0].start()] if matches else ""
print(f"\nContext before: {repr(before)}")