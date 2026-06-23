#!/usr/bin/env python3
"""批量处理律师业务指引 - sources/网络文章/"""

import os
import re
from pathlib import Path
import tempfile

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
TEMP_DIR = Path(tempfile.gettempdir())

CATEGORIES = {
    '劳动': '劳动与社会保障',
    '工伤': '劳动与社会保障',
    '工资': '劳动与社会保障',
    '社保': '劳动与社会保障',
    '劳动合同': '劳动与社会保障',
    '集体协商': '劳动与社会保障',
    '人事争议': '劳动与社会保障',
    '医疗': '医药健康',
    '医院': '医药健康',
    '医药': '医药健康',
    '健康': '医药健康',
    '刑事': '诉讼与仲裁',
    '犯罪': '诉讼与仲裁',
    '诈骗': '诉讼与仲裁',
    '风险防范': '诉讼与仲裁',
    '商事': '公司商事与合规',
    '公司': '公司商事与合规',
    '投资': '公司商事与合规',
    '股权': '公司商事与合规',
    '企业': '公司商事与合规',
    '担保': '公司商事与合规',
    '股东': '公司商事与合规',
    '婚姻': '婚姻家庭与继承',
    '离婚': '婚姻家庭与继承',
    '继承': '婚姻家庭与继承',
    '家庭': '婚姻家庭与继承',
    '抚养': '婚姻家庭与继承',
    '遗嘱': '婚姻家庭与继承',
    '家事': '婚姻家庭与继承',
    '建筑': '建筑工程与房地产',
    '房地产': '建筑工程与房地产',
    '物业': '建筑工程与房地产',
    '工程': '建筑工程与房地产',
    '仓储': '建筑工程与房地产',
    '物流': '建筑工程与房地产',
    '环境': '生态环境与能源',
    '生态': '生态环境与能源',
    '能源': '生态环境与能源',
    '知识产权': '知识产权',
    '专利': '知识产权',
    '商标': '知识产权',
    '版权': '知识产权',
    '金融': '金融与财税',
    '银行': '金融与财税',
    '证券': '金融与财税',
    '保险': '金融与财税',
    '消费': '金融与财税',
    '仲裁': '诉讼与仲裁',
    '调解': '诉讼与仲裁',
    '国际': '国际贸易',
    '外贸': '国际贸易',
    '出口': '国际贸易',
    '涉外': '国际贸易',
    '政府信息': '政府与公共法律服务',
    '行政处罚': '政府与公共法律服务',
    '交通': '诉讼与仲裁',
    '侵权': '诉讼与仲裁',
    '信托': '金融与财税',
    '科技成果': '知识产权',
}

def get_category(title):
    for kw, cat in CATEGORIES.items():
        if kw in title:
            return cat
    return '诉讼与仲裁'

def extract_date(fname):
    m = re.match(r'^(\d{8})_', fname)
    return m.group(1) if m else None

def process_lawyer_guide(src_path):
    fname = src_path.name

    # 检查是否已处理
    base_name = fname.replace('.md', '')

    # 读取内容
    try:
        content = src_path.read_text(encoding='utf-8')
    except Exception as e:
        return f"FAIL|{fname}|read error: {e}"

    # 提取 title
    title = None
    if m := re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE):
        title = m.group(1)
    if not title:
        if m := re.search(r'^##?\s*(.+?)(?:\s*[\n(]|$)', content, re.MULTILINE):
            title = m.group(1).strip()
    if not title:
        title = fname.replace('.md', '')

    date_str = extract_date(fname)
    if not date_str:
        return f"SKIP|{fname}|no date"

    # 判断分类
    category = get_category(title)

    # 生成 wiki 文件名：summary_YYYYMMDD_原文件名（去掉8位日期前缀）
    wiki_name = f"summary_{date_str}_{fname[9:]}"
    wiki_path = WIKI_SUMMARIES / wiki_name

    if wiki_path.exists():
        return f"SKIP|{fname}|{wiki_name} exists"

    # 提取正文前500字
    lines = content.split('\n')
    body_lines = []
    count = 0
    for line in lines:
        if line.startswith('## ') and count > 0:
            break
        if line.strip():
            body_lines.append(line)
            count += 1
        if count >= 20:
            break

    body_preview = '\n'.join(body_lines[:15])

    formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"

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
| 发布日期 | {formatted_date} |
| 关键词 | {category} |
| 核心要点 | 详见正文 |

## 正文

{body_preview}

> 本文件由批量处理生成，来源：sources/网络文章/{fname}
"""

    try:
        wiki_path.write_text(frontmatter, encoding='utf-8')
        return f"OK|{fname}|{wiki_name}"
    except Exception as e:
        return f"FAIL|{fname}|write error: {e}"

def main():
    print("=== 批量处理律师业务指引 ===\n")

    lawyer_guides_path = TEMP_DIR / "lawyer_guides.txt"
    if not lawyer_guides_path.exists():
        print(f"错误: {lawyer_guides_path} 不存在")
        return 0

    with open(lawyer_guides_path, encoding='utf-8') as f:
        files = [line.strip() for line in f if line.strip()]

    print(f"待处理文件数: {len(files)}\n")

    results = {"OK": [], "SKIP": [], "FAIL": []}

    for i, f in enumerate(files, 1):
        src_path = VAULT_ROOT / f
        if not src_path.exists():
            results["FAIL"].append(f"NOT_FOUND|{f}")
            continue

        res = process_lawyer_guide(src_path)
        status = res.split("|")[0]
        results[status].append(res)

        if i % 10 == 0:
            print(f"进度: {i}/{len(files)}")

    print(f"\n=== 处理结果 ===")
    print(f"成功: {len(results['OK'])}")
    print(f"跳过: {len(results['SKIP'])}")
    print(f"失败: {len(results['FAIL'])}")

    if results['OK']:
        print("\n成功列表:")
        for r in results['OK'][:10]:
            parts = r.split("|")
            print(f"  {parts[1]} -> {parts[2]}")
        if len(results['OK']) > 10:
            print(f"  ... 还有 {len(results['OK']) - 10} 个")

    if results['FAIL']:
        print("\n失败列表:")
        for r in results['FAIL']:
            print(f"  {r}")

    return len(results['OK'])

if __name__ == "__main__":
    main()