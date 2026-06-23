#!/usr/bin/env python3
"""
sync_index.py — 自动同步 wiki/index.md

扫描 wiki/ 下所有 .md 文件，读取 frontmatter，按类型分组生成索引。
支持 --apply 模式自动写入，或默认只输出差异。

用法:
    python scripts/sync_index.py              # 预览差异
    python scripts/sync_index.py --apply      # 写入 index.md
    python scripts/sync_index.py --dry-run    # 同上（预览）
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

VAULT_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = VAULT_ROOT / "wiki"
INDEX_PATH = WIKI_DIR / "index.md"

# wiki 子目录 → type 映射
DIR_TYPE_MAP = {
    "concepts": "concept",
    "entities": "entity",
    "syntheses": "synthesis",
    "summaries": "summary",
}


def parse_frontmatter(content: str) -> dict:
    """解析 YAML frontmatter（简化版，不依赖 PyYAML）"""
    fm = {}
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return fm
    for line in match.group(1).split('\n'):
        line = line.strip()
        if ':' in line:
            key, _, val = line.partition(':')
            key = key.strip()
            val = val.strip()
            # 去掉列表格式 [a, b] → 取第一个
            if val.startswith('[') and val.endswith(']'):
                val = val[1:-1].split(',')[0].strip()
            # 去掉 [[ ]]
            val = re.sub(r'\[\[|\]\]', '', val)
            fm[key] = val
    return fm


def scan_wiki() -> dict:
    """扫描 wiki 目录，返回按 type 分组的文件信息"""
    files_by_type = defaultdict(list)

    for subdir_name, expected_type in DIR_TYPE_MAP.items():
        subdir = WIKI_DIR / subdir_name
        if not subdir.exists():
            continue
        for f in sorted(subdir.glob("*.md")):
            content = f.read_text(encoding='utf-8', errors='replace')
            fm = parse_frontmatter(content)
            file_type = fm.get("type", expected_type)
            title = fm.get("title", f.stem)
            created = fm.get("created", "")
            category = fm.get("category", "")
            tags = fm.get("tags", "")
            source = fm.get("source", "")

            # 生成摘要（取正文前80字符，去掉 markdown 标记）
            body_start = content.find('---', content.find('---') + 3)
            if body_start > 0:
                body = content[body_start+3:].strip()
                body = re.sub(r'^#+\s+.*$', '', body, flags=re.MULTILINE).strip()
                body = re.sub(r'\[.*?\]\(.*?\)', '', body).strip()
                body = re.sub(r'\[\[.*?\]\]', '', body).strip()
                summary = body[:80].replace('\n', ' ').strip()
                if len(body) > 80:
                    summary += "..."
            else:
                summary = ""

            files_by_type[file_type].append({
                "path": f,
                "stem": f.stem,
                "title": title,
                "created": created,
                "category": category,
                "tags": tags,
                "source": source,
                "summary": summary,
            })

    return files_by_type


def generate_index(files_by_type: dict) -> str:
    """生成 index.md 内容"""
    lines = []
    lines.append("# Wiki Index")
    lines.append("")
    lines.append("> 本文件由 sync_index.py 自动生成。")
    lines.append("")
    lines.append("---")
    lines.append("")

    # --- Concepts ---
    concepts = files_by_type.get("concept", [])
    lines.append("## Concepts（概念页）")
    lines.append("")
    if concepts:
        lines.append("| 页面 | 摘要 | 更新日期 |")
        lines.append("|------|------|----------|")
        for f in sorted(concepts, key=lambda x: x["created"], reverse=True):
            lines.append(f"| [[{f['stem']}]] | {f['summary']} | {f['created']} |")
    else:
        lines.append("*暂无*")
    lines.append("")

    # --- Entities ---
    entities = files_by_type.get("entity", [])
    lines.append("---")
    lines.append("")
    lines.append("## Entities（实体页）")
    lines.append("")
    if entities:
        lines.append("| 页面 | 摘要 | 日期 |")
        lines.append("|------|------|------|")
        for f in sorted(entities, key=lambda x: x["created"], reverse=True):
            lines.append(f"| [[{f['stem']}]] | {f['summary']} | {f['created']} |")
    else:
        lines.append("*暂无*")
    lines.append("")

    # --- Syntheses ---
    syntheses = files_by_type.get("synthesis", [])
    lines.append("---")
    lines.append("")
    lines.append("## Syntheses（综合分析）")
    lines.append("")
    if syntheses:
        lines.append("| 页面 | 摘要 | 日期 |")
        lines.append("|------|------|------|")
        for f in sorted(syntheses, key=lambda x: x["created"], reverse=True):
            lines.append(f"| [[{f['stem']}]] | {f['summary']} | {f['created']} |")
    else:
        lines.append("*暂无*")
    lines.append("")

    # --- Summaries (by category) ---
    summaries = files_by_type.get("summary", [])
    lines.append("---")
    lines.append("")
    lines.append("## Summaries（来源摘要）")
    lines.append("")
    if summaries:
        # 按 category 分组
        by_category = defaultdict(list)
        for f in summaries:
            cat = f["category"] or "未分类"
            by_category[cat].append(f)

        for cat in sorted(by_category.keys()):
            cat_files = by_category[cat]
            lines.append(f"### {cat}（{len(cat_files)}条）")
            lines.append("| 页面 | 摘要 | 日期 |")
            lines.append("|------|------|------|")
            for f in sorted(cat_files, key=lambda x: x["created"], reverse=True):
                lines.append(f"| [[{f['stem']}]] | {f['summary']} | {f['created']} |")
            lines.append("")
    else:
        lines.append("*暂无*")
    lines.append("")

    # --- Statistics ---
    lines.append("---")
    lines.append("")
    lines.append("## 统计")
    lines.append("")
    lines.append("| 类型 | 数量 |")
    lines.append("|------|------|")
    lines.append(f"| Concepts（概念页） | {len(concepts)} |")
    lines.append(f"| Entities（实体页） | {len(entities)} |")
    lines.append(f"| Syntheses（综合分析） | {len(syntheses)} |")
    lines.append(f"| Summaries（来源摘要） | {len(summaries)} |")
    lines.append(f"| **总计** | **{len(concepts)+len(entities)+len(syntheses)+len(summaries)}** |")
    lines.append("")
    lines.append(f"> 统计数据截至 {datetime.now().strftime('%Y-%m-%d')}。由 sync_index.py 自动生成。")

    return "\n".join(lines) + "\n"


def diff_index(new_content: str) -> str:
    """对比新旧 index.md，输出差异"""
    if not INDEX_PATH.exists():
        return "index.md 不存在，将新建"

    old_content = INDEX_PATH.read_text(encoding='utf-8')

    # 简单对比：逐行
    old_lines = old_content.splitlines()
    new_lines = new_content.splitlines()

    added = len(new_lines) - len(old_lines)
    if added == 0 and old_content == new_content:
        return "无差异"

    diff_summary = []
    if added > 0:
        diff_summary.append(f"新增 {added} 行")
    elif added < 0:
        diff_summary.append(f"减少 {abs(added)} 行")

    # 统计数量变化
    old_stats = re.findall(r'\| (\w+)（.*?） \| (\d+) \|', old_content)
    new_stats = re.findall(r'\| (\w+)（.*?） \| (\d+) \|', new_content)
    old_dict = {k: int(v) for k, v in old_stats}
    new_dict = {k: int(v) for k, v in new_stats}

    for key in new_dict:
        old_val = old_dict.get(key, 0)
        new_val = new_dict[key]
        if old_val != new_val:
            diff_summary.append(f"  {key}: {old_val} → {new_val}")

    return "\n".join(diff_summary) if diff_summary else "内容已更新"


def main():
    apply_mode = "--apply" in sys.argv

    print("扫描 wiki 目录...")
    files_by_type = scan_wiki()

    total = sum(len(v) for v in files_by_type.values())
    print(f"发现 {total} 个 wiki 文件：")
    for t, files in sorted(files_by_type.items()):
        print(f"  {t}: {len(files)}")

    new_index = generate_index(files_by_type)

    if apply_mode:
        INDEX_PATH.write_text(new_index, encoding='utf-8')
        print(f"\n✅ 已写入 {INDEX_PATH}")
    else:
        print(f"\n--- 预览差异 ---")
        diff = diff_index(new_index)
        print(diff)
        print(f"\n使用 --apply 写入 index.md")


if __name__ == "__main__":
    main()
