#!/usr/bin/env python3
"""Extract SPP Guide Cases from source files to wiki/syntheses/"""

import re
from pathlib import Path

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/syntheses")

def extract_cases(content):
    """Extract all cases from a source file"""
    cases = []

    # Pattern 1: **（检例第X号）** followed by **casename** (first batch format)
    pattern_1 = r'\*\*（检例第(\d+)号）\*\*\s*\n\*\*(.+?)\*\*'
    # Pattern 2: ** （检例第X号）** on one line, **casename** on next line (file 39 style)
    pattern_2 = r'\*\* （检例第(\d+)号）\*\*\s*\n\*\*(.+?)\*\*'
    # Pattern 3: **casename** on one line, ** （检例第X号）** on next line (later batch format)
    pattern_3 = r'\*\*(.+?)\*\*\s*\n\*\* （检例第(\d+)号）\*\*'
    # Pattern 4: **casename (no closing **) on line, ** （检例第X号） on next line (file 39 variant)
    pattern_4 = r'\*\*(.+?)\s*\n\*\* （检例第(\d+)号）\*\*'
    # Pattern 5: casename followed by （检例第X号） on next line (some files like file 10)
    pattern_5 = r'^(.+?)\s*\n（检例第(\d+)号）'

    matches_1 = list(re.finditer(pattern_1, content))
    matches_2 = list(re.finditer(pattern_2, content))

    # Combine and sort by position
    all_matches = []
    for m in re.finditer(pattern_1, content, re.MULTILINE):
        all_matches.append((m.start(), m, 1))
    for m in re.finditer(pattern_2, content, re.MULTILINE):
        all_matches.append((m.start(), m, 2))
    for m in re.finditer(pattern_3, content, re.MULTILINE):
        all_matches.append((m.start(), m, 3))
    for m in re.finditer(pattern_4, content, re.MULTILINE):
        all_matches.append((m.start(), m, 4))
    for m in re.finditer(pattern_5, content, re.MULTILINE):
        all_matches.append((m.start(), m, 5))
    all_matches.sort(key=lambda x: x[0])

    for i, (start_pos, match, ptype) in enumerate(all_matches):
        # Handle different patterns - group 1,2 or 3,4 depending on pattern type
        if ptype == 1:
            case_num = int(match.group(1))
            case_name = match.group(2).strip()
        elif ptype == 2:
            case_num = int(match.group(1))
            case_name = match.group(2).strip()
        elif ptype == 3:
            case_name = match.group(1).strip()
            case_num = int(match.group(2))
        elif ptype == 4:
            case_name = match.group(1).strip()
            case_num = int(match.group(2))
        elif ptype == 5:
            case_name = match.group(1).strip()
            case_num = int(match.group(2))

        # Start and end positions for this case
        start = match.end()
        if i + 1 < len(all_matches):
            end = all_matches[i + 1][1].start()
        else:
            end = len(content)

        case_text = content[start:end]

        # Extract sections
        yz_pattern = r'\*\*【要旨】\*\*\s*\n(.*?)(?=\*\*【|$)'
        ja_pattern = r'\*\*【基本案情】\*\*\s*\n(.*?)(?=\*\*【|$)'
        ss_pattern = r'\*\*【诉讼过程】\*\*\s*\n(.*?)(?=\*\*【|$)'

        yz_match = re.search(yz_pattern, case_text, re.DOTALL)
        ja_match = re.search(ja_pattern, case_text, re.DOTALL)
        ss_match = re.search(ss_pattern, case_text, re.DOTALL)

        yz = yz_match.group(1).strip() if yz_match else ""
        ja = ja_match.group(1).strip() if ja_match else ""
        ss = ss_match.group(1).strip() if ss_match else ""

        # Extract related laws
        law_pattern = r'《([^》]+)》'
        laws = re.findall(law_pattern, yz + ja + ss)
        laws = list(set(laws))[:5]  # Dedupe, keep max 5

        cases.append({
            'num': case_num,
            'name': case_name,
            'yazi': yz,
            'anji': ja,
            'susong': ss,
            'laws': laws
        })

    return cases

def generate_wiki_case(case, source_file):
    """Generate wiki page content for a single case"""
    num = case['num']
    name = case['name']
    yazi = case['yazi']
    anji = case['anji']
    susong = case['susong']
    laws = case['laws']

    # Extract topic/keywords from case name
    topics = []
    if '案' in name:
        topic = name.split('案')[0].strip()
        if topic:
            topics.append(topic)

    tags = ['指导性案例', '最高人民检察院', f'检例第{num}号'] + topics

    # Build related links
    related = []
    for law in laws:
        if '刑法' in law:
            related.append(f'[[concept_{law}]]')
        elif '刑事诉讼法' in law:
            related.append(f'[[concept_{law}]]')

    related_str = '\n  - '.join(related) if related else ''

    # Create wiki content
    content = f"""---
title: {name}
type: synthesis
created: 2026-05-11
updated: 2026-05-11
tags: [{', '.join(tags)}]
source: "sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/{source_file}"
related:
  - {related_str}
案例分级: ⭐⭐⭐⭐⭐
问题意识: {name}的裁判要旨
---

## 裁判要旨

{yazi}

## 基本案情

anji

## 诉讼过程

{susong}
"""

    # Clean up empty sections
    content = content.replace('\nanji\n', '\n（详见原文）\n')
    content = content.replace('\nsusong\n', '\n（详见原文）\n')

    return content

def main():
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    source_files = sorted(SOURCE_DIR.glob("*.md"))
    print(f"Source files: {len(source_files)}")

    total_cases = 0
    new_cases = 0

    for src_file in source_files:
        content = src_file.read_text(encoding='utf-8')
        cases = extract_cases(content)
        total_cases += len(cases)

        print(f"{src_file.name}: {len(cases)} cases")

        for case in cases:
            num = case['num']
            target_file = TARGET_DIR / f"SPP_GuideCase_检例第{num}号.md"

            # Skip if already exists
            if target_file.exists():
                continue

            new_cases += 1
            wiki_content = generate_wiki_case(case, src_file.name)
            target_file.write_text(wiki_content, encoding='utf-8')

    print(f"\nTotal cases: {total_cases}")
    print(f"New files created: {new_cases}")

if __name__ == "__main__":
    main()