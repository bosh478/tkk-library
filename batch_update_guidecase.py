#!/usr/bin/env python3
"""Batch update SPP_GuideCase_ files to NotebookLM style format."""

import re
import os
from pathlib import Path

def extract_date_from_filename(filename):
    """Extract date from filename pattern like [2022-06-24] or return None."""
    match = re.search(r'\[(\d{4}-\d{2}-\d{2})\]', filename)
    if match:
        return match.group(1)
    return None

def process_file(filepath):
    """Process a single file and return updated content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse frontmatter
    if not content.startswith('---'):
        return None, "No frontmatter found"

    frontmatter_end = content.find('\n---\n', 4)
    if frontmatter_end == -1:
        return None, "Frontmatter not properly closed"

    frontmatter_text = content[3:frontmatter_end]
    body = content[frontmatter_end + 4:]

    # Parse existing frontmatter fields
    lines = frontmatter_text.split('\n')
    fm = {}
    for line in lines:
        if ':' in line:
            key = line.split(':', 1)[0].strip()
            value = line.split(':', 1)[1].strip()
            fm[key] = value

    # Extract fields
    title = fm.get('title', '最高人民检察院指导性案例')
    source = fm.get('source', '')
    tags_raw = fm.get('tags', '')
    category = fm.get('category', '刑事')

    # Parse tags
    tags_match = re.search(r'\[(.+?)\]', tags_raw)
    if tags_match:
        tags = [t.strip() for t in tags_match.group(1).split(',')]
    else:
        tags = ['最高检', '指导性案例']

    # Get date from frontmatter or filename
    published = fm.get('published', '')
    if not published:
        published = extract_date_from_filename(os.path.basename(filepath))
    if not published:
        published = '2026-04-27'

    # Extract keywords from 【关键词】 sections
    keywords = []
    keyword_matches = re.findall(r'\*\*【关键词】\s*\*\*?\s*([^\n]+)', body)
    for km in keyword_matches:
        cleaned = re.sub(r'[\*]+', '', km).strip()
        if cleaned:
            keywords.append(cleaned)
    if not keywords:
        keywords = ['指导性案例']

    # Limit to 3-5 keywords
    keywords = keywords[:5]

    # Extract core points from 【要旨】 sections
    core_points = []
    yazi_matches = re.findall(r'\*\*【要旨】\s*\*\*(.+?)(?=\*\*【|\n## |\n相关链接|$)', body, re.DOTALL)
    for match in yazi_matches:
        text = match.strip()
        text = re.sub(r'\s+', ' ', text)
        if text and len(text) > 10:
            if len(text) > 150:
                text = text[:150] + "..."
            core_points.append(text)
        if len(core_points) >= 5:
            break

    if len(core_points) < 3:
        sentences = re.findall(r'[^。\n]{20,150}[。]', body)
        for sent in sentences[:10]:
            cleaned = sent.strip()
            if cleaned not in core_points and any(term in cleaned for term in ['犯罪', '认定', '判处', '检察', '违法']):
                core_points.append(cleaned)
                if len(core_points) >= 5:
                    break

    if not core_points:
        core_points = ["本批次指导性案例涉及重要法律适用问题"]

    core_points = core_points[:5]

    # Generate FAQ based on content
    faqs = []

    crime_map = {
        '贪污': '贪污罪', '受贿': '受贿罪', '挪用公款': '挪用公款罪',
        '毒品': '毒品犯罪', '公益诉讼': '公益诉讼', '聚众斗殴': '聚众斗殴罪',
        '绑架': '绑架罪', '金融': '金融领域职务犯罪', '环境监管': '环境监管失职罪',
        '虚假恐怖信息': '编造虚假恐怖信息罪', '洗钱': '洗钱罪'
    }
    crime_types = []
    for term, crime in crime_map.items():
        if term in body and crime not in crime_types:
            crime_types.append(crime)

    if crime_types:
        faqs.append({
            "q": "本批次指导性案例涉及哪些犯罪类型？",
            "a": f"本批次涉及{('、'.join(crime_types[:4]))}等罪名，为相关案件办理提供指导。"
        })

    if '立案' in body and '监督' in body:
        faqs.append({
            "q": "检察机关如何开展立案监督工作？",
            "a": "检察机关通过履行检察职责，发现立案监督线索，依法开展立案监督工作。"
        })

    if '执法' in body or '行政' in body:
        faqs.append({
            "q": "行政公益诉讼的适用条件是什么？",
            "a": "行政机关未依法履行职责致使公共利益受到侵害的，检察机关可以提起行政公益诉讼督促履职。"
        })

    if len(faqs) < 2:
        faqs.append({
            "q": "这批指导性案例有什么指导意义？",
            "a": "这批案例对办理相关类型案件具有参照适用效力，有助于统一执法司法标准。"
        })

    if len(faqs) < 3 and '民事' in body:
        faqs.append({
            "q": "民事公益诉讼的起诉条件是什么？",
            "a": "检察机关在履行公益诉讼职责中发现损害公共利益的行为，可以依法提起民事公益诉讼。"
        })

    faqs = faqs[:3]

    # Find first ## heading in body to skip old intro section
    first_section_match = re.search(r'\n## ', body)
    if first_section_match:
        # Skip past first ## heading (including any content before it if it's just a title)
        body_start = first_section_match.start()
        rest_of_body = body[body_start:]
    else:
        rest_of_body = body

    # Build new content
    new_content = f"""---
title: {title}
type: summary
created: {fm.get('created', '2026-04-15')}
updated: 2026-04-27
tags: [{', '.join(tags)}]
category: {category}
source: {source}
published: {published}
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | {source} |
| 类型 | 指导性案例 |
| 发布日期 | {published} |
| 关键词 | {' / '.join(keywords)} |
| 核心要点 | {len(core_points)}条要点摘要 |

## ❓ 常见问题

"""

    for faq in faqs:
        new_content += f"""> **问：{faq['q']}**
> 答：{faq['a']}

"""

    new_content += rest_of_body

    return new_content, None

def main():
    base_dir = Path("D:/AI agent/tkk-library/wiki/summaries")

    files = list(base_dir.glob("SPP_GuideCase_*.md"))
    print(f"Found {len(files)} files to process")

    success_count = 0
    error_count = 0
    errors = []

    for filepath in sorted(files):
        try:
            new_content, error = process_file(filepath)
            if error:
                errors.append(f"{filepath.name}: {error}")
                error_count += 1
                continue

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

            success_count += 1
            print(f"Updated: {filepath.name}")
        except Exception as e:
            errors.append(f"{filepath.name}: {str(e)}")
            error_count += 1

    print(f"\nSummary: {success_count} success, {error_count} failed")
    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"  - {e}")

if __name__ == "__main__":
    main()
