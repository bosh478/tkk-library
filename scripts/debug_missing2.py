#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

MISSING_FILES = {
    175: "44[2023-06-13]最高人民检察院发布第四十四批指导性案例.md",
    186: "47[2023-08-22]最高检发布第四十七批指导性案例剑指金融领域新型职务犯罪.md",
}

for case_num, filename in MISSING_FILES.items():
    p = Path(f"D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/{filename}")
    content = p.read_text(encoding='utf-8')

    search_str = f"检例第{case_num}号"
    pos = content.find(search_str)
    print(f"\nCase {case_num} in {filename}:")
    print(f"  Position: {pos}")
    if pos >= 0:
        start = max(0, pos - 30)
        end = min(len(content), pos + len(search_str) + 30)
        print(f"  Context: {repr(content[start:end])}")