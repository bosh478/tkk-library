#!/usr/bin/env python3
"""批量处理公号文章 - sources/网络文章/ - 修复版"""

import re
from pathlib import Path

VAULT = Path("D:/AI agent/tkk-library")
WIKI = VAULT / "wiki/summaries"
SOURCES = VAULT / "sources/网络文章"

# 从文件名/内容提取分类
SOURCE_CATS = {
    '上海高院': '诉讼与仲裁',
    '上海一中': '诉讼与仲裁',
    '上海二中': '诉讼与仲裁',
    '上海金融法院': '金融与财税',
    '最高人民法院': '诉讼与仲裁',
    '最高人民检察院': '诉讼与仲裁',
    '湖北高院': '诉讼与仲裁',
    '专题研究': '诉讼与仲裁',
}

TITLE_CATS = {
    '劳动': '劳动与社会保障',
    '休息权': '劳动与社会保障',
    '工伤': '劳动与社会保障',
    '工资': '劳动与社会保障',
    '社保': '劳动与社会保障',
    '离职': '劳动与社会保障',
    '商事': '公司商事与合规',
    '公司': '公司商事与合规',
    '股权': '公司商事与合规',
    '企业': '公司商事与合规',
    '投资': '公司商事与合规',
    '医疗': '医药健康',
    '健康': '医药健康',
    '婚姻': '婚姻家庭与继承',
    '家庭': '婚姻家庭与继承',
    '继承': '婚姻家庭与继承',
    '刑事': '诉讼与仲裁',
    '犯罪': '诉讼与仲裁',
    '诈骗': '诉讼与仲裁',
    '知识产权': '知识产权',
    '商标': '知识产权',
    '专利': '知识产权',
    '版权': '知识产权',
    '不正当竞争': '知识产权',
    '金融': '金融与财税',
    '税务': '金融与财税',
    '消费': '金融与财税',
    '行政': '政府与公共法律服务',
    '处罚': '政府与公共法律服务',
    '建筑': '建筑工程与房地产',
    '房地产': '建筑工程与房地产',
    '物业': '建筑工程与房地产',
    '环境': '生态环境与能源',
    '安全': '生态环境与能源',
    '生产安全': '生态环境与能源',
    '贸易': '国际贸易',
    '涉外': '国际贸易',
}

def get_cat(title, fname):
    for k, v in SOURCE_CATS.items():
        if k in fname:
            return v
    for k, v in TITLE_CATS.items():
        if k in title:
            return v
    return '诉讼与仲裁'

def is_processed(fname):
    """检查fname是否已处理 - 通过检查wiki文件的source字段"""
    for wf in WIKI.glob("*.md"):
        try:
            content = wf.read_text(encoding='utf-8')
            if f'source: "{fname}"' in content or f"source: '{fname}'" in content:
                return True
        except:
            pass
    return False

def process_file(src_path):
    fname = src_path.name
    content = src_path.read_text(encoding='utf-8')

    # 提取标题
    title = None
    m = re.search(r'^#\s+(.+?)(?:\s*$|\n)', content, re.MULTILINE)
    if m:
        title = m.group(1).strip()
    if not title:
        title = fname.replace('.md', '')

    # 提取日期
    date_str = None
    m = re.search(r'^published:\s*(\d{4})-(\d{2})-(\d{2})', content, re.MULTILINE)
    if m:
        date_str = f"{m.group(1)}{m.group(2)}{m.group(3)}"
    else:
        m = re.search(r'(\d{8})', fname)
        if m:
            date_str = m.group(1)
        else:
            date_str = "20260101"

    cat = get_cat(title, fname)

    # 生成wiki文件名
    source_prefix = ""
    for k in ['上海高院', '上海一中', '上海二中', '上海金融法院', '最高人民法院', '最高人民检察院', '湖北高院']:
        if k in fname:
            source_prefix = k + "_"
            break

    clean_title = re.sub(r'[^\w一-鿿]', '_', title[:20])
    clean_title = re.sub(r'_+', '_', clean_title)

    wiki_name = f"summary_{date_str}_{source_prefix}{clean_title}.md"
    wiki_name = re.sub(r'[^\w一-鿿._-]', '', wiki_name)
    wiki_path = WIKI / wiki_name

    # 正文预览
    lines = content.split('\n')
    body = []
    started = False
    for line in lines:
        if not started and line.strip() and not line.startswith('---'):
            started = True
        if started:
            if line.startswith('## ') and body:
                break
            body.append(line)
            if len(body) >= 20:
                break

    body_text = '\n'.join(body[:15])

    fm = f"""---
title: "{title}"
type: summary
category: {cat}
created: 2026-05-19
updated: 2026-05-19
tags: [法院案例, 公号文章]
source: "{fname}"
---

## 正文

{body_text}

> 来源：{fname}
"""

    try:
        wiki_path.write_text(fm, encoding='utf-8')
        return f"OK|{fname}|{wiki_name}"
    except Exception as e:
        return f"FAIL|{fname}|{e}"

def main():
    all_src = list(SOURCES.glob("*.md"))
    processed = 0
    skipped = 0
    failed = 0

    print(f"总源文件数: {len(all_src)}")

    for src_path in all_src:
        fname = src_path.name

        if is_processed(fname):
            skipped += 1
            continue

        res = process_file(src_path)
        status = res.split("|")[0]
        if status == "OK":
            processed += 1
            print(f"OK: {res.split('|')[2][:60]}")
        elif status == "SKIP":
            skipped += 1
        else:
            failed += 1
            print(f"FAIL: {res}")

    print(f"\n=== 结果 ===")
    print(f"成功: {processed}")
    print(f"跳过(已处理): {skipped}")
    print(f"失败: {failed}")

if __name__ == "__main__":
    main()