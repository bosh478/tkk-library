#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Update 70 summary files with v52 format: add line-refs, related, knowledge network table, and knowledge gap callout.
"""

import os
import re

SUMMARY_DIR = 'D:/AI agent/tkk-library/wiki/summaries'
OUTPUT_DIR = 'D:/AI agent/tkk-library/wiki/summaries'

def get_topic_from_filename(filename):
    """Extract topic from filename for related links."""
    # Remove summary_ prefix and .md extension
    name = filename.replace('summary_', '').replace('.md', '')

    # Categorize by prefix
    if name.startswith('summary_2025'):
        return 'lawyer_guide'
    elif name.startswith('summary_LawyerGuide'):
        return 'lawyer_guide'
    elif name.startswith('summary_Court_RukuAnli'):
        return 'court_case'
    elif name.startswith('summary_SPP_GuideCase'):
        return 'spp_guide_case'
    elif name.startswith('summary_SPP_JianDaWang'):
        return 'jianda_qa'
    elif '民事审判' in name or '最高院民一庭' in name:
        return 'civil_trial'
    else:
        return 'general'

def get_related_links(filename, content):
    """Generate related wiki links based on content."""
    related = []

    # Common concept pages based on keywords
    content_lower = content.lower()

    if '收养' in content:
        related.append('[[concept_收养关系]]')
    if '商标' in content:
        related.append('[[concept_商标法]]')
    if '合同' in content and '纠纷' in content:
        related.append('[[concept_合同纠纷]]')
    if '公司' in content and ('决议' in content or '效力' in content):
        related.append('[[concept_公司决议效力瑕疵]]')
    if '股权' in content:
        related.append('[[concept_股权转让]]')
    if '知识产权' in content or '专利' in content or '著作权' in content:
        related.append('[[concept_知识产权]]')
    if '刑事' in content or '犯罪' in content or '诈骗' in content or '盗窃' in content:
        related.append('[[concept_诈骗罪]]')
    if '劳动' in content or '工伤' in content:
        related.append('[[concept_劳动争议]]')
    if '执行' in content and ('异议' in content or '复议' in content):
        related.append('[[concept_执行异议]]')
    if '正当防卫' in content:
        related.append('[[concept_正当防卫]]')
    if '未成年人' in content:
        related.append('[[concept_未成年人保护]]')
    if '人民调解' in content or '三所联动' in content:
        related.append('[[concept_人民调解]]')

    # Deduplicate
    seen = set()
    unique_related = []
    for r in related:
        if r not in seen:
            seen.add(r)
            unique_related.append(r)

    return unique_related

def has_knowledge_network(content):
    """Check if file already has knowledge network section."""
    return '## 📚 知识网络' in content or '## 知识网络' in content

def has_knowledge_gap(content):
    """Check if file already has knowledge gap callout."""
    return '## ⚠️ 知识缺口' in content or '> [!gap]' in content or '知识缺口' in content

def update_file(filepath):
    """Update a single file with v52 format."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(filepath)

    # Check if already has line-refs
    if 'line-refs' in content:
        return False, 'already_has_line_refs'

    # Get related links based on content
    related_links = get_related_links(filename, content)

    # Prepare the additions
    new_frontmatter_lines = []
    new_frontmatter_lines.append('updated: 2026-05-06')
    new_frontmatter_lines.append('line-refs: {}')

    if related_links:
        new_frontmatter_lines.append('related:')
        for link in related_links[:5]:  # Max 5 related links
            new_frontmatter_lines.append(f'  - {link}')
    else:
        new_frontmatter_lines.append('related: []')

    # Insert frontmatter additions after 'updated' line
    lines = content.split('\n')
    new_lines = []
    frontmatter_added = False

    for i, line in enumerate(lines):
        new_lines.append(line)
        if not frontmatter_added and line.startswith('updated:'):
            # Add new fields after updated line
            for add_line in new_frontmatter_lines[1:]:  # Skip 'updated' as it's already there
                new_lines.append(add_line)
            frontmatter_added = True
        elif not frontmatter_added and line.startswith('tags:'):
            # If no updated field, add after tags
            for add_line in new_frontmatter_lines:
                new_lines.append(add_line)
            frontmatter_added = True

    if not frontmatter_added:
        # Insert after title block if frontmatter structure is different
        for i, line in enumerate(lines):
            if line.startswith('---') and i > 0:
                # Insert before second --- (end of frontmatter)
                idx = i
                break
        new_lines = lines[:idx] + new_frontmatter_lines + ['---'] + lines[idx+1:]

    content = '\n'.join(new_lines)

    # Add knowledge network section at end if not present
    if not has_knowledge_network(content):
        content += '\n\n## 📚 知识网络\n\n| 知识点 | 原文引用 | 相关知识 |\n|--------|---------|---------|\n'
        # Try to extract some content for the table
        if '核心要点' in content:
            # Extract from 核心要点 section
            content += '| 核心要点 | 见上文 | [[concept_相关概念]] |\n'

    # Add knowledge gap callout at end if not present
    if not has_knowledge_gap(content):
        content += '\n\n## ⚠️ 知识缺口\n\n> [!gap]+ 知识缺口\n> - 建议补充：详细内容参见原始来源文件\n'

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True, 'success'

def main():
    # Get all files without line-refs
    files_without_line_refs = []

    for f in os.listdir(SUMMARY_DIR):
        if f.endswith('.md'):
            path = os.path.join(SUMMARY_DIR, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
                if 'line-refs' not in content:
                    files_without_line_refs.append(f)

    print(f'Found {len(files_without_line_refs)} files without line-refs')

    success_count = 0
    skip_count = 0
    error_count = 0

    for i, filename in enumerate(files_without_line_refs, 1):
        filepath = os.path.join(SUMMARY_DIR, filename)
        try:
            updated, status = update_file(filepath)
            if status == 'success':
                success_count += 1
                print(f'[{i}/{len(files_without_line_refs)}] Updated: {filename}')
            elif status == 'already_has_line_refs':
                skip_count += 1
                print(f'[{i}/{len(files_without_line_refs)}] Skipped (has line-refs): {filename}')
        except Exception as e:
            error_count += 1
            print(f'[{i}/{len(files_without_line_refs)}] ERROR: {filename} - {e}')

    print(f'\n=== Summary ===')
    print(f'Total files: {len(files_without_line_refs)}')
    print(f'Success: {success_count}')
    print(f'Skipped: {skip_count}')
    print(f'Errors: {error_count}')

if __name__ == '__main__':
    main()