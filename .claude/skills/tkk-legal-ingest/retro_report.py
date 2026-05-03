#!/usr/bin/env python3
"""
retro_report.py
Wiki 回溯更新检查 - 汇总报告生成
"""
import sys
import os
from pathlib import Path
from typing import Dict, List
# Force UTF-8 mode on Windows
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

WIKI_ROOT = Path("D:/AI agent/tkk-library/wiki")
REPORT_DIR = Path("D:/AI agent/tkk-library")
SKILL_DIR = Path("D:/AI agent/tkk-library/.claude/skills/tkk-legal-ingest")

def parse_report(filepath: Path) -> Dict[str, any]:
    """解析单个报告文件"""
    if not filepath.exists():
        return {"total": 0, "levels": {}}

    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")

    result = {"total": 0, "levels": {}}
    for line in lines:
        if "总计检查:" in line:
            try:
                result["total"] = int(line.split("总计检查:")[1].strip())
            except:
                pass
        if "汇总:" in line:
            parts = line.split("汇总:")[1].strip().split(",")
            for part in parts:
                if "=" in part:
                    level = part.split("=")[0].strip()
                    count = int(part.split("=")[1].strip())
                    result["levels"][level] = count
    return result

def main():
    print("=" * 60)
    print("Wiki 回溯更新检查 - 汇总报告")
    print("=" * 60)
    print()

    reports = {
        "D1_frontmatter": REPORT_DIR / "retro_check_D1_report.txt",
        "D2_health": REPORT_DIR / "retro_check_D2_report.txt",
        "D3_category": REPORT_DIR / "retro_check_D3_report.txt",
        "D5_format": REPORT_DIR / "retro_check_D5_report.txt",
        "D6_index": REPORT_DIR / "retro_check_D6_report.txt",
    }

    all_results = {}
    total_files = 0

    for name, path in reports.items():
        result = parse_report(path)
        all_results[name] = result
        total_files = max(total_files, result.get("total", 0))

    # 汇总
    print(f"检查文件总数: {total_files}")
    print()

    total_issues = {}
    for name, result in all_results.items():
        print(f"--- {name} ---")
        for level, count in result.get("levels", {}).items():
            print(f"  {level}: {count}")
            total_issues[level] = total_issues.get(level, 0) + count
        print()

    print("=" * 60)
    print("问题汇总 (按优先级)")
    print("=" * 60)
    for level in ["L1", "L2", "L3", "L4", "L5", "L6"]:
        if level in total_issues:
            print(f"  {level}: {total_issues[level]}")

    print()
    print("优先级处理顺序: L1 → L2 → L3 → L4 → L5 → L6")

    # 生成完整报告
    report_path = WIKI_ROOT.parent / "retro_check汇总报告.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("Wiki 回溯更新检查 - 汇总报告\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"检查文件总数: {total_files}\n\n")

        for name, result in all_results.items():
            f.write(f"--- {name} ---\n")
            for level, count in result.get("levels", {}).items():
                f.write(f"  {level}: {count}\n")
            f.write("\n")

        f.write("=" * 60 + "\n")
        f.write("问题汇总 (按优先级)\n")
        f.write("=" * 60 + "\n")
        for level in ["L1", "L2", "L3", "L4", "L5", "L6"]:
            if level in total_issues:
                f.write(f"  {level}: {total_issues[level]}\n")
        f.write("\n")
        f.write("优先级处理顺序: L1 → L2 → L3 → L4 → L5 → L6\n")

    print(f"\n汇总报告已输出到: {report_path}")

if __name__ == "__main__":
    main()
