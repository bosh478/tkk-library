#!/bin/bash
# 处理检答网集萃36-70的批量转换脚本

SOURCE_DIR="D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-检答网集萃-md"
TARGET_DIR="D:/AI agent/tkk-library/wiki/summaries"

# 创建目标目录
mkdir -p "$TARGET_DIR"

# 获取36-70的文件列表
files=$(ls "$SOURCE_DIR" | grep -E "检答网集萃([3-6][0-9]|70)" | grep -v "检答网集萃[0-3][0-5]" | sort)

count=0
for file in $files; do
    ((count++))
    echo "Processing [$count] $file"

    # 提取日期 (格式: [YYYY-MM-DD])
    date=$(echo "$file" | grep -oE "\[([0-9]{4}-[0-9]{2}-[0-9]{2})\]" | tr -d '[]')

    # 提取集萃编号
    num=$(echo "$file" | grep -oE "检答网集萃[0-9]+" | grep -oE "[0-9]+")

    # 提取标题（去除日期前缀和.md后缀）
    title_raw=$(echo "$file" | sed 's/\[[0-9-]*\]检答网集萃'"$num"'//' | sed 's/\.md$//')

    # 读取源文件内容
    filepath="$SOURCE_DIR/$file"
    content=$(cat "$filepath")

    # 提取咨询类别
    category=$(echo "$content" | grep -oE "咨询类别：.*" | head -1 | sed 's/咨询类别：[[:space:]]*//' | tr -d '\n\r')

    # 提取咨询人
    consultant=$(echo "$content" | grep -oE "咨询人：.*" | head -1 | sed 's/咨询人：[[:space:]]*//' | tr -d '\n\r')

    # 提取咨询内容（从"咨询内容："到"个人意见"之前）
   咨询_content=$(echo "$content" | sed -n '/咨询内容：/,/个人意见/p' | head -n -1 | tail -n +2 | sed 's/^*//' | tr -d '\n\r' | sed 's/[[:space:]]\+/ /g')

    # 提取个人意见
    personal_opinion=$(echo "$content" | sed -n '/个人意见（理由和依据）：/,/解答专家/p' | head -n -1 | tail -n +2 | sed 's/^*//' | tr -d '\n\r')

    # 提取解答专家
    expert_response=$(echo "$content" | sed -n '/解答专家/,/往期回顾/p' | head -n -1 | tail -n +2 | sed 's/^*//' | tr -d '\n\r')

    # 构建目标文件名
    target_file="summary_检答网集萃${num}_${title_raw}.md"
    target_path="$TARGET_DIR/$target_file"

    # 提取关键词
    keywords="认罪认罚/相对不起诉/具结书"

    # 写入目标文件
    cat > "$target_path" << 'EOF'
---
title: 检答网集萃{N} {标题}
type: summary
created: 2026-05-07
updated: 2026-05-07
tags: [检察业务]
category: 诉讼与仲裁
source: {原始文件名}
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | {原始文件名} |
| 类型 | 检察业务咨询 |
| 发布日期 | {日期} |
| 关键词 | {关键词} |
| 核心要点 | {核心要点} |

## 问答摘要
{问答内容}
EOF

    # 替换占位符
    sed -i "s/{N}/${num}/g" "$target_path"
    sed -i "s/{标题}/${title_raw}/g" "$target_path"
    sed -i "s/{原始文件名}/${file}/g" "$target_path"
    sed -i "s/{日期}/${date}/g" "$target_path"
    sed -i "s/{关键词}/${keywords}/g" "$target_path"
    sed -i "s/{核心要点}/详见下方问答摘要/g" "$target_path"
    sed -i "s/{问答内容}/咨询类别：${category}\n咨询人：${consultant}\n\n咨询内容：${consultant}\n\n个人意见：${personal_opinion}\n\n解答专家意见：${expert_response}/g" "$target_path"

    echo "  -> Created: $target_file"
done

echo ""
echo "========================================"
echo "处理完成！共处理 $count 个文件"
echo "========================================"