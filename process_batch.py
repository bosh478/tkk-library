#!/usr/bin/env python3
"""
Batch process Clippings files for tkk-library ingest.
Cleans website artifacts, writes to sources/, generates summaries.
"""
import os
import re
import shutil
from pathlib import Path
from datetime import datetime

CLIPPINGS_DIR = Path("D:/AI agent/tkk-library/Clippings")
SOURCES_DIR = Path("D:/AI agent/tkk-library/sources/网络文章")
SUMMARIES_DIR = Path("D:/AI agent/tkk-library/wiki/summaries")

# Ensure directories exist
SOURCES_DIR.mkdir(parents=True, exist_ok=True)
SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)

def extract_frontmatter(content):
    """Extract frontmatter dict from markdown content."""
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body = parts[2]
            fm = {}
            for line in fm_text.strip().split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    fm[key.strip()] = val.strip().strip('"').strip("'")
            return fm, body
    return {}, content

def extract_published_date(body):
    """Extract publication date from content (format: *YYYY年MM月DD日* or similar)."""
    patterns = [
        r'\*(\d{4})年(\d{1,2})月(\d{1,2})日',
        r'(\d{4})-(\d{2})-(\d{2})',
        r' (\d{4})(\d{2})(\d{2}) ',
    ]
    for p in patterns:
        m = re.search(p, body)
        if m:
            if len(m.groups()) == 3:
                y, mo, d = m.groups()
                return f"{y}-{int(mo):02d}-{int(d):02d}"
    return None

def clean_lawyers_org_content(content):
    """
    Clean content from lawyers.org.cn (东方律师网).
    Remove: breadcrumb nav, committee links, editor info, trailing artifacts.
    """
    lines = content.split('\n')
    cleaned_lines = []
    skip_mode = False
    in_committee_block = False

    for i, line in enumerate(lines):
        # Skip empty lines at start
        if not cleaned_lines and line.strip() == '':
            continue

        # Stop conditions (trailing artifacts)
        if line.strip() in ['---', '<!--']:
            break
        if re.match(r'^\s*<!--|^\s*\*+\s*$', line):
            break
        if line.strip().startswith('编辑：') or line.strip().startswith('审校：') or line.strip().startswith('采写：') or line.strip().startswith('编校：'):
            break
        if '向上滑动看下一个' in line or '继续滑动看下一个' in line:
            break
        if line.strip().startswith('广东省高级人民法院') and len(line.strip()) < 20:
            break

        # Detect breadcrumb navigation start
        if '当前位置' in line and 'lawyers.org.cn' in line:
            skip_mode = True
            continue

        # Detect committee links block start (| ESG | 保险 | ...)
        if re.match(r'^\s*\|.*\|\s*$', line) and ('ESG' in line or '保险' in line or '并购' in line):
            in_committee_block = True
            continue

        # End of committee block (empty line or non-link line)
        if in_committee_block:
            if line.strip() == '' or not re.match(r'^\s*\|', line):
                in_committee_block = False
            else:
                continue

        if skip_mode:
            # Skip until empty line (end of breadcrumb)
            if line.strip() == '':
                skip_mode = False
            continue

        cleaned_lines.append(line)

    # Remove trailing empty lines
    while cleaned_lines and cleaned_lines[-1].strip() == '':
        cleaned_lines.pop()

    return '\n'.join(cleaned_lines)

def extract_core_title(title):
    """Extract core title by removing website suffix."""
    title = re.sub(r'\s*-\s*业务指引\s*-\s*业务研究大厅\s*-\s*东方律师网\s*$', '', title)
    title = re.sub(r'\s*-\s*业务指引\s*-\s*业务研究大厅\s*-\s*东方律师网\s*\(.*\)\s*$', '', title)
    return title.strip()

def generate_summary_filename(core_title, date):
    """Generate summary filename."""
    safe_title = re.sub(r'[（）\[\]【】()【】]', '', core_title)
    safe_title = re.sub(r'\s+', '_', safe_title.strip())
    safe_title = safe_title[:50]
    return f"{date}_{safe_title}.md"

