#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
p = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/39[2022-08-29]最高检发布第三十九批指导性案例.md")
content = p.read_text(encoding='utf-8')

import re
# Try using a simpler approach - split by cases using the section markers
# Find all positions where ** （检例第X号）** appears
header_marker = '** （检例第158号）**'
pos = content.find(header_marker)
print(f"Header marker position: {pos}")

if pos >= 0:
    # Get the text before this header - we need to find the case name before it
    before_text = content[:pos]
    # The case name should be in the last line before the header
    last_newline = before_text.rfind('\n')
    case_name_line = before_text[last_newline+1:]
    print(f"Case name line: {repr(case_name_line)}")

    # Remove the ** from the start if present
    case_name = case_name_line.strip()
    if case_name.startswith('**'):
        case_name = case_name[2:]
    print(f"Case name: {repr(case_name)}")