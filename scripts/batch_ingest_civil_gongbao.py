#!/usr/bin/env python3
"""Batch ingest: sources/2-案例库/公报案例/民事/ -> wiki/syntheses/"""

import re, os, pathlib, sys

VAULT = pathlib.Path(r"D:\AI agent\tkk-library")
SRC_DIR = VAULT / "sources" / "2-案例库" / "公报案例" / "民事"
TGT_DIR = VAULT / "wiki" / "syntheses"
TGT_DIR.mkdir(parents=True, exist_ok=True)

FILES = [
    "公报案例 (2008)苏民三终字第0071号.md",
    "公报案例 (2008)苏民三终字第0220号.md",
    "公报案例 (2009)民提字第17号.md",
    "公报案例 (2009)民提字第84号.md",
    "公报案例 (2009)民申字第1065号.md",
    "公报案例 (2009)民申字第1068号.md",
    "公报案例 (2009)沪一中民五(知)初字第211号.md",
    "公报案例 (2009)沪高民二(商)终字第22号.md",
    "公报案例 (2009)沪高民四(海)终字第239号.md",
    "公报案例 (2009)沪高民四(海)终字第241号.md",
    "公报案例 (2009)湖德商初字第52号.md",
    "公报案例 (2009)苏民三终字第0091号.md",
    "公报案例 (2009)西民四初字第302号.md",
    "公报案例 (2009)长民三(民)初字第1020号.md",
    "公报案例 (2009)静民一(民)初字第779号.md",
    "公报案例 (2010)安民二终字第575号.md",
    "公报案例 (2010)民一终字第13号.md",
    "公报案例 (2010)民一终字第17号.md",
    "公报案例 (2010)民一终字第45号.md",
    "公报案例 (2010)民二终字第19号.md",
    "公报案例 (2010)民再申字第163号.md",
    "公报案例 (2010)民提字第10号.md",
    "公报案例 (2010)民提字第111号.md",
    "公报案例 (2010)民提字第27号.md",
    "公报案例 (2010)民提字第48号.md",
    "公报案例 (2010)民申字第1276号.md",
    "公报案例 (2010)民申字第27号.md",
    "公报案例 (2010)沪一中民二(民)终字第3692号.md",
    "公报案例 (2010)沪二中民四(商)终字第41号.md",
    "公报案例 (2010)黄民三(知)初字第28号.md",
    "公报案例 (2011)宁知民终字第16号.md",
    "公报案例 (2011)平民终字第118号.md",
    "公报案例 (2011)执复字第2号.md",
    "公报案例 (2011)执监字第15号.md",
    "公报案例 (2011)民抗字第48号.md",
    "公报案例 (2011)民提字第104号.md",
    "公报案例 (2011)民提字第12号.md",
    "公报案例 (2011)民提字第16号.md",
    "公报案例 (2011)民提字第292号.md",
    "公报案例 (2011)民提字第29号.md",
    "公报案例 (2011)民提字第307号.md",
    "公报案例 (2011)民提字第320号.md",
    "公报案例 (2011)民提字第331号.md",
    "公报案例 (2011)民提字第6号.md",
    "公报案例 (2011)民申字第429号.md",
    "公报案例 (2011)民申字第512号.md",
    "公报案例 (2011)民申字第777号.md",
    "公报案例 (2011)江宁民初字第04404号.md",
    "公报案例 (2011)湘高法民三终字第55号.md",
    "公报案例 (2011)衡中法民二再终字第3号.md",
]


def normalize_fullwidth(s):
    """全角数字和括号转半角"""
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


def extract_case_number(text):
    """从文件内容提取案号"""
    # Clean up \x07 characters
    clean = text.replace('\x07', '')
    # Try 案号 field first - handle newline between field name and colon
    m = re.search(r'案号\s*[：:]\s*(\([^)]+\)[^\n]*?号)', clean)
    if m:
        return normalize_fullwidth(m.group(1).strip())
    # Try # line
    m = re.search(r'^#\s*(.+?)$', clean, re.MULTILINE)
    if m:
        cn = m.group(1).strip()
        cn = normalize_fullwidth(cn)
        if cn:
            return cn
    return None


