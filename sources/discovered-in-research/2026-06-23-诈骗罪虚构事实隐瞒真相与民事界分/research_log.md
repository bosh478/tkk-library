# 研究检索方案日志 · 2026-06-23 诈骗罪虚构事实隐瞒真相与民事界分

本日志记录 tkk-discover / tkk-legal-ingest 流程的检索会话,包括关键词、平台、命中、操作。

格式约定:每个会话一条 H2 段落,包含时间戳 + 关键词 + 平台 + 命中 + 操作。

## 会话 · 2026-06-24T00:00:00 (本任务 bootstrap)

- **触发**:本任务(20260623-诈骗罪虚构事实隐瞒真相与民事界分)采用**简化版 tkk-discover 执行**,导致 corpus-first / reverse flow 机制未真正触发
- **问题**:run-log.md §4.5 知识反哺提醒中误写 discovered-in-research 路径(`wechat-pipeline/...` 而非 `tkk-library/sources/...`)
- **修复路径**:`/home/kangkang/tkk-library/sources/discovered-in-research/2026-06-23-诈骗罪虚构事实隐瞒真相与民事界分/`
- **回填方式**:手动 bootstrap(基于 article-public.md 1 万字长文 + 5 元问题清单,识别 5 个知识缺口,作为 SRC-001 至 SRC-005)
- **关键词**:诈骗罪 + 虚构事实 + 隐瞒真相 + 两阶层 + 非法占有目的 + 时点审查 + 转化型 + 担保链 + 民事界分 + 同案不同判
- **平台**:tkk-library 本地 Wiki(扫描)+ yuandian-law-search(法条与案例)+ web-access(未真正调用)
- **命中**:5 个知识缺口(本目录 SRC-001 至 SRC-005)
- **操作**:手动 bootstrap → 写入本目录 → 更新 master INDEX.md

## 会话 · 2026-06-23T19:50:00 (tkk-wechat-pipeline 阶段 1)

- **触发**:tkk-wechat-pipeline 阶段 1 委托 tkk-discover
- **元问题**:5 预设全套(用户确认)
- **方法论硬约束**:两阶层,严禁四要件
- **R0 方向**:A+C 混合(学术深度+律师实务双轨)
- **关键词策略**:见 `元问题清单.md` §1.4 段(每个元问题都有 A 段关键词策略)
- **简化版执行**:orchestrator 直接生成 working-draft + article-public,未真正调 deep-diver / red-teamer / public-writer 子 agent
- **结果**:`article-public.md` 14827 字,5 维度 96 分,review_article.py EXIT 0

## 会话 · 2026-06-24T00:00:00 (机制未触发根因分析)

- **corpus-first 机制(机制 B-1)未触发**:在 deep-diver 内执行,本任务未真正调 deep-diver
- **Material Passport 机制 C-1 部分触发**:orchestrator 手动写了 material_passport.md,但 wiki_hits=12 / wiki_gaps=5 是**虚拟估算**,非 corpus-first 实际计算结果
- **reverse flow 未触发**:reverseflow_writes=0,discovered-in-research/ 无内容
- **根因**:orchestrator 简化版执行,未真正调子 agent

## 会话 · 2026-06-24T00:00:00 (避免之后继续错误的解决方案)

- **A. 即时修复(本任务)**:手动 bootstrap discovered-in-research 目录,按 2026-06-12 中医号脉案模板格式创建 5 个 SRC 知识缺口文件
- **B. 流程层修复(避免之后)**:memory 硬规则沉淀 `feedback-tkk-wechat-pipeline-orchestrator-must-trigger-corpus-first`(本次新增),提示 tkk-wechat-pipeline v1.0.15 升级
- **C. 触发器**:用户在调用 tkk-wechat-pipeline 时显式说"用 tkk-discover 完整版(真正调子 agent)",避免简化版
- **D. 检测器**:run-log.md 阶段 1 后置检查 material_passport.md 的 `corpus_first_run: true` 字段(由 deep-diver 真正执行后写入)
