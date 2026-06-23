#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
p = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/39[2022-08-29]最高检发布第三十九批指导性案例.md")
content = p.read_text(encoding='utf-8')

idx = content.find('检例第158号')
print(f"'检例第158号' found at index: {idx}")

# Show surrounding bytes
for offset in range(-60, 60, 20):
    start = idx + offset
    if start < 0:
        continue
    end = min(start + 20, len(content))
    segment = content[start:end]
    print(f"Offset {offset}: {segment.encode('raw_unicode_escape').decode('ascii')}")