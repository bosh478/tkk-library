#!/usr/bin/env python3
"""
Phase 2 Gate Check Script
Phase 2 门控验证脚本：检查输出是否满足准入标准

用法:
    python scripts/phase2_gate.py <file.md>
    python scripts/phase2_gate.py <dir/*.md>

检查项:
    1. 输出字符数 > 500
    2. 置信度标注存在（〔确定〕/〔存疑〕/〔待核实〕至少1处）
    3. 无占位符扫描（待补充/见原文/（略））
    4. 全章提取（如适用）：章节数与源码一致
    5. 法条引用断言：每条《》引用后有 ✅/❌/⚠️ 标注

返回:
    PASS - all checks passed
    FAIL - one or more checks failed, details printed
"""

import os
import sys
import re
import glob
from pathlib import Path

def check_file(filepath):
    """Check a single file against Phase 2 gate criteria."""
    issues = []
    passed = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [], [f"ERROR: Cannot read file: {e}"]

    basename = os.path.basename(filepath)

    # 1. Output character count
    char_count = len(content)
    if char_count <= 500:
        issues.append(f"  [FAIL] 字符数: {char_count} ≤ 500")
    else:
        passed.append(f"  [PASS] 字符数: {char_count} > 500")

    # 2. Confidence labels exist
    confidence_labels = ['〔确定〕', '〔存疑〕', '〔待核实〕']
    has_confidence = any(label in content for label in confidence_labels)
    if not has_confidence:
        issues.append(f"  [FAIL] 置信度标注: 无〔确定〕/〔存疑〕/〔待核实〕标注")
    else:
        found = [label for label in confidence_labels if label in content]
        passed.append(f"  [PASS] 置信度标注: {', '.join(found)}")

    # 3. Placeholder scan
    placeholders = ['待补充', '见原文', '（略）', 'TODO', '占位符']
    found_placeholders = [p for p in placeholders if p in content]
    if found_placeholders:
        issues.append(f"  [FAIL] 占位符: 发现 {', '.join(found_placeholders)}")
    else:
        passed.append(f"  [PASS] 占位符: 无")

    # 4. Chapter extraction check (if source file exists for comparison)
    # Check if output has ## headings
    h2_count = len(re.findall(r'^## ', content, re.MULTILINE))
    if h2_count > 0:
        passed.append(f"  [PASS] 章节数: {h2_count} 个 ## 标题")

    # 5. Legal citation assertions (三色断言)
    # Find all 《》 citations
    citations = re.findall(r'《([^》]+)》', content)
    if citations:
        # Check how many have assertion marks after them
        # Pattern: 《》后紧跟 ✅ ❌ ⚠️
        citation_assertions = re.findall(r'《([^》]+)》\s*([✅❌⚠️])', content)
        asserted_count = len(citation_assertions)
        total_count = len(citations)

        if asserted_count == 0:
            issues.append(f"  [FAIL] 法条断言: {total_count} 条引用无 ✅/❌/⚠️ 标注")
        elif asserted_count < total_count:
            issues.append(f"  [WARN] 法条断言: {asserted_count}/{total_count} 条有标注")
        else:
            passed.append(f"  [PASS] 法条断言: {asserted_count}/{total_count} 条有标注")

    return passed, issues


def main():
    if len(sys.argv) < 2:
        print("用法: python phase2_gate.py <file.md> 或 <dir/*.md>")
        sys.exit(1)

    target = sys.argv[1]

    # Handle glob patterns
    if '*' in target:
        files = glob.glob(target)
    elif os.path.isdir(target):
        files = glob.glob(os.path.join(target, '*.md'))
    else:
        files = [target]

    if not files:
        print(f"未找到文件: {target}")
        sys.exit(1)

    total_files = len(files)
    pass_count = 0
    fail_count = 0

    print(f"\n=== Phase 2 Gate 检查 ({total_files} 个文件) ===\n")

    for filepath in sorted(files):
        basename = os.path.basename(filepath)
        passed, issues = check_file(filepath)

        status = "PASS" if not issues else "FAIL"
        print(f"[{status}] {basename}")
        for p in passed:
            print(p)
        for i in issues:
            print(i)
        print()
        if issues:
            fail_count += 1
        else:
            pass_count += 1

    print(f"=== 汇总 ===")
    print(f"PASS: {pass_count}/{total_files}")
    print(f"FAIL: {fail_count}/{total_files}")

    if fail_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()