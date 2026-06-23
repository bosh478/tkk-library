#!/usr/bin/env python3
"""根据 topic_index.json 生成 concept 聚合页到 wiki/concepts/。

用法：
    python scripts/build_concept_pages.py
    python scripts/build_concept_pages.py --topic "受贿罪"
"""

import json
import os
import sys
from datetime import date
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = VAULT_ROOT / "wiki"
TOPIC_INDEX = WIKI_DIR / "topics" / "topic_index.json"
CONCEPTS_DIR = WIKI_DIR / "concepts"

# 目录分类映射（用于分组显示）
DIR_CATEGORIES = {
    "0-现行规范库": "法律法规/司法解释",
    "2-案例库": "案例",
    "微信公号资料": "检察/法院资讯",
    "业务指引": "律师业务指引",
    "书籍资料": "学术著作",
    "司法观点、案例": "司法观点",
    "《统编教材》法官审判实务": "法官培训教材",
    "《刑事审判参考》": "刑事审判参考",
    "《民法典适用大全》": "民法典适用",
    "《理解与适用》": "理解与适用",
    "证据质证": "证据质证",
    "网络文章": "网络文章",
    "纪委监委案件": "纪检监察",
    "讲座、论文等": "学术讲座/论文",
}

# 相关概念预定义（罪名之间的关联）
RELATED_CONCEPTS = {
    "受贿罪": ["贪污罪", "行贿罪", "利用影响力受贿罪", "挪用公款罪"],
    "贪污罪": ["受贿罪", "挪用公款罪", "私分国有资产罪"],
    "行贿罪": ["受贿罪", "对有影响力的人行贿罪"],
    "盗窃罪": ["抢劫罪", "抢夺罪", "诈骗罪", "职务侵占罪"],
    "诈骗罪": ["盗窃罪", "合同诈骗罪", "集资诈骗罪", "信用卡诈骗罪"],
    "故意伤害罪": ["故意杀人罪", "寻衅滋事罪", "聚众斗殴罪"],
    "交通肇事罪": ["危险驾驶罪", "重大责任事故罪"],
    "非法吸收公众存款罪": ["集资诈骗罪", "诈骗罪"],
    "侵犯公民个人信息罪": ["帮助信息网络犯罪活动罪"],
    "掩饰隐瞒犯罪所得罪": ["盗窃罪", "诈骗罪"],
    "合同诈骗罪": ["诈骗罪", "非法经营罪"],
    "侵犯著作权罪": ["假冒注册商标罪", "侵犯商业秘密罪"],
    "污染环境罪": ["非法采矿罪"],
}


def classify_source(path: str) -> str:
    """根据路径判断源文件分类。"""
    for dir_key, category in DIR_CATEGORIES.items():
        if dir_key in path:
            return category
    return "其他"


def generate_concept_page(topic: str, data: dict) -> str:
    """生成单个 concept 聚合页的 Markdown 内容。"""
    today = str(date.today())
    source_files = data.get("source_files", [])
    wiki_pages = data.get("wiki_pages", [])

    # 按分类分组
    grouped = {}
    for sf in source_files:
        cat = classify_source(sf["path"])
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(sf)

    # 构建 related 链接
    related_lines = []
    # 关联已有的 wiki 页面
    for wp in wiki_pages[:10]:
        wp_name = Path(wp).stem
        related_lines.append(f"  - [[{wp_name}]]")
    # 关联相关概念
    for rc in RELATED_CONCEPTS.get(topic, []):
        related_lines.append(f"  - [[concept_{rc}]]")

    related_yaml = "\n".join(related_lines) if related_lines else "  []"

    # 生成正文
    sections = []
    sections.append(f"## 相关资料总览\n")
    sections.append(f"> 本页聚合了 vault 中所有讨论「{topic}」的资料，共涉及 **{len(source_files)}** 个源文件。\n")

    for cat, files in sorted(grouped.items(), key=lambda x: -len(x[1])):
        sections.append(f"### {cat}（{len(files)} 个）\n")
        sections.append("| 源文件 | 路径 |")
        sections.append("|--------|------|")
        for f in files[:15]:  # 最多显示 15 个
            fname = Path(f["path"]).name
            sections.append(f"| {fname} | `{f['path']}` |")
        if len(files) > 15:
            sections.append(f"| ... | 共 {len(files)} 个，完整列表见 topic_index.json |")
        sections.append("")

    if wiki_pages:
        sections.append("## 相关 Wiki 页面\n")
        for wp in wiki_pages[:10]:
            wp_name = Path(wp).stem
            sections.append(f"- [[{wp_name}]]")
        sections.append("")

    # 组装完整页面
    page = f"""---
title: {topic}
type: concept
created: {today}
updated: {today}
tags: [{topic}, 知识聚合]
source: "不存在"
related:
{related_yaml}
---

## 概念定义

> {topic}相关知识聚合页。本页汇总 vault 中所有涉及该主题的源文件和 wiki 页面。

""" + "\n".join(sections)

    return page


def main():
    if not TOPIC_INDEX.exists():
        print(f"Error: {TOPIC_INDEX} not found. Run build_topic_index.py first.")
        sys.exit(1)

    index = json.loads(TOPIC_INDEX.read_text(encoding='utf-8'))
    topics = index.get("topics", {})

    # 确保输出目录存在
    CONCEPTS_DIR.mkdir(parents=True, exist_ok=True)

    # 可选：只生成指定 topic
    target_topic = None
    if len(sys.argv) > 1 and sys.argv[1] == "--topic":
        target_topic = sys.argv[2]

    count = 0
    for topic, data in topics.items():
        if target_topic and topic != target_topic:
            continue
        # 只为有 3+ 个源文件的主题生成聚合页
        if data.get("source_count", 0) < 3:
            continue

        page_content = generate_concept_page(topic, data)
        filename = f"concept_{topic}.md"
        filepath = CONCEPTS_DIR / filename
        filepath.write_text(page_content, encoding='utf-8')
        count += 1

    print(f"Generated {count} concept pages in {CONCEPTS_DIR}")


if __name__ == "__main__":
    main()
