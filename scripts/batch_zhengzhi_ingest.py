#!/usr/bin/env python3
"""
Batch ingest: 上海二中院-至正法律研究-md (77 files)
Target: wiki/summaries/
Naming: summary_Court_上海二中院_至正法律研究_{title}.md
"""

import os
import re
from pathlib import Path

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/上海二中院/上海二中院-至正法律研究-md")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/summaries")

def extract_title(content):
    """Extract title from first # line."""
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            title = re.sub(r'\s*\|.*$', '', line[2:].strip())
            return title
    return None

def extract_body(content):
    """Extract body - remove title, author, end markers."""
    lines = content.strip().split('\n')
    body_lines = []
    skip_patterns = [
        r'^#\s', r'^本期', r'^转载', r'^预览', r'^__+$',
        r'^刑事审判庭', r'^研究室', r'^撰写：', r'^作者：',
        r'^华东政法', r'^本院青年', r'^北京大学', r'^中国政法',
        r'^西南政法', r'^上海二中院', r'^全日制', r'^法律硕士',
        r'^爱笑的', r'^修改于', r'^以上仅代表', r'^—\s*END',
        r'^\d+\s*$',
    ]
    for line in lines:
        stripped = line.strip()
        if not stripped:
            body_lines.append(line)
            continue
        if any(re.match(p, stripped) for p in skip_patterns):
            continue
        # Skip lines that are just author credits or metadata
        if re.match(r'^.{1,30}(法官|审判|助理|博士|硕士|学士|书记员|负责人)$', stripped):
            continue
        body_lines.append(line)
    return '\n'.join(body_lines).strip()

def generate_tags(title, content):
    """Generate tags based on title and content."""
    tags = ["至正法律研究", "上海二中法院"]

    keyword_tags = {
        "正当防卫": ["正当防卫", "刑事"],
        "防卫过当": ["正当防卫", "刑事"],
        "特殊防卫": ["正当防卫", "刑事"],
        "民事证据": ["民事诉讼", "证据规则"],
        "认罪认罚": ["认罪认罚", "刑事"],
        "监察调查": ["监察法", "职务犯罪"],
        "主动投案": ["自首", "监察法"],
        "自动投案": ["自首", "监察法"],
        "九民纪要": ["九民纪要", "民商事"],
        "公司印章": ["公司法", "民商事"],
        "隐名股东": ["公司法", "股权"],
        "冒名顶替": ["刑事"],
        "高考冒名顶替": ["刑事"],
        "民法典": ["民法典", "民商事"],
        "遗嘱": ["继承法", "婚姻家庭"],
        "离婚": ["婚姻家庭", "离婚"],
        "民间借贷": ["民间借贷", "民商事"],
        "担保": ["担保法", "民商事"],
        "建设工程": ["建设工程", "建筑工程"],
        "强制执行": ["强制执行", "执行"],
        "破产": ["破产法", "民商事"],
        "劳动": ["劳动法", "劳动与社会保障"],
        "工伤": ["工伤保险", "劳动与社会保障"],
        "个人信息": ["个人信息保护", "民商事"],
        "著作权": ["著作权", "知识产权"],
        "商标": ["商标法", "知识产权"],
        "专利": ["专利法", "知识产权"],
        "刑事": ["刑事", "刑法"],
        "民事": ["民事", "民商事"],
        "行政": ["行政法", "行政诉讼"],
        "一房二卖": ["房屋买卖", "民商事"],
        "买房跳单": ["房屋买卖", "民商事"],
        "二手房": ["房屋买卖", "民商事"],
        "敲诈勒索": ["敲诈勒索", "刑事"],
        "利用信息网络": ["网络犯罪", "刑事"],
        "代孕": ["婚姻家庭", "民商事"],
        "亲子关系": ["婚姻家庭", "民商事"],
        "夫妻": ["婚姻家庭", "婚姻"],
        "情侣": ["婚姻家庭", "恋爱财产"],
        "借名买房": ["房屋买卖", "民商事"],
        "执行": ["强制执行", "执行"],
        "证券": ["证券法", "金融"],
        "醉酒": ["危险驾驶", "刑事"],
        "代为": ["民商事"],
        "股东": ["公司法", "股权"],
        "股权转让": ["公司法", "股权"],
        "破产": ["破产法", "民商事"],
        "债务": ["债务", "民商事"],
        "借贷": ["民间借贷", "民商事"],
        "保证": ["担保法", "民商事"],
    }

    for kw, tgs in keyword_tags.items():
        if kw in content or kw in title:
            for tg in tgs:
                if tg not in tags:
                    tags.append(tg)

    return tags

