#!/usr/bin/env python3
"""检查某个知识点的 vault 覆盖度，输出覆盖度报告。

用法：
    python scripts/check_coverage.py --topic "受贿罪"
    python scripts/check_coverage.py --topic "受贿罪" --type crime
"""

import json
import os
import sys
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = VAULT_ROOT / "wiki"
TOPIC_INDEX = WIKI_DIR / "topics" / "topic_index.json"
CONCEPTS_DIR = WIKI_DIR / "concepts"

# 知识点类型到标准维度的映射
DIMENSIONS = {
    "crime": [
        ("构成要件", ["concept", "entity"], ["构成要件", "犯罪构成", "客体", "客观方面", "主体", "主观方面"]),
        ("量刑标准", ["entity", "synthesis"], ["量刑", "数额", "情节", "刑罚"]),
        ("司法解释", ["entity"], ["解释", "规定", "意见", "批复"]),
        ("典型案例", ["synthesis"], ["案例", "指导案例", "典型案例"]),
        ("与相关罪名区分", ["concept"], ["区分", "界限", "对比", "辨析"]),
        ("程序问题", ["concept", "summary"], ["管辖", "证据", "侦查", "程序"]),
        ("实务争议", ["synthesis", "summary"], ["争议", "难点", "实务", "认定"]),
    ],
    "system": [
        ("法律依据", ["entity"], ["法", "条例", "规定"]),
        ("适用条件", ["concept"], ["条件", "范围", "适用"]),
        ("程序流程", ["concept", "summary"], ["流程", "步骤", "程序"]),
        ("典型案例", ["synthesis"], ["案例"]),
        ("常见问题", ["summary", "synthesis"], ["问题", "难点", "实务"]),
    ],
    "procedure": [
        ("法律依据", ["entity"], ["法", "诉讼法", "规定"]),
        ("适用范围", ["concept"], ["范围", "条件", "适用"]),
        ("操作流程", ["concept", "summary"], ["流程", "步骤", "文书"]),
        ("救济途径", ["concept"], ["复议", "上诉", "申诉", "救济"]),
        ("实务要点", ["summary"], ["要点", "实务", "指引"]),
    ],
    "interpretation": [
        ("原文", ["entity"], ["解释", "规定"]),
        ("理解与适用", ["entity"], ["理解", "适用", "解读"]),
        ("实务影响", ["synthesis", "summary"], ["影响", "变化", "适用"]),
        ("与旧解释对比", ["entity", "synthesis"], ["旧解释", "替代", "修订"]),
    ],
}

# 简单关键词到类型的映射
TYPE_KEYWORDS = {
    "crime": ["罪", "犯", "刑罚"],
    "system": ["制度", "原则", "权利", "义务"],
    "procedure": ["程序", "诉讼", "管辖", "审判", "执行"],
    "interpretation": ["解释", "规定", "意见", "批复", "纪要"],
}


def detect_type(topic: str) -> str:
    """根据关键词自动检测知识点类型。"""
    for type_name, keywords in TYPE_KEYWORDS.items():
        for kw in keywords:
            if kw in topic:
                return type_name
    return "crime"  # 默认为罪名类型


def search_wiki(keyword: str, wiki_dir: Path) -> list[dict]:
    """在 wiki 中搜索包含关键词的页面。"""
    results = []
    for subdir in ["entities", "summaries", "syntheses", "concepts"]:
        dir_path = wiki_dir / subdir
        if not dir_path.exists():
            continue
        for f in dir_path.glob("*.md"):
            try:
                content = f.read_text(encoding='utf-8')
            except Exception:
                continue
            if keyword in content:
                rel = os.path.relpath(str(f), str(VAULT_ROOT))
                page_type = subdir.rstrip('s')  # entities -> entity
                results.append({"path": rel, "type": page_type, "name": f.stem})
    return results


