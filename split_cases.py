#!/usr/bin/env python3
"""Split Criminal Trial Reference case files into individual synthesis pages."""

import re
import os
from pathlib import Path

SOURCE_DIR = Path("sources/《刑事审判参考》")
OUTPUT_DIR = Path("wiki/syntheses/Court_刑事审判参考")

def extract_ji_num(filename):
    """Extract volume number from filename like '《刑事审判参考 总第101辑》.md'"""
    match = re.search(r'总第(\d+)辑', filename)
    if match:
        return int(match.group(1))
    # Handle combined volumes like "总第134-136辑"
    match = re.search(r'总第(\d+)-(\d+)辑', filename)
    if match:
        return int(match.group(1))  # Use first number
    return None

def extract_case_info(content):
    """Extract case number and title from case content."""
    # Pattern: [第XXXX号] followed by title (may be on same line or next line)
    match = re.search(r'\[第(\d+)号\](.*?)(?=\n##|\n#|$)', content, re.DOTALL)
    if match:
        case_num = match.group(1)
        title_part = match.group(2).strip()
        # Title is usually after the case number on the same line or next line
        # Example: "文某非法持有毒品案[第1038号]" or "文某非法持有毒品案\n[第1038号]"
        # Or: "[第1038号]\n文某非法持有毒品案"
        return case_num, title_part
    return None, None

def parse_case_body(content):
    """Extract the case body content, removing the case number header."""
    # Remove the [第XXXX号] marker from content
    body = re.sub(r'\[第\d+号\]', '', content, count=1).strip()
    return body

def clean_title(title):
    """Clean case title - remove extra whitespace, brackets content."""
    if not title:
        return None
    # Remove any remaining brackets and their content
    title = re.sub(r'\[.*?\]', '', title)
    # Clean up whitespace
    title = re.sub(r'\s+', ' ', title).strip()
    # Remove trailing markers like —— etc
    title = re.sub(r'——+$', '', title)
    return title if title else None

