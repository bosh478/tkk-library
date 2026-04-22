#!/usr/bin/env python3
"""
刑事审判参考案例拆分脚本
处理每一辑，拆分为独立案例页面
"""

import re
import os
from pathlib import Path

SOURCE_DIR = Path("sources/《刑事审判参考》")
OUTPUT_DIR = Path("wiki/syntheses")

def process_case_file(case_file):
    """处理单个案例文件"""
    filename = case_file.name
    # 提取辑号，如"总第101辑"
    match = re.search(r'总第(\d+)辑', filename)
    if not match:
        print(f"无法识别辑号: {filename}")
        return []

    ji_num = match.group(1)

    content = case_file.read_text(encoding='utf-8')
    lines = content.split('\n')

    # 找到所有案例标题行 (# 标题)
    cases = []
    current_case = None

    for i, line in enumerate(lines):
        # 案例标题行：# 标题 或 ## 标题（避开目录中的）
        # 案例以 # 标题 开头，后面跟着裁判理由等内容
        if line.startswith('# ') and len(line) > 3:
            title = line[2:].strip()
            # 跳过非案例标题（编辑说明等）
            if any(kw in title for kw in ['编辑说明', '特邀编辑', '征稿启事', '征订单', '汇款方法', '调查问卷', '读者反馈', '目录', '刑事审判参考', '编辑委员会']):
                continue
            # 跳过太短的标题
            if len(title) < 4:
                continue
            # 跳过大案传真、经验交流等非案例部分
            if title in ['【指导案例】', '【经验交流】', '【大案传真】', '【立法、司法规范】', '【疑案争鸣】']:
                continue

            # 这是一个新案例
            if current_case:
                cases.append(current_case)

            current_case = {
                'title': title,
                'start_line': i,
                'content_lines': [line]
            }
        elif current_case:
            current_case['content_lines'].append(line)

    if current_case:
        cases.append(current_case)

    # 提取案例编号
    processed_cases = []
    for case in cases:
        content = '\n'.join(case['content_lines'])

        # 查找案例编号
        case_num_match = re.search(r'\[第(\d+)号\]', content)
        case_num = case_num_match.group(1) if case_num_match else f"{ji_num}_{case['title'][:10]}"

        # 清理标题（去除案例编号后缀）
        clean_title = re.sub(r'\[第\d+号\]\s*', '', case['title']).strip()
        clean_title = re.sub(r'\s*[\[（\(【].*', '', clean_title)  # 去除副标题

        # 生成 slug
        slug = re.sub(r'[^一-龥a-zA-Z0-9]', '_', clean_title)[:30]

        processed_cases.append({
            'case_num': case_num,
            'title': clean_title,
            'slug': f"Court_刑事审判参考_{ji_num}辑_{case_num}号_{slug}",
            'ji_num': ji_num,
            'content': content
        })

    return processed_cases

def extract_frontmatter(case_info):
    """提取案例的关键信息用于生成frontmatter"""
    content = case_info['content']

    # 提取主要问题
    questions = re.findall(r'^.+号\s*[——\-]\s*(.+)$', content, re.MULTILINE)
    if not questions:
        # 尝试从"二、主要问题"后的内容提取
        match = re.search(r'## 二、主要问题\s*\n(.+?)(?=\n##|\n#)', content, re.DOTALL)
        if match:
            questions = [match.group(1).strip()[:100]]

    # 提取裁判要旨（简化：取裁判理由后的核心观点）
    key_points = []
    reason_match = re.search(r'## 三、裁判理由\s*\n(.+?)(?=审编：|\n#)', content, re.DOTALL)
    if reason_match:
        reason_text = reason_match.group(1)[:500]
        key_points.append(reason_text[:200] + '...' if len(reason_text) > 200 else reason_text)

    # 生成 tags
    tags = ['刑事审判参考', f'第{case_info["ji_num"]}辑']

    return {
        'case_num': case_info['case_num'],
        'ji_num': case_info['ji_num'],
        'title': case_info['title'],
        'slug': case_info['slug'],
        'content': content,
        'tags': tags
    }

def generate_synthesis_page(case_data):
    """生成 synthesis 页面内容"""
    title = case_data['title']
    case_num = case_data['case_num']
    ji_num = case_data['ji_num']

    # 提取基本案情、主要问题、裁判理由
    content = case_data['content']

    # 提取裁判要旨
    key_points = []
    reason_match = re.search(r'## 三、裁判理由\s*\n(.+?)(?=审编：|\n#|$)', content, re.DOTALL)
    if reason_match:
        text = reason_match.group(1)
        # 提取要点（第一句或段落首句）
        paras = text.split('\n')
        for p in paras:
            p = p.strip()
            if p and len(p) > 20:
                # 取第一个有意义的段落作为裁判要旨
                if not p.startswith('#') and not p.startswith('（') and '裁判理由' not in p:
                    key_points.append(p[:300])
                    break

    # 提取案例编号和案件信息
    case_id = f"第{case_num}号"

    # 生成摘要
    summary = f"刑事审判参考 {ji_num}辑案例，案例编号{case_id}。"
    if key_points:
        summary += f" 裁判要旨：{key_points[0][:150]}"

    # 构建页面
    page = f"""---
title: {title}
type: synthesis
created: 2026-04-22
updated: 2026-04-22
tags: [刑事审判参考, 第{ji_num}辑, 案例{case_id}]
case_num: {case_num}
ji_num: {ji_num}
case_id: "{case_id}"
source: [["《刑事审判参考 总第{ji_num}辑》.md"]]
---

# {title}

**案例编号**：{case_id}
**辑别**：刑事审判参考 总第{ji_num}辑

---

## 案例正文

{content}

---

## 关联

- 上一案例：[[]]
- 下一案例：[[]]
- 本辑目录：[[Court_刑事审判参考_《刑事审判参考 总第{ji_num}辑》.md]]
"""

    return page

def main():
    # 获取所有刑事审判参考文件
    case_files = sorted(SOURCE_DIR.glob("《刑事审判参考 总第*.md"))

    print(f"找到 {len(case_files)} 个案例文件")

    total_cases = 0
    for case_file in case_files:
        print(f"\n处理: {case_file.name}")
        cases = process_case_file(case_file)
        print(f"  发现 {len(cases)} 个案例")

        for case in cases:
            case_data = extract_frontmatter(case)
            page_content = generate_synthesis_page(case_data)

            output_path = OUTPUT_DIR / f"{case_data['slug']}.md"
            output_path.write_text(page_content, encoding='utf-8')
            print(f"  创建: {output_path.name}")

        total_cases += len(cases)

    print(f"\n总计处理 {total_cases} 个案例")

if __name__ == "__main__":
    main()