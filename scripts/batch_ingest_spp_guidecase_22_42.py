#!/usr/bin/env python3
"""Batch ingest SPP Guide Cases batches 23-42 (检例第85号-第170号)."""

import re
from pathlib import Path

VAULT = Path(r"D:\AI agent\tkk-library")
SOURCE_DIR = VAULT / "sources" / "2-案例库" / "最高检-指导性案例"
WIKI_DIR = VAULT / "wiki" / "syntheses"

SOURCE_FILES = [
    "23第二十三批指导性案例-中华人民共和国最高人民检察院.md",
    "24最高检发布4件涉非公经济立案监督指导性案例-中华人民共和国最高人民检察.md",
    "25第二十五批指导性案例-中华人民共和国最高人民检察院.md",
    "26第二十六批指导性案例-中华人民共和国最高人民检察院.md",
    "27第二十七批指导性案例-中华人民共和国最高人民检察院.md",
    "28第二十八批指导性案例-中华人民共和国最高人民检察院.md",
    "29第二十九批指导性案例-中华人民共和国最高人民检察院.md",
    "30第三十批指导性案例-中华人民共和国最高人民检察院.md",
    "31第三十一批指导性案例-中华人民共和国最高人民检察院.md",
    "32第三十二批指导性案例-中华人民共和国最高人民检察院.md",
    "33第三十三批指导性案例-中华人民共和国最高人民检察院.md",
    "34第三十四批指导性案例-中华人民共和国最高人民检察院.md",
    "35第三十五批指导性案例-中华人民共和国最高人民检察院.md",
    "36第三十六批指导性案例-中华人民共和国最高人民检察院.md",
    "37 关于印发最高人民检察院第三十七批指导性案例的通知.md",
    "38 关于印发最高人民检察院第三十八批指导性案例的通知.md",
    "39 关于印发最高人民检察院第三十九批指导性案例的通知.md",
    "40 关于印发最高人民检察院第四十批指导性案例的通知.md",
    "41 关于印发最高人民检察院第四十一批指导性案例的通知.md",
    "42 最高检第四十二批指导性案例.md",
]

BATCH_NUMBERS = {
    "23": "第二十三批", "24": "第二十四批", "25": "第二十五批",
    "26": "第二十六批", "27": "第二十七批", "28": "第二十八批",
    "29": "第二十九批", "30": "第三十批", "31": "第三十一批",
    "32": "第三十二批", "33": "第三十三批", "34": "第三十四批",
    "35": "第三十五批", "36": "第三十六批", "37": "第三十七批",
    "38": "第三十八批", "39": "第三十九批", "40": "第四十批",
    "41": "第四十一批", "42": "第四十二批",
}


def get_batch_num(filename):
    m = re.match(r'(\d+)', filename)
    return m.group(1) if m else None


def strip_frontmatter(text):
    if text.startswith('---'):
        end = text.find('---', 3)
        if end != -1:
            return text[end+3:].strip()
    return text.strip()


def is_standalone_case_marker(line):
    """Check if a line is a standalone case marker like （检例第X号） on its own line.
    Returns False for markers embedded in longer text (notification headers)."""
    stripped = line.strip()
    return bool(re.match(r'^（检例第\d+号）$', stripped))


def is_batch_header(line):
    """Check if a line is a batch-level header (not a case title)."""
    if '关于印发' in line:
        return True
    if '批指导性案例' in line:
        return True
    # "最高人民检察院" followed by batch info patterns
    if line.startswith('最高人民检察院') and ('发布' in line or '批' in line or '印发' in line):
        return True
    return False


