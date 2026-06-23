#!/usr/bin/env python3
"""处理剩余律师指引"""

import re
from pathlib import Path

VAULT = Path("D:/AI agent/tkk-library")
WIKI = VAULT / "wiki/summaries"

files = [
    "sources/网络文章/20161101_律师办理行政诉讼案件操作指引2016.md",
    "sources/网络文章/20170602_律师代理机动车交通事故责任纠纷案件操作指引2017.md",
    "sources/网络文章/20181210_律师办理医疗纠纷案件操作指引2018.md",
    "sources/网络文章/20191105_律师办理商事诉讼业务操作指引2019.md",
]

CATS = {
    '劳动': '劳动与社会保障',
    '工伤': '劳动与社会保障',
    '医疗': '医药健康',
    '商事': '公司商事与合规',
    '行政': '政府与公共法律服务',
}

def get_cat(title):
    for k, v in CATS.items():
        if k in title:
            return v
    return '诉讼与仲裁'

for src in files:
    src_path = VAULT / src
    if not src_path.exists():
        print(f"SKIP: {src} not found")
        continue

    content = src_path.read_text(encoding='utf-8')

    # title
    m = re.search(r'^title:\s*"([^"]+)"', content, re.MULTILINE)
    if not m:
        m = re.search(r'^##\s+(.+)', content)
    title = m.group(1) if m else src_path.stem

    # date from published (handle quotes)
    m = re.search(r'^published:\s*"?(\d{4})-(\d{2})-(\d{2})"?', content, re.MULTILINE)
    if not m:
        # fallback: find first YYYY-MM-DD in content
        m = re.search(r'(\d{4})-(\d{2})-(\d{2})', content)
    pub_date = f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else "2026-01-01"
    date_str = pub_date.replace("-", "")

    cat = get_cat(title)

    # body
    lines = content.split('\n')
    body = []
    for line in lines:
        if line.startswith('## ') and body:
            break
        if line.strip():
            body.append(line)
            if len(body) >= 15:
                break

    wiki_name = f"summary_{date_str}_{title[:15]}.md"
    wiki_name = re.sub(r'[/\\:*?"<>|]', '', wiki_name)
    wiki_path = WIKI / wiki_name

    fm = f"""---
title: "{title}"
type: summary
category: {cat}
created: 2026-05-19
updated: 2026-05-19
tags: [律师业务指引]
source: "{src_path.name}"
---

## 正文

{chr(10).join(body)}

> 来源：{src_path.name}
"""

    wiki_path.write_text(fm, encoding='utf-8')
    print(f"OK: {title[:20]} -> {wiki_name}")