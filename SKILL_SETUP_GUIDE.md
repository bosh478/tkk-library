# tkk-legal-ingest Skill 完整搭建指南

> **目标读者**：零基础用户  
> **目标结果**：在新 Windows 11 电脑上完整搭建 `tkk-legal-ingest` skill 的运行环境（依赖、模型、配置），能被 Claude Code 正常调用并跑通最小流程。  
> **不包含**：Wiki 知识库内容、sources/ 原始资料、批量数据 ingest。

---

## 0. 写在前面

### 0.1 你需要准备的硬件

| 项目 | 最低要求 | 推荐 | 说明 |
|------|----------|------|------|
| 系统 | Windows 11 (64-bit) | Windows 11 Pro | 必须 Windows，macOS/Linux 不在本文档范围 |
| CPU | 4 核 | 8 核+ | rerank 模型加载阶段会吃 CPU |
| 内存 | 16 GB | 32 GB | 模型加载后常驻 ~3 GB |
| GPU | 可选 | NVIDIA 显卡（≥4GB 显存） | rerank 模型可走 CUDA（快）或 CPU（慢） |
| 磁盘 | 30 GB 可用 | 50 GB+ | 模型 + Python 环境 + Skill 文件 + 后续 Wiki 缓存 |
| 网络 | 可访问 GitHub + Hugging Face | 稳定宽带 | 下载模型和 skill 源码 |

> ⚠️ **GPU 不是必需的**：没有 NVIDIA 显卡也能跑，rerank 会自动用 CPU，只是首次响应会慢 5–10 秒。

### 0.2 整体流程图

```
┌──────────────────────────────────────────────────────────┐
│  Step 1: 环境前置 (操作系统/账号)                         │
│     ↓                                                     │
│  Step 2: 基础工具安装 (Claude Code / Python / Git)         │
│     ↓                                                     │
│  Step 3: 模型栈部署 (Ollama + bge-m3, Rerank + bge-reranker)│
│     ↓                                                     │
│  Step 4: qmd CLI 安装与索引                                │
│     ↓                                                     │
│  Step 5: Skill 安装 (克隆 tkk-skills 仓库)                 │
│     ↓                                                     │
│  Step 6: 端到端验证 (Smoke Test)                           │
└──────────────────────────────────────────────────────────┘
```

预计总耗时：**1.5–2.5 小时**（含模型下载，30–60 分钟主要花在 Hugging Face 模型拉取）。

---

## 1. 环境前置

### 1.1 操作系统确认

- 右键「此电脑」→「属性」，确认是 **Windows 11 64-bit**
- 家庭版/专业版均可，不影响 skill 运行

### 1.2 工作目录规划

