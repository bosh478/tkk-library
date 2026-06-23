#!/usr/bin/env python3
"""
Batch process 入库案例 from sources/2-案例库/入库案例/
Target: wiki/syntheses/Court_入库案例_YYYYMMDD_XXX.md
"""
import os
import re
from pathlib import Path
from datetime import datetime

VAULT = Path("D:/AI agent/tkk-library")
SOURCE_DIR = VAULT / "sources/2-案例库/入库案例"
TARGET_DIR = VAULT / "wiki/syntheses"

TODAY = "2026-05-09"

def extract_case_info(content, src_path):
    """Extract case information from source file"""
    info = {
        "name": "",
        "court": "",
        "case_num": "",
        "date": "",
        "anyou": "",
        "入库编号": "",
        "guoyan": "",
        "anjian": "",
    }

    lines = content.split("\n")

    # Extract name (first non-empty line)
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            info["name"] = line[:100]
            break

    # Extract fields
    for i, line in enumerate(lines):
        line = line.strip()
        if "审理法院" in line and i + 1 < len(lines):
            info["court"] = lines[i + 1].strip()
        elif "案号" in line and i + 1 < len(lines):
            info["case_num"] = lines[i + 1].strip()
        elif "裁判日期" in line and i + 1 < len(lines):
            info["date"] = lines[i + 1].strip()
        elif "案由" in line and i + 1 < len(lines):
            info["anyou"] = lines[i + 1].strip()
        elif "入库编号" in line and i + 1 < len(lines):
            info["入库编号"] = lines[i + 1].strip()
        elif "––" in line:
            info["guoyan"] = line.split("––")[-1].strip()[:200]
        elif "基本案情" in line and i + 1 < len(lines):
            # Collect next few lines as 基本案情
            aj_lines = []
            for j in range(i + 1, min(i + 50, len(lines))):
                if lines[j].strip() and not lines[j].strip().startswith("关键词"):
                    aj_lines.append(lines[j].strip())
                else:
                    break
            info["anjian"] = "".join(aj_lines)[:2000]

    return info

def generate_synthesis(info, src_path):
    """Generate synthesis markdown"""
    name = info['name'] or "入库案例"
    入库编号 = info['入库编号'].replace("-", "") if info['入库编号'] else ""

    # Determine category from anyou
    category = "民事"
    if info['anyou']:
        if "刑事" in info['anyou']:
            category = "刑事"
        elif "行政" in info['anyou']:
            category = "行政"
        elif "执行" in info['anyou']:
            category = "执行"

    target_name = f"Court_入库案例_{name[:30]}.md"
    # Sanitize filename
    target_name = re.sub(r'[<>:"/\\|?*]', '_', target_name)

    content = f"""---
title: {name}
type: synthesis
created: {TODAY}
updated: {TODAY}
tags: [{category}, 入库案例, {info['court']}, {info['anyou'].split("/")[-1] if info['anyou'] else ""}]
source: "{src_path}"
related: []
案例分级: ⭐⭐⭐⭐
问题意识: {info['guoyan'] or info['anyou'] or '入库案例裁判要旨'}
---

## 案情

### 基本信息

| 字段 | 内容 |
|------|------|
| 案号 | {info['case_num']} |
| 审理法院 | {info['court']} |
| 裁判日期 | {info['date']} |
| 案由 | {info['anyou']} |
| 入库编号 | {info['入库编号']} |

## 裁判要旨

{info['guoyan'] or '（详见原文）'}

## 基本案情

{info['anjian'] or '（详见原文）'}
"""
    return target_name, content

def process_file(src_path):
    """Process a single source file"""
    try:
        with open(src_path, 'r', encoding='utf-8') as f:
            content = f.read()

        rel_path = str(src_path).replace(str(VAULT) + "/", "")

        info = extract_case_info(content, rel_path)
        target_name, synthesis = generate_synthesis(info, rel_path)

        target_path = TARGET_DIR / target_name

        # Handle duplicate names
        if target_path.exists():
            base_name = target_name.replace(".md", "")
            for i in range(1, 100):
                alt_name = f"{base_name}_{i}.md"
                alt_path = TARGET_DIR / alt_name
                if not alt_path.exists():
                    target_path = alt_path
                    break

        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(synthesis)

        return [("ok", target_name)]
    except Exception as e:
        return [("error", f"{src_path.name}: {str(e)[:50]}")]

def main():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 开始处理入库案例...")

    source_files = list(SOURCE_DIR.rglob("*.md"))
    total = len(source_files)
    print(f"总计 {total} 个源文件")

    stats = {"ok": 0, "skip": 0, "error": 0}
    errors = []

    for i, src_path in enumerate(sorted(source_files)):
        if (i + 1) % 100 == 0:
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
