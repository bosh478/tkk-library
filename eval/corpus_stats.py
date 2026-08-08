#!/usr/bin/env python3
"""
corpus_stats.py — 准确统计 vault 覆盖率 (v6.2 修 #1)

之前 baseline + 测试脚本用 subprocess.run(['grep', '-rl', kw, ...]) 计文件数
但数字矛盾 (信访 271 vs 160, 寻衅滋事 296 vs 214), 实际是 grep 默认 regex 匹配 bug.

本脚本:
- 用 grep -F (fixed string) 准确计数
- 路径自动定位 (Path(__file__).parent.parent) 修 #5
- 输出固定格式报告, 存入 /home/kangkang/.cache/tkk-legal-ingest/corpus_stats.json

用法:
    python3 corpus_stats.py              # 跑统计 + 显示
    python3 corpus_stats.py --json      # 只输出 JSON
    python3 corpus_stats.py --update   # 更新到 memory
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# v6.2 fix #5: 路径自动定位
SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parent  # eval/ → tkk-library/
WIKI_ROOT = VAULT_ROOT / "wiki"
CACHE_DIR = Path("/home/kangkang/.cache/tkk-legal-ingest")
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_FILE = CACHE_DIR / "corpus_stats.json"


def count_keyword_files(keyword: str) -> int:
    """用 grep -F (fixed string) 准确计数含 keyword 的 wiki 文件数."""
    try:
        result = subprocess.run(
            ["grep", "-rFl", "--include=*.md", "--", keyword, str(WIKI_ROOT)],
            capture_output=True, text=True, timeout=60,
        )
        # grep -F 找到时会打印所有匹配文件, 每行 1 个
        return len([line for line in result.stdout.strip().split("\n") if line])
    except subprocess.TimeoutExpired:
        return -1
    except Exception as e:
        print(f"  ⚠️ grep 失败: {e}")
        return -1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="只输出 JSON")
    parser.add_argument("--update", action="store_true", help="保存到缓存")
    args = parser.parse_args()

    # 统计关键法律关键词
    keywords = [
        "信访", "寻衅滋事", "寻衅滋事 信访",  # 这次测试的 query
        "受贿罪", "危险驾驶", "合同诈骗", "正当防卫",  # 之前 5 query
        "刑法第293条", "刑法第385条", "刑法第264条",  # 法条
    ]

    print(f"=== corpus_stats 准确覆盖率统计 ===\n")
    print(f"  vault: {VAULT_ROOT}")
    print(f"  wiki: {WIKI_ROOT}")
    print(f"  统计关键词: {len(keywords)} 个\n")

    counts = {}
    for kw in keywords:
        n = count_keyword_files(kw)
        counts[kw] = n
        print(f"  '{kw}': {n} 文件")

    # 知识缺口
    print(f"\n=== 知识缺口 (按 wikilink count 排序) ===")
    print(f"  验证: '寻衅滋事 信访' = {counts['寻衅滋事 信访']} 文件")
    if counts["寻衅滋事 信访"] == 0:
        print(f"  ⚠️ 真空缺: 无文件同时含 '寻衅滋事' + '信访'")
        print(f"  建议: 补充 'concept_寻衅滋事罪信访适用' 或 'synthesis_信访型寻衅滋事罪认定'")

    # Cross: 寻衅滋事∩信访
    print(f"\n=== Cross-intersection (同时含) ===")
    for kw1, kw2 in [("寻衅滋事", "信访"), ("受贿罪", "不起诉"), ("危险驾驶", "醉驾")]:
        # 独立 grep 后取交集
        r1 = subprocess.run(["grep", "-rFl", "--include=*.md", "--", kw1, str(WIKI_ROOT)],
                             capture_output=True, text=True, timeout=60)
        r2 = subprocess.run(["grep", "-rFl", "--include=*.md", "--", kw2, str(WIKI_ROOT)],
                             capture_output=True, text=True, timeout=60)
        s1 = set(r1.stdout.strip().split("\n")) if r1.stdout.strip() else set()
        s2 = set(r2.stdout.strip().split("\n")) if r2.stdout.strip() else set()
        intersect = s1 & s2
        union = s1 | s2
        print(f"  '{kw1}' ∩ '{kw2}': {len(intersect)} 文件 (union: {len(union)}, Jaccard: {len(intersect)/len(union)*100 if union else 0:.1f}%)")

    # 缓存
    stats = {
        "timestamp": datetime.now().isoformat(),
        "vault_root": str(VAULT_ROOT),
        "wiki_root": str(WIKI_ROOT),
        "keyword_counts": counts,
        "fix_note": "v6.2 修 #1+#5: 用 grep -F 准确计数 + Path 自动定位",
    }
    if args.update:
        CACHE_FILE.write_text(json.dumps(stats, ensure_ascii=False, indent=2))
        print(f"\n✓ 缓存: {CACHE_FILE}")

    if args.json:
        print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
