#!/usr/bin/env python3
"""Batch process 最高法-小案大道理 md files to wiki/summaries/"""

import re
import os
from pathlib import Path

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民法院/最高法-小案大道理-md")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/summaries")
TARGET_DIR.mkdir(parents=True, exist_ok=True)

# Get all md files
files = sorted(SOURCE_DIR.glob("*.md"))
print(f"Total files to process: {len(files)}")

def extract_date_from_filename(filename):
    """Extract date from [YYYY-MM-DD] prefix in filename."""
    match = re.match(r"\[(\d{4}-\d{2}-\d{2})\]", filename)
    if match:
        return match.group(1).replace("-", "")
    return None

def extract_title(content):
    """Extract title from first # heading."""
    match = re.search(r"^#\s+(.+?)\s*$", content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    # Fallback: get first line that's not empty and not a tag
    lines = content.split("\n")
    for line in lines:
        line = line.strip()
        if line and not line.startswith("**") and len(line) > 5:
            # Remove # if present
            if line.startswith("#"):
                line = line.lstrip("#").strip()
            return line
    return "未命名"

def extract_key_points(content):
    """Extract key points from content - paragraphs under 案情回顾, 庭审现场, etc."""
    points = []

    # Extract case facts (案情回顾)
    case_match = re.search(r"案情回顾\s*\n(.+?)(?=\n大V点评|庭审现场|\n代表点评|$)", content, re.DOTALL)
    if case_match:
        text = case_match.group(1).strip()
        # Take first 150 chars as main fact
        if len(text) > 150:
            text = text[:150] + "..."
        points.append(f"案情：{text}")

    # Extract court ruling
    ruling_patterns = [
        r"判决[：:](.+?)(?=\n|$)",
        r"判处(.+?)(?=\n|$)",
        r"判令(.+?)(?=\n|$)",
        r"（(.+?)）",  # parenthetical rulings
    ]
    for pattern in ruling_patterns:
        match = re.search(pattern, content)
        if match and len(match.group(1)) > 5:
            ruling = match.group(1).strip()
            if len(ruling) > 100:
                ruling = ruling[:100] + "..."
            if ruling not in points:
                points.append(f"裁判：{ruling}")
                break

    # Extract legal principle
    principle_patterns = [
        r"(正当防卫|自甘风险|公序良俗|安全保障义务|见义勇为|自首|正当防卫)",
        r"(不具有违法性|不应承担赔偿责任|无罪|正当防卫)",
    ]
    for pattern in principle_patterns:
        match = re.search(pattern, content)
        if match:
            # Get surrounding context
            start = max(0, match.start() - 20)
            end = min(len(content), match.end() + 30)
            context = content[start:end].replace("\n", " ").strip()
            if len(context) > 60:
                context = context[:60] + "..."
            if context not in points:
                points.append(f"原理：{context}")
                break

    # Extract social significance
    sig_patterns = [
        r"(社会主义核心价值观|引领|正能量|社会风尚|道德)",
        r"司法(鼓励|保护|支持|弘扬)",
    ]
    for pattern in sig_patterns:
        match = re.search(pattern, content)
        if match:
            start = max(0, match.start() - 10)
            end = min(len(content), match.end() + 50)
            context = content[start:end].replace("\n", " ").strip()
            if len(context) > 50:
                context = context[:50] + "..."
            if context not in points:
                points.append(f"意义：{context}")
                break

    # Ensure at least 5 points
    while len(points) < 5:
        points.append(f"要点{len(points)+1}：（见原文）")

    return points[:7]  # Max 7 points

def create_summary(content, filename):
    """Create summary wiki page."""
    date_str = extract_date_from_filename(filename)
    title = extract_title(content)
    key_points = extract_key_points(content)

    # Generate filename
    # Clean title for filename - remove quotes and special chars
    clean_title = re.sub(r'[（）、。，！？：""''【】]', '', title)
    clean_title = re.sub(r'\s+', '_', clean_title)
    if len(clean_title) > 30:
        clean_title = clean_title[:30]

    if date_str:
        output_name = f"summary_{date_str}_最高法_小案大道理_{clean_title}.md"
    else:
        output_name = f"summary_最高法_小案大道理_{clean_title}.md"

    output_path = TARGET_DIR / output_name

    # Create frontmatter
    frontmatter = f"""---
title: {title}
type: summary
created: 2026-05-11
updated: 2026-05-11
tags: [司法案例, 最高人民法院, 小案大道理]
source: sources/微信公号资料/最高人民法院/最高法-小案大道理-md/{filename}
related: []
---

## 核心要点

{"".join([f"- {p}\n" for p in key_points])}

## 案情概述

"""

    # Extract case overview section
    overview_match = re.search(r"案情回顾\s*\n(.+?)(?=\n大V点评)", content, re.DOTALL)
    if overview_match:
        overview = overview_match.group(1).strip()
        # Clean up extra whitespace
        overview = re.sub(r"\n{3,}", "\n\n", overview)
        # Remove image references like "资料图片"
        overview = re.sub(r"资料图片\s*", "", overview)
        frontmatter += overview + "\n\n"
    else:
        frontmatter += "（详见原文）\n\n"

    # Add court ruling
    ruling_match = re.search(r"(判决|判处|判令|一审|二审|再审)(.{10,200}?)(?=\n)", content)
    if ruling_match:
        frontmatter += f"**裁判结果**：{ruling_match.group(0).strip()}\n\n"

    # Add expert commentary summary
    vip_match = re.search(r"大V点评\s*\n.*?：(.{50,200}?)", content, re.DOTALL)
    if vip_match:
        frontmatter += f"**专家点评**：{vip_match.group(1).strip()}\n\n"

    # Add representative commentary summary
    rep_match = re.search(r"代表点评\s*\n.*?(.{30,150}?)(?=来源：|编辑：|$)", content, re.DOTALL)
    if rep_match:
        frontmatter += f"**代表意见**：{rep_match.group(1).strip()}\n"

    return output_path, frontmatter

# Process all files
processed = 0
errors = 0

for f in files:
    try:
        content = f.read_text(encoding="utf-8")
        output_path, summary_content = create_summary(content, f.name)

        # Handle duplicate filenames
        counter = 1
        original_path = output_path
        while output_path.exists():
            if date_str := extract_date_from_filename(f.name):
                output_path = TARGET_DIR / f"summary_{date_str}_最高法_小案大道理_{counter}_{clean_title if 'clean_title' in locals() else 'case'}.md"
            counter += 1

        output_path.write_text(summary_content, encoding="utf-8")
        processed += 1

        if processed % 20 == 0:
            print(f"Processed {processed}/{len(files)} files...")

    except Exception as e:
        errors += 1
        print(f"Error processing {f.name}: {e}")

print(f"\nCompleted: {processed} files processed, {errors} errors")