#!/usr/bin/env python3
"""Fix corrupted SPP_GuideCase_ files by removing duplicate sections."""

import re
import os
from pathlib import Path

def fix_file(filepath):
    """Fix file with duplicate sections."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if file has the corruption pattern (## 📋 appearing twice)
    overview_count = content.count('## 📋 文档概览')
    faq_count = content.count('## ❓ 常见问题')

    if overview_count < 2 and faq_count < 2:
        print(f"File OK, skipping: {filepath.name}")
        return True  # Already fixed or wasn't corrupted

    print(f"Fixing corrupted file: {filepath.name}")

    # Find the position of first occurrence of our new content
    first_overview = content.find('## 📋 文档概览')
    last_overview = content.rfind('## 📋 文档概览')

    # Find position where original body starts (after our duplicate section)
    # Look for the original "## 关键要点" which should come after all our sections
    key_points_match = re.search(r'\n## 关键要点', content)
    if not key_points_match:
        print(f"  Could not find ## 关键要点 marker")
        return False

    # The content we want to keep starts from the second ## 关键要点 occurrence
    # But our new content was prepended and then duplicated
    # We need to:
    # 1. Take everything from first ## 关键要点 onwards as the real body
    # 2. Build new clean file with proper header + body

    key_points_pos = key_points_match.start()
    body_content = content[key_points_pos:]

    # Now extract frontmatter
    if not content.startswith('---'):
        print(f"  No frontmatter found")
        return False

    frontmatter_end = content.find('\n---\n', 4)
    if frontmatter_end == -1:
        print(f"  Frontmatter not properly closed")
        return False

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

    title = fm.get('title', '最高人民检察院指导性案例')
    source = fm.get('source', '')
    tags_raw = fm.get('tags', '')
    category = fm.get('category', '刑事')

    tags_match = re.search(r'\[(.+?)\]', tags_raw)
    if tags_match:
        tags = [t.strip() for t in tags_match.group(1).split(',')]
    else:
        tags = ['最高检', '指导性案例']

    published = fm.get('published', '')
    if not published:
        published = '2026-04-27'

    # Extract keywords from body
    keywords = []
    keyword_matches = re.findall(r'\*\*【关键词】\s*\*\*?\s*([^\n]+)', body_content)
    for km in keyword_matches:
        cleaned = re.sub(r'[\*]+', '', km).strip()
        if cleaned:
            keywords.append(cleaned)
    if not keywords:
        keywords = ['指导性案例']
    keywords = keywords[:5]

    # Extract core points from 【要旨】 sections
    core_points = []
    yazi_matches = re.findall(r'\*\*【要旨】\s*\*\*(.+?)(?=\*\*【|\n## |\n相关链接|$)', body_content, re.DOTALL)
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
        sentences = re.findall(r'[^。\n]{20,150}[。]', body_content)
        for sent in sentences[:10]:
            cleaned = sent.strip()
            if cleaned not in core_points and any(term in cleaned for term in ['犯罪', '认定', '判处', '检察', '违法']):
                core_points.append(cleaned)
                if len(core_points) >= 5:
                    break

    if not core_points:
        core_points = ["本批次指导性案例涉及重要法律适用问题"]
    core_points = core_points[:5]

    # Generate FAQ
    faqs = []
    crime_map = {
        '贪污': '贪污罪', '受贿': '受贿罪', '挪用公款': '挪用公款罪',
        '毒品': '毒品犯罪', '公益诉讼': '公益诉讼', '聚众斗殴': '聚众斗殴罪',
        '绑架': '绑架罪', '金融': '金融领域职务犯罪', '环境监管': '环境监管失职罪',
        '虚假恐怖信息': '编造虚假恐怖信息罪', '洗钱': '洗钱罪'
    }
    crime_types = []
    for term, crime in crime_map.items():
        if term in body_content and crime not in crime_types:
            crime_types.append(crime)

    if crime_types:
        faqs.append({
            "q": "本批次指导性案例涉及哪些犯罪类型？",
            "a": f"本批次涉及{('、'.join(crime_types[:4]))}等罪名，为相关案件办理提供指导。"
        })

    if '立案' in body_content and '监督' in body_content:
        faqs.append({
            "q": "检察机关如何开展立案监督工作？",
            "a": "检察机关通过履行检察职责，发现立案监督线索，依法开展立案监督工作。"
        })

    if '执法' in body_content or '行政' in body_content:
        faqs.append({
            "q": "行政公益诉讼的适用条件是什么？",
            "a": "行政机关未依法履行职责致使公共利益受到侵害的，检察机关可以提起行政公益诉讼督促履职。"
        })

    if len(faqs) < 2:
        faqs.append({
            "q": "这批指导性案例有什么指导意义？",
            "a": "这批案例对办理相关类型案件具有参照适用效力，有助于统一执法司法标准。"
        })

    if len(faqs) < 3 and '民事' in body_content:
        faqs.append({
            "q": "民事公益诉讼的起诉条件是什么？",
            "a": "检察机关在履行公益诉讼职责中发现损害公共利益的行为，可以依法提起民事公益诉讼。"
        })

    faqs = faqs[:3]

    # Build new clean content
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

    new_content += body_content

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  Fixed: {filepath.name}")
    return True

def main():
    base_dir = Path("D:/AI agent/tkk-library/wiki/summaries")

    files = list(base_dir.glob("SPP_GuideCase_*.md"))
    print(f"Found {len(files)} files to check")

    success_count = 0
    error_count = 0
    errors = []

    for filepath in sorted(files):
        try:
            if fix_file(filepath):
                success_count += 1
            else:
                error_count += 1
                errors.append(filepath.name)
        except Exception as e:
            errors.append(f"{filepath.name}: {str(e)}")
            error_count += 1

    print(f"\nSummary: {success_count} checked/fixed, {error_count} failed")
    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"  - {e}")

if __name__ == "__main__":
    main()
