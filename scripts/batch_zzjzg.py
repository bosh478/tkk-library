#!/usr/bin/env python3
"""批量处理至正法官札记文件，生成wiki/summaries页面"""

import re
import os
from pathlib import Path

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/上海二中院/上海二中院-至正法官札记-md/")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/summaries/")

def extract_title(content):
    """从第一行提取标题，去除日期前缀和札记编号"""
    match = re.search(r'#\s+(.+?)\s*\|', content)
    if match:
        title = match.group(1).strip()
        # 去除可能的日期前缀 [YYYY-MM-DD]
        title = re.sub(r'^\[[\d-]+\]\s*', '', title)
        return title
    return None

def extract_author(content):
    """提取主笔信息"""
    match = re.search(r'本期主笔[：:](.+)', content)
    if match:
        author_line = match.group(1).strip()
        # 提取第一行（姓名）作为主笔
        author = author_line.split('\n')[0].strip()
        return author
    return None

def extract_date_from_filename(filename):
    """从文件名提取日期"""
    match = re.search(r'\[(\d{4}-\d{2}-\d{2})\]', filename)
    if match:
        return match.group(1)
    return None

def extract_tags(content):
    """根据内容提取标签"""
    tags = ["至正法官札记", "上海二中法院"]
    text_lower = content.lower()
    if any(k in text_lower for k in ['离婚', '抚养', '探望', '婚姻']):
        tags.append("婚姻家庭")
    if any(k in text_lower for k in ['买房', '房产', '房屋', '租赁']):
        tags.append("房产纠纷")
    if any(k in text_lower for k in ['合同', '违约', '转让']):
        tags.append("合同纠纷")
    if any(k in text_lower for k in ['劳动', '工伤', '社保']):
        tags.append("劳动争议")
    if any(k in text_lower for k in ['投资', '理财', '金融']):
        tags.append("金融投资")
    if any(k in text_lower for k in ['刑事', '犯罪', '盗窃', '抢劫']):
        tags.append("刑事案件")
    if any(k in text_lower for k in ['公司', '股权', '合伙']):
        tags.append("公司股权")
    if any(k in text_lower for k in ['侵权', '赔偿', '损失']):
        tags.append("侵权赔偿")
    return tags

def extract_summary(content):
    """提取核心内容摘要"""
    # 去除第一行的标题
    lines = content.split('\n')
    summary_lines = []
    in_main_content = False
    for i, line in enumerate(lines):
        if i == 0:
            continue  # 跳过标题行
        if '本期主笔' in line:
            in_main_content = True
            continue
        if in_main_content and line.strip() and not line.startswith('**') and len(line.strip()) > 10:
            # 获取前面几个段落的正文
            pass

    # 提取粗体段落作为核心内容
    bold_paragraphs = re.findall(r'\*\*([^*]+)\*\*', content)
    if bold_paragraphs:
        # 取前3个粗体段落作为摘要
        summary = ' '.join(bold_paragraphs[:3])
        if len(summary) > 300:
            summary = summary[:300] + '...'
        return summary

    return None

def generate_wiki_content(filename, content):
    """生成wiki页面内容"""
    title = extract_title(content)
    author = extract_author(content)
    date = extract_date_from_filename(filename)
    tags = extract_tags(content)
    summary = extract_summary(content)

    # 去除文件名中的日期前缀，提取标题
    clean_filename = re.sub(r'^\[\d{4}-\d{2}-\d{2}\]\s*', '', filename)
    clean_filename = clean_filename.replace('.md', '')

    # 构建frontmatter
    frontmatter = f'''---
title: {title}
type: summary
category: 诉讼与仲裁
created: 2026-05-11
updated: 2026-05-11
tags: {tags}
source: ["sources/微信公号资料/上海二中院/上海二中院-至正法官札记-md/{filename}"]
related: []
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{filename}]] |
| 类型 | 法官札记 |
| 主笔 | {author or "未知"} |
| 发布日期 | {date or "未知"} |
| 关键词 | {" / ".join(tags)} |

'''

    # 提取正文内容（去除END之后的内容）
    main_content = content.split('**END**')[0] if '**END**' in content else content

    # 去除标题行和主笔行
    content_lines = []
    skip_next = False
    for line in main_content.split('\n'):
        if skip_next:
            skip_next = False
            continue
        if '# ' in line or '本期主笔' in line:
            skip_next = True  # 跳过主笔信息的下一行（可能是职位描述）
            continue
        content_lines.append(line)

    body = '\n'.join(content_lines)

    return frontmatter + body

def main():
    # 确保目标目录存在
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    source_files = list(SOURCE_DIR.glob("*.md"))
    print(f"找到 {len(source_files)} 个源文件")

    created_count = 0
    for sf in source_files:
        filename = sf.name

        # 读取源文件
        with open(sf, 'r', encoding='utf-8') as f:
            content = f.read()

        # 生成wiki文件名
        # 去除日期前缀
        clean_name = re.sub(r'^\[\d{4}-\d{2}-\d{2}\]\s*', '', filename)
        clean_name = clean_name.replace('.md', '')
        wiki_filename = f"summary_Court_上海二中院_法官札记_{clean_name}.md"
        target_path = TARGET_DIR / wiki_filename

        # 生成内容
        wiki_content = generate_wiki_content(filename, content)

        # 写入文件
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(wiki_content)

        created_count += 1

    print(f"创建了 {created_count} 个wiki页面")

if __name__ == '__main__':
    main()
