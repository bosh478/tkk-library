#!/usr/bin/env python3
"""Batch ingest Shanghai First Intermediate Court 类案裁判方法 files to wiki/summaries/"""

import re
import os
from pathlib import Path
import unicodedata

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/上海一中法院/上海一中法院-类案裁判方法-md/")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/summaries/")

# Get all source files
source_files = sorted(SOURCE_DIR.glob("*.md"))
print(f"Found {len(source_files)} source files")

# Category mapping based on case type keywords
CATEGORY_KEYWORDS = {
    "行政": "诉讼与仲裁",
    "政府信息": "诉讼与仲裁",
    "民商事": "诉讼与仲裁",
    "申请再审": "诉讼与仲裁",
    "继承": "婚姻家庭与继承",
    "民间借贷": "金融与财税",
    "股权转让": "公司商事与合规",
    "公司解散": "公司商事与合规",
    "公司": "公司商事与合规",
    "租赁": "建筑工程与房地产",
    "竞业限制": "劳动与社会保障",
    "劳动": "劳动与社会保障",
    "社会保险": "劳动与社会保障",
    "证券": "金融与财税",
    "内幕交易": "金融与财税",
    "股东": "公司商事与合规",
    "仲裁": "诉讼与仲裁",
    "业主": "建筑工程与房地产",
    "违法建筑": "建筑工程与房地产",
    "未成年人": "诉讼与仲裁",
    "校园": "诉讼与仲裁",
    "人格权": "诉讼与仲裁",
    "治安": "诉讼与仲裁",
    "劳务派遣": "劳动与社会保障",
    "清算": "公司商事与合规",
    "执行": "诉讼与仲裁",
    "追加": "诉讼与仲裁",
    "无效": "公司商事与合规",
    "房屋租赁": "建筑工程与房地产",
    "报酬": "劳动与社会保障",
    "轻微暴力": "诉讼与仲裁",
    "死亡": "诉讼与仲裁",
    "司法审查": "诉讼与仲裁",
    "工伤": "劳动与社会保障",
    "消费": "消费者保护",
    "惩罚性赔偿": "消费者保护",
    "非法集资": "金融与财税",
    "夫妻共同债务": "婚姻家庭与继承",
    "共有房屋": "建筑工程与房地产",
    "命案": "诉讼与仲裁",
    "营运车辆": "交通与物流",
    "损害公司利益": "公司商事与合规",
    "抚养": "婚姻家庭与继承",
    "货运": "交通与物流",
    "道路交通": "交通与物流",
    "福利待遇": "劳动与社会保障",
    "提供劳务": "劳动与社会保障",
    "企业借贷": "金融与财税",
    "承包经营": "公司商事与合规",
    "鉴定意见": "诉讼与仲裁",
    "人事争议": "劳动与社会保障",
    "医疗损害": "医药健康",
    "行政驳回": "诉讼与仲裁",
    "借名买房": "建筑工程与房地产",
    "电信网络诈骗": "诉讼与仲裁",
    "分配方案": "公司商事与合规",
    "离婚": "婚姻家庭与继承",
    "案外人": "诉讼与仲裁",
    "委托理财": "金融与财税",
    "操纵证券市场": "金融与财税",
    "市场监督管理": "政府与公共法律服务",
    "合并之诉": "诉讼与仲裁",
    "服务合同": "公司商事与合规",
    "共同侵权": "诉讼与仲裁",
    "买卖合同": "公司商事与合规",
    "贩卖毒品": "诉讼与仲裁",
    "以房抵债": "建筑工程与房地产",
    "组织卖淫": "诉讼与仲裁",
    "聚众斗殴": "诉讼与仲裁",
    "履行法定职责": "诉讼与仲裁",
    "离婚损害赔偿": "婚姻家庭与继承",
    "商品房买卖": "建筑工程与房地产",
    "不当得利": "金融与财税",
    "重复起诉": "诉讼与仲裁",
    "公民个人信息": "知识产权",
    "计算机信息系统": "知识产权",
    "委托合同": "公司商事与合规",
    "合同诈骗": "公司商事与合规",
    "承揽合同": "公司商事与合规",
    "涉外": "国际贸易",
    "涉港澳台": "国际贸易",
    "遗嘱继承": "婚姻家庭与继承",
    "房屋征收": "建筑工程与房地产",
    "公司决议": "公司商事与合规",
    "对赌协议": "金融与财税",
    "公司证照": "公司商事与合规",
    "公证债权": "诉讼与仲裁",
    "互联网平台": "劳动与社会保障",
    "动产": "金融与财税",
    "非婚同居": "婚姻家庭与继承",
    "赡养": "婚姻家庭与继承",
}

def sanitize_filename(filename):
    """Remove or replace characters that are invalid in Windows filenames"""
    filename = re.sub(r'[\\|:*/?"<>|]', '_', filename)
    filename = re.sub(r'_+', '_', filename)
    return filename

def extract_date_from_filename(filename):
    """Extract YYYYMMDD from [YYYY-MM-DD]filename pattern"""
    match = re.match(r"\[(\d{4}-\d{2}-\d{2})\]\s*(.*)", filename)
    if match:
        date_str = match.group(1)
        return date_str.replace("-", ""), match.group(2).strip()
    return None, filename

def extract_title_from_content(content):
    """Extract title from first # heading"""
    match = re.match(r"#\s*类案裁判方法\|\s*(.+?)(?:\n|$)", content)
    if match:
        return match.group(1).strip()
    # Fallback
    lines = content.split("\n")
    for line in lines:
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return "未知标题"

