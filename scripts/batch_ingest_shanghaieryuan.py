#!/usr/bin/env python3
"""
Batch ingest 上海二中院-至正法官札记 to wiki/summaries/
"""
import re
import os
from pathlib import Path

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/上海二中院/上海二中院-至正法官札记-md")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/summaries")
TARGET_DIR.mkdir(parents=True, exist_ok=True)

# Get all source files
source_files = sorted(SOURCE_DIR.glob("*.md"))
print(f"Found {len(source_files)} source files")

def extract_title(content):
    """Extract title from first # heading"""
    match = re.search(r'^#\s+(.+?)\s*[|]', content, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        # Remove trailing spaces and special chars
        title = re.sub(r'\s+', ' ', title)
        return title
    # Fallback: just get first # line content
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "未命名"

def extract_date_from_filename(filename):
    """Extract date from filename like [2021-04-19]xxx.md"""
    match = re.search(r'\[(\d{4}-\d{2}-\d{2})\]', filename)
    if match:
        return match.group(1).replace('-', '')
    return "20260511"

def extract_key_points(content, min_points=5):
    """Extract at least 5 key points from content"""
    points = []

    # Look for bold text (key statements)
    bold_patterns = re.findall(r'\*\*([^*]+)\*\*', content)
    for bp in bold_patterns:
        bp = bp.strip()
        if len(bp) > 10 and bp not in points:
            points.append(bp)
        if len(points) >= min_points:
            break

    # If not enough, extract sentences with key legal/civil terms
    if len(points) < min_points:
        sentences = re.split(r'[。\n]', content)
        key_terms = ['法院', '认定', '规定', '应当', '责任', '权利', '义务', '合同', '争议', '判决']
        for s in sentences:
            s = s.strip()
            if len(s) > 20 and any(term in s for term in key_terms):
                # Clean up markdown
                s = re.sub(r'\*+', '', s)
                if s not in points:
                    points.append(s)
            if len(points) >= min_points:
                break

    return points[:min_points] if len(points) >= min_points else points

def extract_tags(content, title):
    """Extract relevant tags from content"""
    tags = []
    content_lower = content.lower()
    title_lower = title.lower()

    # Category keywords
    if any(kw in content_lower for kw in ['劳动合同', '劳动争议', '劳务协议', '用人单位', '劳动者', '工资', '社保']):
        tags.append('劳动争议')
    if any(kw in content_lower for kw in ['房屋', '房产', '买房', '借名', '租赁', '承租人', '产权']):
        tags.append('房产纠纷')
    if any(kw in content_lower for kw in ['合同', '违约', '解除', '变更']):
        tags.append('合同纠纷')
    if any(kw in content_lower for kw in ['离婚', '抚养', '继承', '婚姻', '夫妻']):
        tags.append('婚姻家庭')
    if any(kw in content_lower for kw in ['侵权', '损害', '赔偿']):
        tags.append('侵权责任')
    if any(kw in content_lower for kw in ['刑事', '犯罪', '盗窃', '抢劫', '诈骗']):
        tags.append('刑事案件')
    if any(kw in content_lower for kw in ['公司', '股东', '股权', '解散']):
        tags.append('公司纠纷')
    if any(kw in content_lower for kw in ['借贷', '借款', '民间借贷', '利率']):
        tags.append('借贷纠纷')

    # Default tag
    if not tags:
        tags.append('民事案件')

    # Add legal analysis tag
    tags.append('法官札记')

    return tags[:4]  # Limit to 4 tags

def create_summary_file(source_file):
    """Process a single source file and create summary"""
    content = source_file.read_text(encoding='utf-8')

    filename = source_file.name
    title = extract_title(content)
    date_str = extract_date_from_filename(filename)
    key_points = extract_key_points(content)
    tags = extract_tags(content, title)

    # Build frontmatter
    frontmatter = f"""---
title: {title}
type: summary
created: 2026-05-11
updated: 2026-05-11
tags: {tags}
source: [[{filename}]]
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{filename}]] |
| 类型 | 法官札记 |
| 发布日期 | {date_str[:4]}-{date_str[4:6]}-{date_str[6:8]} |
| 关键词 | {' / '.join(tags)} |
| 核心要点 | {len(key_points)}条（详见正文） |

## ❓ 关键问题

"""

    # Add key points section
    for i, point in enumerate(key_points, 1):
        # Truncate very long points
        if len(point) > 200:
            point = point[:200] + '...'
        frontmatter += f"{i}. {point}\n"

    # Add main content - extract main body (remove header, end markers)
    main_content = content

    # Remove the # title line
    main_content = re.sub(r'^#\s+.+\|?\s*至正.*$', '', main_content, flags=re.MULTILINE)

    # Remove author info lines
    main_content = re.sub(r'^\*{0,2}本\s*期\s*主\s*笔.*$', '', main_content, flags=re.MULTILINE)
    main_content = re.sub(r'^[^\n]*全日制.*法学.*$', '', main_content, flags=re.MULTILINE)
    main_content = re.sub(r'^[^\n]*华东.*大学.*$', '', main_content, flags=re.MULTILINE)
    main_content = re.sub(r'^[^\n]*复旦大学.*$', '', main_content, flags=re.MULTILINE)

    # Remove END marker and after
    end_idx = main_content.find('**END**')
    if end_idx != -1:
        main_content = main_content[:end_idx]

    # Remove责任编辑, 人像摄影 etc
    main_content = re.sub(r'\*\*责任编辑.*$\n?', '', main_content, flags=re.MULTILINE)
    main_content = re.sub(r'人像摄影.*$\n?', '', main_content, flags=re.MULTILINE)
    main_content = re.sub(r'版面编辑.*$\n?', '', main_content, flags=re.MULTILINE)
    main_content = re.sub(r'预览时标签不可点.*$\n?', '', main_content, flags=re.MULTILINE)
    main_content = re.sub(r'__+$', '', main_content)
    main_content = re.sub(r'\[.*?\]\(https?://.*?\)', '', main_content)  # Remove URLs
    main_content = re.sub(r'更多风采.*$', '', main_content, flags=re.MULTILINE)
    main_content = re.sub(r'更多作品链接.*$', '', main_content, flags=re.MULTILINE)
    main_content = re.sub(r'-\s*$', '', main_content, flags=re.MULTILINE)

    # Clean up excessive newlines
    main_content = re.sub(r'\n{3,}', '\n\n', main_content)
    main_content = main_content.strip()

    # Only add main content if it's substantive
    full_content = frontmatter + "\n\n## 正文\n\n" + main_content if len(main_content) > 100 else frontmatter

    # Create target filename
    # Extract clean title for filename
    clean_title = re.sub(r'[（(].*?[）)]', '', title)  # Remove parenthetical content
    clean_title = re.sub(r'[^一-龥a-zA-Z0-9]', '', clean_title)  # Keep only Chinese, letters, numbers
    clean_title = clean_title[:30]  # Limit length

    target_filename = f"summary_{date_str}_上海二中院_至正法官札记_{clean_title}.md"
    target_path = TARGET_DIR / target_filename

    # Handle duplicates
    if target_path.exists():
        counter = 1
        while target_path.exists():
            target_filename = f"summary_{date_str}_上海二中院_至正法官札记_{clean_title}_{counter}.md"
            target_path = TARGET_DIR / target_filename
            counter += 1

    target_path.write_text(full_content, encoding='utf-8')
    return target_filename, title

# Process all files
success_count = 0
failed_files = []

for i, source_file in enumerate(source_files, 1):
    try:
        target_name, title = create_summary_file(source_file)
        success_count += 1
        if i % 20 == 0 or i == len(source_files):
            print(f"Processed {i}/{len(source_files)}: {target_name}")
    except Exception as e:
        failed_files.append((source_file.name, str(e)))
        print(f"ERROR processing {source_file.name}: {e}")

print(f"\n=== Summary ===")
print(f"Total: {len(source_files)}")
print(f"Success: {success_count}")
print(f"Failed: {len(failed_files)}")
if failed_files:
    print("Failed files:")
    for fn, err in failed_files:
        print(f"  - {fn}: {err}")