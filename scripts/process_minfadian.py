#!/usr/bin/env python3
"""
处理《民法典适用大全》源文件，生成细化的 concept 页面
修复版 v4：解决文件名重复、前言内容、条文边界问题
"""
import os
import re
from pathlib import Path

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/《民法典适用大全》")
OUTPUT_DIR = Path("D:/AI agent/tkk-library/wiki/concepts")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def sanitize_filename(name):
    """清理文件名中的非法字符"""
    name = re.sub(r'[（ ）【】\[\]【】""''""'',，、。：：]', '_', name)
    name = re.sub(r'_+', '_', name)
    name = re.sub(r'^_|_$', '', name)
    return name

def extract_volume_info(filename):
    """从文件名提取卷名和条文范围"""
    # 清理重复的"民法典适用大全"
    basename = filename.replace('《民法典适用大全》', '')
    basename = basename.replace('《民法典适用大全》', '')  # 再清一遍确保干净
    basename = basename.replace('.md', '').strip()

    # 提取条文范围
    range_match = re.search(r'(\d+)-(\d+)', basename)
    if range_match:
        start, end = range_match.groups()
        range_str = f"{start}-{end}"
        # 移除范围部分
        volume_name = re.sub(r'\s*2023年?\s*\d+-\d+\s*$', '', basename)
        volume_name = re.sub(r'\s*\d+-\d+\s*$', '', volume_name)
    else:
        range_str = ""
        volume_name = re.sub(r'\s*2023年?\s*$', '', basename)

    # 清理卷名
    volume_name = volume_name.strip()
    volume_name = re.sub(r'\s+', '_', volume_name)
    volume_name = sanitize_filename(volume_name)

    return volume_name, range_str

def split_by_articles(filepath):
    """将文件按条文分割"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 找到所有条文标题的位置（## 或 ### 开头）
    pattern = r'(##?\s*第[一二三四五六七八九十百千零\d]+条[^\n]*\n)([\s\S]*?)(?=(?:##?\s*第[一二三四五六七八九十百千零\d]+条)|(?:##\s*目录)|(?:##\s*中国民法典适用大全)|(?:#\s*中国民法典适用大全)|$)'

    matches = re.findall(pattern, content)

    articles = []
    for title, body in matches:
        # 提取条文编号
        num_match = re.search(r'第([一二三四五六七八九十百千零\d]+)条', title)
        if not num_match:
            continue
        article_num = num_match.group(1)

        # 提取条文标题（去掉 ## 前缀）
        article_title = re.sub(r'^#+\s*', '', title).strip()

        # 解析内容主体
        parsed_body = parse_body_content(body, article_num)

        if parsed_body['interpretation'] or parsed_body['application_guide']:
            articles.append({
                'article_num': article_num,
                'article_title': article_title,
                'interpretation': parsed_body['interpretation'],
                'application_guide': parsed_body['application_guide']
            })

    return articles

def parse_body_content(body, current_article_num):
    """解析条文主体内容"""
    result = {
        'interpretation': '',
        'application_guide': ''
    }

    lines = body.split('\n')

    current_section = 'interpretation'
    section_lines = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # 检查是否到达下一个条文
        if re.match(r'^#{1,3}\s*第[一二三四五六七八九十百千零\d]+条', line):
            if section_lines:
                content = '\n'.join(section_lines).strip()
                if content:
                    if current_section == 'interpretation':
                        result['interpretation'] = content
                    else:
                        result['application_guide'] = content
            break

        # 检测section切换
        if '适用指引' in line and line.startswith('#'):
            if section_lines:
                content = '\n'.join(section_lines).strip()
                if content and current_section == 'interpretation':
                    result['interpretation'] = content
            current_section = 'application_guide'
            section_lines = []
            i += 1
            continue
        elif '条文释义' in line and line.startswith('#'):
            if section_lines:
                content = '\n'.join(section_lines).strip()
                if content and current_section == 'interpretation':
                    result['interpretation'] = content
            current_section = 'interpretation'
            section_lines = []
            i += 1
            continue

        # 忽略某些section header和无关内容
        if line.startswith('## 关联规定') or line.startswith('# ') or line.startswith('## 目录') or \
           line.startswith('## 中国民法典适用大全') or line.startswith('## 凡例') or \
           line.startswith('## 全面深化') or '青频学习' in line or '音频学习' in line or \
           line.startswith('![](images/'):
            i += 1
            continue

        # 忽略只包含条文编号的行
        if re.match(r'^第[一二三四五六七八九十百千零\d]+条', line) and not line.startswith('#'):
            i += 1
            continue

        # 忽略图片和空行
        if line.startswith('![') or not line:
            i += 1
            continue

        # 收集内容行
        section_lines.append(lines[i])
        i += 1

    # 保存最后的内容
    if section_lines:
        content = '\n'.join(section_lines).strip()
        if content:
            if current_section == 'interpretation':
                result['interpretation'] = content
            else:
                result['application_guide'] = content

    return result

def generate_concept_content(article, volume_name, source_file):
    """生成 concept 页面的内容"""
    article_title = article['article_title']
    article_num = article['article_num']
    interpretation = article['interpretation']
    application_guide = article['application_guide']

    # 清理内容中的多余空行
    interpretation = re.sub(r'\n{3,}', '\n\n', interpretation).strip()
    application_guide = re.sub(r'\n{3,}', '\n\n', application_guide).strip()

    # 截断过长的内容
    if len(interpretation) > 8000:
        interpretation = interpretation[:8000] + '\n\n...（内容过长已截断）'
    if len(application_guide) > 4000:
        application_guide = application_guide[:4000] + '\n\n...（内容过长已截断）'

    interp_section = interpretation if interpretation else '（条文释义内容）'
    guide_section = application_guide if application_guide else '（适用指引内容）'

    content = f"""---