def get_related(content):
    """Get related links based on content."""
    related = []
    if "正当防卫" in content:
        related.append("[[concept_正当防卫]]")
    if "九民纪要" in content:
        related.append("[[entity_九民纪要]]")
    if "公司印章" in content:
        related.append("[[concept_公司法人人格否认]]")
    if "隐名股东" in content or "股东资格" in content:
        related.append("[[concept_有限责任公司]]")
    if "民法典" in content:
        related.append("[[concept_中华人民共和国民法典]]")
    if "民事证据" in content or "举证责任" in content:
        related.append("[[concept_民事诉讼证据]]")
    if "认罪认罚" in content:
        related.append("[[concept_认罪认罚]]")
    if "主动投案" in content or "自动投案" in content:
        related.append("[[concept_自首]]")
    if "高考冒名顶替" in content or "冒名顶替" in content:
        related.append("[[concept_伪造国家机关证件罪]]")
    if "敲诈勒索" in content:
        related.append("[[concept_敲诈勒索罪]]")
    if "危险驾驶" in content or "醉酒驾驶" in content:
        related.append("[[concept_危险驾驶罪]]")
    if "劳动" in content or "工伤" in content:
        related.append("[[concept_工伤保险待遇]]")
    if "建设工程" in content:
        related.append("[[concept_建设工程施工合同]]")
    if not related:
        related.append("[[concept_上海二中院审判研究]]")
    return related

def process_file(src_path):
    """Process a single source file and return the wiki content."""
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()

    title = extract_title(content)
    if not title:
        print(f"  [WARN] Could not extract title from {src_path.name}")
        title = src_path.stem

    clean_title = re.sub(r'[\n\r]+', '', title)
    clean_title = re.sub(r'[\\/:\*\?"<>|]', '', clean_title)
    clean_title = re.sub(r'\s+', ' ', clean_title).strip()

    import datetime
    today = "2026-05-11"

    tags = generate_tags(title, content)
    related = get_related(content)

    # Fix source - single bracket pair around filename
    source_file = src_path.name
    frontmatter = f"""---
title: {clean_title}
type: summary
category: 诉讼与仲裁
created: {today}
updated: {today}
tags: [{', '.join(tags)}]
source: [{source_file}]
related: [{', '.join(related)}]
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{source_file}]] |
| 类型 | 司法实务研究 |
| 发布日期 | {today} |
| 关键词 | {', '.join(tags)} |

## 核心观点

"""

    body = extract_body(content)

    # Try to split into major sections (numbered sections like "1", "2", "3")
    # First normalize whitespace
    body = re.sub(r'\n{3,}', '\n\n', body)

    # Split on numbered sections
    sections = re.split(r'\n(?=\*\*\d+\s*\*\*)', body)
    if len(sections) > 1:
        for i, section in enumerate(sections):
            section = section.strip()
            if not section:
                continue
            # Try to extract section heading
            heading_match = re.search(r'\*\*(\d+)\s*\*\*(.*?)(?=\n|$)', section)
            if heading_match and i > 0:
                heading_text = heading_match.group(2).strip()
                if heading_text:
                    frontmatter += f"### {heading_text}\n\n"
                    frontmatter += re.sub(r'\*\*\d+\s*\*\*.*?(?=\n)', '', section, count=1).strip() + "\n\n"
                else:
                    frontmatter += section + "\n\n"
            else:
                frontmatter += section + "\n\n"
    else:
        # Try splitting on bold headings
        parts = re.split(r'\n(?=\*\*[^\*]{2,30}\*\*)', body)
        if len(parts) > 1:
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                m = re.search(r'\*\*([^\*]+)\*\*', part)
                if m:
                    heading = m.group(1).strip()
                    # Skip if it's just a number or short label
                    if len(heading) > 2 and not heading.isdigit():
                        frontmatter += f"### {heading}\n\n"
                frontmatter += re.sub(r'\*\*[^\*]+\*\*', '', part).strip() + "\n\n"
        else:
            frontmatter += body + "\n"

    # Clean up trailing artifacts
    lines = frontmatter.split('\n')
    cleaned = []
    skip_end = False
    for line in reversed(lines):
        stripped = line.strip()
        if skip_end:
            if not stripped:
                skip_end = False
            continue
        if re.match(r'^(—\s*END|以上仅代表|爱笑的|修改于)', stripped):
            skip_end = True
            continue
        cleaned.insert(0, line)
    frontmatter = '\n'.join(cleaned).strip()

    return frontmatter, clean_title

def main():
    src_files = sorted(SOURCE_DIR.glob("*.md"))
    print(f"Found {len(src_files)} source files")

    existing = set(f.stem for f in TARGET_DIR.glob("summary_Court_上海二中院_至正法律研究_*.md"))
    print(f"Existing target files: {len(existing)}")

    created = 0
    skipped = 0

    for src_path in src_files:
        base_name = src_path.stem
        clean_name = re.sub(r'^\[\d{4}-\d{2}-\d{2}\]', '', base_name).strip()
        target_stem = f"summary_Court_上海二中院_至正法律研究_{clean_name}"

        if target_stem in existing:
            skipped += 1
            continue

        try:
            wiki_content, clean_title = process_file(src_path)
            target_path = TARGET_DIR / f"{target_stem}.md"

            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(wiki_content)

            created += 1
        except Exception as e:
            print(f"  [ERROR] {src_path.name}: {e}")

    print(f"\nDone: created={created}, skipped(existing)={skipped}")

if __name__ == "__main__":
    main()
