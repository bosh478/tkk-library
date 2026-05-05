#!/usr/bin/env python3
"""
retro_fix_related.py
Wiki 回溯更新 - related 字段自动补全脚本

功能：
1. 扫描所有 wiki 页面的 related 字段
2. 对 related 为空的页面，自动基于 tags/层级/类型生成建议链接
3. 输出修复建议，不直接修改文件

用法:
    python retro_fix_related.py [dir]
    python retro_fix_related.py wiki/summaries/
    python retro_fix_related.py --apply  # 实际应用修改
"""

import os
import sys
import re
import glob
from pathlib import Path
from typing import Dict, List, Tuple, Set
import yaml

WIKI_ROOT = Path("D:/AI agent/tkk-library/wiki")


def parse_frontmatter(content: str) -> Tuple[Dict, str]:
    """解析 frontmatter"""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return {}, content
    try:
        fields = yaml.safe_load(match.group(1)) or {}
        body = content[match.end():]
        return fields, body
    except:
        return {}, content


def extract_tags(content: str) -> List[str]:
    """从 frontmatter 提取 tags"""
    fields, _ = parse_frontmatter(content)
    tags = fields.get("tags", [])
    if isinstance(tags, list):
        return [str(t).strip() for t in tags if t]
    elif isinstance(tags, str):
        # tags 可能以逗号分隔
        return [t.strip() for t in tags.split(',') if t.strip()]
    return []


def extract_title(content: str) -> str:
    """提取页面标题"""
    fields, body = parse_frontmatter(content)
    if fields.get("title"):
        return fields["title"]
    # 尝试从第一行 H1 提取
    match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ""


def build_tag_index(all_files: List[Path]) -> Dict[str, List[Tuple[Path, str]]]:
    """建立 tag -> (文件路径, 标题) 的索引"""
    tag_index = {}
    for filepath in all_files:
        try:
            content = filepath.read_text(encoding="utf-8")
            tags = extract_tags(content)
            title = extract_title(content)
            for tag in tags:
                if tag not in tag_index:
                    tag_index[tag] = []
                tag_index[tag].append((filepath, title))
        except Exception:
            continue
    return tag_index


def build_hierarchy_index(all_files: List[Path]) -> Dict[int, List[Tuple[Path, str]]]:
    """建立 hierarchyLevel -> (文件路径, 标题) 的索引"""
    hierarchy_index = {}
    for filepath in all_files:
        try:
            content = filepath.read_text(encoding="utf-8")
            fields, _ = parse_frontmatter(content)
            level = fields.get("hierarchyLevel")
            if level is not None:
                level_int = int(level) if str(level).isdigit() else 0
                title = extract_title(content)
                if level_int not in hierarchy_index:
                    hierarchy_index[level_int] = []
                hierarchy_index[level_int].append((filepath, title))
        except Exception:
            continue
    return hierarchy_index


def find_related_suggestions(filepath: Path, all_files: List[Path],
                             tag_index: Dict[str, List[Tuple[Path, str]]],
                             hierarchy_index: Dict[int, List[Tuple[Path, str]]]) -> List[str]:
    """基于内容分析生成 related 建议"""
    suggestions = []

    try:
        content = filepath.read_text(encoding="utf-8")
    except:
        return suggestions

    fields, body = parse_frontmatter(content)
    tags = extract_tags(content)
    file_type = fields.get("type", "")
    hierarchy_level = fields.get("hierarchyLevel")
    title = extract_title(content)

    # 基于 tags 匹配（同标签页面）
    for tag in tags:
        if tag in tag_index:
            for other_path, other_title in tag_index[tag]:
                if other_path != filepath:
                    suggestions.append(f"  - [[{other_title}]]  # 共享标签: {tag}")

    # 基于 hierarchyLevel 链接（上位法/下位法）
    if hierarchy_level:
        try:
            level = int(hierarchy_level) if str(hierarchy_level).isdigit() else 0
            if level > 1 and (level - 1) in hierarchy_index:
                # 上位法
                for other_path, other_title in hierarchy_index[level - 1]:
                    if other_path != filepath:
                        suggestions.append(f"  - [[{other_title}]]  # 上位法 (层级 {level-1})")
            if level < 6 and (level + 1) in hierarchy_index:
                # 下位法
                for other_path, other_title in hierarchy_index[level + 1]:
                    if other_path != filepath:
                        suggestions.append(f"  - [[{other_title}]]  # 下位法 (层级 {level+1})")
        except:
            pass

    # 基于 type 类型匹配
    type_related_dirs = {
        "concept": ["entities", "summaries", "syntheses"],
        "entity": ["concepts", "summaries", "syntheses"],
        "summary": ["concepts", "entities", "syntheses"],
        "synthesis": ["concepts", "entities", "summaries"],
    }
    if file_type in type_related_dirs:
        for other_dir in type_related_dirs[file_type]:
            dir_path = WIKI_ROOT / other_dir
            if dir_path.exists():
                for other_file in dir_path.glob("*.md"):
                    if other_file == filepath:
                        continue
                    try:
                        other_content = other_file.read_text(encoding="utf-8")
                        other_tags = extract_tags(other_content)
                        # 检查是否有共同标签
                        common = set(tags) & set(other_tags)
                        if common:
                            other_title = extract_title(other_content)
                            suggestions.append(
                                f"  - [[{other_title}]]  # 同类({other_dir}): {', '.join(common)}"
                            )
                    except:
                        continue

    # 去重（基于链接标题）
    seen = set()
    unique = []
    for s in suggestions:
        # 提取 [[标题]] 部分
        link_match = re.search(r'\[\[(.+?)\]\]', s)
        if link_match:
            link_title = link_match.group(1)
            if link_title not in seen:
                seen.add(link_title)
                unique.append(s)

    return unique[:10]  # 最多10个建议


