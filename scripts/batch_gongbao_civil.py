#!/usr/bin/env python3
"""批量处理最高人民法院公报案例(民事)生成synthesis wiki页面"""

import os
import re

VAULT_ROOT = "D:/AI agent/tkk-library"
SOURCE_DIR = os.path.join(VAULT_ROOT, "sources/2-案例库/公报案例/民事")
TARGET_DIR = os.path.join(VAULT_ROOT, "wiki/syntheses")

os.makedirs(TARGET_DIR, exist_ok=True)

# Get first 200 .md files
files = sorted([f for f in os.listdir(SOURCE_DIR) if f.endswith('.md')])[:200]
print(f"Total files to process: {len(files)}")

def extract_case_number(filename):
    """从文件名提取案号，如'公报案例 (1998)知终字第1号.md' -> '1998知终字第1号'"""
    # Match both ASCII () and fullwidth （） parentheses
    match = re.search(r'[（(]([^）)]+)[）)]', filename)
    return match.group(1) if match else ""

def make_target_name(filename):
    """生成目标文件名：GuideCase_1998知终字第1号.md"""
    case_num = extract_case_number(filename)
    return f"GuideCase_{case_num}.md"

def extract_case_title(content, case_number):
    """从内容提取案件标题

    文件格式：案件标题 + 审理法院：... (all on one line after case number header)
    """
    lines = content.strip().split('\n')
    if len(lines) > 1:
        # Second line typically has title + first metadata
        second_line = lines[1].strip()
        # Remove leading #
        second_line = second_line.lstrip('#').strip()

        # Find where 审理法院 starts - title is everything before it
        pos_yz = second_line.find('审理法院')
        if pos_yz > 5:
            title = second_line[:pos_yz].strip()
            return title[:100]

    return f"最高人民法院公报案例 {case_number}"

def parse_case_content(content):
    """解析案件内容，提取各字段

    格式特点：案件标题和元数据在同一行连续排列，无分隔空格
    如：***案审理法院：最高人民法院案号：(2016)最高法民再149号裁判日期：2016.07.28案由：民事/...
    """
    lines = content.strip().split('\n')
    text = content

    if len(lines) > 1:
        combined = lines[1]

        # Find positions of all metadata labels (they appear in order on the combined line)
        pos_yz = combined.find('审理法院')  # 审理法院
        pos_ah = combined.find('案号')      # 案号
        pos_rq = combined.find('裁判日期')  # 裁判日期
        pos_ay = combined.find('案由')      # 案由

        # Extract title (before 审理法院)
        if pos_yz > 5:
            title_part = combined[:pos_yz].strip()
        else:
            title_part = combined[:min(pos_ah, pos_rq, pos_ay) if min(pos_ah, pos_rq, pos_ay) > 0 else len(combined)].strip()

        # Extract court (between 审理法院 and 案号)
        if pos_yz > 0 and pos_ah > pos_yz:
            court = combined[pos_yz+4:pos_ah].replace('：', '').replace(':', '').strip()
        else:
            court = "最高人民法院"

        # Extract case number (between 案号 and 裁判日期)
        if pos_ah > 0 and pos_rq > pos_ah:
            case_number = combined[pos_ah+2:pos_rq].replace('：', '').replace(':', '').replace('(', '').replace('（', '').strip()
        else:
            case_number = ""

        # Extract date (between 裁判日期 and 案由)
        if pos_rq > 0 and pos_ay > pos_rq:
            date = combined[pos_rq+4:pos_ay].replace('：', '').replace(':', '').strip()
        else:
            date = ""

        # Extract case type (after 案由, until 当事人)
        if pos_ay > 0:
            case_type_full = combined[pos_ay+2:].strip()
            # Truncate at 当事人
            ay_idx = case_type_full.find('当')
            if ay_idx > 0:
                case_type = case_type_full[:ay_idx].strip()
            else:
                case_type = case_type_full.strip()
        else:
            case_type = ""

        # Also capture court and date from the full second line for backup
        if not court or court == "最高人民法院":
            court_match = re.search(r'审理法院\s*[:：]\s*([^案号]+?)(?=案号|$)', combined)
            if court_match:
                court = court_match.group(1).strip()
    else:
        court = "最高人民法院"
        case_number = ""
        date = ""
        case_type = ""

    # 案件事实 - look for content after 元数据 line
    facts_match = re.search(r'(?:原审法院经审理查明|审理查明)[：:]?(.*?)(?=(?:本院认为|原审法院认为|上诉人|$))', text, re.DOTALL)
    facts = facts_match.group(1).strip()[:1500] if facts_match else "（事实待补充）"

    # 裁判理由
    reasoning_match = re.search(r'本院认为[：:]?(.*?)判决如下', text, re.DOTALL)
    reasoning = reasoning_match.group(1).strip()[:1200] if reasoning_match else "（裁判理由待补充）"

    # 判决结果
    judgment_match = re.search(r'判决如下[：:]?\s*(.*?)(?=(?:本案|审判长|二审|$))', text, re.DOTALL)
    judgment = judgment_match.group(1).strip()[:500] if judgment_match else "（判决结果待补充）"

    return {
        'court': court,
        'case_number': case_number,
        'date': date,
        'case_type': case_type,
        'facts': facts,
        'reasoning': reasoning,
        'judgment': judgment
    }

def extract_tags(case_type, content):
    """提取tags"""
    tags = ["民事"]
    if case_type:
        parts = case_type.split('/')
        for p in parts[1:]:
            p = p.replace('纠纷', '').strip()
            if p and p not in tags:
                tags.append(p)
    if '知识产权' in content or '专利' in content or '商标' in content:
        tags.append('知识产权')
    if '合同' in content:
        tags.append('合同')
    if '劳动' in content or '工伤' in content:
        tags.append('劳动')
    return tags[:6]

def generate_synthesis(filepath):
    """生成synthesis页面内容"""
    filename = os.path.basename(filepath)
    content = open(filepath, encoding='utf-8').read()

    case_info = parse_case_content(content)
    case_num = case_info['case_number'] or extract_case_number(filename)
    title = extract_case_title(content, case_num)
    tags = extract_tags(case_info['case_type'], content)

    frontmatter = f"""---
title: {title}
type: synthesis
created: 2026-05-09
updated: 2026-05-09
tags: [{', '.join(tags)}, 最高人民法院, 公报案例]
source: "sources/2-案例库/公报案例/民事/{filename}"
related: []
案例分级: ⭐⭐⭐
问题意识: {case_info['case_type'] or '民事案件裁判要点'}
---

"""

    body = f"""## 案情

**审理法院**: {case_info['court']}
**裁判日期**: {case_info['date']}
**案号**: {case_num}
**案由**: {case_info['case_type']}

{case_info['facts']}

## 裁判要旨

{case_info['reasoning']}

## 判决结果

{case_info['judgment']}
"""

    return frontmatter + body

# Process files
processed = 0
skipped = 0
errors = 0

for i, filename in enumerate(files):
    try:
        target_name = make_target_name(filename)
        target_path = os.path.join(TARGET_DIR, target_name)

        # Overwrite existing files to fix content
        # if os.path.exists(target_path):
        #     skipped += 1
        #     continue

        filepath = os.path.join(SOURCE_DIR, filename)
        synthesis_content = generate_synthesis(filepath)

        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(synthesis_content)

        processed += 1
        if processed % 20 == 0:
            print(f"Processed {processed} files...")

    except Exception as e:
        errors += 1
        print(f"Error: {filename}: {e}")

print(f"\nDone: {processed} created, {skipped} skipped, {errors} errors")