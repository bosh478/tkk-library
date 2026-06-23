#!/usr/bin/env python3
"""
Batch ingest script for 上海一中法院 WeChat articles.
Processes all .md files from sources/微信公号资料/上海一中法院/ and creates wiki summaries.
"""
import os
import re
from pathlib import Path
from datetime import datetime

# Configuration
VAULT_ROOT = Path(r"D:\AI agent\tkk-library")
SRC_BASE = VAULT_ROOT / "sources" / "微信公号资料" / "上海一中法院"
DST_BASE = VAULT_ROOT / "wiki" / "summaries"

# Category mapping based on subdirectory
CATEGORY_MAP = {
    "上海一中法院-微课程-md": ("微课程", "诉讼与仲裁"),
    "上海一中法院-类案裁判方法-md": ("类案裁判方法", "诉讼与仲裁"),
    "上海一中法院-开庭-md": ("开庭实务", "诉讼与仲裁"),
    "上海一中法院-法通识-md": ("法通识", "诉讼与仲裁"),
    "上海一中法院-衡石·观点-md": ("衡石观点", "诉讼与仲裁"),
}

def extract_date(filename: str) -> str:
    """Extract date from filename pattern [YYYY-MM-DD]"""
    match = re.search(r'\[(\d{4}-\d{2}-\d{2})\]', filename)
    if match:
        return match.group(1)
    return "unknown"

def extract_title_from_content(content: str, filename: str) -> str:
    """Extract title from first # line or filename"""
    # Try to find title from first # line
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('#'):
            title = line.lstrip('#').strip()
            # Remove common suffixes
            title = re.sub(r'\s*\|\s*(微课程|类案裁判方法|法通识|衡石观点|开庭).*$', '', title)
            title = re.sub(r'\s*(微课程|类案裁判方法|法通识|衡石观点|开庭)$', '', title)
            if title and len(title) > 5:
                return title

    # Fallback: extract from filename
    name = Path(filename).stem
    # Remove date prefix
    name = re.sub(r'^\[\d{4}-\d{2}-\d{2}\]', '', name)
    # Remove category suffixes
    name = re.sub(r'(微课程|类案裁判方法|法通识|衡石观点|开庭)$', '', name)
    return name.strip() if name.strip() else filename

def extract_summary(content: str, max_chars: int = 500) -> str:
    """Extract key content summary (200-500 chars)"""
    lines = content.split('\n')
    summary_lines = []
    char_count = 0
    in_content = False

    for line in lines:
        line = line.strip()

        # Skip metadata and headers
        if line.startswith('---') or line.startswith('title:') or line.startswith('type:'):
            continue
        if line.startswith('source:') or line.startswith('created:') or line.startswith('updated:'):
            continue
        if line.startswith('#') and not in_content:
            in_content = True
            continue

        # Skip empty lines and formatting
        if not line or line.startswith('|') or line.startswith('---'):
            continue
        if line.startswith('**') and line.endswith('**'):
            continue

        # Collect meaningful content
        if len(line) > 20 and not line.startswith('*'):
            summary_lines.append(line)
            char_count += len(line)
            if char_count >= max_chars:
                break

    return '\n'.join(summary_lines[:10])  # Limit to 10 lines

def extract_keywords(content: str, filename: str) -> list:
    """Extract keywords from content"""
    keywords = []

    # Common legal topics
    legal_topics = [
        '合同', '劳动', '婚姻', '继承', '侵权', '公司', '股权', '借贷',
        '担保', '物权', '债权', '知识产权', '行政', '刑事', '民事',
        '执行', '仲裁', '诉讼', '调解', '判决', '裁定', '管辖',
        '证据', '时效', '违约', '解除', '终止', '无效', '撤销',
        '股东', '董事', '清算', '破产', '重整', '和解',
        '房屋', '租赁', '买卖', '转让', '抵押', '质押',
        '人身', '财产', '名誉', '隐私', '人格',
        '交通事故', '医疗', '消费', '保险', '金融',
    ]

    content_lower = content.lower()
    for topic in legal_topics:
        if topic in content:
            keywords.append(topic)
            if len(keywords) >= 5:
                break

    # Add category from filename
    if '类案裁判方法' in filename:
        keywords.append('类案裁判方法')
    if '微课程' in filename:
        keywords.append('微课程')
    if '法通识' in filename:
        keywords.append('法通识')

    return keywords if keywords else ['法律实务']

