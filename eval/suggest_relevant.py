#!/usr/bin/env python3
"""
suggest_relevant.py — query 相关知识缺口建议 (v6.2 修 #3)

问题: mcp-ttk-gap.suggest_new_topic 推全 vault 缺口 (与 query 无关)
修法: 拿全 vault 缺口 × query 相似度, 排序返回最相关

用法:
    python3 suggest_relevant.py --query "信访型寻衅滋事罪认定" --limit 5
    python3 suggest_relevant.py --query "受贿罪 不起诉" --limit 10
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

# v6.2 修 #5: 用 Path 自动定位
SCRIPT_DIR = Path(__file__).resolve().parent
KG_REPAIR = Path.home() / ".claude/skills/tkk-legal-ingest/tool/kg_integrity_repair.py"
RAG = "http://localhost:8081/v1"


def embed(text: str) -> list[float]:
    """用 tkk-rag 嵌入单条文本."""
    import requests
    resp = requests.post(
        f"{RAG}/embeddings",
        json={"model": "BAAI/bge-m3", "input": [text]},
        timeout=30,
    )
    resp.raise_for_status()
    return sorted(resp.json()["data"], key=lambda x: x["index"])[0]["embedding"]


def cosine(a: list[float], b: list[float]) -> float:
    """BGE-M3 输出已 normalize, 点积 = cosine."""
    return sum(x * y for x, y in zip(a, b))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True, help="用户 query")
    parser.add_argument("--limit", type=int, default=5, help="返回 Top N")
    parser.add_argument("--candidates", type=int, default=20, help="从 kg_integrity_repair 拿 N 候选")
    args = parser.parse_args()

    # 1. 拿候选缺口 (kg_integrity_repair --suggest N)
    #    ⚠️ kg_integrity_repair JSON 输出到 stderr (用 logger), stdout 是空
    result = subprocess.run(
        ["python3", str(KG_REPAIR), "--suggest", str(args.candidates)],
        capture_output=True, text=True, timeout=60,
    )
    # 优先从 stderr 读 JSON (logger 输出)
    text = result.stderr if result.stderr.strip() else result.stdout
    # 找最后完整 JSON 块 (从最后一个 { 到对应匹配 })
    depth = 0
    start = -1
    json_text = None
    for i, ch in enumerate(text):
        if ch == '{':
            if depth == 0:
                start = i
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0 and start >= 0:
                json_text = text[start:i+1]
                start = -1
    if not json_text:
        json_text = text.strip()
    try:
        candidates = json.loads(json_text).get("suggested_topics", []) if json_text else []
    except json.JSONDecodeError as e:
        print(f"⚠️  JSON parse 失败: {e}")
        print(f"  text 长度: {len(text)}, 前 200: {text[:200]}")
        return
    if not candidates:
        print("⚠️  kg_integrity_repair 无候选")
        return

    # 2. embed query + 每个 topic
    qvec = embed(args.query)
    import math
    scored = []
    for c in candidates:
        topic = c["topic"]
        try:
            tvec = embed(topic)
        except Exception:
            continue
        sim = cosine(qvec, tvec)
        # v6.2: 用 sim^2 × log(demand) 压制 demand 主导 (之前 demand × sim 让 Top 5 与 query 无关)
        combined = (sim ** 2) * math.log(c["demand"] + 1)
        scored.append({
            "topic": topic,
            "doc_type": c["doc_type_recommendation"],
            "demand": c["demand"],
            "similarity": round(sim, 3),
            "combined_score": round(combined, 3),
        })

    # 3. 按 combined_score 排序
    scored.sort(key=lambda x: x["combined_score"], reverse=True)
    top = scored[:args.limit]

    # 4. 输出
    print(f'=== Query 相关知识缺口 (Top {args.limit} of {len(candidates)}) ===\n')
    print(f"  query: '{args.query}'")
    print(f"  candidate pool: {len(candidates)} (from kg_integrity_repair --suggest {args.candidates})")
    print(f"  ranking: combined_score = similarity^2 × log(demand+1)  (v6.2 修 #3)")
    print(f"  → 相似度主导, demand 仅作补充权重\n")
    for i, t in enumerate(top, 1):
        bar = "█" * int(t["similarity"] * 20)
        print(f"  [{i}] {t['doc_type']:<22} demand={t['demand']:>4} sim={t['similarity']:.3f} combined={t['combined_score']:.3f} {bar}")
        print(f"      {t['topic']}")


if __name__ == "__main__":
    main()
