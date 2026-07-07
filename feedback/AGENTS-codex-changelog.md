# AGENTS.md 历史日志(Codex 端,2026-07-06 neat-freak 迁出)

> **目的**:AGENTS.md 留**当前生效的硬规则 + 速查表**;历史叙事 / 事件流 / 行数演进 / 决策变更 → 本文件。
> **位置选择**:Claude Code memory 仓 (`~/tkk-library/feedback/`) — 与 `feedback-tkk-rag-port-8080-to-8081-2026-07-03.md` 等其他反馈同仓;Codex 端通过 filesystem 直读,无 symlink 副本。
> **本文件内容**:8 条历史叙事(2026-07-03 ~ 2026-07-05 已稳定 ≥ 7 天 + 2026-07-04 opencli / web_search / 收尾决策 4 个独立话题)。

---

## 2026-07-03 §B Handoff 协议 6 步→7 步

- **变更**:§B Handoff 协议 6 步→7 步(加**步骤 0** — ESRS task 创建 + `registry.active_task` 写入)
- **硬规则**:4 条→5 条(加 0 号 `active_task` 必写)
- **路径修正**:ESRS 工具实际路径 `/home/kangkang/esrs/tools/`(旧 AGENTS.md 写错为 `~/.codex-staging/bin/`)
- **触发原因**:6 步协议漏"步骤 0"导致 `goal-resume-cron.sh` 误判"无 active_task"自动清 sentinel,接力永不动

## 2026-07-03 neat-freak 清理记录

- **迁出**:
  - `references/minimax-shim-troubleshoot.md`(§4.2 实战细节 **29→5 行**)
  - `references/long-markdown-write-safely.md`(§4.1 阈值表 **18→1 行**)
- **新增**:**项目级入口** 表加 1 行(电子数据证据对抗 32 篇 L3 完整填充,2026-07-03 立项,02-01 设备数据已完成)
- **行数演进**:347 → 314

## 2026-07-04 网络检索策略章节

- **新增**:
  - §网络检索策略
  - `references/codex-net-search-matrix.md`(76 行,source-of-truth)
- **方法论**:以 Codex 原生 `browser_use` 工具族(stable + 启用 + 完整 CDP)为底,`opencli` / `browser-harness` / `mcp` 为补
- **不照搬** Claude Code 端 `web-access`(架构不兼容)
- **行数演进**:314 → 366
- **soft limit**:300 → 370

## 2026-07-04 web_search 启用

- **原 config**:`[features].web_search_request = true` + `web_search_cached = true`
- **后端**:Bing CN,等价 Claude 内置 WebSearch
- **修正 references 错误**:原写「OpenAI 主动砍掉 search API」,实际是 deprecated + 可用,统一合入 `web_search_request`
- ⚠️ **2026-07-05 已更新**:Codex CLI 0.142.5 弃用 `[features]` 表,合并为顶层 `web_search` 枚举(`live` / `indexed` / `cached` / `disabled`),config.toml 改 `web_search = "live"`,`[features]` 表清空

## 2026-07-04 opencli Chrome 基础打通

- **脚本**:`~/.codex-staging/bin/opencli-chrome-launch.sh`:一键启动 Linux Chrome 带 9222 remote-debug + opencli 扩展
- **独立 profile**:`/home/kangkang/.opencli-chrome-profile`
- **现状**(2026-07-04 快照):
  - Chrome 9222 ✅
  - opencli daemon 19825 ✅
  - opencli 扩展 Service Worker 在跑 ⚠️
  - **扩展 ↔ daemon WS handshake 卡住**(doctor 显示 not connected)
- **根因**:v1.8.4 吞了 WS 错误(PR #1979)
- **解法**:`opencli-upgrade.sh` 升 v1.8.6 修 handshake,或用户在 Linux Chrome GUI 点一次 popup 触发

## 2026-07-04 site-patterns 闭环验证(首个)

- **目标站**:bjcourt.gov.cn(2026-07 公告)
- **工具**:Linux Chrome 149 + cdp-proxy
- **结果**:**3 次 navigate 均无 WAF**(`document.body.innerText.includes("知道创宇") === false`)
- **反例发现**:web-access 2026-06-14 的「CDP /navigate 直接命中 WAF」经验**在 2026-07-04 已不成立**
- **沉淀**:`~/.codex-staging/references/site-patterns/bjcourt.gov.cn.md`(105 行,带 `last_test` / `tested_with` / `status` / `related` 字段)
- **关键经验**:URL 模式是 `newsDetail.htm?NId=19位&channel=9位`(**不**是 `/article/detail/2024/11/id/xxxx.html`,那个是 chinacourt.org 的格式)

## 2026-07-04 收尾决策:不升级 opencli

- **决策**:v1.8.4 扩展握手卡住是已知 bug,但**默认不升级 v1.8.6**
- **理由**:
  1. 传输层重构风险 > 收益
  2. 当前任务(法律/学术/跨境/行情)全部走 PUBLIC 类,无扩展也能用
  3. COOKIE/UI 类(社交/海外)用户日常场景用得少
- **触发升级的 3 个条件**(写在 `opencli-upgrade.sh` 顶部):任务驱动 / 严重 bug / 官方 v1.9+
- **行数快照**:369(soft limit 370,余量 1 行,**临界**)

## 2026-07-04 neat-freak 清理(同日收尾)

- **RAG 端口** 8080 → `${RAG_PORT:-8081}`(AGENTS.md 决策树 + references 同步,跟 `feedback-tkk-rag-port-env-var-2026-07-03.md` 一致)
- **决策树 Q1** `jq` 不可用,改用 `python3 -c` 解析 JSON
- **新增** §配套目录索引(列出 skills / references / site-patterns / bin / config.toml 全部产物)
- **soft limit**:370 → 400(余量给下次扩展)
- **行数演进**:369 → 384

## 2026-07-05 web_search 顶层 key 迁移

- **背景**:Codex CLI 0.142.5 弃用 `[features].web_search_request` / `web_search_cached`
- **新 schema**:顶层 `web_search` 枚举(`live` / `indexed` / `cached` / `disabled`)
- **改动**:
  - `config.toml` 改 `web_search = "live"`
  - `[features]` 表清空
  - `codex doctor` 0 warn 验证
  - `references/codex-net-search-matrix.md` 同步更新
- **行数演进**:384 → 386

---

## 当前 AGENTS.md 行数演进(全会话)

| 时间 | 节点 | 行数 | soft limit |
|------|------|------|-----------|
| 2026-07-01 | 初始 | ~200 | 300 |
| 2026-07-03 | §B 7 步 | 347 | 300(已破)→ 350 |
| 2026-07-03 | neat-freak #1 | 314 | 350 |
| 2026-07-04 | §网络检索策略 | 366 | 370 |
| 2026-07-04 | neat-freak #2 | 384 | 400 |
| 2026-07-05 | web_search 迁移 | 386 | 400 |
| 2026-07-06 | tkk-source-fetch v0.2.1 | 389 | 440 |
| 2026-07-06 | v0.2.2 对抗式审查 11 修 | 392 | 440 |
| 2026-07-06 | v0.2.3 外部黑名单 + retry | 394 | 440 |
| 2026-07-06 | **neat-freak #3(本轮)** | → < 350 | 440 |

> **neat-freak 原则**:`§创建信息` 只留**当前生效的硬规则 + 速查表**;事件流 / 行数演进 / 决策变更 → 本文件 + git log。
