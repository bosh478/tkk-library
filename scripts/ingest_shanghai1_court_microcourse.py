#!/usr/bin/env python3
"""Batch ingest 上海一中法院微课程 141 files to wiki/summaries/"""

import re
import os
from pathlib import Path

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/上海一中法院/上海一中法院-微课程-md")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/summaries")
TARGET_DIR.mkdir(parents=True, exist_ok=True)

# Get all source files
source_files = sorted(SOURCE_DIR.glob("*.md"))
print(f"Found {len(source_files)} source files")

processed = 0
errors = []

def extract_title(content_lines):
    """Extract title from first # line."""
    for line in content_lines:
        line = line.strip()
        if line.startswith("# "):
            # Remove # prefix
            title = line[1:].strip()
            # Remove date prefix [YYYY-MM-DD]
            title = re.sub(r'^\[\d{4}-\d{2}-\d{2}\]', '', title).strip()
            # Remove trailing | 微课程 or 微课程
            title = re.sub(r'\s*[\丨|:]\s*微课程\s*$', '', title).strip()
            return title
    return None

def extract_speaker(content_lines):
    """Extract speaker info from 本期主讲 or similar."""
    for i, line in enumerate(content_lines):
        if "本期主讲" in line or "对谈人" in line or "主讲" in line:
            # Collect next few lines for speaker info
            speaker_lines = []
            for j in range(i, min(i+10, len(content_lines))):
                l = content_lines[j].strip()
                if l and not l.startswith("**") and not l.startswith("课程") and not l.startswith("["):
                    speaker_lines.append(l)
                if l.startswith("**") and len(speaker_lines) > 0:
                    break
            if speaker_lines:
                return " ".join(speaker_lines[:3])
    return None

def extract_core_content(content_lines):
    """Extract substantive content paragraphs."""
    content = []
    skip_patterns = [
        r"^#\s", r"^\*\*编者按", r"^\*\*本期", r"^\*\*课程",
        r"^课程\s+\|\s+视频", r"^课程\s+\|\s+音频", r"^课程\s+\|\s+内容",
        r"^\*\*对谈人", r"^\*\*微课程", r"^\*\*课\s*程",
        r"^文字部分系根据", r"^大家好", r"^点击", r"^\[阅读原文\]",
        r"^预览时标签", r"^修改于", r"^__+$", r"^\*\*要点\d",
        r"^\*\*PROFILE",
    ]

    for line in content_lines:
        line = line.strip()
        # Skip empty lines
        if not line:
            continue
        # Skip lines matching skip patterns
        skip = False
        for pattern in skip_patterns:
            if re.match(pattern, line):
                skip = True
                break
        if skip:
            continue
        # Skip lines that are just formatting markers
        if line in ["**", "●", "___"]:
            continue
        # Keep substantive content
        content.append(line)

    return "\n".join(content[:80])  # Limit to first 80 lines

def generate_frontmatter(title, speaker, source_filename, content_preview):
    """Generate frontmatter for wiki page."""
    # Determine tags based on content
    tags = ["微课程", "法律知识", "上海一中法院"]

    # Add topic-specific tags
    if any(k in title for k in ["刑事", "犯罪", "定罪", "量刑", "诈骗", "非法集资", "洗钱", "贿赂", "盗窃", "抢劫"]):
        tags.append("刑事法律")
    elif any(k in title for k in ["合同", "担保", "债权", "违约", "租赁", "买卖"]):
        tags.append("合同法律")
    elif any(k in title for k in ["劳动", "劳动合同", "工伤", "辞退", "竞业限制", "年终奖", "加班"]):
        tags.append("劳动法律")
    elif any(k in title for k in ["公司", "股东", "股权", "出资", "清算", "法人"]):
        tags.append("公司法")
    elif any(k in title for k in ["侵权", "名誉", "人格权", "高空抛物", "消费者"]):
        tags.append("侵权责任")
    elif any(k in title for k in ["执行", "拍卖", "拒执"]):
        tags.append("执行程序")
    elif any(k in title for k in ["行政", "处罚", "政府信息"]):
        tags.append("行政法律")
    elif any(k in title for k in ["仲裁", "管辖", "撤销仲裁"]):
        tags.append("仲裁程序")
    else:
        tags.append("民事法律")

    # Add round table tag
    if "对谈" in title:
        tags.append("圆桌对谈")

    tags_str = ", ".join(f"'{t}'" for t in tags)

    fm = f"""---
title: {title}
type: summary
category: 诉讼与仲裁
created: 2026-05-11
updated: 2026-05-11
tags: [{tags_str}]
source: [[上海一中法院-微课程-md/{source_filename}]]
related: []
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[上海一中法院-微课程-md/{source_filename}]] |
| 类型 | 微课程 |
| 主题 | {title} |
| 机构 | 上海市第一中级人民法院 |
| 关键词 | {", ".join(tags)} |

## 核心内容

{content_preview[:3000]}

## 相关

- [[index|返回 index]]
"""
    return fm

for sf in source_files:
    try:
        content = sf.read_text(encoding="utf-8")
        content_lines = content.split("\n")

        # Extract title
        title = extract_title(content_lines)
        if not title:
            print(f"WARNING: Could not extract title from {sf.name}")
            title = sf.stem

        # Extract speaker
        speaker = extract_speaker(content_lines)

        # Extract core content
        core_content = extract_core_content(content_lines)

        # Generate output filename
        # Remove date prefix from filename
        clean_title = re.sub(r'^\[\d{4}-\d{2}-\d{2}\]', '', sf.stem)
        clean_title = re.sub(r'微课程$', '', clean_title).strip()
        # Remove trailing 丨 if present
        clean_title = re.sub(r'丨$', '', clean_title).strip()
        output_name = f"summary_Court_上海一中院_微课程_{clean_title}.md"
        output_path = TARGET_DIR / output_name

        # Generate frontmatter
        frontmatter = generate_frontmatter(title, speaker, sf.name, core_content)

        # Write file
        output_path.write_text(frontmatter, encoding="utf-8")
        processed += 1

        if processed % 20 == 0:
            print(f"Processed {processed}/141 files...")

    except Exception as e:
        errors.append((sf.name, str(e)))
        print(f"ERROR processing {sf.name}: {e}")

print(f"\nCompleted: {processed}/141 files")
if errors:
    print(f"Errors: {len(errors)}")
    for fn, err in errors[:5]:
        print(f"  {fn}: {err}")
