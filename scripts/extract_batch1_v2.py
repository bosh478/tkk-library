#!/usr/bin/env python3
"""Extract first batch of topics from 裁判要旨精选"""

import re
import os

source_file = r"D:\AI agent\tkk-library\sources\司法观点、案例\《最高人民法院裁判要旨精选》中 最高法审管办 202504.md"

# Read the source file
with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Topics to extract for batch 1 (20 topics from 民商事篇)
topics_batch1 = [
    ("1_借款合同民间借贷", "借款合同、民间借贷", ["民间借贷", "借款合同"]),
    ("2_金融借款合同", "金融借款合同", ["金融借款"]),
    ("3_金融不良债权转让追偿合同", "金融不良债权转让、追偿合同", ["不良债权", "债权转让", "追偿"]),
    ("4_租赁合同", "租赁合同", ["租赁合同"]),
    ("5_融资租赁合同", "融资租赁合同", ["融资租赁"]),
    ("6_保理合同", "保理合同", ["保理合同"]),
    ("7_建设工程合同", "建设工程合同", ["建设工程", "施工合同"]),
    ("8_其他合同纠纷", "其他合同纠纷", []),
    ("9_合伙", "合伙", ["合伙"]),
    ("10_股东资格确认", "股东资格确认", ["股东资格"]),
    ("11_请求变更公司登记", "请求变更公司登记", ["变更公司登记"]),
    ("12_股东出资", "股东出资", ["股东出资"]),
    ("13_股权转让", "股权转让", ["股权转让"]),
    ("14_股东知情权", "股东知情权", ["知情权"]),
    ("15_公司决议", "公司决议", ["公司决议"]),
    ("16_盈余分配", "盈余分配", ["盈余分配"]),
    ("17_损害公司利益责任", "损害公司利益责任", ["损害公司利益"]),
    ("18_人格混同及损害债权人利益", "人格混同及损害债权人利益", ["人格混同"]),
    ("19_公司减资", "公司减资", ["公司减资"]),
    ("20_公司解散", "公司解散", ["公司解散"]),
]

# Extract cases from content
# Cases have format:
# # N 案例名称 (at start)
# ·案号
# ·合议庭成员
# ·关键词
# ·相关法条
# ## 【裁判要旨】
# content...
# ## 【案情摘要】
# content...

def extract_full_case(start_idx):
    """Extract complete case from start_idx (where a # N 标题 line is)"""
    case_lines = []
    i = start_idx
    in_case = False

    while i < len(lines):
        line = lines[i]

        # Start of a new case
        if re.match(r'^# \d+ ', line):
            if in_case:
                # We've reached the next case
                break
            in_case = True
            case_lines.append(line)
        elif in_case:
            case_lines.append(line)
        i += 1

    return '\n'.join(case_lines), i

def parse_case(case_text):
    """Parse case text into structured format"""
    result = {
        'title': '',
        'case_number': '',
        'panel': '',
        'keywords': '',
        'related_laws': '',
        '裁判要旨': '',
        '案情摘要': ''
    }

    lines = case_text.split('\n')
    current_section = None

    for line in lines:
        line = line.strip()

        # Case title
        title_match = re.match(r'^# \d+ (.+)$', line)
        if title_match:
            result['title'] = title_match.group(1).strip()
            continue

        # Section markers
        if line.startswith('·案号') or line.startswith('·案 号'):
            result['case_number'] = line.replace('·案号', '').replace('·案 号', '').strip()
            continue
        if line.startswith('•合议庭成员') or line.startswith('·合议庭成员'):
            result['panel'] = line.replace('•合议庭成员', '').replace('·合议庭成员', '').strip()
            continue
        if line.startswith('·关键词') or line.startswith('·关键词'):
            result['keywords'] = line.replace('·关键词', '').replace('·关键词', '').strip()
            continue
        if line.startswith('·相关法条') or line.startswith('·相关法条'):
            result['related_laws'] = line.replace('·相关法条', '').replace('·相关法条', '').strip()
            continue

        # Main content sections
        if '## 【裁判要旨】' in line or '【裁判要旨】' in line:
            current_section = '裁判要旨'
            continue
        if '## 【案情摘要】' in line or '【案情摘要】' in line:
            current_section = '案情摘要'
            continue

        if current_section and line:
            if result[current_section]:
                result[current_section] += ' ' + line
            else:
                result[current_section] = line

    return result

# Find all case starts in the content
case_starts = []
for i, line in enumerate(lines):
    if re.match(r'^# \d+ ', line):
        case_starts.append(i)

print(f"Found {len(case_starts)} cases total")

# Group cases by topic keywords
topic_cases = {topic[0]: [] for topic in topics_batch1}

for idx in case_starts:
    case_text, _ = extract_full_case(idx)
    parsed = parse_case(case_text)

    title = parsed.get('title', '')
    keywords = parsed.get('keywords', '')

    # Match to topic
    for topic_id, topic_name, topic_keywords in topics_batch1:
        if topic_keywords:
            for kw in topic_keywords:
                if kw in title or kw in keywords:
                    topic_cases[topic_id].append(parsed)
                    break
        # For "其他合同纠纷" - collect unmatched cases

print("\nCases per topic:")
for topic_id, cases in topic_cases.items():
    print(f"  {topic_id}: {len(cases)} cases")