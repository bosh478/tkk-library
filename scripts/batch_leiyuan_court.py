#!/usr/bin/env python3
"""
Batch ingest: 上海一中法院类案裁判方法 (93 files) - FIXED
处理 sources/微信公号资料/上海一中法院/上海一中法院-类案裁判方法-md/
输出到 wiki/summaries/
"""

import os
import re
from pathlib import Path

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
SOURCE_DIR = VAULT_ROOT / "sources/微信公号资料/上海一中法院/上海一中法院-类案裁判方法-md"
TARGET_DIR = VAULT_ROOT / "wiki/summaries"
TARGET_DIR.mkdir(parents=True, exist_ok=True)

def extract_title(content):
    """从第一行提取标题 - 修复版，处理两种格式"""
    lines = content.split('\n')
    for line in lines:
        if line.startswith('#'):
            # 格式A: #  类案裁判方法 | 实际标题
            # 格式B: #  实际标题 | 类案裁判方法
            if '|' in line:
                parts = line.split('|')
                if len(parts) >= 2:
                    # 检查哪个部分包含"类案裁判方法"
                    part1 = parts[0].replace('#', '').strip()
                    part2 = parts[1].strip()

                    if '类案裁判方法' in part1:
                        # 格式A: title 在第二部分
                        title = part2
                    elif '类案裁判方法' in part2:
                        # 格式B: title 在第一部分
                        title = part1
                    else:
                        # 默认用第二部分
                        title = part2

                    # 清理标题
                    title = re.sub(r'^\[\d{4}-\d{2}-\d{2}]\s*', '', title)
                    return title.strip()
    return None

def clean_title(title):
    """去除日期前缀 [YYYY-MM-DD]"""
    return re.sub(r'^\[\d{4}-\d{2}-\d{2}]\s*', '', title)

def extract_case_type(content):
    """提取案件类型/案由"""
    patterns = [
        r'(行政|民事|刑事|商事)?(纠纷|案件|诉讼)',
        r'(政府信息公开|劳动争议|合同纠纷|继承纠纷)',
        r'(确认|撤销|变更|损害赔偿)'
    ]
    for pattern in patterns:
        match = re.search(pattern, content[:1000])
        if match:
            return match.group(0)
    return "类案裁判方法"

def process_file(src_path):
    """处理单个文件，返回目标文件内容"""
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()

    title = extract_title(content)
    if not title:
        title = src_path.stem
    title = clean_title(title)

    # 生成目标文件名
    safe_title = re.sub(r'[\\/:*?"<>|]', '', title)[:50]
    target_name = f"summary_Court_上海一中院_类案裁判_{safe_title}.md"
    target_path = TARGET_DIR / target_name

    # 如果已存在则跳过
    if target_path.exists():
        return target_path, "SKIP"

    # 提取案件类型
    case_type = extract_case_type(content)

    # 生成 frontmatter
    src_relative = str(src_path.relative_to(VAULT_ROOT)).replace('\\', '/')

    frontmatter = f'''---
title: {title}
type: summary
category: 诉讼与仲裁
created: 2026-05-11
updated: 2026-05-11
tags: [类案裁判方法, 上海一中院, {case_type}]
source: "{src_relative}"
related: []
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{src_path.name}]] |
| 类型 | 类案裁判方法 |
| 发布机构 | 上海一中法院 |
| 核心领域 | {case_type} |

'''

    # 提取正文内容 - 收集各级标题和关键内容
    sections = []
    current_section = []
    in_body = False
    body_start = False

    for line in content.split('\n'):
        # 跳过编者按和元数据部分
        if line.startswith('**编者按'):
            continue
        if '上海一中院探索类案裁判方法总结工作机制' in line:
            body_start = True
            continue
        if not body_start:
            continue

        # 跳过作者信息和目录
        if line.strip() in ['周清', 'ZHOU QING', '商事审判庭', '三级高级法官',
                           '闫伟伟', 'YAN WEIWEI', '一级法官助理',
                           '买卖合同', '目录', '01', '02', '03']:
            continue

        if re.match(r'^#{1,3}\s*[一-龥]', line) and not re.match(r'^#{1,3}\s*\*', line):
            # 新的标题段落
            if current_section:
                sections.append('\n'.join(current_section))
            current_section = []
        elif line.startswith('**一') or line.startswith('**二') or line.startswith('**三') or line.startswith('**四') or line.startswith('**（'):
            if current_section:
                sections.append('\n'.join(current_section))
            current_section = [line.replace('**', '').strip()]
        elif line.strip():
            current_section.append(line.strip())

    if current_section:
        sections.append('\n'.join(current_section))

    # 构建正文 - 过滤空白内容
    valid_sections = []
    for s in sections:
        if s and len(s) > 10:
            valid_sections.append(s)

    body = '\n\n'.join(valid_sections[:25])

    wiki_content = frontmatter + "\n" + body[:12000]

    return target_path, wiki_content

def main():
    source_files = list(SOURCE_DIR.glob("*.md"))
    print(f"Found {len(source_files)} source files")

    results = {"success": 0, "skip": 0, "error": 0, "errors": []}

    for src_path in source_files:
        try:
            result = process_file(src_path)
            if result[1] == "SKIP":
                results["skip"] += 1
                continue

            target_path, content = result
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content)
            results["success"] += 1
        except Exception as e:
            results["error"] += 1
            results["errors"].append(f"{src_path.name}: {str(e)}")

    print(f"Results: {results['success']} created, {results['skip']} skipped, {results['error']} errors")
    if results["errors"]:
        print("Errors:")
        for e in results["errors"][:5]:
            print(f"  {e}")

if __name__ == "__main__":
    main()
