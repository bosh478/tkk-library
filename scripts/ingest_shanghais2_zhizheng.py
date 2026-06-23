#!/usr/bin/env python3
"""
Ingest 至正开放麦 md files into wiki/summaries/
"""
import os
import re
import glob
from pathlib import Path
from datetime import datetime
import concurrent.futures
import hashlib

# VAULT_ROOT 多平台兼容（patched 2026-06-23）：
# 1. 优先 TKK_VAULT_ROOT 环境变量
# 2. Windows: "D:/AI agent/tkk-library"
# 3. Linux/WSL: /home/kangkang/tkk-library 等候选按存在性自动探测
_VAULT_CANDIDATES = [
    os.environ.get("TKK_VAULT_ROOT"),
    "D:/AI agent/tkk-library" if os.name == "nt" else None,
    "/home/kangkang/tkk-library",
    "/mnt/d/AI agent/tkk-library",
    "/mnt/c/Users/汤康康/tkk-library",
]
VAULT_ROOT = next(
    (Path(p) for p in _VAULT_CANDIDATES if p and Path(p).exists()),
    Path(os.environ.get("TKK_VAULT_ROOT", "D:/AI agent/tkk-library"))
)
SOURCE_DIR = VAULT_ROOT / "sources/微信公号资料/上海二中院/上海二中院-至正开放麦-md"
TARGET_DIR = VAULT_ROOT / "wiki/summaries"

# Tags mapping based on content keywords
TAG_KEYWORDS = {
    "公司": ["公司法", "公司资本", "公司治理", "股权转让", "股东", "董事", "高管"],
    "合同": ["合同", "违约", "解除", "效力", "无效", "解除权"],
    "婚姻家庭": ["婚姻", "离婚", "抚养", "彩礼", "继承", "房产分割", "家庭暴力"],
    "劳动": ["劳动", "劳动合同", "竞业限制", "社保", "裁员", "工资"],
    "刑事": ["诈骗", "罪与", "刑法", "犯罪", "量刑", "自首", "追诉"],
    "房产": ["二手房", "购房", "房产", "租房", "房屋", "物业", "小区"],
    "金融": ["金融", "贷款", "投资", "证券", "虚拟盘", "洗钱"],
    "执行": ["执行", "被执行人", "财产", "债权", "债务"],
    "行政": ["行政", "处罚", "投诉", "举报", "诉讼"],
    "消费者": ["消费者", "网络消费", "欺诈", "退一赔三", "平台"],
}

def extract_title(content):
    """Extract title from first # line"""
    lines = content.split('\n')
    for line in lines:
        if line.startswith('#'):
            # Remove # and spaces, then remove date prefix and suffix
            title = line.lstrip('#').strip()
            # Remove date prefix like [2023-02-03]
            title = re.sub(r'^\[\d{4}-\d{2}-\d{2}\]', '', title)
            # Remove trailing "至正开放麦" or variations
            title = re.sub(r'至正开放麦.*$', '', title)
            title = re.sub(r'至正论法.*$', '', title)
            title = re.sub(r'\|.*$', '', title)
            title = title.strip()
            return title
    return "未命名"

def extract_author(content):
    """Extract author info from content"""
    lines = content.split('\n')
    author = None
    court = None
    title = None
    for line in lines:
        if '**上海二中院' in line:
            court = "上海二中院"
        # Match pattern like **焦明静\n**上海二中院...
        if re.match(r'^\*\*[一-龥]+', line):
            name = line.strip('*').strip()
            if not author and court:
                author = name
    return author, court

def extract_date_from_filename(filename):
    """Extract date from filename like [2023-02-03]xxx"""
    match = re.match(r'\[(\d{4}-\d{2}-\d{2})\]', filename)
    if match:
        return match.group(1)
    return "2023-01-01"

def extract_tags(content, title):
    """Extract relevant tags based on content"""
    tags = ["至正开放麦", "上海二中法院"]
    combined = content + title

    for tag, keywords in TAG_KEYWORDS.items():
        for kw in keywords:
            if kw in combined:
                if tag not in tags:
                    tags.append(tag)
                break

    return tags[:8]  # Limit to 8 tags

