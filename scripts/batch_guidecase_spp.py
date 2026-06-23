#!/usr/bin/env python3
"""
Batch process 最高检指导性案例 from sources/2-案例库/最高检-指导性案例/
Target: wiki/syntheses/SPP_GuideCase_检例第X号.md
"""
import os
import re
from pathlib import Path
from datetime import datetime

VAULT = Path("D:/AI agent/tkk-library")
SOURCE_DIR = VAULT / "sources/2-案例库/最高检-指导性案例"
TARGET_DIR = VAULT / "wiki/syntheses"

TODAY = "2026-05-09"

def extract_cases_from_content(content, src_path):
    """Extract individual cases from a batch file"""
    cases = []

    # Pattern: **案例名**\n**（检例第X号）**
    # Split by the pattern: **（检例第X号）**
    pattern = r'\*\*（检例第(\d+)号）\*\*'
    parts = re.split(pattern, content)

    # parts[0] = content before first case (header)
    # parts[1] = case num, parts[2] = content until next case num, etc.

    i = 1
    while i < len(parts):
        case_num = parts[i].strip()
        case_content = parts[i + 1] if i + 1 < len(parts) else ""

        if case_num and case_content:
            # Extract case name - it's right before **（检例第X号）**
            # Find the text between previous \n** and **（检例
            prev_marker = f"**（检例第{case_num}号）**"
            idx = content.find(prev_marker)
            if idx > 0:
                # Go back to find ** before the name
                start = max(0, idx - 500)
                segment = content[start:idx]
                # Find ** that starts the name
                name_matches = list(re.finditer(r'\*\*([^*]+)\*\*$', segment, re.MULTILINE))
                if name_matches:
                    case_name = name_matches[-1].group(1).strip()
                else:
                    case_name = f"检例第{case_num}号"
            else:
                case_name = f"检例第{case_num}号"

            # Extract sections
            yizhi_match = re.search(r'【要旨】\s*(.+?)(?=\n\s*【|【[^一-龥]|$)', case_content, re.DOTALL)
            yizhi = yizhi_match.group(1).strip()[:500] if yizhi_match else ""

            anjian_match = re.search(r'【基本案情】\s*(.+?)(?=\n\s*【|【[^一-龥]|$)', case_content, re.DOTALL)
            anjian = anjian_match.group(1).strip()[:2000] if anjian_match else ""

            guocheng_match = re.search(r'【诉讼过程[和与]结果】\s*(.+?)(?=\n\s*【|【[^一-龥]|$)', case_content, re.DOTALL)
            guocheng = guocheng_match.group(1).strip()[:1000] if guocheng_match else ""

            cases.append({
                "num": case_num,
                "name": case_name,
                "yizhi": yizhi,
                "anjian": anjian,
                "guocheng": guocheng,
            })

        i += 2

    return cases

def generate_synthesis(case_info, src_path):
    """Generate synthesis markdown for a single case"""
    case_name = case_info['name']
    case_num = case_info['num']

    content = f"""---
title: {case_name}
type: synthesis
created: {TODAY}
updated: {TODAY}
tags: [刑事, 最高检, 指导性案例, 检例第{case_num}号]
source: "{src_path}"
related: []
案例分级: ⭐⭐⭐⭐⭐
问题意识: {case_name}的裁判要旨
---

## 案情

### 基本信息

| 字段 | 内容 |
|------|------|
| 案号 | 检例第{case_num}号 |
| 发布机关 | 最高人民检察院 |
| 案例名称 | {case_name} |

## 裁判要旨

{case_info['yizhi'] or '（详见原文）'}

## 基本案情

{case_info['anjian'] or '（详见原文）'}

## 诉讼过程

{case_info['guocheng'] or '（详见原文）'}
"""
    return content

def process_file(src_path):
    """Process a single source file (batch)"""
    try:
        with open(src_path, 'r', encoding='utf-8') as f:
            content = f.read()

        rel_path = str(src_path).replace(str(VAULT) + "/", "")

        # Extract individual cases
        cases = extract_cases_from_content(content, rel_path)

        results = []
        for case in cases:
            target_name = f"SPP_GuideCase_检例第{case['num']}号.md"
            target_path = TARGET_DIR / target_name

            # Skip if exists
            if target_path.exists():
                results.append(("skip", target_name))
                continue

            synthesis = generate_synthesis(case, rel_path)
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(synthesis)
            results.append(("ok", target_name))

        return results
    except Exception as e:
        return [("error", f"{src_path.name}: {str(e)[:100]}")]

def main():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 开始处理最高检指导性案例...")

    source_files = list(SOURCE_DIR.glob("*.md"))
    total = len(source_files)
    print(f"总计 {total} 个源文件")

    stats = {"ok": 0, "skip": 0, "error": 0}
    errors = []

    for i, src_path in enumerate(sorted(source_files)):
        if (i + 1) % 10 == 0:
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
