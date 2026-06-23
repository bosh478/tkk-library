#!/usr/bin/env python3
"""Batch ingest: 上海二中院 WeChat articles -> wiki/summaries/"""

import re
import os
from pathlib import Path

VAULT = Path(r"D:\AI agent\tkk-library")
SOURCE_ROOT = VAULT / "sources" / "微信公号资料" / "上海二中院"
WIKI_SUMMARIES = VAULT / "wiki" / "summaries"

SUBDIRS = [
    "上海二中院-至正法官札记-md",
    "上海二中院-至正开放麦-md",
    "上海二中院-至正法律研究-md",
]

DATE_RE = re.compile(r"\[(\d{4}-\d{2}-\d{2})\]")
TITLE_RE = re.compile(r"^#\s+(.+)", re.MULTILINE)

# Category mapping by subdirectory
CATEGORY_MAP = {
    "至正法官札记": "诉讼与仲裁",
    "至正开放麦": "公司商事与合规",
    "至正法律研究": "诉讼与仲裁",
}

# Tag mapping by subdirectory
TAG_MAP = {
    "至正法官札记": ["上海二中院", "法官札记", "案例分析"],
    "至正开放麦": ["上海二中院", "至正开放麦", "法律观点"],
    "至正法律研究": ["上海二中院", "至正法律研究", "法律解读"],
}

TODAY = "2026-05-27"


def extract_date(filename: str) -> str:
    m = DATE_RE.search(filename)
    return m.group(1) if m else ""


def extract_title(content: str) -> str:
    m = TITLE_RE.search(content)
    if m:
        title = m.group(1).strip()
        # Clean up common suffixes
        for sep in ["|", "｜"]:
            if sep in title:
                title = title.split(sep)[0].strip()
        return title
    return ""


def extract_summary(content: str, max_len: int = 400) -> str:
    """Extract key content after the title for the summary."""
    lines = content.split("\n")
    body_lines = []
    for line in lines[1:]:  # skip title
        line = line.strip()
        if not line:
            continue
        # Skip metadata-like lines
        if line.startswith("本期主笔") or line.startswith("责任编辑"):
            continue
        if line.startswith("版面编辑") or line.startswith("视频"):
            continue
        if line.startswith("[") and line.endswith(")"):
            continue
        if line == "END" or line == "action" or line == "开机":
            continue
        if "预览时标签不可点" in line:
            continue
        if "修改于" in line:
            continue
        if "__" == line:
            continue
        # Strip markdown bold markers
        clean = line.replace("**", "").strip()
        if len(clean) > 2:
            body_lines.append(clean)
        if len("".join(body_lines)) > max_len:
            break
    result = "".join(body_lines)
    if len(result) > max_len:
        result = result[:max_len] + "..."
    return result


def extract_key_points(content: str) -> str:
    """Extract 2-3 key points from the content."""
    lines = content.split("\n")
    points = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        clean = line.replace("**", "").strip()
        # Look for key legal conclusions or points
        if any(kw in clean for kw in ["法院认为", "法官认为", "应当", "可以", "不能", "答案是", "需要注意", "提醒", "建议", "认定"]):
            if len(clean) > 10 and len(clean) < 150:
                points.append(clean)
        if len(points) >= 3:
            break
    if not points:
        # Fallback: take first meaningful paragraph
        for line in lines[1:]:
            line = line.strip().replace("**", "").strip()
            if len(line) > 20 and len(line) < 150:
                points.append(line)
                break
    return "；".join(points[:3]) if points else "详见正文"


def guess_keywords(content: str, subdir_name: str) -> str:
    """Extract keywords from content."""
    kw_set = set()
    keyword_patterns = [
        "民法典", "刑法", "公司法", "合同法", "婚姻法", "继承法",
        "民事诉讼", "刑事诉讼", "行政诉讼", "仲裁",
        "股东", "股权", "借款", "担保", "抵押", "租赁",
        "离婚", "抚养", "赡养", "遗产", "遗嘱",
        "侵权", "交通事故", "劳动", "工伤",
        "证据", "举证", "自认", "鉴定",
        "买卖合同", "租赁合同", "借款合同", "担保合同",
        "知识产权", "商标", "专利", "著作权",
        "房产", "房屋", "土地", "拆迁",
        "诈骗", "盗窃", "故意伤害", "交通肇事",
    ]
    for kw in keyword_patterns:
        if kw in content:
            kw_set.add(kw)
    return " / ".join(list(kw_set)[:5]) if kw_set else "法律实务"


