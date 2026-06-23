#!/usr/bin/env python3
"""
Cleanup script for 上海一中法院 summary duplicates.
Removes old files and keeps new ones with better content.
"""
import os
from pathlib import Path

VAULT_ROOT = Path(r"D:\AI agent\tkk-library")
DST_BASE = VAULT_ROOT / "wiki" / "summaries"

def main():
    print("=" * 60)
    print("Cleanup 上海一中法院 Duplicates")
    print("=" * 60)

    # Find all summary files for 上海一中
    all_files = list(DST_BASE.glob("summary_*上海一中*.md"))
    print(f"Total files before cleanup: {len(all_files)}")

    # Group by date
    date_groups = {}
    for f in all_files:
        # Extract date from filename (format: summary_YYYYMMDD_...)
        name = f.name
        if len(name) > 16:
            date = name[8:16]
        else:
            date = "unknown"

        if date not in date_groups:
            date_groups[date] = []
        date_groups[date].append(f)

    # Process duplicates
    deleted = 0
    kept = 0

    for date, files in date_groups.items():
        if len(files) == 1:
            kept += 1
            continue

        # Sort by filename length (longer = newer/better)
        files.sort(key=lambda x: len(x.name), reverse=True)

        # Keep the first (longest) file, delete the rest
        kept += 1
        for f in files[1:]:
            try:
                f.unlink()
                deleted += 1
            except Exception as e:
                print(f"Error deleting {f.name}: {e}")

    print(f"\nCleanup complete:")
    print(f"  Files kept: {kept}")
    print(f"  Files deleted: {deleted}")

    # Verify final count
    final_files = list(DST_BASE.glob("summary_*上海一中*.md"))
    print(f"\nTotal files after cleanup: {len(final_files)}")

if __name__ == "__main__":
    main()
