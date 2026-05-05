#!/usr/bin/env python3
"""
knowledge_stats.py
知识摄入量统计脚本 - 支撑长期复利分析

功能：
1. 每日知识摄入量统计（按类型分布）
2. 每周知识摄入量统计
3. 每月知识摄入量统计
4. 长期复利分析数据输出

用法:
    python knowledge_stats.py daily      # 今日统计
    python knowledge_stats.py weekly     # 本周统计
    python knowledge_stats.py monthly    # 本月统计
    python knowledge_stats.py all        # 完整统计
    python knowledge_stats.py export     # 导出CSV
    python knowledge_stats.py report     # 生成复利分析报告
"""

import os
import sys
import re
import csv
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Tuple

WIKI_ROOT = Path("D:/AI agent/tkk-library/wiki")
LOG_FILE = Path("D:/AI agent/tkk-library/log.md")


def parse_log_dates() -> Dict[str, List[str]]:
    """解析 log.md 中的日期记录"""
    if not LOG_FILE.exists():
        return {}

    content = LOG_FILE.read_text(encoding="utf-8")
    lines = content.split("\n")

    date_records = defaultdict(list)
    current_date = None

    for line in lines:
        date_match = re.match(r'^## \[(\d{4}-\d{2}-\d{2})\].*', line)
        if date_match:
            current_date = date_match.group(1)
        elif current_date and ("ingest" in line.lower() or "创建" in line or "更新" in line):
            date_records[current_date].append(line.strip())

    return date_records


def count_wiki_files(subdir: str) -> int:
    """统计 wiki 子目录文件数"""
    path = WIKI_ROOT / subdir
    if not path.exists():
        return 0
    return len(list(path.glob("*.md")))


def parse_frontmatter_fields(filepath: Path) -> Dict:
    """从文件解析 frontmatter 关键字段"""
    result = {
        "type": "unknown",
        "quality_grade": None,
        "hierarchy_level": None,
        "tags": []
    }
    try:
        content = filepath.read_text(encoding="utf-8")
        match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if match:
            import yaml
            try:
                fields = yaml.safe_load(match.group(1)) or {}
                result["type"] = fields.get("type", "unknown")
                result["quality_grade"] = fields.get("qualityGrade")
                result["hierarchy_level"] = fields.get("hierarchyLevel")
                result["tags"] = fields.get("tags", [])
            except:
                pass
    except:
        pass
    return result


def get_daily_stats(target_date: str) -> Dict:
    """获取指定日期的统计"""
    date_records = parse_log_dates()
    files_processed = date_records.get(target_date, [])

    stats = {
        "date": target_date,
        "log_entries": len(files_processed),
        "concepts": count_wiki_files("concepts"),
        "entities": count_wiki_files("entities"),
        "summaries": count_wiki_files("summaries"),
        "syntheses": count_wiki_files("syntheses"),
        "total": count_wiki_files("concepts") + count_wiki_files("entities") +
                 count_wiki_files("summaries") + count_wiki_files("syntheses"),
        "quality_grade_dist": {"A": 0, "B": 0, "C": 0, "D": 0},
        "hierarchy_dist": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0},
        "log_details": files_processed
    }

    # 统计质量分级和层级分布
    for subdir in ["summaries", "entities"]:
        subdir_path = WIKI_ROOT / subdir
        if subdir_path.exists():
            for filepath in subdir_path.glob("*.md"):
                fields = parse_frontmatter_fields(filepath)

                if fields["quality_grade"] in ["A", "B", "C", "D"]:
                    stats["quality_grade_dist"][fields["quality_grade"]] += 1

                if fields["hierarchy_level"]:
                    try:
                        level = int(fields["hierarchy_level"])
                        if level in stats["hierarchy_dist"]:
                            stats["hierarchy_dist"][level] += 1
                    except:
                        pass

    return stats


def get_weekly_stats(end_date: str) -> Dict:
    """获取本周统计（最近7天）"""
    end = datetime.strptime(end_date, "%Y-%m-%d")
    start = end - timedelta(days=6)

    daily_stats = []
    current = start
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        daily_stats.append(get_daily_stats(date_str))
        current += timedelta(days=1)

    # 汇总
    total_log_entries = sum(s["log_entries"] for s in daily_stats)

    return {
        "start_date": start.strftime("%Y-%m-%d"),
        "end_date": end_date,
        "days": 7,
        "total_log_entries": total_log_entries,
        "concepts": daily_stats[-1]["concepts"],
        "entities": daily_stats[-1]["entities"],
        "summaries": daily_stats[-1]["summaries"],
        "syntheses": daily_stats[-1]["syntheses"],
        "total": daily_stats[-1]["total"],
        "quality_grade_dist": daily_stats[-1]["quality_grade_dist"],
        "hierarchy_dist": daily_stats[-1]["hierarchy_dist"],
        "daily_breakdown": daily_stats
    }