def make_wiki_filename(title: str, date: str) -> str:
    """Generate wiki filename from title and date."""
    # Clean title for filename
    clean = title.replace("/", "-").replace("\\", "-").replace(":", "-")
    clean = clean.replace("*", "").replace("?", "？").replace('"', "")
    clean = clean.replace("<", "").replace(">", "").replace("|", "-")
    # Truncate if too long
    if len(clean) > 60:
        clean = clean[:60]
    return f"summary_上海二中_{clean}.md"


def build_wiki_page(title: str, date: str, content: str, source_rel: str, subdir_name: str) -> str:
    """Build the wiki summary page."""
    # Determine category and tags
    category = "诉讼与仲裁"
    tags = ["上海二中院", "法律实务"]
    for key, cat in CATEGORY_MAP.items():
        if key in subdir_name:
            category = cat
            break
    for key, t in TAG_MAP.items():
        if key in subdir_name:
            tags = t
            break

    summary = extract_summary(content)
    key_points = extract_key_points(content)
    keywords = guess_keywords(content, subdir_name)

    # Build page
    lines = [
        "---",
        f"title: {title}",
        "type: summary",
        f"created: {TODAY}",
        f"updated: {TODAY}",
        f"tags: [{', '.join(tags)}]",
        f'source: "{source_rel}"',
        f"category: {category}",
        "---",
        "",
        "## 📋 文档概览",
        "",
        "| 字段 | 内容 |",
        "|------|------|",
        f"| 来源 | [[{os.path.basename(source_rel)}]] |",
        "| 类型 | 上海二中院微信文章 |",
        f"| 发布日期 | {date} |",
        f"| 关键词 | {keywords} |",
        f"| 核心要点 | {key_points} |",
        "",
        "## 正文摘要",
        "",
        summary,
        "",
    ]
    return "\n".join(lines)


def main():
    total = 0
    created = 0
    skipped = 0
    errors = []

    for subdir in SUBDIRS:
        subdir_path = SOURCE_ROOT / subdir
        if not subdir_path.exists():
            print(f"[WARN] Subdirectory not found: {subdir_path}")
            continue

        # Get only .md files (exclude .cfg etc.)
        md_files = sorted(subdir_path.glob("*.md"))
        print(f"\n=== Processing {subdir} ({len(md_files)} files) ===")

        for src_file in md_files:
            total += 1
            try:
                content = src_file.read_text(encoding="utf-8", errors="replace")
                title = extract_title(content)
                if not title:
                    title = src_file.stem
                    # Remove date prefix
                    title = DATE_RE.sub("", title).strip()

                date = extract_date(src_file.stem)

                # Build source relative path
                source_rel = f"sources/微信公号资料/上海二中院/{subdir}/{src_file.name}"

                # Generate wiki filename
                wiki_name = make_wiki_filename(title, date)
                wiki_path = WIKI_SUMMARIES / wiki_name

                # Skip if already exists
                if wiki_path.exists():
                    skipped += 1
                    continue

                # Build and write page
                page = build_wiki_page(title, date, content, source_rel, subdir)
                wiki_path.write_text(page, encoding="utf-8")
                created += 1

            except Exception as e:
                errors.append(f"{src_file.name}: {e}")
                print(f"  [ERROR] {src_file.name}: {e}")

        print(f"  Done with {subdir}")

    print(f"\n=== SUMMARY ===")
    print(f"Total files scanned: {total}")
    print(f"Created: {created}")
    print(f"Skipped (existing): {skipped}")
    print(f"Errors: {len(errors)}")
    if errors:
        print("Error details:")
        for e in errors:
            print(f"  {e}")


if __name__ == "__main__":
    main()
