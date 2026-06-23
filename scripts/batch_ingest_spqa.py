#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch ingest 最高检-答记者问-md files to wiki/summaries/
181 files processing with checkpoint support.
"""
from __future__ import print_function

import os
import re
import json
import sys
from pathlib import Path

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import os
import re
import json
from pathlib import Path

# VAULT_ROOT 多平台兼容（patched 2026-06-23）：
# 1. 优先 TKK_VAULT_ROOT 环境变量
# 2. Windows: "D:/AI agent/tkk-library"
# 3. Linux/WSL: /home/kangkang/tkk-library 等候选按存在性自动探测
_VAULT_CANDIDATES = [
    os.environ.get("TKK_VAULT_ROOT"),
    "D:/AI agent/tkk-library" if os.name == "nt" else None,
    "/home/kangkang/tkk-library",
    "/mnt/d/AI agent/tkk-library",
    "/mnt/c/Users/汤康康/tkk-library",
]
VAULT_ROOT = next(
    (Path(p) for p in _VAULT_CANDIDATES if p and Path(p).exists()),
    Path(os.environ.get("TKK_VAULT_ROOT", "D:/AI agent/tkk-library"))
)
SOURCE_DIR = VAULT_ROOT / "sources/微信公号资料/最高人民检察院/最高检-答记者问-md"
TARGET_DIR = VAULT_ROOT / "wiki/summaries"
CHECKPOINT_FILE = VAULT_ROOT / "wiki/.checkpoints/最高检_答记者问_ingest.json"

def extract_date_from_filename(filename):
    """Extract date from [YYYY-MM-DD] prefix in filename."""
    match = re.match(r'\[(\d{4}-\d{2}-\d{2})\]', filename)
    return match.group(1) if match else None

def extract_title(content):
    """Extract title from first # heading."""
    match = re.search(r'^#\s*(.+)$', content, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        # Remove leading/trailing whitespace and normalize
        title = re.sub(r'\s+', ' ', title)
        return title
    return None

def extract_key_points(content):
    """Extract key points from Q&A content."""
    points = []

    # Split by question markers
    qa_pattern = re.compile(r'\*\*问：\*\*(.+?)\*\*答：\*\*(.+?)(?=\*\*问：\*\*|$)', re.DOTALL)
    matches = qa_pattern.findall(content)

    for i, (question, answer) in enumerate(matches[:6], 1):
        # Clean up the answer text
        answer = answer.strip()
        answer = re.sub(r'\s+', ' ', answer)
        # Truncate if too long
        if len(answer) > 300:
            answer = answer[:300] + "..."
        if len(answer) > 50:
            points.append(f"Q{i}: {answer}")

    return points[:8]  # Max 8 points

def clean_title_for_filename(title):
    """Clean title for use in filename."""
    # Remove special characters but keep Chinese, numbers, letters
    cleaned = re.sub(r'[（[】\[\]（）【】]', '', title)
    cleaned = re.sub(r'\s+', '', cleaned)
    if len(cleaned) > 60:
        cleaned = cleaned[:60]
    return cleaned

def process_file(src_path, tgt_path):
    """Process a single file."""
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()

    title = extract_title(content)
    if not title:
        return None, "No title found"

    date = extract_date_from_filename(src_path.name)
    if not date:
        return None, "No date found"

    key_points = extract_key_points(content)

    # Build frontmatter
    filename_date = date.replace('-', '')
    clean_title = clean_title_for_filename(title)
    target_filename = f"summary_{filename_date}_最高检_答记者问_{clean_title}.md"
    target_path = tgt_path / target_filename

    # Create frontmatter
    year = date[:4]
    tags = ["最高人民检察院", "答记者问", "检察工作"]

    frontmatter = f"""---
title: {title}
type: summary
created: 2026-05-11
updated: 2026-05-11
tags: [{', '.join(tags)}]
category: 刑事参考
source: sources/微信公号资料/最高人民检察院/最高检-答记者问-md/{src_path.name}
related: []
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{src_path.name}]] |
| 类型 | 最高检答记者问 |
| 发布日期 | {date} |
| 关键词 | {' / '.join(tags)} |
| 知识点数 | {len(key_points)} 条 |

## 核心要点

"""
    for i, point in enumerate(key_points, 1):
        frontmatter += f"{i}. {point}\n"

    frontmatter += f"""
## 相关

- [[entity_最高人民检察院]]（待关联）

---

*本页面由机器自动整理自最高人民检察院官方发布*
"""

    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter)

    return target_filename, None

def main():
    # Ensure checkpoint dir
    CHECKPOINT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Load checkpoint if exists
    checkpoint = {}
    if CHECKPOINT_FILE.exists():
        try:
            checkpoint = json.loads(CHECKPOINT_FILE.read_text(encoding='utf-8'))
        except:
            checkpoint = {}

    processed = checkpoint.get('processed', [])
    failed = checkpoint.get('failed', [])

    print(f"Starting batch ingest: 181 files")
    print(f"Already processed: {len(processed)}, Failed: {len(failed)}")

    # Get all source files
    source_files = sorted(SOURCE_DIR.glob("*.md"))
    print(f"Found {len(source_files)} source files")

    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    results = {'success': 0, 'failed': 0, 'skipped': 0}

    for src_path in source_files:
        if src_path.name in processed:
            results['skipped'] += 1
            continue

        filename, error = process_file(src_path, TARGET_DIR)

        if error:
            failed.append({'file': src_path.name, 'error': error})
            results['failed'] += 1
            print(f"FAILED: {src_path.name} - {error}")
        else:
            processed.append(src_path.name)
            results['success'] += 1
            print(f"OK: {filename}")

        # Update checkpoint periodically
        if results['success'] % 20 == 0:
            checkpoint['processed'] = processed
            checkpoint['failed'] = failed
            CHECKPOINT_FILE.write_text(json.dumps(checkpoint, ensure_ascii=False), encoding='utf-8')

    # Final checkpoint
    checkpoint['processed'] = processed
    checkpoint['failed'] = failed
    CHECKPOINT_FILE.write_text(json.dumps(checkpoint, ensure_ascii=False), encoding='utf-8')

    print(f"\n=== RESULTS ===")
    print(f"Success: {results['success']}")
    print(f"Failed: {results['failed']}")
    print(f"Skipped (already processed): {results['skipped']}")
    print(f"Total: {results['success'] + results['failed'] + results['skipped']}")

    return results

if __name__ == '__main__':
    main()
