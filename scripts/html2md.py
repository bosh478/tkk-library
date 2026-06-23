#!/usr/bin/env python3
"""
html2md.py - HTML → Markdown 转换器(markdownify 主路径)

职责:
  1. 接受 HTML 字符串或文件
  2. 用 markdownify 转 Markdown
  3. 移除噪声标签(<script> <style> <nav> <footer> <aside> <noscript>)
  4. 可选加 frontmatter(--frontmatter-file 或 --meta)
  5. 写到 stdout 或文件

主路径: markdownify(pip,质量最优,处理 95% HTML 标签)
失败哲学: 缺依赖 → sys.exit(2) + 修复指引(per feedback-no-design-degradation-2026-06-22)
不预埋: urllib / html.parser / 自写标签映射等降级路径

依赖: pip install markdownify (= beautifulsoup4 + soupsieve)
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

# 主路径依赖: markdownify
try:
    import markdownify
except ImportError as e:
    print(
        "[FAIL] 缺依赖 markdownify\n"
        "       原因: pip 包未安装或 Python 环境不一致\n"
        "       修复: pip install --break-system-packages markdownify\n"
        "       验证: python3 -c 'import markdownify; print(\"ok\")'\n"
        f"       原始错误: {e}",
        file=sys.stderr,
    )
    sys.exit(2)

# 默认要从 HTML 剥除的噪声标签
DEFAULT_STRIP_TAGS = [
    "script", "style", "nav", "footer", "aside",
    "noscript", "iframe", "form", "button", "input",
    "header.banner", "div.ad", "div.advertisement",
    "div.cookie-banner", "div.popup", "div.modal",
]


def convert_html_to_md(
    html: str,
    strip_tags: Optional[list] = None,
    keep_all_tags: bool = False,
    heading_style: str = "ATX",
    bullets: str = "-",
    code_language_callback=None,
) -> str:
    """
    把 HTML 字符串转 Markdown。

    主路径: markdownify.markdownify()。
    strip_tags: 显式列出要从 BeautifulSoup parse 阶段就剥除的标签(如 ['script','style','nav'])。
    keep_all_tags: True 时不剥任何标签(默认 False = 剥 DEFAULT_STRIP_TAGS)。
    """
    # markdownify API: strip_tags 是 list(待剥除标签名);strip 是 bool(剥除空白,与"是否剥标签"无关)
    if keep_all_tags:
        strip_tags = []
    else:
        strip_tags = strip_tags if strip_tags is not None else DEFAULT_STRIP_TAGS

    md = markdownify.markdownify(
        html,
        heading_style=heading_style,
        bullets=bullets,
        strip_tags=strip_tags,
        code_language_callback=code_language_callback,
    )
    # 收敛多余空行(>2 个连续空行 → 2 个)
    lines = md.split("\n")
    out_lines = []
    blank_count = 0
    for line in lines:
        if line.strip() == "":
            blank_count += 1
            if blank_count <= 2:
                out_lines.append(line)
        else:
            blank_count = 0
            out_lines.append(line)
    return "\n".join(out_lines).strip() + "\n"


def build_frontmatter(meta: dict) -> str:
    """把 dict 转 YAML frontmatter 块。"""
    lines = ["---"]
    for k, v in meta.items():
        if v is None:
            lines.append(f"{k}: null")
        elif isinstance(v, list):
            if not v:
                lines.append(f"{k}: []")
            else:
                lines.append(f"{k}:")
                for item in v:
                    lines.append(f"  - {item}")
        elif isinstance(v, str) and (":" in v or "#" in v or v.startswith("-") or v.startswith('"')):
            escaped = v.replace('"', '\\"')
            lines.append(f'{k}: "{escaped}"')
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def read_input(input_arg: Optional[str]) -> str:
    """读输入 HTML(string 字面 / 文件路径 / stdin)。"""
    if input_arg is None:
        # 从 stdin 读
        return sys.stdin.read()
    p = Path(input_arg)
    if p.exists() and p.is_file():
        return p.read_text(encoding="utf-8")
    # 视为字面 HTML 字符串
    return input_arg


def main():
    parser = argparse.ArgumentParser(
        description="HTML → Markdown 转换器(markdownify 主路径)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 文件 → 文件
  python html2md.py input.html -o output.md

  # 文件 → stdout
  python html2md.py input.html

  # 加 frontmatter
  python html2md.py input.html -o output.md \\
    --meta title="原文章标题" \\
    --meta author="张三" \\
    --meta publish_date="2026-06-22" \\
    --meta tier=T1

  # 从 stdin
  cat article.html | python html2md.py -o output.md

  # 字面 HTML 字符串
  python html2md.py '<h1>Hi</h1><p>world</p>' -o out.md
        """,
    )
    parser.add_argument("input", nargs="?",
                        help="输入 HTML(文件路径 / 字面字符串 / 留空从 stdin)")
    parser.add_argument("-o", "--output",
                        help="输出 .md 文件路径(留空写 stdout)")
    parser.add_argument("--meta", action="append", default=[],
                        metavar="KEY=VALUE",
                        help="frontmatter 字段(可多次使用,如 --meta title=foo)")
    parser.add_argument("--meta-file",
                        help="从 YAML 文件读 frontmatter 字段(键值对)")
    parser.add_argument("--no-frontmatter", action="store_true",
                        help="不加 frontmatter")
    parser.add_argument("--keep-all-tags", action="store_true",
                        help="不剥除噪声标签(默认剥 script/style/nav 等)")

    args = parser.parse_args()

    # 读 HTML
    html = read_input(args.input)
    if not html.strip():
        print("[FAIL] 输入 HTML 为空", file=sys.stderr)
        sys.exit(1)

    # 解析 --meta
    meta = {}
    if args.meta_file:
        meta_path = Path(args.meta_file)
        if not meta_path.exists():
            print(f"[FAIL] meta 文件不存在: {args.meta_file}", file=sys.stderr)
            sys.exit(1)
        # 简单解析: 每行 "key: value" 或 "key=value"
        for line in meta_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
            elif "=" in line:
                k, v = line.split("=", 1)
                meta[k.strip()] = v.strip()
    for kv in args.meta:
        if "=" not in kv:
            print(f"[FAIL] --meta 格式错(需 KEY=VALUE): {kv}", file=sys.stderr)
            sys.exit(1)
        k, v = kv.split("=", 1)
        meta[k.strip()] = v.strip()

    # 转换
    body_md = convert_html_to_md(html, keep_all_tags=args.keep_all_tags)

    # 加 frontmatter
    if args.no_frontmatter or not meta:
        out_text = body_md
    else:
        out_text = build_frontmatter(meta) + "\n" + body_md

    # 输出
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out_text, encoding="utf-8")
        print(f"[OK] 写入 {out_path} ({len(out_text)} bytes)", file=sys.stderr)
    else:
        sys.stdout.write(out_text)


if __name__ == "__main__":
    main()
