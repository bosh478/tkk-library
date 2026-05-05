---
name: tkk-legal-ingest
description: 法律文档 Ingest Skill — 将法律文档编译为 Obsidian wiki 持久化知识网络。触发场景：用户说"整理xxx"、"消化xxx"、"处理xxx目录"、"ingest 这些文件"、"提取文档要点"、"整理法律资料"、"处理 xxx 目录下的法律文档"。支持5层整理级别（第3层详细级为默认）。当 Clippings/ 目录存在 .md 文件时自动检测并处理。执行时无需用户逐阶段确认，全程自动直到完成。功能：ingest/query/purge/lint/知识复合增长增强
---

# Legal Ingest Skill (v50)

> 📌 **快速导航**：[核心原则](#核心原则) | [四大操作](#四大操作) | [ingest流程](#ingest消化新资料) | [references](#references索引)

---

## @核心原则（铁律，5条）

| # | 规则 | 违反后果 |
|---|------|----------|
| R1 | `sources/` 目录原始文件**只读不删** | 不可逆数据丢失 |
| R2 | 永不生成占位符内容（`TODO`/`待补充`/`（略）`） | wiki 质量下降 |
| R3 | 量刑档次三档/四档**必须全部提取**，不许省略第三档 | 法律分析不完整 |
| R4 | 涉及法条内容（数额/日期/适用范围）**必须引用原文**，不确定时主动向用户核验 | 严重错误，误导用户 |
| R5 | Agent 报告不可信 → **必须用脚本验证**；内容 < 500 字符立即复核 | 产出空洞被放行 |

**三色断言**（法条引用后必须标注）：
- ✅ VERIFIED：已核对原文，确认无误
- ❌ NOT_FOUND：原文未找到该表述
- ⚠️ MISMATCH：存在矛盾，需进一步核验

---

## @四大操作

| 操作 | 触发词 | 说明 | 详细流程 |
|------|--------|------|----------|
| **ingest** | "整理xxx"、"消化xxx"、"处理xxx目录" | 消化新资料，编译进 wiki | [[references/ingest-workflow.md]] |
| **query** | "查询xxx"、"请问xxx"、"解释一下xxx" | 基于 wiki 回答，引用原文 | [[references/query-workflow.md]] |
| **purge** | "删除根据xxx整理的资料" | 删除 wiki 页面，保留源文件 | [[references/purge-workflow.md]] |
| **lint** | "lint检查"、"健康检查" | 断链/矛盾/过时/空白/源文件完整性 | [[references/query-workflow.md]] |

---

## @自动模式：Clippings 检测触发

```bash
ls D:/AI\ agent/tkk-library/Clippings/*.md 2>/dev/null | wc -l
```

| 情况 | 行为 |
|------|------|
| Clippings 为空 | 继续正常操作 |
| Clippings 有文件 | **立即自动执行 ingest**，完成后归档到 `sources/网络文章/` |

---

## @法律效力层级（依据《立法法》2023修正）

> ⚠️ **新增：所有 entity 类型页面必须标注 hierarchyLevel**

| 层级 | 类型 | 制定机关 | effectiveness.type |
|------|------|----------|---------------------|
| 1 | 宪法 | 全国人大 | constitution |
| 2 | 法律 | 全国人大/全国人大常委会 | law |
| 3 | 行政法规 | 国务院 | administrative_regulation |
| 4 | 地方性法规 | 省级人大及其常委会 | local_regulation |
| 5 | 部门规章 / 地方政府规章 | 国务院部委 / 省/设区的市政府 | departmental_regulation |
| 6 | **行政程序规范（行政规范性文件）** | **下级行政机关（司/处/科/县区级）** | **internal_norm** |

**关键约束**：
- 下位法与上位法冲突时，冲突条款**自始无效**
- 行政机关适用"**法无授权不可为**"
- 公民/法人适用"**法无禁止皆可为**"

---

## @文件类型与目标目录

| 文件类型 | 目标目录 | type | 必需字段 | 保留度 | hierarchyLevel |
|----------|----------|------|----------|--------|----------------|
| 律师业务指引 | `wiki/summaries/` | `summary` | `category` | 摘录要点 | — |
| 法律法规 | `wiki/concepts/` | `concept` | `tags`含法律部门 | 摘录要点 | — |
| 司法解释原文 | `wiki/entities/` | `entity` | `tags`含解释文号 | **100%** | 2 |
| 行政法规原文 | `wiki/entities/` | `entity` | `tags`含法规名称 | **100%** | 3 |
| 部门规章 / 地方政府规章 | `wiki/entities/` | `entity` | `tags`含制定机关 | **100%** | 5 |
| **行政程序规范（新增）** | **`wiki/entities/`** | **`entity`** | **`tags`含行政程序** | **100%** | **6** |
| 理解与适用 | `wiki/entities/`或`concepts/` | `entity`或`concept` | `tags`含解释文号 | 摘录要点 | — |
| 案例分析 | `wiki/syntheses/` | `synthesis` | `tags`含罪名 | 摘录要点 | — |

**判断**：文件名含"指引"/"指南"/"规程"→summaries；含"解释"/"规定"→entities；含"案例"/"指导案例"→syntheses；**其他→读前20行确认**

### 行政程序规范识别规则（新增）

以下特征符合时，归入本类型：

- 文件名含"程序规定"、"实施细则"、"操作规程"、"办理规范"、"工作规定"等
- 由司/处/科/县区级行政机关发布（非部委、非省级政府）
- 内容为业务办理的流程性、程序性规则
- 具有"构成要件 + 法律效果"结构（符合即认可，不符合即驳回）

**典型文件**：《XX市公安局办理行政案件程序规定》、《XX市监局行政处罚操作细则》

### entity 类型 hierarchyLevel 速查

| 类型 | hierarchyLevel | effectiveness.type |
|------|----------------|---------------------|
| 司法解释 | 2 | legislation_interpretation |
| 行政法规 | 3 | administrative_regulation |
| 地方性法规 | 4 | local_regulation |
| 部门规章 / 地方政府规章 | 5 | departmental_regulation |
| **行政程序规范** | **6** | **internal_norm** |

**理解与适用类**：文件名含"理解与适用" + 作者为最高人民法院/最高人民检察院/全国人大/全国人大常委会法律工作委员会 → entity；其他 → 按普通律师指引处理

**案例分析五级分类**：

| 分级 | 类型 | 前缀 |
|------|------|------|
| ⭐⭐⭐⭐⭐ | 指导性案例（最高法/最高检） | `GuideCase_` |
| ⭐⭐⭐⭐ | 典型案例（两高单位名义） | `TypicalCase_` |
| ⭐⭐⭐⭐ | 入库案例（最高法案例库） | `Court_FaDaWang_` |
| ⭐⭐⭐ | 参考性案例（省级高院） | `RefCase_` |
| ⭐⭐ | 普通案例分析 | `CaseAnalysis_` |

---

## ingest：消化新资料

> 详细流程见 [[references/ingest-workflow.md]]

### 执行流程（7步 + verify 检查点）

```
首次扫描 → 阶段一 → 阶段二 → 阶段三 → 阶段四 → 阶段五 → 末次扫描
```

| 步骤 | 内容 | Verify 检查点 |
|------|------|--------------|
| 0 | **首次扫描**：`ls sources/xxx/*.md \| wc -l` → 记录到 log.md | ⚠️ 无记录 = 阶段一未完成 |
| 1 | 源文件清单分析 + 去重检查 | 首次扫描已记录到 log.md |
| 2 | 内容提取（分层，不是整文件） | 口述定锚结论（核心定义/常见误解/文档类型）后才能开始 |
| 3 | 数量核验 + 内容质量检查 | 7步骤：比对/大小/抽检/占位符/量刑/分类/源文件完整性 |
| 4 | 整合入库（6步骤） | 6步骤全部执行；related 字段已更新 |
| 5 | 完成报告 | log.md 记录完整（含首次+末次扫描） |
| 6 | **末次扫描**：再次扫描，对比是否一致 | ⚠️ 必须写入 log.md |

**⚠️ qmd embed 不等于整合入库！** 整合入库 = 6步骤（交叉链接→index→INDEX→log→演化字段→qmd embed）

### 行政程序规范 ingest 特殊要求（新增）

1. **识别 hierarchyLevel**：根据制定机关判断是否为层级6
2. **标注 superiorLaw**：在 frontmatter 中列出所有上位法
3. **冲突检测**：如识别到与上位法冲突的条款，在正文中标注并在底部"法律效力说明"区域汇总
4. **完整保留**：100%保留原文，不摘要

### 批量处理策略

| 规模 | 策略 |
|------|------|
| < 20个 | 单 Agent 串行 |
| 20-100个 | 按法律部门分组，≤30个/组 |
| > 100个 | 分层处理，每组≤30个且≤6000行 |
| 超大文件（>5000行） | **单独处理**，按 `# 标题` 拆分，每批≤20章节 |

### ingest 铁律（必须执行）

1. **首次扫描必须记录**：log.md 写入 `## [YYYY-MM-DD] 首次扫描 | sources/xxx/`
2. **定锚 checklist 强制**：阶段二前口述结论（核心定义/常见误解/文档类型），无口述不得进入阶段二
3. **Phase 2 门控检查**：输出 >500 字符 + 置信度标注存在 + 无占位符 + 法条引用有三色断言
4. **末次扫描必须记录**：log.md 写入结果，数量一致输出"验证通过"，不一致立即接管

---

## query：基于 wiki 回答问题

> 详细流程见 [[references/query-workflow.md]]

**两种回答模式**：
1. **简单查询**：使用"快速回答框架"，适用于"请问xxx"的简单问题
2. **刑事法律研究**：使用"刑事研究专用流程"，适用于涉及罪名、构成要件、量刑档次等刑事法律问题

**刑事法律研究流程（8步框架）**：
```
1. 确定法律性质 → 2. 找法条/司法解释 → 3. 分析构成要件
→ 4. 找理解与适用/典型案例 → 5. 找量刑情节
→ 6. 评估争议点 → 7. 提出解决方案
（先定性后量刑）
```

**回答规范**：
1. 多角度分析：对问题进行多维度拆解
2. 基于 wiki 回答：所有结论必须来自 wiki 资料
3. 引用规范：答案列出原文 + 来源（`[[页面名]]`格式）
4. 外部信息标注：若使用 vault 外资料，须特别说明

**刑事研究补充规范**：
- 必须展示"思维路径"（为什么这样分析）
- 每条结论必须追溯到 sources 源文件原文
- 发现 wiki 资料不足时，主动联网检索或告知用户补足方向

**写回 wiki 触发条件**：
- 发现两个概念对比 → 创建 synthesis 对比页
- 发现类案规律 → 补充到相关 synthesis
- 发现矛盾 → 在相关页面标注 ⚠️
- 发现重要但 wiki 未覆盖的概念 → 新建 concept 页面
- 发现新旧解释更替关系 → 更新相关 concept 并标注
- 发现新的构成要件理解 → 补充到相关 entity
- 发现量刑标准变化 → 更新相关 entity 并标注 supersedes

---

## purge：根据原始文件删除对应 wiki 页面

> 详细流程见 [[references/purge-workflow.md]]

**⚠️ 不可逆操作，执行前必须二次确认**

源文件是绝对红线——**只删除 wiki 页面，源文件永不删除**

---

## output格式标准

| type | 最低要求 | 优秀标准 |
|------|----------|----------|
| `summary` | 关键要点 ≥ 5 条，每条原文提取 | ≥ 10 条，含程序步骤/风险点/合规要求，有 wikilink |
| `concept` | 章节结构完整，每条编号+简要释义 | 原文引用+释义+关联规定，量刑档次完整 |
| `entity` | 解释要点 ≥ 3 条，涉及法条列表 | 每条原文+适用要点，有案例 wikilink |
| `synthesis` | 裁判要旨 ≥ 100 字，基本信息完整（案号/法院/日期），案例分级+问题意识必填 | 裁判理由+适用要点详细，有类案 wikilink |

---

## @frontmatter 模板（entity 类型）

### 司法解释 / 行政法规 / 部门规章

```yaml
---
title: 文件标题
type: entity
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [标签1, 标签2]
source: [[源文件名]]
hierarchyLevel: 2  # 依据法律效力层级表填写
effectiveness:
  type: legislation_interpretation  # legislation_interpretation / administrative_regulation / departmental_regulation
  status: valid
superiorLaw:  # 上位法列表（如有）
  - 《XX法》第X条
---
```

### 行政程序规范专用模板（层级6，新增）

```yaml
---
title: 文件标题
type: entity
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [行政程序, XX机关, XX业务]
source: [[源文件名]]
hierarchyLevel: 6
effectiveness:
  type: internal_norm
  status: valid
superiorLaw:
  - 《XX法》第X条
  - 《XX规定》
conflictNote: "当下位法与上位法冲突时，冲突条款自始无效，应适用上位法"
issuingAuthority: XX省XX市XX局XX处  # 行政机关全称
documentNumber: [文号]  # 如：X规〔2024〕X号
---
```

### 冲突条款标注机制（新增）

在页面正文中，如识别到与上位法冲突的条款：

```markdown
⚠️ 该条款与《XX法》第X条冲突，冲突条款自始无效，应适用上位法。
```

在页面底部添加 `## 法律效力说明` 区域：

```markdown
## 法律效力说明

- 层级：行政程序规范（层级6），法理上不具有正式法律效力，实务中具有行政约束力
- 上位法：《XX法》第X-X条
- 冲突条款：第X条与《XX法》第X条冲突，自始无效
- 适用原则：**法无授权不可为**（行政机关）；**法无禁止皆可为**（公民/法人）
```

---

## references索引

| 引用 | 内容 |
|------|------|
| [[references/ingest-workflow.md]] | ingest 五阶段详细流程（含首次/末次扫描铁律、Phase 2 门控、批量策略） |
| [[references/query-workflow.md]] | query 操作详细流程（含快速回答框架） |
| [[references/purge-workflow.md]] | purge 操作详细流程 |
| [[references/lint-workflow.md]] | lint 健康检查详细流程（含7项检查项） |
| [[references/command-ref.md]] | 常用命令速查 |
| [[references/templates.md]] | 模板库（guide/book/lecture/minimal） |
| [[references/VERSION-full.md]] | 完整版本历史 |

---

## 关键文件路径

| 路径 | 说明 |
|------|------|
| `D:\AI agent\tkk-library\` | Vault 根目录 |
| `sources/` | 原始文件目录（只读不删） |
| `sources/INDEX.md` | 源文件索引 |
| `wiki/summaries/` | 律师业务指引摘要 |
| `wiki/concepts/` | 法律法规、概念、制度 |
| `wiki/entities/` | 司法解释原文、法条全文、行政程序规范 |
| `wiki/syntheses/` | 案例分析、综合研究 |
| `log.md` | 活动时间日志 |
| `index.md` | Wiki 目录索引 |
| `scripts/phase2_gate.py` | Phase 2 门控检查脚本 |
| `scripts/phase3_spot_check.py` | Phase 3 内容抽检脚本 |

---

## 版本历史（精华版）

| 版本 | 日期 | 核心变化 |
|------|------|----------|
| v50 | 2026-05-05 | **新增：刑事法律研究专用 query 流程**，8步研究框架引导，思维路径展示，知识缺口主动发现机制 |
| v49 | 2026-05-05 | **新增：行政程序规范类型（层级6，internal_norm）**，法律效力层级表，冲突条款标注机制 |
| v48 | 2026-05-03 | 审计修复：20处缺口全部修复，Phase 2/3 门控脚本 |
| v42 | 2026-05-01 | 理解与适用类资料整理规范 |
| v40 | 2026-05-01 | 案例分析五级分类+法教义学七种解释方法 |
| v38 | 2026-04-28 | Anti-Hallucination Mandate三色断言 |
| v37 | 2026-04-28 | 定锚checklist+第4层内观视角 |
| v31 | 2026-04-27 | 首次扫描+末次扫描铁律 |
| v28 | 2026-04-26 | Clippings自动检测触发功能 |

<details>
<summary>📜 完整版本历史（v1-v48）</summary>

[[references/VERSION-full.md]]

</details>
