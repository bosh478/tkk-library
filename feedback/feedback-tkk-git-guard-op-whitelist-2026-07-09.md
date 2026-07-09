# tkk-legal-ingest git_guard.sh OP 白名单(2026-07-09)

## 一句话

`tkk-legal-ingest/tool/git_guard.sh` 的 `pre/post` 子命令**必须**传白名单内 op(`ingest` / `query` / `purge` / `lint` / `migrate` / `backup` / `sync`),任意字符串会触发 `--no-verify` 自动 commit — 实测 `pre test <vault>` 误 commit 190 文件 / 49,231 行。修复:加 OP 白名单 + 参数解析 case 分支重构(commit `b9271c3`)。

## 4 个关键踩坑

### 1. status / log / rollback 子命令参数错位

- 脚本原签名 `CMD=$1 / OP=$2 / VAULT=$3 / MSG=$4` 假设所有子命令都是 `pre/post` 的 `cmd op vault [msg]` 结构
- 但 `status <vault>` / `log <vault>` / `rollback <vault>` 只接 2 个参数,VAULT=$3 必空值,报 `ERROR: vault_root required`
- **正确解法**:case 分支按子命令分配参数位置(pre/post 在 \$2/\$3,rollback/status/log 在 \$2)

### 2. pre 子命令无 OP 白名单(高危)

- `pre <op> <vault>` 接受任意字符串作 op,`git commit -m "pre-$OP: ..." --no-verify` 直接 commit
- 实测回归测试时跑 `bash git_guard.sh pre test /home/kangkang/tkk-library` → 自动 commit **190 文件 / 49,231 行**
- **正确解法**:case 白名单只接受 `ingest` / `query` / `purge` / `lint` / `migrate` / `backup` / `sync`,非法 op 立即 exit 1

### 3. `--no-verify` 是危险开关

- git_guard 用 `--no-verify` 绕过 pre-commit hook,意味着 hook 检查全部跳过
- 配合无白名单,等于"任意字符串都能绕过所有校验自动 commit"
- **正确解法**:`--no-verify` 必须配合白名单使用,**不能**单独依赖

### 4. 误操作事故复盘(2026-07-09 实际发生)

```
$ bash git_guard.sh pre test /home/kangkang/tkk-library
[d56d926] pre-test: before test operation
 190 files changed, 49231 insertions(+)
 create mode 100644 "Clippings/2026-07-08_掩隐罪费曼稿/01_原始依据陈列_律师自用底稿.md"
```

- **事故规模**:`d56d926` commit 一次性打包 14 modified + 150 untracked + 6 顶层目录,49,231 行
- **立即回滚**:`git reset --hard HEAD~1`(30 秒内完成,数据 0 损失,用户事先说"掩隐罪费曼稿不处理")
- **教训**:跑任何能自动 commit 的脚本前,先确认 OP/动作名合法,不要凭"看起来无害"就试

## 最终方案(可复用 — 给所有 git 类自动脚本)

### 三件套原则(新增 git 类工具必遵循)

1. **动作名白名单** — case 验证输入,白名单外立即 exit 1,不进 git 操作
2. **dry-run 默认** — `./tool.sh <action> <vault>` 默认只 echo 不 commit,加 `--apply` 才真写
3. **非白名单拒执行** — 不接受任意字符串当动作名,不接受未识别 flag

### git_guard.sh 修复后用法

```bash
# 正确用法(白名单内 op)
bash git_guard.sh pre ingest /home/kangkang/tkk-library    # → OK pre-commit
bash git_guard.sh post query /home/kangkang/tkk-library "fix typo"  # → OK post-commit
bash git_guard.sh status /home/kangkang/tkk-library        # → === Git Status ===
bash git_guard.sh log /home/kangkang/tkk-library            # → === Git Guard Log ===
bash git_guard.sh rollback /home/kangkang/tkk-library      # → 回滚到上一 commit

# 错误用法(被白名单拒)
bash git_guard.sh pre test /home/kangkang/tkk-library      # → ERROR: invalid <op>: test
bash git_guard.sh pre "" /home/kangkang/tkk-library        # → ERROR: <op> required
bash git_guard.sh /home/kangkang/tkk-library               # → Usage: ... {pre|post|rollback|log|status}
```

## 关联

- AGENTS.md(Codex 端)硬规则索引表加 1 条 `feedback-tkk-git-guard-op-whitelist-2026-07-09.md`
- skills/tkk-legal-ingest/references/v69.1-REGRESSION.md(本文件 161 行版,完整事故复盘)
- skills/tkk-legal-ingest/tool/git_guard.sh(commit `b9271c3` 修)
- 兄弟规则:`feedback-tkk-rag-port-env-var-2026-07-03.md`(端口 env 变量,同类型"环境即配置"原则)

## 维护

- 创建日期:2026-07-09
- 触发场景:新增 git 类自动脚本 / 修改 git_guard / 排查误 commit
- 重要性:⭐⭐⭐(实测造成 190 文件误 commit,30 秒回滚无损失,但再发生可能没这么幸运)
