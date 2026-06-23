#!/usr/bin/env python3
"""
Batch ingest WeChat articles from 最高人民法院 公众号.
Processes sources/微信公号资料/最高人民法院/ subdirectories into wiki/summaries/.

Currently focused on 最高法-入库案例选介-md (100 files) since other categories are done.
"""

import os
import re
import sys
from pathlib import Path

VAULT_ROOT = Path(r"D:\AI agent\tkk-library")
SOURCE_BASE = VAULT_ROOT / "sources" / "微信公号资料" / "最高人民法院"
WIKI_SUMMARIES = VAULT_ROOT / "wiki" / "summaries"

# Category mapping based on keywords in title/content
CATEGORY_MAP = {
    # Criminal
    "故意伤害": "刑事审判",
    "故意杀人": "刑事审判",
    "正当防卫": "刑事审判",
    "盗窃": "刑事审判",
    "诈骗": "刑事审判",
    "合同诈骗": "刑事审判",
    "信用卡诈骗": "刑事审判",
    "集资诈骗": "刑事审判",
    "保险诈骗": "刑事审判",
    "组织卖淫": "刑事审判",
    "强迫卖淫": "刑事审判",
    "贩卖毒品": "刑事审判",
    "运输毒品": "刑事审判",
    "制造毒品": "刑事审判",
    "走私": "刑事审判",
    "贪污": "刑事审判",
    "受贿": "刑事审判",
    "行贿": "刑事审判",
    "挪用公款": "刑事审判",
    "滥用职权": "刑事审判",
    "玩忽职守": "刑事审判",
    "交通肇事": "刑事审判",
    "危险驾驶": "刑事审判",
    "醉驾": "刑事审判",
    "强奸": "刑事审判",
    "猥亵": "刑事审判",
    "拐卖": "刑事审判",
    "绑架": "刑事审判",
    "抢劫": "刑事审判",
    "抢夺": "刑事审判",
    "敲诈勒索": "刑事审判",
    "故意毁坏": "刑事审判",
    "放火": "刑事审判",
    "爆炸": "刑事审判",
    "投毒": "刑事审判",
    "非法持有枪支": "刑事审判",
    "非法经营": "刑事审判",
    "生产销售伪劣": "刑事审判",
    "假冒注册商标": "刑事审判",
    "侵犯著作权": "刑事审判",
    "侵犯公民个人信息": "刑事审判",
    "掩饰隐瞒犯罪所得": "刑事审判",
    "帮助信息网络犯罪": "刑事审判",
    "开设赌场": "刑事审判",
    "赌博": "刑事审判",
    "寻衅滋事": "刑事审判",
    "聚众斗殴": "刑事审判",
    "非法拘禁": "刑事审判",
    "破坏计算机信息系统": "刑事审判",
    "提供虚假证明文件": "刑事审判",
    "伪造": "刑事审判",
    "买卖国家机关": "刑事审判",
    "信用卡": "刑事审判",
    "宣告无罪": "刑事审判",
    "撤回起诉": "刑事审判",
    "缓刑": "刑事审判",
    "量刑": "刑事审判",
    "犯罪": "刑事审判",
    "刑事": "刑事审判",
    "刑法": "刑事审判",
    # Civil / IP
    "知识产权": "知识产权",
    "商标": "知识产权",
    "专利": "知识产权",
    "著作权": "知识产权",
    "不正当竞争": "知识产权",
    "商业秘密": "知识产权",
    # Labor
    "劳动争议": "诉讼与仲裁",
    "劳动关系": "诉讼与仲裁",
    "劳动合同": "诉讼与仲裁",
    "工伤": "诉讼与仲裁",
    "劳动仲裁": "诉讼与仲裁",
    # Corporate
    "公司": "公司商事与合规",
    "股东": "公司商事与合规",
    "股权": "公司商事与合规",
    "破产": "公司商事与合规",
    "清算": "公司商事与合规",
    "重整": "公司商事与合规",
    # General civil
    "合同纠纷": "诉讼与仲裁",
    "买卖合同": "诉讼与仲裁",
    "租赁合同": "诉讼与仲裁",
    "借款合同": "诉讼与仲裁",
    "担保": "诉讼与仲裁",
    "抵押": "诉讼与仲裁",
    "侵权": "诉讼与仲裁",
    "相邻关系": "诉讼与仲裁",
    "生命权": "诉讼与仲裁",
    "健康权": "诉讼与仲裁",
    "身体权": "诉讼与仲裁",
    "名誉权": "诉讼与仲裁",
    "肖像权": "诉讼与仲裁",
    "隐私权": "诉讼与仲裁",
    "个人信息": "诉讼与仲裁",
    "网络侵权": "诉讼与仲裁",
    "继承": "诉讼与仲裁",
    "收养": "诉讼与仲裁",
    "婚姻": "诉讼与仲裁",
    "离婚": "诉讼与仲裁",
    "抚养": "诉讼与仲裁",
    "赡养": "诉讼与仲裁",
    "交通事故": "诉讼与仲裁",
    "医疗损害": "诉讼与仲裁",
    "饲养动物": "诉讼与仲裁",
    "物权": "诉讼与仲裁",
    "所有权": "诉讼与仲裁",
    "民事": "诉讼与仲裁",
    "诉讼": "诉讼与仲裁",
    "仲裁": "诉讼与仲裁",
    "执行": "诉讼与仲裁",
    "保全": "诉讼与仲裁",
    "行政": "诉讼与仲裁",
}


