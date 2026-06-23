#!/usr/bin/env python3
"""Batch ingest 上海高院案例参考册 to wiki/syntheses/"""

import os
import re
import json
from pathlib import Path

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/上海高院/上海高院-案例参考册-md")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/syntheses")
TARGET_DIR.mkdir(parents=True, exist_ok=True)

def extract_title(content):
    """Extract title from first # heading."""
    match = re.search(r'^#\s+(.+)丨案例参考册', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "未命名"

def extract_keywords(content):
    """Extract keywords from 关键词 line."""
    match = re.search(r'\*\*关键词\*\*\s*\n\s*([^\n]+)', content)
    if match:
        return match.group(1).strip().replace('：', '/').replace(':', '/').replace('、', '/').replace(' ', '')
    return ""

def extract_tags(content):
    """Extract tags from content."""
    tags = []
    # Extract from 关键词
    kw_match = re.search(r'\*\*关键词\*\*(.+?)(?:\n|$)', content)
    if kw_match:
        kw_text = kw_match.group(1).strip()
        # Split by various delimiters
        parts = re.split(r'[/、\s]+', kw_text)
        tags.extend([p.strip() for p in parts if p.strip() and len(p.strip()) > 1])
    return tags[:8]  # Limit to 8 tags

def extract_publish_date(filename):
    """Extract date from filename like [2022-02-24]..."""
    match = re.search(r'\[(\d{4}-\d{2}-\d{2})\]', filename)
    if match:
        return match.group(1)
    return "2022-01-01"

def extract_case_level(content):
    """Extract case level from content."""
    if '参考性案例' in content:
        # Extract case number
        match = re.search(r'[参考性案例第例]+(\d+)号', content)
        if match:
            return f"⭐⭐⭐ (参考性案例第{match.group(1)}号)"
    return "⭐⭐⭐ (参考性案例)"

def extract_problem_awareness(content):
    """Extract one sentence about core legal issue."""
    # Try to find from 裁判要旨/裁判要点
    patterns = [
        r'\*\*裁判要旨\*\*(.+?)(?:\n\*\*|$)',
        r'\*\*裁判要点\*\*(.+?)(?:\n\*\*|$)',
        r'\*\*裁判思路\*\*(.+?)(?:\n|$)',
    ]
    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            text = match.group(1).strip()
            # Take first sentence (first 150 chars)
            sentence = text[:150].split('\n')[0].strip()
            if len(sentence) > 20:
                return sentence
    return "涉及民事/刑事/行政法律问题待明确"

def extract_key_points(content):
    """Extract key points including 裁判要旨 (>=100 chars)."""
    # Find 裁判要旨/裁判要点 section
    patterns = [
        r'\*\*裁判要旨\*\*(.+?)(?:\*\*法官解读|\*\*基本案情|\*\*裁判结果|$)',
        r'\*\*裁判要点\*\*(.+?)(?:\*\*法官解读|\*\*基本案情|\*\*裁判结果|$)',
    ]
    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            text = match.group(1).strip()
            # Clean markdown formatting
            text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
            text = re.sub(r'\*(.+?)\*', r'\1', text)
            text = re.sub(r'\n+', '\n', text)
            text = text.strip()
            if len(text) >= 100:
                return text
    return "详见裁判理由部分"

def extract_judge_reason(content):
    """Extract 裁判理由 section."""
    patterns = [
        r'\*\*裁判理由\*\*(.+?)(?:\*\*相关法条|\*\*案例评析|$)',
        r'法院生效裁判认为[，：](.+?)(?:\*\*相关法条|$)',
    ]
    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            text = match.group(1).strip()
            text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
            return text[:800]
    return ""

def extract_result(content):
    """Extract 裁判结果 section."""
    patterns = [
        r'\*\*裁判结果\*\*\s*\n(.+?)(?:\*\*|$)',
        r'上海市.{0,20}法院于\d{4}年\d{1,2}月\d{1,2}日作出.+?判决[：:](.+?)(?:\*\*|$)',
    ]
    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            text = match.group(1).strip()
            text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
            return text[:500]
    return ""

def extract_related_laws(content):
    """Extract related law articles."""
    laws = []
    match = re.search(r'\*\*相关法条\*\*(.+?)(?:\*\*|$)', content, re.DOTALL)
    if match:
        text = match.group(1)
        law_matches = re.findall(r'《[^》]+》[^。\n]*第?\d+条', text)
        laws.extend([l.strip() for l in law_matches][:10])
    return laws

def create_frontmatter(title, filename, content, tags):
    """Create frontmatter dict."""
    publish_date = extract_publish_date(filename)
    case_level = extract_case_level(content)
    problem = extract_problem_awareness(content)
    key_points = extract_key_points(content)
    judge_reason = extract_judge_reason(content)
    result = extract_result(content)
    related_laws = extract_related_laws(content)

    fm = {
        "title": title,
        "type": "synthesis",
        "created": "2026-05-11",
        "updated": "2026-05-11",
        "tags": tags,
        "source": f"sources/微信公号资料/上海高院/上海高院-案例参考册-md/{filename}",
        "related": related_laws,
        "案例分级": case_level,
        "问题意识": problem,
        "裁判要旨": key_points[:500] if len(key_points) > 500 else key_points,
    }
    return fm

def process_file(filepath):
    """Process a single file and return target path and content."""
    filename = filepath.name
    content = filepath.read_text(encoding='utf-8')

    # Extract title
    title = extract_title(content)
    # Create safe filename
    safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
    safe_title = safe_title[:80]  # Limit length
    target_name = f"Court_上海高院_案例参考册_{safe_title}.md"
    target_path = TARGET_DIR / target_name

    # Extract tags
    tags = extract_tags(content)

    # Create frontmatter
    fm = create_frontmatter(title, filename, content, tags)

    # Build content
    key_points = extract_key_points(content)
    judge_reason = extract_judge_reason(content)
    result = extract_result(content)

    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, list):
            if v:
                lines.append(f"{k}: [{', '.join(repr(str(x)) for x in v)}]")
            else:
                lines.append(f"{k}: []")
        else:
            # Escape special chars in value
            v_str = str(v).replace('"', '\\"')
            lines.append(f'{k}: "{v_str}"')
    lines.append("---")
    lines.append("")
    lines.append(f"## 裁判要旨")
    lines.append("")
    lines.append(key_points)
    lines.append("")

    if judge_reason:
        lines.append("## 裁判理由")
        lines.append("")
        lines.append(judge_reason)
        lines.append("")

    if result:
        lines.append("## 裁判结果")
        lines.append("")
        lines.append(result)
        lines.append("")

    # Add related laws
    if fm.get("related"):
        lines.append("## 相关法条")
        lines.append("")
        for law in fm["related"]:
            lines.append(f"- {law}")
        lines.append("")

    return target_path, "\n".join(lines)

def main():
    files = list(SOURCE_DIR.glob("*.md"))
    print(f"Found {len(files)} files to process")

    processed = 0
    errors = []

    for filepath in sorted(files):
        try:
            target_path, content = process_file(filepath)

            # Handle duplicate names by adding number
            counter = 1
            original_target = target_path
            while target_path.exists():
                target_path = original_target.parent / f"{original_target.stem}_{counter}{original_target.suffix}"
                counter += 1

            target_path.write_text(content, encoding='utf-8')
            processed += 1

            if processed % 20 == 0:
                print(f"Processed {processed}/{len(files)}")

        except Exception as e:
            errors.append(f"{filepath.name}: {str(e)}")
            print(f"Error processing {filepath.name}: {e}")

    print(f"\nCompleted: {processed}/{len(files)}")
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")

if __name__ == "__main__":
    main()