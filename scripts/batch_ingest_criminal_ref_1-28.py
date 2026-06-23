#!/usr/bin/env python3
"""
刑事审判参考批量Ingest脚本 - 处理1-28辑
按辑处理，每辑拆分为多个案例页
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
    # 特殊处理"总第3卷 上辑"
    match = re.search(r'总第(\d+)卷', filename)
    if match:
        return match.group(1) + "_上"
    return None

def split_cases(content, ji_num):
    """将一辑内容拆分为多个案例"""
    lines = content.split('\n')
    cases = []
    current_case = None

    i = 0
    while i < len(lines):
        line = lines[i]

        # 案例标题行：以 # 开头，后面是案例名称
        # 匹配模式：# 案例名称 或 ## 一、基本案情 等章节
        if line.startswith('# ') and len(line) > 3:
            title = line[2:].strip()

            # 跳过非案例标题
            skip_keywords = [
                '编辑说明', '特邀编辑', '征稿启事', '征订单', '汇款方法',
                '调查问卷', '读者反馈', '目录', '刑事审判参考', '编辑委员会',
                '发刊词', '本期要目', '出版', '发行', '法律出版社'
            ]
            if any(kw in title for kw in skip_keywords):
                i += 1
                continue

            # 跳过太短的标题
            if len(title) < 4:
                i += 1
                continue

            # 跳过无意义的标题
            if title in ['【指导案例】', '【经验交流】', '【大案传真】',
                        '【立法、司法规范】', '【疑案争鸣】', '案例']:
                i += 1
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

        i += 1

    if current_case:
        cases.append(current_case)

    return cases

def generate_synthesis_page(case_info, ji_num, case_index, total_cases):
    """生成 synthesis 页面"""
    title = case_info['title']
    content = '\n'.join(case_info['content_lines'])

    # 提取案例编号
    case_num_match = re.search(r'\[第(\d+)号\]', content)
    if case_num_match:
        case_num = case_num_match.group(1)
    else:
        # 从标题中提取或生成
        case_num = f"{ji_num}_{case_index + 1}"

    # 清理标题
    clean_title = re.sub(r'\[第\d+号\]\s*', '', title).strip()
    clean_title = re.sub(r'\s*[\[（\(【].*', '', clean_title)

    # 生成 slug
    slug_title = re.sub(r'[^一-龥a-zA-Z0-9]', '_', clean_title)[:25]
    slug = f"Court_刑事审判参考_{ji_num}辑_{case_num}号_{slug_title}"

    # 提取裁判要旨（从"裁判理由"部分）
    key_point = ""
    reason_match = re.search(r'裁判理由[：:]\s*\n+(.+?)(?=\n##|\n#|$)', content, re.DOTALL)
    if reason_match:
        reason_text = reason_match.group(1).strip()
        # 取第一段作为关键点
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
    cases = split_cases(content, ji_num)

    created_count = 0
    for idx, case in enumerate(cases):
        slug, page_content = generate_synthesis_page(case, ji_num, idx, len(cases))
        output_path = OUTPUT_DIR / f"{slug}.md"

        # 检查是否已存在
        if output_path.exists():
            # 跳过已存在的
            continue

        output_path.write_text(page_content, encoding='utf-8')
        created_count += 1

    return created_count

def main():
    print("=" * 60)
    print("刑事审判参考 1-28辑 批量Ingest")
    print("=" * 60)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total_created = 0
    total_files = 0

    for filename in SOURCE_FILES:
        source_path = SOURCE_DIR / filename

        if not source_path.exists():
            print(f"⚠️ 文件不存在: {filename}")
            continue

        print(f"\n处理: {filename}")
        count = process_file(source_path)
        print(f"  → 新增 {count} 个案例页")
        total_created += count
        total_files += 1

    print("\n" + "=" * 60)
    print(f"完成！处理 {total_files} 个文件，新增 {total_created} 个案例页")
    print("=" * 60)

if __name__ == "__main__":
    main()