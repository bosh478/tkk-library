"""
Batch ingest script for 最高检-指导性案例-md files.
Creates wiki summary pages in wiki/summaries/.
"""

import os
import re
from pathlib import Path

VAULT_ROOT = Path(r"D:\AI agent\tkk-library")
SOURCE_DIR = VAULT_ROOT / "sources" / "微信公号资料" / "最高人民检察院" / "最高检-指导性案例-md"
TARGET_DIR = VAULT_ROOT / "wiki" / "summaries"


def extract_date_from_filename(filename: str) -> str:
    """Extract date from [YYYY-MM-DD] pattern in filename."""
    m = re.search(r'\[(\d{4}-\d{2}-\d{2})\]', filename)
    if m:
        return m.group(1).replace('-', '')
    return ''


def extract_date_from_content(content: str) -> str:
    """Extract date from excerpt line (actual pub date) or frontmatter 'created' field."""
    # Try excerpt line first (actual publication date) like > ,2016-08-11
    m = re.search(r'>\s*,\s*(\d{4}-\d{2}-\d{2})', content)
    if m:
        return m.group(1).replace('-', '')
    # Try source URL for date like /201909/t20190925_
    m = re.search(r'source:.*?/(\d{4})(\d{2})/t\1\2(\d{2})_', content)
    if m:
        return f"{m.group(1)}{m.group(2)}{m.group(3)}"
    # Fallback to frontmatter created field
    m = re.search(r'created:\s*(\d{4}-\d{2}-\d{2})', content)
    if m:
        return m.group(1).replace('-', '')
    return ''


def extract_title(content: str, filename: str) -> str:
    """Extract title from first # line in content, or from filename."""
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('#'):
            title = line.lstrip('#').strip()
            # Remove common prefixes/suffixes
            title = title.replace('_中华人民共和国最高人民检察院', '')
            title = title.replace('-中华人民共和国最高人民检察院', '')
            title = re.sub(r'^\s*最高人民检察院\s*', '', title)
            if title and len(title) > 3:
                return title
    # Fallback: extract from filename
    name = Path(filename).stem
    # Remove number prefix like "01", "37"
    name = re.sub(r'^\d+', '', name)
    # Remove date bracket
    name = re.sub(r'\[\d{4}-\d{2}-\d{2}\]', '', name)
    # Remove suffix
    name = name.replace('-中华人民共和国最高人民检察院', '')
    name = name.replace('_中华人民共和国最高人民检察院', '')
    return name.strip()


def extract_keywords(content: str) -> list:
    """Extract keywords from 【关键词】 section."""
    m = re.search(r'【关键词】\s*(.*?)(?:\n\n|\*\*【)', content, re.DOTALL)
    if m:
        kw_text = m.group(1).strip()
        kw_text = re.sub(r'\*\*', '', kw_text)
        kw_text = re.sub(r'\s+', ' ', kw_text)
        return [k.strip() for k in kw_text.split() if k.strip()][:5]
    return []


def extract_key_points(content: str) -> str:
    """Extract key points from 【要旨】 sections."""
    points = []
    for m in re.finditer(r'【要旨】\s*(.*?)(?=\*\*【基本案情】|\*\*【|$)', content, re.DOTALL):
        point = m.group(1).strip()
        point = re.sub(r'\*\*', '', point)
        point = re.sub(r'\s+', ' ', point).strip()
        if point and len(point) > 10:
            points.append(point[:200])
        if len(points) >= 3:
            break
    return '；'.join(points) if points else ''


def extract_case_numbers(content: str) -> list:
    """Extract case numbers like 检例第X号."""
    return re.findall(r'检例第(\d+)号', content)


