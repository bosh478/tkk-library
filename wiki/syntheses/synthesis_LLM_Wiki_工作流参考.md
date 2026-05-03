---
type: synthesis
created: 2026-05-03
title: LLM Wiki 工作流参考
updated: 2026-05-03
tags: [待分类]
source: 〔来源文件不存在〕
source: 〔来源文件不存在〕
source: 〔来源文件不存在〕
---
# LLM Wiki 工作流参考卡

## Ingest（消化新资料）

```
1. 将原始文件放入 sources/ 对应子目录
   ├── 裁判文书/  → .docx / .pdf / 文本
   ├── 法律法规/  → 法律文本
   ├── 网络文章/  → .md / 网页
   └── 书籍资料/  → 笔记/摘要

2. 告诉 LLM："消化这份资料：[文件名]"

3. LLM 执行：
   - 阅读原始文件
   - 与用户讨论关键要点
   - 写入 wiki/summaries/ 摘要页
   - 更新 wiki/concepts/ 或 wiki/entities/ 相关页面
   - 更新 index.md
   - 在 log.md 记录
```

## Query（查询问题）

```
告诉 LLM："查询：[问题]"

LLM 执行：
1. 读取 index.md 定位相关页面
2. 读取相关 wiki 页面
3. 综合回答，标注来源 页面

提示：好的回答可以存为新页面：
"把这个分析存入 wiki"
```

## Lint（健康检查）

```
告诉 LLM："对 wiki 做一次 lint 检查"

LLM 检查：
1. 断链（orphan pages）
2. 矛盾（同一问题不同说法）
3. 过时（新来源推翻旧结论）
4. 空白（重要概念无页面）
5. 交叉引用缺失

结果记入 log.md
```

---

## Obsidian 插件建议

| 插件 | 用途 |
|------|------|
| **Dataview** | 动态查询页面 frontmatter，生成看板 |
| **qmd** | 本地 markdown 搜索（BM25+向量） |
| **Marp** | 从 markdown 生成幻灯片 |
| **Obsidian Web Clipper** | 浏览器一键 clipping |

## 快捷操作

- `Ctrl+Shift+D`：下载当前页图片到 `raw/assets/`
- 定期：`grep "^## \[" log.md | tail -5` 查看最近活动
