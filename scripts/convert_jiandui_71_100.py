#!/usr/bin/env python3
"""Convert Jianduiwang Jicui 71-100 to V52 wiki format"""

import re
import os
from pathlib import Path

SRC_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-检答网集萃-md")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/summaries")

def extract_date_filename(filename):
    """Extract date prefix from filename"""
    m = re.match(r'\[(\d{4}-\d{2}-\d{2})\]', filename.name)
    return m.group(1) if m else ""

def extract_number_title(content):
    """Extract issue number and title from content"""
    # Line 1: # 【检答网集萃—{N}】{标题}
    m = re.search(r'检答网集萃[—\-](\d+)[】]*(.*)', content)
    if m:
        return int(m.group(1)), m.group(2).strip()
    return None, None

def extract_meta(content):
    """Extract 咨询类别, 咨询人, 咨询内容"""
    meta = {}

    cat_m = re.search(r'\*\*咨询类别[：:]\*\*\s*(.+?)(?=\*\*|$)', content, re.DOTALL)
    if cat_m:
        meta['category'] = cat_m.group(1).strip()

    person_m = re.search(r'\*\*咨询人[：:]\*\*\s*(.+?)(?=\*\*|$)', content, re.DOTALL)
    if person_m:
        meta['person'] = person_m.group(1).strip()

    content_m = re.search(r'\*\*咨询内容[：:]\*\*\s*((?:.*?\n)*?)(?=\*\*最高检|来源：|$)', content, re.DOTALL)
    if content_m:
        meta['question'] = content_m.group(1).strip()

    return meta

def extract_answer(content):
    """Extract answer section"""
    # Try 最高检专家组解答意见
    m = re.search(r'\*\*最高检专家组解答意见[：:]*\s*((?:.|\n)*?)(?=来源：|\*\*往期|$)', content, re.DOTALL)
    if m:
        return m.group(1).strip()
    # Try 广东省检察院王映答疑意见
    m = re.search(r'\*\*.*?答疑意见[：:]*\s*((?:.|\n)*?)(?=来源：|$)', content, re.DOTALL)
    if m:
        return m.group(1).strip()
    return ""

def clean_content(text):
    """Remove irrelevant content like 阅读原文, 编辑:, 检察日报"""
    text = re.sub(r'来源：.*?检察日报', '', text)
    text = re.sub(r'编辑：.*?(?=\n|$)', '', text)
    text = re.sub(r'预览时标签不可点', '', text)
    text = re.sub(r'\[阅读原文\].*?javascript:;', '', text)
    text = re.sub(r'__+\s*', '', text)
    text = re.sub(r'\*\*往期回顾\*\*.*', '', text, flags=re.DOTALL)
    text = re.sub(r'http://mp\.weixin.*?\)', '', text)
    text = re.sub(r'https://mp\.weixin.*?\)', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def extract_keywords(number, meta, question, answer):
    """Extract keywords from content"""
    kw_set = set()
    if meta.get('category'):
        kw_set.add(meta['category'].replace(' ', ''))
    if '抗诉' in question or '抗诉' in answer:
        kw_set.add('刑事抗诉')
    if '不起诉' in question or '不起诉' in answer:
        kw_set.add('不起诉')
    if '国家赔偿' in question or '国家赔偿' in answer:
        kw_set.add('国家赔偿')
    if '社区矫正' in question or '社区矫正' in answer:
        kw_set.add('社区矫正')
    if '未成年人' in question or '未成年人' in answer:
        kw_set.add('未成年人犯罪')
    if '认罪认罚' in question or '认罪认罚' in answer:
        kw_set.add('认罪认罚')
    if '强制措施' in question or '强制措施' in answer:
        kw_set.add('强制措施')
    if '民事检察' in question or '民事检察' in answer:
        kw_set.add('民事检察监督')
    return list(kw_set) if kw_set else ['检察业务']

def process_file(src_path):
    """Process single file"""
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()

    number, title = extract_number_title(content)
    if not number:
        return None, "Failed to extract number/title"

    if number < 71 or number > 100:
        return None, f"Number {number} outside range 71-100"

    meta = extract_meta(content)
    answer = extract_answer(content)
    clean_answer = clean_content(answer)

    date_str = extract_date_filename(src_path)
    keywords = extract_keywords(number, meta, content, answer)

    target_name = f"summary_检答网集萃{number}_{title}.md"
    target_path = TARGET_DIR / target_name

    # Build frontmatter
    frontmatter = f"""---
title: 检答网集萃{number} {title}
type: summary
created: 2026-05-07
updated: 2026-05-07
tags: {keywords}
category: 诉讼与仲裁
source: [{src_path.name}]
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | {src_path.name} |
| 类型 | 检察业务咨询 |
| 发布日期 | {date_str} |
| 关键词 | {' / '.join(keywords)} |
| 核心要点 | {meta.get('category', '检察业务咨询')}问题解答 |

## 问答摘要

**咨询类别：** {meta.get('category', '未知')}
**咨询人：** {meta.get('person', '未知')}

**咨询内容：**
{meta.get('question', '')}

**最高检解答意见：**
{clean_answer}
"""

    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter)

    return number, target_name

def main():
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(SRC_DIR.glob("*检答网集萃*.md"))

    success = []
    failed = []

    for f in files:
        num_m = re.search(r'集萃(\d+)', f.name)
        if not num_m:
            continue
        num = int(num_m.group(1))
        if 71 <= num <= 100:
            result, msg = process_file(f)
            if result:
                success.append((result, msg))
            else:
                failed.append((f.name, msg))

    print(f"成功处理: {len(success)}个")
    print(f"失败: {len(failed)}个")
    if failed:
        print("\n失败文件:")
        for name, err in failed:
            print(f"  - {name}: {err}")

if __name__ == "__main__":
    main()