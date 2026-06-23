#!/usr/bin/env python3
"""
Batch process 公报案例 (Gazette Cases) from sources/2-案例库/公报案例/
Target: wiki/syntheses/GuideCase_案号.md
"""
import os
import re
from pathlib import Path
from datetime import datetime

VAULT = Path("D:/AI agent/tkk-library")
SOURCE_DIR = VAULT / "sources/2-案例库/公报案例"
TARGET_DIR = VAULT / "wiki/syntheses"

TODAY = "2026-05-09"

def extract_case_info(content, src_path):
    """Extract case information from source file"""
    info = {
        "案号": "",
        "审理法院": "最高人民法院",
        "裁判日期": "",
        "案由": "",
        "当事人": "",
        "案件事实": "",
        "裁判理由": "",
        "判决结果": "",
        "案件名称": ""
    }

    lines = content.split("\n")
    current_section = ""
    section_content = []

    for i, line in enumerate(lines):
        line = line.strip()

        # 提取案号（括号内的内容）
        if not info["案号"] and re.match(r'^#\s*\(', line):
            info["案号"] = re.search(r'\(([^)]+)\)', line).group(1) if re.search(r'\(([^)]+)\)', line) else ""
            # 尝试从内容中提取案件名称（去掉案号后）
            name_match = re.sub(r'\([^)]*\)', '', line).strip()
            name_match = re.sub(r'^[一二三四五六七八九十]+、', '', name_match)
            info["案件名称"] = name_match if name_match else ""

        # 提取关键信息
        if "审理法院" in line or "法院" in line[:10]:
            match = re.search(r'法院[：:]\s*([^　\s]+)', line)
            if match:
                info["审理法院"] = match.group(1)

        if "裁判日期" in line or "日期" in line[:10]:
            match = re.search(r'(\d{4}[./-]\d{1,2}[./-]\d{1,2})', line)
            if match:
                info["裁判日期"] = match.group(1).replace("/", "-").replace(".", "-")

        if "案由" in line[:10]:
            parts = line.split("：")
            if len(parts) > 1:
                info["案由"] = parts[-1].strip()
            elif len(lines) > i + 1 and "案由" not in lines[i+1]:
                info["案由"] = lines[i+1].strip()

        # 收集主要内容
        if any(kw in line for kw in ["上诉人", "被上诉人", "原告", "被告", "当事人"]):
            info["当事人"] += line + "\n"

        if "法院认为" in line or "本院认为" in line:
            current_section = "裁判理由"
            section_content = [line]
        elif "判决如下" in line or "裁判结果" in line:
            current_section = "判决结果"
            section_content = [line]
        elif "案情" in line and len(line) < 20:
            current_section = "案件事实"
            section_content = []
        elif current_section == "裁判理由" and line:
            section_content.append(line)
        elif current_section == "判决结果" and line:
            section_content.append(line)
        elif current_section == "案件事实" and line and len(line) > 20:
            section_content.append(line)

    info["裁判理由"] = "\n".join(section_content[:20]) if section_content else ""

    if not info["案件名称"]:
        # 从案由提取
        if info["案由"]:
            info["案件名称"] = info["案由"].split("/")[-1].strip() if "/" in info["案由"] else info["案由"]

    return info

def generate_synthesis(info, src_path):
    """Generate synthesis markdown content"""
    # 提取案由关键词
    tags = ["民事", "公报案例", "最高人民法院"]
    if info["案由"]:
        tag_parts = info["案由"].split("/")
        for part in tag_parts:
            part = part.strip()
            if part and len(part) > 1:
                tags.append(part)

    case_name = info["案件名称"] or f"公报案例 {info['案号']}"

    content = f"""---
title: {case_name}
type: synthesis
created: {TODAY}
updated: {TODAY}
tags: {tags}
source: "{src_path}"
related: []
案例分级: ⭐⭐⭐⭐⭐
问题意识: {info['案由'] or '公报案例裁判要旨'}
---

## 案情

### 基本信息

| 字段 | 内容 |
|------|------|
| 案号 | {info['案号']} |
| 审理法院 | {info['审理法院']} |
| 裁判日期 | {info['裁判日期']} |
| 案由 | {info['案由']} |

### 当事人信息

{info['当事人'] or '（详见原文）'}

## 裁判要旨

{info['裁判理由'][:1500] if info['裁判理由'] else '（详见原文）'}

## 判决结果

{info['判决结果'] or '（详见原文）'}
"""
    return content

def process_file(src_path):
    """Process a single source file"""
    try:
        with open(src_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取案号
        fname = src_path.stem  # 不带 .md
        case_name = fname.replace("公报案例 ", "")
        target_name = f"GuideCase_{case_name}.md"
        target_path = TARGET_DIR / target_name

        # 跳过已存在的文件
        if target_path.exists():
            return "skip", target_name

        # 提取信息
        rel_path = str(src_path).replace(str(VAULT) + "/", "")
        info = extract_case_info(content, rel_path)

        # 生成内容
        synthesis = generate_synthesis(info, rel_path)

        # 写入文件
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(synthesis)

        return "ok", target_name
    except Exception as e:
        return "error", f"{src_path.name}: {str(e)[:50]}"

def main():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 开始处理公报案例...")

    # 统计
    stats = {"ok": 0, "skip": 0, "error": 0}
    errors = []

    # 获取所有源文件
    source_files = list(SOURCE_DIR.rglob("*.md"))
    total = len(source_files)
    print(f"总计 {total} 个源文件")

    for i, src_path in enumerate(sorted(source_files)):
        if (i + 1) % 50 == 0:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 已处理 {i+1}/{total}")

        status, detail = process_file(src_path)
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
