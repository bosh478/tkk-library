#!/usr/bin/env python3
"""
verify_wikilinks.py
验证所有 wikilink 指向的目标文件存在，检测断链
忽略 markdown 加粗格式 **text** 中的 text

用法: python scripts/verify_wikilinks.py
"""

import re
from pathlib import Path

VAULT_PATH = Path("D:/AI agent/tkk-library/wiki")
SOURCES_PATH = Path("D:/AI agent/tkk-library/sources")

def preprocess_content(content):
    """预处理内容：移除 markdown 加粗格式"""
    content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)
    content = re.sub(r'^\|?[-:]+\|.*$', '', content, flags=re.MULTILINE)
    return content

def extract_wikilinks(content):
    """提取所有 wikilink"""
    content = preprocess_content(content)
    return re.findall(r'\[\[([^\]#^]+)', content)

def build_lookup_table(root_path):
    """构建 lookup 表：lowercase -> set of actual filenames"""
    lookup = {}
    for f in root_path.rglob("*.md"):
        rel_path = f.relative_to(root_path).as_posix()
        name_no_ext = rel_path.replace('.md', '')
        key = name_no_ext.lower()
        if key not in lookup:
            lookup[key] = set()
        lookup[key].add(name_no_ext)
        lookup[key].add(rel_path)
    return lookup

def verify_link_fast(link_target, wiki_lookup, sources_lookup):
    """快速验证链接是否存在"""
    base = link_target.split('#')[0].split('^')[0]
    if not base:
        return True, None

    candidates = [
        base,
        f"{base}.md",
        base.replace('/', '_'),
        f"{base.replace('/', '_')}.md",
    ]

    for candidate in candidates:
        key = candidate.lower()
        if key in wiki_lookup:
            return True, None
        if key in sources_lookup:
            return True, None

    return False, base

def main():
    print(f"{'='*50}")
    print("Wikilink 断链检测")
    print(f"{'='*50}\n")

    print("构建文件索引...")
    wiki_lookup = build_lookup_table(VAULT_PATH)
    sources_lookup = build_lookup_table(SOURCES_PATH)
    print(f"  wiki 文件: {len(wiki_lookup)} 条目")
    print(f"  sources 文件: {len(sources_lookup)} 条目")

    broken_links = []
    total_links = 0
    processed = 0

    print("\n扫描中...")

    for md_file in VAULT_PATH.rglob("*.md"):
        processed += 1
        if processed % 1000 == 0:
            print(f"  已处理 {processed} 文件...")

        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        links = extract_wikilinks(content)
        for link in links:
            total_links += 1
            exists, target = verify_link_fast(link, wiki_lookup, sources_lookup)
            if not exists:
                broken_links.append((md_file.relative_to(VAULT_PATH), link))

    print(f"\n总计检查 wikilink: {total_links} 个")
    print(f"总文件数: {len(wiki_lookup)}")
    print()

    if broken_links:
        print(f"=== 发现 {len(broken_links)} 个断链 ===\n")
        by_file = {}
        for file, link in broken_links:
            if file not in by_file:
                by_file[file] = []
            by_file[file].append(link)

        for file, links in sorted(by_file.items())[:50]:
            print(f"  {file}:")
            for link in links[:10]:
                print(f"    - [[{link}]]")
            if len(links) > 10:
                print(f"    ... 还有 {len(links) - 10} 个")
            print()
        if len(by_file) > 50:
            print(f"  ... 还有 {len(by_file) - 50} 个文件有断链")
    else:
        print("=== 断链检测: PASS ===")
        print("所有 wikilink 均有效")

    print(f"\n{'='*50}")
    return len(broken_links) == 0

if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
