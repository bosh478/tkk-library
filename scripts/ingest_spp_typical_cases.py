"""
Batch ingest SPP Typical Case files (201 files) from sources to wiki/syntheses/
"""
import re
import os
import json
from pathlib import Path
from datetime import datetime

VAULT = Path("D:/AI agent/tkk-library")
SOURCES_DIR = VAULT / "sources/微信公号资料/最高人民检察院/最高检-典型案例-md"
TARGET_DIR = VAULT / "wiki/syntheses"
LOG_FILE = VAULT / "log.md"

def extract_title_from_content(content):
    """Extract article title from # heading."""
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('# ') and len(line) > 2:
            # Remove leading # and spaces
            title = line.lstrip('#').strip()
            return title
    return None

def clean_title(title):
    """Remove date prefix and clean title."""
    # Remove date prefix like [2021-01-14] or [2021-01-14]全文
    title = re.sub(r'^\[\d{4}-\d{2}-\d{2}\](全文)?', '', title)
    # Remove 最高检发布 prefix
    title = re.sub(r'^全文?最高检发布', '', title)
    title = re.sub(r'^最高检公安部发布', '', title)
    title = title.strip()
    return title

def make_filename(title):
    """Create safe filename from title."""
    # Remove special chars
    safe = re.sub(r'[【】\[\]（）\(\)（）""'']', '', title)
    safe = re.sub(r'\s+', '_', safe)
    safe = re.sub(r'[^\w一-鿿_-]', '', safe)
    # Truncate if too long
    if len(safe) > 80:
        safe = safe[:80]
    return safe

def extract_case_info(content):
    """Extract case basic info, key points, legal issues."""
    lines = content.split('\n')

    # Extract case numbers
    case_numbers = []
    for line in lines:
        nums = re.findall(r'[一-鿿].*?[检法院]\s*[一-鿿]第?[0-9]+号', line)
        if nums and '第' in line:
            case_numbers.extend(nums)

    # Extract prosecutor info
    prosecutors = []
    for line in lines:
        matches = re.findall(r'[一-鿿]+检察院', line)
        if matches:
            prosecutors.extend(matches)

    # Extract parties
    parties = []
    for line in lines:
        matches = re.findall(r'[一-鿿]{2,4}(?:一-鿿)*(?:多)?(?:人|案|分子|被告)', line)
        if matches and len(matches[0]) >= 2:
            parties.extend(matches[:3])

    # Extract key points (typical significance sections)
    key_points = []
    in_significance = False
    sig_lines = []
    for line in lines:
        if '典型意义' in line or '典型价值' in line or '法律要旨' in line:
            in_significance = True
            continue
        if in_significance and line.strip().startswith('**') and ('案例' in line or '法律' in line or '规定' in line):
            if sig_lines:
                key_points.append(' '.join(sig_lines[:3]))
                sig_lines = []
            sig_lines.append(line.strip())
        elif in_significance:
            sig_lines.append(line.strip())
            if len(sig_lines) > 5:
                key_points.append(' '.join(sig_lines[:4]))
                sig_lines = []

    if sig_lines:
        key_points.append(' '.join(sig_lines[:4]))

    # Extract legal issues (罪名/法条 mentions)
    legal_issues = []
    crime_pattern = r'([一-鿿]+罪)'
    for line in lines:
        if re.search(crime_pattern, line):
            crimes = re.findall(crime_pattern, line)
            legal_issues.extend([c for c in crimes if c not in legal_issues and len(c) > 2][:5])

    return {
        'case_numbers': list(dict.fromkeys(case_numbers))[:5],
        'prosecutors': list(dict.fromkeys(prosecutors))[:5],
        'parties': list(dict.fromkeys(parties))[:5],
        'key_points': key_points[:5],
        'legal_issues': legal_issues[:8]
    }

def build_tags(content, legal_issues):
    """Build appropriate tags from content."""
    tags_set = {"典型案例", "最高人民检察院"}

    # Detect subject area
    content_lower = content.lower()
    if '疫情' in content or '防控' in content or '新冠' in content:
        tags_set.add("疫情防控")
    if '网络' in content or '电信' in content or '诈骗' in content:
        tags_set.add("网络犯罪")
    if '未成年人' in content or '未成年' in content:
        tags_set.add("未成年人保护")
    if '公益诉讼' in content:
        tags_set.add("公益诉讼")
    if '行政' in content or '行政执法' in content:
        tags_set.add("行政检察")
    if '民事' in content or '审判' in content:
        tags_set.add("民事检察")
    if '刑事' in content:
        tags_set.add("刑事检察")
    if '企业' in content or '合规' in content or '公司' in content:
        tags_set.add("企业合规")
    if '环境' in content or '生态' in content:
        tags_set.add("生态环境")
    if '食品安全' in content:
        tags_set.add("食品安全")
    if '个人信息' in content or '数据' in content:
        tags_set.add("个人信息保护")

    # Add legal issue tags
    for issue in legal_issues[:3]:
        if issue.endswith('罪'):
            tags_set.add(issue)

    return sorted(list(tags_set))[:8]

