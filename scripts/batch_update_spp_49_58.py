#!/usr/bin/env python3
"""Batch update SPP GuideCase wiki pages (cases 195-237) from source files."""

import re
import os

BASE = "D:/AI agent/tkk-library"
SRC_DIR = f"{BASE}/sources/2-案例库/最高检-指导性案例"
WIKI_DIR = f"{BASE}/wiki/syntheses"

# Source file -> case numbers mapping
SOURCE_CASES = {
    "49 关于印发最高人民检察院第四十九批指导性案例的通知.md": [195, 196, 197, 198, 199],
    "50 关于印发最高人民检察院第五十批指导性案例的通知.md": [201, 203, 204],
    "51 关于印发最高人民检察院第五十一批指导性案例的通知.md": [205, 206, 207, 208],
    "52 关于印发最高人民检察院第五十二批指导性案例的通知.md": [209, 210, 211, 212],
    "53 关于印发最高人民检察院第五十三批指导性案例的通知.md": [213, 214, 215, 216, 217],
    "55 关于印发最高人民检察院第五十五批指导性案例的通知.md": [219, 220, 221, 222],
    "56 关于印发最高人民检察院第五十六批指导性案例的通知.md": [223, 224, 225, 226, 227],
    "57 关于印发最高人民检察院第五十七批指导性案例的通知.md": [228, 229, 230, 231, 232],
    "58 关于印发最高人民检察院第五十八批指导性案例的通知.md": [233, 234, 235, 236, 237],
}

BATCH_NUMS = {
    "49": 49, "50": 50, "51": 51, "52": 52, "53": 53,
    "55": 55, "56": 56, "57": 57, "58": 58,
}


def split_cases(text):
    """Split source text into individual case blocks."""
    # Find all case markers
    case_pattern = r'（检例第(\d+)号）'
    matches = list(re.finditer(case_pattern, text))

    cases = {}
    for i, m in enumerate(matches):
        case_num = int(m.group(1))
        start = m.start()

        # Find the case name (look backwards for non-empty, non-section lines)
        lines_before = text[:start].split('\n')
        name_parts = []
        for j in range(len(lines_before) - 1, max(len(lines_before) - 5, -1), -1):
            line = lines_before[j].strip()
            if line and not line.startswith('【') and not line.startswith('（检例'):
                name_parts.insert(0, line)
            elif line.startswith('（检例'):
                break

        case_name = ' '.join(name_parts).strip().replace('**', '')

        # Find the end of this case (start of next case's name or end of text)
        if i + 1 < len(matches):
            # Look for the next case title line (the line before the next case number)
            next_start = matches[i + 1].start()
            # Find the line that contains the next case's title
            text_between = text[m.end():next_start]
            # The end is where the next case title begins
            # Look for a line that looks like a case title (Chinese text + "案")
            title_pattern = r'\n([一-鿿][一-鿿\s]{2,40}案)\s*\n\n（检例第'
            title_match = re.search(title_pattern, text[m.end():])
            if title_match:
                end = m.end() + title_match.start()
            else:
                end = next_start
        else:
            end = len(text)

        cases[case_num] = {
            'name': case_name,
            'text': text[start:end]
        }

    return cases


def extract_sections(case_text):
    """Extract sections from a case text block."""
    sections = {}

    # Extract 【关键词】
    kw_match = re.search(r'【关键词】\s*\n(.*?)(?=\n【|$)', case_text, re.DOTALL)
    if kw_match:
        sections['keywords'] = kw_match.group(1).strip()

    # Extract 【要旨】
    zy_match = re.search(r'【要旨】\s*\n(.*?)(?=\n【|$)', case_text, re.DOTALL)
    if zy_match:
        sections['summary'] = zy_match.group(1).strip()

    # Extract 【相关立法】 or 【相关规定】
    law_match = re.search(r'【相关(?:立法|规定)】\s*\n(.*?)(?=\n办案检察院|\n案例撰稿|\n承办检察官|\n\n[一-鿿]|$)', case_text, re.DOTALL)
    if law_match:
        sections['law'] = law_match.group(1).strip()

    # Extract 【基本案情】
    aq_match = re.search(r'【基本案情】\s*\n(.*?)(?=\n【|$)', case_text, re.DOTALL)
    if aq_match:
        sections['facts'] = aq_match.group(1).strip()

    # Extract 【诉讼过程】 or 【检察机关履职过程】
    proc_match = re.search(r'【(?:诉讼过程|检察机关履职过程)】\s*\n(.*?)(?=\n【|$)', case_text, re.DOTALL)
    if proc_match:
        sections['process'] = proc_match.group(1).strip()

    return sections


def get_existing_created(wiki_path):
    """Get the existing created date from wiki page."""
    if not os.path.exists(wiki_path):
        return "2026-05-11"
    with open(wiki_path, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'created:\s*(\d{4}-\d{2}-\d{2})', content)
    if match:
        return match.group(1)
    return "2026-05-11"


