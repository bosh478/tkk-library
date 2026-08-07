# CLAUDE.md — LLM Wiki Schema

本文件是 LLM Wiki 的 Schema，定义 wiki 的结构、约定和工作流程。LLM 应遵循本文件的规范维护 wiki。

---

## 核心理念

wiki 是一个**持久化、累积性的知识库**。它不是每次查询时从原始文档重新检索的 RAG 系统，而是 LLM 增量构建和维护的结构化知识体。

交叉引用已在其中。矛盾已标注。综合已形成。新资料进入时，LLM 负责将其整合进已有 wiki，而非仅做索引。

---

## 三层架构

### 1. Raw Sources（原始资料）

路径：`/sources/`

- 存放来源文件，**不可直接修改**
- 分类组织：`/sources/裁判文书/`、`/sources/法律法规/`、`/sources/网络文章/`、`/sources/书籍资料/`
- 每个来源文件附带元数据注释（来源 URL、获取日期、文件类型）

### 2. Wiki（维基页面）

路径：`/wiki/`

LLM 完全拥有的知识层，所有 wiki 页面存于此：

| 子目录 | 内容 |
|--------|------|
| `entities/` | 实体页：案件、法条、机构、人物 |
| `concepts/` | 概念页：罪名、制度、法律原则、程序 |
| `syntheses/` | 综合分析页：专题研究、对比分析、案件复盘 |
| `summaries/` | 来源摘要页：每个原始资料的消化摘要 |

### 3. Schema（本文件）

即本文件，定义工作规范。

---

## 文件命名约定

- **Wiki 页面**：`类型_标题.md`（如 `concept_受贿罪.md`、`entity_最高法2026解释二.md`）
- **来源文件**：保留原始文件名，仅在顶部加 YAML frontmatter 记录元数据
- **目录**：全小写，用下划线分隔（如 `source_documents`）

---

## Wiki 页面格式

每个 wiki 页面必须包含：

```markdown
---
title: 页面标题
type: concept | entity | synthesis | summary
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [标签1, 标签2]
sources: [关联来源文件列表]
---

## 正文
```

- 正文用 Markdown 格式
- 法条引用格式：`《刑法》第XX条`（无书名号内空格）
- 案例引用格式：`[案件名]（[案号]）`
- 重要论断需标注来源：`① 来源：xxx`

### Summary 页面附加要求

`wiki/summaries/` 下的摘要页 **必须** 在 frontmatter 中包含 `category` 字段，用于自动汇总到 index.md：

```yaml
---
title: 律师办理公司对外担保业务操作指引2024
type: summary
published: 2024-12-17
created: 2026-04-14
tags: [律师业务指引]
category: 诉讼与仲裁
source: [[20241217_律师办理公司对外担保业务操作指引2024]]
---
```

**NotebookLM 风格格式（含以下全部或部分 section）**：

```markdown
## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[源文件名]] |
| 类型 | 律师业务指引 / 司法解释 / 案例分析 / ... |
| 发布日期 | YYYY-MM-DD |
| 关键词 | tag1 / tag2 / tag3 |
| 核心要点 | 3-5 条精炼摘要 |

## ❓ 常见问题

> 问：...
> 答：...

## 📅 时间线（立法类文档适用）

| 时间 | 事件 | 主要变化 |
|------|------|----------|
| YYYY-MM | 版本/解释X发布 | 主要内容... |

## 正文
```

**格式说明**：
- `## 📋 文档概览`：NotebookLM 的 Source Overview Card，5 列结构化元数据
- `## ❓ 常见问题`：AI 自动生成的 FAQ，增强页面交互性
- `## 📅 时间线`：立法进程、解释演进类文档适用，Timeline 格式

> 注意：
> - 书籍摘要（刑法释义、司法解释全书、审判指导案例、公诉人指南）不归入 summaries，而是移入 `wiki/concepts/` 或 `wiki/syntheses/`，不使用 category 字段。
> - FAQ 和时间线为建议添加项，文档概览为必填项

category 取值：
- **律师业务指引类**（存放于 `wiki/summaries/`）：
  - 诉讼与仲裁 / 公司商事与合规 / 劳动与社会保障 / 医药健康 / 国际贸易 / 婚姻家庭与继承 / 建筑工程与房地产 / 政府与公共法律服务 / 生态环境与能源 / 知识产权 / 诉讼与仲裁（民商事） / 金融与财税
- **刑事参考类**（存放于 `wiki/summaries/`，仅限律师业务指引中的刑事相关内容）

---

## 交叉引用规范

- Wiki 内部用 Obsidian 双向链接 `[[页面标题]]`
- 同罪名/概念在不同条文的差异 → 对比表格
- 相关概念页之间在底部 `## 相关` 互相链接
- 矛盾/更新关系明确标注: `⚠️ 与 [[xxx]] 存在冲突,以 [[xxx]] 为准`

