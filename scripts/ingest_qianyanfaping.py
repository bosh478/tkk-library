#!/usr/bin/env python3
"""批量处理最高法-前沿法评文章"""

import os
import re
from pathlib import Path

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民法院/最高法-前沿法评-md")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/summaries")

def extract_title(content):
    """从 # 标题行提取文章标题"""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        # 去除可能的前缀空格
        title = re.sub(r'^\s+', '', title)
        return title
    return None

def extract_main_content(content):
    """提取正文内容（去除开栏的话、编者按、来源信息等）"""
    lines = content.split('\n')

    # 跳过开栏的话、编者按等开头部分，找到正文开始
    main_content_lines = []
    skip_patterns = [
        r'^\*\*\s*开栏的话\s*\*\*',
        r'^\*\*\s*编者按\s*\*\*',
        r'^#\s+',  # 标题行
        r'^来源：',
        r'^作者[：:]',
        r'^责任编辑',
        r'^联系电话',
        r'^电子信箱',
        r'^新媒体编辑',
        r'^预览时标签不可点',
        r'^__+$',
    ]

    capture = False
    for i, line in enumerate(lines):
        # 检查是否是标题行（正文标题，通常在编者按之后）
        if re.match(r'^#\s+[一-龥]', line):
            # 这是主要标题行，跳过（已经在标题中提取）
            continue

        # 遇到来源信息开始跳过
        if re.match(r'^来源：', line):
            break

        # 跳过开头部分
        if not capture:
            if any(re.search(p, line) for p in skip_patterns):
                # 检查是否是标题行后面跟着编者按
                if i > 0 and re.match(r'^\*\*\s*编者按\s*\*\*', line):
                    # 找到编者按，继续找正文开始
                    continue
                continue
            # 如果不是特殊标记，可能是正文开始
            if line.strip() and not line.startswith('**'):
                capture = True
                main_content_lines.append(line)
        else:
            main_content_lines.append(line)

    return '\n'.join(main_content_lines).strip()

def extract_keywords(title, content):
    """从标题和内容中提取关键词"""
    # 基于标题提取
    tags = []

    # 常见主题词
    topic_words = [
        '民法典', '合同编', '债法', '反不正当竞争法', '数字改革', '审判工作',
        '人工智能', '司法', '劳动法', '仲裁', '企业破产法', '知识产权',
        '环境资源', '民营经济', '刑事', '行政', '执行', '司法公正',
        '生态', '一带一路', '涉外法治', '国际商事', '个人信息', '数据',
        '竞争法', '平台经济', '营商环境', '法治宣传教育', '东京审判'
    ]

    text = title + content
    for tw in topic_words:
        if tw in text:
            tags.append(tw)

    # 去除重复
    tags = list(set(tags))
    if len(tags) > 8:
        tags = tags[:8]

    return tags

def generate_frontmatter(title, source_file, tags):
    """生成 frontmatter"""
    return f"""---
title: {title}
type: summary
category: 诉讼与仲裁
created: 2026-05-11
updated: 2026-05-11
tags: [{', '.join(tags)}]
source: "sources/微信公号资料/最高人民法院/最高法-前沿法评-md/{source_file}"
related: []
---"""

def process_file(source_path):
    """处理单个文件"""
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取标题
    title = extract_title(content)
    if not title:
        print(f"无法提取标题: {source_path}")
        return None

    # 生成目标文件名
    source_name = source_path.name
    # 去除日期前缀 [YYYY-MM-DD]
    clean_name = re.sub(r'^\[\d{4}-\d{2}-\d{2}\]', '', source_name)
    target_name = f"summary_CourtFa_最高法_前沿法评_{clean_name}"
    target_path = TARGET_DIR / target_name

    # 提取正文
    main_content = extract_main_content(content)

    # 提取关键词
    tags = extract_keywords(title, main_content)
    # 确保有基础标签
    if '前沿法评' not in tags:
        tags.insert(0, '前沿法评')
    if '最高人民法院' not in tags:
        tags.insert(0, '最高人民法院')

    # 生成 frontmatter
    frontmatter = generate_frontmatter(title, source_name, tags)

    # 组装完整内容
    full_content = frontmatter + "\n\n## 📋 文档概览\n\n"
    full_content += f"| 字段 | 内容 |\n|------|------|\n"
    full_content += f"| 来源 | [[{source_name}]] |\n"
    full_content += f"| 类型 | 前沿法评（法学研究） |\n"
    full_content += f"| 关键词 | {' / '.join(tags)} |\n\n"
    full_content += "## 核心观点\n\n"
    full_content += main_content + "\n"

    # 写入文件
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(full_content)

    return target_name

def main():
    # 获取所有源文件
    source_files = list(SOURCE_DIR.glob("*.md"))
    print(f"找到 {len(source_files)} 个源文件")

    # 批量处理
    success_count = 0
    for i, source_file in enumerate(source_files, 1):
        result = process_file(source_file)
        if result:
            print(f"[{i}/{len(source_files)}] 处理完成: {result}")
            success_count += 1
        else:
            print(f"[{i}/{len(source_files)}] 处理失败: {source_file.name}")

    print(f"\n处理完成: {success_count}/{len(source_files)} 成功")

if __name__ == "__main__":
    main()