> ⚠️ **路径里有空格会带来一系列坑**。本指南假设你使用 `~/tkk-library\` 作为根目录（与原作者一致）。如果你改用其他目录，把文中所有 `~/tkk-library\` 替换为你的路径即可。

推荐目录结构：

```
~/tkk-library\           ← vault 根目录
├── .claude\
│   └── skills\                     ← Claude Code skill 安装位置
├── models\                         ← 大模型本地缓存
│   └── bge-reranker-v2-m3\
├── rerank_venv\                    ← Python 虚拟环境（rerank 服务用）
├── scripts\                        ← 启动脚本、健康检查、rerank_server.py
├── logs\                           ← 启动/运行日志
├── sources\                        ← (可选)后续放原始资料
└── wiki\                           ← (可选)后续放知识库页
```

**先创建空骨架**（PowerShell 中执行）：

```powershell
New-Item -ItemType Directory -Force "~/tkk-library\.claude\skills"
New-Item -ItemType Directory -Force "~/tkk-library\models"
New-Item -ItemType Directory -Force "~/tkk-library\rerank_venv"
New-Item -ItemType Directory -Force "~/tkk-library\scripts"
New-Item -ItemType Directory -Force "~/tkk-library\logs"
```

### 1.3 网络确认

打开 PowerShell 试一下：

```powershell
Test-NetConnection github.com -Port 443
Test-NetConnection huggingface.co -Port 443
```

两个都应返回 `TcpTestSucceeded: True`。如果失败：

- 检查是否需要代理（公司网络常见）
- 检查 DNS：`nslookup github.com`

---

## 2. 基础工具安装

### 2.1 Claude Code CLI

**用途**：运行本 skill 的宿主环境。

**安装**：

```powershell
# 需要 Node.js 18+（如未装，先去 https://nodejs.org 下载 LTS 版）
npm install -g @anthropic-ai/claude-code
```

**验证**：

```powershell
claude --version
```

**登录**（首次使用）：

```powershell
claude login
```

按提示在浏览器中完成授权。

> ⚠️ **路径带空格的坑**：Claude Code 默认会扫描 `~/.claude/skills/`，但 Windows 的 `%USERPROFILE%` 通常是 `C:\Users\<用户名>`，**没有空格**，没问题。但项目工作目录有空格（如本指南的 `D:\AI agent\`）时，部分 npm 工具可能报错——遇到再单独处理。

### 2.2 Python 3.11+

**用途**：运行 rerank_server.py。

**安装**：

1. 访问 https://www.python.org/downloads/
2. 下载 **Python 3.11.x 或 3.12.x**（避开 3.13+，部分依赖如 `sentence-transformers` 可能不稳）
3. 安装时**勾选** `Add Python to PATH`（默认未勾，这是最大坑）

**验证**：

```powershell
python --version
pip --version
```

> ⚠️ **PATH 没生效？** 关闭并重开 PowerShell 窗口。Windows 安装器只修改当前 PATH，要新终端才生效。

### 2.3 Git

**用途**：克隆 skill 仓库。

**安装**：访问 https://git-scm.com/download/win，下载 64-bit 安装包，全部默认选项即可。

**验证**：

```powershell
git --version
```

### 2.4 curl

Windows 10/11 自带。验证：

```powershell
curl --version
```

若提示找不到，去 https://curl.se/windows/ 下载。

### 2.5 Obsidian（可选）

**用途**：浏览 Wiki（如果后续要消费 skill 产物）。

**安装**：https://obsidian.md/download

---

## 3. 模型栈部署

### 3.1 Ollama 安装 + bge-m3（Embedding 模型）

**bge-m3** 用于把文本转为向量（embedding）。模型大小约 **1.2 GB**。

#### 3.1.1 安装 Ollama

1. 访问 https://ollama.com/download/windows
2. 下载 `OllamaSetup.exe`
3. 默认安装到 `C:\Users\<你>\AppData\Local\Programs\Ollama\`
4. 安装完**手动启动一次**（开始菜单搜 `Ollama`），让它跑在后台

> ⚠️ **Ollama 默认不开机自启**。需要时手动启动，或参照第六章做开机自启。

#### 3.1.2 验证 Ollama

```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" --version
```

或 PATH 已生效：

```powershell
ollama --version
```

#### 3.1.3 拉取 bge-m3 模型

```powershell
ollama pull bge-m3
```

预期：

```
pulling manifest...
pulling [SHA256]...
pulling [SHA256]...
verifying sha256 digest
writing manifest
removing any unused layers
success
```

耗时：10–30 分钟（取决于网速）。

#### 3.1.4 启动 Ollama 服务

```powershell
ollama serve
```

预期输出：

```
Ollama server listening on 127.0.0.1:11434
```

> ⚠️ **必须保持这个窗口不关闭**，或让它在后台运行（推荐方式见第六章）。

#### 3.1.5 验证 embedding

另开一个 PowerShell：

```powershell
curl http://localhost:11434/api/tags
```

预期返回 JSON，`models[0].name == "bge-m3:latest"`。

**端到端测试**：

```powershell
curl -X POST http://localhost:11434/api/embeddings -H "Content-Type: application/json" -d '{\"model\":\"bge-m3\",\"prompt\":\"测试文本\"}'
```

应返回含 `"embedding":[...]` 的 JSON。

---

### 3.2 Rerank 服务（rerank_server.py）

**bge-reranker-v2-m3** 用于对召回结果重排序，显著提升检索质量。模型大小约 **2.2 GB**。

#### 3.2.1 创建 Python 虚拟环境

```powershell
cd "~/tkk-library"
python -m venv rerank_venv
```

#### 3.2.2 安装依赖

```powershell
& "~/tkk-library\rerank_venv\Scripts\pip.exe" install --upgrade pip
& "~/tkk-library\rerank_venv\Scripts\pip.exe" install torch transformers sentence-transformers fastapi uvicorn pydantic
```

预期耗时：5–15 分钟（torch 约 800 MB，是大头）。

> ⚠️ **CUDA 还是 CPU？**
> - 如果你有 NVIDIA 显卡且装了 CUDA Toolkit → `pip install torch` 会自动拉 CUDA 版（默认行为，但若网络不通会失败）
> - 如果你没显卡 → `pip install torch` 会拉 CPU 版（2 GB+，够用）
> - 验证：`python -c "import torch; print(torch.cuda.is_available())"` → `True` = 有 GPU，`False` = CPU only

#### 3.2.3 下载 bge-reranker-v2-m3 模型

模型来源：https://huggingface.co/BAAI/bge-reranker-v2-m3

需要下载的 5 个文件，全部放到 `~/tkk-library\models\bge-reranker-v2-m3\`：

| 文件 | 大小 | 说明 |
|------|------|------|
| `config.json` | 几 KB | 模型架构配置 |
| `model.safetensors` | ~2.1 GB | 权重 |
| `tokenizer.json` | ~10 MB | 分词器 |
| `tokenizer_config.json` | 几 KB | 分词器配置 |
| `special_tokens_map.json` | 几 KB | 特殊 token 映射 |

**方式 A（推荐）：用 huggingface-cli**

```powershell
& "~/tkk-library\rerank_venv\Scripts\pip.exe" install huggingface_hub
$env:HF_HUB_ENABLE_HF_TRANSFER = "1"
& "~/tkk-library\rerank_venv\Scripts\huggingface-cli.exe" download BAAI/bge-reranker-v2-m3 --local-dir "~/tkk-library\models\bge-reranker-v2-m3"
```

**方式 B：手动下载**

到 https://huggingface.co/BAAI/bge-reranker-v2-m3/tree/main ，逐个下载上述 5 个文件，扔进 `~/tkk-library\models\bge-reranker-v2-m3\`。

**验证**：

```powershell
Get-ChildItem "~/tkk-library\models\bge-reranker-v2-m3"
```

应看到 5 个文件，总计约 2.2 GB。

#### 3.2.4 部署 rerank_server.py

`rerank_server.py` 是 skill 自带的服务脚本。把 tkk-skills 仓库的 `scripts/rerank_server.py`（或仓库根的同名文件）复制到 `~/tkk-library\scripts\`。

> **路径常量在脚本顶部**：
> ```python
> MODEL_PATH = r"~/tkk-library\models\bge-reranker-v2-m3"
> ```
> 如果你的根目录不是这个，**改这一行**。

#### 3.2.5 启动 rerank 服务

```powershell
& "~/tkk-library\rerank_venv\Scripts\python.exe" "~/tkk-library\scripts\rerank_server.py"
```

预期输出（首次启动要加载模型，**慢 30–90 秒**是正常的）：

```
[start] BGE Reranker 服务 | 监听 0.0.0.0:8080
[load] 加载模型: ~/tkk-library\models\bge-reranker-v2-m3
[load] 设备: CUDA, dtype: torch.float16
[load] 模型加载完成 | device=cuda | GPU mem=1.14GB
INFO:     Uvicorn running on http://0.0.0.0:8080
```

> ⚠️ **必须保持这个窗口不关闭**。

#### 3.2.6 验证 rerank 服务

另开 PowerShell：

```powershell
curl http://localhost:8080/health
```

预期返回：

```json
{"status":"ok","model":"BAAI/bge-reranker-v2-m3","device":"cuda","gpu_mem_gb":1.14}
```

**端到端测试**：

```powershell
curl -X POST http://localhost:8080/rerank -H "Content-Type: application/json" -d '{\"model\":\"BAAI/bge-reranker-v2-m3\",\"query\":\"故意杀人\",\"documents\":[\"张三故意杀人被判处死刑\",\"李四盗窃公私财物\"],\"top_n\":2}'
```

应返回带 `relevance_score` 排序的 JSON。

---

## 4. qmd CLI 安装与索引

**qmd** 是本 skill 依赖的本地全文/向量混合检索工具。

### 4.1 安装 qmd

```powershell
npm install -g qmd
```

> ⚠️ **npm 全局安装目录默认在 `%APPDATA%\npm\`**（Windows）。如果安装完 `qmd` 命令找不到，说明 PATH 没生效，**关闭重开 PowerShell**。

### 4.2 验证

```powershell
qmd --version
```

预期：`qmd 2.1.0`（或更新版本）。

### 4.3 初始化 collection

```powershell
qmd collection add "~/tkk-library" --name vault
```

> **collection 名是什么**：是 qmd 给你的 vault 目录起的"别名"。Skill 默认期望叫 `vault`，所以**必须用 `--name vault`**。

### 4.4 验证索引

```powershell
qmd query "故意杀人" --collection vault --limit 5
```

首次跑会触发索引（看 vault 大小，30 秒 – 数分钟）。预期返回命中列表。

> ⚠️ **qmd 索引会扫描所有 Markdown 文件**。如果你的 vault 里已经有几万文件，索引耗时会很长。本指南假设是全新空 vault，首次索引几秒即可。

---

## 5. Skill 安装

### 5.1 克隆 tkk-skills 仓库

```powershell
cd "~/tkk-library"
git clone https://github.com/bosh478/tkk-skills.git _repo_tkk-skills
```

预期：在 vault 根下出现 `_repo_tkk-skills/` 目录。

> **为什么叫 `_repo_` 前缀**：下划线开头让 Obsidian 等工具把它当成"非笔记目录"忽略，避免 skill 源码污染 Wiki 浏览。

### 5.2 把 tkk-legal-ingest 放到 skill 目录

skill 的"激活位置"是 Claude Code 启动时扫描的 `~/.claude/skills/`：

```powershell
# Windows 下 ~/.claude/ 等价于 %USERPROFILE%\.claude\
$skillsRoot = "$env:USERPROFILE\.claude\skills"
if (-not (Test-Path $skillsRoot)) { New-Item -ItemType Directory -Force -Path $skillsRoot | Out-Null }

