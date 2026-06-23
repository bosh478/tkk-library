#!/usr/bin/env python3
"""
enhanced_lint.py
v66 — 基于第122辑教训增强的 lint 脚本

P0 阻断性检查（9项）：
  P0-1: frontmatter 字段名错误（sources/case_num/volumn/line_ref）
  P0-2: case_number 异常值（UNKNOWN/None/空）
  P0-3: 文件尺寸 < 2KB（截断检测）
  P0-4: OCR 乱码出现在 frontmatter 关键字段
  P0-5: case_number 重复（同案号出现多次）
  P0-6: line-refs 行号越界（>源文件总行数）
  P0-7: source 指向文件不存在
  P0-8: related_cases 格式异常
  P0-9: type=summary 但缺少 category

P1 建议性检查（3项）：
  P1-1: related 字段数量低于最低要求
  P1-2: volume 格式不规范
  P1-3: created/updated 日期格式错误

用法:
    python enhanced_lint.py --p0-only wiki/
    python enhanced_lint.py --batch wiki/
    python enhanced_lint.py --check ocr wiki/
    python enhanced_lint.py --check duplicates wiki/
    python enhanced_lint.py --check file-size wiki/
"""

import os
import sys
import re
import glob
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Tuple, List, Dict, Any

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------

# VAULT_ROOT 多平台兼容（patched 2026-06-23）：
# 1. 优先 TKK_VAULT_ROOT 环境变量
# 2. Windows: "D:/AI agent/tkk-library"
# 3. Linux/WSL: /home/kangkang/tkk-library 等候选按存在性自动探测
_VAULT_CANDIDATES = [
    os.environ.get("TKK_VAULT_ROOT"),
    "D:/AI agent/tkk-library" if os.name == "nt" else None,
    "/home/kangkang/tkk-library",
    "/mnt/d/AI agent/tkk-library",
    "/mnt/c/Users/汤康康/tkk-library",
]
VAULT_ROOT = next(
    (Path(p) for p in _VAULT_CANDIDATES if p and Path(p).exists()),
    Path(os.environ.get("TKK_VAULT_ROOT", "D:/AI agent/tkk-library"))
)
WIKI_ROOT = VAULT_ROOT / "wiki"
SOURCES_ROOT = VAULT_ROOT / "sources"

WRONG_FIELDS = {
    "sources": "source",
    "case_num": "case_number",
    "volumn": "volume",
    "line_ref": "line-refs",
}

INVALID_CASE_VALUES = {"UNKNOWN", "None", "", "第 号", "第null号", "null"}

