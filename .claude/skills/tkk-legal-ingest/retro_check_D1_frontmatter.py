#!/usr/bin/env python3
"""
retro_check_D1_frontmatter.py
Wiki 回溯更新检查 - D1: frontmatter 完备性检查
"""
import sys
import os
from pathlib import Path
import re
import yaml
# Force UTF-8 mode on Windows
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

WIKI_ROOT = Path("D:/AI agent/tkk-library/wiki")
REQUIRED_FIELDS = ["title", "type", "created", "tags"]
OPTIONAL_FIELDS = ["updated", "source", "category"]
VALID_TYPES = ["concept", "entity", "synthesis", "summary"]
CATEGORY_REQUIRED_FOR = ["summary"]
CATEGORY_VALUES = [
    "诉讼与仲裁", "公司商事与合规", "劳动与社会保障", "医药健康",
    "国际贸易", "婚姻家庭与继承", "建筑工程与房地产", "政府与公共法律服务",
    "生态环境与能源", "知识产权", "金融与财税", "刑事参考"
]

def parse_frontmatter(content: str) -> Tuple[Dict, str]:
    """解析 frontmatter，返回 (fields_dict, body)"""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return {}, content
    try:
        fields = yaml.safe_load(match.group(1)) or {}
        body = content[match.end():]
        return fields, body
    except:
        return {}, content

def check_file(filepath: Path) -> List[str]:
    """检查单个文件，返回问题列表"""
    issues = []
    try:
        content = filepath.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            content = filepath.read_text(encoding="gbk")
        except:
            issues.append(f"L1-编码错误: 无法读取文件编码")
            return issues
        issues.append(f"L1-编码问题: 使用 GBK 编码读取")

    fields, body = parse_frontmatter(content)

    # D1-1: type 字段
    file_type = fields.get("type")
    if not file_type:
        issues.append("L1-type字段缺失")
    elif file_type not in VALID_TYPES:
        issues.append(f"L3-type字段值无效: {file_type}")

    # D1-2: created/updated
    if not fields.get("created"):
        issues.append("L1-created字段缺失")
    if not fields.get("updated"):
        issues.append("L3-updated字段缺失")

    # D1-3: category (仅 summary 类型需要)
    if file_type == "summary":
        cat = fields.get("category")
        if not cat:
            issues.append("L1-category字段缺失(summary类型必填)")
        elif cat not in CATEGORY_VALUES:
            issues.append(f"L3-category值不在允许列表: {cat}")

    # D1-4: tags
    if not fields.get("tags"):
        issues.append("L3-tags字段缺失")

    # D1-5: source
    if not fields.get("source") and file_type in ["summary", "concept"]:
        issues.append("L3-source字段缺失")

    # D1-6: title
    if not fields.get("title"):
        issues.append("L3-title字段缺失")

    return issues

def main():
    results = {"L1": [], "L3": []}
    total = 0

    for subdir in ["concepts", "entities", "summaries", "syntheses"]:
        dir_path = WIKI_ROOT / subdir
        if not dir_path.exists():
            continue
        for filepath in dir_path.glob("*.md"):
            total += 1
            issues = check_file(filepath)
            for issue in issues:
                level = issue.split("-")[0]
                if level in results:
                    results[level].append(f"{filepath.name}: {issue}")

    print(f"=== D1 frontmatter 检查报告 ===")
    print(f"总计检查: {total} 个文件\n")

    for level in ["L1", "L3"]:
        if results[level]:
            print(f"--- {level} 问题 ({len(results[level])} 项) ---")
            for item in sorted(results[level]):
                print(f"  {item}")
            print()
        else:
            print(f"--- {level} 问题: 0 项 ✓ ---")
            print()

    # 汇总
    l1_count = len(results["L1"])
    l3_count = len(results["L3"])
    print(f"汇总: L1={l1_count}, L3={l3_count}")

    # 输出到文件
    report_path = WIKI_ROOT.parent / "retro_check_D1_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"=== D1 frontmatter 检查报告 ===\n")
        f.write(f"总计检查: {total} 个文件\n\n")
        for level in ["L1", "L3"]:
            f.write(f"--- {level} 问题 ({len(results[level])} 项) ---\n")
            for item in sorted(results[level]):
                f.write(f"  {item}\n")
            f.write("\n")
        f.write(f"汇总: L1={l1_count}, L3={l3_count}\n")
    print(f"\n报告已输出到: {report_path}")

if __name__ == "__main__":
    main()
