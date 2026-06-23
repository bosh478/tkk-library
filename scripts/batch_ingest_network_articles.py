#!/usr/bin/env python3
"""批量处理 sources/网络文章/ 律师业务指引"""

import os
import re
import shutil
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
SOURCES_DIR = VAULT_ROOT / "sources/网络文章"
WIKI_SUMMARIES = VAULT_ROOT / "wiki/summaries"
LOG_FILE = VAULT_ROOT / "log.md"

def extract_date_from_filename(fname):
    """从文件名提取日期，如 20240327"""
    match = re.match(r'^(\d{8})_', fname)
    return match.group(1) if match else None

def extract_title_from_frontmatter(content):
    """从frontmatter提取title"""
    match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    return match.group(1) if match else None

def extract_category(content):
    """根据内容判断category"""
    content_lower = content.lower()
    if any(kw in content_lower for kw in ['劳动', '工伤', '工资', '社保', '劳动合同']):
        return '劳动与社会保障'
    elif any(kw in content_lower for kw in ['医疗', '医院', '医生', '纠纷']):
        return '医药健康'
    elif any(kw in content_lower for kw in ['刑事', '犯罪', '诈骗', '盗窃']):
        return '诉讼与仲裁'
    elif any(kw in content_lower for kw in ['商事', '公司', '投资', '股权']):
        return '公司商事与合规'
    elif any(kw in content_lower for kw in ['婚姻', '离婚', '继承', '家庭', '抚养']):
        return '婚姻家庭与继承'
    elif any(kw in content_lower for kw in ['建筑', '房地产', '工程', '物业']):
        return '建筑工程与房地产'
    elif any(kw in content_lower for kw in ['环境', '生态', '能源']):
        return '生态环境与能源'
    elif any(kw in content_lower for kw in ['知识产权', '专利', '商标', '版权']):
        return '知识产权'
    elif any(kw in content_lower for kw in ['金融', '银行', '证券', '保险']):
        return '金融与财税'
    elif any(kw in content_lower for kw in ['国际', '外贸', '海关', '出口']):
        return '国际贸易'
    else:
        return '诉讼与仲裁'

def process_file(src_path):
    """处理单个源文件，生成 wiki summary"""
    fname = src_path.name
    date_str = extract_date_from_filename(fname)
    if not date_str:
        print(f"  [SKIP] {fname} - 无法提取日期")
        return False

    # 读取源文件
    content = src_path.read_text(encoding='utf-8')

    # 提取title
    title = extract_title_from_frontmatter(content)
    if not title:
        # 从第一行markdown提取
        match = re.search(r'^##?\s*(.+?)(?:\s*[\n(]|$)', content, re.MULTILINE)
        if match:
            title = match.group(1).strip()

    if not title:
        title = fname.replace('.md', '')

    # 判断category
    category = extract_category(content)

    # 生成 wiki 文件名
    wiki_name = f"summary_{date_str}_{fname.replace('.md', '')}.md"
    wiki_path = WIKI_SUMMARIES / wiki_name

    # 避免重复
    if wiki_path.exists():
        print(f"  [SKIP] {wiki_name} - 已存在")
        return False

    # 提取正文前500字
    lines = content.split('\n')
    body_lines = []
    in_body = False
    for line in lines:
        if line.startswith('## ') and len(line) > 3:
            in_body = True
        if in_body and len(body_lines) < 30:
            body_lines.append(line)

    body_preview = '\n'.join(body_lines[:15])

    # 生成 frontmatter
    frontmatter = f"""---
title: "{title}"
type: summary
category: {category}
created: 2026-05-19
updated: 2026-05-19
tags: [律师业务指引]
source: "{fname}"
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{fname}]] |
| 类型 | 律师业务指引 |
| 发布日期 | {date_str[:4]}-{date_str[4:6]}-{date_str[6:8]} |
| 关键词 | {category} |
| 核心要点 | 详见正文 |

## 正文

{body_preview}

> 本文件由批量处理生成，来源：sources/网络文章/{fname}
"""

    wiki_path.write_text(frontmatter, encoding='utf-8')
    print(f"  [OK] {wiki_name}")
    return True

def main():
    print("=== 处理 sources/网络文章/ ===")

    # 读取待处理文件列表
    todo_file = Path("/tmp/to_process.txt")
    if todo_file.exists():
        with open(todo_file) as f:
            files = [line.strip() for line in f if line.strip()]
    else:
        # 手动获取所有文件
        files = list(SOURCES_DIR.glob("*.md"))
        files = [f for f in files if not (WIKI_SUMMARIES / f"summary_{f.name}").exists()]

    print(f"待处理文件数: {len(files)}")

    success = 0
    for i, f in enumerate(files[:20], 1):  # 先处理前20个
        src_path = Path(f) if isinstance(f, str) else f
        if process_file(src_path):
            success += 1

    print(f"\n完成: {success}/20")
    return success

if __name__ == "__main__":
    main()