## 工作流程

### 批量 Ingest 三阶段门（处理 5 个以上文件）

1. **阶段一（Agent 执行）**: 并行 Agent / batch script 处理。**禁止更新 index.md / log.md**
2. **阶段二（清理验证）**: 检测截断 (< 5KB / < 20 行 → 可疑);去重 (同名保留最大);sources ↔ summaries 一一对应
3. **阶段三（索引更新）**: summary `category` 字段汇总 → index.md 条目 → log.md 记录

> ⚠️ 阶段门是硬性规则;阶段一完成前不得执行阶段二/三;并行 Agent 运行期间主会话**不做任何不可逆写操作**。

### 批量 Ingest 执行规范（经验固化 v2, 精简版）

处理 10 个以上文件时,核心硬规则如下。**任何规模都必须执行**。

| # | 阶段 | 必做 |
|---|------|------|
| 1 | 处理前 | `ls sources/xxx/*.md \| wc -l`;预判覆盖/命名;检查 frontmatter `structure` 长度 |
| 2 | 并行 Agent | **每批完成后立即验证**:`ls wiki/*.md \| wc -l` 计数;**Agent 报告不可信**,必须用脚本验证 |
| 3 | 命名差异 | `base_clean=$(echo "$name" \| sed 's/（[0-9]*年[修正修订]*）//g')` |
| 4 | 数量核验 | Phase 1→2 之间**必须** `SOURCE_COUNT == TARGET_COUNT` 否则主会话接管 |
| 5 | 进度监控 | 每批后查 `ls wiki/*.md \| wc -l`;Phase 3 完后验 `index.md` |
| 6 | 内容质量 | **禁止占位符** (`TODO`/`待补充`/`（略）`);不合格 Phase 2 返工 |
| 7 | frontmatter | `type/category/tags/source/created/updated` 一次写齐 |
| 8 | 索引策略 | < 20 逐条 / ≥ 20 类目概述 + glob 引用 |
| 9 | Phase 2 门控 | 数量核验 + 断链 `grep -r "\[\["` + 尺寸 + 内容抽检(每类 3 个) + 命名验证(3-5 个);**任一不达标 → 返工** |
| 10 | 脚本命名 | 跑前抽检 3-5 个实际文件名 vs `extract_date()` 正则 |

**Agent 报告"全部完成"≠ 内容合格**;**Agent 报告"处理 3-5 个"≠ 上下文限制**,要用 `ls` 实际数。

**关键代码片段**(完整命令清单见 `references/ingest-workflow.md`):

```bash
# Phase 1→2 数量核验(最关键!)
SOURCE_COUNT=$(ls sources/xxx/*.md | wc -l)
TARGET_COUNT=$(ls wiki/summaries/*.md | wc -l)
[ "$SOURCE_COUNT" -eq "$TARGET_COUNT" ] || echo "⚠️ 数量不一致!"
```

**占位符内容禁例**:`(待补充具体内容)` / `TODO` / `（略）` / 空 frontmatter 一律返工。Phase 1 摘要必须从源码提取(关键段落 + 要点列表)。

---

### Ingest（消化新资料）

1. 将原始文件放入对应 `sources/` 子目录
2. LLM 阅读原始文件
3. 讨论关键要点（与用户）
4. 写入摘要页到 `wiki/summaries/`
5. 更新 `index.md` 中的相关条目
6. 在 `log.md` 中记录 ingest 事件
7. 检查是否需要更新已有的 entity/concept 页面

### Query（回答问题）

1. 读取 `index.md` 定位相关页面
2. 读取相关 wiki 页面
3. 综合回答，标注来源
4. **重要**：如果回答产生有价值的新内容（分析、对比、发现），将其写入 wiki 作为新页面

### Lint（健康检查）

定期（每次重要 ingest 后或每周）执行：

1. 检查断链（orphan pages）
2. 检查矛盾（同一问题在不同页面的说法是否一致）
3. 检查过时（较新的来源是否推翻旧结论）
4. 检查空白（重要概念是否已有页面）
5. **验证 index.md Summaries 条目数与 wiki/summaries/ 文件数一致，各分类计数与实际条目匹配**
6. 将检查结果记入 `log.md`

---

## index.md 格式

```markdown
# Index

## Entities（实体）
| 页面 | 摘要 | 更新日期 | 来源数 |
|------|------|----------|--------|

## Concepts（概念）
| 页面 | 摘要 | 更新日期 | 相关法条 |

## Syntheses（综合）
| 页面 | 摘要 | 日期 |

## Summaries（来源摘要）
| 来源 | 摘要 | 日期 |
```

---

## log.md 格式

