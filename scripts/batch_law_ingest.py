#!/usr/bin/env python3
"""
批量处理法律源文件 → wiki/concepts/ concept页面
处理 sources/0-现行规范库/法律/ 目录下的所有法律文件
"""

import re
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

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
SOURCES_DIR = VAULT_ROOT / "sources/0-现行规范库/法律"
TARGET_DIR = VAULT_ROOT / "wiki/concepts"

def extract_metadata(content: str) -> Dict[str, str]:
    """从源文件提取metadata"""
    metadata = {}

    # 提取发文机关
    match = re.search(r'发文机关[：:]\s*([^\n]+)', content)
    if match:
        metadata['发文机关'] = match.group(1).strip()

    # 提取发布日期
    match = re.search(r'发布日期[：:]\s*([^\n]+)', content)
    if match:
        metadata['发布日期'] = match.group(1).strip()

    # 提取生效日期
    match = re.search(r'生效日期[：:]\s*([^\n]+)', content)
    if match:
        metadata['生效日期'] = match.group(1).strip()

    # 提取时效性
    match = re.search(r'时效性[：:]\s*([^\n]+)', content)
    if match:
        metadata['时效性'] = match.group(1).strip()

    # 提取文号
    match = re.search(r'文号[：:]\s*([^\n]+)', content)
    if match:
        metadata['文号'] = match.group(1).strip()

    return metadata

def extract_title_from_filename(filename: str) -> str:
    """从文件名提取标题"""
    # 移除.md后缀
    name = filename.replace('.md', '')
    return name

def clean_title(title: str) -> str:
    """清理标题，移除年份和修订/修正标注"""
    # 移除年份标注如（2023修订）、（2020修正）等
    cleaned = re.sub(r'（\d{4}年?[修订修正]*）', '', title)
    return cleaned

def detect_revision_year(filename: str) -> Optional[str]:
    """检测修订年份"""
    match = re.search(r'（(\d{4})年?[修订修正]*）', filename)
    if match:
        return match.group(1)
    return None

def is_recent_revision(filename: str) -> bool:
    """判断是否为2025/2026年修订版本"""
    year = detect_revision_year(filename)
    if year:
        return year in ['2025', '2026']
    return False

def extract_chapters(content: str) -> List[Tuple[str, str]]:
    """提取章节结构：返回 [(章节名, 包含的条文范围), ...]"""
    chapters = []

    # 匹配第X章 总则/分则等
    chapter_pattern = r'(第[一二三四五六七八九十百]+章\s*[^\n]*)'
    matches = re.finditer(chapter_pattern, content)

    for match in matches:
        chapter_title = match.group(1).strip()
        start_pos = match.start()

        # 找下一个章节或文件结尾
        next_chapter_match = re.search(chapter_pattern, content[start_pos + 1:])
        if next_chapter_match:
            end_pos = start_pos + 1 + next_chapter_match.start()
        else:
            end_pos = len(content)

        chapter_content = content[start_pos:end_pos]

        # 提取该章节的条文
        articles = extract_articles(chapter_content)
        if articles:
            chapters.append((chapter_title, articles))

    # 如果没有找到章节（简单文件），按条文提取
    if not chapters:
        articles = extract_articles(content)
        if articles:
            chapters.append(('全文', articles))

    return chapters

def extract_articles(content: str) -> str:
    """提取条文要点"""
    # 匹配条文格式：第X条 ...（或者更简单的：提取前几个实质条文）
    lines = content.split('\n')
    article_lines = []

    for line in lines:
        line = line.strip()
        # 匹配条文：第XX条 开头的内容
        if re.match(r'第[一二三四五六七八九十百\d]+条', line):
            # 简化条文内容（取前100字符）
            if len(line) > 100:
                line = line[:100] + '...'
            article_lines.append(line)

    return '\n'.join(article_lines[:50])  # 最多50条

def build_related_tags(title: str) -> List[str]:
    """根据标题构建相关标签"""
    tags = []

    # 基础标签
    tags.append('法律')

    # 基于标题的分类
    if '刑法' in title:
        tags.append('刑法')
    elif '刑事诉讼法' in title:
        tags.append('刑事诉讼法')
    elif '民法典' in title or '民事诉讼法' in title:
        tags.append('民法')
    elif '行政' in title:
        tags.append('行政法')
    elif '劳动' in title:
        tags.append('劳动法')
    elif '公司' in title:
        tags.append('公司法')
    elif '证券' in title:
        tags.append('证券法')
    elif '知识产权' in title or '专利' in title or '商标' in title:
        tags.append('知识产权')
    elif '环境' in title:
        tags.append('环境法')
    elif '海关' in title or '关税' in title:
        tags.append('海关法')
    elif '保险' in title:
        tags.append('保险法')
    elif '银行' in title or '金融' in title:
        tags.append('金融法')

    return tags

