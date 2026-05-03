#!/usr/bin/env python3
"""
retro_check_D6_index.py
Wiki 回溯更新检查 - D6: 索引完整性检查
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

def parse_frontmatter(content: str) -> Tuple[Dict, str]:
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return {}, content
    try:
        fields = yaml.safe_load(match.group(1)) or {}
        body = content[match.end():]
        return fields, body
    except:
        return {}, content

def build_link_target_set() -> Set[str]:
    """构建所有 wiki 页面的链接目标集合"""
    targets = set()
    for subdir in ["concepts", "entities", "summaries", "syntheses"]:
        dir_path = WIKI_ROOT / subdir
        if not dir_path.exists():
            continue
        for filepath in dir_path.glob("*.md"):
            # 提取标题作为链接目标
            try:
                content = filepath.read_text(encoding="utf-8")
            except:
                continue
            fields, _ = parse_frontmatter(content)
            title = fields.get("title", "")
            if title:
                targets.add(title)
    return targets

def check_index_consistency() -> Dict[str, any]:
    """检查 index.md 统计与实际文件数的一致性"""
    issues = []

    # 读取 index.md
    index_path = WIKI_ROOT / "index.md"
    if not index_path.exists():
        return [{"L3-index.md不存在"}]

    try:
        content = index_path.read_text(encoding="utf-8")
    except:
        return [{"L3-index.md读取失败"}]

    # 统计实际文件数
    actual_counts = {}
    for subdir in ["concepts", "entities", "summaries", "syntheses"]:
        dir_path = WIKI_ROOT / subdir
        if dir_path.exists():
            actual_counts[subdir] = len(list(dir_path.glob("*.md")))
        else:
            actual_counts[subdir] = 0

    # 尝试从 index.md 提取统计数字
    # 查找 "Summaries（来源摘要） | 543" 这样的行
    summary_match = re.search(r"Summaries（来源摘要）\s*\|\s*(\d+)", content)
    if summary_match:
        reported = int(summary_match.group(1))
        actual = actual_counts.get("summaries", 0)
        if reported != actual:
            issues.append(f"L3-index统计不一致: summaries reported={reported}, actual={actual}")

    return issues

def main():
    results = {"L3": [], "L5": [], "L6": []}
    total = 0

    # 构建链接目标集合
    targets = build_link_target_set()

    # 检查各目录文件
    for subdir in ["concepts", "entities", "summaries", "syntheses"]:
        dir_path = WIKI_ROOT / subdir
        if not dir_path.exists():
            continue
        for filepath in dir_path.glob("*.md"):
            total += 1
            try:
                content = filepath.read_text(encoding="utf-8")
            except:
                results["L5"].append(f"{subdir}/{filepath.name}: L1-编码错误")
                continue

            # D6-2: 断链检测
            wikilinks = re.findall(r'\[\[([^\]]+)\]\]', content)
            for link in wikilinks:
                # 跳过头部锚点和外部链接
                if link.startswith("#") or "://" in link or link.startswith("http"):
                    continue
                # 检查链接目标是否存在
                if link not in targets and not any(link in t for t in targets):
                    results["L5"].append(f"{subdir}/{filepath.name}: L5-断链 [[{link}]]")

            # D6-3: concept 相关字段检查
            if subdir == "concepts":
                fields, _ = parse_frontmatter(content)
                if not fields.get("related"):
                    results["L6"].append(f"{subdir}/{filepath.name}: L6-缺related字段")

    print(f"=== D6 索引完整性检查报告 ===")
    print(f"总计检查: {total} 个文件\n")

    # index 一致性检查
    index_issues = check_index_consistency()
    for issue in index_issues:
        results["L3"].append(f"index.md: {issue}")

    for level in ["L3", "L5", "L6"]:
        if results[level]:
            print(f"--- {level} 问题 ({len(results[level])} 项) ---")
            for item in sorted(results[level])[:50]:  # 限制输出
                print(f"  {item}")
            if len(results[level]) > 50:
                print(f"  ... 还有 {len(results[level])-50} 项")
            print()
        else:
            print(f"--- {level} 问题: 0 项 ✓ ---")
            print()

    l3_count = len(results["L3"])
    l5_count = len(results["L5"])
    l6_count = len(results["L6"])
    print(f"汇总: L3={l3_count}, L5={l5_count}, L6={l6_count}")

    # 输出到文件
    report_path = WIKI_ROOT.parent / "retro_check_D6_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"=== D6 索引完整性检查报告 ===\n")
        f.write(f"总计检查: {total} 个文件\n\n")
        for level in ["L3", "L5", "L6"]:
            f.write(f"--- {level} 问题 ({len(results[level])} 项) ---\n")
            for item in sorted(results[level]):
                f.write(f"  {item}\n")
            f.write("\n")
        f.write(f"汇总: L3={l3_count}, L5={l5_count}, L6={l6_count}\n")
    print(f"\n报告已输出到: {report_path}")

if __name__ == "__main__":
    main()
