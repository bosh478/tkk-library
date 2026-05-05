# 文件类型与目标目录

> SKILL.md 第73-120行 内容提取
> 法律文档分类规则、hierarchyLevel 速查、案例分级

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