def extract_date(filename: str) -> str:
    """Extract date from filename like [2024-04-18]..."""
    m = re.search(r"\[(\d{4}-\d{2}-\d{2})\]", filename)
    if m:
        return m.group(1)
    return ""


def extract_title_from_filename(filename: str) -> str:
    """Extract clean title from filename."""
    # Remove date prefix
    name = re.sub(r"^\[\d{4}-\d{2}-\d{2}\]", "", filename)
    # Remove .md extension
    name = name.replace(".md", "")
    return name.strip()


def extract_title_from_content(content: str) -> str:
    """Extract title from first # line in content."""
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("#"):
            title = line.lstrip("#").strip()
            # Remove markdown bold markers
            title = title.replace("**", "").strip()
            if title:
                return title
    return ""


def classify_article(title: str, content: str) -> str:
    """Classify article into category based on keywords."""
    text = title + " " + content[:1000]

    # Priority-based matching
    for keyword, category in CATEGORY_MAP.items():
        if keyword in text:
            return category

    return "诉讼与仲裁"  # Default


def extract_keywords(title: str, content: str) -> list:
    """Extract key topics from title and content."""
    keywords = []

    # Extract case name patterns like XXX案, XXX纠纷
    case_name = re.findall(r"[一-鿿]{2,10}(?:案|纠纷|罪)", title)
    keywords.extend(case_name)

    # Extract specific legal topics
    topic_patterns = [
        r"(正当防卫)", r"(劳动争议)", r"(交通事故)",
        r"(知识产权)", r"(不正当竞争)", r"(破产重整)",
        r"(劳动关系)", r"(工伤)", r"(侵权责任)",
        r"(合同纠纷)", r"(婚姻家庭)",
        r"(继承)", r"(收养)", r"(相邻关系)",
        r"(生命权)", r"(健康权)", r"(名誉权)",
        r"(肖像权)", r"(隐私权)", r"(个人信息)",
        r"(网络侵权)", r"(饲养动物)", r"(环境污染)",
        r"(产品责任)", r"(医疗损害)", r"(民间借贷)",
        r"(房屋买卖)", r"(租赁)", r"(物业服务)",
        r"(建设工程)", r"(股权转让)", r"(公司决议)",
        r"(清算责任)", r"(破产债权)",
        r"(贪污)", r"(受贿)", r"(诈骗)", r"(盗窃)",
        r"(故意伤害)", r"(交通肇事)", r"(危险驾驶)",
        r"(组织卖淫)", r"(贩卖毒品)", r"(走私)",
        r"(非法经营)", r"(假冒注册商标)", r"(侵犯著作权)",
        r"(信用卡诈骗)", r"(合同诈骗)", r"(集资诈骗)",
        r"(掩饰隐瞒)", r"(帮助信息网络)", r"(开设赌场)",
        r"(寻衅滋事)", r"(非法拘禁)", r"(非法持有枪支)",
        r"(提供虚假证明文件)", r"(破坏计算机信息系统)",
        r"(买卖国家机关公文)", r"(侵犯公民个人信息)",
        r"(宣告无罪)", r"(撤回起诉)", r"(缓刑)",
        r"(物权)", r"(担保)", r"(抵押)", r"(保证)",
        r"(执行异议)", r"(仲裁)", r"(行政确认)",
    ]

    for pattern in topic_patterns:
        matches = re.findall(pattern, title + " " + content[:500])
        keywords.extend(matches)

    # Deduplicate and limit
    seen = set()
    unique = []
    for kw in keywords:
        if kw not in seen and len(kw) >= 2:
            seen.add(kw)
            unique.append(kw)

    return unique[:5] if unique else [title[:20]]


