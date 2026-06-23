#!/usr/bin/env python3
"""Batch ingest 公报案例 民事 2012-2014 files to wiki/syntheses/"""

import os
import re
from pathlib import Path

VAULT = Path(r"D:\AI agent\tkk-library")
SRC_DIR = VAULT / "sources" / "2-案例库" / "公报案例" / "民事"
TGT_DIR = VAULT / "wiki" / "syntheses"

TARGET_FILES = [
    "公报案例 (2012)广汉民初字第191号.md",
    "公报案例 (2012)民再申字第310号.md",
    "公报案例 (2012)民四终字第15号.md",
    "公报案例 (2012)民抗字第24号.md",
    "公报案例 (2012)民抗字第65号.md",
    "公报案例 (2012)民提字第11号.md",
    "公报案例 (2012)民提字第156号.md",
    "公报案例 (2012)民提字第1号.md",
    "公报案例 (2012)民提字第205号.md",
    "公报案例 (2012)民提字第44号.md",
    "公报案例 (2012)民申字第1282号.md",
    "公报案例 (2012)民申字第386号.md",
    "公报案例 (2012)沪高民三(知)终字第67号.md",
    "公报案例 (2012)苏中知民初字第0243号.md",
    "公报案例 (2012)鄂武东开民一初字第00028号.md",
    "公报案例 (2012)高民终字第918号.md",
    "公报案例 (2012)鲁民三终字第33号.md",
    "公报案例 (2012)黄浦民一(民)初字第95号.md",
    "公报案例 (2013)北民一终字第14号.md",
    "公报案例 (2013)宁民终字第2605号.md",
    "公报案例 (2013)徐民终字第0803号.md",
    "公报案例 (2013)民一终字第18号.md",
    "公报案例 (2013)民再申字第27号.md",
    "公报案例 (2013)民提字第116号.md",
    "公报案例 (2013)民提字第207号.md",
    "公报案例 (2013)民提字第210号.md",
    "公报案例 (2013)民提字第225号.md",
    "公报案例 (2013)民提字第231号.md",
    "公报案例 (2013)民提字第6号.md",
    "公报案例 (2013)民提字第73号.md",
    "公报案例 (2013)民提字第90号.md",
    "公报案例 (2013)民提字第95号.md",
    "公报案例 (2013)民申字第1567号.md",
    "公报案例 (2013)民申字第29号.md",
    "公报案例 (2013)民申字第675号.md",
    "公报案例 (2013)民申字第790号.md",
    "公报案例 (2013)鄂武昌民初字第00444号.md",
    "公报案例 (2013)鄂武汉中民终字第01019号.md",
    "公报案例 (2014)三中民终字第09467号.md",
    "公报案例 (2014)民一终字第38号.md",
    "公报案例 (2014)民一终字第56号.md",
    "公报案例 (2014)民一终字第69号.md",
    "公报案例 (2014)民二终字第199号.md",
    "公报案例 (2014)民提字第178号.md",
    "公报案例 (2014)民提字第191号.md",
    "公报案例 (2014)民申字第2225号.md",
    "公报案例 (2014)江宁民再初字第1号.md",
    "公报案例 (2014)江宁民初字第3935号.md",
    "公报案例 (2014)沪高民五(商)再提字第1号.md",
    "公报案例 (2014)长民一(民)初字第221号.md",
]


def normalize_fullwidth(text):
    """Convert fullwidth digits and parens to halfwidth"""
    # Fullwidth digits ０-９ -> 0-9
    for i in range(10):
        text = text.replace(chr(0xFF10 + i), str(i))
    # Fullwidth parens
    text = text.replace('（', '(').replace('）', ')')
    # Fullwidth period
    text = text.replace('．', '.')
    return text


def clean_text(text):
    """Remove control characters like \\x07 from text"""
    return text.replace('\x07', '')


def extract_field(text, field_name):
    """Extract a field value like '审理法院：xxx' or '案号：xxx'"""
    # Clean control chars first
    cleaned = clean_text(text)
    # Pattern: field_name + ：or : + value (until next field marker)
    # Handle newlines and whitespace between field name and colon
    pattern = rf'{field_name}\s*[：:]\s*(.*?)(?=\s*(?:审理法院|案号|裁判日期|案由)\s*[：:]|\Z)'
    m = re.search(pattern, cleaned, re.DOTALL)
    if m:
        val = m.group(1).strip()
        # Take only the first line of the value
        val = val.split('\n')[0].strip()
        return val
    return ""


def extract_court_name(text):
    """Extract court name"""
    return extract_field(text, "审理法院")


def extract_case_number(text):
    """Extract case number"""
    return extract_field(text, "案号")


def extract_date(text):
    """Extract judgment date and normalize to YYYY-MM-DD"""
    raw = extract_field(text, "裁判日期")
    if not raw:
        return ""
    # Normalize
    raw = raw.replace('年', '.').replace('月', '.').replace('日', '')
    raw = raw.strip().rstrip('.')
    parts = raw.split('.')
    if len(parts) == 3:
        y, m, d = parts
        return f"{y}-{int(m):02d}-{int(d):02d}"
    return raw


