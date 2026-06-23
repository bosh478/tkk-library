#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理监外执行专题中的 4 个大法规（>50KB）
"""
import os
import re
import sys
from pathlib import Path

VAULT = Path(r'D:\AI agent\tkk-library')
SRC_DIR = VAULT / 'sources' / '1-专题研究' / '监外执行'
WIKI_ENTITIES = VAULT / 'wiki' / 'entities'
WIKI_CONCEPTS = VAULT / 'wiki' / 'concepts'
TODAY = '2026-06-09'

# 4 个大法规
BIG_LAWS = {
    '20210301_最高人民法院关于适用《中华人民共和国刑事诉讼法》的解释（2021年）.txt': {
        'entity': 'entity_最高人民法院关于适用刑事诉讼法的解释（2021年）.md',
        'type': '司法解释',
        'wenhao': '法释〔2021〕1号',
        'date': '2021-03-01',
        'category': '刑事诉讼法',
    },
    '20200901_公安机关办理刑事案件程序规定（2020年修正）.txt': {
        'entity': 'entity_公安机关办理刑事案件程序规定（2020年修正）.md',
        'type': '部门规章',
        'wenhao': '公安部令第159号',
        'date': '2020-09-01',
        'category': '刑事诉讼法',
    },
    '20240701_国家安全机关办理刑事案件程序规定.txt': {
        'entity': 'entity_国家安全机关办理刑事案件程序规定.md',
        'type': '部门规章',
        'wenhao': '',
        'date': '2024-07-01',
        'category': '刑事诉讼法',
    },
    '20261101_中华人民共和国监狱法（2026年修订）.txt': {
        'entity': 'entity_中华人民共和国监狱法（2026年修订）.md',
        'type': '法律',
        'wenhao': '',
        'date': '2026-11-01',
        'category': '监狱管理',
    },
}


def parse_metadata(content):
    """解析元数据"""
    meta = {}
    m = re.search(r'文章属性(.*?)(?=\n\s*正文|\Z)', content, re.DOTALL)
    if not m:
        return meta
    text = m.group(1)
    patterns = {
        'issuer': r'【制定机关】\s*(.+?)(?:\n|$)',
        'date': r'【公布日期】\s*(.+?)(?:\n|$)',
        'wenhao': r'【文\s*号】\s*(.+?)(?:\n|$)',
        'effective': r'【施行日期】\s*(.+?)(?:\n|$)',
        'level': r'【效力等级】\s*(.+?)(?:\n|$)',
        'status': r'【时效性】\s*(.+?)(?:\n|$)',
        'category': r'【主题分类】\s*(.+?)(?:\n|$)',
    }
    for k, p in patterns.items():
        m2 = re.search(p, text)
        if m2:
            meta[k] = m2.group(1).strip()
    return meta


def extract_chapters(body):
    """提取章节（章级标题）"""
    chapters = []
    cur = None
    for line in body.split('\n'):
        s = line.strip()
        if s.startswith('第') and '章' in s and len(s) < 50:
            if cur:
                chapters.append(cur)
            cur = {'title': s, 'content': ''}
        elif cur is not None:
            cur['content'] += line + '\n'
    if cur:
        chapters.append(cur)
    return chapters


def make_big_law_page(src_filename, meta, body, config):
    """为大法规生成页面"""
    title = src_filename.replace('.txt', '').replace('.md', '')
    # 清理 title
    title_clean = re.sub(r'^\d+_', '', title)
    issuer = meta.get('issuer', '')
    date = meta.get('date', config.get('date', ''))
    wenhao = meta.get('wenhao', config.get('wenhao', ''))
    effective = meta.get('effective', '')
    level = meta.get('level', config.get('type', ''))
    status = meta.get('status', '现行有效')
    category = meta.get('category', config.get('category', ''))

    # frontmatter
    tags = ['刑事执行', '刑事诉讼法']
    if '监狱' in title:
        tags = ['法律', '监狱管理', '刑事执行']
    if '公安' in title:
        tags = ['部门规章', '公安', '刑事执行']
    if '国安' in title or '国家安全' in title:
        tags = ['部门规章', '国家安全', '刑事执行']
    tags_str = ', '.join(tags)

    frontmatter = f"""---
