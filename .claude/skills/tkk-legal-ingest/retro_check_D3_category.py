#!/usr/bin/env python3
"""
retro_check_D3_category.py
Wiki 回溯更新检查 - D3: 分类正确性检查
"""
import sys
import os
from pathlib import Path
import re
import yaml
from typing import Dict, List, Tuple, Set
# Force UTF-8 mode on Windows
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

WIKI_ROOT = Path("D:/AI agent/tkk-library/wiki")
SOURCES_ROOT = Path("D:/AI agent/tkk-library/sources")

# 各类源文件对应的正确目录
SOURCE_TYPE_MAP = {
    "理解与适用": ("concepts", "concept"),
    "司法解释全书": ("concepts", "concept"),
    "司法解释原文": ("entities", "entity"),
    "律师业务指引": ("summaries", "summary"),
    "审判指导案例": ("syntheses", "synthesis"),
    "刑事审判参考": ("syntheses", "synthesis"),
    "刑法释义": ("concepts", "concept"),
    "书籍资料": ("concepts", "concept"),
}

# summaries 允许的 category 值
CATEGORY_VALUES = [
    "诉讼与仲裁", "公司商事与合规", "劳动与社会保障", "医药健康",
    "国际贸易", "婚姻家庭与继承", "建筑工程与房地产", "政府与公共法律服务",
    "生态环境与能源", "知识产权", "金融与财税", "刑事参考"
]

def detect_source_type(filepath: Path) -> str:
    """根据文件名/路径推测源文件类型"""
    path_str = str(filepath).replace("\\", "/").lower()
    name = filepath.stem.lower()

    if "理解与适用" in path_str or "理解与适用" in name:
        return "理解与适用"
    if "司法解释全书" in path_str or "司法解释全书" in name:
        return "司法解释全书"
    if re.search(r"司解释|法释\[?\d{4}\]?\d+号", name):
        return "司法解释原文"
    if "律师办理" in name and ("指引" in name or "操作指引" in name):
        return "律师业务指引"
    if "指导性案例" in name or "指导案例" in name or "检例" in name:
        return "审判指导案例"
    if "刑事审判参考" in path_str:
        return "刑事审判参考"
    if "刑法释义" in path_str or "刑法释义" in name:
        return "刑法释义"

    return "unknown"

def check_file(filepath: Path, subdir: str) -> List[str]:
    """检查单个文件的分类正确性，返回问题列表"""
    issues = []

    try:
        content = filepath.read_text(encoding="utf-8")
    except:
        return ["L1-编码错误"]

    fields, _ = parse_frontmatter(content)
    file_type = fields.get("type", "")

    # 检查 summaries 是否有 category
    if subdir == "summaries":
        cat = fields.get("category")
        if not cat:
            issues.append("L1-summary无category")
        elif cat not in CATEGORY_VALUES:
            issues.append(f"L3-category值无效: {cat}")

    # 检查 type 与目录一致性
    expected_type_map = {
        "concepts": "concept",
        "entities": "entity",
        "summaries": "summary",
        "syntheses": "synthesis",
    }
    expected_type = expected_type_map.get(subdir, "")
    if expected_type and file_type != expected_type:
        issues.append(f"L3-目录type不一致: 文件type={file_type}, 目录应为{subdir}")

    return issues

def parse_frontmatter(content: str) -> Tuple[Dict, str]:
    """解析 frontmatter，处理双 frontmatter 的情况（返回最后一个）"""
    matches = list(re.finditer(r'^---\n(.*?)\n---\n', content, re.DOTALL))
    if not matches:
        return {}, content
    # 使用最后一个 frontmatter（实际内容）
    last = matches[-1]
    try:
        fields = yaml.safe_load(last.group(1)) or {}
        body = content[last.end():]
        return fields, body
    except:
        return {}, content

def main():
    results = {"L1": [], "L2": [], "L3": []}
    total = 0
    type_counts = {"concepts": 0, "entities": 0, "summaries": 0, "syntheses": 0}

    for subdir in ["concepts", "entities", "summaries", "syntheses"]:
        dir_path = WIKI_ROOT / subdir
        if not dir_path.exists():
            continue
        for filepath in dir_path.glob("*.md"):
            total += 1
            type_counts[subdir] += 1
            issues = check_file(filepath, subdir)
            for issue in issues:
                level = issue.split("-")[0]
                if level in results:
                    results[level].append(f"{subdir}/{filepath.name}: {issue}")

    print(f"=== D3 分类正确性检查报告 ===")
    print(f"总计检查: {total} 个文件\n")

    # 文件数量统计
    print("--- 各目录文件数量 ---")
    for subdir, count in type_counts.items():
        print(f"  {subdir}: {count}")
    print()

    for level in ["L1", "L2", "L3"]:
        if results[level]:
            print(f"--- {level} 问题 ({len(results[level])} 项) ---")
            for item in sorted(results[level]):
                print(f"  {item}")
            print()
        else:
            print(f"--- {level} 问题: 0 项 ✓ ---")
            print()

    l1_count = len(results["L1"])
    l2_count = len(results["L2"])
    l3_count = len(results["L3"])
    print(f"汇总: L1={l1_count}, L2={l2_count}, L3={l3_count}")

    # 输出到文件
    report_path = WIKI_ROOT.parent / "retro_check_D3_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"=== D3 分类正确性检查报告 ===\n")
        f.write(f"总计检查: {total} 个文件\n\n")
        f.write("--- 各目录文件数量 ---\n")
        for subdir, count in type_counts.items():
            f.write(f"  {subdir}: {count}\n")
        f.write("\n")
        for level in ["L1", "L2", "L3"]:
            f.write(f"--- {level} 问题 ({len(results[level])} 项) ---\n")
            for item in sorted(results[level]):
                f.write(f"  {item}\n")
            f.write("\n")
        f.write(f"汇总: L1={l1_count}, L2={l2_count}, L3={l3_count}\n")
    print(f"\n报告已输出到: {report_path}")

if __name__ == "__main__":
    main()
