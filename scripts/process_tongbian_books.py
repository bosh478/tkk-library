#!/usr/bin/env python3
"""
处理《统编教材》法官审判实务系列书籍，按章节生成细化的 concept 页面
"""

import os
import re
from pathlib import Path

BASE_DIR = Path("D:/AI agent/tkk-library")
SOURCES_DIR = BASE_DIR / "sources/《统编教材》法官审判实务"
WIKI_DIR = BASE_DIR / "wiki/concepts"

# 书籍列表和章节信息
BOOKS = {
    "《统编教材》刑事审判实务上册3.md": {
        "book_title": "统编教材·刑事审判实务（上册）",
        "short_name": "刑事审判实务_上册",
        "tags": ["统编教材", "审判实务", "刑事"],
        "chapters": [
            ("刑事法基本原则", "第一编"),
            ("宽严相济刑事政策", "第一编"),
            ("犯罪与刑事责任", "第二编"),
            ("刑罚适用", "第二编"),
            ("危害公共安全罪", "第二编"),
            ("生产、销售伪劣商品犯罪", "第二编"),
            ("走私犯罪", "第二编"),
            ("金融犯罪", "第二编"),
            ("危害税收征管犯罪", "第二编"),
            ("扰乱市场秩序罪", "第二编"),
            ("侵犯公民人身权利罪", "第二编"),
            ("侵犯财产罪", "第二编"),
        ]
    },
    "《统编教材》刑事审判实务下册3.md": {
        "book_title": "统编教材·刑事审判实务（下册）",
        "short_name": "刑事审判实务_下册",
        "tags": ["统编教材", "审判实务", "刑事"],
        "chapters": [
            ("电信网络诈骗相关犯罪", "下册"),
            ("妨害社会管理秩序罪", "下册"),
            ("涉恶犯罪", "下册"),
            ("毒品犯罪", "下册"),
            ("职务犯罪", "下册"),
            ("以审判为中心的刑事诉讼制度", "第三编"),
            ("刑事证据审查与运用", "第三编"),
            ("刑事一审、二审程序", "第三编"),
            ("认罪认罚从宽制度", "第三编"),
        ]
    },
    "《统编教材》审判监督实务上册9.md": {
        "book_title": "统编教材·审判监督实务（上册）",
        "short_name": "审判监督实务_上册",
        "tags": ["统编教材", "审判实务", "审判监督"],
        "chapters": [
            ("审判监督工作的指导思想", "第一章"),
            ("审判监督制度概述", "第二章"),
            ("启动情形", "第三章"),
            ("启动方式", "第四章"),
            ("再审审理程序", "第五章"),
            ("再审庭审", "第六章"),
            ("再审处理", "第七章"),
            ("再审裁判文书", "第八章"),
            ("依法纠正刑事重大冤错案件", "第九章"),
        ]
    },
    "《统编教材》审判监督实务下册9.md": {
        "book_title": "统编教材·审判监督实务（下册）",
        "short_name": "审判监督实务_下册",
        "tags": ["统编教材", "审判实务", "审判监督"],
        "chapters": [
            ("审判监督工作的指导思想", "下册"),
            ("审判监督制度概述", "下册"),
            ("启动情形", "下册"),
            ("启动方式", "下册"),
            ("再审审理程序", "下册"),
            ("再审庭审", "下册"),
            ("再审处理", "下册"),
            ("再审裁判文书", "下册"),
            ("纠正冤错案件", "下册"),
        ]
    },
}