def check_dimension(dimension: str, search_terms: list[str], wiki_dir: Path, topic_data: dict) -> dict:
    """检查单个维度的覆盖情况。"""
    found_pages = []
    source_count = 0

    # 在 wiki 中搜索
    for term in search_terms:
        pages = search_wiki(term, wiki_dir)
        found_pages.extend(pages)

    # 去重
    seen = set()
    unique_pages = []
    for p in found_pages:
        if p["path"] not in seen:
            seen.add(p["path"])
            unique_pages.append(p)

    # 检查 topic_index 中的源文件
    source_files = topic_data.get("source_files", [])
    for sf in source_files:
        for term in search_terms:
            if term in sf.get("path", ""):
                source_count += 1
                break

    # 判断覆盖状态
    if len(unique_pages) >= 2:
        status = "covered"
    elif len(unique_pages) == 1:
        status = "partial"
    else:
        status = "missing"

    return {
        "dimension": dimension,
        "status": status,
        "pages": unique_pages[:5],  # 最多显示 5 个
        "source_count": source_count,
    }


def generate_report(topic: str, topic_type: str, topic_data: dict) -> str:
    """生成覆盖度报告。"""
    dimensions = DIMENSIONS.get(topic_type, DIMENSIONS["crime"])
    results = []

    for dim_name, _, search_terms in dimensions:
        result = check_dimension(dim_name, search_terms, WIKI_DIR, topic_data)
        results.append(result)

    # 统计覆盖度
    covered = sum(1 for r in results if r["status"] == "covered")
    partial = sum(1 for r in results if r["status"] == "partial")
    total = len(results)

    # 生成报告
    lines = [
        f"## 📊 资料覆盖度报告\n",
        f"**知识点**：{topic}",
        f"**类型**：{topic_type}",
        f"**覆盖度**：{covered}/{total} 维度已覆盖（{partial} 个部分覆盖）\n",
        "| 维度 | 状态 | 已有资料 |",
        "|------|------|----------|",
    ]

    for r in results:
        if r["status"] == "covered":
            status = "✅ 已覆盖"
        elif r["status"] == "partial":
            status = "⚠️ 部分覆盖"
        else:
            status = "❌ 未覆盖"

        pages_str = ", ".join([f"[[{p['name']}]]" for p in r["pages"][:3]])
        if not pages_str:
            pages_str = "无"
        elif len(r["pages"]) > 3:
            pages_str += f" 等{len(r['pages'])}个"

        lines.append(f"| {r['dimension']} | {status} | {pages_str} |")

    # 建议补充
    missing_dims = [r for r in results if r["status"] != "covered"]
    if missing_dims:
        lines.append(f"\n**建议补充**：")
        for i, r in enumerate(missing_dims, 1):
            if r["status"] == "missing":
                lines.append(f"{i}. 补充「{r['dimension']}」相关资料 → 建议 ingest 相关文章/解释")
            else:
                lines.append(f"{i}. 完善「{r['dimension']}」→ 当前仅有部分覆盖，建议补充更多维度")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 3 or sys.argv[1] != "--topic":
        print("Usage: python scripts/check_coverage.py --topic <topic_name> [--type crime|system|procedure|interpretation]")
        sys.exit(1)

    topic = sys.argv[2]
    topic_type = None

    if len(sys.argv) > 4 and sys.argv[3] == "--type":
        topic_type = sys.argv[4]
        if topic_type not in DIMENSIONS:
            print(f"Error: --type must be one of: {', '.join(DIMENSIONS.keys())}")
            sys.exit(1)

    # 自动检测类型
    if not topic_type:
        topic_type = detect_type(topic)

    # 加载 topic_index
    if not TOPIC_INDEX.exists():
        print(f"Error: {TOPIC_INDEX} not found. Run build_topic_index.py first.")
        sys.exit(1)

    index = json.loads(TOPIC_INDEX.read_text(encoding='utf-8'))
    topics = index.get("topics", {})

    topic_data = topics.get(topic, {"source_files": [], "wiki_pages": []})

    # 生成报告
    report = generate_report(topic, topic_type, topic_data)

    # 输出到文件
    safe_name = topic.replace("/", "_").replace("\\", "_").replace("..", "")
    output_file = VAULT_ROOT / "wiki" / f"coverage_report_{safe_name}.md"
    output_file.write_text(report, encoding='utf-8')
    print(f"Coverage report generated: {output_file}")
    print(f"\n{report}")


if __name__ == "__main__":
    main()