def extract_cause(text):
    """Extract cause of action (案由)"""
    raw = extract_field(text, "案由")
    if not raw:
        return ""
    # Get the last part after slashes (most specific)
    parts = raw.split('/')
    return parts[-1].strip() if parts else raw.strip()


def extract_parties(text):
    """Extract party names from the document"""
    lines = text.split('\n')
    parties = []
    for line in lines:
        line = line.strip()
        # Match patterns like "原告XXX" "被告XXX" "上诉人XXX" etc.
        m = re.match(r'(原告|被告|上诉人|被上诉人|再审申请人|被申请人|一审原告|一审被告|申请再审人)[：:（(]?([^，,。\n]+)', line)
        if m:
            role = m.group(1)
            name = m.group(2).strip().rstrip('。').rstrip('，')
            # Clean up
            name = re.sub(r'（.*?）', '', name)  # Remove parenthetical
            name = name.strip()
            if name and len(name) < 50:
                parties.append(f"{role}：{name}")
    return parties


def extract_parties_from_header(text):
    """Extract parties from the case header area (first few lines after title)"""
    cleaned = clean_text(text)
    # Get text between the title line and the first field marker
    m = re.search(r'案号\s*[：:]', cleaned[:5000])
    if not m:
        return ""
    header = cleaned[:m.start()]

    # Find party lines
    parties = []
    for line in header.split('\n'):
        line = line.strip()
        if not line:
            continue
        # Match party declarations
        m2 = re.match(r'^(原告|被告|上诉人|被上诉人|再审申请人|被申请人|一审原告|一审被告|一审第三人|申请再审人|原审原告|原审被告|申诉人|被申诉人)[：:（(]?', line)
        if m2:
            role = m2.group(1)
            rest = line[m2.end():]
            # Extract name - usually first entity name
            name_match = re.match(r'([^，,。\s（(]+)', rest)
            if name_match:
                name = name_match.group(1).strip()
                parties.append(f"{role}：{name}")
    return '、'.join(parties[:5]) if parties else ""


def extract_fact_section(text):
    """Extract the fact section (案件事实)"""
    text = clean_text(text)
    # Try to find "经审理查明" or similar sections
    markers = ['经审理查明', '一审法院查明', '本院查明', '原审查明', '一审认定']
    fact_start = -1
    for marker in markers:
        idx = text.find(marker)
        if idx >= 0:
            fact_start = idx
            break

    if fact_start < 0:
        # Try to get from after parties section
        fact_start = text.find('审理法院')
        if fact_start >= 0:
            # Skip past the metadata block
            after_meta = text[fact_start:]
            m = re.search(r'案由[：:].*?\n', after_meta)
            if m:
                fact_start = fact_start + m.end()
            else:
                fact_start = -1

    if fact_start < 0:
        return ""

    # Find the end - typically "本院认为" or similar reasoning section
    end_markers = ['本院认为', '一审法院认为', '原审法院认为', '本院经审查认为', '综上', '裁判要旨']
    fact_end = len(text)
    for marker in end_markers:
        idx = text.find(marker, fact_start + 100)
        if idx >= 0 and idx < fact_end:
            fact_end = idx

    fact_text = text[fact_start:fact_end].strip()

    # Clean up and truncate if too long
    fact_text = re.sub(r'\s+', ' ', fact_text)
    if len(fact_text) > 3000:
        fact_text = fact_text[:3000] + '……'

    return fact_text


def extract_reasoning(text):
    """Extract court reasoning (裁判理由)"""
    text = clean_text(text)
    markers = ['本院认为', '一审法院认为', '原审法院认为', '本院经审查认为']
    reason_start = -1
    for marker in markers:
        idx = text.find(marker)
        if idx >= 0:
            reason_start = idx
            break

    if reason_start < 0:
        return ""

    # Find the end - typically "判决如下" or "裁定如下"
    end_markers = ['判决如下', '裁定如下', '综上所述']
    reason_end = len(text)
    for marker in end_markers:
        idx = text.find(marker, reason_start)
        if idx >= 0 and idx < reason_end:
            reason_end = idx

    reason_text = text[reason_start:reason_end].strip()
    reason_text = re.sub(r'\s+', ' ', reason_text)
    if len(reason_text) > 3000:
        reason_text = reason_text[:3000] + '……'

    return reason_text


def extract_result(text):
    """Extract judgment result (裁判结果)"""
    text = clean_text(text)
    markers = ['判决如下', '裁定如下']
    result_start = -1
    for marker in markers:
        idx = text.find(marker)
        if idx >= 0:
            result_start = idx + len(marker)
            break

    if result_start < 0:
        return ""

    # Get until the judge signature or end
    end_markers = ['审 判', '审判长', '书 记', '二〇', '二0', '扫一扫']
    result_end = len(text)
    for marker in end_markers:
        idx = text.find(marker, result_start)
        if idx >= 0 and idx < result_end:
            result_end = idx

    result_text = text[result_start:result_end].strip()
    result_text = re.sub(r'\s+', '\n', result_text)
    return result_text


