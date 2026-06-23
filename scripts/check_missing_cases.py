#!/usr/bin/env python3
"""Check which SPP Guide Cases are missing"""

import re
from pathlib import Path

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/syntheses")

def extract_case_numbers(content):
    """Extract all case numbers from source content"""
    pattern = r'检例第(\d+)号'
    matches = re.findall(pattern, content)
    return [int(m) for m in matches]

def main():
    # Get all case numbers from source files
    all_source_nums = set()
    for f in SOURCE_DIR.glob("*.md"):
        content = f.read_text(encoding='utf-8')
        nums = extract_case_numbers(content)
        all_source_nums.update(nums)

    # Get all existing wiki files
    existing_nums = set()
    for f in TARGET_DIR.glob("SPP_GuideCase_*.md"):
        # Extract number from filename
        match = re.search(r'检例第(\d+)号', f.name)
        if match:
            existing_nums.add(int(match.group(1)))

    print(f"Total source case numbers: {len(all_source_nums)}")
    print(f"Existing wiki files: {len(existing_nums)}")

    # Find missing
    missing = sorted(all_source_nums - existing_nums)
    print(f"Missing: {len(missing)}")
    if missing:
        print(f"Missing range: {missing[0]} - {missing[-1]}")
        # Group by batch (consecutive)
        ranges = []
        start = missing[0]
        prev = missing[0]
        for num in missing[1:]:
            if num != prev + 1:
                ranges.append((start, prev))
                start = num
            prev = num
        ranges.append((start, prev))

        for r in ranges:
            print(f"  Missing {r[0]}-{r[1]} ({r[1]-r[0]+1} files)")

    # Check existing
    existing_sorted = sorted(existing_nums)
    if existing_sorted:
        print(f"\nExisting range: {existing_sorted[0]} - {existing_sorted[-1]}")

if __name__ == "__main__":
    main()