# 链接 tkk-legal-ingest（推荐方式）
New-Item -ItemType Junction -Path "$skillsRoot\tkk-legal-ingest" -Target "~/tkk-library\_repo_tkk-skills\tkk-legal-ingest"
```

> ⚠️ **Junction（目录联接）vs 复制？**
> - **Junction（推荐）**：用 `New-Item -ItemType Junction`。原仓库更新后，`git pull` 一次，skill 同步生效。
> - **复制**：如果不懂 junction，直接 `Copy-Item -Recurse` 也行，但要记得后续手动同步更新。

### 5.3 验证 Skill 被识别

启动 Claude Code：

```powershell
claude
```

在交互界面输入：

```
/tkk-legal-ingest
```

如果 Claude 显示出 skill 的描述（按 `SKILL.md` 中的 description 字段），说明安装成功。

> ⚠️ **常见失败**：
> - `/` 命令列表里看不到 skill → 检查 junction 路径是否有误
> - 看到 skill 但报 YAML 解析错误 → skill 内的 `SKILL.md` YAML frontmatter 格式损坏，去仓库 issues 报
> - 完全没响应 → 重启 Claude Code 进程

### 5.4 其他相关 Skill（按需）

原仓库里通常还有其他 skill（如 `tkk-legal-review`、`tkk-legal-deep-research` 等），它们都按同样方式安装：

```powershell
New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\skills\tkk-legal-review" -Target "~/tkk-library\_repo_tkk-skills\tkk-legal-review"
# 重复其他 skill...
```

---

## 6. 端到端 Smoke Test

目的：验证 4 件事能同时跑通——Ollama、rerank_server、qmd、Claude Code skill 加载。

### 6.1 启动 stack

**方式 A：手动逐个启动**

3 个窗口分别执行：

```powershell
# 窗口1
ollama serve
```

```powershell
# 窗口2
& "~/tkk-library\rerank_venv\Scripts\python.exe" "~/tkk-library\scripts\rerank_server.py"
```

```powershell
# 窗口3（qmd 是按需触发，无需常驻）
# 不需要预先启动
```

**方式 B：写一个一键启动脚本（推荐）**

保存以下内容为 `~/tkk-library\scripts\one_click_start.bat`：

```batch
@echo off
setlocal

