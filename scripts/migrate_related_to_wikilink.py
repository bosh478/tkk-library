#!/usr/bin/env python3
"""
migrate_related_to_wikilink.py
批量将 related 字段迁移为标准 wikilink 格式

用法: python scripts/migrate_related_to_wikilink.py [--dry-run] [--path <路径>]
"""

import re
from pathlib import Path
import argparse

VAULT_PATH = Path("D:/AI agent/tkk-library/wiki")

def is_valid_link(link):
    """验证是否有效链接（排除加粗、表格等格式字符）"""
    link = link.strip()
    if not link:
        return False
    if '**' in link:
        return False
    if '|' in link:
        return False
    if link.startswith('[') or link.endswith(']'):
        return False
    if link.startswith('-') or link.startswith('*'):
        return False
    if link.startswith('http'):
        return False
    if re.match(r'^[\|\-\*\s]+$', link):
        return False
    if re.match(r'^\|?[-:]+\|', link):
        return False
    return True

def extract_related_links_from_field(field_value):
    """从 related 字段值中提取链接（仅扫描该字段，不扫描全文）"""
    links = []
    content = field_value

    # [[link]] 格式
    for match in re.finditer(r'\[\[([^\]]+)\]\]', content):
        link = match.group(1)
        if is_valid_link(link):
            links.append(link)

    # [link1, link2] 单行数组格式
    if content.strip().startswith('[') and ']' in content:
        inner = re.search(r'\[(.+)\]', content, re.DOTALL)
        if inner:
            for item in inner.group(1).split(','):
                item = item.strip().strip('"').strip("'")
                if is_valid_link(item):
                    links.append(item)

    # 无括号格式（逗号分隔）
    else:
        for line in content.split('\n'):
            line = line.strip().rstrip(',')
            line = re.sub(r'^[\-\*\s]+', '', line)
            if line and not line.startswith('[') and not line.startswith('#'):
                parts = re.split(r'[,\s]+', line)
                for part in parts:
                    part = part.strip().strip('"').strip("'").strip('[]')
                    if is_valid_link(part):
                        links.append(part)

    return list(set(links))

def clean_link(link):
    """清理链接：去除 .md 后缀"""
    link = link.strip()
    if link.endswith('.md'):
        link = link[:-3]
    return link

def migrate_file(filepath, dry_run=True):
    """迁移单个文件的 related 字段"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否已经是 wikilink 格式（related:\n 开头）
    if re.search(r'^related:\s*\n', content, re.MULTILINE):
        return False

    # 仅提取 related 字段值进行扫描
    match = re.search(r'^related:\s*(.+?)(?=^\w|\Z)', content, re.MULTILINE | re.DOTALL)
    if not match:
        return False

    field_value = match.group(1)
    links = extract_related_links_from_field(field_value)
    if not links:
        return False

    # 清理链接
    cleaned_links = [clean_link(link) for link in links if clean_link(link)]

    # 构建新的 related 格式
    new_related = "related:\n" + "\n".join([f"  - [[{link}]]" for link in cleaned_links])

    # 替换
    new_content = re.sub(
        r'^related:\s*.+?(?=^\w|\Z)',
        new_related,
        content,
        flags=re.MULTILINE | re.DOTALL
    )

    if new_content != content:
        if not dry_run:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
        return True
    return False

def main():
    parser = argparse.ArgumentParser(description='迁移 related 字段为 wikilink')
    parser.add_argument('--dry-run', action='store_true', help='仅预览不写入')
    parser.add_argument('--path', type=str, help='指定路径')
    args = parser.parse_args()

    dry_run = args.dry_run
    target_path = Path(args.path) if args.path else VAULT_PATH

    print(f"{'='*50}")
    print(f"related 字段迁移工具")
    print(f"模式: {'预览' if dry_run else '执行'}")
    print(f"目录: {target_path}")
    print(f"{'='*50}\n")

    count = 0
    for md_file in target_path.rglob("*.md"):
        try:
            if migrate_file(md_file, dry_run=dry_run):
                rel_path = md_file.relative_to(VAULT_PATH)
                print(f"{'[执行]' if not dry_run else '[预览]'}: {rel_path}")
                count += 1
        except Exception as e:
            print(f"[错误] {md_file}: {e}")

    print(f"\n{'='*50}")
    print(f"{'预览' if dry_run else '迁移'}完成: {count} 个文件")
    if dry_run:
        print("（使用 --dry-run 参数仅预览，实际迁移请不加此参数）")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
