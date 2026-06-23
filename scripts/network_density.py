#!/usr/bin/env python3
"""
network_density.py
统计知识网络密度指标

用法: python scripts/network_density.py
"""

import re
from pathlib import Path
from collections import defaultdict

VAULT_PATH = Path("D:/AI agent/tkk-library/wiki")

def count_links_and_refs():
    stats = {
        'total_files': 0,
        'total_outlinks': 0,
        'files_with_no_outlinks': 0,
        'files_with_no_inlinks': 0,
        'by_type': defaultdict(lambda: {'outlinks': 0, 'inlinks': 0, 'files': 0})
    }

    # 全局 inlink 统计
    all_links = defaultdict(list)  # target -> sources

    files = list(VAULT_PATH.rglob("*.md"))
    stats['total_files'] = len(files)

    for md_file in files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 获取 type
        type_match = re.search(r'^type:\s*(\w+)', content, re.MULTILINE)
        file_type = type_match.group(1) if type_match else 'unknown'
        stats['by_type'][file_type]['files'] += 1

        # 提取 outlinks（排除脚注定义中的链接）
        outlinks = re.findall(r'\[\[([^\]#^]+)', content)
        # 过滤掉脚注定义中的链接（[^fnN]格式）
        outlinks = [l for l in outlinks if not re.match(r'^[0-9]+$', l)]

        stats['total_outlinks'] += len(outlinks)
        stats['by_type'][file_type]['outlinks'] += len(outlinks)

        # 记录 inlinks
        for link in outlinks:
            all_links[link].append(md_file.relative_to(VAULT_PATH))

        if len(outlinks) == 0:
            stats['files_with_no_outlinks'] += 1

    # 计算 inlinks
    for md_file in files:
        rel_path = md_file.relative_to(VAULT_PATH).as_posix()
        inlink_count = 0

        # 精确匹配
        inlink_count += len(all_links.get(rel_path, []))
        inlink_count += len(all_links.get(rel_path.replace('.md', ''), []))

        # 大小写不敏感匹配
        rel_path_lower = rel_path.lower()
        for key, sources in all_links.items():
            if key.lower() == rel_path_lower:
                inlink_count += len(sources)

        if inlink_count == 0:
            stats['files_with_no_inlinks'] += 1

        type_match = re.search(r'^type:\s*(\w+)', open(md_file, encoding='utf-8').read(), re.MULTILINE)
        file_type = type_match.group(1) if type_match else 'unknown'
        stats['by_type'][file_type]['inlinks'] += inlink_count

    return stats

def main():
    stats = count_links_and_refs()

    print("=" * 60)
    print("知识网络密度统计")
    print("=" * 60)
    print()
    print(f"总文件数:     {stats['total_files']}")
    print(f"总出链数:     {stats['total_outlinks']}")
    print(f"平均出链:     {stats['total_outlinks']/stats['total_files']:.2f}")
    print(f"孤立节点(无出链): {stats['files_with_no_outlinks']}")
    print(f"孤立节点(无入链): {stats['files_with_no_inlinks']}")
    print()

    print("按类型统计:")
    print(f"{'类型':<12} {'文件数':<8} {'出链':<8} {'入链':<8} {'平均出链':<10}")
    print("-" * 60)
    for ftype, counts in sorted(stats['by_type'].items()):
        avg = counts['outlinks'] / counts['files'] if counts['files'] > 0 else 0
        print(f"{ftype:<12} {counts['files']:<8} {counts['outlinks']:<8} {counts['inlinks']:<8} {avg:<10.2f}")

    print()
    print("=" * 60)

    # 返回孤立文件列表
    print("\n孤立节点（无入链）前10个:")
    files = list(VAULT_PATH.rglob("*.md"))
    orphan_files = []

    all_links = defaultdict(list)
    for md_file in files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        outlinks = re.findall(r'\[\[([^\]#^]+)', content)
        for link in outlinks:
            if not re.match(r'^[0-9]+$', link):
                all_links[link].append(md_file.relative_to(VAULT_PATH))

    for md_file in files:
        rel_path = md_file.relative_to(VAULT_PATH).as_posix()
        inlink_count = len(all_links.get(rel_path, [])) + len(all_links.get(rel_path.replace('.md', ''), []))
        if inlink_count == 0:
            type_match = re.search(r'^type:\s*(\w+)', open(md_file, encoding='utf-8').read(), re.MULTILINE)
            file_type = type_match.group(1) if type_match else 'unknown'
            if file_type != 'summary':  # summary 允许孤立
                orphan_files.append((rel_path, file_type))

    for rel_path, ftype in sorted(orphan_files)[:10]:
        print(f"  [{ftype}] {rel_path}")

    if len(orphan_files) > 10:
        print(f"  ... 还有 {len(orphan_files) - 10} 个")

    return stats

if __name__ == '__main__':
    main()
