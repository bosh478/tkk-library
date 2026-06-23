#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

p = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/39[2022-08-29]最高检发布第三十九批指导性案例.md")

# Check raw bytes
raw = p.read_bytes()
print(f"File size: {len(raw)} bytes")

# Find the position of '检例第158号' in raw bytes
search = '检例第158号'.encode('utf-8')
pos = raw.find(search)
print(f"Search string position in bytes: {pos}")

if pos >= 0:
    # Show surrounding bytes
    start = max(0, pos - 20)
    end = min(len(raw), pos + len(search) + 20)
    print(f"Raw bytes around position: {raw[start:end]}")
    print(f"Decoded: {raw[start:end].decode('utf-8', errors='replace')}")