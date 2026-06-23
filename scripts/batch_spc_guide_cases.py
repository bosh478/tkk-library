#!/usr/bin/env python3
"""批量处理最高法指导性案例生成synthesis wiki页面"""

import os
import re
import sys

VAULT_ROOT = "D:/AI agent/tkk-library"
SOURCE_DIR = os.path.join(VAULT_ROOT, "sources/2-案例库/最高法-指导性案例")
TARGET_DIR = os.path.join(VAULT_ROOT, "wiki/syntheses")

def extract_case_number(filename):
    """从文件名提取案例编号，如'指导案例144号' -> 144"""
    match = re.search(r'指导.例(\d+)号', filename)
    return int(match.group(1)) if match else None

def extract_case_name(filename):
    """从文件名提取案例简称"""
    # 去掉扩展名
    name = os.path.splitext(filename)[0]
    # 去掉"指导案例NN号："或"指导性案例NN号："前缀
    match = re.match(r'指导案例?\d+号：?(.*)', name)
    return match.group(1) if match else name

def extract_tags(content):
    """从内容提取关键词作为tags"""
    tags = ["最高法指导性案例"]
    # 提取关键词行
    keyword_match = re.search(r'关键词[:：]\s*(.+?)(?=\n|$)', content)
    if keyword_match:
        keywords = keyword_match.group(1)
        # 处理关键词中的中英文斜杠
        for kw in re.split(r'[/／]', keywords):
            kw = kw.strip()
            if kw and kw not in tags:
                if kw in ['刑事', '民事', '行政', '执行']:
                    tags.append(kw)
                elif any(x in kw for x in ['正当防卫', '合同', '侵权', '劳动', '执行', '信息公开', '专利', '商标', '环境', '金融']):
                    tags.append(kw)
    return tags[:6]  # 限制tag数量

def extract_problem意识(content):
    """从裁判要点提取问题意识（一句话）"""
    # 找裁判要点
    match = re.search(r'裁判要点\s*\n\s*(.+?)(?=\n相关法条)', content, re.DOTALL)
    if match:
        points = match.group(1).strip()
        # 取第一点的前50字
        first_point = points.split('\n')[0].strip()
        if len(first_point) > 60:
            return first_point[:57] + "..."
        return first_point
    return "核心法律问题待提取"

def extract_related_laws(content):
    """提取相关法条"""
    match = re.search(r'相关法条\s*\n\s*(.+?)(?=\n基本案情)', content, re.DOTALL)
    if match:
        laws = match.group(1).strip()
        # 提取法条名
        law_matches = re.findall(r'《([^》]+)》', laws)
        return law_matches
    return []

def read_source_file(filepath):
    """读取源文件内容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def generate_synthesis(filename, content):
    """生成synthesis页面内容"""
    case_num = extract_case_number(filename)
    case_name = extract_case_name(filename)

    if not case_num:
        return None

    tags = extract_tags(content)
    problem意识 = extract_problem意识(content)
    related_laws = extract_related_laws(content)

    # 构建related字段
    related = []
    for law in related_laws[:3]:
        # 转换为concept名
        concept_name = f"concept_{law.replace('《', '').replace('》', '')}"
        related.append(f"  - [[{concept_name}]]")

    # 生成line-refs
    line_refs_key = filename

    frontmatter = f"""---
title: 指导案例{case_num}号：{case_name}
type: synthesis
created: 2026-05-08
updated: 2026-05-08
tags: [{', '.join(tags)}]
source: sources/2-案例库/最高法-指导性案例/{filename}
案例分级: ⭐⭐⭐⭐⭐
问题意识: {problem意识}
line-refs:
  "{filename}": [1]
related:
{chr(10).join(related) if related else '  - []'}
---

# 指导案例{case_num}号：{case_name}

## 裁判要点

"""

    # 提取裁判要点正文
    points_match = re.search(r'裁判要点\s*\n\s*(.+?)(?=\n相关法条)', content, re.DOTALL)
    if points_match:
        frontmatter += points_match.group(1).strip() + "\n\n"

    # 添加相关法条
    if related_laws:
        frontmatter += "## 相关法条\n\n"
        for law in related_laws:
            frontmatter += f"- {law}\n"
        frontmatter += "\n"

    # 提取基本案情
    case_match = re.search(r'基本案情\s*\n\s*(.+?)(?=\n裁判结果)', content, re.DOTALL)
    if case_match:
        frontmatter += "## 基本案情\n\n" + case_match.group(1).strip() + "\n\n"

    # 提取裁判结果
    result_match = re.search(r'裁判结果\s*\n\s*(.+?)(?=\n裁判理由)', content, re.DOTALL)
    if result_match:
        frontmatter += "## 裁判结果\n\n" + result_match.group(1).strip() + "\n\n"

    # 提取裁判理由
    reason_match = re.search(r'裁判理由\s*\n\s*(.+?)$', content, re.DOTALL)
    if reason_match:
        frontmatter += "## 裁判理由\n\n" + reason_match.group(1).strip() + "\n"

    return frontmatter

def process_files(start_num, end_num):
    """处理指定编号范围的案例文件"""
    files = os.listdir(SOURCE_DIR)

    processed = 0
    skipped = 0

    for filename in files:
        case_num = extract_case_number(filename)
        case_name = extract_case_name(filename)
        if case_num is None:
            continue
        if case_num < start_num or case_num > end_num:
            continue

        # 检查目标文件是否已存在
        # 截断过长的案件名，避免文件名超限
        safe_name = case_name[:80] if len(case_name) > 80 else case_name
        target_name = f"SPC_GuideCase_指导案例{case_num}号_{safe_name}.md"
        target_path = os.path.join(TARGET_DIR, target_name)

        if os.path.exists(target_path):
            print(f"SKIP (exists): {target_name}")
            skipped += 1
            continue

        # 也检查无后缀版本（兼容旧文件）
        target_name_no_suffix = f"SPC_GuideCase_指导案例{case_num}号.md"
        target_path_no_suffix = os.path.join(TARGET_DIR, target_name_no_suffix)
        if os.path.exists(target_path_no_suffix):
            # 删除旧文件，重写新文件
            os.remove(target_path_no_suffix)
            print(f"REPLACE (old): {target_name_no_suffix} -> {target_name}")

        # 读取源文件
        content = read_source_file(os.path.join(SOURCE_DIR, filename))
        if content is None:
            continue

        # 生成synthesis
        synthesis = generate_synthesis(filename, content)
        if synthesis is None:
            continue

        # 写入目标文件
        try:
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(synthesis)
            print(f"OK: {target_name}")
            processed += 1
        except Exception as e:
            print(f"ERROR writing {target_name}: {e}")

    print(f"\n处理完成: {processed} 成功, {skipped} 跳过")
    return processed, skipped

if __name__ == "__main__":
    # 处理全部241个文件
    start = 1
    end = 999  # 足够大，会自动过滤不存在的
    if len(sys.argv) > 1:
        start = int(sys.argv[1])
    if len(sys.argv) > 2:
        end = int(sys.argv[2])

    print(f"处理范围: 指导案例{start}号 - 指导案例{end}号")
    process_files(start, end)