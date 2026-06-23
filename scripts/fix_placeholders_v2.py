#!/usr/bin/env python3
"""
修复刑事审判参考占位符页面 v2
直接从源文件提取案例内容，替换占位符
"""

import re
import os
from pathlib import Path

# VAULT_ROOT 多平台兼容（patched 2026-06-23）：
# 1. 优先 TKK_VAULT_ROOT 环境变量
# 2. Windows: "D:/AI agent/tkk-library"
# 3. Linux/WSL: /home/kangkang/tkk-library 等候选按存在性自动探测
_VAULT_CANDIDATES = [
    os.environ.get("TKK_VAULT_ROOT"),
    "D:/AI agent/tkk-library" if os.name == "nt" else None,
    "/home/kangkang/tkk-library",
    "/mnt/d/AI agent/tkk-library",
    "/mnt/c/Users/汤康康/tkk-library",
]
VAULT_ROOT = next(
    (Path(p) for p in _VAULT_CANDIDATES if p and Path(p).exists()),
    Path(os.environ.get("TKK_VAULT_ROOT", "D:/AI agent/tkk-library"))
)
SOURCE_DIR = VAULT_ROOT / "sources/刑事审判参考/刑事审判参考-100以内"
OUTPUT_DIR = VAULT_ROOT / "wiki/syntheses/Court_刑事审判参考"

def extract_ji_num(filename):
    match = re.search(r'总第(\d+)', filename)
    if match:
        return match.group(1)
    match = re.search(r'总第(\d+)卷', filename)
    if match:
        return match.group(1) + "_上"
    return None

def parse_source_headings(content):
    """直接从源文件解析案例标题（按# 标题）"""
    cases = []
    lines = content.split('\n')

    # 找到所有以 # 开头的行（非表格内的标题行）
    in_metadata = True  # 跳过开头的元数据区域
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue

        # 跳过元数据区域（书名、CIP信息等）
        if stripped.startswith('---') or stripped.startswith('*') or '参考' in stripped[:10]:
            if '图书在版编目' in stripped or '法律出版社' in stripped:
                in_metadata = False
            if in_metadata and '## ' not in stripped:
                continue

        # 找到案例标题（以# 开头，后面是案例名）
        if stripped.startswith('# ') and len(stripped) > 5:
            title = stripped[2:].strip()

            # 过滤掉明显不是案例的标题
            skip_patterns = [
                '刑事审判参考', '中华人民共和国最高人民法院',
                'Reference to', '发刊词', '目 录', '【', '】',
                '的理解与适用', '的理解和适用', '的解释',
                '的规定', '的通知', '的批复', '的理解', '的理解'
            ]

            is_case = True
            for pattern in skip_patterns:
                if pattern in title:
                    is_case = False
                    break

            # 案例标题通常包含罪名关键词
            crime_keywords = ['走私', '诈骗', '盗窃', '抢劫', '杀人', '伤害', '强奸',
                             '贩卖', '受贿', '贪污', '非法', '贩毒', '赌博', '绑架',
                             '拐卖', '重婚', '交通', '伪造', '侵占', '敲诈', '寻衅',
                             '经营', '爆炸', '持有', '挪用', '脱逃', '窝藏', '容留',
                             '组织', '介绍', '强迫', '敲诈', '破坏', '出售', '购买',
                             '骗取', '窃取', '侵入', '拒不', '故意', '过失', '玩忽职守']

            if is_case:
                for kw in crime_keywords:
                    if kw in title:
                        # 找到案例标题了
                        # 标题可能跨行（案例名 + 副标题），检查下一行是否也是标题的一部分
                        case_text = title
                        break
                else:
                    is_case = False

            if is_case and len(title) > 3:
                cases.append((i + 1, title))  # 行号从1开始

    return cases

def extract_case_content(content, start_line):
    """提取案例内容"""
    lines = content.split('\n')

    # 从指定行开始提取，直到下一个# 标题
    start_idx = start_line - 1
    case_lines = []

    for i in range(start_idx, len(lines)):
        line = lines[i]

        # 如果遇到下一个# 标题（不在案例内容中），停止
        if i > start_idx and line.strip().startswith('# '):
            # 检查这是否是一个新的案例标题
            stripped = line.strip()
            skip_patterns = ['刑事审判参考', 'Reference', '的理解', '的规定', '的通知', '的批复']
            is_new_case = any(p in stripped for p in skip_patterns)
            if not is_new_case and len(stripped) > 5:
                break

        case_lines.append(line)

    return '\n'.join(case_lines)

def main():
    # 获取所有需要修复的占位符文件
    placeholder_files = []
    for f in OUTPUT_DIR.glob("*.md"):
        content = f.read_text(encoding='utf-8')
        if '（内容待提取）' in content:
            placeholder_files.append(f)

    print(f"发现 {len(placeholder_files)} 个占位符文件")

    fixed = 0
    for wiki_path in placeholder_files:
        # 从wiki文件名提取辑号
        filename = wiki_path.name
        m = re.search(r'_(\d+)辑_', filename)
        if not m:
            continue
        ji_num = m.group(1)

        # 找到对应的源文件
        source_file = f"《刑事审判参考 总第{ji_num}辑》.md"
        source_path = SOURCE_DIR / source_file
        if not source_path.exists():
            # 可能是第3卷上辑
            if ji_num == '3':
                source_file = "《刑事审判参考 总第3卷 上辑》.md"
                source_path = SOURCE_DIR / source_file

        if not source_path.exists():
            print(f"⚠️ 源文件不存在: {source_file}")
            continue

        content = source_path.read_text(encoding='utf-8')

        # 获取wiki文件中的案例标题
        wiki_content = wiki_path.read_text(encoding='utf-8')
        # 从frontmatter后的标题行提取标题
        match = re.search(r'^# (.+)$', wiki_content, re.MULTILINE)
        if not match:
            continue
        case_title = match.group(1).strip()

        # 在源文件中找到这个案例的起始行
        lines = content.split('\n')
        case_start_line = None
        for i, line in enumerate(lines):
            if line.strip().startswith('# ') and case_title[:15] in line:
                case_start_line = i + 1
                break

        if not case_start_line:
            # 尝试模糊匹配
            for i, line in enumerate(lines):
                if case_title[:10] in line and len(line.strip()) > 5:
                    case_start_line = i + 1
                    break

        if not case_start_line:
            continue

        # 提取案例内容
        case_content = extract_case_content(content, case_start_line)

        # 更新wiki文件
        if case_content and len(case_content) > 100:
            # 保留frontmatter，只替换正文
            wiki_lines = wiki_content.split('\n')
            new_wiki_lines = []
            in_frontmatter = True
            for line in wiki_lines:
                if line.strip() == '---':
                    if in_frontmatter:
                        in_frontmatter = False
                        new_wiki_lines.append(line)
                    else:
                        new_wiki_lines.append(line)
                elif in_frontmatter:
                    new_wiki_lines.append(line)
                else:
                    if line.startswith('## ') and '基本案情' in line:
                        # 找到基本案情标题，继续添加提取的内容
                        new_wiki_lines.append(line)
                        new_wiki_lines.append('\n')
                        new_wiki_lines.append(case_content[:5000])
                        break
                    new_wiki_lines.append(line)

            new_wiki_content = '\n'.join(new_wiki_lines)
            wiki_path.write_text(new_wiki_content, encoding='utf-8')
            fixed += 1

    print(f"\n修复完成: {fixed}/{len(placeholder_files)}")

if __name__ == '__main__':
    main()