def main():
    apply_mode = "--apply" in sys.argv
    target_dir = sys.argv[-1] if not apply_mode else sys.argv[-2]

    if target_dir == "--apply":
        target_dir = "."

    target_path = WIKI_ROOT / target_dir if not Path(target_dir).is_absolute() else Path(target_dir)

    if not target_path.exists():
        print(f"目录不存在: {target_path}")
        sys.exit(1)

    # 收集所有 wiki 文件（用于跨目录匹配）
    all_files = []
    for subdir in ["concepts", "entities", "summaries", "syntheses"]:
        subdir_path = WIKI_ROOT / subdir
        if subdir_path.exists():
            all_files.extend(subdir_path.glob("*.md"))

    print(f"索引了 {len(all_files)} 个 wiki 文件")

    # 建立索引
    print("建立 tag 索引...")
    tag_index = build_tag_index(all_files)
    print(f"tag 索引: {len(tag_index)} 个标签")

    print("建立 hierarchyLevel 索引...")
    hierarchy_index = build_hierarchy_index(all_files)
    print(f"hierarchyLevel 索引: {len(hierarchy_index)} 个层级")

    # 扫描 related 字段为空的页面
    missing_count = 0
    results = []

    # 确定要扫描的目录
    if target_path.is_file():
        scan_files = [target_path]
    else:
        scan_files = list(target_path.glob("*.md"))

    print(f"\n扫描 {len(scan_files)} 个文件...")

    for filepath in scan_files:
        try:
            content = filepath.read_text(encoding="utf-8")
            fields, _ = parse_frontmatter(content)

            related = fields.get("related", "")
            # related 可能为空字符串、None、[] 或列表
            if not related or related == [] or related == "" or related is None:
                suggestions = find_related_suggestions(filepath, all_files, tag_index, hierarchy_index)
                if suggestions:
                    missing_count += 1
                    results.append({
                        "file": filepath.relative_to(WIKI_ROOT),
                        "filepath": filepath,
                        "title": extract_title(content),
                        "type": fields.get("type", "unknown"),
                        "tags": extract_tags(content),
                        "hierarchyLevel": fields.get("hierarchyLevel"),
                        "suggestions": suggestions
                    })
        except Exception as e:
            continue

    print(f"\n{'='*60}")
    print("related 字段补全建议")
    print(f"{'='*60}")
    print(f"related 为空且有建议的页面: {missing_count} 个\n")

    for r in results:
        print(f"--- {r['file']} ---")
        print(f"  类型: {r['type']}")
        print(f"  标签: {', '.join(r['tags']) if r['tags'] else '无'}")
        if r['hierarchyLevel']:
            print(f"  层级: {r['hierarchyLevel']}")
        print(f"  建议关联:")
        for s in r["suggestions"]:
            print(s)
        print()

        # 如果是 apply 模式，写入建议到文件的 ## 相关 区域
        if apply_mode:
            apply_suggestions(r["filepath"], r["suggestions"])

    print(f"\n汇总: {missing_count} 个页面需要补充 related 字段")

    if apply_mode:
        print("\n✅ 已将建议写入相关页面的 ## 相关 区域")
    else:
        print("\n💡 使用 --apply 参数实际应用修改")

    # 输出一个可执行的 sed 命令示例
    if missing_count > 0 and not apply_mode:
        print("\n--- 手动修复示例 ---")
        if results:
            sample = results[0]
            print(f"# 为 {sample['file']} 添加 related 字段")
            print(f"# 编辑 {sample['file']}")
            print(f"# 在 frontmatter 中添加:")
            print(f"related:")
            for s in sample["suggestions"][:3]:
                link_match = re.search(r'\[\[(.+?)\]\]', s)
                if link_match:
                    print(f"  - [[{link_match.group(1)}]]")


def apply_suggestions(filepath: Path, suggestions: List[str]):
    """将建议应用到文件"""
    try:
        content = filepath.read_text(encoding="utf-8")

        # 检查是否已有 ## 相关 区域
        if "## 相关" in content:
            # 追加到现有区域
            print(f"  → {filepath.name}: 已存在 ## 相关 区域，跳过")
            return

        # 提取 frontmatter
        match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if not match:
            return

        # 构建 related 值
        related_links = []
        for s in suggestions[:5]:  # 最多5个
            link_match = re.search(r'\[\[(.+?)\]\]', s)
            if link_match:
                related_links.append(f"  - [[{link_match.group(1)}]]")

        if not related_links:
            return

        # 添加 related 到 frontmatter
        frontmatter = match.group(1)
        related_yaml = "related:\n" + "\n".join(related_links) + "\n"
        new_frontmatter = frontmatter.rstrip() + "\n" + related_yaml

        # 重新组装文件
        new_content = "---\n" + new_frontmatter + "---\n" + content[match.end():]

        # 添加 ## 相关 区域到正文末尾
        related_section = "\n\n## 相关\n\n" + "\n".join(related_links) + "\n"
        new_content = new_content.rstrip() + related_section

        # 写回
        filepath.write_text(new_content, encoding="utf-8")
        print(f"  → {filepath.name}: 已添加 related 字段")

    except Exception as e:
        print(f"  → {filepath.name}: 失败 ({e})")


if __name__ == "__main__":
    main()
