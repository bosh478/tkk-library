#!/usr/bin/env python3
"""Batch ingest: sources/2-案例库/公报案例/民事/ (2014-2017) -> wiki/syntheses/"""

import re, os, pathlib

VAULT = pathlib.Path(r"D:\AI agent\tkk-library")
SRC_DIR = VAULT / "sources" / "2-案例库" / "公报案例" / "民事"
TGT_DIR = VAULT / "wiki" / "syntheses"
TGT_DIR.mkdir(parents=True, exist_ok=True)

FILES = [
    "公报案例 (2014)黄浦民五(商)初字第9721号.md",
    "公报案例 (2015)宁民诉终字第36号.md",
    "公报案例 (2015)民一终字第150号.md",
    "公报案例 (2015)民一终字第260号.md",
    "公报案例 (2015)民一终字第37号.md",
    "公报案例 (2015)民一终字第78号.md",
    "公报案例 (2015)民三终字第8号.md",
    "公报案例 (2015)民二终字第167号.md",
    "公报案例 (2015)民二终字第191号.md",
    "公报案例 (2015)民二终字第236号.md",
    "公报案例 (2015)民二终字第351号.md",
    "公报案例 (2015)民二终字第428号.md",
    "公报案例 (2015)民四终字第9号.md",
    "公报案例 (2015)民提字第126号.md",
    "公报案例 (2015)民提字第128号.md",
    "公报案例 (2015)民提字第175号.md",
    "公报案例 (2015)民提字第23号.md",
    "公报案例 (2015)民提字第64号.md",
    "公报案例 (2015)民提字第74号.md",
    "公报案例 (2015)民申字第1070号.md",
    "公报案例 (2015)民申字第1366号.md",
    "公报案例 (2015)民申字第1823号.md",
    "公报案例 (2015)民申字第2633号.md",
    "公报案例 (2015)民申字第3640号.md",
    "公报案例 (2015)民申字第956号.md",
    "公报案例 (2015)沪二中民一(民)终字第1807号.md",
    "公报案例 (2015)沪二中民一(民)终字第1854号.md",
    "公报案例 (2015)沪知民初字第58号.md",
    "公报案例 (2015)黄浦民一(民)初字第2228号.md",
    "公报案例 (2015)鼓商初字第1972号.md",
    "公报案例 (2016)最高法民再149号.md",
    "公报案例 (2016)最高法民再238号.md",
    "公报案例 (2016)最高法民再251号.md",
    "公报案例 (2016)最高法民再51号.md",
    "公报案例 (2016)最高法民再61号.md",
    "公报案例 (2016)最高法民申1045号.md",
    "公报案例 (2016)最高法民终124号.md",
    "公报案例 (2016)最高法民终19号.md",
    "公报案例 (2016)最高法民终528号.md",
    "公报案例 (2016)最高法民终650号.md",
    "公报案例 (2016)最高法民终763号.md",
    "公报案例 (2016)最高法民终802号.md",
    "公报案例 (2016)最高法民终字第484号.md",
    "公报案例 (2016)沪0115民初81221号.md",
    "公报案例 (2016)苏0116民初1733号.md",
    "公报案例 (2016)苏01民终116号.md",
    "公报案例 (2017)最高法民再174号.md",
    "公报案例 (2017)最高法民申2148号.md",
    "公报案例 (2017)最高法民申2483号.md",
    "公报案例 (2017)最高法民申2817号.md",
]


def normalize_fullwidth(s):
    result = []
    for ch in s:
        code = ord(ch)
        if 0xFF10 <= code <= 0xFF19:
            result.append(chr(code - 0xFEE0))
        elif ch == '（':
            result.append('(')
        elif ch == '）':
            result.append(')')
        else:
            result.append(ch)
    return ''.join(result)


def extract_field_multiline(text, field_name):
    """Extract field from multi-line format where field name, colon, and value are on separate lines"""
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if field_name in line:
            # Check if value is on same line after colon
            m = re.search(rf'{field_name}[：:]\s*(.+)', line)
            if m:
                return normalize_fullwidth(m.group(1).strip())
            # Check if colon is on next line
            if i + 1 < len(lines) and re.match(r'^[：:]\s*$', lines[i+1]):
                if i + 2 < len(lines):
                    val = lines[i+2].strip()
                    if val:
                        return normalize_fullwidth(val)
            # Check if value is on next line (colon on same line)
            if i + 1 < len(lines) and '：' not in line:
                val = lines[i+1].strip()
                if val and not any(f in val for f in ['审理法院', '案号', '裁判日期', '案由']):
                    return normalize_fullwidth(val)
    return None