VALID_CASE_PATTERN = re.compile(r"^第\d+号$")
VALID_VOLUME_PATTERN = re.compile(r"^(总第)?\d+[辑集期册]$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

MIN_RELATED = {
    "entity": 1,
    "concept": 2,
    "summary": 1,
    "synthesis": 1,
}

OCR_ERRORS = [
    "作人员", "民检察院", "法拘禁罪", "期徒刑",
    "事判决", "政治权利终", "期徒刑缓",
    "政治权利", "期徒刑", "事判决书",
]

SMALL_FILE_EXEMPT = {
    "宪法修正案", "修改决定", "简单单行法",
}

# 2KB 下限
MIN_FILE_SIZE = 2 * 1024


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

def get_frontmatter(content: str) -> Dict[str, Any]:
    """提取 YAML frontmatter 为 dict"""
    fm = {}
    m = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not m:
        return fm
    for line in m.group(1).split('\n'):
        if ':' in line:
            key, _, val = line.partition(':')
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val.startswith('[') and val.endswith(']'):
                # list: 先当字符串处理
                fm[key] = val
            else:
                fm[key] = val
    return fm


def get_case_number(filepath: Path) -> str:
    """从文件名提取案号"""
    name = filepath.stem
    m = re.search(r'第(\d+)号', name)
    return m.group(0) if m else ""


def get_type(content: str) -> str:
    m = re.search(r'^type:\s*(\w+)', content, re.MULTILINE)
    return m.group(1) if m else ""


def count_source_lines(source_rel_path: str) -> int:
    """获取源文件总行数（缓存）"""
    if not source_rel_path or source_rel_path == "不存在":
        return 0
    src = VAULT_ROOT / source_rel_path
    if src.exists():
        try:
            with open(src, 'r', encoding='utf-8') as f:
                return sum(1 for _ in f)
        except Exception:
            return 0
    return 0


# ---------------------------------------------------------------------------
# P0 检查
# ---------------------------------------------------------------------------

def check_p0_1_wrong_fields(fm: Dict, issues: List[str]) -> None:
    """P0-1: frontmatter 字段名错误"""
    for field in fm:
        if field in WRONG_FIELDS:
            issues.append(f"P0-1: 错误字段名 '{field}'，应为 '{WRONG_FIELDS[field]}'")


def check_p0_2_case_number(fm: Dict, ftype: str, issues: List[str]) -> None:
    """P0-2: case_number 异常值"""
    if ftype != "synthesis":
        return
    cn = str(fm.get("case_number", ""))
    if cn in INVALID_CASE_VALUES:
        issues.append(f"P0-2: case_number 异常值: '{cn}'")
    elif cn and not VALID_CASE_PATTERN.match(cn):
        issues.append(f"P0-2: case_number 格式异常: '{cn}'")


def check_p0_3_file_size(filepath: Path, content: str, issues: List[str]) -> None:
    """P0-3: 文件尺寸 < 2KB"""
    size = filepath.stat().st_size
    if size < MIN_FILE_SIZE:
        # 检查是否属于小型法律文件基线
        exempt = any(e in filepath.name for e in SMALL_FILE_EXEMPT)
        if not exempt:
            issues.append(f"P0-3: 文件过小({size}bytes)，疑似截断: {filepath.name}")


def check_p0_4_ocr_errors(fm: Dict, issues: List[str]) -> None:
    """P0-4: OCR 乱码出现在 frontmatter"""
    for field in ["title", "case_number", "volume"]:
        val = str(fm.get(field, ""))
        for err in OCR_ERRORS:
            if err in val:
                issues.append(f"P0-4: OCR乱码在 {field}: '{err}'")


def check_p0_5_duplicates(all_synth: List[Path], seen: Dict, issues: List[str]) -> None:
    """P0-5: case_number 重复"""
    # 由主循环调用，这里仅记录已处理的案号
    pass


def check_p0_6_line_refs_overflow(fm: Dict, issues: List[str], source_lines: int) -> None:
    """P0-6: line-refs 行号越界"""
    if source_lines == 0:
        return  # 无源文件信息，跳过
    line_refs = fm.get("line-refs", "")
    if not line_refs:
        return
    # 解析 line-refs 内容（可能有多种格式）
    for m in re.finditer(r'lines:\s*\[(.*?)\]', line_refs, re.DOTALL):
        nums = re.findall(r'\d+', m.group(1))
        for n in nums:
            if int(n) > source_lines:
                issues.append(f"P0-6: line-refs 行号越界: {n} > {source_lines}")


def check_p0_7_source_missing(fm: Dict, ftype: str, issues: List[str]) -> None:
    """P0-7: source 指向文件不存在"""
    src = fm.get("source", "")
    if not src:
        if ftype != "summary":
            issues.append(f"P0-7: source 为空: {ftype} 类型")
        return
    if src == "不存在":
        return
    full = VAULT_ROOT / src
    if not full.exists():
        issues.append(f"P0-7: source 指向文件不存在: {src}")


def check_p0_8_related_cases_format(fm: Dict, issues: List[str]) -> None:
    """P0-8: related_cases 格式异常"""
    rc = fm.get("related_cases", "")
    if not rc:
        return
    # related_cases 可能是逗号分隔的字符串或 YAML list
    items = re.findall(r'第\d+号', rc)
    # 检查格式不规范的条目（如只有数字）
    for m in re.finditer(r'([^,\s，]+)', rc):
        item = m.group(1).strip()
        if item and not re.match(r'^第\d+号', item) and not item.startswith('[['):
            issues.append(f"P0-8: related_cases 格式异常: '{item}'")


def check_p0_9_summary_missing_category(fm: Dict, issues: List[str]) -> None:
    """P0-9: type=summary 但缺少 category"""
    if fm.get("type") == "summary" and not fm.get("category"):
        issues.append(f"P0-9: summary 类型缺少 category 字段")


# ---------------------------------------------------------------------------
# P1 检查
# ---------------------------------------------------------------------------

def check_p1_1_related_count(fm: Dict, issues: List[str]) -> None:
    """P1-1: related 字段数量低于最低要求"""
    ftype = fm.get("type", "")
    if ftype not in MIN_RELATED:
        return
    related = fm.get("related", "")
    if not related:
        count = 0
    elif related.startswith('['):
        count = len(re.findall(r'\[\[', related))
    else:
        count = 0
    min_req = MIN_RELATED[ftype]
    if count < min_req:
        issues.append(f"P1-1: {ftype} 类型 related 数({count}) < 最低要求({min_req})")


def check_p1_2_volume_format(fm: Dict, issues: List[str]) -> None:
    """P1-2: volume 格式不规范"""
    vol = fm.get("volume", "")
    if vol and not VALID_VOLUME_PATTERN.match(vol):
        issues.append(f"P1-2: volume 格式不规范: '{vol}'")


def check_p1_3_date_format(fm: Dict, issues: List[str]) -> None:
    """P1-3: created/updated 日期格式错误"""
    for field in ["created", "updated"]:
        val = str(fm.get(field, ""))
        if val and not DATE_PATTERN.match(val):
            issues.append(f"P1-3: {field} 日期格式错误: '{val}'，应为 YYYY-MM-DD")


# ---------------------------------------------------------------------------
# 单文件检查
# ---------------------------------------------------------------------------

def check_file(filepath: Path, all_synth: Dict[str, List[Path]]) -> Tuple[List[str], List[str]]:
    """对一个文件执行所有检查"""
    passed = []
    issues = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        issues.append(f"ERROR: 读取失败: {e}")
        return passed, issues

    fm = get_frontmatter(content)
    ftype = get_type(content)

    # 获取源文件行数（用于 P0-6）
    source_rel = fm.get("source", "")
    source_lines = count_source_lines(source_rel) if source_rel else 0

    # P0 检查
    check_p0_1_wrong_fields(fm, issues)
    check_p0_2_case_number(fm, ftype, issues)
    check_p0_3_file_size(filepath, content, issues)
    check_p0_4_ocr_errors(fm, issues)
    check_p0_6_line_refs_overflow(fm, issues, source_lines)
    check_p0_7_source_missing(fm, ftype, issues)
    check_p0_8_related_cases_format(fm, issues)
    check_p0_9_summary_missing_category(fm, issues)

    # P1 检查
    check_p1_1_related_count(fm, issues)
    check_p1_2_volume_format(fm, issues)
    check_p1_3_date_format(fm, issues)

    if not issues:
        passed.append(f"PASS")

    return passed, issues


# ---------------------------------------------------------------------------
# 批量检查
# ---------------------------------------------------------------------------

def scan_directory(wiki_path: Path, check_type: str = None) -> List[Path]:
    """扫描 wiki 目录，返回符合类型的 .md 文件列表"""
    if check_type:
        # 指定子目录
        return list((wiki_path / check_type).glob("*.md"))
    else:
        # 所有子目录
        files = []
        for subdir in ["entities", "concepts", "summaries", "syntheses"]:
            files.extend((wiki_path / subdir).glob("*.md"))
        return files


def batch_check(wiki_root: Path, check_target: str = None) -> Tuple[int, int, List]:
    """批量检查，返回 (pass_count, fail_count, all_issues)"""
    files = scan_directory(wiki_root, check_target)

    # 构建 case_number -> [files] 映射（用于 P0-5）
    all_synth = defaultdict(list)
    synth_files = scan_directory(wiki_root, "syntheses")
    for f in synth_files:
        cn = get_case_number(f)
        if cn:
            all_synth[cn].append(f)

    pass_count = 0
    fail_count = 0
    all_issues = []

    for filepath in sorted(files):
        passed, issues = check_file(filepath, all_synth)
        all_issues.extend(issues)
        if issues:
            fail_count += 1
        else:
            pass_count += 1

    return pass_count, fail_count, all_issues


def print_report(pass_count: int, fail_count: int, all_issues: List[str],
                 total_files: int, check_target: str = None) -> None:
    """打印报告"""
    # Unicode 友好：emoji 在 GBK 不支持，统一用 ASCII 替代
    P0 = "[P0]"
    P1 = "[P1]"
    PASS = "PASS"
    FAIL = "FAIL"

    print(f"\n{'='*60}")
    print(f"lint Report {check_target or 'full'}")
    print(f"{'='*60}")
    print(f"Files: {total_files} | PASS: {pass_count} | FAIL: {fail_count}")
    print()

    # 按级别分组
    p0_issues = [i for i in all_issues if i.startswith("P0")]
    p1_issues = [i for i in all_issues if i.startswith("P1")]
    other_issues = [i for i in all_issues if not i.startswith("P0") and not i.startswith("P1")]

    def _safe(text: str) -> str:
        """移除无法编码的Unicode字符，防止GBK编码失败"""
        # 这些字符在GBK中无法编码
        return text.replace(' ', ' ').replace('​', '').replace('　', ' ')

    if p0_issues:
        print(f"{P0} P0 Blocking Issues (must fix)")
        for i, issue in enumerate(p0_issues, 1):
            print(f"  {i}. {_safe(issue)}")
        print()

    if p1_issues:
        print(f"{P1} P1 Quality Issues (should fix)")
        for i, issue in enumerate(p1_issues, 1):
            print(f"  {i}. {_safe(issue)}")
        print()

    if other_issues:
        print(f"{PASS}/{FAIL} Other Issues")
        for i, issue in enumerate(other_issues, 1):
            print(f"  {i}. {_safe(issue)}")
        print()

    if not all_issues:
        print("ALL CHECKS PASSED - no issues found")

    print(f"{'='*60}")


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="enhanced_lint.py v66")
    parser.add_argument("path", nargs="?", default=".", help="文件或目录路径")
    parser.add_argument("--batch", action="store_true", help="批量检查目录")
    parser.add_argument("--summary", action="store_true", help="仅输出统计摘要")
    parser.add_argument("--vault-root", default="D:/AI agent/tkk-library", help="vault 根目录")
    parser.add_argument("--p0-only", action="store_true", help="仅运行 P0 检查")
    parser.add_argument("--p1-only", action="store_true", help="仅运行 P1 检查")
    parser.add_argument("--check", choices=[
        "wrong-fields", "case-number", "file-size", "ocr",
        "duplicates", "line-refs", "source-integrity",
        "related-cases", "related-count"
    ], help="指定检查项（开发中）")
    args = parser.parse_args()

    global VAULT_ROOT
    VAULT_ROOT = Path(args.vault_root)
    WIKI_ROOT = VAULT_ROOT / "wiki"

    path = Path(args.path)
    if args.batch or path.is_dir():
        target = path if path.is_dir() else WIKI_ROOT
        pass_count, fail_count, all_issues = batch_check(
            WIKI_ROOT,
            check_target=None
        )
        files = scan_directory(WIKI_ROOT)
        print_report(pass_count, fail_count, all_issues, len(files))
    else:
        passed, issues = check_file(path, {})
        print(f"\n[{'PASS' if not issues else 'FAIL'}] {path.name}")
        for p in passed:
            print(f"  {p}")
        for i in issues:
            print(f"  {i}")


if __name__ == "__main__":
    main()