def get_monthly_stats(end_date: str) -> Dict:
    """获取本月统计"""
    end = datetime.strptime(end_date, "%Y-%m-%d")
    start = end.replace(day=1)

    daily_stats = []
    current = start
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        daily_stats.append(get_daily_stats(date_str))
        current += timedelta(days=1)

    total_log_entries = sum(s["log_entries"] for s in daily_stats)

    # 汇总质量分级
    total_quality = {"A": 0, "B": 0, "C": 0, "D": 0}
    total_hierarchy = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    for s in daily_stats:
        for g in ["A", "B", "C", "D"]:
            total_quality[g] += s["quality_grade_dist"][g]
        for l in range(1, 7):
            total_hierarchy[l] += s["hierarchy_dist"][l]

    return {
        "start_date": start.strftime("%Y-%m-%d"),
        "end_date": end_date,
        "days": len(daily_stats),
        "total_log_entries": total_log_entries,
        "concepts": daily_stats[-1]["concepts"],
        "entities": daily_stats[-1]["entities"],
        "summaries": daily_stats[-1]["summaries"],
        "syntheses": daily_stats[-1]["syntheses"],
        "total": daily_stats[-1]["total"],
        "quality_grade_dist": total_quality,
        "hierarchy_dist": total_hierarchy,
        "daily_breakdown": daily_stats
    }


def print_stats(stats: Dict, title: str = ""):
    """打印统计信息"""
    if title:
        print(f"\n{'='*50}")
        print(title)
        print(f"{'='*50}")
    elif "start_date" in stats:
        print(f"\n{'='*50}")
        print(f"统计周期: {stats['start_date']} ~ {stats['end_date']} ({stats['days']}天)")
        print(f"{'='*50}")
    else:
        print(f"\n{'='*50}")
        print(f"统计日期: {stats['date']}")
        print(f"{'='*50}")

    print(f"活动记录数: {stats.get('total_log_entries', stats.get('log_entries', 0))}")
    print(f"知识节点统计:")
    print(f"  - concepts:  {stats['concepts']}")
    print(f"  - entities:  {stats['entities']}")
    print(f"  - summaries: {stats['summaries']}")
    print(f"  - syntheses: {stats['syntheses']}")
    print(f"  - 总计:      {stats['total']}")

    if "quality_grade_dist" in stats:
        print(f"\n质量分级分布:")
        total_graded = sum(stats["quality_grade_dist"].values())
        for grade in ["A", "B", "C", "D"]:
            count = stats["quality_grade_dist"][grade]
            pct = count / total_graded * 100 if total_graded > 0 else 0
            print(f"  - Grade {grade}: {count} ({pct:.1f}%)")

    if "hierarchy_dist" in stats:
        total_hier = sum(stats["hierarchy_dist"].values())
        if total_hier > 0:
            print(f"\n法律效力层级分布:")
            level_names = {
                1: "宪法",
                2: "法律",
                3: "行政法规",
                4: "地方性法规",
                5: "部门规章",
                6: "行政程序规范"
            }
            for level in range(1, 7):
                count = stats["hierarchy_dist"][level]
                pct = count / total_hier * 100 if total_hier > 0 else 0
                name = level_names.get(level, f"层级{level}")
                print(f"  - {name}({level}): {count} ({pct:.1f}%)")

    if "daily_breakdown" in stats:
        print(f"\n每日详情:")
        for day in stats["daily_breakdown"]:
            print(f"  {day['date']}: {day['log_entries']} 条活动, {day['total']} 个节点")


def export_csv(stats: Dict, filename: str = "knowledge_stats.csv"):
    """导出统计为 CSV"""
    output_path = WIKI_ROOT.parent / filename

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["日期", "活动数", "concepts", "entities", "summaries", "syntheses", "总计"])

        if "daily_breakdown" in stats:
            for day in stats["daily_breakdown"]:
                writer.writerow([
                    day["date"],
                    day["log_entries"],
                    day["concepts"],
                    day["entities"],
                    day["summaries"],
                    day["syntheses"],
                    day["total"]
                ])
        else:
            writer.writerow([
                stats["date"],
                stats["log_entries"],
                stats["concepts"],
                stats["entities"],
                stats["summaries"],
                stats["syntheses"],
                stats["total"]
            ])

    print(f"\nCSV 已导出到: {output_path}")