def extract_case_number(text):
    # Try multi-line format first
    cn = extract_field_multiline(text, '案号')
    if cn:
        # Clean up: extract just the case number pattern
        m = re.search(r'(\([^)]+\)[^\n]*?号)', cn)
        if m:
            return normalize_fullwidth(m.group(1).strip())
        return cn
    # Fallback: try single line
    m = re.search(r'案号[：:]\s*(\([^)]+\)[^\n]*?号)', text)
    if m:
        return normalize_fullwidth(m.group(1).strip())
    m = re.search(r'^#\s*(.+?)$', text, re.MULTILINE)
    if m:
        cn = m.group(1).strip()
        cn = normalize_fullwidth(cn)
        if cn:
            return cn
    return None


def extract_field(text, field_name):
    """Extract field value, handling both single-line and multi-line formats"""
    # Try multi-line format first
    val = extract_field_multiline(text, field_name)
    if val:
        return val
    # Fallback: try single line format
    next_fields = r'(?:审理法院|案号|裁判日期|案由|上诉人|被上诉人|申请再审|被申请人|一审原告|一审被告|原告|被告|申请人|再审申请人|委托代理|法定代表|原审被告|原审原告|一审第三人|第三人)'
    pattern = rf'{field_name}[：:]\s*(.+?)(?={next_fields}|$)'
    m = re.search(pattern, text)
    if m:
        val = m.group(1).strip().rstrip()
        return normalize_fullwidth(val)
    return None


def extract_parties(text):
    parties = []
    patterns = [
        r'(?:原告|上诉人|再审申请人|申请人)[（(][^)）]*[)）]：(.+?)(?:[。，])',
        r'(?:被告|被上诉人|被申请人)[（(][^)）]*[)）]：(.+?)(?:[。，])',
        r'(?:原审被告|原审原告|一审被告|一审原告)[：:](.+?)(?:[。，])',
    ]
    for pat in patterns:
        for m in re.finditer(pat, text):
            name = m.group(1).strip()
            name = re.split(r'[，,。]', name)[0].strip()
            name = re.sub(r'委托代理人[：:].*$', '', name).strip()
            if name and 1 < len(name) < 30 and name not in parties:
                parties.append(name)
    return '、'.join(parties[:6]) if parties else ''


def extract_court(text):
    court = extract_field(text, '审理法院')
    if not court:
        m = re.search(r'审理法院[：:]\s*(.+?)(?:\s|$)', text)
        if m:
            court = m.group(1).strip()
    return court or ''


def extract_date(text):
    date_str = extract_field(text, '裁判日期')
    if not date_str:
        m = re.search(r'裁判日期[：:]\s*(.+?)(?:\s|$)', text)
        if m:
            date_str = m.group(1).strip()
    if date_str:
        date_str = normalize_fullwidth(date_str)
        m = re.match(r'(\d{4})[.\-/](\d{1,2})[.\-/](\d{1,2})', date_str)
        if m:
            return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    return ''


def extract_cause(text):
    cause = extract_field(text, '案由')
    if not cause:
        m = re.search(r'案由[：:]\s*(.+?)(?:\s|$)', text)
        if m:
            cause = m.group(1).strip()
    if cause:
        cause = normalize_fullwidth(cause)
        parts = [p.strip() for p in cause.split('/') if p.strip()]
        if len(parts) > 1:
            return parts[-1]
        return parts[0] if parts else cause
    return ''


def extract_title(text, case_number):
    lines = text.strip().split('\n')
    for line in lines[:5]:
        line = line.strip().lstrip('#').strip()
        if not line or re.match(r'^\d+\s*$', line):
            continue
        title = re.split(r'审理法院|案号|裁判日期|案由', line)[0].strip()
        title = normalize_fullwidth(title)
        if title and len(title) > 3:
            return title[:80]
    return case_number


def extract_judgment(text):
    sections = []
    for m in re.finditer(r'(?:判决如下|裁定如下)[：:](.+?)(?=\n审判长|\n本判决|\n如不服|$)', text, re.DOTALL):
        sections.append(m.group(1).strip())
    if sections:
        return sections[-1][:2000]
    return ''


