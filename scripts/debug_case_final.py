#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from pathlib import Path

file_path = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/39[2022-08-29]最高检发布第三十九批指导性案例.md")
content = file_path.read_text(encoding='utf-8')

case_num = 158
header_pattern = rf'\n\*\* （检例第{case_num}号）\*\*'
match = re.search(header_pattern, content)
print(f"Header pattern: {repr(header_pattern)}")
print(f"Match found: {match}")
if match:
    print(f"Match position: {match.start()}")
    print(f"Match text: {repr(match.group())}")
else:
    # Try without the leading newline
    header_pattern2 = rf'\*\* （检例第{case_num}号）\*\*'
    match2 = re.search(header_pattern2, content)
    print(f"Without leading newline: {match2}")
    if match2:
        print(f"  Position: {match2.start()}")
        print(f"  Text: {repr(match2.group())}")