def extract_chapter_content(source_file, chapter_pattern):
    """从源文件中提取指定章节的内容"""
    content = source_file.read_text(encoding='utf-8')
    lines = content.split('\n')

    chapter_content = []
    in_chapter = False
    chapter_num = ""

    for line in lines:
        # 检测章节开始
        if chapter_pattern in line or f"第{chapter_pattern}" in line or chapter_pattern.replace("第", "") in line:
            in_chapter = True
            chapter_num = line.strip()
            chapter_content.append(line)
            continue

        if in_chapter:
            # 遇到下一章或明显的新章节标题时停止
            if re.match(r'^#{1,3}\s*第[一二三四五六七八九十\d]+章', line):
                if chapter_pattern not in line:
                    break
            # 遇到目录标记或明显的目录内容时停止
            if '## 目录' in line or '目 录' in line:
                break
            chapter_content.append(line)

    return '\n'.join(chapter_content)

def create_concept_from_book(book_file, chapter_info):
    """为一个章节创建 concept 页面"""
    book_title = chapter_info["book_title"]
    short_name = chapter_info["short_name"]
    tags = chapter_info["tags"]
    chapter_name = chapter_info["chapters"][0][0] if chapter_info["chapters"] else "概述"

    filename = f"concept_统编教材_{short_name}_{chapter_name}_2025年.md"
    filepath = WIKI_DIR / filename

    # 避免重复创建
    if filepath.exists():
        return None, "already_exists"

    # 生成 frontmatter
    frontmatter = f"""---
title: {book_title}·{chapter_name}
type: concept
created: 2026-04-22
updated: 2026-04-22
tags: {tags}
source: [["《统编教材》{short_name.split('_')[0]}]]
---

# {book_title}·{chapter_name}

## 章节概述

本章节内容源自《统编教材》{book_title}。

"""
    return filepath, frontmatter

def main():
    """主处理函数"""
    created_count = 0
    skipped_count = 0

    for book_file, info in BOOKS.items():
        source_path = SOURCES_DIR / book_file
        if not source_path.exists():
            print(f"源文件不存在: {source_path}")
            continue

        # 读取源文件内容
        content = source_path.read_text(encoding='utf-8')

        for chapter_name, chapter_section in info["chapters"]:
            filename = f"concept_统编教材_{info['short_name']}_{chapter_name}_2025年.md"
            filepath = WIKI_DIR / filename

            if filepath.exists():
                skipped_count += 1
                continue

            # 生成 concept 内容
            concept_content = f"""---
title: {info['book_title']}·{chapter_name}
type: concept
created: 2026-04-22
updated: 2026-04-22
tags: {info['tags']}
source: [["《统编教材》{info['short_name'].split('_')[0]}]]
---

# {info['book_title']}·{chapter_name}

## 章节概述

本章节内容源自《统编教材》{info['book_title']}的{chapter_section}。

"""

            # 从源文件中提取该章节的实际内容
            # 简单搜索章节标题
            lines = content.split('\n')
            in_chapter = False
            chapter_lines = []
            next_chapter_patterns = ['第', '##', '###', '续表', '## 目录']

            for i, line in enumerate(lines):
                if chapter_name in line and (line.startswith('第') or '##' in line[:5]):
                    in_chapter = True
                    chapter_lines.append(line)
                    continue

                if in_chapter:
                    # 检查是否到达下一章节
                    is_new_chapter = False
                    for pattern in next_chapter_patterns:
                        if line.strip().startswith(pattern) and chapter_name not in line:
                            is_new_chapter = True
                            break

                    if is_new_chapter and len(chapter_lines) > 10:
                        break
                    chapter_lines.append(line)

            if len(chapter_lines) > 5:
                # 添加提取的内容
                concept_content += "## 章节内容\n\n"
                concept_content += '\n'.join(chapter_lines[:500])  # 限制长度
                concept_content += "\n\n---\n\n*本页面内容源自《统编教材》法官审判实务系列，由 AI 自动提取整理。*"
            else:
                concept_content += "\n\n> 内容待从源文件中提取补充。\n"

            filepath.write_text(concept_content, encoding='utf-8')
            created_count += 1
            print(f"创建: {filename}")

    print(f"\n处理完成: 创建 {created_count} 个文件, 跳过 {skipped_count} 个已存在文件")

if __name__ == "__main__":
    main()
