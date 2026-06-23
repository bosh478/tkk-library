#!/usr/bin/env python3
"""
Batch ingest SPP Q&A (答记者问) files from sources to wiki/summaries/
Usage: python batch_ingest_spq_qa.py
"""

import os
import re
import shutil
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
LOG_FILE = VAULT_ROOT / "log.md"

def extract_title(content):
    """Extract title from # line"""
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('#'):
            # Remove # and extra spaces, get title
            title = line.lstrip('#').strip()
            return title
    return None

def clean_title(title):
    """Clean title for target filename and frontmatter"""
    # Remove leading date pattern [YYYY-MM-DD] or YYYY-MM-DD
    title = re.sub(r'^\[?\d{4}-\d{2}-\d{2}\]?\s*', '', title)
    # Remove 答记者问 suffix
    title = re.sub(r'[\s_]*答记者问\s*$', '', title)
    # Remove trailing .md if any
    title = title.rstrip('.md')
    return title.strip()

def generate_summary_filename(title, date_prefix=""):
    """Generate target filename"""
    if date_prefix:
        return f"summary_SPP_答记者问_{date_prefix}{title}.md"
    return f"summary_SPP_答记者问_{title}.md"

def extract_date_from_filename(filename):
    """Extract date from source filename like [2018-11-18]xxx.md"""
    match = re.match(r'\[(\d{4}-\d{2}-\d{2})\]', filename)
    if match:
        return match.group(1)
    return ""

def extract_key_content(content, title):
    """
    Extract key content from Q&A article.
    Returns structured content for wiki page.
    """
    lines = content.split('\n')

    # Find key Q&A pairs (those marked with 问： and 答：)
    key_points = []
    current_q = None
    current_a = []
    in_answer = False

    for line in lines:
        line = line.strip()
        if line.startswith('**问：**') or line.startswith('问：'):
            if current_q and current_a:
                key_points.append((current_q, '\n'.join(current_a)))
            current_q = re.sub(r'^\*\*问：\*?\*?\s*', '', line).strip()
            current_a = []
            in_answer = False
        elif line.startswith('**答：**') or line.startswith('答：'):
            in_answer = True
            answer_text = re.sub(r'^\*\*答：\*?\*?\s*', '', line).strip()
            if answer_text:
                current_a.append(answer_text)
        elif in_answer and line and not line.startswith('#') and not line.startswith('（') and not line.startswith('预览'):
            if line.startswith('➤') or line.startswith('*') or line.startswith('一、') or line.startswith('二、') or line.startswith('三、'):
                current_a.append(line)
            elif current_a and not line.startswith('**') and not line.startswith('问') and not line.startswith('答'):
                # Continuation of answer
                current_a.append(line)

    if current_q and current_a:
        key_points.append((current_q, '\n'.join(current_a)))

    return key_points

def create_wiki_page(source_file, target_file, title, content, date_str):
    """Create wiki summary page"""

    # Extract key points
    key_points = extract_key_content(content, title)

    # Build frontmatter
    frontmatter = f"""---
title: "最高检{title}答记者问"
type: summary
created: 2026-05-11
updated: 2026-05-11
tags: [答记者问, 最高人民检察院, 检察政策, 刑事参考]
category: 刑事参考
source: [[{source_file.name}]]
related: []
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{source_file.name}]] |
| 类型 | 答记者问/政策解读 |
| 发布日期 | {date_str} |
| 关键词 | 最高人民检察院 / 检察政策 / 司法解释 / 指导性案例 |
| 核心要点 | {len(key_points)} 个问答 |

## 关键内容

"""

    # Add key Q&A content
    for i, (q, a) in enumerate(key_points[:8], 1):  # Limit to 8 Q&A pairs
        if q and a:
            frontmatter += f"### {i}. {q}\n\n{a[:500]}..." if len(a) > 500 else f"### {i}. {q}\n\n{a}\n\n"

    # Add footer
    frontmatter += f"""
---

*本页面由机器自动从 [[{source_file.name}]] 提取生成*
"""

    # Write file
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(frontmatter)

    return len(key_points)

def main():
    # Get source files
    source_files = sorted(SOURCE_DIR.glob("*.md"))
    print(f"Total source files: {len(source_files)}")

    # Count existing target files
    existing = list(TARGET_DIR.glob("summary_SPP_答记者问_*.md"))
    print(f"Existing target files: {len(existing)}")

    # Process files
    processed = 0
    errors = 0

    for source_file in source_files:
        try:
            # Generate target filename
            date_str = extract_date_from_filename(source_file.name)
            content = source_file.read_text(encoding='utf-8')
            raw_title = extract_title(content)

            if not raw_title:
                print(f"  [WARN] Could not extract title from {source_file.name}")
                errors += 1
                continue

            cleaned_title = clean_title(raw_title)
            target_filename = generate_summary_filename(cleaned_title, date_str[:10] + "_" if date_str else "")
            target_file = TARGET_DIR / target_filename

            # Skip if exists
            if target_file.exists():
                print(f"  [SKIP] Skip existing: {target_filename}")
                continue

            # Create wiki page
            q_count = create_wiki_page(source_file, target_file, cleaned_title, content, date_str)
            print(f"  [OK] Created: {target_filename} ({q_count} Q&A)")
            processed += 1

        except Exception as e:
            print(f"  [ERROR] Error processing {source_file.name}: {e}")
            errors += 1

    print(f"\n=== Summary ===")
    print(f"Processed: {processed}")
    print(f"Errors: {errors}")
    print(f"Total source: {len(source_files)}")
    print(f"Existing target: {len(existing)}")
    print(f"New files created: {processed}")

if __name__ == "__main__":
    main()