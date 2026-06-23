#!/usr/bin/env python3
"""Create synthesis files for first batch of topics"""

import re
import os

source_file = r"D:\AI agent\tkk-library\sources\司法观点、案例\《最高人民法院裁判要旨精选》中 最高法审管办 202504.md"
output_dir = r"D:\AI agent\tkk-library\wiki\syntheses"

# Read the source file
with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

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
        '案情摘要': '',
        'author': ''
    }

    lines = case_text.split('\n')
    current_section = None

    for i, line in enumerate(lines):
        line_stripped = line.strip()

        # Case title
        title_match = re.match(r'^# \d+ (.+)$', line_stripped)
        if title_match:
            result['title'] = title_match.group(1).strip()
            continue

        # Metadata
        if '·案号' in line or '·案 号' in line:
            result['case_number'] = re.sub(r'^[·•]\案号[：:]?\s*', '', line).strip()
            continue
        if '•合议庭成员' in line or '·合议庭成员' in line:
            result['panel'] = re.sub(r'^[·•]\合议庭成员[：:]?\s*', '', line).strip()
            continue
        if '·关键词' in line or '·关键词' in line:
            result['keywords'] = re.sub(r'^[·•]\关键词[：:]?\s*', '', line).strip()
            continue
        if '·相关法条' in line or '·相关法条' in line:
            result['related_laws'] = re.sub(r'^[·•]\相关法条[：:]?\s*', '', line).strip()
            continue

        # Main content sections
        if '## 【裁判要旨】' in line or '【裁判要旨】' in line:
            current_section = '裁判要旨'
            continue
        if '## 【案情摘要】' in line or '【案情摘要】' in line:
            current_section = '案情摘要'
            continue

        if current_section and line_stripped:
            if result[current_section]:
                result[current_section] += ' ' + line_stripped
            else:
                result[current_section] = line_stripped

        # Author at end
        if '（撰写人：' in line:
            author_match = re.search(r'（撰写人：([^）]+)）', line)
            if author_match:
                result['author'] = author_match.group(1)

    return result

# Find all case starts
case_starts = []
for i, line in enumerate(lines):
    if re.match(r'^# \d+ ', line):
        case_starts.append(i)

print(f"Found {len(case_starts)} cases total")

# Define topics with their keywords
topics_config = [
    ("synthesis_裁判要旨精选_中_01_借款合同民间借贷", "借款合同、民间借贷", ["民间借贷", "借款合同纠纷"]),
    ("synthesis_裁判要旨精选_中_02_金融借款合同", "金融借款合同", ["金融借款"]),
    ("synthesis_裁判要旨精选_中_03_金融不良债权转让追偿合同", "金融不良债权转让、追偿合同", ["不良债权", "债权转让", "追偿"]),
    ("synthesis_裁判要旨精选_中_04_租赁合同", "租赁合同", ["租赁合同"]),
    ("synthesis_裁判要旨精选_中_05_融资租赁合同", "融资租赁合同", ["融资租赁"]),
    ("synthesis_裁判要旨精选_中_06_保理合同", "保理合同", ["保理合同"]),
    ("synthesis_裁判要旨精选_中_07_建设工程合同", "建设工程合同", ["建设工程", "施工合同"]),
    ("synthesis_裁判要旨精选_中_08_其他合同纠纷", "其他合同纠纷", []),
    ("synthesis_裁判要旨精选_中_09_合伙", "合伙", ["合伙"]),
    ("synthesis_裁判要旨精选_中_10_股东资格确认", "股东资格确认", ["股东资格"]),
    ("synthesis_裁判要旨精选_中_11_请求变更公司登记", "请求变更公司登记", ["变更公司登记"]),
    ("synthesis_裁判要旨精选_中_12_股东出资", "股东出资", ["股东出资"]),
    ("synthesis_裁判要旨精选_中_13_股权转让", "股权转让", ["股权转让"]),
    ("synthesis_裁判要旨精选_中_14_股东知情权", "股东知情权", ["知情权"]),
    ("synthesis_裁判要旨精选_中_15_公司决议", "公司决议", ["公司决议"]),
    ("synthesis_裁判要旨精选_中_16_盈余分配", "盈余分配", ["盈余分配"]),
    ("synthesis_裁判要旨精选_中_17_损害公司利益责任", "损害公司利益责任", ["损害公司利益"]),
    ("synthesis_裁判要旨精选_中_18_人格混同损害债权人利益", "人格混同及损害债权人利益", ["人格混同"]),
    ("synthesis_裁判要旨精选_中_19_公司减资", "公司减资", ["公司减资"]),
    ("synthesis_裁判要旨精选_中_20_公司解散", "公司解散", ["公司解散"]),
]

def create_synthesis_file(topic_id, topic_name, cases, keywords):
    """Create synthesis file for a topic"""
    if not cases:
        return False

    # Build content
    case_list = []
    for i, case in enumerate(cases, 1):
        case_entry = f"""### {i}. {case['title']}

**案号**：{case['case_number']}

**合议庭**：{case['panel']}

**关键词**：{case['keywords']}

**相关法条**：{case['related_laws']}

**裁判要旨**：

{case['裁判要旨']}

**案情摘要**：

{case['案情摘要']}

**撰写人**：{case['author']}
"""
        case_list.append(case_entry)

    content = f"""---
title: 裁判要旨精选（中册）——{topic_name}
type: synthesis
created: 2026-04-22
updated: 2026-04-22
tags: [最高法裁判要旨, 民商事篇, {topic_name}]
source: [[《最高人民法院裁判要旨精选》中 最高法审管办 202504]]
related: [synthesis_裁判要旨精选_中_01_借款合同民间借贷]
---

# {topic_name}

本页面汇总最高法裁判要旨精选（中册）民商事篇中涉及**{topic_name}**的裁判要旨。

## 案例汇总

{"".join(case_list)}

## 相关主题

"""

    for other_id, other_name, _ in topics_config:
        if other_id != topic_id:
            content += f"- [[{other_id}]]\n"

    return content

# Process each topic
results = {}
for topic_id, topic_name, keywords in topics_config:
    matched_cases = []

    for idx in case_starts:
        case_text, _ = extract_full_case(idx)
        parsed = parse_case(case_text)

        title = parsed.get('title', '')
        case_keywords = parsed.get('keywords', '')

        # Match by keywords
        matched = False
        if keywords:
            for kw in keywords:
                if kw in title or kw in case_keywords:
                    matched = True
                    break
        else:
            # For 其他合同纠纷 - collect cases not matched by other topics
            # This is a catch-all, skip for now
            pass

        if matched:
            matched_cases.append(parsed)

    results[topic_id] = {
        'topic_name': topic_name,
        'cases': matched_cases,
        'count': len(matched_cases)
    }

# Print results
print("\n匹配结果：")
for topic_id, info in results.items():
    print(f"  {topic_id}: {info['count']} 个案例")

# Create synthesis files for topics with cases
created_files = []
for topic_id, info in results.items():
    if info['count'] > 0:
        keywords_for_topic = next(kw for tid, _, kw in topics_config if tid == topic_id)
        content = create_synthesis_file(topic_id, info['topic_name'], info['cases'], keywords_for_topic)

        output_file = os.path.join(output_dir, f"{topic_id}.md")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        created_files.append(output_file)
        print(f"Created: {output_file}")

print(f"\n共创建 {len(created_files)} 个文件")