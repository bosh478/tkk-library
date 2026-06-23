# -*- coding: utf-8 -*-
import os
import re
from pathlib import Path

source_dir = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-高质效办好每一个案件-md/")
target_dir = Path("D:/AI agent/tkk-library/wiki/summaries/")

target_dir.mkdir(parents=True, exist_ok=True)

files = sorted(source_dir.glob("*.md"))
print(f"Total files to process: {len(files)}")

for idx, f in enumerate(files, 1):
    # Read source file
    content = f.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Extract title from first # line
    title = ""
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            # Remove # and extra spaces
            title = re.sub(r'^#+\s*', '', line)
            break

    if not title:
        title = f.stem

    # Clean title: remove date prefix like [YYYY-MM-DD]
    clean_title = re.sub(r'^\[\d{4}-\d{2}-\d{2}\]\s*', '', title)

    # Create filename
    filename = f"summary_SPP_高质效办好每一个案件_{clean_title}.md"
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)  # Sanitize filename
    target_path = target_dir / filename

    # Extract tags from content
    tags = ["高质效办案", "检察实务"]

    # Extract keywords from content for additional tags
    content_lower = content.lower()
    if "民事" in content:
        tags.append("民事检察")
    if "刑事" in content:
        tags.append("刑事检察")
    if "公益诉讼" in content:
        tags.append("公益诉讼")
    if "认罪认罚" in content:
        tags.append("认罪认罚")
    if "少捕慎诉" in content:
        tags.append("少捕慎诉")
    if "侦查监督" in content:
        tags.append("侦查监督")
    if "公开听证" in content:
        tags.append("公开听证")
    if "数字检察" in content:
        tags.append("数字检察")

    # Extract frontmatter fields
    # author/来源信息
    author = ""
    source_match = re.search(r'作者[为：:]\s*([^摘\n]+)', content)
    if source_match:
        author = source_match.group(1).strip()

    # Extract key content for body
    # Remove front matter, navigation, source links
    body_lines = []
    capture = False
    for line in lines:
        if line.strip().startswith('**') and len(line.strip()) > 4:
            capture = True
        if capture and not line.strip().startswith('[阅读原文') and '预览时标签不可点' not in line:
            clean_line = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', line)  # Remove links
            clean_line = clean_line.strip()
            if clean_line and clean_line != '__':
                body_lines.append(clean_line)

    body = '\n\n'.join(body_lines[:50])  # Limit to first 50 significant lines

    # Create frontmatter
    frontmatter = f"""---
title: {clean_title}
type: summary
category: 刑事参考
created: 2026-05-11
updated: 2026-05-11
tags: {tags}
source: [[{f.name}]]
related: [["高质效办好每一个案件"概念页]]
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{f.name}]] |
| 类型 | 检察实务文章 |
| 发布日期 | {f.stem[:10] if f.stem[0] == '[' else '2023'} |
| 关键词 | {", ".join(tags)} |

## 核心内容

{body[:3000] if len(body) > 3000 else body}

## 实践启示

（详见原文）

---
*本摘要由AI自动生成，原始文件：{f.name}*
"""

    # Write file
    target_path.write_text(frontmatter, encoding='utf-8')

    if idx % 20 == 0:
        print(f"Processed {idx}/{len(files)}: {filename[:50]}...")

print(f"\nDone! Processed {len(files)} files")
print(f"Output directory: {target_dir}")