def determine_related(legal_issues, case_info):
    """Build related links array."""
    related = []

    # Add legal concept links based on crimes
    for issue in legal_issues[:2]:
        if issue.endswith('罪'):
            # These will be linked if concept pages exist
            related.append(f"[[concept_{issue}]]")

    # Add prosecutor links
    for p in case_info['prosecutors'][:1]:
        if '检察院' in p:
            clean = p.replace('检察院', '').strip()
            if clean and len(clean) < 10:
                related.append(f"[[entity_{clean}人民检察院]]")

    return related[:3]

def build_problem_awareness(content, legal_issues):
    """Build one-sentence problem awareness."""
    if legal_issues:
        return f"涉及{legal_issues[0]}等罪名的认定与处理"
    if '疫情' in content:
        return "疫情防控期间违法犯罪行为的法律适用问题"
    if '网络' in content:
        return "网络空间治理中刑事法律适用问题"
    if '未成年人' in content:
        return "未成年人保护与犯罪预防的法律适用问题"
    return "检察机关依法履行法律监督职能的典型实践"

def process_file(src_path):
    """Process a single source file and return target path and content."""
    filename = src_path.name

    # Extract date from filename
    date_match = re.match(r'\[(\d{4}-\d{2}-\d{2})\]', filename)
    date_str = date_match.group(1) if date_match else "2021-01-01"

    # Read content
    content = src_path.read_text(encoding='utf-8')

    # Extract title
    title = extract_title_from_content(content)
    if not title:
        title = filename.replace('.md', '')

    # Clean title
    clean_t = clean_title(title)

    # Extract case info
    case_info = extract_case_info(content)

    # Build tags
    tags = build_tags(content, case_info['legal_issues'])

    # Build related
    related = determine_related(case_info['legal_issues'], case_info)

    # Build problem awareness
    problem_awareness = build_problem_awareness(content, case_info['legal_issues'])

    # Build output filename
    safe_name = make_filename(clean_t)
    target_filename = f"SPP_TypicalCase_{safe_name}.md"
    target_path = TARGET_DIR / target_filename

    # Check for duplicate filename
    counter = 1
    while target_path.exists():
        target_filename = f"SPP_TypicalCase_{safe_name}_{counter}.md"
        target_path = TARGET_DIR / target_filename
        counter += 1

    # Extract content body (everything after the title)
    body_lines = content.split('\n')
    body_start = 0
    for i, line in enumerate(body_lines):
        if line.strip().startswith('# ') and i > 0:
            body_start = i
            break

    body = '\n'.join(body_lines[body_start:])

    # Build frontmatter
    frontmatter = f"""---
title: {clean_t}
type: synthesis
created: 2026-05-11
updated: 2026-05-11
tags: [{', '.join(tags)}]
source: "sources/微信公号资料/最高人民检察院/最高检-典型案例-md/{filename}"
related: [{', '.join(related)}]
案例分级: ⭐⭐⭐⭐
问题意识: {problem_awareness}
---

{body}
"""

    return target_path, frontmatter, clean_t, filename

def main():
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    # Get all source files
    src_files = sorted(SOURCES_DIR.glob("*.md"))
    total = len(src_files)
    print(f"Found {total} source files")

    results = []
    errors = []

    for i, src_path in enumerate(src_files, 1):
        try:
            target_path, content, clean_t, orig_name = process_file(src_path)
            target_path.write_text(content, encoding='utf-8')
            results.append((orig_name, target_path.name, 'OK'))
            if i % 20 == 0:
                print(f"Processed {i}/{total}: {clean_t[:40]}")
        except Exception as e:
            errors.append((str(src_path), str(e)))
            print(f"ERROR {src_path.name}: {e}")

    print(f"\n=== SUMMARY ===")
    print(f"Total: {total}")
    print(f"Success: {len(results)}")
    print(f"Errors: {len(errors)}")

    # Verify count
    target_files = list(TARGET_DIR.glob("SPP_TypicalCase_*.md"))
    print(f"Target files: {len(target_files)}")

    # List errors if any
    if errors:
        print("\n=== ERRORS ===")
        for path, err in errors:
            print(f"  {path}: {err}")

    # Write to log
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    log_entry = f"""
## [2026-05-11] ingest | 最高检典型案例 (201 files)
- 操作: 消化 201 个最高检典型案例 md 文件
- 创建页面: {len(results)} 个 wiki/syntheses/ 页面
- 命名格式: SPP_TypicalCase_*.md
- 备注: {'无错误' if not errors else f'错误 {len(errors)} 个，见上方错误列表'}
"""
    if LOG_FILE.exists():
        existing = LOG_FILE.read_text(encoding='utf-8')
        log_entry = existing + log_entry
    LOG_FILE.write_text(log_entry, encoding='utf-8')
    print(f"\nLog written to {LOG_FILE}")

if __name__ == "__main__":
    main()
