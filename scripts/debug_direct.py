#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import re

p = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/39[2022-08-29]最高检发布第三十九批指导性案例.md")
content = p.read_text(encoding='utf-8')

# Direct approach: find the position of the case number, then work backwards
idx = content.find('检例第158号')
print(f"Case number at index: {idx}")

# Find the last ** before this position
before = content[:idx]
last_dbl_star = before.rfind('**')
print(f"Last ** before case number at: {last_dbl_star}")
print(f"Context: {repr(content[last_dbl_star:idx+20])}")

# Now we need to find the case name:
# It should be the text between last ** and the case number
# But in this format, line 16 is **casename (only opening **)
# So the case name starts after **

case_name = content[last_dbl_star+2:idx].strip()
print(f"Extracted case name: {repr(case_name)}")