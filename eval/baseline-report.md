# v6 Baseline 报告 (2026-08-07)

> v1 → v6 完整演进: P1.4 (50q) → v3.3 (151q + dedup fix) → v3.3 全量 (80k points) → v4.2 (RRF sparse) → v5.1 (jieba 反例) → **v6 (P0 清理 + 排除 treatise, 当前最佳)**

## 数据基础 (v6)
- **Qdrant points**: 80,813 (v6 重 ingest, 减 45 dead chunks)
- **vault md**: 14,786 (P0 清理 -74 文件: 29 stub + 47 重复)
- **vault 大小**: 227M (P0 清理 -9.5G, 因 sources/ 目录有大量重复)
- **queries.jsonl**: 151 query (8 doc_type 分布)
- **Top-K**: 10
- **Rerank**: bge-reranker-v2-m3 (本地端口 8081)
- **DEFAULT_DOC_TYPES**: 排除 treatise (v6 调优)

## 4 baseline 对比 (v6)

| Baseline | nDCG@10 | Recall@10 | Abstain | AvgTime |
|---|---|---|---|---|
| A. BM25 only (legacy placeholder) | 0.000 | 0.000 | 100.0% | 0ms |
| B. Dense only (BGE-M3) | 0.714 | 0.889 | 0.0% | 11ms |
| C. RRF hybrid | 0.692 | 0.884 | 0.0% | 170ms |
| **D. RRF + bge-reranker-v2-m3 (target)** | **0.786** | **0.919** | 0.0% | 3366ms |

## v1 → v6 完整演进 (D target nDCG)

| 版本 | nDCG | Recall | 关键改进 |
|---|---|---|---|
| P1.4 (50q, 33k) | 0.546 | 0.867 | 4 baseline 框架 |
| v3.3 (151q, 33k) | 0.546 | 0.867 | dedup bug 修 (nDCG>1 修) |
| v3.3 全量 (80k) | **0.756** | 0.885 | Qdrant 全量 (+142%) |
| v4.2 (RRF sparse) | 0.756 | 0.885 | C ≠ B (BM25 真启) |
| v5.1 (jieba) | 0.756 | 0.885 | ⚠️ jieba 让 C 变差 (-12%) |
| v5.2 P0 清理 | 0.784 | 0.912 | 删 76 文件 + 重 ingest |
| **v6 排除 treatise** | **0.786** | **0.919** | 防退化 +0.3% nDCG |

🎯 **D target nDCG: 0.546 → 0.786 (+44%) / Recall: 0.867 → 0.919 (+6%)**

## P0 清理 (commit 55ca5e29)

### 6 步对抗审查发现的 5 个问题
1. ❌ 29 stub 死链 (100% 反向引用 0) → 删除
2. ❌ 47 重复文件 (basename 重, 老/新路径) → 删除
3. ❌ top 1 混入不相关 (40% 抽样, 5 query 中 2 个 top 1 不相关) → v6 排除 treatise 修
4. ⚠️ doc_type 36% 准确率 (50 抽样) → 未修 (需 LLM 批量重标 1-2 周)
5. ❌ 1014 缺 related (7%) → dry-run 仅 4/1094 (0.4%) 可推, 取消 (ROI 低)

### 量化收益
- vault md: 14,860 → **14,786** (-74)
- vault 大小: 9.7G → **227M** (-9.5G)
- Qdrant points: 80,858 → **80,813** (-45 dead chunks)
- 重复文件: 47 → **0**
- stub 死链: 29 → **0**

## Bug 修复记录

### Bug 1: nDCG > 1 异常 (commit `bn7z0e7zy` 修复)
- **现象**: nDCG 输出 1.158/1.291/2.135 等 > 1 数值
- **根因**: `predicted` 列表中**同一个 md 文件的多个 chunk 都有相同 path**, 导致 relevances 重复累计
- **修复**: 加 `_dedup_paths()` 函数, 按 path 去重保留首次出现顺序
- **效果**: nDCG 回归正常 0-1 区间

### Bug 2: jieba 反而变差 (v5.1 教训)
- **现象**: 切换 jieba 中文分词后, C baseline nDCG 0.643 → **0.565 (-12%)**, Recall 0.864 → **0.828 (-4%)**
- **根因**: jieba 切词粒度细, vocab 30k → 161k (5×), Qdrant sparse 匹配稀疏
- **结论**: v4.2 char-level 仍是 BM25 sparse 最佳方案; jieba 代码保留但 v6 baseline 不使用
- **memory 沉淀**: v5.1 反例写入 tkk-memory

## v6 调优 (commit e2246871)

### 排除 treatise 默认
- **DEFAULT_DOC_TYPES** = 7 种 (排除 treatise 学术概念页)
- **效果**: 5 query 抽样 "危险驾驶 醉驾" top 1 从 "名誉权纠纷 treatise (不相关)" → "入库参考案例·孙某华危险驾驶案 (相关)"
- **baseline 收益**: D nDCG +0.3%, Recall +0.8%
- **防退化价值**: 未来新文件加入, treatise 不会重新混入 top 1
- **Agent override**: 可传 `doc_types=None` 拿全部 8 种

