#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
p = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/39[2022-08-29]最高检发布第三十九批指导性案例.md")
content = p.read_text(encoding='utf-8')

import re
# Maybe line 16 is **陈某某刑事申诉公开听证案\n (just one ** at start)
# and line 17 is ** （检例第158号）**
# Let's try to find any ** followed by the case name and newline
pattern = r'\*\*陈某某刑事申诉公开听证案\n'
match = re.search(pattern, content)
print(f"Pattern found: {match is not None}")
if match:
    print(f"Position: {match.start()}")
    print(f"Context: {repr(content[match.start():match.start()+50])}")

# Also try just looking for the newline pattern after case name
pattern2 = r'陈某某刑事申诉公开听证案\n'
match2 = re.search(pattern2, content)
print(f"\nPattern2 found: {match2 is not None}")
if match2:
    print(f"Position: {match2.start()}")
    print(f"Context: {repr(content[match2.start():match2.start()+50])}")