def extract_core_points(content: str) -> str:
    """Extract 2-3 key points from content."""
    lines = content.split("\n")
    points = []

    # Look for 裁判要旨 section
    in_summary = False
    for line in lines:
        line = line.strip()
        if "裁判要旨" in line or "裁判理由" in line:
            in_summary = True
            continue
        if in_summary:
            if line and not line.startswith("#") and not line.startswith("**"):
                # Clean up
                clean = line.replace("**", "").strip()
                if clean and len(clean) > 10:
                    points.append(clean[:150])
                    if len(points) >= 2:
                        break
            elif line.startswith("#") and "裁判" not in line:
                break

    # If no 裁判要旨 found, take first substantial paragraph
    if not points:
        for line in lines[2:15]:
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("**"):
                clean = line.replace("**", "").strip()
                if len(clean) > 20:
                    points.append(clean[:150])
                    if len(points) >= 2:
                        break

    return "；".join(points) if points else ""


def extract_summary(content: str) -> str:
    """Extract a concise summary (200-500 chars) from content."""
    lines = content.split("\n")
    summary_parts = []

    # Strategy: find key sections and extract main content
    key_sections = ["裁判要旨", "基本案情", "裁判理由", "裁判结果"]
    current_section = ""
    section_content = []

    for line in lines:
        stripped = line.strip()

        # Check for section headers
        found_section = None
        for section in key_sections:
            if section in stripped:
                found_section = section
                break

        if found_section:
            # Save previous section
            if current_section and section_content:
                text = "\n".join(section_content)
                if len(text) > 20:
                    summary_parts.append(f"**{current_section}**：{text[:200]}")
            current_section = found_section
            section_content = []
        elif current_section:
            # Collect content
            if stripped and not stripped.startswith("#"):
                clean = stripped.replace("**", "").strip()
                if clean:
                    section_content.append(clean)

    # Save last section
    if current_section and section_content:
        text = "\n".join(section_content)
        if len(text) > 20:
            summary_parts.append(f"**{current_section}**：{text[:200]}")

    if summary_parts:
        return "\n\n".join(summary_parts)

    # Fallback: take first few paragraphs
    paragraphs = []
    for line in lines[1:20]:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith("**"):
            clean = stripped.replace("**", "").strip()
            if len(clean) > 20:
                paragraphs.append(clean)

    if paragraphs:
        text = "\n\n".join(paragraphs[:3])
        return text[:500]

    return ""


def generate_tags(title: str, category: str, content: str) -> list:
    """Generate tags for the article."""
    tags = ["最高人民法院", "入库案例", "人民法院案例库"]

    # Add category-based tag
    if category == "刑事审判":
        tags.append("刑事案例")
    elif category == "知识产权":
        tags.append("知识产权案例")
    elif category == "公司商事与合规":
        tags.append("商事案例")
    else:
        tags.append("民事案例")

    # Add specific topic tags
    topic_keywords = [
        "正当防卫", "劳动争议", "交通事故", "知识产权",
        "不正当竞争", "破产", "侵权", "合同纠纷",
        "婚姻家庭", "继承", "物权", "债权",
        "刑事", "民事", "行政", "执行",
    ]
    for kw in topic_keywords:
        if kw in title or kw in content[:500]:
            if kw not in tags:
                tags.append(kw)

    return tags


