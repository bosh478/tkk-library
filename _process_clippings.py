#!/usr/bin/env python3
"""
处理 Clippings/ 目录下的律师业务指引，生成 wiki summaries
遵循批量 Ingest 执行规范（经验固化）
"""
import os
import re
from pathlib import Path

VAULT_ROOT = Path("D:/AI agent/tkk-library")
CLIPPINGS_DIR = VAULT_ROOT / "Clippings"
SUMMARIES_DIR = VAULT_ROOT / "wiki" / "summaries"

def extract_key_content(content, max_lines=80):
    """从内容提取关键段落（去除网站导航、页眉页脚等干扰内容）"""
    lines = content.split('\n')
    result = []
    skip_patterns = [
        r'^!\[.*\]$',  # 图片
        r'^__+$',  # 分隔线
        r'^source:', r'^author:', r'^created:', r'^tags:', r'^description:',
        r'^#+\s*$',  # 空标题
        r'javascript:void',
        r'^-\s*\[.*\]\(https?://',  # 外部链接
        r'^-\s*"clippings"',  # 导航水印
        r'^当前位置：',
        r'^\s*>>\s*\[',
        r'^\s*\[业务指引\]',
        r'^\s*\[业务研究大厅\]',
        r'^\s*\[请点击此处反馈\]',
        r'本指引于\s*\d{4}年',  # 指引发布时间
        r'^\s*日期：',
        r'^\s*\*\*+\s*本指引于',
        r'^\s*\*\*+目\s*录',
        r'^\s*目\s*录',
        r'^\s*第[一二三四五六七八九十]+章',
        r'^\s*第[0-9]+条',  # 单独的法条编号
        r'^\s*\*\*+',  # 加粗的标题标记
        r'^\s*\[阅读原文\]',
    ]
    skip_count = 0
    for i, line in enumerate(lines):
        if i < 5:
            continue
        line_stripped = line.strip()
        skip = False
        for pattern in skip_patterns:
            if re.search(pattern, line_stripped):
                skip = True
                break
        if skip:
            skip_count += 1
            continue
        # 去除行首标题标记，保留内容
        clean = re.sub(r'^#+\s*', '', line_stripped)
        if clean and len(clean) > 5 and not clean.startswith('- ['):
            result.append(clean)
        if len(result) >= max_lines:
            break
    return '\n'.join(result[:max_lines])

def extract_title(content, filename):
    """从内容提取标题"""
    lines = content.strip().split('\n')
    for line in lines[:15]:
        line = line.strip()
        if line.startswith('#'):
            return line.lstrip('#').strip()
    return filename.replace('.md', '')

def extract_date_from_content(content):
    """从内容提取日期"""
    match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', content)
    if match:
        return f"{match.group(1)}-{int(match.group(2)):02d}-{int(match.group(3)):02d}"
    match = re.search(r'(\d{4})-(\d{2})-(\d{2})', content[:500])
    if match:
        return match.group(0)
    return "2026-04-15"

def clean_filename(name):
    """清理文件名，去除机构后缀"""
    name = re.sub(r'\s*-\s*业务指引\s*-\s*业务研究大厅\s*-\s*东方律师网\s*$', '', name)
    name = re.sub(r'\s*-\s*业务指引\s*-\s*东方律师网\s*$', '', name)
    name = re.sub(r'\s*（附全文）\s*$', '', name)
    name = re.sub(r'\s*（\d+）\s*$', '', name)
    return name.strip()

def determine_category(title):
    """根据标题判断 category"""
    if any(k in title for k in ['诉讼', '仲裁', '辩护', '审判', '庭审']):
        return '诉讼与仲裁（民商事）'
    if any(k in title for k in ['公司', '企业', '股权', '股东', '章程', '关联交易', '担保']):
        return '公司商事与合规'
    if any(k in title for k in ['劳动', '竞业限制', '工伤', '劳动合同']):
        return '劳动与社会保障'
    if any(k in title for k in ['医疗', '医药', '医院', '健康']):
        return '医药健康'
    if any(k in title for k in ['海关', '进出口', '外贸', '国际']):
        return '国际贸易'
    if any(k in title for k in ['婚姻', '离婚', '继承', '遗嘱', '监护', '家族']):
        return '婚姻家庭与继承'
    if any(k in title for k in ['建筑', '房地产', '物业', '征收', '土地']):
        return '建筑工程与房地产'
    if any(k in title for k in ['政府', '行政', '信息公开', '信访']):
        return '政府与公共法律服务'
    if any(k in title for k in ['环境', '能源', '光伏', '电池', 'CCER', '生态']):
        return '生态环境与能源'
    if any(k in title for k in ['知识产权', '版权', '专利', '商标']):
        return '知识产权'
    if any(k in title for k in ['税务', '财税', '税', '发票', '私募', '基金', '融资', '投资']):
        return '金融与财税'
    if any(k in title for k in ['走私', '刑事', '诈骗', '盗窃', '抢劫']):
        return '诉讼与仲裁（民商事）'
    if any(k in title for k in ['广东高院', '港澳', '商事纠纷', '证人', '司法规则']):
        return '民商事'
    return '公司商事与合规'

def process_all():
    total = 0
    created = 0

    for f in sorted(CLIPPINGS_DIR.glob("*.md")):
        raw = f.read_text(encoding='utf-8')
        title = extract_title(raw, f.name)
        clean_title = clean_filename(f.name.replace('.md', ''))

        key_content = extract_key_content(raw, max_lines=60)
        date = extract_date_from_content(raw)
        category = determine_category(title)

        # 生成摘要文件名
        date_prefix = date.replace('-', '')[:8]
        safe_title = re.sub(r'[【】\[\]（）()《》<>：:\"\'\s]', '_', clean_title)
        safe_title = re.sub(r'_{3,}', '_', safe_title).strip('_')
        dest_name = f"{date_prefix}_{safe_title}.md"
        dest = SUMMARIES_DIR / dest_name

        content = f"""---
title: {clean_title if clean_title else title}
type: summary
created: {date}
updated: 2026-04-15
tags: [律师业务指引]
category: {category}
source: [[{f.name}]]
---

## 关键要点

{key_content[:2000] if key_content else '（见原文）'}

## 相关链接
- 原文来源：[[{f.name}]]
"""
        with open(dest, 'w', encoding='utf-8') as out:
            out.write(content)
        created += 1
        total += 1

    print(f"=== 完成，共处理 {total} 个文件 ===")
    print(f"新建/更新: {created} 个")
    current = len(list(SUMMARIES_DIR.glob("*.md")))
    print(f"wiki/summaries/ 当前文件数: {current}")

if __name__ == "__main__":
    process_all()