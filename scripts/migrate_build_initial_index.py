#!/usr/bin/env python3
"""一次性迁移编排器：构建 topic_index + 生成 concept 聚合页 + 更新 index.md。

用法：
    python scripts/migrate_build_initial_index.py
"""

import json
import re
import subprocess
import sys
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = VAULT_ROOT / "scripts"


def run_script(name: str, args: list[str] | None = None):
    """运行指定脚本并检查返回码。"""
    script_path = SCRIPTS_DIR / name
    cmd = [sys.executable, str(script_path)] + (args or [])
    print(f"\n{'='*60}")
    print(f"Running: {name}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, cwd=str(VAULT_ROOT))
    if result.returncode != 0:
        print(f"ERROR: {name} failed with exit code {result.returncode}")
        sys.exit(1)


def update_index_md():
    """根据 topic_index.json 更新 wiki/index.md 中的 concept 索引。"""
    topic_index_path = VAULT_ROOT / "wiki" / "topics" / "topic_index.json"
    index_md = VAULT_ROOT / "wiki" / "index.md"

    if not topic_index_path.exists():
        print("topic_index.json not found, skipping index.md update")
        return

    index = json.loads(topic_index_path.read_text(encoding='utf-8'))
    topics = index.get("topics", {})

    # 按 source_count 排序，取 top 30 个主题
    sorted_topics = sorted(topics.items(), key=lambda x: -x[1]['source_count'])
    top_topics = sorted_topics[:30]

    # 生成 concept 索引块
    lines = [
        "\n## Concepts (概念聚合)\n",
        "> 自动生成自 topic_index.json，按关联源文件数排序\n",
        "| 主题 | 源文件数 | Wiki 页面数 | 聚合页 |",
        "|------|----------|-------------|--------|",
    ]

    for kw, data in top_topics:
        source_count = data['source_count']
        wiki_count = len(data.get('wiki_pages', []))
        concept_link = f"[[concept_{kw}]]"
        lines.append(f"| {kw} | {source_count} | {wiki_count} | {concept_link} |")

    if len(sorted_topics) > 30:
        lines.append(f"\n> 共 {len(sorted_topics)} 个主题已索引，完整列表见 [[wiki/topics/topic_index.json]]\n")

    concept_block = "\n".join(lines) + "\n"

    if index_md.exists():
        content = index_md.read_text(encoding='utf-8')
        # 检查是否已有 Concepts 块
        if "## Concepts" in content:
            # 替换现有块
            content = re.sub(
                r"## Concepts.*?(?=## |\Z)",
                concept_block.strip() + "\n",
                content,
                flags=re.DOTALL
            )
        else:
            # 在文件末尾追加
            content = content.rstrip() + "\n" + concept_block

        index_md.write_text(content, encoding='utf-8')
        print(f"Updated wiki/index.md with {len(top_topics)} concept entries")
    else:
        index_md.write_text(f"# Index\n\n{concept_block}", encoding='utf-8')
        print(f"Created wiki/index.md with {len(top_topics)} concept entries")


def main():
    print("V56 Migration: Building cross-file knowledge association layer")
    print(f"Vault root: {VAULT_ROOT}")

    # Step 1: 构建 topic_index.json
    run_script("build_topic_index.py")

    # Step 2: 生成 concept 聚合页
    run_script("build_concept_pages.py")

    # Step 3: 更新 index.md
    print(f"\n{'='*60}")
    print("Updating wiki/index.md")
    print(f"{'='*60}")
    update_index_md()

    print(f"\n{'='*60}")
    print("Migration complete!")
    print(f"{'='*60}")
    print(f"  - wiki/topics/topic_index.json: keyword -> source files mapping")
    print(f"  - wiki/concepts/concept_*.md: human-readable aggregation pages")
    print(f"  - wiki/index.md: updated with concept index")


if __name__ == "__main__":
    main()
