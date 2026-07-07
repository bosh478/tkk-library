# feedback-tkk-rag-port-8080-to-8081-2026-07-03

## 背景

`tkk-rag.service`(TKK Legal Ingest RAG Server, bge-m3 embedding + bge-reranker)长期占着 `8080` 端口,需要让出给其他程序(具体让给谁未明示)。**目标**:把 RAG 迁到 8081,永久稳定,不影响 tkk-legal-ingest skill 业务调用。

## 关键踩坑(给下次换端口的人)

### 坑 1:`server.py:161` 端口硬编码,unit 文件没显式 `--port`

- `tkk-rag.service` unit 文件 `ExecStart=` 只调 `python server.py`,没传 `--port` 参数
- 端口写死在 `server.py:161` 的 `uvicorn.run(app, host="0.0.0.0", port=8080)`
- **正确解法**:把 `server.py` 改成 `port=int(os.environ.get("RAG_PORT", "8080"))`,在 systemd unit 配 `Environment="RAG_PORT=8081"`,**以后换端口不动 .py**

### 坑 2:system 级 service 的 `Restart=always` 会"弹簧重启"

- 杀进程后 systemd 5 秒内自动拉起,跟我玩"按住弹簧"游戏
- 必须用 `sudo systemctl mask tkk-rag`(或手动 `ln -sf /dev/null /etc/systemd/system/tkk-rag.service`)让 unit 永久失效
- 单纯 `stop` 不够,`disable` 也不够 —— **`mask` 才是终极保险**

### 坑 3:user 级 service 不能跟 system 级 unit 同名

- 计划是把 tkk-rag 从 system 级迁到 user 级(`~/.config/systemd/user/`),跟 `minimax-shim` 同架构
- 但 mask system unit 报 `File already exists` —— 因为**同名 unit 在 system 侧,systemd 不允许 mask 覆盖非 symlink**
- **正确解法**:把 user 级 unit 改名 `tkk-rag.service → tkk-rag-user.service`,再 mask system 级即可

### 坑 4:exec_command 通道的 sudo 不通

- 在 exec 通道里跑 `sudo systemctl mask ...` 永远要密码(PTY 之外的 sudo 行为)
- 只能**用户在新 shell 跑一次密码**,后续系统级操作靠 `sudo -n` 验证
- **不依赖 sudo 的所有改 systemd 操作**都走 user 级:写到 `~/.config/systemd/user/`,权限内任意改

### 坑 5:`enable-linger` 让 user 级 service 在无登录态自启

- 默认 user 级 service 只在用户登录 session 时跑
- `sudo loginctl enable-linger kangkang` 让 user 级 service **开机就起来,无需登录**
- WSL2 重启场景:不配 linger = 8081 不起来,tkk-legal-ingest 业务废

## 最终方案(可复用)

### 1. 改 server.py:port 走环境变量

```python
# server.py:161
uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("RAG_PORT", "8080")))
```

### 2. 改 systemd unit:显式 `Environment="RAG_PORT=8081"`

```ini
[Service]
WorkingDirectory=/home/kangkang/rag
ExecStart=/home/kangkang/rag/.venv/bin/python /home/kangkang/rag/server.py
Environment="RAG_PORT=8081"
Environment="RAG_EMBED_MODEL_PATH=/home/kangkang/tkk-library/models/bge-m3"
Environment="RAG_RERANK_MODEL_PATH=/mnt/d/AI agent/rag/models/bge-reranker-v2-m3"
```

### 3. 迁到 user 级 service(`tkk-rag-user.service`)

- 路径:`~/.config/systemd/user/tkk-rag-user.service`
- 不依赖 sudo,改不需密码
- 跟 `minimax-shim` / `cdp-proxy` / `opencode-web` 同级

### 4. 关停 system 级(`sudo` 必走)

```bash
sudo systemctl disable --now tkk-rag      # 停+解自启
sudo ln -sf /dev/null /etc/systemd/system/tkk-rag.service  # mask 终极保险
sudo systemctl daemon-reload
sudo rm /etc/systemd/system/tkk-rag.service.bak-8080        # 清理备份
```

### 5. enable-linger(防止重启 WSL 后 8081 不起)

```bash
sudo loginctl enable-linger kangkang
```

### 6. 改客户端硬编码(本机所有指向 8080 的工具/文档)

| 文件 | 改法 |
|---|---|
| `~/.codex-staging/skills/tkk-legal-ingest/tool/query_router.py:544, 629` | `f"http://localhost:{os.environ.get('RAG_PORT','8080')}/v1/rerank"` |
| `~/.codex-staging/skills/tkk-legal-ingest/references/query-workflow.md:129,130` | `${RAG_PORT:-8080}` 兜底语法 |
| `~/.codex-staging/skills/tkk-legal-ingest/SKILL.md:25` | `${RAG_PORT:-8080}` 兜底语法 |

> **设计原则**:客户端**不**强依赖 8080 特定端口,读 env 变量 + 默认值兜底 → 以后再换 8082 改 unit 即可,客户端无需动。

## 验证清单

| 项 | 验证命令 | 预期 |
|---|---|---|
| 8080 释放 | `ss -tlnp \| grep :8080` | 空 |
| 8081 在跑 | `ss -tlnp \| grep :8081` | `python` LISTEN |
| user service active | `systemctl --user status tkk-rag-user` | `active (running)` |
| system unit masked | `ls -l /etc/systemd/system/tkk-rag.service` | `→ /dev/null` |
| linger 生效 | `loginctl show-user kangkang \| grep Linger` | `Linger=yes` |
| 业务端点 | `curl http://127.0.0.1:8081/v1/health` | `{"ok":true,...}` |
| rerank 端点 | `curl -X POST http://127.0.0.1:8081/v1/rerank -d '{...}'` | `{"results":[{...}]}` |
| embedding 端点 | `curl -X POST http://127.0.0.1:8081/v1/embeddings -d '{...}'` | 1024 维向量 |

## 关联

- AGENTS.md §4.2(minimax-shim 架构,可类比)
- skills/tkk-legal-ingest/SKILL.md 启动自检 3 项里的 `curl -s -m 2 http://localhost:8080/v1/health` 现已升级为 `${RAG_PORT:-8080}`
- system unit 旧 unit 已 mask → /dev/null,留个 .bak 备份在 system 侧(`/etc/systemd/system/tkk-rag.service.bak-8080` ← 需 sudo 删)

## 创建信息

- 创建日期:2026-07-03
- 创建原因:把 8080 让出 + 修服务端硬编码 + 同步 3 处客户端引用
- 维护策略:本文件是一次性变更记录,完成即归档,后续如要再换端口(8082/8083)走"最终方案"那 6 步即可
