#!/usr/bin/env python3
"""
quality_check.py
网络文章质量分级检查脚本

用法:
    python quality_check.py <file.md>
    python quality_check.py D:/AI\ agent/tkk-library/Clippings/*.md
    python quality_check.py wiki/summaries/

检查项:
    1. qualityGrade 字段存在且有效值（A/B/C/D）
    2. sourceCredibility 字段存在且有效值
    3. contentCompleteness 字段存在且有效值
    4. 来源可信度与质量等级一致性检查
    5. 网络文章必须有 url 字段（注明来源）

返回:
    PASS - 质量分级完整
    FAIL - 缺少必要字段
    WARN - 质量分级与来源不一致
"""

import os
import sys
import re
import glob
from pathlib import Path
from typing import List, Tuple, Dict

QUALITY_GRADES = ["A", "B", "C", "D"]
CREDIBILITY_LEVELS = ["official", "professional", "general", "unknown"]
COMPLETENESS_LEVELS = ["high", "medium", "low"]

# 权威来源映射（用于自动分级）
OFFICIAL_SOURCES = [
    "最高人民法院", "最高人民检察院", "全国人民代表大会", "全国人大常委会",
    "国务院", "司法部", "公安部", "法释", "法检联发", "法发", "法研"
]

PROFESSIONAL_SOURCES = [
    "省高级人民法院", "省人民检察院", "高级人民法院", "人民检察院",
    "各省级司法机关", "中国法学会", "中华全国律师协会", "律师协会",
    "国家法官学院", "国家检察官学院"
]

GENERAL_SOURCES = [
    "人民法院报", "检察日报", "法制日报", "正义网", "新浪司法",
    "腾讯司法", "凤凰网法律", "搜狐法律"
]


def extract_source_info(content: str) -> Dict[str, str]:
    """从正文中提取来源信息"""
    info = {
        "source_name": "",
        "credibility_level": "unknown",
        "has_url": False,
        "author": None
    }

    # 提取作者/发布机构
    author_patterns = [
        r'(?:作者|发布|发布机关|来源)[:：]\s*([^\n，。]+)',
        r'发布于[:：]\s*([^\n，。]+)',
    ]
    for pattern in author_patterns:
        author_match = re.search(pattern, content[:1000])
        if author_match:
            info["source_name"] = author_match.group(1).strip()
            break

    # 检测来源级别
    for src in OFFICIAL_SOURCES:
        if src in content[:2000]:
            info["credibility_level"] = "official"
            break

    if info["credibility_level"] == "unknown":
        for src in PROFESSIONAL_SOURCES:
            if src in content[:2000]:
                info["credibility_level"] = "professional"
                break

    if info["credibility_level"] == "unknown":
        for src in GENERAL_SOURCES:
            if src in content[:2000]:
                info["credibility_level"] = "general"
                break

    # 检测是否有 URL
    url_patterns = [
        r'https?://[^\s<>"{}|\\^`\[\]]+',
        r'url[:：]\s*(https?://[^\s]+)',
    ]
    for pattern in url_patterns:
        if re.search(pattern, content):
            info["has_url"] = True
            break

    return info


