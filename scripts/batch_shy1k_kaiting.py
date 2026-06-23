#!/usr/bin/env python3
"""Batch process 上海一中法院 开庭 md files to wiki/summaries/"""

import re
import os
from pathlib import Path

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/上海一中法院/上海一中法院-开庭-md")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/summaries")

def extract_title(content):
    """Extract title from first # heading, removing date prefix."""
    match = re.search(r'^#\s+(?:\[\d{4}-\d{2}-\d{2}\]\s*)?(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "Untitled"

def extract_tags(content, title):
    """Derive tags from content and title."""
    tags = ["庭审", "民事诉讼", "上海一中院"]

    if "刑事" in content:
        tags.append("刑事诉讼")
    if "答辩" in title or "答辩" in content:
        tags.append("答辩")
    if "辩论" in title or "辩论" in content:
        tags.append("法庭辩论")
    if "证据" in content:
        tags.append("证据")
    if "证人" in content:
        tags.append("证人证言")
    if "鉴定" in content:
        tags.append("司法鉴定")
    if "管辖" in content:
        tags.append("管辖")
    if "调解" in content:
        tags.append("调解")
    if "劳动" in content:
        tags.append("劳动争议")
    if "侵权" in content:
        tags.append("侵权责任")
    if "二审" in content:
        tags.append("二审程序")

    return tags

def extract_key_points(content):
    """Extract meaningful key points from content - skip headers/boilerplate."""
    points = []

    # Lines that look like actual content (not headers, not editor notes)
    # Skip lines with only special characters, URLs, etc.
    skip_patterns = [
        r'^#', r'^\*\*编者按', r'^\*\*第\d+期', r'^官方微信', r'^点击链接',
        r'近期热文', r'预览时标签', r'^值班编辑', r'^图：', r'^文：',
        r'^上海一中院', r'http://', r'mp\.weixin', r'微课程'
    ]

    # Find numbered key points in original content (like 01, 02, 1., 2.)
    # These often contain the core recommendations
    numbered_sections = re.findall(
        r'(?:^|\n)(?:01|02|03|04|05|1\.|2\.|3\.|4\.|5\.)[\s　]+([^。\n]{20,})',
        content
    )
    for m in numbered_sections:
        m = m.strip().strip('*：:').strip()
        if len(m) > 15:
            points.append(m)

    # Find content between ** ** that looks like recommendations
    bold_sections = re.findall(r'\*\*([^*]{20,100})\*\*', content)
    for m in bold_sections:
        m = m.strip()
        # Skip if it looks like a header
        if len(m) > 20 and not re.match(r'^[\d۰-９]+', m) and not m.endswith('：'):
            points.append(m)

    # Extract lines that contain practical recommendations (contain "建议", "应当", "可以", etc.)
    recommendation_lines = re.findall(r'[^。\n。]*[建议应当可以注意务必][^。\n。]{15,}', content)
    for line in recommendation_lines:
        line = line.strip()
        if len(line) > 20 and len(line) < 200:
            # Clean up the line
            line = re.sub(r'\*+', '', line)
            if line not in points:
                points.append(line)

    # Deduplicate while preserving order
    seen = set()
    unique_points = []
    for p in points:
        # Normalize for comparison
        p_norm = re.sub(r'\s+', '', p)[:40]
        if p_norm not in seen and len(p) > 15:
            seen.add(p_norm)
            unique_points.append(p)

    return unique_points[:8]

def process_file(src_path):
    """Process a single source file."""
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract date from filename
    filename = src_path.name
    date_match = re.match(r'\[(\d{4}-\d{2}-\d{2})\](.+)\.md', filename)
    if not date_match:
        print(f"Skipping invalid filename format: {filename}")
        return None

    date_str = date_match.group(1)
    title = extract_title(content)
    tags = extract_tags(content, title)

    # Build key points section
    key_points = extract_key_points(content)
    key_points_section = ""
    if key_points:
        key_points_section = "\n\n## 关键要点\n\n"
        for i, point in enumerate(key_points[:7], 1):
            # Truncate very long points
            display_point = point[:150] + "..." if len(point) > 150 else point
            key_points_section += f"{i}. {display_point}\n"

    # Build related links based on content
    related = []
    if "刑事" in content:
        related.append("[[concept_刑事庭审程序]]")
    if "劳动" in content:
        related.append("[[concept_劳动争议处理]]")
    if "侵权" in content:
        related.append("[[concept_侵权责任认定]]")
    if "证据" in content or "鉴定" in content:
        related.append("[[concept_民事诉讼证据]]")
    if "管辖" in content:
        related.append("[[concept_民事诉讼管辖]]")
    if "调解" in content:
        related.append("[[concept_诉讼调解]]")

    # Build frontmatter
    frontmatter = f"""---
title: {title}
type: summary
created: 2026-05-11
updated: 2026-05-11
tags: [{', '.join(tags)}]
source: "sources/微信公号资料/上海一中法院/上海一中法院-开庭-md/{filename}"
related: [{', '.join(related)}]
---"""

    # Build target filename
    date_compact = date_str.replace('-', '')
    target_filename = f"summary_{date_compact}_上海一中法院_开庭_{title}.md"
    target_path = TARGET_DIR / target_filename

    # Body with key points
    body = f"{frontmatter}\n\n{key_points_section}\n\n## 正文概要\n\n本文基于上海一中院《开庭》栏目法官实务经验，探讨庭审相关问题。"

    return target_path, body

def main():
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    source_files = sorted(SOURCE_DIR.glob("*.md"))
    print(f"Found {len(source_files)} files to process")

    results = []
    for src_path in source_files:
        result = process_file(src_path)
        if result:
            target_path, body = result
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(body)
            results.append(target_path.name)
            print(f"  Created: {target_path.name}")

    print(f"\nProcessed {len(results)} files total")

if __name__ == "__main__":
    main()
