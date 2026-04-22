# -*- coding: utf-8 -*-
"""
刑事审判参考案例拆分脚本
将每一辑拆分为独立的案例页面
"""

import re
import os
from pathlib import Path

# 设置路径
SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/《刑事审判参考》")
OUTPUT_DIR = Path("D:/AI agent/tkk-library/wiki/syntheses/Court_刑事审判参考")
LOG_FILE = Path("D:/AI agent/tkk-library/log.md")

def log(msg):
    """记录日志"""
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def parse_case_file(filepath):
    """解析案例文件，返回案例列表"""
    content = filepath.read_text(encoding="utf-8")
    lines = content.split('\n')

    # 提取辑号
    match = re.search(r'总第(\d+)辑', filepath.name)
    ji_num = match.group(1) if match else "000"

    cases = []
    current_case = None

    for i, line in enumerate(lines):
        # 案例以 "# 标题" 开头
        if line.startswith('# ') and len(line) > 4:
            title = line[2:].strip()
            # 过滤掉非案例的标题
            skip_keywords = [
                '编辑说明', '特邀编辑', '征稿启事', '征订单', '汇款方法',
                '调查问卷', '读者反馈', '目录', '编辑委员会', '指导案例',
                '经验交流', '大案传真', '立法、司法规范', '疑案争鸣',
                '刑事审判参考', '总第', '【', '】', '2014', '2015',
            ]
            if any(kw in title for kw in skip_keywords):
                continue
            if len(title) < 5:
                continue

            if current_case:
                cases.append(current_case)

            current_case = {
                'title': title,
                'line': i + 1,
                'ji_num': ji_num,
                'lines': [line]
            }
        elif current_case:
            current_case['lines'].append(line)

    if current_case:
        cases.append(current_case)

    return cases

def extract_case_info(case):
    """从案例内容提取关键信息"""
    content = '\n'.join(case['lines'])

    # 提取案例编号
    num_match = re.search(r'\[第(\d+)号\]', content)
    case_num = num_match.group(1) if num_match else "000000"

    # 清理标题
    clean_title = re.sub(r'\[第\d+号\]\s*', '', case['title'])
    clean_title = re.sub(r'\s*[（\(【【].*', '', clean_title)
    clean_title = clean_title.strip()

    # 提取主要问题（副标题）
    subtitle_match = re.search(r'\[第\d+号\]\s*[一-龥]+(.*)', content)
    subtitle = subtitle_match.group(1).strip()[:100] if subtitle_match else ""

    # 提取裁判要旨（从裁判理由部分）
    key_points = []
    reason_match = re.search(r'## 三、裁判理由\s*\n(.+?)(?=审编：|\n#)', content, re.DOTALL)
    if reason_match:
        text = reason_match.group(1).strip()
        # 取第一段作为裁判要旨摘要
        paras = text.split('\n')
        for p in paras:
            p = p.strip()
            if p and len(p) > 30 and not p.startswith('#') and not p.startswith('（'):
                key_points.append(p[:500])
                break

    # 生成文件 slug
    slug_title = re.sub(r'[^一-龥a-zA-Z0-9]', '_', clean_title)[:25]
    slug = f"Court_刑事审判参考_{case['ji_num']}辑_{case_num}号_{slug_title}"

    return {
        'case_num': case_num,
        'ji_num': case['ji_num'],
        'title': clean_title,
        'subtitle': subtitle,
        'key_point': key_points[0] if key_points else "",
        'slug': slug,
        'content': content
    }

def generate_page(case_info):
    """生成 synthesis 页面"""
    title = case_info['title']
    case_num = case_info['case_num']
    ji_num = case_info['ji_num']
    subtitle = case_info['subtitle']
    key_point = case_info['key_point']
    content = case_info['content']

    page = f"""---
title: {title}
type: synthesis
created: 2026-04-22
updated: 2026-04-22
tags: [刑事审判参考, 第{ji_num}辑, 案例集]
case_num: {case_num}
ji_num: {ji_num}
source: [["《刑事审判参考 总第{ji_num}辑》.md"]]
---

# {title}

**案例编号**：第{case_num}号
**辑别**：刑事审判参考 总第{ji_num}辑

{subtitle}

---

## 正文

{content}

---

## 裁判要旨

{key_point}

---

## 关联

- 本辑目录：[[Court_刑事审判参考_《刑事审判参考 总第{ji_num}辑》.md]]
"""

    return page

def main():
    # 确保输出目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    log("\n## [2026-04-22] 细化整理：刑事审判参考案例拆分")

    # 获取所有案例文件
    case_files = sorted(SOURCE_DIR.glob("《刑事审判参考 总第*.md"))

    total_files = len(case_files)
    total_cases = 0

    for case_file in case_files:
        log(f"- 处理：{case_file.name}")

        # 解析案例文件
        cases = parse_case_file(case_file)
        log(f"  - 发现 {len(cases)} 个案例")

        for case in cases:
            case_info = extract_case_info(case)

            # 生成页面
            page_content = generate_page(case_info)
            output_path = OUTPUT_DIR / f"{case_info['slug']}.md"

            output_path.write_text(page_content, encoding="utf-8")
            log(f"  + 创建：{output_path.name}")

        total_cases += len(cases)

    log(f"- 总计：处理 {total_files} 辑，{total_cases} 个案例")
    print(f"\n完成！共处理 {total_cases} 个案例")

if __name__ == "__main__":
    main()