def extract_tags(cause):
    """Generate tags from cause of action"""
    tags = ["公报案例", "民事"]
    if cause:
        tags.append(cause)
    return tags


def extract_cause_short(cause):
    """Extract short cause tag"""
    if not cause:
        return ""
    # Remove common prefixes
    for prefix in ['民事/', '与公司、证券、保险、票据等有关的民事纠纷/', '合同纠纷/']:
        if cause.startswith(prefix):
            cause = cause[len(prefix):]
    return cause.split('/')[-1] if '/' in cause else cause


def get_source_filename(filename):
    """Get the source reference filename without .md"""
    return filename.replace('.md', '')


def get_wiki_filename(case_number):
    """Generate wiki filename from case number"""
    # Clean case number
    cn = normalize_fullwidth(case_number)
    # Remove spaces
    cn = cn.replace(' ', '')
    # Extract just the number part for filename
    return f"Court_公报案例_{cn}.md"


def make_short_title(case_number, cause):
    """Make a short title for the wiki page"""
    cn = normalize_fullwidth(case_number)
    cause_short = extract_cause_short(cause)
    if cause_short:
        return f"{cn} {cause_short}"
    return cn


def format_fact(fact):
    """Format fact text with proper paragraph breaks"""
    if not fact:
        return "（源文件未提供可提取的事实部分）"

    # Try to split into meaningful paragraphs
    # Split on sentence boundaries
    sentences = re.split(r'(?<=[。；])', fact)
    paragraphs = []
    current = ""
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        current += s
        if len(current) > 200:
            paragraphs.append(current)
            current = ""
    if current:
        paragraphs.append(current)

    return '\n\n'.join(paragraphs[:8])  # Limit to 8 paragraphs


def format_reasoning(reasoning):
    """Format reasoning text"""
    if not reasoning:
        return ""
    sentences = re.split(r'(?<=[。；])', reasoning)
    paragraphs = []
    current = ""
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        current += s
        if len(current) > 300:
            paragraphs.append(current)
            current = ""
    if current:
        paragraphs.append(current)
    return '\n\n'.join(paragraphs[:10])


def process_file(filename):
    """Process a single source file and write wiki page"""
    src_path = SRC_DIR / filename
    if not src_path.exists():
        return f"SKIP: {filename} not found"

    with open(src_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Clean control characters
    text = clean_text(text)

    # Extract fields
    case_number_raw = extract_case_number(text)
    case_number = normalize_fullwidth(case_number_raw)
    court = extract_court_name(text)
    date = extract_date(text)
    cause_raw = extract_cause(text)
    cause = cause_raw.split('/')[-1].strip() if '/' in cause_raw else cause_raw.strip()

    # Extract content sections
    parties = extract_parties_from_header(text)
    fact = extract_fact_section(text)
    reasoning = extract_reasoning(text)
    result = extract_result(text)

    # Generate wiki filename
    wiki_fn = get_wiki_filename(case_number_raw)
    tgt_path = TGT_DIR / wiki_fn

    # Generate short title
    short_title = make_short_title(case_number_raw, cause_raw)

    # Tags
    tags = extract_tags(cause)

    # Source reference
    source_ref = f"[[{get_source_filename(filename)}]]"

    # Format parties for table
    parties_display = parties if parties else "见判决书"

    # Build fact content
    fact_display = format_fact(fact)
    reasoning_display = format_reasoning(reasoning)

    # Build wiki page
    content = f"""---
title: {short_title}
type: synthesis
tags: [{', '.join(tags)}]
case_number: {case_number}
court: {court}
date: {date}
cause: {cause}
source: "{source_ref}"
created: 2026-05-27
---

## 案件信息

| 字段 | 内容 |
|------|------|
| 案号 | {case_number} |
| 审理法院 | {court} |
| 裁判日期 | {date} |
| 案由 | {cause} |
| 当事人 | {parties_display} |

## 案件事实

{fact_display}

## 裁判要旨

{reasoning_display}

## 裁判结果

{result}

## 相关

- {source_ref}
"""

    with open(tgt_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return f"OK: {wiki_fn}"


def main():
    TGT_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    for fn in TARGET_FILES:
        r = process_file(fn)
        results.append(r)

    # Count results
    ok = sum(1 for r in results if r.startswith("OK"))
    skip = sum(1 for r in results if r.startswith("SKIP"))
    err = sum(1 for r in results if r.startswith("ERR"))

    print(f"\n=== Results ===")
    print(f"OK: {ok}, SKIP: {skip}, ERR: {err}, Total: {len(results)}")

    for r in results:
        if not r.startswith("OK"):
            print(r)


if __name__ == "__main__":
    main()
