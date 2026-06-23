#!/usr/bin/env python3
"""
Batch process 今晚九点半 articles from 最高人民检察院
Extract title, tags, key points, and create wiki/summaries files
"""
import os
import re
from pathlib import Path
from datetime import datetime

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
SOURCE_DIR = VAULT_ROOT / "sources/微信公号资料/最高人民检察院/最高检-今晚九点半-md"
TARGET_DIR = VAULT_ROOT / "wiki/summaries"

# Tags mapping for these articles
CATEGORY = "刑事参考"

def extract_title(content):
    """Extract title from first # heading"""
    match = re.search(r'^#\s+(.+)｜今晚九点半', content, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        # Remove any leading/trailing whitespace and special chars
        title = re.sub(r'^[\s　]+|[\s　]+$', '', title)
        return title
    # Fallback: just get first # heading
    match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "未命名"

def extract_date_from_filename(filename):
    """Extract date from filename like [2025-09-20]xxx.md"""
    match = re.search(r'\[(\d{4}-\d{2}-\d{2})\]', filename)
    if match:
        return match.group(1)
    return "2025-01-01"

def extract_key_points(content):
    """Extract at least 5 key points from content"""
    points = []

    # Extract sentences with important facts
    # Look for sentences with numbers, specific details
    lines = content.split('\n')
    important_patterns = [
        r'(\d+[多余亿千万百个名/人/元/万元]+)',
        r'(构成?[男女]?罪)',
        r'(判处.*?[年个月]+)',
        r'(检察院|法院|公安)',
        r'(正当防卫|防卫过当|故意伤害|诈骗|盗窃|虚假诉讼)',
        r'(涉案金额\d+[亿万千百万元]+)',
        r'(被害人\d+[多名]+)',
        r'(有期徒刑\d+[年个月]+)',
    ]

    key_sentences = []
    for line in lines:
        line = line.strip()
        if len(line) > 10 and not line.startswith('#') and not line.startswith('**') and not line.startswith('来源：'):
            for pattern in important_patterns:
                if re.search(pattern, line):
                    key_sentences.append(line)
                    break

    # Deduplicate while preserving order
    seen = set()
    for s in key_sentences:
        # Normalize for comparison
        normalized = re.sub(r'\s+', '', s)[:50]
        if normalized not in seen and len(s) > 15:
            seen.add(normalized)
            points.append(s)
            if len(points) >= 8:
                break

    # If we don't have enough, add general content
    if len(points) < 5:
        for line in lines:
            line = line.strip()
            if line and len(line) > 30 and not line.startswith('#') and not line.startswith('**') and '来源' not in line and '编辑' not in line and '作者' not in line:
                if line not in points:
                    points.append(line)
                    if len(points) >= 5:
                        break

    return points[:10]  # Return up to 10 points

def extract_tags(content, title):
    """Extract relevant tags from content"""
    tags = ["最高检", "今晚九点半", "检察日报"]

    # Add topic-related tags
    tag_keywords = {
        "诈骗": ["诈骗罪", "电信诈骗", "网络诈骗"],
        "盗窃": ["盗窃罪", "盗窃"],
        "正当防卫": ["正当防卫", "防卫过当"],
        "故意伤害": ["故意伤害罪"],
        "虚假诉讼": ["虚假诉讼罪"],
        "挪用": ["挪用资金罪", "挪用公款罪"],
        "受贿": ["受贿罪"],
        "毒品": ["毒品犯罪", "制毒", "贩毒"],
        "未成年人": ["未成年人保护", "附条件不起诉"],
        "劳动争议": ["劳动争议", "工伤"],
        "知识产权": ["知识产权", "侵权", "假冒"],
        "生态环境": ["环境污染", "生态保护"],
        "消费者": ["消费者权益", "欺诈"],
        "非法集资": ["非法集资", "集资诈骗"],
    }

    content_lower = content.lower()
    title_lower = title.lower()

    for keyword, related_tags in tag_keywords.items():
        if keyword in content_lower or keyword in title_lower:
            tags.extend(related_tags[:2])  # Add up to 2 related tags

    # Deduplicate
    seen = set()
    unique_tags = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            unique_tags.append(t)

    return unique_tags[:8]  # Return up to 8 tags

def create_wiki_content(source_file, content, title, date_str):
    """Create wiki summary content with frontmatter"""
    source_path = f"sources/微信公号资料/最高人民检察院/最高检-今晚九点半-md/{source_file}"

    # Build filename
    clean_title = re.sub(r'[【】""''（）\(\)（）]', '', title)
    clean_title = re.sub(r'[^a-zA-Z0-9一-鿿]', '_', clean_title)
    clean_title = clean_title[:50]  # Limit length
    clean_title = re.sub(r'_+', '_', clean_title)

    filename = f"summary_{date_str.replace('-','')}_最高检_今晚九点半_{clean_title}.md"
    filename = re.sub(r'_+', '_', filename)

    key_points = extract_key_points(content)
    tags = extract_tags(content, title)

    # Build frontmatter
    frontmatter = f'''---
title: {title}
type: summary
created: 2026-05-11
updated: 2026-05-11
tags: [{", ".join(tags)}]
source: "{source_path}"
related: []
category: {CATEGORY}
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{source_file}]] |
| 类型 | 案例分析/检察普法 |
| 发布日期 | {date_str} |
| 关键词 | {" / ".join(tags[:5])} |
| 核心要点 | {len(key_points)} 条 |

'''

    # Add key points section
    body = "## 核心要点\n\n"
    for i, point in enumerate(key_points, 1):
        # Clean up point
        point_clean = point.strip()
        point_clean = re.sub(r'^[\s　]+|[\s　]+$', '', point_clean)
        if point_clean:
            body += f"{i}. {point_clean}\n\n"

    # Add related links section
    body += "\n## 相关\n\n"
    body += "- [[今晚九点半]]（系列索引）\n"

    return filename, frontmatter + body

def process_file(source_file):
    """Process a single source file and return (target_file, content)"""
    source_path = SOURCE_DIR / source_file
    if not source_path.exists():
        return None, None

    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()

    date_str = extract_date_from_filename(source_file)
    title = extract_title(content)
    filename, wiki_content = create_wiki_content(source_file, content, title, date_str)

    return filename, wiki_content

def main():
    # Get all source files
    source_files = sorted([f for f in os.listdir(SOURCE_DIR) if f.endswith('.md')])

    print(f"Found {len(source_files)} files to process")
    print(f"Source: {SOURCE_DIR}")
    print(f"Target: {TARGET_DIR}")

    # Ensure target directory exists
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    errors = []

    for i, source_file in enumerate(source_files, 1):
        try:
            filename, wiki_content = process_file(source_file)
            if filename and wiki_content:
                target_path = TARGET_DIR / filename

                # Check if file already exists
                if target_path.exists():
                    print(f"[{i}/{len(source_files)}] SKIP (exists): {filename}")
                    results.append((source_file, filename, "skipped"))
                else:
                    with open(target_path, 'w', encoding='utf-8') as f:
                        f.write(wiki_content)
                    print(f"[{i}/{len(source_files)}] OK: {filename}")
                    results.append((source_file, filename, "created"))
            else:
                print(f"[{i}/{len(source_files)}] ERROR: Could not process {source_file}")
                errors.append((source_file, "Processing returned None"))
        except Exception as e:
            print(f"[{i}/{len(source_files)}] ERROR: {source_file}: {e}")
            errors.append((source_file, str(e)))

    # Summary
    print(f"\n=== Summary ===")
    print(f"Total: {len(source_files)}")
    print(f"Created: {len([r for r in results if r[2] == 'created'])}")
    print(f"Skipped (exists): {len([r for r in results if r[2] == 'skipped'])}")
    print(f"Errors: {len(errors)}")

    if errors:
        print("\nErrors:")
        for src, err in errors[:10]:
            print(f"  - {src}: {err}")

    # Verify count
    summary_files = list(TARGET_DIR.glob("summary_*最高检_今晚九点半_*.md"))
    print(f"\nVerification: {len(summary_files)} summary files in target directory")

if __name__ == "__main__":
    main()