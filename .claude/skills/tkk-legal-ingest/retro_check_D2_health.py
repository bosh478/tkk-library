#!/usr/bin/env python3
"""
retro_check_D2_health.py
Wiki 回溯更新检查 - D2: 文件健康状态检查
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
SIZE_THRESHOLD_KB = 5
LINE_COUNT_THRESHOLD = 20
PLACEHOLDER_PATTERNS = [
    r"^#+\s*$",  # 空标题行
    r"^待补充",
    r"^TODO",
    r"^（待.*?）",
    r"^<.*?>$",  # HTML标签残留
    r"^\s*$",     # 空白行
]
PLACEHOLDER_RE = re.compile("|".join(PLACEHOLDER_PATTERNS), re.IGNORECASE)

def check_file(filepath: Path) -> List[str]:
    """检查单个文件，返回问题列表"""
    issues = []
    try:
        content = filepath.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            content = filepath.read_text(encoding="gbk")
            issues.append(f"L1-编码问题: 使用 GBK 编码读取")
        except:
            issues.append(f"L1-编码错误: 无法读取文件编码")
            return issues

    lines = content.split("\n")

    # D2-1: 文件截断检查
    size_kb = filepath.stat().st_size / 1024
    non_empty_lines = [l for l in lines if l.strip()]
    line_count = len(non_empty_lines)

    if size_kb < SIZE_THRESHOLD_KB and line_count < LINE_COUNT_THRESHOLD:
        issues.append(f"L1-可疑截断: {size_kb:.1f}KB, {line_count}行")

    # D2-2: 内容空洞检查 - 检查正文前100字符
    body_match = re.match(r'^---\n.*?\n---\n', content, re.DOTALL)
    body_start = body_match.end() if body_match else 0
    body_preview = content[body_start:body_start+200].strip()

    # 提取前100实际字符（跳过空行）
    preview_lines = []
    for line in body_preview.split("\n"):
        if line.strip():
            preview_lines.append(line.strip())
        if len("\n".join(preview_lines)) >= 100:
            break
    preview_text = "".join(preview_lines)[:100]

    if not preview_text:
        issues.append("L1-内容空洞: 正文前100字符为空")
    elif PLACEHOLDER_RE.match(preview_text):
        issues.append(f"L1-内容空洞: 前100字符为占位符 '{preview_text[:20]}'")

    # D2-4: 编码问题检测（Unicode转义失败特征）
    if "\\u" in content or "\\x" in content:
        issues.append("L1-编码问题: 检测到未转义的Unicode转义序列")

    return issues

def main():
    results = {"L1": [], "L4": []}
    total = 0
    size_stats = {"concepts": [], "entities": [], "summaries": [], "syntheses": []}

    for subdir in ["concepts", "entities", "summaries", "syntheses"]:
        dir_path = WIKI_ROOT / subdir
        if not dir_path.exists():
            continue
        for filepath in dir_path.glob("*.md"):
            total += 1
            size_kb = filepath.stat().st_size / 1024
            size_stats[subdir].append(size_kb)

            issues = check_file(filepath)
            for issue in issues:
                level = issue.split("-")[0]
                if level in results:
                    results[level].append(f"{subdir}/{filepath.name}: {issue}")

    print(f"=== D2 文件健康状态检查报告 ===")
    print(f"总计检查: {total} 个文件\n")

    # 打印各目录 size 分布
    for subdir, sizes in size_stats.items():
        if sizes:
            sizes_sorted = sorted(sizes)
            p25 = sizes_sorted[int(len(sizes)*0.25)]
            p50 = sizes_sorted[int(len(sizes)*0.50)]
            p75 = sizes_sorted[int(len(sizes)*0.75)]
            print(f"--- {subdir} 文件大小分布 ---")
            print(f"  数量: {len(sizes)}, P25={p25:.1f}KB, P50={p50:.1f}KB, P75={p75:.1f}KB")
            print()

    for level in ["L1", "L4"]:
        if results[level]:
            print(f"--- {level} 问题 ({len(results[level])} 项) ---")
            for item in sorted(results[level]):
                print(f"  {item}")
            print()
        else:
            print(f"--- {level} 问题: 0 项 ✓ ---")
            print()

    l1_count = len(results["L1"])
    l4_count = len(results["L4"])
    print(f"汇总: L1={l1_count}, L4={l4_count}")

    # 输出到文件
    report_path = WIKI_ROOT.parent / "retro_check_D2_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"=== D2 文件健康状态检查报告 ===\n")
        f.write(f"总计检查: {total} 个文件\n\n")
        for subdir, sizes in size_stats.items():
            if sizes:
                sizes_sorted = sorted(sizes)
                p25 = sizes_sorted[int(len(sizes)*0.25)]
                p50 = sizes_sorted[int(len(sizes)*0.50)]
                p75 = sizes_sorted[int(len(sizes)*0.75)]
                f.write(f"--- {subdir} 文件大小分布 ---\n")
                f.write(f"  数量: {len(sizes)}, P25={p25:.1f}KB, P50={p50:.1f}KB, P75={p75:.1f}KB\n\n")
        for level in ["L1", "L4"]:
            f.write(f"--- {level} 问题 ({len(results[level])} 项) ---\n")
            for item in sorted(results[level]):
                f.write(f"  {item}\n")
            f.write("\n")
        f.write(f"汇总: L1={l1_count}, L4={l4_count}\n")
    print(f"\n报告已输出到: {report_path}")

if __name__ == "__main__":
    main()
