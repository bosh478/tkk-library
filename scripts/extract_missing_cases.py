#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract missing SPP Guide Cases (158, 175, 184, 186, 228)"""

import re
from pathlib import Path

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/syntheses")

MISSING_FILES = {
    175: "44[2023-06-13]最高人民检察院发布第四十四批指导性案例.md",
    186: "46[2023-08-03]最高检发布第四十六批指导性案例.md",
}

def extract_case_from_file(file_path, case_num):
    content = file_path.read_text(encoding='utf-8')

    # Pattern: ** （检例第X号） with spaces around and  ** closing
    # For files like 44, 46 where formatting has extra spaces
    header_pattern = rf'\n\*\* （检例第{case_num}号）  \*\*\n'
    match = re.search(header_pattern, content)
    if not match:
        return None

    # Get the line before the header - which is the case name line
    # The line structure is: **casename\n** （检例第X号）\n
    start = match.start()
    before = content[:start]
    last_newline = before.rfind('\n')
    case_name_line = before[last_newline+1:].strip()

    # Remove leading ** from case name
    if case_name_line.startswith('**'):
        case_name = case_name_line[2:].strip()
    else:
        case_name = case_name_line

    # Now find the content between this header and the next header
    content_start = match.end()
    next_header = re.search(r'\n\*\* （检例第\d+号） \*\*\n', content[content_start:])
    if next_header:
        content_end = content_start + next_header.start()
    else:
        content_end = len(content)

    case_text = content[content_start:content_end]

    yz_pattern = r'\*\*【要旨】\*\*\s*\n(.*?)(?=\*\*【|$)'
    ja_pattern = r'\*\*【基本案情】\*\*\s*\n(.*?)(?=\*\*【|$)'
    ss_pattern = r'\*\*【诉讼过程】\*\*\s*\n(.*?)(?=\*\*【|$)'
    ting_pattern = r'\*\*【检察听证过程】\*\*\s*\n(.*?)(?=\*\*【|$)'
    gzy_pattern = r'\*\*【指导意义】\*\*\s*\n(.*?)(?=\*\*【|$)'

    yz_match = re.search(yz_pattern, case_text, re.DOTALL)
    ja_match = re.search(ja_pattern, case_text, re.DOTALL)
    ss_match = re.search(ss_pattern, case_text, re.DOTALL)
    ting_match = re.search(ting_pattern, case_text, re.DOTALL)
    gzy_match = re.search(gzy_pattern, case_text, re.DOTALL)

    yz = yz_match.group(1).strip() if yz_match else ""
    ja = ja_match.group(1).strip() if ja_match else ""
    ss = ss_match.group(1).strip() if ss_match else ""
    ting = ting_match.group(1).strip() if ting_match else ""
    gzy = gzy_match.group(1).strip() if gzy_match else ""

    law_pattern = r'《([^》]+)》'
    laws = re.findall(law_pattern, yz + ja + ss + ting + gzy)
    laws = list(set(laws))[:5]

    return {
        'num': case_num,
        'name': case_name,
        'yazi': yz,
        'anji': ja,
        'susong': ss,
        'tingzheng': ting,
        'laws': laws
    }

def generate_wiki_content(case, source_file):
    num = case['num']
    name = case['name']
    yazi = case['yazi']
    anji = case['anji']
    susong = case['susong']
    laws = case['laws']

    topics = []
    if '案' in name:
        topic = name.split('案')[0].strip()
        if topic:
            topics.append(topic)

    tags = ['指导性案例', '最高人民检察院', f'检例第{num}号'] + topics

    related = []
    for law in laws:
        if '刑法' in law:
            related.append(f'[[concept_{law}]]')
        elif '刑事诉讼法' in law:
            related.append(f'[[concept_{law}]]')

    related_str = '\n  - '.join(related) if related else ''

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

    content = content.replace('\nanji\n', '\n（详见原文）\n')
    content = content.replace('\nsusong\n', '\n（详见原文）\n')

    return content

def main():
    for case_num, filename in MISSING_FILES.items():
        src_path = SOURCE_DIR / filename
        if not src_path.exists():
            print(f"File not found: {filename}")
            continue

        print(f"Processing case {case_num} from {filename}...")
        case = extract_case_from_file(src_path, case_num)
        if case:
            content = generate_wiki_content(case, filename)
            target_path = TARGET_DIR / f"SPP_GuideCase_检例第{case_num}号.md"
            target_path.write_text(content, encoding='utf-8')
            print(f"  Created: {target_path.name}")
        else:
            print(f"  Failed to extract case {case_num}")

if __name__ == "__main__":
    main()