---
type: discovered-research-task-index
task_id: tkk-discover/2026-06-23-诈骗罪虚构事实隐瞒真相与民事界分
schema_version: 1.0
updated_at: 2026-06-24
---

# 任务内索引 · 2026-06-23 诈骗罪虚构事实隐瞒真相与民事界分

## 原始资料清单

| source_id | 标题 | tier | origin_url | authenticity | ingested_to_wiki |
|---|---|---|---|---|---|
| SRC-001 | 两阶层 vs 四要件实务差异的本土化路径 | T3(待研究) | — | pending | — |
| SRC-002 | 刑民界分"同案不同判"的实证研究 | T3(待研究) | — | pending | — |
| SRC-003 | "前无后有"型案件的具体判例 | T1(待研究) | — | pending | — |
| SRC-004 | 转化型案件的罪名选择标准 | T1(待研究) | — | pending | — |
| SRC-005 | 担保链后续欺骗的独立评价 | T1(待研究) | — | pending | — |

> **说明**:本任务采用**简化版 tkk-discover 执行**(未真正调 deep-diver / public-writer 子 agent),所以**没有 web-access 抓取的原始资料**。本目录的 5 个 SRC 是**知识缺口**(corpus-first 机制应识别但未真正识别的内容),用于后续用 tkk-legal-ingest 消化到本地 Wiki。

## 检索方案摘要

详见同目录 `research_log.md`。

## 元问题关联

- 元问题 1:诈骗罪中虚构事实、隐瞒真相的两阶层构成要件认定
- 元问题 2:诈骗罪与普通民事纠纷的界分
- 元问题 3:非法占有目的的时点演变认定(用户 2026-06-23 增量追问)
- 元问题 4:非法占有目的的七种推定情形 + 转化型案件
- 元问题 5:以贷还贷 / 担保链后续欺骗 / 被害人承诺的出罪可能

## 方法论硬约束(2026-06-23 永久记忆)

- 刑事案件分析必须用两阶层(构成要件该当性 + 违法性 + 有责性),严禁四要件
- 关联 memory:`feedback-criminal-law-two-tier-system.md`
- 关联方法论手册:`/home/kangkang/tkk-library/methodology/legal-analysis-methodology-v1.0-two-tier.md`

## 维护说明

- 任务级 INDEX.md 由 `scripts/markdown_converter.py` 写入新 SRC 时自动追加行
- `research_log.md` 由 `scripts/markdown_converter.py` 追加检索会话条目
- 任务结束后本目录永久保留
- **本任务**通过手动 bootstrap 方式回填(因为 tkk-discover 简化版未触发 reverse flow)
