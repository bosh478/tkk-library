#!/usr/bin/env python3
"""
Batch ingest for 最高检-高质效办案在基层-md (56 files)
Processes source files to wiki/summaries/ with naming pattern summary_SPP_高质效办案在基层_*.md
"""

import os
import re
from pathlib import Path

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
SOURCE_DIR = VAULT_ROOT / "sources/微信公号资料/最高人民检察院/最高检-高质效办案在基层-md"
TARGET_DIR = VAULT_ROOT / "wiki/summaries"

def extract_title(content):
    """Extract title from first # line"""
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            # Remove bold markers ** and strip
            title = line[2:].strip()
            title = re.sub(r'\*\*', '', title)
            return title
    return None

def strip_date_prefix(filename):
    """Remove [YYYY-MM-DD] prefix from filename"""
    return re.sub(r'^\[\d{4}-\d{2}-\d{2}\]', '', filename).strip()

def create_summary(source_file, target_file):
    """Create a summary wiki page from source file"""
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    title = extract_title(content)
    if not title:
        print(f"  [WARN] Could not extract title from {source_file.name}")
        title = source_file.stem

    # Generate frontmatter
    date_str = "2026-05-11"

    # Determine tags based on content analysis
    tags = ["高质效办案", "基层检察", "检察实务"]

    # Determine related links based on topic
    related = []
    if "检察护企" in content or "企业" in content:
        related.append("[[concept_检察护企专项行动]]")
    if "知识产权" in content:
        related.append("[[concept_知识产权综合履职]]")
    if "数字检察" in content or "数智" in content:
        related.append("[[concept_数字检察]]")
    if "公益诉讼" in content:
        related.append("[[concept_公益诉讼检察]]")
    if "未成年人" in content:
        related.append("[[concept_未成年人检察]]")

    # If no specific matches, use a general link
    if not related:
        related = ["[[concept_检察工作现代化]]"]

    # Build content sections
    sections = []
    lines = content.split('\n')

    current_section = None
    current_content = []

    for line in lines:
        if line.startswith('**') and line.endswith('**'):
            # Section header
            if current_section and current_content:
                sections.append((current_section, current_content))
            current_section = line.strip('*').strip()
            current_content = []
        elif line.startswith('#'):
            # Skip title line
            continue
        elif line.startswith('来源：') or line.startswith('记者：') or line.startswith('编辑：'):
            # Skip metadata
            continue
        elif line.startswith('预览时标签不可点') or line.startswith('[ 阅读原文 ]'):
            continue
        elif line.strip() == '__':
            continue
        elif current_section:
            line = line.strip()
            if line:
                current_content.append(line)

    if current_section and current_content:
        sections.append((current_section, current_content))

    # Build markdown content
    markdown_parts = []
    markdown_parts.append("## 核心内容\n")

    for section_name, section_lines in sections:
        markdown_parts.append(f"### {section_name}\n")
        for line in section_lines[:8]:  # Limit to first 8 lines per section
            markdown_parts.append(f"{line}\n\n")

    # Extract key takeaways
    key_points = []
    if "创新" in content:
        key_points.append("以创新驱动检察工作发展")
    if "服务" in content and "企业" in content:
        key_points.append("服务企业高质量发展")
    if "保护" in content:
        key_points.append("强化司法保护职能")
    if "治理" in content:
        key_points.append("推动社会治理现代化")

    if key_points:
        markdown_parts.append("## 实践启示\n")
        for point in key_points[:4]:
            markdown_parts.append(f"- {point}\n")

    full_content = ''.join(markdown_parts)

    # Create frontmatter
    frontmatter = f"""---
title: {title}
type: summary
published: {date_str[:10]}
created: {date_str}
updated: {date_str}
tags: {tags}
category: 刑事参考
source: "sources/微信公号资料/最高人民检察院/最高检-高质效办案在基层-md/{source_file.name}"
related: {related}
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{source_file.name}]] |
| 类型 | 检察实务报道 |
| 发布日期 | {date_str[:10]} |
| 关键词 | 高质效办案 / 基层检察 / 检察实务 |
| 核心要点 | 各地检察机关高质效办案经验与创新实践 |

{full_content}
"""

    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(frontmatter)

    return True

def main():
    # Get all source files
    source_files = list(SOURCE_DIR.glob("*.md"))
    source_count = len(source_files)
    print(f"Source files found: {source_count}")

    if source_count == 0:
        print("No source files found!")
        return

    # Ensure target directory exists
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    # Process each file
    success_count = 0
    fail_count = 0

    for i, source_file in enumerate(sorted(source_files), 1):
        # Generate target filename
        filename_no_ext = source_file.stem
        date_stripped = strip_date_prefix(filename_no_ext)
        target_name = f"summary_SPP_高质效办案在基层_{date_stripped}.md"
        target_file = TARGET_DIR / target_name

        print(f"[{i}/{source_count}] Processing: {source_file.name}")
        print(f"  -> Target: {target_name}")

        try:
            create_summary(source_file, target_file)
            success_count += 1
            print(f"  [OK] Created {target_name}")
        except Exception as e:
            fail_count += 1
            print(f"  [FAIL] {e}")

    print(f"\n=== Summary ===")
    print(f"Total: {source_count}")
    print(f"Success: {success_count}")
    print(f"Failed: {fail_count}")

if __name__ == "__main__":
    main()