def summarize_content(content: str) -> str:
    """Generate a concise summary of the article."""
    # Try to get 要旨 first
    key_points = extract_key_points(content)
    if key_points:
        return key_points[:500]

    # Fallback: extract first meaningful paragraph after title
    lines = content.split('\n')
    summary_lines = []
    in_content = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            in_content = True
            continue
        if in_content and not line.startswith('---') and not line.startswith('>'):
            # Skip frontmatter-style lines
            if line.startswith('created:') or line.startswith('tags:') or line.startswith('source:'):
                continue
            clean = re.sub(r'\*\*', '', line)
            clean = re.sub(r'\s+', ' ', clean).strip()
            if len(clean) > 15:
                summary_lines.append(clean)
            if sum(len(s) for s in summary_lines) > 400:
                break

    return '。'.join(summary_lines)[:500] if summary_lines else ''


def sanitize_filename(name: str) -> str:
    """Remove or replace characters not allowed in filenames."""
    # Remove characters not allowed in Windows filenames
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\s+', '_', name)
    # Truncate if too long
    if len(name) > 80:
        name = name[:80]
    return name.strip('_')


def determine_category(content: str, title: str) -> str:
    """Determine the category based on content analysis."""
    # Most guiding cases are criminal
    criminal_keywords = ['刑事', '犯罪', '毒品', '绑架', '故意杀人', '抢劫', '诈骗',
                         '贪污', '受贿', '走私', '贩卖', '盗窃', '强奸', '猥亵',
                         '聚众斗殴', '交通肇事', '危险驾驶', '非法', '渎职',
                         '徇私舞弊', '抗诉', '不起诉', '逮捕', '起诉']
    civil_keywords = ['民事', '合同', '侵权', '婚姻', '继承', '劳动', '知识产权']
    admin_keywords = ['行政', '公益诉讼', '环保', '生态']

    combined = title + content[:2000]

    for kw in criminal_keywords:
        if kw in combined:
            return '刑事审判'
    for kw in admin_keywords:
        if kw in combined:
            return '诉讼与仲裁'
    for kw in civil_keywords:
        if kw in combined:
            return '诉讼与仲裁'

    return '刑事审判'  # Default for SPP guiding cases


def determine_tags(content: str, title: str, category: str) -> list:
    """Generate relevant tags."""
    tags = ['最高检', '指导性案例']

    # Extract case numbers
    case_nums = extract_case_numbers(content)
    if case_nums:
        tags.append(f'检例第{"、".join(case_nums[:3])}号')

    # Add category-based tag
    crime_types = {
        '毒品': '毒品犯罪', '绑架': '绑架罪', '故意杀人': '故意杀人罪',
        '抢劫': '抢劫罪', '诈骗': '诈骗罪', '贪污': '贪污罪',
        '受贿': '受贿罪', '走私': '走私罪', '盗窃': '盗窃罪',
        '交通肇事': '交通肇事罪', '危险驾驶': '危险驾驶罪',
        '聚众斗殴': '聚众斗殴罪', '强奸': '强奸罪', '猥亵': '猥亵罪',
        '公益诉讼': '公益诉讼', '行政': '行政检察',
        '民事': '民事检察', '生态': '生态环境',
        '金融': '金融犯罪', '职务': '职务犯罪',
        '网络': '网络犯罪', '电诈': '电信诈骗',
    }
    combined = title + content[:3000]
    for kw, tag in crime_types.items():
        if kw in combined and tag not in tags:
            tags.append(tag)
            if len(tags) >= 6:
                break

    return tags


def get_batch_number(filename: str) -> str:
    """Extract batch number from filename."""
    m = re.match(r'^(\d+)', filename)
    if m:
        num = int(m.group(1))
        # Convert number to Chinese batch notation
        cn_nums = ['', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十',
                   '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
                   '二十一', '二十二', '二十三', '二十四', '二十五', '二十六', '二十七', '二十八', '二十九', '三十',
                   '三十一', '三十二', '三十三', '三十四', '三十五', '三十六', '三十七', '三十八', '三十九', '四十',
                   '四十一', '四十二', '四十三', '四十四', '四十五', '四十六', '四十七', '四十八', '四十九', '五十',
                   '五十一', '五十二', '五十三', '五十四', '五十五', '五十六', '五十七', '五十八']
        if num < len(cn_nums):
            return f'第{cn_nums[num]}批'
    return ''