title: 民法典适用大全 - {volume_name} - 第{article_num}条
type: concept
created: 2026-04-22
updated: 2026-04-22
tags: [民法典, 司法解释, {volume_name}, 第{article_num}条]
source: [["《民法典适用大全》{source_file}"]]
---

## {article_title}

### 条文释义

{interp_section}

### 适用指引

{guide_section}

## 相关

- [[concept_民法典适用大全_{volume_name}]]
"""

    return content

def process_file(filepath):
    """处理单个文件"""
    filename = os.path.basename(filepath)
    print(f"处理文件: {filename}")

    volume_name, range_str = extract_volume_info(filename)
    print(f"  卷名: {volume_name}, 条文范围: {range_str}")

    articles = split_by_articles(filepath)
    print(f"  发现 {len(articles)} 个条文")

    generated = 0
    for article in articles:
        if not article['article_num']:
            continue

        # 生成文件名
        output_filename = f"concept_民法典适用大全_{volume_name}_第{article['article_num']}条.md"
        output_path = OUTPUT_DIR / output_filename

        # 生成内容
        content = generate_concept_content(article, volume_name, filename)

        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        generated += 1

    print(f"  生成 {generated} 个 concept 页面")
    return generated

def main():
    """主函数"""
    # 先删除旧的生成文件
    old_files = list(OUTPUT_DIR.glob("concept_民法典适用大全_*.md"))
    if old_files:
        print(f"删除旧的 {len(old_files)} 个文件")
        for f in old_files:
            f.unlink()

    files = list(SOURCE_DIR.glob("*.md"))
    print(f"发现 {len(files)} 个源文件\n")

    total_generated = 0
    for filepath in sorted(files):
        try:
            count = process_file(filepath)
            total_generated += count
        except Exception as e:
            print(f"  处理出错: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n总计: 处理 {len(files)} 个文件, 生成 {total_generated} 个 concept 页面")

if __name__ == "__main__":
    main()