def extract_summary(content, title):
    """Extract key content from article"""
    lines = content.split('\n')

    # Skip header lines until we hit real content
    summary_points = []
    in_content = False
    author_block = False

    for i, line in enumerate(lines):
        # Skip header tags
        if line.strip() in ['开机', '** 至正开放麦 **', '第一场  第一条', 'action']:
            continue

        # Skip author info block
        if '责任编辑' in line or '视频' in line or '版面编辑' in line:
            author_block = True
            continue
        if line.strip() == '__':
            author_block = False
            continue

        if author_block:
            continue

        # Real content
        if line.startswith('#'):
            continue

        # Collect substantive lines
        stripped = line.strip()
        if stripped and len(stripped) > 10:
            # Clean markdown formatting
            cleaned = re.sub(r'\*+', '', stripped)
            if cleaned and not cleaned.startswith('预览时标签不可点') and not cleaned.startswith('修改于'):
                summary_points.append(cleaned)

    # Build summary
    if len(summary_points) > 3:
        # First point is often the intro
        summary = summary_points[0][:200] if len(summary_points[0]) > 200 else summary_points[0]
    else:
        summary = " ".join(summary_points[:3])

    return summary, summary_points[:5]

def generate_related(content):
    """Generate related links based on content"""
    related = []
    if "合同" in content:
        related.append("[[concept_合同效力]]")
    if "公司" in content:
        related.append("[[concept_公司法律制度]]")
    if "房产" in content or "二手房" in content:
        related.append("[[concept_二手房买卖]]")
    if "诈骗" in content:
        related.append("[[concept_诈骗罪]]")
    if "劳动" in content:
        related.append("[[concept_劳动合同]]")
    if "婚姻" in content or "离婚" in content:
        related.append("[[concept_离婚纠纷]]")
    if "继承" in content:
        related.append("[[concept_继承纠纷]]")

    if not related:
        related = ["[[concept_民事诉讼]]"]

    return related

def process_file(filepath):
    """Process a single file and return the wiki content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        filename = filepath.name
        title = extract_title(content)
        date = extract_date_from_filename(filename)
        tags = extract_tags(content, title)
        summary, points = extract_summary(content, title)
        related = generate_related(content)

        # Create frontmatter
        frontmatter = f"""---
title: {title}
type: summary
category: 诉讼与仲裁
created: 2026-05-11
updated: 2026-05-11
tags: [{', '.join(tags)}]
source: "sources/微信公号资料/上海二中院/上海二中院-至正开放麦-md/{filename}"
related: [{', '.join(related)}]
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{filename}]] |
| 类型 | 司法案例分析 / 法律知识普及 |
| 发布日期 | {date} |
| 关键词 | {', '.join(tags[:5])} |
| 核心要点 | {len(points)}条 |

## 核心内容

"""

        # Add summary points
        for i, point in enumerate(points, 1):
            if len(point) > 300:
                point = point[:300] + "..."
            frontmatter += f"{i}. {point}\n\n"

        # Add practical tips section
        frontmatter += """
## 实践要点

"""

        # Extract practical tips (usually from conclusion)
        conclusion_lines = []
        in_conclusion = False
        for line in content.split('\n'):
            if '希望' in line or '建议' in line or '注意' in line:
                in_conclusion = True
            if in_conclusion:
                cleaned = re.sub(r'\*+', '', line.strip())
                if cleaned and len(cleaned) > 5:
                    conclusion_lines.append(cleaned)
                if len(conclusion_lines) > 5:
                    break

        if conclusion_lines:
            for tip in conclusion_lines[:3]:
                frontmatter += f"- {tip}\n"
        else:
            frontmatter += "- 详见全文分析\n"

        return frontmatter, title, date
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return None, None, None

def main():
    # Get list of source files (exclude .cfg files)
    source_files = []
    for f in SOURCE_DIR.glob("*.md"):
        if not f.name.endswith('.cfg') and '.baiduyun' not in f.name:
            source_files.append(f)

    print(f"Found {len(source_files)} source files")

    # Process files in parallel
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(process_file, f): f for f in source_files}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result[0]:
                results.append(result)

    print(f"Processed {len(results)} files")

    # Write output files
    for content, title, date in results:
        if content and title:
            # Clean title for filename
            clean_title = re.sub(r'[^一-龥a-zA-Z0-9]', '', title)
            clean_title = clean_title[:50]  # Limit length
            filename = f"summary_Court_上海二中院_至正开放麦_{clean_title}.md"
            filepath = TARGET_DIR / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Created: {filename}")

    print(f"\nTotal files created: {len(results)}")

if __name__ == "__main__":
    main()