#!/bin/bash
#===========================================================
# 阶段一查重筛选脚本 v2.0
# 用途：检查指定 sources 子目录中的 .md 文件是否已被 wiki 整理
# 输入：sources 子目录路径（如 司法观点、案例/）
# 输出：
#   - 已整理.md — 已存在于 wiki 中的文件
#   - 未整理.md — 需要继续处理的文件
#   - 清理旧的输出文件后再生成新结果，避免污染
#===========================================================

set -euo pipefail

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查参数
if [ $# -lt 1 ]; then
    echo -e "${RED}用法: $0 <sources子目录路径>${NC}"
    echo -e "示例: $0 司法观点、案例/"
    exit 1
fi

SUBDIR="$1"

# 解析为完整路径（去除结尾斜杠，处理是否带 sources/ 前缀）
SUBDIR="${SUBDIR%/}"
SUBDIR="${SUBDIR#sources/}"
SUBDIR="${SUBDIR#sources}"
SUBDIR="${SUBDIR#/}"

FULL_SOURCES_DIR="sources/${SUBDIR}"

echo -e "${YELLOW}正在检查目录: sources/${SUBDIR}${NC}"

#===========================================================
# 【重要】步骤0：清理旧输出文件，避免结果污染
#===========================================================
echo -e "${YELLOW}[0/4] 清理旧的输出文件...${NC}"
rm -f "已整理.md" "未整理.md" 2>/dev/null || true
rm -f "已整理.txt" "未整理.txt" 2>/dev/null || true

# 创建唯一临时文件（使用PID+时间戳，避免多进程冲突）
TEMP_WIKI_SOURCES_LIST=$(mktemp)

# 清理函数
cleanup() {
    rm -f "${TEMP_WIKI_SOURCES_LIST}" 2>/dev/null || true
}
trap cleanup EXIT

#===========================================================
# 步骤1: 收集所有 wiki 文件中的 source/sources 字段值
#===========================================================
echo -e "${YELLOW}[1/4] 正在扫描 wiki 目录中的 source 字段...${NC}"

WIKI_DIRS=("wiki/summaries" "wiki/concepts" "wiki/entities" "wiki/syntheses")

> "${TEMP_WIKI_SOURCES_LIST}"

for wiki_dir in "${WIKI_DIRS[@]}"; do
    if [ -d "${wiki_dir}" ]; then
        # 提取 frontmatter 中的 source 和 sources 字段
        # 处理格式:
        #   source: [[文件名.md]]
        #   source: [["文件名.md"]]
        #   sources: [[文件名]]
        #   sources: [["文件名1.md"], ["文件名2.md"]]
        #   source: ["sources/目录/文件名.md"]
        #   sources: [["文件名.md"]]
        grep -rE "^source[s]?:" "${wiki_dir}"/ --include="*.md" -h 2>/dev/null | \
            sed -E 's/^source[s]?:\s*//' | \
            # 去掉首尾的 [[ 和 ]]
            sed -E 's/^\[\[//' | sed -E 's/\]\]$//' | \
            # 按 ], [ 分割成多行
            sed -E 's/\],\s*\[/\n/g' | \
            # 去掉每行首尾的 [ 和 ]
            sed -E 's/^\[//' | sed -E 's/\]$//' | \
            sed -E 's/^"//g; s/"$//g' | \
            grep -v '^$' | \
            while IFS= read -r line; do
                # 去除可能的 sources/ 前缀，只保留纯文件名
                basename "${line}" 2>/dev/null || echo "${line}"
            done
    fi
done | sort -u > "${TEMP_WIKI_SOURCES_LIST}"

echo "  找到 $(wc -l < "${TEMP_WIKI_SOURCES_LIST}") 个唯一的 source 引用"

#===========================================================
# 步骤2: 遍历指定 sources 子目录的所有 .md 文件
#===========================================================
echo -e "${YELLOW}[2/4] 正在遍历 sources/${SUBDIR} 中的 .md 文件...${NC}"

if [ -d "${FULL_SOURCES_DIR}" ]; then
    mapfile -t MD_FILES < <(find "${FULL_SOURCES_DIR}" -maxdepth 1 -type f -name "*.md" -printf "%f\n" 2>/dev/null | sort)
else
    echo -e "${RED}错误: 无法访问目录 ${FULL_SOURCES_DIR}${NC}"
    exit 1
fi

TOTAL_FILES=${#MD_FILES[@]}
echo "  共有 ${TOTAL_FILES} 个 .md 文件"

if [ ${TOTAL_FILES} -eq 0 ]; then
    echo -e "${YELLOW}该目录下没有 .md 文件${NC}"
    touch "已整理.md" "未整理.md"
    exit 0
fi

#===========================================================
# 步骤3: 精确匹配并分类
#===========================================================
echo -e "${YELLOW}[3/4] 正在精确匹配 source 字段...${NC}"

> "已整理.md"
> "未整理.md"

MATCHED=0
UNMATCHED=0

for md_file in "${MD_FILES[@]}"; do
    if grep -Fqx "${md_file}" "${TEMP_WIKI_SOURCES_LIST}"; then
        echo "${md_file}" >> "已整理.md"
        ((MATCHED++)) || true
    else
        echo "${md_file}" >> "未整理.md"
        ((UNMATCHED++)) || true
    fi
done

#===========================================================
# 步骤4: 输出结果
#===========================================================
echo -e "${YELLOW}[4/4] 生成输出文件...${NC}"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}查重筛选完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "  ${GREEN}已整理: ${MATCHED} 个文件${NC}"
echo -e "  ${YELLOW}未整理: ${UNMATCHED} 个文件${NC}"
echo ""
echo "输出文件:"
echo "  - $(pwd)/已整理.md"
echo "  - $(pwd)/未整理.md"
echo ""

# 显示文件内容预览
if [ ${MATCHED} -gt 0 ]; then
    echo -e "${GREEN}--- 已整理.md 内容预览 ---${NC}"
    head -10 "已整理.md"
    [ ${MATCHED} -gt 10 ] && echo "  ... (共 ${MATCHED} 条)"
    echo ""
fi

if [ ${UNMATCHED} -gt 0 ]; then
    echo -e "${YELLOW}--- 未整理.md 内容预览 ---${NC}"
    head -10 "未整理.md"
    [ ${UNMATCHED} -gt 10 ] && echo "  ... (共 ${UNMATCHED} 条)"
fi