def build_wiki_page(case_num, case_name, sections, batch_num, src_filename, created_date):
    """Build the wiki page content."""
    case_name = case_name.replace('**', '').strip()

    # Determine related concepts
    related = []
    keywords = sections.get('keywords', '')
    summary = sections.get('summary', '')

    crime_keywords = {
        '假释': 'concept_假释制度',
        '盗窃': 'concept_盗窃罪',
        '诈骗': 'concept_诈骗罪',
        '虚假诉讼': 'concept_虚假诉讼罪',
        '掩饰、隐瞒犯罪所得': 'concept_掩饰、隐瞒犯罪所得罪',
        '组织卖淫': 'concept_组织卖淫罪',
        '工伤': 'concept_工伤保险条例',
        '宅基地': 'concept_宅基地使用权',
        '烈士': 'concept_烈士褒扬条例',
        '欺诈发行债券': 'concept_欺诈发行证券罪',
        '违规披露': 'concept_违规披露、不披露重要信息罪',
        '内幕交易': 'concept_内幕交易、泄露内幕信息罪',
        '操纵证券市场': 'concept_操纵证券市场罪',
        '故意损毁文物': 'concept_故意损毁文物罪',
        '拒不执行判决': 'concept_拒不执行判决、裁定罪',
        '故意伤害': 'concept_故意伤害罪',
        '猥亵': 'concept_猥亵儿童罪',
        '强奸': 'concept_强奸罪',
        '敲诈勒索': 'concept_敲诈勒索罪',
        '淫秽物品': 'concept_制作、贩卖、传播淫秽物品牟利罪',
        '帮助信息网络犯罪': 'concept_帮助信息网络犯罪活动罪',
        '侵犯公民个人信息': 'concept_侵犯公民个人信息罪',
        '容留卖淫': 'concept_容留卖淫罪',
        '行政公益诉讼': 'concept_行政公益诉讼',
        '民事公益诉讼': 'concept_民事公益诉讼',
        '文物保护': 'concept_文物保护法',
        '民间借贷': 'concept_民间借贷',
        '赠与': 'concept_赠与合同',
        '交通事故': 'concept_机动车交通事故责任',
        '医疗美容': 'concept_消费者权益保护法',
        '行政奖励': 'concept_行政奖励',
        '山林权属': 'concept_山林权属争议',
        '安全生产': 'concept_安全生产法',
        '职业病': 'concept_职业病防治法',
        '村民委员会': 'concept_村民委员会',
    }

    for kw, concept in crime_keywords.items():
        if kw in keywords or kw in summary:
            if concept not in related:
                related.append(concept)

    related_yaml = ""
    if related:
        related_yaml = "\n".join(f"  - [[{r}]]" for r in related[:3])
    else:
        related_yaml = "  - []"

    # Build tags
    tags = [f"检例第{case_num}号"]
    if case_name:
        name_parts = re.findall(r'[一-鿿]+', case_name)
        for part in name_parts[:3]:
            if len(part) >= 2:
                tags.append(part)

    tags_str = ", ".join(tags)

    page = f"""---
title: {case_name}
type: synthesis
created: {created_date}
updated: 2026-05-27
tags: [指导性案例, 最高人民检察院, {tags_str}]
source: "sources/2-案例库/最高检-指导性案例/{src_filename}"
related:
{related_yaml}
案例分级: ⭐⭐⭐⭐⭐
问题意识: {case_name}的法律要旨与实践意义
---

## 📋 案例信息

| 字段 | 内容 |
|------|------|
| 案例编号 | 检例第{case_num}号 |
| 案例名称 | {case_name} |
| 发布机关 | 最高人民检察院 |
| 发布批次 | 第{batch_num}批 |
| 关键词 | {sections.get('keywords', '（未在原文中标注）')} |

## 要旨

{sections.get('summary', '（未在原文中标注）')}

## 相关立法

{sections.get('law', '（未在原文中标注）')}

## 基本案情

{sections.get('facts', '（未在原文中标注）')}

## 诉讼过程

{sections.get('process', '（未在原文中标注）')}
"""
    return page


def main():
    updated = 0
    errors = []

    for src_filename, case_nums in SOURCE_CASES.items():
        src_path = os.path.join(SRC_DIR, src_filename)
        if not os.path.exists(src_path):
            errors.append(f"Source file not found: {src_path}")
            continue

        with open(src_path, 'r', encoding='utf-8') as f:
            text = f.read()

        batch_key = src_filename.split(' ')[0]
        batch_num = BATCH_NUMS.get(batch_key, 0)

        # Split into individual cases
        cases = split_cases(text)

        for case_num in case_nums:
            if case_num not in cases:
                errors.append(f"Case {case_num} not found in {src_filename}")
                continue

            case_data = cases[case_num]
            sections = extract_sections(case_data['text'])

            wiki_path = os.path.join(WIKI_DIR, f"SPP_GuideCase_检例第{case_num}号.md")
            created_date = get_existing_created(wiki_path)

            page_content = build_wiki_page(
                case_num, case_data['name'], sections, batch_num, src_filename, created_date
            )

            with open(wiki_path, 'w', encoding='utf-8') as f:
                f.write(page_content)

            updated += 1
            print(f"Updated: SPP_GuideCase_检例第{case_num}号.md ({case_data['name']})")

    print(f"\n=== Summary ===")
    print(f"Updated: {updated} files")
    if errors:
        print(f"Errors: {len(errors)}")
        for e in errors:
            print(f"  - {e}")


if __name__ == "__main__":
    main()
