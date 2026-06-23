#!/usr/bin/env python3
"""Convert SKILL_SETUP_GUIDE.md to a single styled HTML file on desktop."""
from pathlib import Path
import markdown
from markdown.extensions.toc import TocExtension

SRC = Path(r"D:\AI agent\tkk-library\SKILL_SETUP_GUIDE.md")
DST = Path(r"C:\Users\汤康康\Desktop\SKILL_SETUP_GUIDE.html")

md_text = SRC.read_text(encoding="utf-8")

html_body = markdown.markdown(
    md_text,
    extensions=[
        "fenced_code",
        "tables",
        TocExtension(toc_depth="2-3", anchorlink=False),
        "nl2br",
        "sane_lists",
    ],
)

HTML = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>tkk-legal-ingest Skill 完整搭建指南</title>
<style>
  :root {{
    --bg: #ffffff;
    --fg: #1f2328;
    --muted: #57606a;
    --accent: #0969da;
    --accent-bg: #ddf4ff;
    --warn-bg: #fff8c5;
    --warn-border: #d4a72c;
    --code-bg: #f6f8fa;
    --border: #d0d7de;
    --ok: #1a7f37;
    --fail: #cf222e;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", "PingFang SC", sans-serif;
    color: var(--fg);
    background: var(--bg);
    max-width: 980px;
    margin: 0 auto;
    padding: 32px 48px 96px;
    line-height: 1.6;
    font-size: 15px;
  }}
  h1, h2, h3, h4 {{ line-height: 1.25; font-weight: 600; }}
  h1 {{ font-size: 2em; border-bottom: 1px solid var(--border); padding-bottom: 0.3em; margin-top: 0; }}
  h2 {{ font-size: 1.5em; border-bottom: 1px solid var(--border); padding-bottom: 0.3em; margin-top: 2em; }}
  h3 {{ font-size: 1.2em; margin-top: 1.6em; }}
  h4 {{ font-size: 1.05em; margin-top: 1.4em; }}
  p, ul, ol, table {{ margin: 0.6em 0; }}
  a {{ color: var(--accent); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  hr {{ border: 0; border-top: 1px solid var(--border); margin: 2em 0; }}
  code {{
    font-family: "Cascadia Code", "JetBrains Mono", Consolas, "Courier New", monospace;
    background: var(--code-bg);
    padding: 0.15em 0.35em;
    border-radius: 4px;
    font-size: 0.9em;
  }}
  pre {{
    background: var(--code-bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 14px 16px;
    overflow-x: auto;
    line-height: 1.45;
    font-size: 13px;
  }}
  pre code {{ background: transparent; padding: 0; font-size: inherit; }}
  blockquote {{
    border-left: 4px solid var(--accent);
    background: var(--accent-bg);
    margin: 1em 0;
    padding: 0.6em 1em;
    color: var(--fg);
    border-radius: 0 4px 4px 0;
  }}
  table {{
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
    font-size: 0.94em;
  }}
  th, td {{
    border: 1px solid var(--border);
    padding: 8px 12px;
    text-align: left;
    vertical-align: top;
  }}
  th {{ background: var(--code-bg); font-weight: 600; }}
  tr:nth-child(even) td {{ background: #fafbfc; }}
  ul, ol {{ padding-left: 2em; }}
  li {{ margin: 0.2em 0; }}
  li > p {{ margin: 0.4em 0; }}
  /* warning callout for ⚠️ paragraphs */
  p:has(> strong:first-child), li:has(> strong:first-child) {{}}
  /* Highlight warning markers */
  strong:contains("⚠️") {{ color: var(--warn-border); }}

  /* Side TOC */
  #toc {{
    position: sticky;
    top: 24px;
    float: right;
    width: 240px;
    margin-left: 24px;
    margin-right: -260px;
    background: var(--code-bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 14px 18px;
    font-size: 0.88em;
    max-height: calc(100vh - 48px);
    overflow-y: auto;
  }}
  #toc h2 {{ font-size: 1em; margin: 0 0 8px 0; border: 0; padding: 0; }}
  #toc ul {{ list-style: none; padding-left: 0; }}
  #toc ul ul {{ padding-left: 14px; font-size: 0.92em; }}
  #toc a {{ color: var(--muted); }}
  #toc a:hover {{ color: var(--accent); }}

  @media (max-width: 1100px) {{
    #toc {{ display: none; }}
  }}
  @media print {{
    body {{ max-width: none; padding: 12mm; font-size: 11pt; }}
    h2 {{ page-break-before: always; }}
    h2:first-of-type {{ page-break-before: avoid; }}
    pre {{ font-size: 9.5pt; }}
    table {{ font-size: 10pt; }}
    #toc {{ display: none; }}
  }}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

DST.write_text(HTML, encoding="utf-8")
print(f"Wrote {DST}")
print(f"Size: {DST.stat().st_size / 1024:.1f} KB")
print(f"Sections found: {html_body.count('<h2')}")