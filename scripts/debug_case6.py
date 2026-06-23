#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
p = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/39[2022-08-29]最高检发布第三十九批指导性案例.md")
content = p.read_text(encoding='utf-8')

# Find all ** positions
import re
positions = []
for m in re.finditer(r'\*\*', content):
    positions.append(m.start())

print(f"Found {len(positions)} ** markers")
# Show first 20 positions with context
for i, pos in enumerate(positions[:20]):
    start = max(0, pos - 20)
    end = min(len(content), pos + 40)
    print(f"{i}: pos={pos}, context={repr(content[start:end])}")