def extract_cases(text, batch_num):
    """Extract individual cases by finding standalone （检例第X号） markers."""
    body = strip_frontmatter(text)
    lines = body.split('\n')

    # Find STANDALONE case markers (the actual case entries, not notification references)
    case_markers = []
    for i, line in enumerate(lines):
        if is_standalone_case_marker(line):
            m = re.search(r'检例第(\d+)号', line)
            if m:
                case_markers.append((i, int(m.group(1))))

    if not case_markers:
        return []

    cases = []
    for idx, (line_idx, case_num) in enumerate(case_markers):
        # Title: look backwards from the marker line
        title = ''
        for j in range(line_idx - 1, max(line_idx - 5, -1), -1):
            candidate = lines[j].strip().strip('#').strip()
            if candidate and not candidate.startswith('---') and not candidate.startswith('>'):
                if is_batch_header(candidate):
                    continue
                title = candidate
                break

        if not title:
            title = f"检例第{case_num}号"

        # Content: from after the marker line to the next marker
        next_line_idx = case_markers[idx + 1][0] if idx + 1 < len(case_markers) else len(lines)

        content_start = line_idx + 1

        # End: exclude the next case's title line(s)
        content_end = next_line_idx
        if idx + 1 < len(case_markers):
            next_marker_line = case_markers[idx + 1][0]
            for j in range(next_marker_line - 1, max(next_marker_line - 5, -1), -1):
                candidate = lines[j].strip()
                if candidate and not candidate.startswith('---') and not candidate.startswith('>'):
                    if not is_batch_header(candidate):
                        content_end = j
                        break

        content_lines = lines[content_start:content_end]
        content_text = '\n'.join(content_lines).strip()

        # Extract 【...】 sections
        sections = {}
        section_pattern = re.compile(r'【(.*?)】\s*\n([\s\S]*?)(?=【[^】]*】\s*\n|$)')
        for sm in section_pattern.finditer(content_text):
            sec_name = sm.group(1).strip()
            sec_content = sm.group(2).strip()
            sections[sec_name] = sec_content

        keywords = sections.get('关键词', '').strip()
        zhiyao = sections.get('要旨', '').strip()
        anqing = sections.get('基本案情', '').strip()
        lvguo = sections.get('检察机关履职过程', '').strip() or sections.get('诉讼过程', '').strip()
        zhidao = sections.get('指导意义', '').strip() or sections.get('裁判要旨', '').strip()
        guiding = sections.get('相关规定', '').strip()

        cases.append({
            'num': case_num,
            'title': title,
            'batch': BATCH_NUMBERS.get(batch_num, f"第{batch_num}批"),
            'keywords': keywords,
            'zhiyao': zhiyao,
            'anqing': anqing,
            'lvguo': lvguo,
            'zhidao': zhidao,
            'guiding': guiding,
        })

    return cases


def guess_crime_tags(keywords, title, zhiyao):
    tags = []
    crime_keywords = [
        '串通投标', '行贿', '受贿', '贪污', '挪用公款', '诈骗', '合同诈骗',
        '非法吸收公众存款', '集资诈骗', '假冒注册商标', '污染环境',
        '走私', '贩毒', '贩卖毒品', '故意杀人', '故意伤害', '抢劫',
        '盗窃', '强奸', '绑架', '放火', '爆炸', '交通肇事',
        '危险驾驶', '妨害公务', '拒不执行', '非法经营',
        '生产销售伪劣产品', '伪劣产品', '假冒', '侵权',
        '民事公益诉讼', '行政公益诉讼', '刑事附带民事公益诉讼',
        '立案监督', '不起诉', '抗诉', '再审', '执行监督',
        '涉黑', '涉恶', '黑社会', '组织领导参加',
        '未成年人', '家暴', '正当防卫', '防卫过当',
        '知识产权', '著作权', '专利', '商业秘密',
        '网络犯罪', '电信诈骗', '帮信', '侵犯公民个人信息',
        '公益诉讼', '生态环境', '食品药品安全',
        '安全生产', '重大责任事故', '渎职', '滥用职权', '玩忽职守',
        '强制猥亵', '猥亵儿童', '拐卖', '收买',
        '非公经济', '民营企业', '企业合规',
        '仲裁', '仲裁枉法', '枉法仲裁',
        '证券', '内幕交易', '操纵市场',
        '走私废物', '走私普通货物',
        '虚假诉讼', '违法所得没收', '巨额财产来源不明',
        '强制医疗', '社区矫正', '减刑假释',
        '行政检察', '行政违法行为监督',
        '刑事申诉', '国家赔偿',
        '数据安全', '个人信息',
        '催收非法债务', '高利贷',
        '袭警', '袭警罪',
        '饮用水', '万峰湖', '公益损害', '流域治理',
        '安全生产', '重大责任事故',
    ]

    full_text = f"{keywords} {title} {zhiyao}"
    for kw in crime_keywords:
        if kw in full_text:
            tags.append(kw)

    return tags[:5] if tags else ['指导性案例']