set "PYTHON_VENV=~/tkk-library\rerank_venv\Scripts\python.exe"
set "OLLAMA=%LOCALAPPDATA%\Programs\Ollama\ollama.exe"
set "SCRIPT_DIR=~/tkk-library\scripts"

REM 检查 Ollama
netstat -an | findstr ":11434.*LISTENING" >nul 2>&1
if errorlevel 1 (
    echo [start] starting ollama...
    start "ollama" /B "%OLLAMA%" serve
) else (
    echo [skip] ollama already running
)

REM 检查 rerank
netstat -an | findstr ":8080.*LISTENING" >nul 2>&1
if errorlevel 1 (
    echo [start] starting rerank_server...
    start "rerank_server" /B "%PYTHON_VENV%" "%SCRIPT_DIR%\rerank_server.py"
) else (
    echo [skip] rerank_server already running
)

echo.
echo Wait 30s for rerank model to load...
timeout /t 30 /nobreak >nul

echo.
echo Verifying:
curl -s http://localhost:11434/api/tags | findstr "bge-m3" && echo [OK] ollama || echo [FAIL] ollama
curl -s http://localhost:8080/health | findstr "ok" && echo [OK] rerank || echo [FAIL] rerank
qmd collection list 2>nul | findstr "vault" && echo [OK] qmd || echo [FAIL] qmd

