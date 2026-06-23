#!/usr/bin/env python3
"""Batch process 今晚九点半 articles into wiki summaries."""

import os
import re
import sys
from pathlib import Path

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-今晚九点半-md")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/summaries")
TARGET_DIR.mkdir(parents=True, exist_ok=True)

def extract_title(content):
    """Extract article title from first # heading."""
    match = re.search(r'^#\s+(.+?)\s*[,，]?\s*今晚九点半', content, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        title = re.sub(r'^[,，.\s]+|[,，.\s]+$', '', title)
        return title
    match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "未命名"

def extract_tags(content, title):
    """Extract relevant tags from content."""
    tags = ["今晚九点半", "法治故事", "检察教育"]

    if any(k in content for k in ["虚假诉讼", "伪造证据", "骗取调解"]):
        tags.append("虚假诉讼")
    if any(k in content for k in ["工伤", "劳动争议", "执行异议"]):
        tags.append("劳动纠纷")
    if any(k in content for k in ["诈骗", "被骗", "电诈"]):
        tags.append("诈骗犯罪")
    if any(k in content for k in ["贩毒", "制毒", "毒品"]):
        tags.append("毒品犯罪")
    if any(k in content for k in ["盗窃", "盗墓", "偷盗"]):
        tags.append("盗窃犯罪")
    if any(k in content for k in ["贪污", "受贿", "职务侵占"]):
        tags.append("职务犯罪")
    if any(k in content for k in ["故意伤害", "杀人", "命案"]):
        tags.append("暴力犯罪")
    if any(k in content for k in ["醉驾", "酒驾", "交通肇事"]):
        tags.append("交通犯罪")
    if any(k in content for k in ["侵犯公民信息", "个人信息"]):
        tags.append("信息犯罪")
    if any(k in content for k in ["正当防卫", "自卫"]):
        tags.append("正当防卫")
    if any(k in content for k in ["民事检察", "监督", "检察建议"]):
        tags.append("民事检察")
    if any(k in content for k in ["刑事检察", "公诉", "审查起诉"]):
        tags.append("刑事检察")

    return tags

def extract_related(content):
    """Extract related wiki links from content keywords."""
    related = []

    topic_map = {
        "虚假诉讼": ["concept_虚假诉讼罪"],
        "劳动争议": ["concept_劳动争议", "concept_工伤保险条例"],
        "工伤赔偿": ["concept_工伤保险条例"],
        "执行异议": ["concept_执行异议"],
        "民事检察": ["concept_民事检察"],
        "检察建议": ["concept_检察建议"],
        "正当防卫": ["concept_正当防卫", "entity_刑法第二十条"],
        "职务侵占": ["concept_职务侵占罪"],
        "贪污": ["concept_贪污罪"],
        "诈骗": ["concept_诈骗罪"],
        "电诈": ["concept_诈骗罪"],
        "盗窃": ["concept_盗窃罪"],
        "毒品": ["concept_毒品犯罪"],
        "侵犯公民个人信息": ["concept_侵犯公民个人信息罪"],
    }

    for keyword, pages in topic_map.items():
        if keyword in content:
            for page in pages:
                if page not in related:
                    related.append(page)

    return related[:3]

def extract_date_from_filename(filename):
    """Extract date from filename [YYYY-MM-DD]."""
    match = re.search(r'\[(\d{4}-\d{2}-\d{2})\]', filename)
    if match:
        return match.group(1)
    return "2025-09-20"

def extract_content(body):
    """Extract main content, removing footer elements."""
    footer_patterns = [
        r'欢迎点赞、留言、转发朋友圈\s*',
        r'每晚九点半，不见不散哟\s*',
        r'来源：[^\n]+\s*',
        r'作者：[^\n]+\s*',
        r'漫画：[^\n]+\s*',
        r'编辑：[^\n]+\s*',
        r'预览时标签不可点\s*',
        r'\[阅读原文\]\s*',
        r'__+\s*',
    ]

    content = body
    for pattern in footer_patterns:
        content = re.sub(pattern, '', content)

    return content.strip()

def process_file(filepath):
    """Process a single source file into wiki summary."""
    filename = filepath.name

    date_match = re.match(r'\[(\d{4}-\d{2}-\d{2})\]', filename)
    date_str = date_match.group(1) if date_match else "2025-09-20"

    base_name = re.sub(r'^\[\d{4}-\d{2}-\d{2}\]', '', filename)
    base_name = base_name.replace('今晚九点半.md', '')
    base_name = base_name.strip()

    target_name = f"summary_SPP_今晚九点半_{base_name}.md"
    target_path = TARGET_DIR / target_name

    if target_path.exists():
        print(f"SKIP: {target_name} (exists)")
        return "skip"

    content = filepath.read_text(encoding='utf-8')

    parts = content.split('---', 2)
    body = parts[2] if len(parts) >= 3 else content

    title = extract_title(body)
    tags = extract_tags(body, title)
    related = extract_related(body)
    related_str = ', '.join([f'[[{r}]]' for r in related]) if related else ''

    # Remove original # heading from body
    main_content = re.sub(r'^#\s+.+?今晚九点半[ ]*\n', '', body, count=1)
    main_content = extract_content(main_content)

    output = f"""---
title: {title}
type: summary
category: 刑事参考
created: 2026-05-11
updated: 2026-05-11
tags: [{', '.join(tags)}]
source: [[{filename}]]
related: [{related_str}]
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{filename}]] |
| 类型 | 法治故事/检察教育 |
| 发布日期 | {date_str} |
| 关键词 | {' / '.join(tags)} |

## 核心内容

{main_content}
"""

    target_path.write_text(output, encoding='utf-8')
    print(f"OK: {target_name}")
    return "ok"

def main():
    source_files = sorted(SOURCE_DIR.glob("*.md"))
    print(f"Found {len(source_files)} files to process")

    results = {"ok": 0, "skip": 0, "error": 0}

    for f in source_files:
        try:
            result = process_file(f)
            results[result] += 1
        except Exception as e:
            print(f"ERROR: {f.name} - {e}")
            results["error"] += 1

    print(f"\nResults: OK={results['ok']}, Skip={results['skip']}, Error={results['error']}")

if __name__ == "__main__":
    main()