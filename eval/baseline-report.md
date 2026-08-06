# v3.3 Baseline 报告 (2026-08-06)

## 数据基础
- **Qdrant points**: 80,858 (v3.1 全量 ingest, 从 33,337 增长 142%)
- **vault md**: 14,860 (wiki 4 子目录)
- **queries.jsonl**: 151 query (v3.3 扩展 50→151, 8 种 doc_type 分布)
- **Top-K**: 10
- **Rerank**: bge-reranker-v2-m3 (本地端口 8081)

## 4 baseline 对比

| Baseline | nDCG@10 | Recall@10 | Abstain | AvgTime |
|---|---|---|---|---|
| A. BM25 only (legacy placeholder) | 0.000 | 0.000 | 100.0% | 0ms |
| B. Dense only (BGE-M3) | 0.704 | 0.869 | 0.0% | 22ms |
| C. RRF hybrid | 0.704 | 0.869 | 0.0% | 17ms |
| **D. RRF + bge-reranker-v2-m3 (target)** | **0.756** | **0.885** | 0.0% | 4046ms |

## vs P1.4 baseline (50 query, 33k points)

| Baseline | P1.4 (50q) | v3.3 (151q) | Δ |
|---|---|---|---|
| D target nDCG | 0.546 | 0.756 | **+38.5%** |
| D target Recall | 0.867 | 0.885 | +2.1% |

**结论**：Qdrant 全量 (33k → 80k points) 带来 nDCG 大幅提升 (+38.5%)。

## Bug 修复记录

### nDCG > 1 异常 (commit `bn7z0e7zy` 修复)
- **现象**: nDCG 输出 1.158/1.291/2.135 等 > 1 数值
- **根因**: `predicted` 列表中**同一个 md 文件的多个 chunk 都有相同 path**, 导致 relevances 重复累计 (例如 predicted 5 个同 path → relevances=[1,1,1,1,1,0,0,0,0,0])
- **修复**: 加 `_dedup_paths()` 函数, 按 path 去重保留首次出现顺序
- **效果**: nDCG 回归正常 0-1 区间

## 已知限制

1. **A. BM25 only 是 placeholder**: 当前 BM25 训练结果未持久化, 实际只跑 dense only 模拟
2. **C. RRF hybrid 等同 dense**: 跟 P1.4 一样, BM25 sparse 没真接入
3. **D. 4046ms 较慢**: bge-reranker-v2-m3 CPU 推理, FlashRank ONNX 待网络恢复启用

## 后续改进方向

1. 接 BM25 sparse 进 RRF (P1 留的优化)
2. FlashRank ONNX (10× CPU 加速, 等网络)
3. 用 chunk_no 而非 path 去重 (更精细)
4. doc_types 过滤提升精度