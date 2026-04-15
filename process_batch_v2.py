#!/usr/bin/env python3
"""
Improved batch processor for tkk-library Clippings.
Accurate pattern matching for 东方律师网 format.
"""
import os
import re
import shutil
from pathlib import Path
from datetime import datetime

CLIPPINGS_DIR = Path("D:/AI agent/tkk-library/Clippings")
SOURCES_DIR = Path("D:/AI agent/tkk-library/sources/网络文章")
SUMMARIES_DIR = Path("D:/AI agent/tkk-library/wiki/summaries")
CLEANUP_SOURCES = True  # Clean up bad sources from previous run

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
    """Extract publication date from content - try multiple patterns."""
    patterns = [
        r'### 日期：(\d{4})-(\d{2})-(\d{2})',
        r'\*(\d{4})年(\d{1,2})月(\d{1,2})日',
        r'\((\d{4})年(\d{1,2})月(\d{1,2})日',
        r' (\d{4})-(\d{2})-(\d{2}) ',
    ]
    for p in patterns:
        m = re.search(p, body)
        if m:
            y, mo, d = m.groups()
            return f"{y}-{int(mo):02d}-{int(d):02d}"
    return None

def clean_lawyers_org_content(filepath, body):
    """
    Clean content from lawyers.org.cn (东方律师网).
    Strategy:
    - Find the first real content heading (## 律师从事... or ## 律师代理...)
    - Include content until "常用工具" or similar trailing navigation section
    - Remove: breadcrumb nav, committee links, trailing nav, editor info
    """
    lines = body.split('\n')

    # Find where real content starts (first ## heading after frontmatter)
    content_start = 0
    for i, line in enumerate(lines):
        if re.match(r'^## \u5f8b\u5e08[\u4ece\u4ee3\u7406\u529e\u7406]', line):  # ## 律师从事/代理/办理
            content_start = i
            break
        # Also match ## 广东省高级人民法院 etc for official docs
        if re.match(r'^## \u5e7f\u4e1c\u7701\u9ad8\u7b49\u4eba\u6c11\u6cd5\u9662', line):
            content_start = i
            break

    if content_start == 0:
        # Fallback: start after frontmatter
        for i, line in enumerate(lines):
            if line.strip() == '' and i > 5:
                content_start = i + 1
                break

    # Find where trailing junk starts
    trailing_markers = [
        '常用工具',
        '继续滑动看下一个',
        '向上滑动看下一个',
        '编辑：',
        '审校：',
        '采写：',
        '编校：',
    ]

    content_end = len(lines)
    for i, line in enumerate(lines[content_start:], start=content_start):
        for marker in trailing_markers:
            if marker in line:
                content_end = i
                break
        if content_end != len(lines):
            break

    # Extract cleaned content
    cleaned_lines = lines[content_start:content_end]

    # Remove trailing empty lines
    while cleaned_lines and cleaned_lines[-1].strip() == '':
        cleaned_lines.pop()

    return '\n'.join(cleaned_lines)

def extract_core_title(title):
    """Extract core title by removing website suffix."""
    title = re.sub(r'\s*-\s*业务指引\s*-\s*业务研究大厅\s*-\s*东方律师网\s*$', '', title)
    title = re.sub(r'\s*-\s*业务指引\s*-\s*业务研究大厅\s*-\s*东方律师网\s*\(.*\)\s*$', '', title)
    title = re.sub(r'\s*（附全文）\s*$', '', title)
    return title.strip()

