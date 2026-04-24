#!/usr/bin/env python3
"""
修复 vault 质量问题：
1. 为 Court_GuideCase 系列文件添加标准 frontmatter
2. 修复 source: [["xxx"]] → sources: ["xxx"] 格式
3. 为内容过少的入库案例文件补充内容（从 sources 目录读取）
"""

import os
import re
import glob

WIKI_DIR = r"D:\AI agent\tkk-library\wiki"
SOURCES_DIR = r"D:\AI agent\tkk-library\sources"

def safe_read_file(filepath):
    """安全读取文件，尝试多种编码"""
    encodings = ['utf-8', 'gbk', 'gb2312', 'latin1']
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    return None

def safe_write_file(filepath, content):
    """安全写入文件，使用 utf-8"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"    Error writing {filepath}: {e}")
        return False

def add_frontmatter_to_court_guide_case(filepath, content):
    """为 Court_GuideCase 文件添加 frontmatter"""
    filename = os.path.basename(filepath)

    if filename.startswith("Court_GuideCase_"):
        rest = filename[16:]

        if rest.startswith("("):
            parts = rest.split("_", 1)
            if len(parts) > 1:
                title = parts[1].replace(".md", "").strip()
            else:
                title = rest.replace(".md", "").strip()
        else:
            match = re.match(r'^(\d+)_(.*)\.md$', rest)
            if match:
                case_num = match.group(1)
                title = f"指导性案例{case_num}号 - {match.group(2)}"
            else:
                title = rest.replace(".md", "").strip()

        frontmatter = f"""---
title: {title}
type: synthesis
created: 2026-04-18
updated: 2026-04-18
tags: [指导性案例, 最高人民法院]
source: [[Court_GuideCase_{filename[16:]}]]
---

"""
        if content.startswith('---'):
            return False, "already has frontmatter"

        return True, frontmatter
    return False, "not a Court_GuideCase file"

def fix_source_format(content):
    """修复 source: [["xxx"]] → sources: ["xxx"] 格式"""
    fixed = False
    pattern = r'source:\s*\[\[([^\]]+)\]\]'
    match = re.search(pattern, content)
    if match:
        inner = match.group(1)
        new_value = inner.replace('"', '').replace('[[', '').replace(']]', '')
        new_line = f"sources: [{new_value}]"
        content = re.sub(pattern, new_line, content, count=1)
        fixed = True

    return fixed, content

def check_content_too_short(content):
    """检查文件内容是否过少"""
    if not content:
        return False, 0

    lines = content.split('\n')
    in_frontmatter = False
    body_start = 0
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
            else:
                body_start = i + 1
                break

    if body_start < len(lines):
        body = '\n'.join(lines[body_start:])
        return len(body) < 100, len(body)
    return False, 0

def find_source_file_for_ruku_case(filename):
    """为入库案例 wiki 文件查找对应的 source 文件"""
    # 从 wiki 文件名提取 source 文件名
    # 格式: Court_入库案例_2023-02-1-233-001_入库案例 2023-02-1-233-001.md
    # 目标: 入库案例 2023-02-1-233-001.md

    # 提取日期和编号
    # Court_入库案例_2023-02-1-233-001_入库案例 2023-02-1-233-001.md
    match = re.search(r'Court_入库案例_(\d{4}-\d{2}-\d-\d{3}-\d{3})_', filename)
    if match:
        case_id = match.group(1)
        # 在 sources 目录搜索
        search_pattern = f"入库案例 {case_id}.md"
        for root, dirs, files in os.walk(SOURCES_DIR):
            for f in files:
                if f == f"入库案例 {case_id}.md":
                    return os.path.join(root, f)
    return None

def process_file(filepath):
    """处理单个文件"""
    filename = os.path.basename(filepath)
    results = []

    content = safe_read_file(filepath)
    if content is None:
        results.append(f"  - {filename}: ERROR reading file")
        return results

    needs_write = False
    new_content = content

    # 1. 检查是否需要添加 Court_GuideCase frontmatter
    if filename.startswith("Court_GuideCase_"):
        if not content.startswith('---'):
            success, frontmatter_or_msg = add_frontmatter_to_court_guide_case(filepath, content)
            if success:
                new_content = frontmatter_or_msg + content
                needs_write = True
                results.append(f"  - {filename}: added frontmatter")
        else:
            results.append(f"  - {filename}: already has frontmatter")

    # 2. 检查是否需要修复 source 格式
    fixed, new_content = fix_source_format(new_content)
    if fixed:
        needs_write = True
        results.append(f"  - {filename}: fixed source format")

    # 3. 检查文件内容是否过少 - 尝试从 source 补充
    too_short, body_len = check_content_too_short(new_content)
    if too_short and "Court_入库案例_" in filename:
        source_file = find_source_file_for_ruku_case(filename)
        if source_file and os.path.exists(source_file):
            source_content = safe_read_file(source_file)
            if source_content:
                # 从 source 提取内容（跳过第一行标题）
                lines = source_content.split('\n')
                body_lines = []
                capture = False
                for line in lines[1:]:
                    body_lines.append(line)

                source_body = '\n'.join(body_lines).strip()
                if len(source_body) > 100:
                    # 构建新内容：保留 frontmatter，替换正文
                    frontmatter_end = new_content.find('---', 3) + 4
                    frontmatter = new_content[:frontmatter_end]
                    new_content = frontmatter + '\n' + source_body
                    needs_write = True
                    results.append(f"  - {filename}: filled content from source ({len(source_body)} chars)")
                else:
                    results.append(f"  - {filename}: content too short ({body_len} chars, source also short)")
            else:
                results.append(f"  - {filename}: content too short ({body_len} chars)")
        else:
            results.append(f"  - {filename}: content too short ({body_len} chars, no source found")
    elif too_short:
        results.append(f"  - {filename}: content too short ({body_len} chars)")

    if needs_write:
        safe_write_file(filepath, new_content)

    return results

def main():
    print("开始修复 vault 质量问题...")
    print()

    syntheses_dir = os.path.join(WIKI_DIR, "syntheses")

    stats = {
        "court_guide_case_fixed": 0,
        "source_format_fixed": 0,
        "content_too_short": 0,
        "content_filled": 0,
        "errors": 0,
    }

    for root, dirs, files in os.walk(syntheses_dir):
        for filename in files:
            if filename.endswith('.md'):
                filepath = os.path.join(root, filename)
                try:
                    results = process_file(filepath)
                    for r in results:
                        print(r)
                        if "added frontmatter" in r:
                            stats["court_guide_case_fixed"] += 1
                        if "fixed source format" in r:
                            stats["source_format_fixed"] += 1
                        if "content too short" in r:
                            stats["content_too_short"] += 1
                        if "filled content" in r:
                            stats["content_filled"] += 1
                        if "ERROR" in r:
                            stats["errors"] += 1
                except Exception as e:
                    print(f"  - {filename}: ERROR - {e}")
                    stats["errors"] += 1

    print()
    print("=" * 50)
    print("修复完成统计:")
    print(f"  - Court_GuideCase 添加 frontmatter: {stats['court_guide_case_fixed']}")
    print(f"  - 修复 source 格式: {stats['source_format_fixed']}")
    print(f"  - 内容过少的文件: {stats['content_too_short']}")
    print(f"  - 从 source 补充内容: {stats['content_filled']}")
    print(f"  - 错误文件数: {stats['errors']}")

if __name__ == "__main__":
    main()