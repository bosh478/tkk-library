# tkk-library/scripts · E2E 文章捕获到 wiki 工具集

> 把网络文章（命中 wiki 知识库缺口）自动捕获到 `sources/discovered-in-research/<task_id>/`,
> 供 `tkk-legal-ingest` v67 后续入库。

**主路径设计哲学**（per `feedback-no-design-degradation-2026-06-22`）：
- 不预埋 urllib / 标准库降级
- 缺依赖 / CDP 不通 → loudly 报错 + 修复指引,不静默降级
- 失败 exit 码非 0 + stderr 含修复步骤

---

## 3 个脚本

### 1. `html2md.py` — HTML → Markdown 转换器

**主路径依赖**：`markdownify`（pip）+ `beautifulsoup4` + `soupsieve`

```bash
# 安装(per .gitignore 习惯,WSL 用 --break-system-packages)
pip install --break-system-packages markdownify
```

**CLI**：
```bash
# 文件 → 文件
python html2md.py input.html -o output.md

# 加 frontmatter(--meta 可多次)
python html2md.py input.html -o output.md \
  --meta title="标题" \
  --meta author="作者" \
  --meta tier=T1

# 从 stdin
cat article.html | python html2md.py -o output.md
```

**自动剥除**：`script` / `style` / `nav` / `footer` / `aside` / `noscript` / `iframe` / `form` / `button` / `input` 等（用 `--keep-all-tags` 关闭）

**错误处理**：
- 缺 markdownify → exit 2 + 提示 `pip install --break-system-packages markdownify`
- 输入为空 → exit 1
- --meta 格式错 → exit 1

### 2. `markdown_converter.py` — 写入 discovered-in-research/ 工具（已存在）

**职责**：接受**已转 markdown 的**正文 + 元数据 → 加 schema frontmatter → 写入 `SRC-NNN__标题.md` + 增量更新 `INDEX.md` + `research_log.md`

**重要**：本脚本**不做 HTML→MD 转换**。`html2md.py` 负责转换,本脚本负责写入。

### 3. `ingest_web_to_research.py` — E2E orchestrator

**主路径**：web-access/CDP (主) → `html2md.py` (主) → `markdown_converter.py` (主)

**前置**：CDP Proxy 跑在 localhost:3456
```bash
# 1. Chrome 开 remote-debugging
# 2. 启动 CDP Proxy
node ~/.claude/skills/web-access/scripts/cdp-proxy.mjs &
# 3. 验证
curl -s http://localhost:3456/health
```

**CLI 模式 1**（主路径 · 通过 web-access/CDP 抓 URL）：
```bash
python ingest_web_to_research.py \
  --url https://www.bjnews.com.cn/detail/123456 \
  --task-id tkk-discover/2026-06-22-主题名 \
  --title "新京报原文标题" \
  --tier T1 \
  --keywords "主题1 主题2" \
  --platform 新京报官网 \
  --search-engine Baidu
```

**CLI 模式 2**（备模式 · 已下载的 HTML 文件）：
```bash
python ingest_web_to_research.py \
  --html-file /path/to/captured.html \
  --task-id tkk-discover/2026-06-22-主题名 \
  --title "..." \
  --origin-url "https://..." \
  --tier T2 \
  --keywords "..."
```

**错误处理**：
- CDP 不通 → exit 3 + 3 步修复指引
- CDP /new 失败 → exit 4
- html2md.py 失败 → exit 5
- markdown_converter 失败 → exit 6
- 必传参数缺失 → exit 1
- --url + --html-file 互斥 → exit 1

### 4. `test_html2md.py` — 单元测试

5 个测试用例:字面 HTML / frontmatter / 剥噪声 / 复杂 HTML(表格+图片) / 输入校验

```bash
python test_html2md.py
# 期望输出: [OK] 5/5 测试通过
```

---

## E2E 流程图

```
[LLM/agent 用 web-access 抓取 URL → 拿 HTML]
                ↓
[可选: 已存为 .html 文件, 走 --html-file 模式]
                ↓
ingest_web_to_research.py
                ↓
Step 1: fetch_html_via_cdp() 或读 .html 文件(主路径)
                ↓
Step 2: subprocess → html2md.py(主路径:markdownify)
                ↓
Step 3: markdown_converter.write_research_source()(主路径)
                ↓
[tasks/discovered-in-research/<task_id>/SRC-NNN__标题.md]
                ↓
[INDEX.md + research_log.md 增量更新]
                ↓
[后续: tkk-legal-ingest v67 catch-up mode 自动处理]
```

---

## 与 tkk-* skill 集成

- **tkk-discover 环节 3 触发**：识别到 wiki 缺口 → 调 web-access 抓资料 → 用本工具集自动入库
- **tkk-legal-ingest v67 catch-up mode**：自动扫描 `sources/discovered-in-research/*/SRC-*.md` 并入 wiki
- **web-access skill**：提供 CDP Proxy (本工具集的唯一外部数据源)

---

## 失败哲学(per `feedback-no-design-degradation-2026-06-22`)

| 场景 | 工具集行为 | 替代方案(禁止) |
|------|------------|---------------|
| CDP 端口不通 | exit 3 + 3 步修复 | ~~urllib 直接抓~~ |
| markdownify 缺 | exit 2 + pip 指引 | ~~html.parser 自写~~ |
| 目标 URL 需要登录 | exit 4 + 提示 | ~~强制抓取拿残页~~ |
| Python 进程 import 失败 | exit 2 + 指引 | ~~降级到 partial flow~~ |

**不预埋降级路径,失败 loudly 报错 → LLM/用户修复 → 重跑**。

---

## 历史

- **2026-06-22 v1.0**: 初版
  - `html2md.py`(主路径 markdownify)
  - `ingest_web_to_research.py`(主路径 web-access/CDP)
  - `test_html2md.py`(5 用例)
  - 修 double frontmatter bug(html2md 不加 fm,markdown_converter 统一加)
