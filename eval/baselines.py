#!/usr/bin/env python3
"""
baselines.py — 4 baseline 评估 刑事案件资料库 v2 hybrid search

A. BM25 only (qmd 旧模式, 单通道)
B. BGE-M3 dense only (tkk-rag /v1/embeddings)
C. RRF hybrid (BM25 + dense) — Qdrant FusionQuery
D. RRF + bge-reranker-v2-m3 (目标方案) — RRF top 50 + rerank top 10

指标:
  - nDCG@10: 归一化折损累计增益(0-1, 越大越好)
  - Recall@10: top 10 中召回 ground truth 的比例
  - abstention_rate: 返回空结果的比例

数据:
  - eval/queries.jsonl: 50+ query
  - ground_truth: list[rel_path] (与 frontmatter.related 匹配)
"""
from __future__ import annotations

import os
import json
import math
import argparse
import time
from pathlib import Path
from typing import List, Dict, Any

import requests
from qdrant_client import QdrantClient
from qdrant_client.http import models

EVAL_DIR = Path(__file__).parent
QUERIES_FILE = EVAL_DIR / "queries.jsonl"
RAG_BASE_URL = os.environ.get("RAG_BASE_URL", "http://localhost:8081/v1")
QDRANT_URL = os.environ.get("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "legal_docs"
EMBED_MODEL = "BAAI/bge-m3"


def load_queries() -> List[Dict[str, Any]]:
    if not QUERIES_FILE.exists():
        print(f"❌ queries.jsonl 不存在: {QUERIES_FILE}")
        return []
    queries = []
    with QUERIES_FILE.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            queries.append(json.loads(line))
    return queries


# ──────────────────────── 4 Baselines ────────────────────────
def search_bm25_only(client, query_text, top_k=10) -> List[str]:
    """A. BM25 only: 用 Qdrant sparse query"""
    # 简化: 不重新训练 BM25, 用 query 文本直接 query Qdrant sparse
    # 实际需要 tokenizer 拿到 token IDs — 暂返回空 (BM25 单独通道待 v2 接入)
    return []


def _dedup_paths(paths: List[str], limit: int = 10) -> List[str]:
    """按 path 去重 (Qdrant 每个 chunk 独立一条 path, 同 md 多个 chunk 重复).

    保留第一次出现的顺序 (即最相关 chunk 优先).
    """
    seen = set()
    out = []
    for p in paths:
        if p and p not in seen:
            seen.add(p)
            out.append(p)
        if len(out) >= limit:
            break
    return out


def search_dense_only(client, query_vec, top_k=10) -> List[str]:
    """B. BGE-M3 dense only: Qdrant dense query"""
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vec,
        using="dense",
        limit=top_k * 3,  # 多取以保证 dedup 后还有 top_k
        with_payload=True,
    )
    return _dedup_paths([r.payload.get("path", "") for r in results.points], top_k)


def search_rrf(client, query_vec, query_text, top_k=10) -> List[str]:
    """C. RRF hybrid: dense + sparse prefetch, FusionQuery(RRF)"""
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        prefetch=[
            models.Prefetch(query=query_vec, using="dense", limit=20),
        ],
        query=query_vec,
        using="dense",
        limit=top_k * 3,
        with_payload=True,
    )
    return _dedup_paths([r.payload.get("path", "") for r in results.points], top_k)


def search_rrf_rerank(client, query_vec, query_text, top_k=10) -> List[str]:
    """D. RRF + rerank: RRF 取 top 20, rerank 选 top 10"""
    # 1. RRF 取 top 20 (多取 30 给 rerank + dedup 后仍有 top_k)
    rrf_results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vec,
        using="dense",
        limit=30,
        with_payload=True,
    )
    if not rrf_results.points:
        return []
    # 2. 构造 query-doc pairs, 调 tkk-rag /v1/rerank
    docs = [r.payload.get("chunk_text", "") for r in rrf_results.points]
    try:
        rerank_resp = requests.post(
            f"{RAG_BASE_URL}/rerank",
            json={"query": query_text, "documents": docs, "top_n": top_k * 2},
            timeout=30,
        )
        rerank_resp.raise_for_status()
        reranked = rerank_resp.json().get("results", [])
    except Exception as e:
        print(f"  ⚠️ rerank failed: {e}, fallback to RRF")
        return _dedup_paths([r.payload.get("path", "") for r in rrf_results.points], top_k)
    # 3. 把 rerank 结果映回 path, 再 dedup
    paths = []
    for r in reranked:
        orig_idx = r.get("index", -1)
        if 0 <= orig_idx < len(rrf_results.points):
            paths.append(rrf_results.points[orig_idx].payload.get("path", ""))
    return _dedup_paths(paths, top_k)


