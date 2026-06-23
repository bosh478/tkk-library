#!/usr/bin/env python3
"""Batch process Supreme Court public account articles into wiki summaries."""

import re
import os
from pathlib import Path
from datetime import datetime

VAULT = Path("D:/AI agent/tkk-library")
SOURCES = VAULT / "sources/微信公号资料/最高人民法院"

DIRS = {
    "最高法-凡人小事-md": {
        "prefix": "Summary_凡人小事_",
        "category": "诉讼与仲裁",
        "tags": ["凡人小事", "最高人民法院", "案例故事"]
    },
    "最高法-前沿法评-md": {
        "prefix": "Summary_前沿法评_",
        "category": "知识产权",
        "tags": ["前沿法评", "最高人民法院", "法学评论"]
    },
    "最高法-小案大道理-md": {
        "prefix": "Summary_小案大道理_",
        "category": "诉讼与仲裁",
        "tags": ["小案大道理", "最高人民法院", "案例解读"]
    },
    "最高法-法答网精选答问-md": {
        "prefix": "Summary_法答网精选_",
        "category": "知识产权",
        "tags": ["法答网精选", "最高人民法院", "法律问答"],
        "multi_qa": True
    },
}

def extract_date_from_filename(filename):
    """Extract date from [YYYY-MM-DD] prefix in filename."""
    match = re.match(r"\[(\d{4}-\d{2}-\d{2})\](.+)\.md", filename)
    if match:
        return match.group(1), match.group(2).strip()
    return None, filename.replace(".md", "")

def extract_title_and_content(content):
    """Extract title and core content from file."""
    lines = content.split("\n")
    title = ""
    body_lines = []
    in_body = False

    for i, line in enumerate(lines):
        line = line.strip()
        if not title and line.startswith("#"):
            title = line.lstrip("#").strip()
            continue
        if line.startswith("**") and "来源" in line or line.startswith("来源："):
            break
        if title and line:
            body_lines.append(line)
            in_body = True
        elif in_body and not line:
            continue
        elif in_body and line:
            body_lines.append(line)

    body = "\n\n".join(body_lines[:20])
    return title, body

def process_fada_file(src_path, dst_dir, config):
    """Process 法答网精选 file with multiple Q&A."""
    filename = src_path.name
    content = src_path.read_text(encoding="utf-8")

    # Extract batch name from first line
    title_match = re.search(r"法答网精选答问（第[一二三四五六七八九十百]+批）", content)
    batch_name = title_match.group() if title_match else "未知批次"

    # Extract each Q&A - non-greedy match to handle multi-line titles
    qa_pattern = r"\*\*\s*问题(\d+)[:：]\s*(.+?)\s*\*\*"
    matches = list(re.finditer(qa_pattern, content))

    if not matches:
        # Fallback: treat entire file as one entry
        return [process_single_fada(src_path, dst_dir, config, content, filename, "1", filename)]

    results = []
    for i, match in enumerate(matches):
        qa_num = match.group(1)
        qa_title = match.group(2).strip()

        # Get content between this Q and next Q (or end)
        start = match.end()
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(content)

        qa_content = content[start:end]

        result = process_single_fada(src_path, dst_dir, config, qa_content, filename, qa_num, qa_title)
        results.append(result)

    return results

