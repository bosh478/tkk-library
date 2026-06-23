#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

p = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/39[2022-08-29]最高检发布第三十九批指导性案例.md")
content = p.read_text(encoding='utf-8')

# Write content around position 1106 to file
pos = 1106
start = max(0, pos - 50)
end = min(len(content), pos + 50)

with open("D:/AI agent/tkk-library/scripts/raw_content.txt", "w", encoding="utf-8") as f:
    f.write(f"Position: {pos}\n")
    f.write(f"Content around position:\n")
    f.write(repr(content[start:end]))

print(f"Wrote to raw_content.txt")
print(f"Start: {start}, End: {end}")
print(f"Content (print): {content[start:end]}")