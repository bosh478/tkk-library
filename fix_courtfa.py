import os
import re
from pathlib import Path

TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/syntheses")

files = list(TARGET_DIR.glob("CourtFa_入库案例_*.md"))
print(f"Found {len(files)} files to fix")

fixed_bracket = 0
fixed_fname = 0

for f in files:
    # Fix 1: triple bracket issue in related field
    content = f.read_text(encoding="utf-8")
    if "[[[concept_" in content:
        content = content.replace("[[[concept_", "[[concept_")
        f.write_text(content, encoding="utf-8")
        fixed_bracket += 1

    # Fix 2: clean filename prefix
    fname = f.name
    if "入库参考案例选介" in fname or "入库参考案例解读" in fname:
        new_fname = fname.replace("入库参考案例选介", "").replace("入库参考案例解读", "")
        if new_fname != fname:
            new_path = TARGET_DIR / new_fname
            f.rename(new_path)
            fixed_fname += 1
            print(f"Renamed: {fname} -> {new_fname}")

print(f"\nFixed {fixed_bracket} bracket issues")
print(f"Renamed {fixed_fname} files")