#!/usr/bin/env python3
"""
刑事审判参考批量Ingest脚本 v6 - 处理未整理的辑(1-34, 43-48, 84-88)
基于v5脚本改进，专门处理未按规范整理的文件

文件命名格式: Court_刑事审判参考_{辑号}辑_{案例号}号_{标题}.md
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

# 需要处理的源文件列表（未整理的辑）
SOURCE_FILES = [
    # 1-34 未整理
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
    # 43-48 未整理
    "《刑事审判参考 总第43辑》.md",
    "《刑事审判参考 总第44辑》.md",
    "《刑事审判参考 总第45辑》.md",
    "《刑事审判参考 总第46辑》.md",
    "《刑事审判参考 总第47辑》.md",
    "《刑事审判参考 总第48辑》.md",
    # 84-88 未整理
    "《刑事审判参考 总第84辑》.md",
    "《刑事审判参考 总第85辑》.md",
    "《刑事审判参考 总第86辑》.md",
    "《刑事审判参考 总第87辑》.md",
    "《刑事审判参考 总第88辑》.md",
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

def parse_toc_cases(content, ji_num):
    """从目录中提取案例编号和标题的对应关系"""
    cases_toc = []
    lines = content.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # 格式1：[第XX号] 在行中（如第10辑的目录）
        if '[第' in line and '号]' in line:
            m = re.search(r'\[第(\d+)号\]', line)
            if m:
                case_num = m.group(1)
                title_part = line.split('[')[0].strip()
                if title_part and len(title_part) > 2:
                    if title_part.endswith('案'):
                        title_part = title_part[:-1]
                    cases_toc.append((case_num, title_part))
                    i += 1
                    continue

        # 格式2：案例名[第XX号]-副标题（第1辑等）
        if '[' in line and '第' in line and '号]' in line:
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
                i += 1
                continue

        # 格式3：[原第XX号]在分类行，标题在下一行（如第3卷上辑）
        if '[原第' in line and '号]' in line:
            m = re.search(r'\[原第(\d+)号\]', line)
            if m:
                case_num = m.group(1)
                # 标题可能在下一行
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line and not next_line.startswith('[') and not next_line.startswith('#'):
                        title = next_line
                        if title.endswith('案'):
                            title = title[:-1]
                        cases_toc.append((case_num, title))
                        i += 2
                        continue
                cases_toc.append((case_num, f"案例{case_num}"))
                i += 1
                continue

        i += 1

    return cases_toc

def extract_case_content(content, case_title, case_num, ji_num):
    """从源文件中提取案例的完整内容"""
    # 找到案例标题位置
    case_patterns = [
        f"# {case_title}",
        f"# {case_title}\n",
        f"## {case_title}",
        f"# {case_title.replace('-', ' ')}",
    ]

    start_pos = -1
    for pattern in case_patterns:
        pos = content.find(pattern)
        if pos != -1:
            start_pos = pos
            break

    if start_pos == -1:
        # 尝试模糊匹配
        for line in content.split('\n'):
            if case_title in line and ('# ' in line or '## ' in line):
                start_pos = content.find(line)
                break

    if start_pos == -1:
        return None

    # 提取案例内容（到下一个案例或下一节之前）
    remaining = content[start_pos + 1000:]
    next_case = -1
    next_section = -1

    # 寻找下一个案例
    lines = remaining.split('\n')
    for i, line in enumerate(lines):
        if line.strip().startswith('# ') and i > 5:
            next_case = i
            break

    if next_case > 0:
        case_content = remaining[:next_case * 100]  # 粗略估计
    else:
        # 找到下一个 # 标题
        for i, line in enumerate(lines):
            if (line.startswith('# ') or line.startswith('## ')) and i > 10:
                next_section = i
                break
        if next_section > 0:
            case_content = remaining[:next_section * 100]
        else:
            case_content = remaining[:8000]

    return case_content[:8000] if case_content else None

def generate_wiki_content(case_num, case_title, ji_num, case_content, source_file, line_refs):
    """生成wiki页面内容"""
    # 提取罪名/问题类型
    tags = ["刑事审判参考", f"第{ji_num}辑"]

    # 常见罪名关键词
    crime_keywords = ['盗窃', '抢劫', '诈骗', '故意杀人', '故意伤害', '强奸', '贩卖毒品',
                      '受贿', '贪污', '走私', '非法经营', '敲诈勒索', '寻衅滋事',
                      '交通肇事', '危险驾驶', '绑架', '拐卖', '组织卖淫', '赌博']

    for kw in crime_keywords:
        if kw in case_title:
            tags.append(kw)
            break

    # 生成 frontmatter
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

    # 添加内容（如果提取到的话）
    if case_content:
        # 截取关键部分
        body = case_content[:6000]
        frontmatter += body
    else:
        frontmatter += "## 基本案情\n\n（内容待提取）\n"

    return frontmatter

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    stats = {
        'processed': 0,
        'skipped': 0,
        'errors': 0
    }

    for source_file in SOURCE_FILES:
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

        # 解析目录获取案例列表
        cases_toc = parse_toc_cases(content, ji_num)
        print(f"  发现 {len(cases_toc)} 个案例")

        # 逐个案例生成 wiki 文件
        for case_num, case_title in cases_toc:
            # 生成文件名
            safe_title = case_title.replace('/', '-').replace('\\', '-')[:30]
            wiki_filename = f"Court_刑事审判参考_{ji_num}辑_{case_num}号_{safe_title}.md"
            wiki_path = OUTPUT_DIR / wiki_filename

            # 检查是否已存在
            if wiki_path.exists():
                print(f"  跳过(已存在): {case_num}号 {case_title[:20]}")
                stats['skipped'] += 1
                continue

            # 提取案例内容
            case_content = extract_case_content(content, case_title, case_num, ji_num)

            # 生成行号引用
            line_refs = {f'"{source_file}"': []}
            # 简单搜索定位
            for i, line in enumerate(content.split('\n'), 1):
                if case_title[:10] in line:
                    line_refs[f'"{source_file}"'].append(i)
                    if len(line_refs[f'"{source_file}"']) >= 5:
                        break

            # 生成 wiki 内容
            wiki_content = generate_wiki_content(case_num, case_title, ji_num, case_content, source_file, line_refs)

            # 写入文件
            wiki_path.write_text(wiki_content, encoding='utf-8')
            print(f"  创建: {case_num}号 {case_title[:25]}...")
            stats['processed'] += 1

    print(f"\n=== 处理完成 ===")
    print(f"已处理: {stats['processed']}")
    print(f"跳过(已存在): {stats['skipped']}")
    print(f"错误: {stats['errors']}")

if __name__ == '__main__':
    main()