# purge：根据原始文件删除对应 wiki 页面

> 详细流程文档，被 SKILL.md 引用
> 功能完全体，请配合 SKILL.md 主入口使用

---

## 核心原则

源文件是绝对红线——**只删除 wiki 页面，源文件永不删除**

## @执行流程

```
1. 查询 sources/INDEX.md，找到该源文件对应的所有 wiki 页面
2. 列出待删除的 wiki 页面，请求用户确认
3. 删除这些 wiki 页面
4. 从 sources/INDEX.md 中移除该源文件的记录
5. 更新 log.md（记录 purge 事件）
```

## @查询命令

```bash
# 在 INDEX.md 中查找
grep "源文件名" sources/INDEX.md

# 列出待删除页面
ls wiki/summaries/源文件名*.md
ls wiki/concepts/源文件名*.md
```

## ⚠️ 不可逆操作，执行前必须二次确认
