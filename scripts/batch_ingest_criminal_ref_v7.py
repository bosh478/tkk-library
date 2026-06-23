#!/usr/bin/env python3
"""
刑事审判参考批量Ingest脚本 v7 - 处理未整理的辑(1-34, 43-48, 84-88)
改进版：正确处理目录格式差异

第1-8,10-34辑：目录中无[第XX号]格式，案例用顺序号
第36-82辑：目录中有[第XX号]格式
第3卷上辑：[原第XX号]在分类行
第88辑：实际上是刑诉法解释，不是案例集
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
OUTPUT_DIR = VAULT_ROOT / "wiki/syntheses/Court_刑事审判参考"

# 需要处理的源文件列表（按格式分组）
# A组：目录有案例编号的（第36辑以后）
FILES_WITH_CASE_NUM = [
    "《刑事审判参考 总第43辑》.md",
    "《刑事审判参考 总第44辑》.md",
    "《刑事审判参考 总第45辑》.md",
    "《刑事审判参考 总第46辑》.md",
    "《刑事审判参考 总第47辑》.md",
    "《刑事审判参考 总第48辑》.md",
    "《刑事审判参考 总第84辑》.md",
    "《刑事审判参考 总第85辑》.md",
    "《刑事审判参考 总第86辑》.md",
    "《刑事审判参考 总第87辑》.md",
]

# B组：目录无案例编号，用顺序提取（第1-34辑）
FILES_WITHOUT_CASE_NUM = [
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

def parse_toc_with_case_num(content, ji_num):
    """解析目录（目录有[第XX号]格式）"""
    cases_toc = []
    lines = content.split('\n')

    for i, line in enumerate(lines):
        line = line.strip()
        # 格式: 案例名[第XX号]-副标题 或 案例名[第XX号]
        if '[第' in line and '号]' in line:
            m = re.search(r'([^[]+)\[第(\d+)号\](.*)', line)
            if m:
                title = m.group(1).strip()
                case_num = m.group(2)
                subtitle = m.group(3).strip()
                if subtitle:
                    title = title + subtitle
                if title.endswith('案'):
                    title = title[:-1]
                cases_toc.append((case_num, title))

    return cases_toc

def parse_toc_without_case_num(content, ji_num):
    """解析目录（目录无案例编号格式）- 按位置顺序分配编号"""
    cases_toc = []
    lines = content.split('\n')

    # 找到【案例】部分开始的位置
    case_start = -1
    for i, line in enumerate(lines):
        if '【案例】' in line or '【案例】' in line:
            case_start = i
            break

    if case_start == -1:
        return cases_toc

    # 从案例部分开始，收集案例标题
    case_num = 1  # 从1开始分配编号
    for i in range(case_start + 1, len(lines)):
        line = lines[i].strip()

        # 跳过空行和非标题行
        if not line or line.startswith('#') or line.startswith('【') or line.startswith('['):
            continue

        # 检查是否是案例标题（以"案"结尾或包含常见罪名）
        crime_keywords = ['走私', '诈骗', '盗窃', '抢劫', '杀人', '伤害', '强奸', '贩卖',
                         '受贿', '贪污', '非法', '贩毒', '赌博', '绑架', '拐卖', '重婚',
                         '交通', '伪造', '侵占', '敲诈', '寻衅', '经营', '爆炸', '持有']

        is_case = False
        for kw in crime_keywords:
            if kw in line:
                is_case = True
                break

        if is_case:
            title = line
            if title.endswith('案'):
                title = title[:-1]
            # 清理多余的空白字符
            title = ' '.join(title.split())
            cases_toc.append((str(case_num), title))
            case_num += 1

    return cases_toc

def extract_case_content(content, case_title, case_num, ji_num):
    """从源文件中提取案例的完整内容"""
    # 尝试多种模式匹配
    patterns = [
        f"# {case_title}\n",
        f"## {case_title}\n",
        f"# {case_title}",
        f"## {case_title}",
    ]

    start_pos = -1
    for pattern in patterns:
        pos = content.find(pattern)
        if pos != -1:
            start_pos = pos
            break

    if start_pos == -1:
        # 尝试模糊匹配（取前15个字）
        short_title = case_title[:15]
        for i, line in enumerate(content.split('\n')):
            if short_title in line and ('# ' in line or '## ' in line):
                start_pos = content.find(line)
                break

    if start_pos == -1:
        return None

    # 提取案例内容
    remaining = content[start_pos:]
    lines = remaining.split('\n')

    # 找到下一个案例（下一个 # 标题）
    case_end = len(lines)
    for i in range(3, min(len(lines), 200)):
        line = lines[i].strip()
        if (line.startswith('# ') or line.startswith('## 【')) and i > 10:
            case_end = i
            break

    case_content = '\n'.join(lines[:case_end])
    return case_content[:6000] if case_content else None

def generate_wiki_content(case_num, case_title, ji_num, case_content, source_file, line_refs):
    """生成wiki页面内容"""
    tags = ["刑事审判参考", f"第{ji_num}辑"]

    # 常见罪名关键词
    crime_keywords = ['盗窃', '抢劫', '诈骗', '故意杀人', '故意伤害', '强奸', '贩卖毒品',
                      '受贿', '贪污', '走私', '非法经营', '敲诈勒索', '寻衅滋事',
                      '交通肇事', '危险驾驶', '绑架', '拐卖', '组织卖淫', '赌博',
                      '毒品', '重婚', '伪造', '侵占', '爆炸', '持有']

    for kw in crime_keywords:
        if kw in case_title:
            tags.append(kw)
            break

    frontmatter = f'''---
title: {case_title}
type: synthesis
created: 2026-05-17
updated: 2026-05-17
tags: [{", ".join(tags)}]
case_num: 第{case_num}号
ji_num: {ji_num}
source: "sources/刑事审判参考/刑事审判参考-100以内/{source_file}"
related: []
line-refs: {line_refs}
---

# {case_title}

'''

    if case_content:
        frontmatter += case_content[:6000]
    else:
        frontmatter += "## 基本案情\n\n（内容待提取）\n"

    return frontmatter

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    stats = {'processed': 0, 'skipped': 0, 'errors': 0}

    # 处理有案例编号的
    print("=== 处理 A组（有案例编号格式） ===")
    for source_file in FILES_WITH_CASE_NUM:
        source_path = SOURCE_DIR / source_file
        if not source_path.exists():
            print(f"⚠️ 文件不存在: {source_file}")
            stats['errors'] += 1
            continue

        ji_num = extract_ji_num(source_file)
        if not ji_num:
            print(f"⚠️ 无法提取辑号: {source_file}")
            stats['errors'] += 1
            continue

        print(f"\n处理: {source_file} (辑{ji_num})")
        content = source_path.read_text(encoding='utf-8')

        cases_toc = parse_toc_with_case_num(content, ji_num)
        print(f"  发现 {len(cases_toc)} 个案例")

        for case_num, case_title in cases_toc:
            # 更彻底地清理标题中的非法字符
            import unicodedata
            safe_title = unicodedata.normalize('NFKC', case_title)
            safe_title = ''.join(c for c in safe_title if c.isalnum() or c in ' _-').strip()
            if not safe_title:
                safe_title = f"案例{case_num}"
            safe_title = safe_title[:40]
            wiki_filename = f"Court_刑事审判参考_{ji_num}辑_{case_num}号_{safe_title}.md"
            wiki_path = OUTPUT_DIR / wiki_filename

            if wiki_path.exists():
                stats['skipped'] += 1
                continue

            case_content = extract_case_content(content, case_title, case_num, ji_num)

            # 查找行号
            line_refs = {f'"{source_file}"': []}
            for i, line in enumerate(content.split('\n'), 1):
                if case_title[:10] in line:
                    line_refs[f'"{source_file}"'].append(i)
                    if len(line_refs[f'"{source_file}"']) >= 3:
                        break

            wiki_content = generate_wiki_content(case_num, case_title, ji_num, case_content, source_file, line_refs)
            wiki_path.write_text(wiki_content, encoding='utf-8')
            stats['processed'] += 1

    # 处理无案例编号的（按顺序分配编号）
    print("\n=== 处理 B组（无案例编号格式） ===")
    for source_file in FILES_WITHOUT_CASE_NUM:
        source_path = SOURCE_DIR / source_file
        if not source_path.exists():
            print(f"⚠️ 文件不存在: {source_file}")
            stats['errors'] += 1
            continue

        ji_num = extract_ji_num(source_file)
        if not ji_num:
            print(f"⚠️ 无法提取辑号: {source_file}")
            stats['errors'] += 1
            continue

        print(f"\n处理: {source_file} (辑{ji_num})")
        content = source_path.read_text(encoding='utf-8')

        cases_toc = parse_toc_without_case_num(content, ji_num)
        print(f"  发现 {len(cases_toc)} 个案例")

        for case_num, case_title in cases_toc:
            if not case_title or len(case_title) < 2:
                continue

            # 更彻底地清理标题中的非法字符
            import unicodedata
            safe_title = unicodedata.normalize('NFKC', case_title)
            safe_title = ''.join(c for c in safe_title if c.isalnum() or c in ' _-').strip()
            if not safe_title:
                safe_title = f"案例{case_num}"
            safe_title = safe_title[:40]
            wiki_filename = f"Court_刑事审判参考_{ji_num}辑_{case_num}号_{safe_title}.md"
            wiki_path = OUTPUT_DIR / wiki_filename

            if wiki_path.exists():
                stats['skipped'] += 1
                continue

            case_content = extract_case_content(content, case_title, case_num, ji_num)

            line_refs = {f'"{source_file}"': []}
            for i, line in enumerate(content.split('\n'), 1):
                if case_title[:10] in line:
                    line_refs[f'"{source_file}"'].append(i)
                    if len(line_refs[f'"{source_file}"']) >= 3:
                        break

            wiki_content = generate_wiki_content(case_num, case_title, ji_num, case_content, source_file, line_refs)
            wiki_path.write_text(wiki_content, encoding='utf-8')
            stats['processed'] += 1
            print(f"  创建: {case_num}号 {case_title[:25]}...")

    print(f"\n=== 处理完成 ===")
    print(f"已处理: {stats['processed']}")
    print(f"跳过(已存在): {stats['skipped']}")
    print(f"错误: {stats['errors']}")

if __name__ == '__main__':
    main()