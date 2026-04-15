#!/usr/bin/env python3
"""
更好的处理：从source内容提取真正摘要
"""
import os
import re
from pathlib import Path

VAULT_ROOT = Path("D:/AI agent/tkk-library")
SOURCES_DIR = VAULT_ROOT / "sources" / "微信公号资料"
SUMMARIES_DIR = VAULT_ROOT / "wiki" / "summaries"

def extract_key_content(content, max_lines=80):
    """从内容提取关键段落（前max_lines行，去除干扰内容）"""
    lines = content.split('\n')
    result = []
    skip_patterns = [
        r'^!\[.*\]$',  # 图片
        r'^__+$',  # 分隔线
        r'^source:',  # frontmatter字段
        r'^author:',  # frontmatter字段
        r'^created:',  # frontmatter字段
        r'^tags:',  # frontmatter字段
        r'^#+\s*$',  # 空标题
        r'在小说阅读器中沉浸阅读',
        r'检察日报',
        r'javascript:void',
    ]
    skip_count = 0
    for i, line in enumerate(lines):
        # 跳过开头的干扰行（前10行通常是封面信息）
        if i < 8:
            continue
        # 跳过图片和干扰标记
        skip = False
        for pattern in skip_patterns:
            if re.search(pattern, line.strip()):
                skip = True
                break
        if skip:
            skip_count += 1
            continue
        # 去除行首标题标记，保留内容
        clean = re.sub(r'^#+\s*', '', line).strip()
        if clean and len(clean) > 5:
            result.append(clean)
        if len(result) >= max_lines:
            break
    return '\n'.join(result[:max_lines])

def extract_title(body, filename):
    """从内容提取标题"""
    lines = body.strip().split('\n')
    for line in lines[:15]:
        line = line.strip()
        if line.startswith('#'):
            return line.lstrip('#').strip()
        if '】' in line and '【' in line:
            match = re.search(r'【(.+?)】', line)
            if match:
                return match.group(1)
    return filename.replace('.md', '')

def extract_date(filename):
    """从文件名提取日期"""
    match = re.search(r'\[?(\d{4}-\d{2}-\d{2})\]?', filename)
    return match.group(1) if match else ""

def process_all():
    total = 0
    created = 0

    # 1. 指导性案例
    source_dir = SOURCES_DIR / "最高检-指导性案例-md"
    for f in sorted(source_dir.glob("*.md")):
        raw = f.read_text(encoding='utf-8')
        # 解析frontmatter
        lines = raw.split('\n')
        frontmatter = {}
        body_lines = []
        in_fm = False
        for line in lines:
            if line.strip() == '---':
                if not in_fm:
                    in_fm = True
                else:
                    in_fm = False
                    continue
            elif in_fm and ':' in line:
                k, v = line.split(':', 1)
                frontmatter[k.strip()] = v.strip()
            else:
                body_lines.append(line)
        body = '\n'.join(body_lines)

        title = extract_title(body, f.name)
        key_content = extract_key_content(body, max_lines=60)

        dest_name = f"SPP_GuideCase_{f.stem}.md"
        dest = SUMMARIES_DIR / dest_name

        src_ref = frontmatter.get('source', f.name)

        content = f"""---
title: {title}
type: summary
created: 2026-04-15
updated: 2026-04-15
tags: [最高检,指导性案例]
category: 刑事
category: 刑事
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

    # 2. 检答网集萃
    source_dir = SOURCES_DIR / "最高检-检答网集萃-md"
    for f in sorted(source_dir.glob("*.md")):
        raw = f.read_text(encoding='utf-8')
        lines = raw.split('\n')
        body_lines = [l for l in lines if l.strip() and not l.strip().startswith('![') and not re.match(r'^__+$', l.strip())]
        body = '\n'.join(body_lines[10:])  # 跳过前10行干扰
        title = extract_title(body, f.name)
        key_content = extract_key_content(body, max_lines=50)

        date = extract_date(f.name)
        dest_name = f"SPP_JianDaWang_{date}_{f.stem}.md"
        dest = SUMMARIES_DIR / dest_name

        content = f"""---
title: {title}
type: summary
created: 2026-04-15
updated: 2026-04-15
tags: [最高检,检答网]
category: 刑事
category: 刑事
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

    # 3. 入库案例选介
    source_dir = SOURCES_DIR / "最高法-入库案例选介-md"
    for f in sorted(source_dir.glob("*.md")):
        raw = f.read_text(encoding='utf-8')
        lines = raw.split('\n')
        body_lines = [l for l in lines if l.strip() and not l.strip().startswith('![') and not re.match(r'^__+$', l.strip())]
        body = '\n'.join(body_lines[10:])
        title = extract_title(body, f.name)
        key_content = extract_key_content(body, max_lines=50)

        date = extract_date(f.name)
        dest_name = f"Court_RukuAnli_{date}_{f.stem}.md"
        dest = SUMMARIES_DIR / dest_name

        content = f"""---
title: {title}
type: summary
created: 2026-04-15
updated: 2026-04-15
tags: [最高法,人民法院案例库]
category: 民商事
category: 民商事
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

    # 4. 法答网精选答问
    source_dir = SOURCES_DIR / "最高法-法答网精选答问-md"
    for f in sorted(source_dir.glob("*.md")):
        raw = f.read_text(encoding='utf-8')
        lines = raw.split('\n')
        body_lines = [l for l in lines if l.strip() and not l.strip().startswith('![') and not re.match(r'^__+$', l.strip())]
        body = '\n'.join(body_lines[10:])
        title = extract_title(body, f.name)
        key_content = extract_key_content(body, max_lines=50)

        dest_name = f"Court_FaDaWang_{f.stem}.md"
        dest = SUMMARIES_DIR / dest_name

        content = f"""---
title: {title}
type: summary
created: 2026-04-15
updated: 2026-04-15
tags: [最高法,法答网]
category: 民商事
category: 民商事
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
    current = len(list(SUMMARIES_DIR.glob("*.md")))
    print(f"wiki/summaries/ 当前文件数: {current}")

if __name__ == "__main__":
    process_all()
