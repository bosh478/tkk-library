#!/usr/bin/env python3
"""Batch ingest for 纪委监委案件 directory"""
import json
import re
from pathlib import Path
import os
from datetime import date

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
SRC_DIR = VAULT_ROOT / "sources/纪委监委案件"
OUT_DIR = VAULT_ROOT / "wiki/summaries"

# Mapping table: source file -> (target_name, category, author, publisher, year)
FILE_CONFIG = {
    "《审查调查六项核心技能》李剑平 法律 2026年.md": {
        "title": "审查调查六项核心技能",
        "category": "刑事参考",
        "author": "李剑平",
        "publisher": "法律出版社",
        "year": "2026",
        "tags": ["纪检监察", "审查调查", "职务犯罪", "技能培训"]
    },
    "《新型隐性受贿犯罪实务疑难解析》万龙 中国检察 2025年.md": {
        "title": "新型隐性受贿犯罪实务疑难解析",
        "category": "刑事参考",
        "author": "万龙",
        "publisher": "中国检察出版社",
        "year": "2025",
        "tags": ["受贿罪", "新型腐败", "隐性腐败", "职务犯罪", "实务解析"]
    },
    "关于办理贪污贿赂刑事案件适用法律若干问题的解释(二) 疑难问题与案例指导 王晓东 法律 2026年.md": {
        "title": "贪污贿赂刑事案件解释(二)疑难问题与案例指导",
        "category": "刑事参考",
        "author": "王晓东",
        "publisher": "法律出版社",
        "year": "2026",
        "tags": ["贪污罪", "受贿罪", "挪用公款罪", "司法解释", "案例指导"]
    },
    "职务犯罪审判指导/2022《职务犯罪审判指导》第1辑 最高法刑二庭 法制 2022年.md": {
        "title": "职务犯罪审判指导（第1辑）",
        "category": "刑事参考",
        "author": "最高法刑二庭",
        "publisher": "法制出版社",
        "year": "2022",
        "tags": ["职务犯罪", "审判指导", "受贿罪", "贪污罪", "案例分析"]
    },
    "职务犯罪审判指导/2023《职务犯罪审判指导》第2辑 最高法刑二庭 法制 2023年.md": {
        "title": "职务犯罪审判指导（第2辑）",
        "category": "刑事参考",
        "author": "最高法刑二庭",
        "publisher": "法制出版社",
        "year": "2023",
        "tags": ["职务犯罪", "审判指导", "受贿罪", "贪污罪", "案例分析"]
    },
    "职务犯罪审判指导/2024《职务犯罪审判指导》第3辑 最高法刑二庭 法制 2024年.md": {
        "title": "职务犯罪审判指导（第3辑）",
        "category": "刑事参考",
        "author": "最高法刑二庭",
        "publisher": "法制出版社",
        "year": "2024",
        "tags": ["职务犯罪", "审判指导", "受贿罪", "贪污罪", "案例分析"]
    },
    "职务犯罪审判指导/2025《职务犯罪审判指导》第4辑 最高法刑二庭 法制 2025年.md": {
        "title": "职务犯罪审判指导（第4辑）",
        "category": "刑事参考",
        "author": "最高法刑二庭",
        "publisher": "法制出版社",
        "year": "2025",
        "tags": ["职务犯罪", "审判指导", "受贿罪", "贪污罪", "案例分析"]
    }
}

def extract_frontmatter(content):
    """Extract key info from source file"""
    lines = content.split('\n')
    result = {
        "description": "",
        "has_toc": False,
        "chapter_count": 0
    }

    # Check for TOC
    for line in lines[:100]:
        if '目录' in line or 'CONTENTS' in line.upper():
            result["has_toc"] = True
            break

    # Count chapters (lines starting with numbers or 第X章)
    chapter_pattern = re.compile(r'^(第[一二三四五六七八九十百千\d]+[章节篇部]|[0-9]+[.．])')
    for line in lines:
        if chapter_pattern.match(line.strip()):
            result["chapter_count"] += 1

    # Get first substantial paragraph (skip CIP/table of contents)
    in_content = False
    paragraphs = []
    for line in lines:
        if len(line.strip()) > 50 and not line.strip().startswith('#') and not line.startswith('|'):
            paragraphs.append(line.strip()[:200])
            if len(paragraphs) >= 3:
                break

    result["description"] = ' '.join(paragraphs)[:300] if paragraphs else ""
    return result

def process_file(src_path, config):
    """Process a single source file"""
    content = src_path.read_text(encoding='utf-8', errors='ignore')

    # Get file stats
    size_kb = len(content) // 1024
    lines = content.count('\n')

    # Extract info
    info = extract_frontmatter(content)

    # Generate summary content
    # Take first 3000 chars of meaningful content
    body_start = content.find('## ')
    if body_start == -1:
        body_start = content.find('\n\n')
    if body_start == -1:
        body_start = 0

    body = content[body_start:body_start+3000].strip()

    # Create frontmatter
    frontmatter = f"""---
title: {config['title']}
type: summary
created: {str(date.today())}
updated: {str(date.today())}
tags: {json.dumps(config['tags'], ensure_ascii=False)}
source: sources/纪委监委案件/{src_path.relative_to(SRC_DIR).as_posix()}
category: {config['category']}
author: {config['author']}
publisher: {config['publisher']}
year: {config['year']}
source_size: {size_kb}KB
source_lines: {lines}
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | {src_path.name} |
| 类型 | 纪检监察/职务犯罪实务指引 |
| 发布日期 | {config['year']}年 |
| 作者 | {config['author']} |
| 出版社 | {config['publisher']} |
| 文件大小 | {size_kb}KB |
| 关键词 | {' / '.join(config['tags'])} |

## ❓ 核心问题意识

本资料聚焦职务犯罪审查调查与审判实践，重点解决：
- 新型隐性受贿犯罪的认定难题
- 审查调查六项核心技能（记/调/读/谈/算/写）
- 贪污贿赂刑事案件法律适用问题

## 📖 内容摘要

{body[:1500]}...

## 补充说明

- 章节数：约 {info['chapter_count']} 章
- 包含目录：{'是' if info['has_toc'] else '否'}
- 关键词：{info['description'][:200] if info['description'] else '见tags'}

## 相关法律依据

- 《刑法》第八章（贪污贿赂罪）
- 《监察法》
- 《刑事诉讼法》
- 最高法、最高检相关司法解释

## 相关概念

- [[受贿罪]]
- [[贪污罪]]
- [[挪用公款罪]]
- [[职务侵占罪]]
- [[巨额财产来源不明罪]]
"""

    return frontmatter, len(content)

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    for rel_path, config in FILE_CONFIG.items():
        src_path = SRC_DIR / rel_path
        if not src_path.exists():
            print(f"[MISS] {rel_path}")
            continue

        try:
            content, size = process_file(src_path, config)

            # Generate output filename
            safe_name = config['title'].replace(' ', '_').replace('（', '').replace('）', '')
            out_path = OUT_DIR / f"summary_{safe_name}_{config['year']}.md"

            out_path.write_text(content, encoding='utf-8')
            results.append(f"[OK] {out_path.name} ({size//1024}KB)")

        except Exception as e:
            results.append(f"[FAIL] {rel_path}: {e}")

    print("\n=== JJWJ Case Ingest Done ===")
    print(f"Processed: {len(results)} files")
    for r in results:
        print(f"  {r}")

if __name__ == "__main__":
    main()