echo Done.
pause
```

双击运行即可。预期看到 3 个 `[OK]`。

### 6.2 验证 qmd + Claude 协同

```powershell
# 在 vault 里放一个测试文件
@"
故意杀人罪是指故意非法剥夺他人生命的行为。
盗窃罪是指以非法占有为目的，窃取公私财物的行为。
"@ | Out-File -Encoding utf8 "~/tkk-library\sources\test.md"

# 重建索引
qmd collection rebuild vault

# 启动 Claude Code
claude
```

在 Claude 中说：

```
请用 qmd 检索 "故意杀人" 相关内容
```

Claude 应该会调用 qmd 工具返回结果。

### 6.3 验证 Skill 可触发

在 Claude Code 中：

```
/tkk-legal-ingest 帮我看看有什么可以做的
```

预期 Claude 加载 skill 描述并给出引导。

---

## 7. 故障排查速查表

### 7.1 端口冲突

| 端口 | 占用者 | 解决 |
|------|--------|------|
| 11434 | Ollama | `netstat -ano | findstr :11434`，找到 PID 后 `taskkill /F /PID <pid>` |
| 8080 | 其他服务 | 修改 `rerank_server.py` 顶部的 `PORT = 8080` 为其他端口 |

### 7.2 模型加载失败

```
OSError: [Errno 22] Invalid argument
或
FileNotFoundError: model.safetensors
```

→ 检查 5 个文件是否齐全，路径是否完全匹配 `MODEL_PATH` 变量。

### 7.3 CUDA 不可用

```
torch.cuda.is_available() == False
```

→ 正常，会自动用 CPU。但首次 rerank 会慢 5–10 秒。如果想用 GPU：

1. 装 NVIDIA 显卡驱动
2. 装匹配版本的 CUDA Toolkit
3. `pip uninstall torch && pip install torch --index-url https://download.pytorch.org/whl/cu121`（以 cu12.1 为例）

### 7.4 qmd 索引失败

```
Error: collection 'vault' not found
```

→ 重新执行 `qmd collection add "~/tkk-library" --name vault`

### 7.5 Skill 不被 Claude 识别

1. 确认 junction 已创建：`dir "$env:USERPROFILE\.claude\skills\tkk-legal-ingest"` 应能看到内容
2. 重启 Claude Code（关掉再开）
3. 看 Claude 的报错信息——通常会指出哪个 SKILL.md 解析失败

### 7.6 PowerShell 与 cmd 编码错乱

> ⚠️ 这是 Windows 中文用户最高频的坑。

症状：脚本里的中文 echo 显示成乱码，且命令解析错位（如 `'戳' is not recognized`）。

根因：PowerShell 默认 ANSI 编码（GBK），`.bat` 文件默认无 BOM 被 cmd 当 ANSI 解析。

**解决**：
- `.bat` 文件中**只用 ASCII**，不要写中文 echo（用 `[OK]` `[FAIL]` 这类英文标签）
- 在 PowerShell 调用 `.bat` 前加一行：`chcp 65001 | Out-Null`
- 或者用 PowerShell 脚本（`.ps1`）替代 `.bat`