def determine_tags(content: str, category: str) -> list:
    """Determine tags based on content and category"""
    tags = ["上海一中法院"]

    # Add category tag
    tags.append(category)

    # Detect content type
    if '刑事' in content or '犯罪' in content or '刑罚' in content:
        tags.append('刑事')
    if '民事' in content or '民法' in content:
        tags.append('民事')
    if '行政' in content or '政府' in content:
        tags.append('行政')
    if '公司' in content or '企业' in content:
        tags.append('公司商事')
    if '劳动' in content or '雇佣' in content:
        tags.append('劳动')
    if '合同' in content:
        tags.append('合同')
    if '程序' in content or '诉讼' in content:
        tags.append('诉讼程序')

    return tags

def generate_summary_filename(date: str, category: str, title: str) -> str:
    """Generate summary filename"""
    # Clean title for filename
    clean_title = re.sub(r'[<>:"/\\|?*]', '', title)
    clean_title = clean_title[:50]  # Limit length

    # Format: summary_YYYYMMDD_上海一中法院_类别_标题.md
    date_compact = date.replace('-', '')
    return f"summary_{date_compact}_上海一中法院_{category}_{clean_title}.md"

def create_summary_page(src_file: Path, subcategory: str) -> tuple:
    """Create a summary wiki page for a source file"""
    try:
        # Read source file
        with open(src_file, 'r', encoding='utf-8') as f:
            content = f.read()

        filename = src_file.name
        date = extract_date(filename)
        title = extract_title_from_content(content, filename)
        summary = extract_summary(content)
        keywords = extract_keywords(content, filename)

        # Get category info
        cat_info = CATEGORY_MAP.get(subcategory, ("其他", "诉讼与仲裁"))
        category_name, main_category = cat_info

        tags = determine_tags(content, category_name)

        # Generate output filename
        out_filename = generate_summary_filename(date, category_name, title)
        out_path = DST_BASE / out_filename

        # Create summary content
        summary_content = f"""---
title: {title}
type: summary
published: {date}
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
tags: [{', '.join(tags)}]
source: "sources/微信公号资料/上海一中法院/{subcategory}/{filename}"
category: {main_category}
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{filename}]] |
| 类型 | 上海一中法院{category_name} |
| 发布日期 | {date} |
| 关键词 | {', '.join(keywords)} |
| 核心要点 | {summary[:100]}... |

## 正文摘要

{summary}

## 关键要点

"""
        # Add key points from summary
        points = summary.split('\n')[:5]
        for i, point in enumerate(points, 1):
            if point.strip():
                summary_content += f"{i}. {point.strip()}\n"

        return out_path, summary_content, title

    except Exception as e:
        print(f"Error processing {src_file}: {e}")
        return None, None, None

def main():
    """Main processing function"""
    print("=" * 60)
    print("上海一中法院 WeChat Articles Batch Ingest")
    print("=" * 60)

    # Ensure output directory exists
    DST_BASE.mkdir(parents=True, exist_ok=True)

    total_processed = 0
    total_errors = 0
    results = {}

    # Process each subdirectory
    for subcategory in CATEGORY_MAP.keys():
        src_dir = SRC_BASE / subcategory
        if not src_dir.exists():
            print(f"Warning: Directory not found: {src_dir}")
            continue

        # Get all .md files
        md_files = list(src_dir.glob("*.md"))
        print(f"\nProcessing {subcategory}: {len(md_files)} files")

        processed = 0
        errors = 0

        for src_file in md_files:
            out_path, content, title = create_summary_page(src_file, subcategory)

            if content:
                # Write summary file
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                processed += 1
                total_processed += 1
            else:
                errors += 1
                total_errors += 1

        results[subcategory] = {
            'total': len(md_files),
            'processed': processed,
            'errors': errors
        }

        print(f"  Processed: {processed}/{len(md_files)}")

    # Print summary
    print("\n" + "=" * 60)
    print("PROCESSING COMPLETE")
    print("=" * 60)
    print(f"Total files processed: {total_processed}")
    print(f"Total errors: {total_errors}")
    print("\nBreakdown by category:")
    for cat, stats in results.items():
        print(f"  {cat}: {stats['processed']}/{stats['total']}")

    # List generated files
    print(f"\nGenerated files in: {DST_BASE}")
    generated = list(DST_BASE.glob("summary_*上海一中*.md"))
    print(f"Total summary files: {len(generated)}")

if __name__ == "__main__":
    main()