def check_quality_grading(filepath: str) -> Tuple[List[str], List[str]]:
    """检查网络文章质量分级"""
    passed = []
    issues = []
    warnings = []

    try:
        content = Path(filepath).read_text(encoding="utf-8")
    except Exception as e:
        return [], [f"[ERROR] 无法读取文件: {e}"]

    # 解析 frontmatter
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        issues.append("[FAIL] frontmatter: 缺少 YAML frontmatter")
        return passed, issues

    frontmatter = match.group(1)

    # 检查 type 是否为 summary（质量分级仅适用于 summary 类型）
    type_match = re.search(r'^type:\s*(.+)$', frontmatter, re.MULTILINE)
    if not type_match or 'summary' not in type_match.group(1):
        # 非 summary 类型，跳过质量分级检查
        return ["[SKIP] 非 summary 类型，跳过质量分级检查"], []

    # 检查 qualityGrade
    grade_match = re.search(r'qualityGrade:\s*([A-D])', frontmatter)
    if not grade_match:
        issues.append("[FAIL] qualityGrade: 缺少 qualityGrade 字段")
    else:
        grade = grade_match.group(1)
        if grade in QUALITY_GRADES:
            passed.append(f"[PASS] qualityGrade: {grade}")
        else:
            issues.append(f"[FAIL] qualityGrade: 无效值 {grade}")

    # 检查 sourceCredibility
    cred_match = re.search(r'sourceCredibility:\s*(\w+)', frontmatter)
    if not cred_match:
        issues.append("[FAIL] sourceCredibility: 缺少 sourceCredibility 字段")
    else:
        cred = cred_match.group(1)
        if cred in CREDIBILITY_LEVELS:
            passed.append(f"[PASS] sourceCredibility: {cred}")
        else:
            issues.append(f"[FAIL] sourceCredibility: 无效值 {cred}")

    # 检查 contentCompleteness
    comp_match = re.search(r'contentCompleteness:\s*(\w+)', frontmatter)
    if not comp_match:
        issues.append("[FAIL] contentCompleteness: 缺少 contentCompleteness 字段")
    else:
        comp = comp_match.group(1)
        if comp in COMPLETENESS_LEVELS:
            passed.append(f"[PASS] contentCompleteness: {comp}")
        else:
            issues.append(f"[FAIL] contentCompleteness: 无效值 {comp}")

    # 检查 url 字段（网络文章必须有来源URL）
    url_match = re.search(r'^url:\s*(.+)$', frontmatter, re.MULTILINE)
    if not url_match:
        issues.append("[FAIL] url: 网络文章必须注明来源 URL")
    else:
        passed.append(f"[PASS] url: {url_match.group(1).strip()[:50]}...")

    # 一致性检查：来源级别 vs 质量等级
    if grade_match and cred_match:
        grade = grade_match.group(1)
        cred = cred_match.group(1)

        # 从正文检测实际来源
        source_info = extract_source_info(content)

        # 如果 frontmatter 的 credibility 与正文检测不一致，发出警告
        if source_info["credibility_level"] != "unknown":
            if source_info["credibility_level"] != cred:
                warnings.append(
                    f"[WARN] 一致性: frontmatter={cred}, 正文检测={source_info['credibility_level']}"
                )

        # 官方来源应该是 A 或 B 级
        if cred == "official" and grade not in ["A", "B"]:
            warnings.append(f"[WARN] 一致性: {cred} 来源但质量等级为 {grade}，建议升到 A/B")

        # 专业来源应该是 B 或 C 级
        if cred == "professional" and grade not in ["B", "C"]:
            warnings.append(f"[WARN] 一致性: {cred} 来源但质量等级为 {grade}，建议调整为 B/C")

        # 一般来源应该是 C 或 D 级
        if cred == "general" and grade not in ["C", "D"]:
            warnings.append(f"[WARN] 一致性: {cred} 来源但质量等级为 {grade}，建议降级")

        # 无名来源应该是 D 级
        if cred == "unknown" and grade != "D":
            warnings.append(f"[WARN] 一致性: unknown 来源建议为 D 级")

    # 内容完整性检查
    if comp_match:
        comp = comp_match.group(1)
        content_length = len(content)

        if comp == "high" and content_length < 5000:
            warnings.append(f"[WARN] 完整性: contentCompleteness=high 但内容仅 {content_length} 字")

        if comp == "low" and content_length > 10000:
            warnings.append(f"[WARN] 完整性: contentCompleteness=low 但内容达 {content_length} 字")

    return passed, issues + warnings


