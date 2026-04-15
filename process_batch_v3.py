#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch process Clippings files for tkk-library ingest.
Accurate pattern matching for lawyers.org.cn format.
"""
import os
import re
from pathlib import Path

CLIPPINGS_DIR = Path("D:/AI agent/tkk-library/Clippings")
SOURCES_DIR = Path("D:/AI agent/tkk-library/sources/网络文章")
SUMMARIES_DIR = Path("D:/AI agent/tkk-library/wiki/summaries")
CLEANUP_MODE = True  # Clean truncated/duplicate files

SOURCES_DIR.mkdir(parents=True, exist_ok=True)
SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)

def extract_frontmatter(content):
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
    patterns = [
        r'### 日期：(\d{4})-(\d{2})-(\d{2})',
        r'\((\d{4})年(\d{1,2})月(\d{1,2})日',
    ]
    for p in patterns:
        m = re.search(p, body)
        if m:
            y, mo, d = m.groups()
            return f"{y}-{int(mo):02d}-{int(d):02d}"
    return None

def clean_lawyers_org_content(body):
    lines = body.split('\n')

    # Find where real content starts
    # Chinese headings: 律师从事, 律师代理, 律师办理, 广东省高级人民法院
    content_start = 0
    content_heading_chars = ['律师从事', '律师代理', '律师办理', '广东省高级人民法院']

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('## '):
            for heading in content_heading_chars:
                if heading in stripped:
                    content_start = i
                    break
            if content_start > 0:
                break

    if content_start == 0:
        # Fallback: find first non-empty line after line 5
        for i, line in enumerate(lines):
            if i > 5 and line.strip():
                content_start = i
                break

    # Find trailing junk
    trailing_markers = ['常用工具', '继续滑动看下一个', '向上滑动看下一个',
                       '编辑：', '审校：', '采写：', '编校：']
    content_end = len(lines)
    for i, line in enumerate(lines[content_start:], start=content_start):
        for marker in trailing_markers:
            if marker in line:
                content_end = i
                break
        if content_end != len(lines):
            break

    cleaned_lines = lines[content_start:content_end]
    while cleaned_lines and cleaned_lines[-1].strip() == '':
        cleaned_lines.pop()

    return '\n'.join(cleaned_lines)

def extract_core_title(title):
    title = re.sub(r'\s*-\s*业务指引\s*-\s*业务研究大厅\s*-\s*东方律师网\s*$', '', title)
    title = re.sub(r'\s*（附全文）\s*$', '', title)
    return title.strip()

def safe_filename(title, date_str):
    safe = re.sub(r'[<>:"/\\|?*（）()【】\[\]]', '', title)
    safe = re.sub(r'\s+', '_', safe.strip())
    safe = safe[:80]
    return f"{date_str}_{safe}.md"

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        fm, body = extract_frontmatter(content)
        title = fm.get('title', filepath.stem)
        source_url = fm.get('source', '')
        created = fm.get('created', '2026-04-14')

        cleaned_body = clean_lawyers_org_content(body)
        published_date = extract_published_date(cleaned_body)
        if not published_date:
            published_date = fm.get('published', created)
        if not published_date:
            published_date = created

        core_title = extract_core_title(title)
        date_for_file = published_date.replace('-', '')

        source_filename = safe_filename(core_title, date_for_file)
        source_path = SOURCES_DIR / source_filename

        counter = 1
        while source_path.exists():
            source_filename = safe_filename(core_title, f"{date_for_file}_{counter}")
            source_path = SOURCES_DIR / source_filename
            counter += 1

        new_fm = f'''---
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

{cleaned_body}'''

        with open(source_path, 'w', encoding='utf-8') as f:
            f.write(new_fm)

        summary_filename = safe_filename(core_title, date_for_file)
        summary_path = SUMMARIES_DIR / summary_filename
        counter = 1
        while summary_path.exists():
            summary_filename = safe_filename(core_title, f"{date_for_file}_{counter}")
            summary_path = SUMMARIES_DIR / summary_filename
            counter += 1

        summary_content = generate_summary(cleaned_body, core_title, published_date, source_filename)
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)

        return (True, source_path.name, summary_path.name, published_date, len(cleaned_body), None)
    except Exception as e:
        return (False, filepath.name, None, None, 0, str(e))

def generate_summary(body, title, date, source_name):
    lines = body.split('\n')
    key_points = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#') or '日期：' in line:
            continue
        if len(line) > 30 and len(key_points) < 6:
            if len(line) > 200:
                line = line[:200] + '...'
            key_points.append(f"- {line}")

    kp_text = '\n'.join(key_points) if key_points else "- 内容已清洗存档，请查阅来源文件"
    return f'''---
title: {title}
type: summary
created: 2026-04-14
updated: 2026-04-14
tags: [律师业务指引]
source: [[{source_name}]]
---

## 关键要点

{kp_text}

## 相关链接
- [[{source_name}]]
'''

def cleanup():
    """Remove truncated source files (< 1KB) and duplicate date files."""
    removed = 0
    all_sources = list(SOURCES_DIR.glob("*.md"))

    # Remove files smaller than 500 bytes
    for f in all_sources:
        if f.stat().st_size < 500:
            print(f"  REMOVE (too small {f.stat().st_size}b): {f.name}")
            f.unlink()
            removed += 1

    # For files with 20260414 date (fallback), check if there's a better version
    fallback_files = [f for f in SOURCES_DIR.glob("20260414_*.md")]
    for ff in fallback_files:
        # Look for a file with same title but different date
        base_name = ff.stem[9:]  # Remove "20260414_"
        for other in SOURCES_DIR.glob(f"*_{base_name}"):
            if other != ff and other.stat().st_size > ff.stat().st_size * 2:
                print(f"  REMOVE (fallback date, keep {other.name}): {ff.name}")
                ff.unlink()
                removed += 1
                break

    # Remove duplicate small files from previous run (with _1, _2 suffixes)
    for f in SOURCES_DIR.glob("*_1.md"):
        if f.stat().st_size < 5000:
            print(f"  REMOVE (dup small): {f.name}")
            f.unlink()
            removed += 1

    print(f"  Cleaned up {removed} files")
    return removed

def main():
    print("=" * 60)
    print("tkk-library Batch Ingest v3")
    print("=" * 60)

    if CLEANUP_MODE:
        print("\n[Cleanup]")
        cleanup()

    clipping_files = list(CLIPPINGS_DIR.glob("*.md"))
    print(f"\n[Processing] {len(clipping_files)} files")

    results = []
    failed = []

    for fp in clipping_files:
        ok, src, smry, pub, chars, err = process_file(fp)
        if ok:
            results.append((fp.name, src, smry, pub, chars))
            print(f"  OK [{pub}] {chars:6d} chars -> {src}")
        else:
            failed.append((fp.name, err))
            print(f"  FAIL: {fp.name} -> {err}")

    src_count = len(list(SOURCES_DIR.glob("*.md")))
    smry_count = len(list(SUMMARIES_DIR.glob("*.md")))
    print(f"\n{'=' * 60}")
    print(f"Done: {len(results)} ok, {len(failed)} failed")
    print(f"Sources: {src_count} | Summaries: {smry_count}")

if __name__ == "__main__":
    main()