def make_wiki_filename(title: str, date: str) -> str:
    """Generate wiki filename from title and date."""
    # Clean title for filename
    clean = title
    # Remove special chars
    clean = re.sub(r'[<>:"/\\|?*]', '', clean)
    # Truncate if too long
    if len(clean) > 60:
        clean = clean[:60]

    date_prefix = date.replace("-", "") if date else "unknown"
    return f"summary_{date_prefix}_最高法_入库案例_{clean}.md"


def process_file(source_path: Path, subcategory: str) -> dict:
    """Process a single source file and return wiki content."""
    try:
        content = source_path.read_text(encoding="utf-8")
    except Exception as e:
        return {"error": f"Read error: {e}"}

    filename = source_path.stem
    date = extract_date(filename)
    title_from_fn = extract_title_from_filename(filename)
    title_from_content = extract_title_from_content(content)

    # Prefer content title, fallback to filename
    title = title_from_content if title_from_content else title_from_fn
    if not title:
        title = filename

    category = classify_article(title, content)
    keywords = extract_keywords(title, content)
    core_points = extract_core_points(content)
    summary = extract_summary(content)
    tags = generate_tags(title, category, content)

    # Build wiki content
    wiki_content = f"""---
title: "{title}"
type: summary
created: 2026-05-27
updated: 2026-05-27
tags: [{', '.join(tags)}]
source: "sources/微信公号资料/最高人民法院/{subcategory}/{source_path.name}"
category: {category}
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{source_path.name}]] |
| 类型 | 最高法微信公号文章·入库案例选介 |
| 发布日期 | {date} |
| 关键词 | {' / '.join(keywords) if keywords else title} |
| 核心要点 | {core_points[:150] if core_points else '见正文摘要'} |

## 正文摘要

{summary if summary else content[:500]}
"""

    wiki_name = make_wiki_filename(title, date)
    return {
        "wiki_name": wiki_name,
        "wiki_content": wiki_content,
        "title": title,
        "date": date,
        "category": category,
    }


def main():
    subcategory = "最高法-入库案例选介-md"
    source_dir = SOURCE_BASE / subcategory

    if not source_dir.exists():
        print(f"ERROR: Source directory not found: {source_dir}")
        sys.exit(1)

    # Get all source files
    source_files = sorted(source_dir.glob("*.md"))
    print(f"Found {len(source_files)} source files in {subcategory}")

    # Check existing wiki files
    existing = set()
    for f in WIKI_SUMMARIES.glob("summary_*最高法*入库案例*.md"):
        existing.add(f.name)

    # Also check for any existing summaries with matching dates
    existing_dates = set()
    for f in WIKI_SUMMARIES.glob("summary_*最高法*入库*.md"):
        existing_dates.add(f.stem)

    print(f"Found {len(existing)} existing wiki summaries for 入库案例")

    processed = 0
    skipped = 0
    errors = []

    for source_path in source_files:
        result = process_file(source_path, subcategory)

        if "error" in result:
            errors.append(f"{source_path.name}: {result['error']}")
            continue

        wiki_path = WIKI_SUMMARIES / result["wiki_name"]

        # Skip if already exists
        if wiki_path.exists():
            skipped += 1
            continue

        # Write wiki file
        try:
            wiki_path.write_text(result["wiki_content"], encoding="utf-8")
            processed += 1
        except Exception as e:
            errors.append(f"{source_path.name}: Write error: {e}")

    print(f"\nResults:")
    print(f"  Processed: {processed}")
    print(f"  Skipped (already exist): {skipped}")
    print(f"  Errors: {len(errors)}")

    if errors:
        print(f"\nErrors:")
        for err in errors[:10]:
            print(f"  - {err}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")

    # Verify
    new_count = len(list(WIKI_SUMMARIES.glob("summary_*最高法*入库案例*.md")))
    print(f"\nVerification: {new_count} total wiki summaries for 入库案例")


if __name__ == "__main__":
    main()