title: {title_clean}
type: entity
created: {TODAY}
updated: {TODAY}
tags: [{tags_str}]
related:
  - [[concept_中华人民共和国刑事诉讼法]]
  - [[concept_中华人民共和国监狱法]]
  - [[concept_社区矫正]]
  - [[concept_暂予监外执行]]
  - [[concept_减刑]]
  - [[concept_假释]]
source: '[[{src_filename}]]'
---

## 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{src_filename}]] |
| 类型 | {config.get('type', '法律/部门规章')} |
| 制定机关 | {issuer or '全国人大常委会/国务院'} |
| 公布日期 | {date} |
| 文号 | {wenhao} |
| 施行日期 | {effective} |
| 时效性 | {status} |
| 主题分类 | {category} |

## 与监外执行相关的核心条文

"""

    # 提取监外执行相关条款
    related_keywords = ['暂予监外执行', '保外就医', '监外执行', '生活不能自理', '社区矫正', '交付执行', '减刑', '假释', '保外', '严重疾病']
    related_sections = []
    for kw in related_keywords:
        idx = 0
        while True:
            pos = body.find(kw, idx)
            if pos < 0:
                break
            # 找这一段
            start = max(0, pos - 200)
            end = min(len(body), pos + 400)
            snippet = body[start:end].strip()
            if kw not in [s[:5] for s in related_sections]:
                related_sections.append(f'**{kw}** 相关：...{snippet}...')
            idx = pos + 1
            if len(related_sections) >= 15:
                break
        if len(related_sections) >= 15:
            break
    frontmatter += '\n'.join(related_sections) + '\n\n'

    # 提取章节列表
    chapters = extract_chapters(body)
    if chapters:
        frontmatter += '## 主要章节\n\n'
        for ch in chapters[:30]:
            frontmatter += f'### {ch["title"]}\n\n{ch["content"][:800]}\n\n' if len(ch['content']) > 800 else f'### {ch["title"]}\n\n{ch["content"]}\n\n'

    frontmatter += f"""
## 完整文本

{body[:30000]}

"""
    if len(body) > 30000:
        frontmatter += f"\n> 注：原文超过 30000 字，此处仅展示前 30000 字。完整内容见源文件 [[{src_filename}]]。\n"

    frontmatter += """
## 相关

- [[concept_中华人民共和国刑事诉讼法]]
- [[concept_中华人民共和国监狱法]]
- [[concept_社区矫正]]
- [[concept_暂予监外执行]]
- [[concept_减刑]]
- [[concept_假释]]
"""
    return frontmatter


def process_big():
    processed = 0
    skipped = 0
    for src_name, config in BIG_LAWS.items():
        src_path = SRC_DIR / src_name
        if not src_path.exists():
            print(f'[ERR] 文件不存在: {src_name}')
            continue
        target_name = config['entity']
        target_path = WIKI_ENTITIES / target_name
        if target_path.exists():
            print(f'[SKIP] 已存在: {target_name}')
            skipped += 1
            continue
        try:
            with open(src_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(src_path, 'r', encoding='gbk') as f:
                content = f.read()
        meta = parse_metadata(content)
        # 提取正文
        m = re.search(r'\n\s*正文\s*\n(.*)', content, re.DOTALL)
        body = m.group(1).strip() if m else content
        page = make_big_law_page(src_name, meta, body, config)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(page)
        processed += 1
        print(f'[OK] {target_name} ({len(page)} bytes)')
    print(f'\n处理完成: 成功 {processed} 个，跳过 {skipped} 个')


if __name__ == '__main__':
    process_big()