def process_single_fada(src_path, dst_dir, config, content, orig_filename, qa_num, qa_title):
    """Process a single Q&A from 法答网精选."""
    # Extract date from footer or use a placeholder
    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", content)
    date = date_match.group(1) if date_match else "2025-01-01"

    # Extract key info
    answer_lines = []
    in_answer = False
    expert_lines = []

    for line in content.split("\n"):
        line = line.strip()
        if "**答疑意见：**" in line or line.startswith("答疑意见："):
            in_answer = True
            continue
        if "**点评专家：**" in line or line.startswith("点评专家："):
            in_answer = False
            continue
        if in_answer and line and not line.startswith("**"):
            answer_lines.append(line)
        if line.startswith("**点评专家：") or line.startswith("点评意见："):
            break

    answer = "\n\n".join(answer_lines[:15]) if answer_lines else "（内容提取中）"

    # Clean title
    clean_title = re.sub(r"[^\w\s一-鿿]", "", qa_title)[:50]

    dst_name = f"{config['prefix']}{qa_num.zfill(2)}_{clean_title}.md"
    dst_path = dst_dir / dst_name

    counter = 1
    while dst_path.exists():
        dst_name = f"{config['prefix']}{qa_num.zfill(2)}_{clean_title}_{counter}.md"
        dst_path = dst_dir / dst_name
        counter += 1

    frontmatter = f"""---
title: {qa_title}
type: summary
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
tags: {config['tags']}
source: [[{orig_filename}]]
category: {config['category']}
---

## 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | {orig_filename} |
| 编号 | 问题{qa_num} |
| 发布日期 | {date} |
| 类型 | 法律问答 |

## 问题

{qa_title}

## 答疑意见

{answer[:2000]}
"""

    try:
        dst_path.write_text(frontmatter, encoding="utf-8")
        return True
    except Exception as e:
        print(f"  Error writing {dst_name}: {e}")
        return False

def process_file(src_path, dst_dir, config):
    """Process single file to summary page."""
    filename = src_path.name
    date, base_name = extract_date_from_filename(filename)

    if not date:
        print(f"  Cannot parse date from: {filename}")
        return False

    try:
        content = src_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  Error reading {filename}: {e}")
        return False

    title, body = extract_title_and_content(content)

    if not title:
        title = base_name

    title = re.sub(r"[\[【\[].*?[\]】\]]", "", title).strip()
    title = re.sub(r"^[【\[].*?[\]】]", "", title).strip()

    clean_base = re.sub(r"[^\w\s一-鿿-]", "", base_name)[:50]
    dst_name = f"{config['prefix']}{date}_{clean_base}.md"
    dst_path = dst_dir / dst_name

    counter = 1
    while dst_path.exists():
        dst_name = f"{config['prefix']}{date}_{clean_base}_{counter}.md"
        dst_path = dst_dir / dst_name
        counter += 1

    doc_type = '法律问答' if '法答网' in config['prefix'] else '案例故事' if '凡人小事' in config['prefix'] else '案例解读' if '小案大道理' in config['prefix'] else '法学评论'

    frontmatter = f"""---
title: {title}
type: summary
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
tags: {config['tags']}
source: [[{filename}]]
category: {config['category']}
---

## 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | {filename} |
| 发布日期 | {date} |
| 类型 | {doc_type} |

## 核心内容

{body[:2000] if body else '（内容提取中）'}
"""

    try:
        dst_path.write_text(frontmatter, encoding="utf-8")
        return True
    except Exception as e:
        print(f"  Error writing {dst_name}: {e}")
        return False

def main():
    """Process all directories."""
    wiki_summaries = VAULT / "wiki/summaries"
    wiki_summaries.mkdir(parents=True, exist_ok=True)

    total_processed = 0
    total_failed = 0

    for dir_name, config in DIRS.items():
        src_dir = SOURCES / dir_name
        if not src_dir.exists():
            print(f"Directory not found: {src_dir}")
            continue

        files = list(src_dir.glob("*.md"))
        print(f"\nProcessing {dir_name}: {len(files)} files")

        processed = 0
        failed = 0

        for src_file in files:
            if config.get("multi_qa"):
                results = process_fada_file(src_file, wiki_summaries, config)
                processed += sum(1 for r in results if r)
                failed += sum(1 for r in results if not r)
            else:
                if process_file(src_file, wiki_summaries, config):
                    processed += 1
                else:
                    failed += 1

        print(f"  Processed: {processed}, Failed: {failed}")
        total_processed += processed
        total_failed += failed

    print(f"\n{'='*50}")
    print(f"Total processed: {total_processed}, Failed: {total_failed}")

if __name__ == "__main__":
    main()