```markdown
# Log

## [YYYY-MM-DD] ingest | 来源标题
- 操作：消化 xxx
- 创建/更新页面：[[页面1]] [[页面2]]
- 备注：...

## [YYYY-MM-DD] query | 用户问题摘要
- 涉及页面：[[页面x]]
- 关键结论：...

## [YYYY-MM-DD] lint
- 检查结果：...
- 发现问题：...
```

---

## 输出格式优先级

1. **对比表格** (罪名/制度/情节对比) → 2. **ASCII 流程** (程序步骤/因果) → 3. **结构化清单** (构成要件/证据/风险) → 4. **时间线** (立法/案件) → 5. 文字仅作图表补充

## 域特定规范（法律）

- 罪名按犯罪类型分类(贪腐/暴力/财产/经济/职务/知识产权/...)；每个罪名页含构成要件/立案标准/量刑档次/司法解释/典型案例
- 法条修改历史在对应 concept 页中记录；司法解释与刑法条文的关系**明确标注**(解释重点/补充/修改)
- 司法解释文号 (法释〔YYYY〕X号) 在 entity 页 `tags` 中**必须**含涉及罪名

## 多维索引规范（支持复杂查询）

### 五大索引维度(支持"复杂查询"和"疑难问题查询")

| 维度 | 典型查询 | 文件归类 |
|------|----------|----------|
| **罪名** | "贪污罪与职务侵占罪的界限" | `wiki/concepts/` (按刑法分则章节) |
| **业务** | "公司对外担保合规审查要点" | `wiki/summaries/` 按 `category` 归类 |
| **程序** | "刑事合规整改第三方监督评估程序" | `wiki/concepts/` |
| **法条** | "《刑法》第388条斡旋受贿的认定" | `wiki/concepts/` + `wiki/entities/` |
| **解释** | "法释〔2026〕6号解释（二）" | `wiki/entities/` (按文号) |

**交叉引用规则**:Concept 页 `related` 字段列同章节罪名 + `## 相关` 链 entity/同类;Summary 页 `tags` 含业务+程序;Entity 页 `tags` 含文号+涉及罪名。

**文件类型 → 目标目录**:`summaries/` 律师指引(`type:summary,category`) | `concepts/` 释义/概念(`type:concept`) | `entities/` 司法解释原文(`type:entity`) | `syntheses/` 案例/对比(`type:synthesis`)

**Ingest 流程**(4 步):1. 判文件类型 → 2. 写目标目录 + 更新 `related` → 3. 同步 `index.md` 索引 → 4. `log.md` 记录事件

---

## 自我验证规则（纠错经验总结,精简版）

| # | 必查 | 必做 | 触红线场景 |
|---|------|------|------------|
| 1 | **量刑档次完整性** | 核对原文"三年以下/三-七年/七年以上"等所有幅度,逐档有对应条目 | 漏第三档 |
| 2 | **批量文件处理完整性** | 处理前 `ls \| wc -l`,处理后逐个核对;问"还有哪些未处理" | 报告"完成"实际漏 2 个 |
| 3 | **明确指令优先** | 用户说"直接安装"→不审计;"继续创建"→先总结已完成的,再继续 | 自行加 skill-vetter / 占位符 |
| 4 | **Wiki 质量** | 无 UI 残留 / 无 `TODO` / frontmatter 完整 / 交叉引用有效 | - |
| 5 | **法律条文准确性** | 法条引用须注源文件;不确定数额/效力时主动问用户 | 编造法律条文 / 主观推测"数额提高" |

**生成后自检顺序**:
1. 量刑档 → 2. 数量 → 3. 指令依从 → 4. Wiki 质量 → 5. 法律准确性

**验证脚本**（vault 根 `scripts/`）:
- `phase2_gate.py` — 输出>500 字符 / 置信度 / 无占位符 / 三色断言
- `phase3_spot_check.py` — frontmatter 完整性 / 正文非空

**硬性规定**:不确定时主动向用户核验,**严禁编造法律条文内容**。

---

## 🗄️ 远端备份(2026-07-02 落地)

| 仓库 | 路径 | 远端 |
|------|------|------|
| `tkk-library` | vault 整盘 (含 Clippings/scripts/.obsidian) | `git@github.com:bosh478/tkk-library.git` |
| `tkk-wiki` | **只** `wiki/` 知识资产 (12,205 文件 / 8.65 MB) | `https://github.com/bosh478/tkk-wiki.git` |

- 本地 `wiki/` = **source-of-truth**;两库各 commit 各 push,互不嵌套
- 排除: `.cache/` `.drafts/` `.checkpoints/`
- Push: `wiki-push.sh [-m "vault: <msg>"]` (脚本在 `~/.codex-staging/bin/wiki-push.sh`)
- 灾难恢复: `git clone git@github.com:bosh478/tkk-wiki.git`