### 7.7 路径有空格导致命令失败

症状：

```
'D:\AI' is not recognized as an internal or external command
```

→ 任何引用路径的地方**全程加双引号**：

```powershell
& "~/tkk-library\rerank_venv\Scripts\python.exe" "~/tkk-library\scripts\rerank_server.py"
```

---

## 8. 升级与维护

### 8.1 Skill 升级

```powershell
cd "~/tkk-library\_repo_tkk-skills"
git pull
```

因为用的是 junction（不是复制），pull 一次即可同步到 `~/.claude/skills/`。

### 8.2 模型升级

```powershell
# Ollama 模型
ollama pull bge-m3

# Rerank 模型
& "~/tkk-library\rerank_venv\Scripts\huggingface-cli.exe" download BAAI/bge-reranker-v2-m3 --local-dir "~/tkk-library\models\bge-reranker-v2-m3"
```

### 8.3 备份清单

定期备份以下内容即可保留完整运行环境（**不包含 Wiki 内容**）：

```
~/tkk-library\
├── .claude\settings*        ← Claude Code 本地配置
├── _repo_tkk-skills\.git\   ← skill 源码（git 仓库自管）
├── rerank_venv\             ← 可选（pip freeze + requirements.txt 重建更省空间）
└── scripts\rerank_server.py ← 1 个文件
```

---

## 9. 全流程验证清单

> 逐项打勾。每个项目都给出 **命令 → 期望输出 → 成功标志**，照着对即可。
>
> 验证失败时跳到第 7 章排查。

### 9.1 环境前置验证

| # | 验证项 | 命令 | 期望输出 | 成功标志 |
|---|--------|------|----------|----------|
| 1 | Windows 版本 | `Win+R` → 输入 `winver` 回车 | 弹窗显示 "Windows 11" + 版本号 | 版本号 ≥ 22000 |
| 2 | 网络通 GitHub | `Test-NetConnection github.com -Port 443` | `TcpTestSucceeded: True` | True |
| 3 | 网络通 HuggingFace | `Test-NetConnection huggingface.co -Port 443` | `TcpTestSucceeded: True` | True |
| 4 | 工作目录可写 | `Test-Path "~/tkk-library"` | `True` | True |

### 9.2 基础工具验证

| # | 工具 | 命令 | 期望输出 | 成功标志 |
|---|------|------|----------|----------|
| 5 | Claude Code | `claude --version` | 类似 `claude-code 1.x.x` | 输出含版本号 |
| 6 | Python | `python --version` | `Python 3.11.x` 或 `3.12.x` | 3.11+ |
| 7 | pip | `pip --version` | `pip 2x.x from ...python3.11` | pip 可执行 |
| 8 | Git | `git --version` | `git version 2.x.x` | 2.x+ |
| 9 | curl | `curl --version` | 多行输出，首行含 `curl 8.x.x` | 任意 7.x+ |
| 10 | npm | `npm --version` | `10.x.x` | 9+（装 Claude Code 用） |
| 11 | qmd | `qmd --version` | `qmd 2.1.0` 或更新 | 2.0+ |

**小技巧**：把这 7 个命令串成一行一次性验证：

```powershell
claude --version; python --version; git --version; curl --version | Select-Object -First 1; npm --version; qmd --version
```

应看到 6 行非空输出。

### 9.3 Ollama + bge-m3 验证

| # | 验证项 | 命令 | 期望输出 | 成功标志 |
|---|--------|------|----------|----------|
| 12 | Ollama 可执行 | `& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" --version` | `ollama version 0.x.x` | 输出版本号 |
| 13 | Ollama 进程运行 | `Get-Process ollama -ErrorAction SilentlyContinue` | 表格含 ollama 进程 | 至少 1 个进程 |
| 14 | 端口 11434 监听 | `netstat -an \| Select-String ":11434.*LISTENING"` | `TCP    127.0.0.1:11434 ... LISTENING` | 含 LISTENING |
| 15 | bge-m3 模型已拉取 | `curl http://localhost:11434/api/tags` | JSON 含 `"name":"bge-m3:latest"` | models 数组非空 |
| 16 | Embedding 端到端 | `curl -X POST http://localhost:11434/api/embeddings -H "Content-Type: application/json" -d '{\"model\":\"bge-m3\",\"prompt\":\"测试\"}'` | JSON 含 `"embedding":[0.1,0.2,...]` | 数组长度 = 1024 |