def extract_field(text, field_name):
    """提取元数据字段，处理包含\x07分隔符和换行的格式"""
    # Clean up \x07 characters for easier parsing
    clean = text.replace('\x07', '')
    # Find the field name
    idx = clean.find(field_name)
    if idx == -1:
        return None
    # Skip to after the field name
    after_name = clean[idx + len(field_name):]
    # Find the colon (may be preceded by newline/whitespace)
    colon_match = re.search(r'[\s\n]*[：:]\s*', after_name)
    if not colon_match:
        return None
    # Start after the colon
    start = colon_match.end()
    rest = after_name[start:]
    # Split by known field names
    end_markers = ['审理法院', '案号', '裁判日期', '案由', '上诉人', '被上诉人',
                   '申请再审', '被申请人', '一审原告', '一审被告', '原告', '被告',
                   '申请人', '再审申请人', '委托代理', '法定代表', '原审被告',
                   '原审原告', '一审第三人', '第三人']
    end = len(rest)
    for marker in end_markers:
        pos = rest.find(marker)
        if pos != -1 and pos < end:
            end = pos
    # Also check for double newline (section separator)
    double_nl = rest.find('\n\n')
    if double_nl != -1 and double_nl < end:
        end = double_nl
    val = rest[:end].strip()
    # Remove any remaining newlines within the value
    val = re.sub(r'\n+', ' ', val).strip()
    if val:
        return normalize_fullwidth(val)
    return None


def extract_parties(text):
    """提取当事人信息"""
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
    """提取审理法院"""
    court = extract_field(text, '审理法院')
    if not court:
        m = re.search(r'审理法院[：:]\s*(.+?)(?:\s|$)', text)
        if m:
            court = m.group(1).strip()
    return court or ''


def extract_date(text):
    """提取裁判日期，返回YYYY-MM-DD格式"""
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
    """提取案由"""
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
    """生成简要案名"""
    lines = text.strip().split('\n')
    found_hash = False
    for line in lines[:10]:
        line_stripped = line.strip()
        # Skip the # line (case number)
        if line_stripped.startswith('#'):
            found_hash = True
            continue
        # Skip empty lines
        if not line_stripped:
            continue
        # Skip lines that are just numbers
        if re.match(r'^\d+\s*$', line_stripped):
            continue
        # After the # line, the next non-empty line should be the case title
        if found_hash:
            # Remove trailing metadata fields
            title = re.split(r'审理法院|案号|裁判日期|案由', line_stripped)[0].strip()
            title = normalize_fullwidth(title)
            if title and len(title) > 3:
                return title[:80]
    return case_number


def extract_judgment(text):
    """提取裁判结果段落"""
    sections = []
    for m in re.finditer(r'(?:判决如下|裁定如下)[：:](.+?)(?=\n审判长|\n本判决|\n如不服|$)', text, re.DOTALL):
        sections.append(m.group(1).strip())
    if sections:
        return sections[-1][:2000]
    return ''


def extract_reasoning(text):
    """提取裁判要旨/本院认为"""
    reasoning_parts = []
    for m in re.finditer(r'本院(?:再审)?(?:经审理)?(?:认为)[：,，](.+?)(?=\n(?:综上|判决|裁定|依照|审判长))', text, re.DOTALL):
        reasoning_parts.append(m.group(1).strip())
    if reasoning_parts:
        longest = max(reasoning_parts, key=len)
        return longest[:3000]
    for m in re.finditer(r'(?:一审|二审)?法院(?:经审理)?(?:认为)[：,，](.+?)(?=\n(?:综上|判决|裁定|依照|审判长))', text, re.DOTALL):
        reasoning_parts.append(m.group(1).strip())
    if reasoning_parts:
        longest = max(reasoning_parts, key=len)
        return longest[:3000]
    return ''


def extract_facts(text):
    """提取案件事实"""
    facts_parts = []
    for m in re.finditer(r'(?:一审|二审)?法院(?:经审理)?查明[：,，](.+?)(?=\n(?:一审|二审)?法院(?:经审理)?认为|\n本院认为)', text, re.DOTALL):
        facts_parts.append(m.group(1).strip())
    if facts_parts:
        longest = max(facts_parts, key=len)
        return longest[:3000]
    for m in re.finditer(r'经审理查明[：,，](.+?)(?=\n本院|\n一审法院认为|\n法院认为)', text, re.DOTALL):
        facts_parts.append(m.group(1).strip())
    if facts_parts:
        return max(facts_parts, key=len)[:3000]
    return ''


def get_tags(cause, court):
    """生成标签"""
    tags = ['公报案例', '民事']
    if cause:
        tags.append(cause)
    if '最高' in court:
        tags.append('最高人民法院')
    elif '高级' in court:
        tags.append('高级人民法院')
    return tags


def make_wiki_filename(case_number):
    """生成wiki文件名"""
    clean = case_number.replace('/', '_').replace('\\', '_')
    clean = re.sub(r'[<>:"|?*]', '_', clean)
    return f"Court_公报案例_{clean}.md"


def process_file(src_name):
    """处理单个文件"""
    src_path = SRC_DIR / src_name
    if not src_path.exists():
        print(f"SKIP (not found): {src_name}")
        return False

    text = src_path.read_text(encoding='utf-8')

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