def build_wiki_content(case, source_filename):
    crime_tags = guess_crime_tags(case['keywords'], case['title'], case['zhiyao'])
    all_tags = crime_tags + ['最高检', '指导性案例', f"检例第{case['num']}号"]
    seen = set()
    unique_tags = []
    for t in all_tags:
        if t not in seen:
            seen.add(t)
            unique_tags.append(t)

    tags_str = ', '.join(unique_tags)

    related_lines = []
    for tag in crime_tags:
        if tag not in ('指导性案例', '最高检', '不起诉', '立案监督', '抗诉', '再审', '执行监督',
                        '民事公益诉讼', '行政公益诉讼', '刑事附带民事公益诉讼'):
            related_lines.append(f"  - [[concept_{tag}]]")

    related_section = '\n'.join(related_lines) if related_lines else '  -'

    content = f"""---
title: {case['title']}
type: synthesis
created: 2026-05-09
updated: 2026-05-27
tags: [{tags_str}]
source: "[[{source_filename}]]"
related:
{related_section}
---

## 📋 案例信息

| 字段 | 内容 |
|------|------|
| 案例编号 | 检例第{case['num']}号 |
| 案例名称 | {case['title']} |
| 发布机关 | 最高人民检察院 |
| 发布批次 | {case['batch']} |
| 关键词 | {case['keywords']} |

## 要旨

{case['zhiyao']}

## 相关立法

{case['guiding'] if case['guiding'] else '（详见原文）'}

## 基本案情

{case['anqing']}

## 诉讼过程

{case['lvguo']}

## 指导意义

{case['zhidao']}

## 关键词

{case['keywords']}
"""
    return content


def main():
    processed = 0
    errors = []
    seen_nums = set()

    for src_file in SOURCE_FILES:
        src_path = SOURCE_DIR / src_file
        if not src_path.exists():
            print(f"SKIP (not found): {src_file}")
            continue

        batch_num = get_batch_num(src_file)
        print(f"\n=== Processing batch {batch_num}: {src_file} ===")

        text = src_path.read_text(encoding='utf-8')
        cases = extract_cases(text, batch_num)
        print(f"  Found {len(cases)} cases: {[c['num'] for c in cases]}")

        for case in cases:
            if case['num'] in seen_nums:
                print(f"  SKIP (duplicate): 检例第{case['num']}号")
                continue
            seen_nums.add(case['num'])

            wiki_file = WIKI_DIR / f"SPP_GuideCase_检例第{case['num']}号.md"
            wiki_content = build_wiki_content(case, src_file)

            try:
                wiki_file.write_text(wiki_content, encoding='utf-8')
                print(f"  Wrote: 检例第{case['num']}号 - {case['title'][:40]}")
                processed += 1
            except Exception as e:
                err = f"Error writing 检例第{case['num']}号: {e}"
                print(f"  ERROR: {err}")
                errors.append(err)

    print(f"\n=== Summary ===")
    print(f"Processed: {processed} unique cases")
    if seen_nums:
        print(f"Case range: {min(seen_nums)}-{max(seen_nums)}")
    if errors:
        print(f"Errors: {len(errors)}")
        for e in errors:
            print(f"  - {e}")


if __name__ == '__main__':
    main()
