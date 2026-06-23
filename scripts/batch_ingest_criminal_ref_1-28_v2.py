#!/usr/bin/env python3
"""
刑事审判参考批量Ingest脚本 v2 - 处理1-28辑
改进版：只提取有案例编号[第XX号]的案例
"""

import re
import os
from pathlib import Path

# VAULT_ROOT 多平台兼容（patched 2026-06-23）：
# 1. 优先 TKK_VAULT_ROOT 环境变量
# 2. Windows: "D:/AI agent/tkk-library"
# 3. Linux/WSL: /home/kangkang/tkk-library 等候选按存在性自动探测
_VAULT_CANDIDATES = [
    os.environ.get("TKK_VAULT_ROOT"),
    "D:/AI agent/tkk-library" if os.name == "nt" else None,
    "/home/kangkang/tkk-library",
    "/mnt/d/AI agent/tkk-library",
    "/mnt/c/Users/汤康康/tkk-library",
]
VAULT_ROOT = next(
    (Path(p) for p in _VAULT_CANDIDATES if p and Path(p).exists()),
    Path(os.environ.get("TKK_VAULT_ROOT", "D:/AI agent/tkk-library"))
)
SOURCE_DIR = VAULT_ROOT / "sources/刑事审判参考/刑事审判参考-100以内"
OUTPUT_DIR = VAULT_ROOT / "wiki/syntheses"

# 源文件清单（28个文件）
SOURCE_FILES = [
    "《刑事审判参考 总第1辑》.md",
    "《刑事审判参考 总第2辑》.md",
    "《刑事审判参考 总第3卷 上辑》.md",
    "《刑事审判参考 总第3辑》.md",
    "《刑事审判参考 总第4辑》.md",
    "《刑事审判参考 总第5辑》.md",
    "《刑事审判参考 总第6辑》.md",
    "《刑事审判参考 总第7辑》.md",
    "《刑事审判参考 总第8辑》.md",
    "《刑事审判参考 总第10辑》.md",
    "《刑事审判参考 总第11辑》.md",
    "《刑事审判参考 总第12辑》.md",
    "《刑事审判参考 总第14辑》.md",
    "《刑事审判参考 总第15辑》.md",
    "《刑事审判参考 总第16辑》.md",
    "《刑事审判参考 总第17辑》.md",
    "《刑事审判参考 总第19辑》.md",
    "《刑事审判参考 总第20辑》.md",
    "《刑事审判参考 总第21辑》.md",
    "《刑事审判参考 总第22辑》.md",
    "《刑事审判参考 总第23辑》.md",
    "《刑事审判参考 总第24辑》.md",
    "《刑事审判参考 总第26辑》.md",
    "《刑事审判参考 总第27辑》.md",
    "《刑事审判参考 总第29辑》.md",
    "《刑事审判参考 总第31辑》.md",
    "《刑事审判参考 总第32辑》.md",
    "《刑事审判参考 总第33辑》.md",
    "《刑事审判参考 总第34辑》.md",
]

def extract_ji_num(filename):
    """从文件名提取辑号"""
    match = re.search(r'总第(\d+)', filename)
    if match:
        return match.group(1)
    match = re.search(r'总第(\d+)卷', filename)
    if match:
        return match.group(1) + "_上"
    return None

def split_cases_v2(content, ji_num):
    """将一辑内容拆分为多个案例 - 只处理有[第XX号]的"""
    lines = content.split('\n')
    cases = []
    current_case = None
    case_start_line = 0

    i = 0
    while i < len(lines):
        line = lines[i]

        # 检查是否是案例标题行（含[第XX号]）
        if line.startswith('# ') and '[第' in line:
            # 提取案例编号
            case_num_match = re.search(r'\[第(\d+)号\]', line)
            if case_num_match:
                case_num = case_num_match.group(1)

                # 提取标题（去除案例编号）
                title = re.sub(r'\[第\d+号\]\s*', '', line[2:]).strip()
                title = re.sub(r'\s*[\[（\(【].*', '', title)  # 去除副标题

                # 如果有正在处理的案例，保存它
                if current_case:
                    cases.append({
                        'case_num': current_case['case_num'],
                        'title': current_case['title'],
                        'start_line': current_case['start_line'],
                        'content_lines': current_case['content_lines']
                    })

                # 开始新案例
                current_case = {
                    'case_num': case_num,
                    'title': title,
                    'start_line': i,
                    'content_lines': [line]
                }
            else:
                # 有#但没有案例编号，作为普通章节处理
                if current_case:
                    current_case['content_lines'].append(line)
        elif current_case:
            # 继续当前案例
            current_case['content_lines'].append(line)

        i += 1

    # 保存最后一个案例
    if current_case:
        cases.append({
            'case_num': current_case['case_num'],
            'title': current_case['title'],
            'start_line': current_case['start_line'],
            'content_lines': current_case['content_lines']
        })

    return cases

