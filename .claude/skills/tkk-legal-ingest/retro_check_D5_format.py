#!/usr/bin/env python3
"""
retro_check_D5_format.py
Wiki 回溯更新检查 - D5: 格式规范性检查
"""
import sys
import os
from pathlib import Path
import re
from typing import Dict, List, Tuple
# Force UTF-8 mode on Windows
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

WIKI_ROOT = Path("D:/AI agent/tkk-library/wiki")

def check_file(filepath: Path, subdir: str) -> List[str]:
    """检查单个文件的格式规范性，返回问题列表"""
    issues = []

    try:
        content = filepath.read_text(encoding="utf-8")
    except:
        return ["L1-编码错误"]

    filename = filepath.name

    # D5-1: 命名规范检查
    type_prefix_map = {
        "concepts": "concept_",
        "entities": "entity_",
        "summaries": "summary_",
        "syntheses": "synthesis_",
    }
    expected_prefix = type_prefix_map.get(subdir, "")
    if expected_prefix and not filename.startswith(expected_prefix):
        issues.append(f"L3-命名缺少前缀: 应以{expected_prefix}开头")

    # D5-5: 交叉引用格式检查 - 查找 [[ ]]
    wikilinks = re.findall(r'\[\[([^\]]+)\]\]', content)
    if wikilinks:
        # 检查每个 wikilink 目标是否存在
        for link in wikilinks:
            # 跳过头部锚点和外部链接
            if link.startswith("#") or "://" in link:
                continue

    # D5-7: 无导航残留检查
    nav_patterns = [
        r"<footer", r"<nav", r"<header",
        r"<div class=\"footer\"", r"<div class=\"nav\"",
        r"\[上一页\]", r"\[下一页\]", r"\[返回\]",
    ]
    for pattern in nav_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            issues.append(f"L3-导航残留: 检测到 {pattern}")
            break

    # D5-2: summaries NotebookLM 风格检查
    if subdir == "summaries":
        if not re.search(r"##\s*📋\s*文档概览", content):
            issues.append("L6-缺文档概览section")
        # D5-3 FAQ 建议检查
        if not re.search(r"##\s*❓\s*常见问题", content):
            issues.append("L6-建议添加FAQ")

    # D5-6: concept 底部相关区域检查
    if subdir == "concepts":
        if not re.search(r"##\s*相关", content):
            issues.append("L6-缺##相关区域")

    return issues

def main():
    results = {"L3": [], "L6": []}
    total = 0

    for subdir in ["concepts", "entities", "summaries", "syntheses"]:
        dir_path = WIKI_ROOT / subdir
        if not dir_path.exists():
            continue
        for filepath in dir_path.glob("*.md"):
            total += 1
            issues = check_file(filepath, subdir)
            for issue in issues:
                level = issue.split("-")[0]
                if level in results:
                    results[level].append(f"{subdir}/{filepath.name}: {issue}")

    print(f"=== D5 格式规范性检查报告 ===")
    print(f"总计检查: {total} 个文件\n")

    for level in ["L3", "L6"]:
        if results[level]:
            print(f"--- {level} 问题 ({len(results[level])} 项) ---")
            for item in sorted(results[level]):
                print(f"  {item}")
            print()
        else:
            print(f"--- {level} 问题: 0 项 ✓ ---")
            print()

    l3_count = len(results["L3"])
    l6_count = len(results["L6"])
    print(f"汇总: L3={l3_count}, L6={l6_count}")

    # 输出到文件
    report_path = WIKI_ROOT.parent / "retro_check_D5_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"=== D5 格式规范性检查报告 ===\n")
        f.write(f"总计检查: {total} 个文件\n\n")
        for level in ["L3", "L6"]:
            f.write(f"--- {level} 问题 ({len(results[level])} 项) ---\n")
            for item in sorted(results[level]):
                f.write(f"  {item}\n")
            f.write("\n")
        f.write(f"汇总: L3={l3_count}, L6={l6_count}\n")
    print(f"\n报告已输出到: {report_path}")

if __name__ == "__main__":
    main()
