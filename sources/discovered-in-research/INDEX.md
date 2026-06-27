---
type: discovered-research-master-index
schema_version: 1.0
updated_at: 2026-06-13
---

# 研究过程发现 · 原始资料总索引

本目录存放 **tkk-discover 流程中 web-access 自动捕获**的原始资料 Markdown 副本（含 frontmatter 标注 origin_url / publish_date / tier 等真实性证据链字段）。

## 目录结构约定

```
discovered-in-research/
├── INDEX.md                                ← 本文件（总索引）
├── YYYY-MM-DD-任务简名/                     ← 一个研究任务 = 一个子目录
│   ├── INDEX.md                            ← 任务内索引
│   ├── research_log.md                     ← 检索方案记录
│   ├── SRC-001__标题.md
│   ├── SRC-002__标题.md
│   └── ...
└── ...
```

## 按真实性状态过滤视图

| source_id | task_id | action | wiki_paths | processed_at | tier | authenticity |
|---|---|---|---|---|---|---|
| （暂无记录，待 tkk-discover 流程首次运行后填充） | | | | | | |
| SRC-001..005 | 2026-06-23-诈骗罪虚构事实隐瞒真相与民事界分 | pending | 待 tkk-legal-ingest 消化 | pending | T1-T3 | pending |

## 待核验积压清单（authenticity_status = pending）

| source_id | task_id | tier | pending_since | reason |
|---|---|---|---|---|
| （暂无待核验项） | | | | |

## 维护说明

- 原始资料永久保留，**不删除、不归档、不清理**（即使 wiki 已合并）
- `INDEX.md` 在每次 ingest 完成后自动增量更新
- 跨任务去重：相同 file_hash_sha256 的资料在 INDEX.md 中合并展示，标注「被 N 个任务引用」

## 上游 skill 集成

- **tkk-discover 环节 3**：web-access 命中权威资料 → 自动调用 `scripts/markdown_converter.py` → 写入本目录
- **tkk-legal-ingest ingest 流程**：双入口之一（另一个是 `Clippings/`）