**端到端命令的"成功的样子"**（截取关键片段）：

```json
{
  "model": "bge-m3",
  "embedding": [
    0.0123, -0.0456, 0.0789, ...
    // 总共 1024 个浮点数
  ],
  "total_duration": 12345678
}
```

### 9.4 Rerank 服务验证

| # | 验证项 | 命令 | 期望输出 | 成功标志 |
|---|--------|------|----------|----------|
| 17 | venv 存在 | `Test-Path "~/tkk-library\rerank_venv\Scripts\python.exe"` | `True` | True |
| 18 | 依赖已装 | `& "~/tkk-library\rerank_venv\Scripts\pip.exe" list \| Select-String "torch\|fastapi\|transformers"` | 3 行 | 3 个包都在 |
| 19 | 模型文件齐全 | `Get-ChildItem "~/tkk-library\models\bge-reranker-v2-m3"` | 5 个文件 | 见下表 |
| 20 | 模型大小正确 | `(Get-ChildItem "~/tkk-library\models\bge-reranker-v2-m3" -Recurse \| Measure-Object Length -Sum).Sum / 1GB` | 约 `2.2` | 1.8 ~ 2.5 GB |
| 21 | rerank_server.py 在位 | `Test-Path "~/tkk-library\scripts\rerank_server.py"` | `True` | True |
| 22 | rerank 进程运行 | `Get-Process python -ErrorAction SilentlyContinue \| Where-Object { $_.MainModule.FileName -like "*rerank_venv*" }` | 1 个 python 进程 | PID 存在 |
| 23 | 端口 8080 监听 | `netstat -an \| Select-String ":8080.*LISTENING"` | `TCP    0.0.0.0:8080 ... LISTENING` | LISTENING |
| 24 | /health 端点 | `curl http://localhost:8080/health` | `{"status":"ok","model":"BAAI/bge-reranker-v2-m3","device":"cuda","gpu_mem_gb":1.14}` | status=ok |
| 25 | /rerank 端到端 | 见下方命令 | 见下方 JSON | relevance_score 在 [0,1] |

**第 19 项必备文件清单**：

| 文件 | 大小 | 必须存在 |
|------|------|----------|
| `config.json` | ~1 KB | ✓ |
| `model.safetensors` | ~2.1 GB | ✓ |
| `tokenizer.json` | ~10 MB | ✓ |
| `tokenizer_config.json` | ~1 KB | ✓ |
| `special_tokens_map.json` | ~1 KB | ✓ |

**第 25 项端到端测试命令**：

```powershell
curl -X POST http://localhost:8080/rerank `
  -H "Content-Type: application/json" `
  -d '{"model":"BAAI/bge-reranker-v2-m3","query":"故意杀人","documents":["张三故意杀人被判处死刑","李四盗窃公私财物"],"top_n":2}'
```

**期望返回**（关键字段）：

```json
{
  "results": [
    {
      "index": 0,
      "relevance_score": 0.987,    ← 故意杀人相关，最高分
      "document": "张三故意杀人被判处死刑"
    },
    {
      "index": 1,
      "relevance_score": 0.012,    ← 盗窃，不相关，低分
      "document": "李四盗窃公私财物"
    }
  ]
}
```

**成功标志**：第 0 个文档的 `relevance_score` 明显高于第 1 个（差值 > 0.5）。

### 9.5 qmd 验证

| # | 验证项 | 命令 | 期望输出 | 成功标志 |
|---|--------|------|----------|----------|
| 26 | qmd 可执行 | `qmd --version` | `qmd 2.1.0` | 2.0+ |
| 27 | vault collection 存在 | `qmd collection list` | 表格含 `vault` | vault 行存在 |
| 28 | qmd 检索返回 | `qmd query "test" --collection vault --limit 3` | JSON 数组 | 非空数组 |

**第 27 项成功的样子**：

```
NAME    PATH                            INDEXED  FILES
vault   ~/tkk-library        yes      N
```

（N 是已索引文件数，首次建索引时可能为 0，需要等几分钟）

### 9.6 Skill 安装验证