def process_file(filepath):
    """Process a single clipping file. Returns (success, source_file, summary_file, error)."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        fm, body = extract_frontmatter(content)
        title = fm.get('title', filepath.stem)
        source_url = fm.get('source', '')
        created = fm.get('created', '2026-04-14')

        # Clean body content
        cleaned_body = clean_lawyers_org_content(body)

        # Extract published date from content
        published_date = extract_published_date(cleaned_body)
        if not published_date:
            # Try frontmatter published
            published_date = fm.get('published', created)

        # Extract core title
        core_title = extract_core_title(title)

        # Generate filenames
        date_str = published_date.replace('-', '')[:10] if published_date else created.replace('-', '')[:10]
        source_filename = f"{date_str}_{core_title}.md"
        source_filename = re.sub(r'[<>:"/\\|?*]', '_', source_filename)
        source_filename = source_filename[:100]

        # Write cleaned source
        source_path = SOURCES_DIR / source_filename
        new_fm = f"""---
title: "{core_title}"
source: "{source_url}"
author:
published: "{published_date}"
created: "{created}"
description:
tags:
  - "clippings"
  - "律师业务指引"
---

{cleaned_body}"""

        # Handle duplicate filenames
        counter = 1
        original_source_path = source_path
        while source_path.exists():
            source_filename = f"{date_str}_{core_title}_{counter}.md"
            source_filename = re.sub(r'[<>:"/\\|?*]', '_', source_filename)[:100]
            source_path = SOURCES_DIR / source_filename
            counter += 1

        with open(source_path, 'w', encoding='utf-8') as f:
            f.write(new_fm)

        # Generate summary
        summary_filename = f"{date_str}_{core_title}.md"
        summary_filename = re.sub(r'[<>:"/\\|?*]', '_', summary_filename)[:100]
        summary_path = SUMMARIES_DIR / summary_filename

        counter = 1
        original_summary_path = summary_path
        while summary_path.exists():
            summary_filename = f"{date_str}_{core_title}_{counter}.md"
            summary_filename = re.sub(r'[<>:"/\\|?*]', '_', summary_filename)[:100]
            summary_path = SUMMARIES_DIR / summary_filename
            counter += 1

        # Extract key points for summary (first 3-5 bullet-worthy sections)
        summary_content = generate_summary(cleaned_body, core_title, published_date, source_filename)

        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)

        return (True, source_path.name, summary_path.name, None)

    except Exception as e:
        return (False, filepath.name, None, str(e))

def generate_summary(body, title, date, source_name):
    """Generate summary content from cleaned body."""
    # Extract first few paragraphs or sections as key points
    lines = body.split('\n')
    key_points = []

    # Look for numbered sections or headings
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Skip the title/date line at top
        if line.startswith('## ') or line.startswith('**'):
            continue
        if '日期：' in line or '*20' in line:
            continue
        # Collect substantive paragraphs
        if len(line) > 20 and len(key_points) < 5:
            # Truncate long lines
            if len(line) > 150:
                line = line[:150] + '...'
            key_points.append(f"- {line}")

    key_points_text = '\n'.join(key_points) if key_points else "- 内容已清洗存档，请查阅来源文件"

    return f"""---
title: {title}
type: summary
created: 2026-04-14
updated: 2026-04-14
tags: [律师业务指引]
source: [[{source_name}]]
---

## 关键要点

{key_points_text}

## 相关链接
- [[{source_name}]]
"""

def main():
    print("=" * 60)
    print("tkk-library Batch Ingest")
    print("=" * 60)

    # Get all md files in Clippings
    clipping_files = list(CLIPPINGS_DIR.glob("*.md"))
    print(f"\nFound {len(clipping_files)} files in Clippings/")

    # Filter out already processed (skip if source already exists with good size)
    results = []
    skipped = 0
    processed = 0

    for fp in clipping_files:
        # Quick check: if corresponding source exists and is > 5KB, likely already done
        potential_source = SOURCES_DIR / fp.name
        if potential_source.exists():
            size = potential_source.stat().st_size
            if size > 5000:
                print(f"  SKIP (already done): {fp.name} ({size} bytes)")
                skipped += 1
                continue

        success, source_fn, summary_fn, err = process_file(fp)
        if success:
            results.append((fp.name, source_fn, summary_fn))
            processed += 1
            print(f"  OK: {fp.name} -> {source_fn}")
        else:
            print(f"  FAIL: {fp.name} -> {err}")

    print(f"\n{'=' * 60}")
    print(f"Summary: {processed} processed, {skipped} skipped, {len(results)} results")
    print(f"Sources: {SOURCES_DIR}")
    print(f"Summaries: {SUMMARIES_DIR}")

    return results

if __name__ == "__main__":
    main()