def extract_reasoning(text):
    reasoning_parts = []
    for m in re.finditer(r'本院(?:再审)?(?:经审理)?(?:认为)[：,，](.+?)(?=\n(?:综上|判决|裁定|依照|审判长))', text, re.DOTALL):
        reasoning_parts.append(m.group(1).strip())
    if reasoning_parts:
        return max(reasoning_parts, key=len)[:3000]
    for m in re.finditer(r'(?:一审|二审)?法院(?:经审理)?(?:认为)[：,，](.+?)(?=\n(?:综上|判决|裁定|依照|审判长))', text, re.DOTALL):
        reasoning_parts.append(m.group(1).strip())
    if reasoning_parts:
        return max(reasoning_parts, key=len)[:3000]
    return ''


def extract_facts(text):
    facts_parts = []
    for m in re.finditer(r'(?:一审|二审)?法院(?:经审理)?查明[：,，](.+?)(?=\n(?:一审|二审)?法院(?:经审理)?认为|\n本院认为)', text, re.DOTALL):
        facts_parts.append(m.group(1).strip())
    if facts_parts:
        return max(facts_parts, key=len)[:3000]
    for m in re.finditer(r'经审理查明[：,，](.+?)(?=\n本院|\n一审法院认为|\n法院认为)', text, re.DOTALL):
        facts_parts.append(m.group(1).strip())
    if facts_parts:
        return max(facts_parts, key=len)[:3000]
    return ''


def get_tags(cause, court):
    tags = ['公报案例', '民事']
    if cause:
        tags.append(cause)
    if '最高' in court:
        tags.append('最高人民法院')
    elif '高级' in court:
        tags.append('高级人民法院')
    return tags


def make_wiki_filename(case_number):
    clean = case_number.replace('/', '_').replace('\\', '_')
    clean = re.sub(r'[<>:"|?*]', '_', clean)
    return f"Court_公报案例_{clean}.md"


def clean_text(text):
    """Remove control characters and clean up text"""
    # Remove BEL and other control characters except newline/tab
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    # Clean up whitespace
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'\r', '\n', text)
    return text


def process_file(src_name):
    src_path = SRC_DIR / src_name
    if not src_path.exists():
        print(f"SKIP (not found): {src_name}")
        return False

    text = src_path.read_text(encoding='utf-8')
    text = clean_text(text)
    case_number = extract_case_number(text)
    if not case_number:
        print(f"SKIP (no case number): {src_name}")
        return False

    court = extract_court(text)
    date = extract_date(text)
    cause = extract_cause(text)
    parties = extract_parties(text)
    title = extract_title(text, case_number)
    facts = extract_facts(text)
    reasoning = extract_reasoning(text)
    judgment = extract_judgment(text)
    tags = get_tags(cause, court)

    wiki_name = make_wiki_filename(case_number)
    wiki_path = TGT_DIR / wiki_name

    tags_str = ', '.join(tags)
    fm = f"""---
title: {title}
type: synthesis
tags: [{tags_str}]
case_number: {case_number}
court: {court}
date: {date}
cause: {cause}
source: "[[{src_name.replace('.md', '')}]]"
created: 2026-05-27
---"""

    body_parts = [fm, '', '## 案件信息', '']
    body_parts.append('| 字段 | 内容 |')
    body_parts.append('|------|------|')
    body_parts.append(f'| 案号 | {case_number} |')
    body_parts.append(f'| 审理法院 | {court} |')
    body_parts.append(f'| 裁判日期 | {date} |')
    body_parts.append(f'| 案由 | {cause} |')
    if parties:
        body_parts.append(f'| 当事人 | {parties} |')
    body_parts.append('')

    if facts:
        body_parts.append('## 案件事实')
        body_parts.append('')
        body_parts.append(facts)
        body_parts.append('')

    if reasoning:
        body_parts.append('## 裁判要旨')
        body_parts.append('')
        body_parts.append(reasoning)
        body_parts.append('')

    if judgment:
        body_parts.append('## 裁判结果')
        body_parts.append('')
        body_parts.append(judgment)
        body_parts.append('')

    body_parts.append('## 相关')
    body_parts.append('')
    body_parts.append(f'- [[{src_name.replace(".md", "")}]]')

    content = '\n'.join(body_parts)
    wiki_path.write_text(content, encoding='utf-8')
    print(f"OK: {wiki_name}")
    return True


def main():
    success = 0
    fail = 0
    for fname in FILES:
        if process_file(fname):
            success += 1
        else:
            fail += 1
    print(f"\nDone: {success} success, {fail} fail out of {len(FILES)}")


if __name__ == '__main__':
    main()