| # | 验证项 | 命令 | 期望输出 | 成功标志 |
|---|--------|------|----------|----------|
| 29 | junction 存在 | `Get-Item "$env:USERPROFILE\.claude\skills\tkk-legal-ingest"` | DirectoryInfo（带 Target 字段） | LinkType=Junction |
| 30 | SKILL.md 可读 | `Test-Path "$env:USERPROFILE\.claude\skills\tkk-legal-ingest\SKILL.md"` | `True` | True |
| 31 | Claude 能识别 | 启动 `claude` 后输入 `/tkk` | 自动补全出 `tkk-legal-ingest` | 出现在列表 |

**第 31 项成功的样子**（Claude Code 提示）：

```
> /tkk
> /tkk-legal-ingest       [loaded]
> /tkk-legal-review
> /tkk-legal-deep-research
> ...
```

`[loaded]` 标记说明 skill 已被加载并可用。

### 9.7 端到端 Smoke Test（最终）

按顺序运行，每步必须成功才能进入下一步：

```
[ ] 9.7.1  启动 stack（双击 one_click_start.bat 或手动）
        ↓ 期望：3 个 [OK]
        ↓
[ ] 9.7.2  ollama tags       → 见 bge-m3
        ↓
[ ] 9.7.3  rerank /health    → status:ok
        ↓
[ ] 9.7.4  rerank 端到端     → relevance_score 排序正确
        ↓
[ ] 9.7.5  qmd collection    → 含 vault
        ↓
[ ] 9.7.6  claude            → 启动成功
        ↓
[ ] 9.7.7  /tkk-legal-ingest → 出现在 skill 列表
        ↓
[ ] 9.7.8  qmd query 测试    → 返回命中结果
        ↓
[✓] 全部通过 = Skill 完全可用
```

### 9.8 验证失败的快速诊断流程

```
任意验证失败
  ↓
看 netstat 输出：11434 / 8080 是否在 LISTENING？
  ├─ 都没监听 → 服务没启动，去看第 6 章启动 stack
  ├─ 只有一个 → 看第 7.1 节端口冲突
  └─ 都在 → 看具体哪个 API 报错
            ↓
看 API 报错内容
  ├─ "model not loaded" → 等 30 秒，模型还在加载
  ├─ "ECONNREFUSED"     → 服务没起来，重启
  ├─ "FileNotFoundError" → 模型文件不全，看 9.4 第 19 项
  └─ 其他 → 看第 7 章故障排查
```

---

## 10. 一页流程速查

```powershell
# ====== 一次性安装（按顺序） ======

# 1) 工具（按 2.x 节）
npm install -g @anthropic-ai/claude-code
# Python 3.11+, Git, curl 走官网
npm install -g qmd

# 2) Ollama + bge-m3
# 装 OllamaSetup.exe
ollama pull bge-m3

# 3) Rerank
python -m venv ~/tkk-library\rerank_venv
~/tkk-library\rerank_venv\Scripts\pip.exe install torch transformers sentence-transformers fastapi uvicorn pydantic
~/tkk-library\rerank_venv\Scripts\huggingface-cli.exe download BAAI/bge-reranker-v2-m3 --local-dir "~/tkk-library\models\bge-reranker-v2-m3"

# 4) Skill
git clone https://github.com/bosh478/tkk-skills.git "~/tkk-library\_repo_tkk-skills"
New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\skills\tkk-legal-ingest" -Target "~/tkk-library\_repo_tkk-skills\tkk-legal-ingest"

# 5) qmd 索引
qmd collection add "~/tkk-library" --name vault

# ====== 每次开机启动 ======

# 方式 A: 手动 3 个窗口
ollama serve
& "~/tkk-library\rerank_venv\Scripts\python.exe" "~/tkk-library\scripts\rerank_server.py"

# 方式 B: 一键脚本（按 6.1 节 one_click_start.bat）

# ====== 验证 ======

curl http://localhost:11434/api/tags        # 应见 bge-m3
curl http://localhost:8080/health           # 应见 status:ok
qmd query "测试" --collection vault         # 应见命中
claude                                      # 启动 Claude Code
# 在 Claude 中输入 /tkk-legal-ingest        # 应见 skill 描述
```

---

**版本**：v1  
**适用 skill**：`tkk-legal-ingest` (tkk-skills repo, main 分支)  
**验证日期**：2026-06-10