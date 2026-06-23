#!/usr/bin/env python3
"""
Batch ingest 最高法凡人小事 md files into wiki/summaries/
Processes 180 files in parallel using multiprocessing.
"""
import os
import re
import json
from pathlib import Path
from datetime import datetime
from multiprocessing import Pool, cpu_count

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
SOURCE_DIR = VAULT_ROOT / "sources/微信公号资料/最高人民法院/最高法-凡人小事-md"
TARGET_DIR = VAULT_ROOT / "wiki/summaries"
SCRIPT_DIR = VAULT_ROOT / "scripts"

TARGET_DIR.mkdir(parents=True, exist_ok=True)

def process_single_file(args):
    """Process a single source file and write wiki summary."""
    src_path, idx, total = args
    try:
        content = src_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Extract title from line 1 (after "# ")
        title = ""
        for line in lines:
            line = line.strip()
            if line.startswith("# "):
                title = line[2:].strip()
                break

        if not title:
            title = src_path.stem

        # Clean title: remove date prefix from filename if present
        # Filename format: [YYYY-MM-DD]标题.md
        clean_title = re.sub(r"^\[\d{4}-\d{2}-\d{2}]\s*", "", title)

        # Get filename for source reference
        src_filename = src_path.name

        # Extract date from filename for frontmatter
        date_match = re.search(r"\[(\d{4}-\d{2}-\d{2})]", src_filename)
        date_str = date_match.group(1) if date_match else "2024-01-01"

        # Extract keywords/themes from content for tags
        tags = ["凡人小事", "最高人民法院", "司法为民"]
        content_lower = content.lower()

        # Add specific tags based on content analysis
        if "赡养" in content or "老人" in content or "养老" in content:
            tags.append("赡养纠纷")
        if "执行" in content:
            tags.append("执行案件")
        if "调解" in content:
            tags.append("诉前调解")
        if "未成年人" in content or "孩子" in content or "少年" in content:
            tags.append("未成年人保护")
        if "妇女" in content or "家暴" in content:
            tags.append("妇女儿童权益")
        if "劳动" in content or "务工" in content or "讨薪" in content:
            tags.append("劳动争议")
        if "婚姻" in content or "家庭" in content or "离婚" in content:
            tags.append("婚姻家庭")
        if "社区" in content:
            tags.append("社区治理")
        if "农村" in content or "乡村" in content or "田间" in content:
            tags.append("乡村振兴")
        if "企业" in content or "营商" in content:
            tags.append("营商环境")

        # Extract judge name if present
        judge_name = ""
        name_patterns = [
            r"法官(\S{2,4})",
            r"(\S{2,4})法官",
            r"法官兼\S+(\S{2,4})",
        ]
        for pattern in name_patterns:
            match = re.search(pattern, content)
            if match:
                possible_name = match.group(1)
                if len(possible_name) >= 2 and len(possible_name) <= 4:
                    judge_name = possible_name
                    break

        # Extract court name if present
        court_name = ""
        court_patterns = [
            r"(\S+法院)",
            r"(\S+县人民法院)",
            r"(\S+市\S+区人民法院)",
        ]
        for pattern in court_patterns:
            match = re.search(pattern, content)
            if match:
                court_name = match.group(1)
                break

        # Extract key story points
        key_points = []
        # Find quotes or key statements
        for line in lines:
            if "说：" in line or "表示" in line or "体会到" in line:
                clean_line = line.strip()
                if len(clean_line) > 10 and len(clean_line) < 200:
                    key_points.append(clean_line[:150])

        # Get article body (skip header lines until content starts)
        body_lines = []
        in_body = False
        for line in lines:
            if line.strip() and not line.startswith("#") and not line.startswith("**"):
                in_body = True
            if in_body:
                body_lines.append(line)

        body = "\n".join(body_lines)
        # Remove source/author footer
        body = re.sub(r"来源：.*", "", body)
        body = re.sub(r"作者：.*", "", body)
        body = re.sub(r"编辑：.*", "", body)
        body = re.sub(r"预览时标签.*", "", body)
        body = re.sub(r"__", "", body)
        body = body.strip()

        # Truncate body for summary if too long
        if len(body) > 2000:
            body = body[:2000] + "\n\n（......）"

        # Generate frontmatter
        frontmatter = f"""---
title: {clean_title}
type: summary
category: 诉讼与仲裁
created: 2026-05-11
updated: 2026-05-11
tags: [{", ".join(tags)}]
source: "sources/微信公号资料/最高人民法院/最高法-凡人小事-md/{src_filename}"
related: []
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{src_filename}]] |
| 类型 | 人民法院凡人小事 |
| 关键词 | {", ".join(tags)} |
| 核心主题 | 司法为民 / 基层法官故事 |

"""

        # Add judge info if found
        if judge_name:
            frontmatter += f"**法官**：{judge_name}　　"
        if court_name:
            frontmatter += f"**法院**：{court_name}\n\n"

        # Generate document body
        frontmatter += f"## 📖 正文\n\n{body}\n\n"

        # Add key quotes/insights if available
        if key_points:
            frontmatter += "## 💬 法官心声\n\n"
            for i, point in enumerate(key_points[:3], 1):
                frontmatter += f"{i}. {point}\n\n"

        # Write output file
        # Clean title for filename (remove special chars)
        safe_title = re.sub(r'[【】\[\]（）\(\)《》<>:,"\'\?？\/\\|]', '', clean_title)
        safe_title = safe_title[:80]  # Limit filename length
        out_filename = f"summary_CourtFa_最高法_凡人小事_{safe_title}.md"
        out_path = TARGET_DIR / out_filename

        # Handle duplicate filenames
        counter = 1
        while out_path.exists():
            out_filename = f"summary_CourtFa_最高法_凡人小事_{safe_title}_{counter}.md"
            out_path = TARGET_DIR / out_filename
            counter += 1

        out_path.write_text(frontmatter, encoding="utf-8")

        return (str(src_path), str(out_path), True, "")
    except Exception as e:
        return (str(src_path), "", False, str(e))


def main():
    # Get all source files
    source_files = sorted(SOURCE_DIR.glob("*.md"))
    print(f"Found {len(source_files)} source files")

    # Prepare arguments
    args_list = [(f, i, len(source_files)) for i, f in enumerate(source_files)]

    # Process in parallel
    num_workers = min(cpu_count() * 2, 16)
    print(f"Processing with {num_workers} workers...")

    results = []
    with Pool(num_workers) as pool:
        for result in pool.imap_unordered(process_single_file, args_list):
            results.append(result)
            if result[2]:
                print(f"[{len(results)}/{len(source_files)}] OK: {Path(result[0]).name}")
            else:
                print(f"[{len(results)}/{len(source_files)}] FAIL: {Path(result[0]).name} - {result[3]}")

    # Summary
    success = sum(1 for r in results if r[2])
    failed = [r for r in results if not r[2]]

    print(f"\n=== SUMMARY ===")
    print(f"Total: {len(results)}")
    print(f"Success: {success}")
    print(f"Failed: {len(failed)}")

    if failed:
        print("\nFailed files:")
        for f in failed:
            print(f"  - {Path(f[0]).name}: {f[3]}")

    # Verify output count
    output_files = list(TARGET_DIR.glob("summary_CourtFa_最高法_凡人小事_*.md"))
    print(f"\nOutput files in wiki/summaries/: {len(output_files)}")


if __name__ == "__main__":
    main()
