#!/usr/bin/env python3
"""
Batch process 最高法指导性案例 from sources/2-案例库/最高法-指导性案例/
Target: wiki/syntheses/SPC_GuideCase_指导案例XXX号.md
"""
import os
import re
from pathlib import Path
from datetime import datetime

VAULT = Path("D:/AI agent/tkk-library")
SOURCE_DIR = VAULT / "sources/2-案例库/最高法-指导性案例"
TARGET_DIR = VAULT / "wiki/syntheses"

TODAY = "2026-05-09"

def extract_case_info(content, src_path):
    """Extract case information from source file"""
    info = {
        "num": "",
        "name": "",
        "guoyan": "",  # 裁判要点
        "anjian": "",   # 基本案情
        "jieguo": "",   # 裁判结果
        "liyou": ""     # 裁判理由
    }

    # Extract case number from first line: 指导案例XXX号 或 指导性案例XXX号
    num_match = re.search(r'指导性?案例(\d+)号', content)
    if num_match:
        info["num"] = num_match.group(1)

    # Extract case name - from lines after case number until **关键词
    # The name may span multiple lines
    name_match = re.search(r'指导案例\d+号\s*\n([^\n]+(?:\n[^\n]+){0,5}?)(?=\n\s*\*\*|$)', content)
    if name_match:
        name = name_match.group(1).replace('\n', '').replace('**', '').strip()
        name = re.sub(r'\*+', '', name)
        info["name"] = name[:100]

    # Extract 裁判要点
    guoyan_match = re.search(r'\*\*裁判要点\*\*\s*(.+?)(?=\n\s*\*\*|$)', content, re.DOTALL)
    if guoyan_match:
        info["guoyan"] = guoyan_match.group(1).strip()[:500]

    # Extract 基本案情
    anjian_match = re.search(r'\*\*基本案情\*\*\s*(.+?)(?=\n\s*\*\*裁判|$)', content, re.DOTALL)
    if anjian_match:
        info["anjian"] = anjian_match.group(1).strip()[:2000]

    # Extract 裁判结果
    jieguo_match = re.search(r'\*\*裁判结果\*\*\s*(.+?)(?=\n\s*\*\*裁判|$)', content, re.DOTALL)
    if jieguo_match:
        info["jieguo"] = jieguo_match.group(1).strip()[:500]

    # Extract 裁判理由
    liyou_match = re.search(r'\*\*裁判理由\*\*\s*(.+?)(?=\n\s*[\*\(（]|$)', content, re.DOTALL)
    if liyou_match:
        info["liyou"] = liyou_match.group(1).strip()[:1500]

    return info

def generate_synthesis(info, src_path):
    """Generate synthesis markdown"""
    case_name = info['name'] or f"指导案例{info['num']}号"
    case_num = info['num']

    content = f"""---
title: {case_name}
type: synthesis
created: {TODAY}
updated: {TODAY}
tags: [民事, 最高法, 指导性案例, 指导案例{case_num}号]
source: "{src_path}"
related: []
案例分级: ⭐⭐⭐⭐⭐
问题意识: {case_name}的裁判要点
---

## 案情

### 基本信息

| 字段 | 内容 |
|------|------|
| 案号 | 指导案例{case_num}号 |
| 发布机关 | 最高人民法院 |
| 案例名称 | {case_name} |

## 裁判要点

{info['guoyan'] or '（详见原文）'}

## 基本案情

{info['anjian'] or '（详见原文）'}

## 裁判结果

{info['jieguo'] or '（详见原文）'}

## 裁判理由

{info['liyou'] or '（详见原文）'}
"""
    return content

def process_file(src_path):
    """Process a single source file"""
    try:
        with open(src_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract case number
        num_match = re.search(r'指导案例(\d+)号', content)
        if not num_match:
            return [("error", f"{src_path.name}: 无法提取案号")]

        case_num = num_match.group(1)
        target_name = f"SPC_GuideCase_指导案例{case_num}号.md"
        # Check if already exists with different naming
        if not target_path.exists():
            alt_name = f"SPC_GuideCase_指导性案例{case_num}号.md"
            alt_path = TARGET_DIR / alt_name
            if alt_path.exists():
                target_name = alt_name
                target_path = alt_path
        target_path = TARGET_DIR / target_name

        # Skip if exists
        if target_path.exists():
            return [("skip", target_name)]

        rel_path = str(src_path).replace(str(VAULT) + "/", "")

        info = extract_case_info(content, rel_path)
        synthesis = generate_synthesis(info, rel_path)

        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(synthesis)

        return [("ok", target_name)]
    except Exception as e:
        return [("error", f"{src_path.name}: {str(e)[:50]}")]

def main():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 开始处理最高法指导性案例...")

    source_files = list(SOURCE_DIR.glob("*.md"))
    total = len(source_files)
    print(f"总计 {total} 个源文件")

    stats = {"ok": 0, "skip": 0, "error": 0}
    errors = []

    for i, src_path in enumerate(sorted(source_files)):
        if (i + 1) % 50 == 0:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 已处理 {i+1}/{total}")

        results = process_file(src_path)
        for status, detail in results:
            stats[status] += 1
            if status == "error":
                errors.append(detail)

    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 处理完成!")
    print(f"成功: {stats['ok']}, 跳过: {stats['skip']}, 错误: {stats['error']}")

    if errors:
        print("\n错误列表:")
        for e in errors[:10]:
            print(f"  - {e}")

    return stats

if __name__ == "__main__":
    main()