def create_concept_content(
    title: str,
    filename: str,
    metadata: Dict[str, str],
    chapters: List[Tuple[str, str]],
    is_recent: bool = False
) -> str:
    """构建concept文件内容"""
    now = datetime.now().strftime('%Y-%m-%d')
    clean = clean_title(title)
    tags_str = ", ".join(build_related_tags(title))
    revision_year = detect_revision_year(filename) or ""

    # frontmatter
    lines = [
        "---",
        f"title: {clean}",
        "type: concept",
        f"created: {now}",
        f"updated: {now}",
        f"tags: [{tags_str}]",
        f"source: sources/0-现行规范库/法律/{filename}",
        "related: []",
        "line-refs: []",
        "---",
        "",
        "## 📋 文档概览",
        "",
        "| 字段 | 内容 |",
        "|------|------|",
        f"| 来源 | [[sources/0-现行规范库/法律/{filename}]] |",
        "| 类型 | 法律 |",
        f"| 发布日期 | {metadata.get('发布日期', '未知')} |",
        f"| 生效日期 | {metadata.get('生效日期', '未知')} |",
        f"| 时效性 | {metadata.get('时效性', '现行有效')} |",
        f"| 文号 | {metadata.get('文号', '无')} |",
    ]

    content = "\n".join(lines)

    # 2025/2026修订版本的变更说明
    if is_recent:
        content += f"\n\n## ⚠️ 相比旧版的核心变更\n\n> 本版本为{revision_year}年修订版本，与前一版本相比的主要变化需对照原条文确认。\n"

    # 章节内容
    content += "\n\n## 📑 章节结构\n\n"

    for chapter_title, articles in chapters:
        content += f"### {chapter_title}\n\n"
        if articles:
            for line in articles.split('\n'):
                if line.strip():
                    content += f"- {line}\n"
        content += "\n"

    return content

def process_single_file(filepath: Path) -> Tuple[bool, str]:
    """处理单个文件，返回(是否成功, 消息)"""
    try:
        filename = filepath.name
        title = extract_title_from_filename(filename)

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取metadata
        metadata = extract_metadata(content)

        # 提取章节结构
        chapters = extract_chapters(content)

        # 判断是否近期修订
        recent = is_recent_revision(filename)

        # 构建concept内容
        concept_content = create_concept_content(
            title=title,
            filename=filename,
            metadata=metadata,
            chapters=chapters,
            is_recent=recent
        )

        # 生成目标文件名
        clean = clean_title(title)
        target_name = f"concept_{clean}.md"
        target_path = TARGET_DIR / target_name

        # 写入文件
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(concept_content)

        return True, f"OK: {target_name}"
    except Exception as e:
        return False, f"ERROR: {filename} - {str(e)}"

def main():
    """主函数：批量处理法律文件"""
    # 确保目标目录存在
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    # 获取所有md文件
    files = list(SOURCES_DIR.glob('*.md'))
    total = len(files)

    print(f"总计发现 {total} 个法律源文件")
    print(f"目标目录: {TARGET_DIR}")
    print("-" * 60)

    success_count = 0
    error_count = 0
    errors = []

    for i, filepath in enumerate(files, 1):
        success, msg = process_single_file(filepath)
        if success:
            success_count += 1
            if i % 30 == 0 or i == total:
                print(f"[{i}/{total}] {msg}")
        else:
            error_count += 1
            errors.append(msg)
            print(f"[{i}/{total}] {msg}")

    print("-" * 60)
    print(f"处理完成: 成功 {success_count}, 失败 {error_count}")

    if errors:
        print("\n错误列表:")
        for e in errors:
            print(f"  - {e}")

    # 验证数量
    concept_files = list(TARGET_DIR.glob('concept_*.md'))
    print(f"\n验证: wiki/concepts/ 目录下共有 {len(concept_files)} 个concept文件")

if __name__ == '__main__':
    main()