def generate_synthesis_page(case_info, ji_num):
    """生成 synthesis 页面"""
    title = case_info['title']
    case_num = case_info['case_num']
    content = '\n'.join(case_info['content_lines'])

    # 清理标题
    clean_title = re.sub(r'\s*[\[（\(【].*', '', title).strip()

    # 生成 slug
    slug_title = re.sub(r'[^一-龥a-zA-Z0-9]', '_', clean_title)[:25]
    slug = f"Court_刑事审判参考_{ji_num}辑_{case_num}号_{slug_title}"

    # 提取裁判要旨（从"裁判理由"部分）
    key_point = ""
    reason_match = re.search(r'裁判理由[：:]\s*\n+(.+?)(?=\n##|\n#|$)', content, re.DOTALL)
    if reason_match:
        reason_text = reason_match.group(1).strip()
        paras = reason_text.split('\n')
        for p in paras:
            p = p.strip()
            if p and len(p) > 30 and not p.startswith('#'):
                key_point = p[:200]
                break

    # 生成日期
    import datetime
    today = datetime.date.today().isoformat()

    # 构建页面
    page = f"""---
title: {clean_title}
type: synthesis
created: {today}
updated: {today}
tags: [刑事审判参考, 第{ji_num}辑, 案例第{case_num}号]
case_num: "{case_num}"
ji_num: "{ji_num}"
case_id: "第{case_num}号"
source: ["sources/刑事审判参考/刑事审判参考-100以内/《刑事审判参考 总第{ji_num}辑》.md"]
related: []
---

# {clean_title}

**案例编号**：第{case_num}号
**辑别**：刑事审判参考 总第{ji_num}辑

---

## 案例正文

{content}

---

## 裁判要旨

{key_point if key_point else "（见案例正文）"}

---

## 关联

- 本辑目录：[[Court_刑事审判参考_总第{ji_num}辑_目录.md]]
"""

    return slug, page

def process_file(source_path):
    """处理单个源文件"""
    filename = source_path.name
    ji_num = extract_ji_num(filename)

    if not ji_num:
        print(f"  ⚠️ 无法识别辑号: {filename}")
        return 0

    content = source_path.read_text(encoding='utf-8')
    cases = split_cases_v2(content, ji_num)

    created_count = 0
    skipped_count = 0

    for case in cases:
        slug, page_content = generate_synthesis_page(case, ji_num)
        output_path = OUTPUT_DIR / f"{slug}.md"

        # 检查是否已存在
        if output_path.exists():
            skipped_count += 1
            continue

        output_path.write_text(page_content, encoding='utf-8')
        created_count += 1

    return created_count, skipped_count

def main():
    print("=" * 60)
    print("刑事审判参考 1-28辑 批量Ingest v2")
    print("=" * 60)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total_created = 0
    total_skipped = 0
    total_files = 0

    for filename in SOURCE_FILES:
        source_path = SOURCE_DIR / filename

        if not source_path.exists():
            print(f"⚠️ 文件不存在: {filename}")
            continue

        print(f"\n处理: {filename}")
        created, skipped = process_file(source_path)
        print(f"  → 新增 {created} 个案例页 (已存在 {skipped} 个)")
        total_created += created
        total_skipped += skipped
        total_files += 1

    print("\n" + "=" * 60)
    print(f"完成！处理 {total_files} 个文件，新增 {total_created} 个案例页")
    print(f"已存在跳过: {total_skipped} 个")
    print("=" * 60)

if __name__ == "__main__":
    main()