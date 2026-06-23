#!/usr/bin/env python3
"""Process SPP 检答网集萃 source files into wiki summaries"""

import re
import os
from pathlib import Path

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-检答网集萃-md")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/summaries")
TARGET_DIR.mkdir(parents=True, exist_ok=True)

def extract_title(content):
    """Extract title from # line - handle various quote types"""
    patterns = [
        (r'^#\s*【检答网集萃(\d+)】(.+?)$', 2),
        (r'^#\s*【检答网集萃—(\d+)】(.+?)$', 2),
        (r'^#\s*【检答网集萃】(.+?)$', 1),
    ]
    for pattern, group_idx in patterns:
        match = re.search(pattern, content, re.MULTILINE)
        if match:
            title = match.group(group_idx).strip()
            title = re.sub(r'^\[\d{4}-\d{2}-\d{2}\]', '', title).strip()
            return title
    return None

def extract_single_qa(block):
    """Extract Q&A from a single block, handling various formats"""
    # Flexible pattern for **咨询类别：**
    cat_match = re.search(r'\*\*\s*咨询类别[：:]\s*\*\*\s*(\S+)', block)
    category = cat_match.group(1) if cat_match else ""

    # Flexible pattern for **咨询内容：**
    cons_match = re.search(r'\*\*\s*咨询内容[：:]\s*\*\*\s*(.+?)(?=\*\*咨询人|\*\*答疑人|\*\*解答专家|\*\*编辑|预览时标签|$)', block, re.DOTALL)
    consult_content = cons_match.group(1).strip() if cons_match else ""

    # Flexible pattern for **咨询人：** or **答疑人XXX：**
    consul_match = re.search(r'\*\*\s*(?:咨询人|答疑人[^：]*)[：:]\s*\*\*\s*(\S[\s\S]*?)(?=\*\*|$)', block)
    consultant = consul_match.group(1).strip() if consul_match else ""
    consultant = re.sub(r'\*\*', '', consultant).strip()

    # Flexible pattern for **解答专家XXX：** or **答疑人XXX：**
    ans_match = re.search(r'\*\*\s*(?:解答专家|答疑人)[^：]*[：:]\s*\*\*\s*(.+?)(?=\*\*问题|\*\*编辑|预览时标签|$)', block, re.DOTALL)
    answer = ans_match.group(1).strip() if ans_match else ""

    return {
        'category': category,
        'content': consult_content,
        'consultant': consultant,
        'answer': answer
    }

def extract_questions_answers(content):
    """Extract all question-answer pairs"""
    pairs = []

    # Pattern 1: **问题一：** **question text** (question label + question on next bold line)
    q_label_pattern = re.compile(r'\*\*(问题\s*[一二三四五六七八九十\d]+(?:\.\d)?)\s*[：:]\*\*\s*\*\*(.+?)\*\*')
    matches = list(q_label_pattern.finditer(content))

    if matches:
        for i, m in enumerate(matches):
            label = m.group(1)
            question_text = m.group(2)
            start = m.end()
            end = matches[i+1].start() if i+1 < len(matches) else len(content)
            block = content[start:end]
            qa = extract_single_qa(block)
            pairs.append({
                'label': question_text,
                **qa
            })
    else:
        # Pattern 2: **问题一：** (standalone question label)
        q_simple = re.compile(r'\*\*(问题\s*[一二三四五六七八九十\d]+(?:\.\d)?)\s*[：:]\*\*')
        q_matches = list(q_simple.finditer(content))

        if q_matches:
            for i, m in enumerate(q_matches):
                label = m.group(1)
                start = m.end()
                end = q_matches[i+1].start() if i+1 < len(q_matches) else len(content)
                block = content[start:end]
                qa = extract_single_qa(block)
                pairs.append({
                    'label': label,
                    **qa
                })
        else:
            # Pattern 3: No standard question markers - treat whole content as single Q&A
            # Look for 咨询类别 or 咨询内容 to identify valid content
            if re.search(r'\*\*\s*咨询类别', block := content):
                qa = extract_single_qa(content)
                if qa['content'] or qa['answer']:
                    # Extract label from title or first line
                    label_match = re.search(r'^#\s*【检答网集萃[^】]*】\s*(.+?)\s*$', content, re.MULTILINE)
                    label = label_match.group(1) if label_match else "问题"
                    pairs.append({
                        'label': label,
                        **qa
                    })

    return pairs

def create_summary(source_file):
    """Create a summary wiki page from source file"""
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    title = extract_title(content)
    if not title:
        print(f"Could not extract title from {source_file.name}")
        return None

    pairs = extract_questions_answers(content)

    basename = source_file.stem
    frontmatter = f"""---
title: {title}
type: summary
category: 刑事参考
created: 2026-05-11
updated: 2026-05-11
tags: [检答网, 法律问答, 检察实务]
source: [[{basename}]]
related: []
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{basename}]] |
| 类型 | 检答网集萃 |
| 涉及领域 | {pairs[0]['category'] if pairs else '综合'} |
| 问题数量 | {len(pairs)} |

"""

    for i, pair in enumerate(pairs, 1):
        frontmatter += f"""## ❓ 问题{i}：{pair['label']}

**咨询类别：** {pair['category']}
**咨询内容：** {pair['content']}
**解答专家答复：** {pair['answer']}

"""

    safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)[:100]
    output_file = TARGET_DIR / f"summary_SPP_检答网集萃_{safe_title}.md"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(frontmatter)

    return output_file.name

def main():
    files = sorted(SOURCE_DIR.glob("*.md"))
    print(f"Found {len(files)} files")

    created = []
    failed = []
    for f in files:
        result = create_summary(f)
        if result:
            created.append(result)
        else:
            failed.append(f.name)

    print(f"Created {len(created)} summary files")
    if failed:
        print(f"Failed: {len(failed)} files")
        for name in failed[:10]:
            print(f"  - {name}")

if __name__ == "__main__":
    main()
