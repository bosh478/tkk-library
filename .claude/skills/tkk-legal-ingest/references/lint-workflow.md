# lint：健康检查

> 详细流程文档，被 SKILL.md 引用
> 功能完全体，请配合 SKILL.md 主入口使用

---

## @基础检查项

1. **断链检查**：`grep -r "\[\[" wiki/ | grep -v "\[\[.*\]\]"`
2. **矛盾检查**：同一数额标准在不同页面是否一致（如3万/20万/300万是否出现在所有相关罪名页）
3. **过时检查**：较新来源是否推翻旧结论
4. **空白检查**：重要概念是否已有页面
5. **交叉链接检查**：重要 concept 是否链接相关 entity/synthesis
6. **分类统计验证**：各目录文件数与预期一致
7. **源文件完整性验证**：wiki 页面的 source 字段指向的源文件是否存在

## @源文件完整性验证脚本

```bash
# 检查 wiki 页面的 source 是否仍存在于 sources/
missing=0
for f in wiki/summaries/*.md wiki/concepts/*.md; do
  if grep -q "^source:" "$f"; then
    # 提取 source 字段中的文件名
    sources=$(grep "^source:" "$f" | sed 's/^source: *//' | tr -d '[]' | tr ',' '\n')
    for src in $sources; do
      # 提取文件名（去除 [[ ]] 和路径前缀）
      fname=$(echo "$src" | sed 's/.*\///' | tr -d ']')
      if [ -n "$fname" ] && [ ! -f "sources/$fname" ] && [ ! -f "sources/网络文章/$fname" ]; then
        echo "⚠️ 源文件缺失：$fname（被 $f 引用）"
        missing=$((missing+1))
      fi
    done
  fi
done
[ "$missing" -eq 0 ] && echo "✅ 源文件完整性检查通过"
```

## @小型法律文件基线（不触发空洞告警）

| 类型 | 示例 | 预期大小 |
|------|------|----------|
| 宪法修正案 | 1988/1993/1999/2004/2018修正案 | 1-3KB |
| 法律修改决定 | 关于修改XX法的决定 | 1-3KB |
| 简单单行法 | 兵役法/人民调解法等 | 2-5KB |

## @进阶任务

- 概念空白检查：常见罪名是否都有 concept 页
- 发现待新建页面：旧知识是否被新资料推翻但页面未更新
- 建议下一步来源：根据空白建议补充
- 孤立页面检查：无入站链接的页面

## @lint 报告格式

```
## Lint 报告 [日期]

### 基础检查
- 断链：N 个
- 矛盾：N 个
- 占位符：N 个
- 空洞文件：N 个

### 统计
- concepts：N 个
- summaries：N 个
- qmd 索引：N documents

### 建议
- 建议补充来源：...
- 建议新建页面：...
- 建议优先修复：Level 1-2 文件 N 个
```