def generate_report(stats: Dict, period: str = "daily"):
    """生成复利分析报告"""
    report_path = WIKI_ROOT.parent / f"knowledge_compound_report_{period}.md"

    period_names = {
        "daily": "日报",
        "weekly": "周报",
        "monthly": "月报"
    }

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# 知识复利分析报告\n\n")
        f.write(f"> 报告周期: {stats.get('start_date', stats.get('date'))}\n\n")

        f.write("## 知识节点统计\n\n")
        f.write("### 当前总量\n\n")
        f.write("| 类型 | 数量 | 占比 |\n")
        f.write("|------|------|------|\n")

        total = stats["total"]
        for node_type in ["concepts", "entities", "summaries", "syntheses"]:
            count = stats.get(node_type, 0)
            pct = count / total * 100 if total > 0 else 0
            f.write(f"| {node_type} | {count} | {pct:.1f}% |\n")

        f.write(f"| **总计** | **{total}** | 100% |\n\n")

        if "quality_grade_dist" in stats:
            f.write("### 质量分级分布\n\n")
            total_graded = sum(stats["quality_grade_dist"].values())
            f.write("| 等级 | 数量 | 占比 |\n")
            f.write("|------|------|------|\n")
            for grade in ["A", "B", "C", "D"]:
                count = stats["quality_grade_dist"][grade]
                pct = count / total_graded * 100 if total_graded > 0 else 0
                f.write(f"| Grade {grade} | {count} | {pct:.1f}% |\n\n")

        if "hierarchy_dist" in stats:
            total_hier = sum(stats["hierarchy_dist"].values())
            if total_hier > 0:
                f.write("### 法律效力层级分布\n\n")
                f.write("| 层级 | 类型 | 数量 | 占比 |\n")
                f.write("|------|------|------|------|\n")
                level_names = {
                    1: "宪法", 2: "法律", 3: "行政法规",
                    4: "地方性法规", 5: "部门规章", 6: "行政程序规范"
                }
                for level in range(1, 7):
                    count = stats["hierarchy_dist"][level]
                    pct = count / total_hier * 100 if total_hier > 0 else 0
                    name = level_names.get(level, f"层级{level}")
                    f.write(f"| {level} | {name} | {count} | {pct:.1f}% |\n")
                f.write("\n")

        f.write("## 复利效应评估\n\n")
        log_entries = stats.get("total_log_entries", stats.get("log_entries", 0))
        f.write(f"- 本期活动记录数: {log_entries}\n")
        f.write(f"- 知识节点总数: {total}\n")

        if log_entries > 0:
            f.write(f"- 平均每日活动: {log_entries / stats.get('days', 1):.1f} 条\n")

        f.write("\n## 建议\n\n")
        f.write("1. 定期检查孤立页面，补充 related 字段\n")
        f.write("2. 关注 Grade C/D 页面是否可合并或提升\n")
        f.write("3. 检查同类资料是否产生新差异点\n")

    print(f"\n复利分析报告已生成: {report_path}")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "daily"
    today = datetime.now().strftime("%Y-%m-%d")

    if mode == "daily":
        stats = get_daily_stats(today)
        print_stats(stats)
    elif mode == "weekly":
        stats = get_weekly_stats(today)
        print_stats(stats, "本周统计")
    elif mode == "monthly":
        stats = get_monthly_stats(today)
        print_stats(stats, "本月统计")
    elif mode == "all":
        print("=== 今日统计 ===")
        print_stats(get_daily_stats(today))
        print("\n=== 本周统计 ===")
        print_stats(get_weekly_stats(today), "本周统计")
        print("\n=== 本月统计 ===")
        print_stats(get_monthly_stats(today), "本月统计")
    elif mode == "export":
        stats = get_monthly_stats(today)
        export_csv(stats)
    elif mode == "report":
        period = sys.argv[2] if len(sys.argv) > 2 else "monthly"
        if period == "weekly":
            stats = get_weekly_stats(today)
        elif period == "monthly":
            stats = get_monthly_stats(today)
        else:
            stats = get_daily_stats(today)
        generate_report(stats, period)
    else:
        print(f"未知模式: {mode}")
        print("用法: python knowledge_stats.py [daily|weekly|monthly|all|export|report]")


if __name__ == "__main__":
    main()
