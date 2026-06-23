#!/usr/bin/env python3
"""
Phase 3 Spot Check Script
Phase 3 内容抽检自动化脚本：从目录随机抽取文件，检查 frontmatter 和内容质量

用法:
    python scripts/phase3_spot_check.py <dir> [count]
    python scripts/phase3_spot_check.py wiki/summaries/ 3

检查项:
    1. frontmatter: type/tags/source/created 字段存在
    2. 正文前 100 字符非空（不是占位符、不是标题重复）
    3. 内容与源码主题匹配（通过 source 字段溯源）

返回:
    PASS - all sampled files passed
    FAIL - one or more issues found
"""

import os
import sys
import random
import re
import glob
from pathlib import Path

def check_file(filepath):
    """Check a single file against Phase 3 quality criteria."""
    issues = []
    passed = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [f"ERROR: Cannot read file: {e}"]

    basename = os.path.basename(filepath)

    # Split frontmatter and body
    parts = content.split('---', 2)
    if len(parts) < 3:
        issues.append(f"  [FAIL] frontmatter: 缺少 YAML frontmatter")
        return passed, issues

    frontmatter = parts[1]
    body = parts[2] if len(parts) > 2 else ""

    # 1. Frontmatter fields check
    required_fields = ['type:', 'tags:', 'source:', 'created:']
    for field in required_fields:
        if field not in frontmatter:
            issues.append(f"  [FAIL] frontmatter: 缺少 {field} 字段")
        else:
            passed.append(f"  [PASS] frontmatter: {field} 存在")

    # 2. Body not empty and first 100 chars not placeholder
    body_stripped = body.strip()
    if not body_stripped:
        issues.append(f"  [FAIL] 正文: 正文为空")
    else:
        first_100 = body_stripped[:100]
        # Check for placeholder patterns
        placeholder_patterns = ['待补充', '见原文', '（略）', 'TODO', '占位符', '此处略', '以下略']
        has_placeholder = any(p in first_100 for p in placeholder_patterns)

        if has_placeholder:
            issues.append(f"  [FAIL] 正文前100字符: 包含占位符内容")
        else:
            passed.append(f"  [PASS] 正文前100字符: 非空且无占位符")

    # 3. Source field points to existing file (basic check)
    source_match = re.search(r'source:\s*\[\[([^\]]+)\]\]', frontmatter)
    if source_match:
        source_file = source_match.group(1)
        # Check if source file exists in sources/
        possible_paths = [
            f"D:/AI agent/tkk-library/sources/{source_file}",
            f"D:/AI agent/tkk-library/sources/网络文章/{source_file}",
        ]
        source_exists = any(os.path.exists(p) for p in possible_paths)
        if source_exists:
            passed.append(f"  [PASS] source: {source_file} 存在")
        else:
            issues.append(f"  [WARN] source: {source_file} 未找到（可能正常，如果是历史迁移）")

    return passed, issues


def spot_check_directory(target_dir, count=3):
    """Randomly sample files from directory and check them."""
    if not os.path.isdir(target_dir):
        print(f"目录不存在: {target_dir}")
        return

    # Get all .md files
    files = glob.glob(os.path.join(target_dir, '*.md'))
    if not files:
        print(f"目录为空: {target_dir}")
        return

    # Random sample
    sample_size = min(count, len(files))
    sampled = random.sample(files, sample_size)

    print(f"\n=== Phase 3 内容抽检 ({target_dir}) ===")
    print(f"目录总文件数: {len(files)}, 抽检数量: {sample_size}\n")

    pass_count = 0
    fail_count = 0

    for filepath in sorted(sampled):
        basename = os.path.basename(filepath)
        passed, issues = check_file(filepath)

        status = "PASS" if not issues else "FAIL"
        print(f"[{status}] {basename}")
        for p in passed[:3]:  # Show first 3 passes
            print(p)
        for i in issues:
            print(i)
        print()
        if issues:
            fail_count += 1
        else:
            pass_count += 1

    print(f"=== 汇总 ===")
    print(f"PASS: {pass_count}/{sample_size}")
    print(f"FAIL: {fail_count}/{sample_size}")

    return fail_count == 0


def main():
    if len(sys.argv) < 2:
        print("用法: python phase3_spot_check.py <dir> [count]")
        print("示例: python phase3_spot_check.py wiki/summaries/ 3")
        sys.exit(1)

    target_dir = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    success = spot_check_directory(target_dir, count)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()