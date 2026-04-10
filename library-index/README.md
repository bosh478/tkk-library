# 数字图书馆检索系统

## 概述

个人法律数字图书馆全文检索系统，支持从 47 本法律书籍中进行语义检索。

## 目录结构

```
D:\AI agent\tkk图书馆\
├── library-index/           # 检索系统目录
│   ├── build-index.js       # 索引构建脚本
│   ├── search.js            # 检索核心模块
│   ├── library-search.js    # 命令行检索工具
│   ├── index.json           # 书籍元数据索引
│   ├── sections.json        # 章节结构索引
│   ├── search-index.json    # MiniSearch 全文索引
│   └── package.json
└── [书籍文件...]
```

## 使用方式

### 方式一：Claude Code Skill（推荐）

在 Claude Code 中直接输入：
```
/tkk-library 检索问题
```

### 方式二：命令行检索

```bash
cd D:\AI agent\tkk图书馆\library-index
node library-search.js "检索问题"
```

示例：
```bash
node library-search.js "刑讯逼供"
node library-search.js "第1038号案例"
node library-search.js "毒品犯罪量刑"
```

## 支持的书库

| 分类 | 数量 | 说明 |
|------|------|------|
| 刑事审判参考 | 42 本 | 总第101-147辑（部分） |
| 司法解释全书 | 1 本 | 2023年版 |
| 刑事审判方法 | 1 本 | 2015年 |
| 刑事审判实务规范 | 1 本 | 2017年 |
| 民商事审判实务 | 1 本 | 法院培训教材 |
| 审委会手册 | 1 本 | 民商事卷 2025年 |

## 检索流程

1. **自动检查索引** - 检查索引是否存在且最新
2. **自动重建索引** - 如有新增资料，自动重建
3. **关键词预筛选** - 使用 MiniSearch 全文索引快速找到候选段落
4. **AI 语义排序** - 使用 Claude AI 判断相关度并排序（通过 /tkk-library）
5. **结构化输出** - 返回原文、来源、路径、相关度

## 新增资料后

当在 `D:\AI agent\tkk图书馆` 文件夹中新增 .md 格式的书籍资料后：

1. 系统会自动检测并重建索引
2. 也可以手动重建：
```bash
cd D:\AI agent\tkk图书馆\library-index
node build-index.js
```

## 索引统计

- 书籍数量：47 本
- 章节数量：17,960 个
- 案例编号：已提取

## Claude Code Skill

触发词：`/tkk-library`

```
/tkk-library 刑讯逼供取得的证据如何处理
/tkk-library 第1038号案例
/tkk-library 毒品犯罪量刑标准
```
