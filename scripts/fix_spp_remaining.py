# -*- coding: utf-8 -*-
"""Fix remaining SPP_GuideCase_ placeholder and empty-body pages."""
import os, sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

SRC_DIR = 'D:/AI agent/tkk-library/sources/2-案例库/最高检-指导性案例'
WIKI_DIR = 'D:/AI agent/tkk-library/wiki/syntheses'

def find_case_in_source(src_content, case_num):
    """Extract case content from source file for a specific case number."""
    # Find the case section: **Case Name** \n **（检例第X号）**
    # Pattern: find the case header, then extract sections until next case header
    pattern = rf'\*\*[^*]*\*\*\s*\n\s*\*\*（检例第{case_num}号）\*\*'
    match = re.search(pattern, src_content)
    if not match:
        # Try alternative pattern
        pattern = rf'检例第{case_num}号'
        match = re.search(pattern, src_content)
        if not match:
            return None

    start = match.start()
    # Find the next case header (检例第Y号) or end of file
    next_case = re.search(r'\*\*[^*]*\*\*\s*\n\s*\*\*（检例第\d+号）\*\*', src_content[match.end():])
    if next_case:
        end = match.end() + next_case.start()
    else:
        end = len(src_content)

    section = src_content[start:end]

    # Extract case name
    name_m = re.search(r'\*\*([^*]+)\*\*\s*\n\s*\*\*（检例第\d+号）\*\*', src_content[:match.end()])
    case_name = name_m.group(1).strip() if name_m else f'检例第{case_num}号'

    # Extract sections
    def extract_section(name):
        # Try **【name】** pattern
        p = rf'【{name}】\s*\n(.*?)(?=【|$)'
        m = re.search(p, section, re.DOTALL)
        if m:
            text = m.group(1).strip()
            # Clean up: remove leading/trailing whitespace and newlines
            text = re.sub(r'^\s*　*', '', text, flags=re.MULTILINE)
            text = text.strip()
            return text if text else '（未在原文中标注）'
        return '（未在原文中标注）'

    return {
        'name': case_name,
        'keywords': extract_section('关键词'),
        'summary': extract_section('要旨'),
        'legislation': extract_section('相关立法'),
        'facts': extract_section('基本案情'),
        'process': extract_section('诉讼过程'),
    }

def build_wiki_page(case_num, case_data, source_file):
    """Build the wiki page content."""
    name = case_data['name']
    keywords = case_data['keywords']
    summary = case_data['summary']
    legislation = case_data['legislation']
    facts = case_data['facts']
    process = case_data['process']

    # Extract batch number from source filename
    batch_m = re.search(r'第(\w+)批', source_file)
    batch = f'第{batch_m.group(1)}批' if batch_m else '未知'

    # Build tags
    tags_list = ['指导性案例', '最高人民检察院', f'检例第{case_num}号']
    # Add keyword-based tags
    if keywords and keywords != '（未在原文中标注）':
        for kw in re.split(r'[,，、\s]+', keywords):
            kw = kw.strip()
            if kw and len(kw) >= 2:
                tags_list.append(kw)

    tags_str = ', '.join(tags_list)

    # Build related field from keywords
    related_concepts = []
    if keywords and keywords != '（未在原文中标注）':
        for kw in re.split(r'[,，、\s]+', keywords):
            kw = kw.strip()
            if kw and len(kw) >= 2:
                related_concepts.append(f'[[concept_{kw}]]')

    if related_concepts:
        if len(related_concepts) == 1:
            related_str = f'related: {related_concepts[0]}'
        else:
            related_str = 'related:\n  ' + '\n  '.join(f'- {r}' for r in related_concepts)
    else:
        related_str = 'related:\n  - '

    return f"""---
title: {name}
type: synthesis
created: 2026-05-09
updated: 2026-05-27
tags: [{tags_str}]
source: "sources/2-案例库/最高检-指导性案例/{source_file}"
{related_str}
案例分级: ⭐⭐⭐⭐⭐
问题意识: {name}的裁判要旨
---

## 📋 案例信息

| 字段 | 内容 |
|------|------|
| 案例编号 | 检例第{case_num}号 |
| 案例名称 | {name} |
| 发布机关 | 最高人民检察院 |
| 发布批次 | {batch} |
| 关键词 | {keywords} |

## 要旨

{summary}

## 相关立法

{legislation}

## 基本案情

{facts}

## 诉讼过程

{process}
"""

# Build source file index
src_files = {}
for fname in os.listdir(SRC_DIR):
    if not fname.endswith('.md'):
        continue
    fpath = os.path.join(SRC_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Find all case numbers in this file
    case_nums = [int(m) for m in re.findall(r'检例第(\d+)号', content)]
    for cn in case_nums:
        src_files[cn] = (fname, content)

# Identify files to fix
to_fix = []
for fname in sorted(os.listdir(WIKI_DIR)):
    if not (fname.startswith('SPP_GuideCase_') and fname.endswith('.md')):
        continue
    path = os.path.join(WIKI_DIR, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    needs_fix = False
    reason = ''

    # Check if still placeholder
    if '详见原文' in content:
        needs_fix = True
        reason = 'placeholder'
    # Check if empty body
    elif 'updated: 2026-05-27' in content:
        body = content.split('---')[-1] if '---' in content else content
        要旨_m = re.search(r'## 要旨\s*\n(.+?)(?=\n##|\Z)', body, re.DOTALL)
        案情_m = re.search(r'## 基本案情\s*\n(.+?)(?=\n##|\Z)', body, re.DOTALL)
        要旨 = 要旨_m.group(1).strip() if 要旨_m else ''
        案情 = 案情_m.group(1).strip() if 案情_m else ''
        if len(要旨) <= 20 or len(案情) <= 20:
            needs_fix = True
            reason = 'empty_body'

    if needs_fix:
        # Extract case number
        cn_m = re.search(r'检例第(\d+)号', fname)
        if cn_m:
            case_num = int(cn_m.group(1))
            to_fix.append((fname, case_num, reason))

print(f'Files to fix: {len(to_fix)}')

# Fix each file
fixed = 0
errors = 0
for fname, case_num, reason in to_fix:
    if case_num not in src_files:
        print(f'  SKIP {fname}: source not found for case {case_num}')
        errors += 1
        continue

    src_file, src_content = src_files[case_num]
    case_data = find_case_in_source(src_content, case_num)

    if not case_data:
        print(f'  SKIP {fname}: case {case_num} not found in {src_file}')
        errors += 1
        continue

    # Only fix if we have actual content
    if case_data['summary'] == '（未在原文中标注）' and case_data['facts'] == '（未在原文中标注）':
        print(f'  SKIP {fname}: no extractable content in source')
        errors += 1
        continue

    wiki_path = os.path.join(WIKI_DIR, fname)
    new_content = build_wiki_page(case_num, case_data, src_file)

    with open(wiki_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    fixed += 1
    print(f'  FIXED {fname} ({reason})')

print(f'\nDone: {fixed} fixed, {errors} errors')
