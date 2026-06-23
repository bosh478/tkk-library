#!/usr/bin/env python3
"""Batch ingest入库案例选介 to wiki/syntheses/"""

import re
import os
from pathlib import Path

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民法院/最高法-入库案例选介-md")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/syntheses")

def extract_title(content):
    """Extract title from first # heading"""
    m = re.search(r'^#\s+【?入库案例选介】?(.*)', content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    m = re.search(r'^#\s+(.*)', content, re.MULTILINE)
    return m.group(1).strip() if m else "未命名"

def extract_case_number(content):
    """Extract case number like (2021)浙1003民初417号"""
    m = re.search(r'（(\d{4})[^）]*号）', content)
    return m.group(0) if m else ""

def extract入库编号(content):
    """Extract 入库编号"""
    m = re.search(r'入库编号[：:]?\s*([0-9-]+)', content)
    return m.group(1) if m else ""

def extract_keywords(content):
    """Extract 关键词"""
    m = re.search(r'关键词[：:]\s*(.*?)(?:\n|$)', content)
    if m:
        kw = m.group(1).strip()
        return [k.strip() for k in re.split(r'[、，]', kw) if k.strip()]
    return []

def extract裁判要旨(content):
    """Extract 裁判要旨 section or key 裁判要旨 paragraphs"""
    # Try to find the 裁判要旨 section
    m = re.search(r'\*\*裁判要旨\*\*\s*(.*?)(?:\n\s*\n|\*\*【)', content, re.DOTALL)
    if m:
        text = m.group(1).strip()
        # Remove bold markers and clean up
        text = re.sub(r'\*\*', '', text)
        return text
    # Fallback: find paragraphs starting with 裁判要旨 or numbered 裁判要旨
    sections = []
    for line in content.split('\n'):
        if '裁判要旨' in line and len(line) > 20:
            clean = re.sub(r'\*\*', '', line).strip()
            sections.append(clean)
    return '\n\n'.join(sections[:3]) if sections else ""

def extract基本案情(content):
    """Extract 基本案情"""
    m = re.search(r'【基本案情】\s*(.*?)(?=【|$)', content, re.DOTALL)
    return m.group(1).strip() if m else ""

def extract裁判理由(content):
    """Extract 裁判理由"""
    m = re.search(r'【裁判理由】\s*(.*?)(?=【|$)', content, re.DOTALL)
    return m.group(1).strip() if m else ""

def extract专家点评(content):
    """Extract 专家点评"""
    m = re.search(r'【专家点评】\s*(.*?)(?=来源：|编辑：|$)', content, re.DOTALL)
    return m.group(1).strip() if m else ""

def extract_case_level(content):
    """Determine case level based on filename/content"""
    if '入库参考案例' in content:
        return "⭐⭐⭐⭐（入库参考案例）"
    return "⭐⭐⭐⭐（入库案例）"

def create_frontmatter(title, source_file, content):
    """Create frontmatter for synthesis"""
    case_no = extract_case_number(content)
    case_level = extract_case_level(content)
    keywords = extract_keywords(content)
    入库编号 = extract入库编号(content)
    裁判要旨 = extract裁判要旨(content)

    tags = keywords if keywords else []
    if '刑事' in ' '.join(tags):
        tags.append('刑事审判')
    if '民事' in ' '.join(tags):
        tags.append('民事审判')
    if '行政' in ' '.join(tags):
        tags.append('行政审判')

    # Extract core issue for 问题意识
    first_line = content.split('\n')[0] if content else ""
    问题意识 = f"入库案例：{title}"

    fm = f"""---
title: {title}
type: synthesis
created: 2026-05-11
updated: 2026-05-11
tags: [{', '.join(tags)}]
source: [[sources/微信公号资料/最高人民法院/最高法-入库案例选介-md/{source_file}]]
related: []
案例分级: {case_level}
问题意识: {问题意识}
入库编号: {入库编号}
裁判要旨: |
  {裁判要旨[:500]}...
---

## 基本案情

{extract基本案情(content)}

## 裁判理由

{extract裁判理由(content)}

## 裁判要旨

{裁判要旨}

## 相关法条

{extract_related_laws(content)}

## 关联索引

{extract_case_refs(content)}
"""
    return fm

def extract_related_laws(content):
    """Extract related law articles"""
    laws = re.findall(r'《([^》]+)》第?([零一二三四五六七八九十百千万\d]+条)', content)
    if laws:
        return '\n'.join([f"- {law[0]}第{law[1]}条" for law in laws])
    # Check for simple law references
    simple = re.findall(r'《([^》]+)》', content)
    if simple:
        uniq = list(dict.fromkeys(simple))
        return '\n'.join([f"- {l}" for l in uniq])
    return "- 《民法典》相关条款"

def extract_case_refs(content):
    """Extract case references"""
    refs = []
    m = re.search(r'\*\*一审：\*\*(.*?)(?:\n|$)', content)
    if m:
        refs.append(f"- 一审：{m.group(1).strip()}")
    m = re.search(r'\*\*二审：\*\*(.*?)(?:\n|$)', content)
    if m:
        refs.append(f"- 二审：{m.group(1).strip()}")
    m = re.search(r'\*\*再审：\*\*(.*?)(?:\n|$)', content)
    if m:
        refs.append(f"- 再审：{m.group(1).strip()}")
    return '\n'.join(refs) if refs else "- 详见原文"

def process_file(src_path):
    """Process single file"""
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title
    title = extract_title(content)
    if not title or title == "未命名":
        # Try alternate pattern
        m = re.search(r'^#\s+人民法院案例库入库参考案例选介[：:]?\s*(.*)', content, re.MULTILINE)
        if m:
            title = m.group(1).strip()
        else:
            # Use filename
            title = src_path.stem

    source_file = src_path.name

    # Generate target filename
    clean_title = re.sub(r'[（()（）\s、，。！？：:""'']', '_', title)
    clean_title = re.sub(r'_+', '_', clean_title)
    clean_title = clean_title[:60]  # Limit length
    target_file = f"CourtFa_入库案例_{clean_title}.md"
    target_path = TARGET_DIR / target_file

    # Check if already exists
    if target_path.exists():
        return "skipped", source_file

    # Create frontmatter and body
    body = create_frontmatter(title, source_file, content)

    # Extract expert comments section
    专家点评 = extract专家点评(content)
    if 专家点评:
        body += f"\n\n## 专家点评\n\n{专家点评}\n"

    # Add case reference info
    case_no = extract_case_number(content)
    入库编号 = extract入库编号(content)
    if 入库编号:
        body += f"\n\n---\n**入库编号**：{入库编号}\n"
    if case_no:
        body += f"\n**案号**：{case_no}\n"

    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(body)

    return "created", source_file

def main():
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    source_files = list(SOURCE_DIR.glob("*.md"))
    print(f"Found {len(source_files)} source files")

    results = {"created": 0, "skipped": 0, "errors": []}

    for i, src_path in enumerate(source_files, 1):
        try:
            status, src = process_file(src_path)
            results[status] += 1
            if i % 10 == 0:
                print(f"Processed {i}/{len(source_files)}: {src[:40]}...")
        except Exception as e:
            results["errors"].append(f"{src_path.name}: {e}")
            print(f"Error processing {src_path.name}: {e}")

    print(f"\nSummary: {results['created']} created, {results['skipped']} skipped, {len(results['errors'])} errors")
    if results['errors']:
        print("\nErrors:")
        for e in results['errors'][:10]:
            print(f"  - {e}")

if __name__ == "__main__":
    main()