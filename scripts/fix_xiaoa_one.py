#!/usr/bin/env python3
"""Process one file with proper encoding handling."""

import re
import os
from pathlib import Path

SOURCE_FILE = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民法院/最高法-小案大道理-md/[2024-06-22]学生在校磕断牙学校要担责吗.md")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/summaries")
TARGET_DIR.mkdir(parents=True, exist_ok=True)

content = SOURCE_FILE.read_text(encoding="utf-8")

# Extract date
date_match = re.search(r"\[(\d{4}-\d{2}-\d{2})\]", SOURCE_FILE.name)
date_str = date_match.group(1).replace("-", "")  # "20240622"

# Extract title from first # heading
title_match = re.search(r"^#\s+(.+?)\s*$", content, re.MULTILINE)
title = title_match.group(1).strip() if title_match else "学生在校磕断牙学校要担责吗"

# Create summary content
key_points = [
    "案情：六年级学生小徐放学下楼时在楼梯台阶上摔倒，牙齿磕到墙面受伤",
    "争议焦点：学校是否存在过错、是否尽到教育管理职责",
    "裁判：法院驳回原告诉讼请求，学校不承担侵权责任",
    "原理：学校已常态化进行安全教育，设施有安全提示标志，已尽到教育管理职责",
    "意义：明确"孩子虽在校、家长也有责、校园安全须共同守护"的理念",
]

frontmatter = f"""---
title: {title}
type: summary
created: 2026-05-11
updated: 2026-05-11
tags: [司法案例, 最高人民法院, 小案大道理, 校园安全]
source: sources/微信公号资料/最高人民法院/最高法-小案大道理-md/{SOURCE_FILE.name}
related: []
---

## 核心要点

- {key_points[0]}
- {key_points[1]}
- {key_points[2]}
- {key_points[3]}
- {key_points[4]}

## 案情概述

2024年的一天傍晚，六年级的小徐跟随老师和同学们一起放学下楼，在从三楼下至二楼的过程中，小徐在楼梯台阶上不小心摔倒，跌至楼梯间的平台转角处，牙齿磕到了墙面。带队老师发现小徐摔倒后，立即联系家长并陪同送医。经医院诊断，小徐有一颗牙齿折断、唇挫伤擦伤。小徐父亲诉至法院，要求学校承担医疗费及赔偿合计8万元。

法院经审理认为，根据现场勘验及证据，小徐摔倒受伤并非楼梯等设施场所缺陷导致，亦非学校过错行为导致。学校已常态化开展安全警示教育，楼梯有安全提示标志，已尽到教育管理职责。在小徐受伤后，学校及时通知家长、陪同就医、配合调查，已履行必要管理职责。据此，法院驳回原告的诉讼请求。

**裁判结果**：驳回原告的诉讼请求，学校不承担侵权责任

**法官心语**：《民法典》第1200条规定，限制民事行为能力人在学校学习期间受到人身损害，学校未尽到教育、管理职责的，应当承担侵权责任。校园伤害事件中认定侵权责任，不能仅因事故发生在校园即认定学校一定负有责任。

**代表点评**：本案以"小案例"阐释"大道理"，明确通过审查校方教育和管理职责来厘清校园安全事故中学校的权责，让保护未成年合法权益和维护学校正常教学管理秩序达成统一。
"""

# Save file - use safe filename
safe_title = re.sub(r'[^一-龥a-zA-Z0-9]', '', title)  # keep only Chinese, letters, numbers
safe_title = safe_title[:25]  # limit length
output_name = f"summary_{date_str}_最高法_小案大道理_{safe_title}.md"
output_path = TARGET_DIR / output_name

output_path.write_text(frontmatter, encoding="utf-8")
print(f"Created: {output_name}")