def split_cases(source_file):
    """Split a source file into individual cases."""
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all case markers - handle multiple styles:
    # 1. [第XXXX号] or ［第XXXX号］ - standard style
    # 2. ## [第 XXXX 号] ## Title - inline header style
    case_pattern = r'\[第(\d+)号\]|［第(\d+)号］'
    matches = list(re.finditer(case_pattern, content))

    cases = []
    for i, match in enumerate(matches):
        # Handle both bracket styles
        case_num = match.group(1) if match.group(1) else match.group(2)
        start = match.start()

        # Find end of the [第XXXX号] or ［第XXXX号］ marker
        bracket_end = match.end()

        # Check what follows the marker:
        # Body case formats:
        #   A: [XXXX号]\n\n# Title (markdown header)
        #   B: [XXXX号]\n\nTitle (plain text, no #)
        #   C: Title[XXXX号] (inline - TOC entry)
        following_text = content[bracket_end:bracket_end+100]

        # Check for markdown header format
        has_header = following_text.startswith('\n\n#') or following_text.startswith('\n#')

        # For non-header format, check if followed by text (not another marker right away)
        # Real case: [XXXX号]\n\nTitle\n\n[NEXT]
        # TOC entry: Title[XXXX号] - has text before the marker

        # TOC detection: if followed by description text (no header soon), it's TOC
        # Also check for list marker after newline
        is_toc = not has_header

        # Additional TOC pattern: has list marker right after newline
        if '\n' in following_text[:20] and not has_header:
            next_newline_idx = following_text.index('\n')
            next_line_content = following_text[next_newline_idx+1:next_newline_idx+10].lstrip()
            if next_line_content.startswith('-') or next_line_content.startswith('•'):
                is_toc = True

        if is_toc:
            continue  # Skip TOC entries

        # End is either next case or end of content
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)

        case_content = content[start:end]

        # Extract title - look for # header after the case marker
        title_match = re.search(r'\n#+\s*(.+?)\s*\n', case_content)
        if title_match:
            raw_title = title_match.group(1).strip()
        else:
            # Try inline pattern: "Title[第XXXX号]" at start of line
            title_match = re.search(r'^([^\[#\n]+?)\s*\[第\d+号\]', case_content, re.MULTILINE)
            if title_match:
                raw_title = title_match.group(1).strip()
            else:
                # Try: [第XXXX号]\nTitle (plain text format)
                title_match = re.search(r'^\[第\d+号\]\s*\n+\s*([^\n]+)', case_content, re.MULTILINE)
                if title_match:
                    raw_title = title_match.group(1).strip()
                else:
                    first_line = case_content.split('\n')[0]
                    raw_title = re.sub(r'\[第\d+号\]|［第\s*\d+\s*号］', '', first_line).strip()

        title = clean_title(raw_title)

        # Remove both bracket styles from body
        body = re.sub(r'\[第\d+号\]', '', case_content, count=1).strip()
        body = re.sub(r'［第\s*\d+\s*号］', '', body, count=1).strip()

        cases.append({
            'case_num': case_num,
            'title': title,
            'body': body
        })

    # Also handle inline header style: ## [第 XXXX 号] ## Title
    # Pattern: ## followed by case number in brackets, then ## followed by title
    # Handle both thin [ and full-width ［ brackets, with optional spaces
    inline_pattern = r'##\s*\[第\s*(\d+)\s*号\]|##\s*［第\s*(\d+)\s*号］'
    inline_matches = list(re.finditer(inline_pattern, content))

    for match in inline_matches:
        case_num = match.group(1) if match.group(1) else match.group(2)

        # Find the title - look for the ## that follows with the title
        # Pattern: ## [num] ## Title
        title_pattern = r'##\s*\[第\s*\d+\s*号\]\s*##\s*([^\n]+)|##\s*［第\s*\d+\s*号］\s*##\s*([^\n]+)'
        title_match = re.search(title_pattern, content[match.start():match.start()+200])
        if title_match:
            title = clean_title((title_match.group(1) or title_match.group(2)).strip())
        else:
            title = None

        # Get content - find next case or end
        start = match.start()
        next_match = None
        for im in inline_matches:
            if im.start() > start:
                next_match = im
                break

        end = next_match.start() if next_match else len(content)

        # Check if we already have this case (avoid duplicates based on case_num and similar position)
        existing = [c for c in cases if c['case_num'] == case_num and abs(cases.index(c) - start) < 10000]
        if existing:
            continue

        case_content = content[start:end]

        body = re.sub(r'##\s*\[第\s*\d+\s*号\]|##\s*［第\s*\d+\s*号］', '', case_content, count=1).strip()
        body = re.sub(r'##\s*', '', body).strip()  # Remove remaining ## markers

        cases.append({
            'case_num': case_num,
            'title': title or f'案例{case_num}',
            'body': body
        })

    return cases

def write_case_file(case_info, ji_num, source_file):
    """Write a single case to synthesis file."""
    case_num = case_info['case_num']
    title = case_info['title'] or f"案例{case_num}"
    body = case_info['body']

    # Create safe filename
    safe_title = re.sub(r'[^一-龥a-zA-Z0-9]', '_', title)
    safe_title = re.sub(r'_+', '_', safe_title).strip('_')

    filename = f"Court_刑事审判参考_{ji_num}辑_{case_num}号_{safe_title}.md"
    filepath = OUTPUT_DIR / filename

    frontmatter = f"""---
title: {title}
type: synthesis
created: 2026-04-22
updated: 2026-04-22
tags: [刑事审判参考, 第{ji_num}辑, 案例集]
case_num: {case_num}
ji_num: {ji_num}
source: [["{source_file}"]]
---

"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter + body)

    return filename

def main():
    # Get all source files sorted
    source_files = sorted(SOURCE_DIR.glob("*.md"))

    total_files = 0
    total_cases = 0

    for source_file in source_files:
        ji_num = extract_ji_num(source_file.name)
        if ji_num is None:
            print(f"Skipping: {source_file.name} (cannot extract volume number)")
            continue

        print(f"Processing: {source_file.name} (辑:{ji_num})")

        try:
            cases = split_cases(source_file)
            print(f"  Found {len(cases)} cases")

            for case in cases:
                filename = write_case_file(case, ji_num, source_file.name)
                total_cases += 1

            total_files += 1

        except Exception as e:
            print(f"  Error processing {source_file.name}: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n=== Summary ===")
    print(f"Processed {total_files} source files")
    print(f"Extracted {total_cases} cases")

if __name__ == '__main__':
    main()