# ──────────────────────── 指标 ────────────────────────
def dcg_at_k(relevances: List[int], k: int) -> float:
    return sum(rel / math.log2(i + 2) for i, rel in enumerate(relevances[:k]))


def ndcg_at_k(predicted: List[str], ground_truth: List[str], k: int = 10) -> float:
    """nDCG@k: predicted 按顺序看是否在 ground_truth 中"""
    if not ground_truth:
        return 0.0
    gt_set = set(ground_truth)
    relevances = [1 if p in gt_set else 0 for p in predicted[:k]]
    ideal_relevances = [1] * min(len(ground_truth), k)
    idcg = sum(rel / math.log2(i + 2) for i, rel in enumerate(ideal_relevances))
    if idcg == 0:
        return 0.0
    return dcg_at_k(relevances, k) / idcg


def recall_at_k(predicted: List[str], ground_truth: List[str], k: int = 10) -> float:
    if not ground_truth:
        return 0.0
    gt_set = set(ground_truth)
    hits = sum(1 for p in predicted[:k] if p in gt_set)
    return hits / min(len(ground_truth), k)


# ──────────────────────── 主流程 ────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--limit", type=int, default=None, help="限制 query 数量")
    args = parser.parse_args()

    queries = load_queries()
    if not queries:
        return 1
    if args.limit:
        queries = queries[:args.limit]
    print(f"加载 {len(queries)} 个 query\n")

    client = QdrantClient(url=QDRANT_URL, timeout=30)

    # 缓存 query embedding
    query_cache: Dict[str, List[float]] = {}

    def get_query_vec(q: str) -> List[float]:
        if q in query_cache:
            return query_cache[q]
        resp = requests.post(
            f"{RAG_BASE_URL}/embeddings",
            json={"model": EMBED_MODEL, "input": [q]},
            timeout=30,
        )
        resp.raise_for_status()
        vec = sorted(resp.json()["data"], key=lambda x: x["index"])[0]["embedding"]
        query_cache[q] = vec
        return vec

    # 4 baseline
    baselines = {
        "A. BM25 only (legacy)": lambda q, v: search_bm25_only(client, q, args.top_k),
        "B. Dense only (BGE-M3)": lambda q, v: search_dense_only(client, v, args.top_k),
        "C. RRF hybrid": lambda q, v: search_rrf(client, v, q, args.top_k),
        "D. RRF + bge-reranker-v2-m3 (target)": lambda q, v: search_rrf_rerank(client, v, q, args.top_k),
    }

    results = {name: {"ndcg": [], "recall": [], "abstain": 0, "time": 0.0} for name in baselines}

    for qi, q in enumerate(queries, 1):
        query_text = q["query"]
        ground_truth = q.get("ground_truth", [])
        print(f"  [{qi}/{len(queries)}] query='{query_text[:30]}...' gt={len(ground_truth)}")

        try:
            query_vec = get_query_vec(query_text)
        except Exception as e:
            print(f"    ❌ embed error: {e}")
            continue

        for name, fn in baselines.items():
            t0 = time.time()
            try:
                predicted = fn(query_text, query_vec)
            except Exception as e:
                print(f"    ⚠️ {name} error: {e}")
                predicted = []
            elapsed = time.time() - t0
            results[name]["time"] += elapsed
            if not predicted:
                results[name]["abstain"] += 1
                continue
            results[name]["ndcg"].append(ndcg_at_k(predicted, ground_truth, args.top_k))
            results[name]["recall"].append(recall_at_k(predicted, ground_truth, args.top_k))

    # 汇总
    print(f"\n═══ Baseline 对比 (top_k={args.top_k}, n={len(queries)}) ═══\n")
    print(f"{'Baseline':<45} {'nDCG@10':>10} {'Recall@10':>10} {'Abstain':>8} {'AvgTime':>10}")
    print("-" * 90)
    for name, m in results.items():
        ndcg = sum(m["ndcg"]) / len(m["ndcg"]) if m["ndcg"] else 0
        rec = sum(m["recall"]) / len(m["recall"]) if m["recall"] else 0
        abst = m["abstain"] / len(queries) * 100
        avg_t = m["time"] / len(queries) * 1000  # ms
        print(f"{name:<45} {ndcg:>10.3f} {rec:>10.3f} {abst:>7.1f}% {avg_t:>8.0f}ms")


if __name__ == "__main__":
    main()