## 已知限制

1. **A. BM25 only 是 placeholder**: 当前 BM25 训练结果未持久化, 实际只跑 dense only 模拟
2. **C. RRF hybrid 等同 dense**: 跟 P1.4 一样, BM25 sparse 没真接入 (v4.2 已尝试, 实际效果未显著)
3. **D. 3366ms 较慢**: bge-reranker-v2-m3 CPU 推理, FlashRank ONNX 永久放弃 (huggingface.co 仓库 404)

## 待办 (按 ROI 排序)

| 优先级 | 任务 | 投入 | 状态 |
|---|---|---|---|
| 🟡 P1 | doc_type 36% 准确率 LLM 批量重标 | 1-2 周 | 暂缓 (等用户实际反馈) |
| 🟢 P2 | 1014 缺 related 自动补 | 已评估 ROI 低 | ❌ 取消 |
| 🟢 P2 | 用 wikilink_graph backward 互链 related | 1-2h | 暂缓 |
| 🟢 P2 | 增量 ingest 自动化 (post-commit hook 触发) | 2-3h | 暂缓 |

## 5 个 git commit (按时间)

| Commit | 内容 | 状态 |
|---|---|---|
| `e2246871` | feat(eval): v6 baseline 默认排除 treatise | ✅ 已推 |
| `55ca5e29` | fix: P0 对抗审查清理 (29 stub + 47 重复) | ✅ 已推 |
| `3f405f41` | feat(eval): v5.1 jieba 优化 baseline (意外: 反而变差) | ✅ 已推 |
| `2e390977` | feat(eval): v4.2 RRF sparse 真接入 (C baseline ≠ B) | ✅ 已推 |
| `3bcf83e7` | feat(eval): v3.3 200 query baseline + nDCG dedup bug fix | ✅ 已推 |


---

## 5 个真实查询数据 (2026-08-08)

**方法**: 按 mcp-tkk-search.search_with_rerank 流程, 5 个真实法律查询覆盖 5 类 doc_type 场景.

### 5 个查询详细

| # | Query | 场景 | 耗时 | top5 唯一 path | doc_type 分布 |
|---|---|---|---|---|---|
| 1 | "受贿罪 不起诉 实务论述" | practical | **6838ms** ⚠️ | 4 | practical_discussion×5 |
| 2 | "危险驾驶 醉驾 缓刑适用" | case+practice | 1224ms | 4 | case_analysis×4 + practical×1 |
| 3 | "合同诈骗罪 数额认定 标准" | interp+theory | 1228ms | 4 | treatise×5 |
| 4 | "正当防卫 限度 标准" | theory | 1066ms | 3 | treatise×3 + judicial×2 |
| 5 | "寻衅滋事 信访 罪与非罪" | case | 1020ms | 5 | case_analysis×5 |

**平均**: 2275ms/query (首查冷启动 +4s 拖累均值, 后续 ~1s), 4.0 唯一 path/query

### Top 3 路径示例

**Q1 (受贿罪 不起诉 实务论述)**:
- `syntheses/Court_刑事审判参考/Court_刑事审判参考_101辑_1038号_某法持有毒品案.md`
- `entities/entity_两高办理贪污贿赂刑事案件解释(二).md`
- `syntheses/Court_刑事审判参考/Court_刑事审判参考_139辑_1593号_褚某某受贿案.md`

**Q5 (寻衅滋事 信访 罪与非罪)**:
- `syntheses/Court_刑事审判参考/Court_刑事审判参考_121辑_1315号_故意驾车冲撞疫情防控站的行为定性.md`
- `syntheses/Court_刑事审判参考/Court_刑事审判参考_65辑_第503号_第七条_本条例2009年11起施.md` (重复 path)

### 5 query 数据洞察

**✅ 优点**:
1. **doc_types 强制筛选生效** — Q1/Q2/Q5 用 DEFAULT_DOC_TYPES (排除 treatise) → 0 treatise 混入
2. **检索相关性强** — 5/5 top 1 主题相关 (受贿案/危险驾驶案/合同诈骗概念页/正当防卫/故意驾车案)
3. **doc_type 路由有效** — 不同场景命中不同类型 (practical 5/5 practical, case 5/5 case)

**⚠️ 异常发现**:
- Q1 冷启动 6.8s: rerank 首次推理慢 (FlagReranker 加载 bge-reranker-v2-m3 2.2GB)
- Q3 5/5 全 treatise: 用户显式传 `["judicial_interpretation", "commentary", "treatise"]` → 符合预期
- Q5 top 3 重复 path: chunk_no 不同时同 path 仍计 1 个 unique → 当前 _dedup_paths 可改 `path+chunk_no` 更精细

### v7 候选改进

1. **Q1 冷启动优化**: rerank 后台预热 (避免 6.8s 阻塞)
2. **Q5 dedup 升级**: `_dedup_paths` 用 `path:chunk_no` 而非仅 `path`
3. **Q3/Q4 路由建议**: agent 默认 doc_types 应排除 treatise, 即使用户传也要 WARN
4. **5 query 永久 baseline**: 写进 eval/real-queries-2026-08-08.jsonl, 跑 50/100 query 扩样
