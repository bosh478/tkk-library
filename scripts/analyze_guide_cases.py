#!/usr/bin/env python3
"""分析指导性案例源文件，提取所有案例编号"""

import re
from pathlib import Path

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-指导性案例-md")

def extract_case_numbers(file_path):
    """从源文件中提取所有检例编号"""
    content = file_path.read_text(encoding='utf-8')
    # 匹配模式：检例第X号
    pattern = r'检例第(\d+)号'
    matches = re.findall(pattern, content)
    return [int(m) for m in matches]

def main():
    source_files = sorted(SOURCE_DIR.glob("*.md"))
    all_cases = set()

    print(f"源文件数量: {len(source_files)}")
    print()

    for f in source_files:
        cases = extract_case_numbers(f)
        all_cases.update(cases)
        if cases:
            min_case = min(cases)
            max_case = max(cases)
            print(f"{f.name}: 检例第{min_case}-{max_case}号 ({len(cases)}个)")

    print(f"\n总计案例编号: {len(all_cases)}个")
    print(f"案例编号范围: {min(all_cases)} - {max(all_cases)}")

    # 检查已有文件
    existing = []
    for i in range(1, 300):
        p = Path(f"D:/AI agent/tkk-library/wiki/syntheses/SPP_GuideCase_检例第{i}号.md")
        if p.exists():
            existing.append(i)

    print(f"\n已有文件: {len(existing)}个")
    if existing:
        print(f"已有编号: {existing[0]}-{existing[-1]}")

    # 计算需要创建的
    needed = [i for i in sorted(all_cases) if i not in existing]
    print(f"\n需要创建: {len(needed)}个")
    if needed:
        print(f"需要创建的编号范围: {needed[0]}-{needed[-1]}")

if __name__ == "__main__":
    main()