#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import re

# Check file 47 for case 186
p = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/47[2023-08-22]最高检发布第四十七批指导性案例剑指金融领域新型职务犯罪.md")
content = p.read_text(encoding='utf-8')

# Find position of case 186
search_str = "检例第186号"
pos = content.find(search_str)
print(f"Case 186 position: {pos}")

if pos >= 0:
    start = max(0, pos - 30)
    end = min(len(content), pos + len(search_str) + 30)
    print(f"Context: {repr(content[start:end])}")
else:
    # Try just "186号"
    search_str2 = "186号"
    pos2 = content.find(search_str2)
    print(f"186号 position: {pos2}")
    if pos2 >= 0:
        start = max(0, pos2 - 30)
        end = min(len(content), pos2 + 30)
        print(f"Context: {repr(content[start:end])}")