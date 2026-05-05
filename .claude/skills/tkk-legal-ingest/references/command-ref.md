# 命令速查

> 常用命令参考，被 SKILL.md 引用
> 功能完全体，请配合 SKILL.md 主入口使用

---

## ingest 常用命令

### 阶段一：扫描源文件

```bash
ls sources/xxx/*.md | wc -l                    # 统计文件数
ls sources/xxx/*.md | grep -E '\([0-9]+\)$'   # 检测重复后缀
```

### 阶段三：精确比对（发现遗漏）

```bash
for f in sources/xxx/*.md; do
  name=$(basename "$f" .md)
  base_clean=$(echo "$name" | sed 's/（[0-9]*年[修正修订]*）//g')
  [ -f "wiki/concept_${name}.md" ] && continue
  [ -f "wiki/concept_${base_clean}.md" ] && continue
  echo "$name"
done
```

### 阶段三：占位符扫描

```bash
grep -r "待补充\|见原文\|（略）" wiki/summaries/*.md -l
```

### 阶段三：文件大小检查

```bash
for f in wiki/concepts/*.md; do
  size=$(wc -c < "$f")
  [ "$size" -lt 5000 ] && echo "⚠️ 可疑：$size bytes: $(basename "$f")"
done
```

### 阶段四：整合入库

```bash
qmd update && qmd embed
# 模型未下载时使用国内加速
HF_ENDPOINT=https://hf-mirror.com qmd embed
```

---

## lint 常用命令

### 断链检查

```bash
grep -r "\[\[" wiki/ | grep -v "\[\[.*\]\]"
```

### 源文件完整性验证

```bash
grep -r "^source:" wiki/summaries/*.md | sed 's/.*\///' | cut -d: -f1 | sort -u > /tmp/summary_sources.txt
ls sources/*.md sources/网络文章/*.md 2>/dev/null | sed 's|.*/||' | sort -u > /tmp/all_sources.txt
diff /tmp/summary_sources.txt /tmp/all_sources.txt | grep "^<" | sed 's/^< //' | while read f; do [ -f "sources/$f" ] || echo "⚠️ $f"; done
```

---

## purge 常用命令

### 查询源文件对应的wiki页面

```bash
grep "源文件名" sources/INDEX.md
```

### 删除前确认

```bash
ls wiki/summaries/源文件名*.md wiki/concepts/源文件名*.md
```

---

## qmd 维护

```bash
# 模型已下载（~/.cache/qmd/models/），直接运行即可
qmd status                              # 查看索引状态
qmd update                              # 更新文件索引（ingest后必运行）
qmd embed                               # 增量生成向量（已下载模型）

# 首次下载模型（国内加速）
# HF_ENDPOINT=https://hf-mirror.com qmd embed

# 维度冲突时
qmd embed -f                           # 重跑全量（耗时5-10分钟）
```