def determine_tags(title, content):
    """Determine tags based on title and content"""
    tags = ["类案裁判方法", "上海一中院"]

    # Add case type tags based on keywords
    for keyword, tag in CATEGORY_KEYWORDS.items():
        if keyword in title:
            if tag not in tags:
                tags.append(tag)

    # Criminal cases
    if any(k in title for k in ["犯罪", "毒品", "诈骗", "内幕交易", "操纵证券", "卖淫", "聚众斗殴"]):
        if "刑事" not in tags:
            tags.append("刑事")

    # Administrative cases
    if any(k in title for k in ["行政", "处罚", "政府信息"]):
        if "行政" not in tags:
            tags.append("行政")

    return tags

def determine_category(title):
    """Determine category based on title keywords"""
    for keyword, category in CATEGORY_KEYWORDS.items():
        if keyword in title:
            return category
    return "诉讼与仲裁"

def extract_key_points(content, min_points=5):
    """Extract key points from content - meaningful sentences from body"""
    key_points = []

    # Remove editor's note section and title
    content = re.sub(r"\*\*编者按\*\*.*?(?=\n\*\*|$)", "", content, flags=re.DOTALL)
    content = re.sub(r"#{1,6}\s*类案裁判方法\|?\s*", "", content)

    # Find all major sections and extract first substantial sentence from each
    sections = re.split(r"\n(?=\*\*[一二三四五六七八九十]+|\*\*\d+\*\*|\*\*案例|\*\*三|\*\*四|\*\*五)", content)

    for section in sections:
        if not section.strip() or len(section.strip()) < 30:
            continue

        # Clean markdown
        clean = re.sub(r"\*\*(.*?)\*\*", r"\1", section)
        clean = re.sub(r"#{1,6}\s*", "", clean)

        # Find first meaningful sentence (>= 30 chars with proper ending)
        sentences = re.findall(r"[^。！？.!?\n]{30,200}[。！？.!?]?", clean)
        for sent in sentences:
            sent = sent.strip()
            # Skip if it looks like a heading or too short
            if len(sent) < 25:
                continue
            # Skip if it contains only numbers or single word repeats
            if sent not in key_points and sent[:10] != sent[10:20]:
                key_points.append(sent[:180])
                break

        if len(key_points) >= min_points + 2:
            break

    # If still not enough, extract from body more liberally
    if len(key_points) < min_points:
        body = re.sub(r"#{1,6}\s*", "", content)
        sentences = re.findall(r"[^。！？.!?\n]{40,200}[。！？.!?]?", body)
        for sent in sentences:
            sent = sent.strip()
            if sent and sent not in key_points and len(sent) > 30:
                key_points.append(sent[:180])
            if len(key_points) >= min_points + 2:
                break

    return key_points[:min_points + 2]

def create_summary_file(source_file, target_dir):
    """Create a wiki summary file from a source file"""
    content = source_file.read_text(encoding="utf-8")

    # Extract date and original filename
    date_str, rest = extract_date_from_filename(source_file.name)
    if not date_str:
        print(f"  SKIP (no date): {source_file.name}")
        return False

    # Extract title
    title = extract_title_from_content(content)

    # Determine tags and category
    tags = determine_tags(title, content)
    category = determine_category(title)

    # Extract key points
    key_points = extract_key_points(content)
    key_points_str = "\n".join([f"{i+1}. {p}" for i, p in enumerate(key_points[:5])])

    # Get body content for abbreviated section
    body_start = content.find("**一**")
    if body_start == -1:
        body_start = content.find("\n", content.find("#"))
    body_content = content[body_start:body_start + 2000] if body_start > 0 else content[:2000]
    body_content = re.sub(r"#{1,6}\s*类案裁判方法\|?\s*", "", body_content)
    body_content = re.sub(r"\*\*编者按\*\*.*?(?=\n\*\*|$)", "", body_content, flags=re.DOTALL)

    # Create frontmatter
    frontmatter = f"""---
title: {title}
type: summary
published: {date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}
created: 2026-05-11
updated: 2026-05-11
tags: [{", ".join(tags)}]
category: {category}
source: [[{source_file.name}]]
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{source_file.name}]] |
| 类型 | 类案裁判方法 |
| 发布日期 | {date_str[:4]}-{date_str[4:6]}-{date_str[6:8]} |
| 关键词 | {", ".join(tags)} |

## 核心要点

{key_points_str}

## 裁判方法摘要

{body_content}...
"""

    # Create target filename using just date and a short identifier
    title_short = re.sub(r'[【】\[\]（）\(\)《》<>]', '', title)[:20]
    title_short = sanitize_filename(title_short)

    target_filename = f"summary_{date_str}_上海一中法院_类案裁判方法_{title_short}.md"
    target_path = target_dir / target_filename

    # Write file
    target_path.write_text(frontmatter, encoding="utf-8")
    return True

# Process all files
success_count = 0
fail_count = 0

for i, source_file in enumerate(source_files, 1):
    try:
        if create_summary_file(source_file, TARGET_DIR):
            success_count += 1
            if success_count % 20 == 0:
                print(f"Processed {success_count}/{len(source_files)} files...")
    except Exception as e:
        print(f"  ERROR: {source_file.name}: {e}")
        fail_count += 1

print(f"\nCompleted: {success_count} succeeded, {fail_count} failed")
print(f"Total: {len(source_files)} source files")