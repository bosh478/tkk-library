#!/usr/bin/env python3
"""Batch ingest 入库案例选介 to wiki/syntheses/ - Fixed version"""

import re
import os
from pathlib import Path

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民法院/最高法-入库案例选介-md")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/syntheses")

def extract_title(content):
    """Extract title from first # heading"""
    m = re.search(r'^#\s+【?入库案例选介】?(.*?)(?:\n|$)', content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    # Try alternate pattern
    m = re.search(r'^#\s+人民法院案例库入库参考案例选介[：:]\s*(.*)', content, re.MULTILINE)
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
    m = re.search(r'入库编号[：:：]?\s*([0-9][0-9-]+)', content)
    return m.group(1) if m else ""

def extract_keywords(content):
    """Extract 关键词"""
    m = re.search(r'\*\*\s*关键词\s*\*\*[：:]\s*(.*?)(?:\n|$)', content)
    if m:
        kw = m.group(1).strip()
        return [k.strip() for k in re.split(r'[、，]', kw) if k.strip()]
    # Try inline pattern
    m = re.search(r'关键词[：:]\s*(.*?)(?:\n|$)', content)
    if m:
        kw = m.group(1).strip()
        return [k.strip() for k in re.split(r'[、，]', kw) if k.strip()]
    return []

def extract_section(content, section_name):
    """Extract section content using **Section** pattern"""
    # Try **基本案情** pattern
    pattern = rf'\*\*{section_name}\*\*\s*(.*?)(?=\*\*[【一-龥]|$)'
    m = re.search(pattern, content, re.DOTALL)
    if m:
        text = m.group(1).strip()
        # Remove bold markers
        text = re.sub(r'\*+', '', text)
        return text
    # Try 【】 pattern
    pattern = rf'【{section_name}】\s*(.*?)(?=【|\*\*关联索引|$)'
    m = re.search(pattern, content, re.DOTALL)
    return m.group(1).strip() if m else ""

def extract裁判要旨(content):
    """Extract 裁判要旨 section - find the section after **裁判要旨**"""
    # Find **裁判要旨** followed by content
    pattern = r'\*\*裁判要旨\*\*\s*(.*?)(?=\*\*【|来源：|编辑：|$)'
    m = re.search(pattern, content, re.DOTALL)
    if m:
        text = m.group(1).strip()
        text = re.sub(r'\*+', '', text)
        return text
    # Fallback: find numbered 裁判要旨 items
    items = re.findall(r'\d+\.([^\n]+?)(?=\n\d+\.|\n\*\*|$)', content)
    if items:
        return '\n'.join(items)
    return ""

def extract专家点评(content):
    """Extract 专家点评 section"""
    pattern = r'\*\*【专家点评】\*\*\s*(.*?)(?=来源：|编辑：|$)'
    m = re.search(pattern, content, re.DOTALL)
    if m:
        text = m.group(1).strip()
        text = re.sub(r'\*+', '', text)
        return text
    # Look for expert comment after 专家点评
    pattern = r'专家点评\s*\*+\s*(.*?)(?=来源：|$)'
    m = re.search(pattern, content, re.DOTALL)
    return m.group(1).strip() if m else ""

def extract_case_level(content):
    """Determine case level based on content"""
    if '入库参考案例' in content:
        return "⭐⭐⭐⭐（入库参考案例）"
    return "⭐⭐⭐⭐（入库案例）"

def extract_related_laws(content):
    """Extract related law articles"""
    laws = re.findall(r'《([^》]+)》第?([零一二三四五六七八九十百千万\d]+条)', content)
    if laws:
        return '\n'.join([f"- {law[0]}第{law[1]}条" for law in laws])
    # Check for simple law references
    simple = re.findall(r'《([^》]+)》', content)
    if simple:
        uniq = list(dict.fromkeys(simple))
        return '\n'.join([f"- {l}" for l in uniq[:5]])
    return ""

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
    return '\n'.join(refs) if refs else ""

def process_file(src_path):
    """Process single file"""
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title
    title = extract_title(content)
    if not title or title == "未命名":
        m = re.search(r'^#\s+人民法院案例库入库参考案例选介[：:]?\s*(.*)', content, re.MULTILINE)
        if m:
            title = m.group(1).strip()

    source_file = src_path.name

    # Generate target filename
    clean_title = re.sub(r'[（()（）\s、，。！？：:""''·]', '_', title)
    clean_title = re.sub(r'_+', '_', clean_title).strip('_')
    clean_title = clean_title[:60]
    target_file = f"CourtFa_入库案例_{clean_title}.md"
    target_path = TARGET_DIR / target_file

    if target_path.exists():
        return "skipped", source_file

    case_level = extract_case_level(content)
    入库编号 = extract入库编号(content)
    keywords = extract_keywords(content)
    裁判要旨 = extract裁判要旨(content)
    基本案情 = extract_section(content, '基本案情')
    裁判理由 = extract_section(content, '裁判理由')
    专家点评 = extract专家点评(content)
    related_laws = extract_related_laws(content)
    case_refs = extract_case_refs(content)
    case_no = extract_case_number(content)

    tags = keywords if keywords else []
    # Auto-tag based on content
    text_lower = content.lower()
    if '刑事' in text_lower or '故意' in text_lower or '盗窃' in text_lower or '诈骗' in text_lower:
        tags.append('刑事案件')
    if '民事' in text_lower or '纠纷' in text_lower or '侵权' in text_lower:
        tags.append('民事案件')
    if '行政' in text_lower:
        tags.append('行政案件')

    tags_str = ', '.join(f"'{t}'" for t in tags) if tags else ''

    # Build body
    body_parts = [f"""---
title: {title}
type: synthesis
created: 2026-05-11
updated: 2026-05-11
tags: [{tags_str}]
source: [[sources/微信公号资料/最高人民法院/最高法-入库案例选介-md/{source_file}]]
related: []
案例分级: {case_level}
问题意识: 入库案例裁判要旨分析
入库编号: {入库编号}
---

## 基本案情

{基本案情 if 基本案情 else '（详见原文）'}

## 裁判理由

{裁判理由 if 裁判理由 else '（详见原文）'}

## 裁判要旨

{裁判要旨 if 裁判要旨 else '（详见原文）'}

## 相关法条

{related_laws if related_laws else '- 《刑法》相关条款'}
"""]

    if case_refs:
        body_parts.append(f"\n## 关联索引\n\n{case_refs}\n")

    if 专家点评:
        body_parts.append(f"\n## 专家点评\n\n{专家点评}\n")

    if 入库编号:
        body_parts.append(f"\n---\n**入库编号**：{入库编号}")
    if case_no:
        body_parts.append(f"\n**案号**：{case_no}")

    with open(target_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(body_parts))

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
            if i % 20 == 0:
                print(f"Processed {i}/{len(source_files)}")
        except Exception as e:
            results["errors"].append(f"{src_path.name}: {e}")
            print(f"Error: {src_path.name}: {e}")

    print(f"\nSummary: {results['created']} created, {results['skipped']} skipped, {len(results['errors'])} errors")
    if results['errors']:
        print("\nErrors:")
        for e in results['errors'][:5]:
            print(f"  - {e}")

if __name__ == "__main__":
    main()