def create_wiki_page(filepath: Path) -> tuple:
    """Create a wiki summary page for a source file. Returns (success, filename, error)."""
    try:
        content = filepath.read_text(encoding='utf-8')
        filename = filepath.name

        # Extract metadata
        date = extract_date_from_filename(filename)
        if not date:
            date = extract_date_from_content(content)
        if not date:
            date = '20250527'  # Default date

        title = extract_title(content, filename)
        if not title:
            title = filename.replace('.md', '')

        batch = get_batch_number(filename)
        category = determine_category(content, title)
        tags = determine_tags(content, title, category)
        summary = summarize_content(content)
        case_nums = extract_case_numbers(content)

        # Build wiki page title
        wiki_title = f'最高检_指导性案例_{title}'
        wiki_title = sanitize_filename(wiki_title)

        # Build target filename
        target_name = f'summary_{date}_{wiki_title}.md'
        target_name = sanitize_filename(target_name)
        target_path = TARGET_DIR / target_name

        # Skip if already exists
        if target_path.exists():
            return (True, target_name, 'already_exists')

        # Build source path for frontmatter
        source_rel = f"sources/微信公号资料/最高人民检察院/最高检-指导性案例-md/{filename}"

        # Build case number string for overview
        case_num_str = '、'.join([f'检例第{n}号' for n in case_nums[:5]]) if case_nums else ''

        # Build keywords string
        keywords = extract_keywords(content)
        keywords_str = ' / '.join(keywords[:5]) if keywords else title

        # Build wiki content
        pub_date = ''
        if date and len(date) == 8:
            pub_date = f'{date[:4]}-{date[4:6]}-{date[6:8]}'

        wiki_content = f"""---
title: {title}
type: summary
created: 2026-05-27
updated: 2026-05-27
tags: {tags}
source: "{source_rel}"
category: {category}
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{filename}]] |
| 类型 | 最高检微信公号文章 · 指导性案例{f' · {batch}' if batch else ''} |
| 发布日期 | {pub_date} |
| 关键词 | {keywords_str} |
| 核心要点 | {f'{case_num_str}：' if case_num_str else ''}{summary[:150] if summary else title} |

## 正文摘要

{summary if summary else f'最高人民检察院{batch + "指导性案例" if batch else "指导性案例"}，详见原文。'}
"""
        target_path.write_text(wiki_content, encoding='utf-8')
        return (True, target_name, '')

    except Exception as e:
        return (False, filepath.name, str(e))


def main():
    """Main entry point."""
    # Ensure target directory exists
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    # Get all source files
    source_files = sorted(SOURCE_DIR.glob('*.md'))
    total = len(source_files)
    print(f"Found {total} source files in {SOURCE_DIR}")

    success_count = 0
    skip_count = 0
    fail_count = 0
    errors = []

    for i, filepath in enumerate(source_files, 1):
        ok, name, err = create_wiki_page(filepath)
        if ok:
            if err == 'already_exists':
                skip_count += 1
                if skip_count <= 5:
                    print(f"  [{i}/{total}] SKIP (exists): {name}")
            else:
                success_count += 1
                if success_count <= 10 or success_count % 10 == 0:
                    print(f"  [{i}/{total}] OK: {name}")
        else:
            fail_count += 1
            errors.append((name, err))
            print(f"  [{i}/{total}] FAIL: {name} - {err}")

    print(f"\n{'='*60}")
    print(f"Results: {success_count} created, {skip_count} skipped, {fail_count} failed")
    print(f"Total processed: {success_count + skip_count + fail_count}/{total}")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for name, err in errors:
            print(f"  - {name}: {err}")

    # Verify count
    existing = list(TARGET_DIR.glob('summary_*_最高检_指导性案例_*.md'))
    print(f"\nTotal 最高检_指导性案例 summary files in wiki/summaries/: {len(existing)}")


if __name__ == '__main__':
    main()