def generate_safe_filename(title, date_str):
    """Generate safe filename from title and date."""
    safe = re.sub(r'[<>:"/\\|?*（）()【】\[\]]', '', title)
    safe = re.sub(r'\s+', '_', safe.strip())
    safe = safe[:80]
    return f"{date_str}_{safe}.md"

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
        cleaned_body = clean_lawyers_org_content(filepath, body)

        # Extract published date from content
        published_date = extract_published_date(cleaned_body)
        if not published_date:
            published_date = fm.get('published', created)
        if not published_date:
            published_date = created

        # Extract core title
        core_title = extract_core_title(title)

        # Generate date string for filename
        date_for_file = published_date.replace('-', '')

        # Generate source filename
        source_filename = generate_safe_filename(core_title, date_for_file)
        source_path = SOURCES_DIR / source_filename

        # Handle duplicate filenames
        counter = 1
        while source_path.exists():
            source_filename = generate_safe_filename(core_title, f"{date_for_file}_{counter}")
            source_path = SOURCES_DIR / source_filename
            counter += 1

        # Write cleaned source
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

        with open(source_path, 'w', encoding='utf-8') as f:
            f.write(new_fm)

        # Generate summary
        summary_filename = generate_safe_filename(core_title, date_for_file)
        summary_path = SUMMARIES_DIR / summary_filename

        counter = 1
        while summary_path.exists():
            summary_filename = generate_safe_filename(core_title, f"{date_for_file}_{counter}")
            summary_path = SUMMARIES_DIR / summary_filename
            counter += 1

        summary_content = generate_summary(cleaned_body, core_title, published_date, source_filename)

        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)

        return (True, source_path.name, summary_path.name, published_date, len(cleaned_body), None)

    except Exception as e:
        return (False, filepath.name, None, None, 0, str(e))

def generate_summary(body, title, date, source_name):
    """Generate summary content from cleaned body."""
    lines = body.split('\n')
    key_points = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Skip heading markers and date lines
        if line.startswith('#') or '日期：' in line or re.match(r'\*20', line):
            continue
        # Collect substantive paragraphs
        if len(line) > 30 and len(key_points) < 6:
            if len(line) > 200:
                line = line[:200] + '...'
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

def cleanup_bad_sources():
    """Remove source files smaller than 5KB (likely truncated from previous run)."""
    removed = 0
    for f in SOURCES_DIR.glob("*.md"):
        if f.stat().st_size < 5000:
            # Check if there's a corresponding good file
            good_file = None
            base_name = f.stem
            for candidate in SOURCES_DIR.glob("*.md"):
                if candidate.stem.startswith(base_name.split('_')[0]) and candidate != f:
                    if candidate.stat().st_size > 5000:
                        good_file = candidate
                        break
            if good_file:
                print(f"  REMOVE (truncated): {f.name} ({f.stat().st_size} bytes) - keep {good_file.name}")
                f.unlink()
                removed += 1
            else:
                print(f"  WARN (small): {f.name} ({f.stat().st_size} bytes)")
    print(f"  Cleaned up {removed} truncated files")
    return removed

def main():
    print("=" * 60)
    print("tkk-library Batch Ingest v2")
    print("=" * 60)

    # Cleanup bad sources from previous run
    if CLEANUP_SOURCES:
        print("\n[Cleanup phase]")
        cleanup_bad_sources()

    # Get all md files in Clippings
    clipping_files = list(CLIPPINGS_DIR.glob("*.md"))
    print(f"\n[Processing] Found {len(clipping_files)} files in Clippings/")

    results = []
    failed = []

    for fp in clipping_files:
        success, source_fn, summary_fn, pub_date, body_len, err = process_file(fp)
        if success:
            results.append((fp.name, source_fn, summary_fn, pub_date, body_len))
            print(f"  OK [{pub_date}] {source_fn} ({body_len} chars)")
        else:
            failed.append((fp.name, err))
            print(f"  FAIL: {fp.name} -> {err}")

    print(f"\n{'=' * 60}")
    print(f"Results: {len(results)} ok, {len(failed)} failed")
    print(f"Sources: {SOURCES_DIR} ({len(list(SOURCES_DIR.glob('*.md')))} files)")
    print(f"Summaries: {SUMMARIES_DIR} ({len(list(SUMMARIES_DIR.glob('*.md')))} files)")

    if failed:
        print(f"\nFailed files:")
        for fn, err in failed:
            print(f"  - {fn}: {err}")

    return results

if __name__ == "__main__":
    main()