def get_quality_stats(files: List[Path]) -> Dict:
    """统计质量分级分布"""
    stats = {
        "total": 0,
        "graded": {"A": 0, "B": 0, "C": 0, "D": 0},
        "ungraded": 0,
        "by_credibility": {"official": 0, "professional": 0, "general": 0, "unknown": 0}
    }

    for filepath in files:
        try:
            content = filepath.read_text(encoding="utf-8")
            match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
            if not match:
                continue

            frontmatter = match.group(1)
            type_match = re.search(r'^type:\s*(.+)$', frontmatter, re.MULTILINE)

            if not type_match or 'summary' not in type_match.group(1):
                continue

            stats["total"] += 1

            grade_match = re.search(r'qualityGrade:\s*([A-D])', frontmatter)
            cred_match = re.search(r'sourceCredibility:\s*(\w+)', frontmatter)

            if grade_match:
                stats["graded"][grade_match.group(1)] += 1
            else:
                stats["ungraded"] += 1

            if cred_match:
                stats["by_credibility"][cred_match.group(1)] += 1

        except Exception:
            continue

    return stats


def main():
    if len(sys.argv) < 2:
        print("用法: python quality_check.py <file.md> 或 <dir/*.md> 或 <dir/>")
        sys.exit(1)

    target = sys.argv[1]

    if '*' in target:
        files = glob.glob(target)
    elif os.path.isdir(target):
        files = glob.glob(os.path.join(target, '*.md'))
    else:
        files = [target]

    if not files:
        print(f"未找到文件: {target}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print("网络文章质量分级检查")
    print(f"{'='*60}\n")

    total = len(files)
    pass_count = 0
    fail_count = 0
    skip_count = 0

    all_results = []

    for filepath in sorted(files):
        basename = os.path.basename(filepath)
        passed, results = check_quality_grading(filepath)

        has_fail = any(r.startswith("[FAIL]") for r in results)
        has_warn = any(r.startswith("[WARN]") for r in results)
        is_skip = any(r.startswith("[SKIP]") for r in results)

        if is_skip:
            skip_count += 1
            status = "SKIP"
        elif has_fail:
            fail_count += 1
            status = "FAIL"
        else:
            pass_count += 1
            status = "PASS"

        all_results.append({
            "file": basename,
            "status": status,
            "passed": passed,
            "results": results
        })

        print(f"[{status}] {basename}")
        for p in passed:
            if not p.startswith("[SKIP]"):
                print(f"  {p}")
        for r in results:
            print(f"  {r}")
        print()

    # 质量分级分布统计
    print(f"{'='*60}")
    print("质量分级分布统计")
    print(f"{'='*60}")

    wiki_files = [Path(f) for f in files if 'wiki/summaries' in f]
    if wiki_files:
        stats = get_quality_stats(wiki_files)
        print(f"\n检查文件数: {stats['total']}")
        print(f"已分级: {sum(stats['graded'].values())}")
        print(f"未分级: {stats['ungraded']}")
        print(f"\n等级分布:")
        for grade in ["A", "B", "C", "D"]:
            count = stats["graded"][grade]
            pct = count / stats['total'] * 100 if stats['total'] > 0 else 0
            print(f"  Grade {grade}: {count} ({pct:.1f}%)")
        print(f"\n来源分布:")
        for cred in ["official", "professional", "general", "unknown"]:
            print(f"  {cred}: {stats['by_credibility'][cred]}")

    # 汇总
    print(f"\n{'='*60}")
    print("汇总")
    print(f"{'='*60}")
    print(f"总文件数: {total}")
    print(f"PASS: {pass_count}")
    print(f"FAIL: {fail_count}")
    print(f"SKIP: {skip_count}")

    if fail_count > 0:
        print(f"\n⚠️ 有 {fail_count} 个文件缺少必要的质量分级字段")
        print("请补充 qualityGrade、sourceCredibility、contentCompleteness 和 url 字段")

    sys.exit(1 if fail_count > 0 else 0)


if __name__ == "__main__":
    main()
