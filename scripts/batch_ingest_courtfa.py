#!/usr/bin/env python3
"""Batch ingest 最高法-小案大道理-md files to wiki/summaries/"""

import os
import re
from pathlib import Path

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民法院/最高法-小案大道理-md")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/summaries")
TARGET_DIR.mkdir(parents=True, exist_ok=True)

def extract_title(content):
    """Extract title from first # line, clean it"""
    lines = content.strip().split('\n')
    for line in lines:
        if line.startswith('#'):
            title = line.lstrip('#').strip()
            # Remove suffix like "——小案大道理" or patterns
            title = re.sub(r'[\s　]*[—―-]*\s*小案大道理.*$', '', title).strip()
            title = re.sub(r'[\s　]*[：:]\s*小案大道理.*$', '', title).strip()
            # Remove date prefix [YYYY-MM-DD]
            title = re.sub(r'^\[\d{4}-\d{2}-\d{2}\][\s　]*', '', title)
            title = re.sub(r'^\d{4}-\d{2}-\d{2}\s*', '', title)
            # Remove quotes, brackets, special chars from title
            title = title.strip('"\'（）()【】[]《》<>')
            return title
    return "未知标题"

def extract_key_content(content):
    """Extract key content sections, removing headers and noise"""
    # Remove the main # title line
    content = re.sub(r'^# [^\n]+\n', '', content)
    # Remove markdown section dividers
    content = re.sub(r'\* \* \*.*', '', content, flags=re.DOTALL)
    # Remove footer noise
    content = re.sub(r'更多精彩.*', '', content, flags=re.DOTALL)
    content = re.sub(r'预览时标签.*', '', content, flags=re.DOTALL)
    content = re.sub(r'修改于.*', '', content, flags=re.DOTALL)
    # Remove 开栏的话 section (from ** 开栏的话 ** to 案情回顾)
    content = re.sub(r'\*\*[^\n]*?开栏的话[^\n]*\*\*[\s\S]*?案情(回顾)?', '案情回顾', content)
    # Remove extra newlines
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content.strip()

def generate_wiki_content(title, content, source_file):
    """Generate wiki page content with frontmatter"""
    tags = ["小案大道理", "最高人民法院", "典型案例"]

    # Detect case type from content
    if "以危险方法危害公共安全" in content:
        tags.append("危害公共安全罪")
    if "高空抛物" in content:
        tags.append("高空抛物")
    if "侵权" in content or "赔偿" in content:
        tags.append("侵权责任")
    if "见义勇为" in content:
        tags.append("见义勇为")
    if "猝死" in content:
        tags.append("生命权")
    if "盗窃" in content:
        tags.append("盗窃罪")
    if "诈骗" in content:
        tags.append("诈骗罪")
    if "正当防卫" in content:
        tags.append("正当防卫")
    if "自助行为" in content:
        tags.append("自助行为")
    if "好意同乘" in content:
        tags.append("好意同乘")
    if "醉驾" in content or "危险驾驶" in content:
        tags.append("危险驾驶罪")
    if "妨害公务" in content:
        tags.append("妨害公务罪")
    if "精神损害" in content:
        tags.append("精神损害赔偿")
    if "劳动争议" in content or "工伤" in content:
        tags.append("劳动争议")
    if "交通事故" in content:
        tags.append("交通事故")
    if "医疗" in content:
        tags.append("医疗纠纷")
    if "教育" in content:
        tags.append("教育纠纷")
    if "个人信息" in content or "隐私" in content:
        tags.append("个人信息保护")
    if "野生动物" in content:
        tags.append("野生动物保护")
    if "枪支" in content:
        tags.append("非法持枪")
    if "毒品" in content:
        tags.append("毒品犯罪")
    if "开设赌场" in content:
        tags.append("开设赌场罪")
    if "帮助信息网络犯罪" in content:
        tags.append("帮信罪")
    if "污染环境" in content:
        tags.append("污染环境罪")
    if "消费者权益" in content or "欺诈" in content:
        tags.append("消费者权益")
    if "房屋买卖" in content or "房产" in content:
        tags.append("房产纠纷")
    if "借款" in content or "借贷" in content:
        tags.append("借贷纠纷")
    if "担保" in content:
        tags.append("担保纠纷")
    if "执行" in content or "失信" in content:
        tags.append("执行异议")
    if "醉驾" in content:
        tags.append("危险驾驶罪")
    if "性骚扰" in content or "职场" in content:
        tags.append("职场性骚扰")
    if "性侵" in content:
        tags.append("性侵犯罪")
    if "猥亵" in content:
        tags.append("猥亵犯罪")
    if "虐待" in content:
        tags.append("虐待罪")
    if "遗弃" in content:
        tags.append("遗弃罪")
    if "拒不支付" in content or "劳动报酬" in content:
        tags.append("拒不支付劳动报酬罪")
    if "走私" in content:
        tags.append("走私犯罪")
    if "偷渡" in content or "跨境" in content:
        tags.append("偷渡犯罪")
    if "邪教" in content or "组织" in content and "利用" in content:
        tags.append("利用邪教组织犯罪")
    if "寻衅滋事" in content:
        tags.append("寻衅滋事罪")
    if "聚众斗殴" in content:
        tags.append("聚众斗殴罪")
    if "非法拘禁" in content:
        tags.append("非法拘禁罪")
    if "绑架" in content:
        tags.append("绑架罪")
    if "拐卖" in content:
        tags.append("拐卖妇女儿童罪")
    if "收买" in content and "被拐卖" in content:
        tags.append("收买被拐卖的妇女儿童罪")
    if "破坏" in content and ("环境" in content or "资源" in content):
        tags.append("破坏环境资源保护罪")
    if "黑恶" in content or "黑社会" in content:
        tags.append("黑社会性质组织罪")
    if "套路贷" in content:
        tags.append("套路贷")
    if "虚假诉讼" in content:
        tags.append("虚假诉讼罪")
    if "妨害司法" in content:
        tags.append("妨害司法罪")
    if "伪造" in content and ("证件" in content or "公文" in content):
        tags.append("伪造证件公文罪")
    if "故意伤害" in content:
        tags.append("故意伤害罪")
    if "故意杀人" in content:
        tags.append("故意杀人罪")
    if "过失" in content and ("人死亡" in content or "重伤" in content):
        tags.append("过失致人伤亡罪")
    if "抢夺" in content:
        tags.append("抢夺罪")
    if "抢劫" in content:
        tags.append("抢劫罪")
    if "敲诈" in content:
        tags.append("敲诈勒索罪")
    if "强迫" in content and "交易" in content:
        tags.append("强迫交易罪")
    if "非法吸收" in content or "集资" in content:
        tags.append("非法吸收公众存款罪")
    if "组织" in content and "卖淫" in content:
        tags.append("组织卖淫罪")
    if "强迫" in content and "卖淫" in content:
        tags.append("强迫卖淫罪")
    if "传播" in content and ("淫秽" in content or "色情" in content):
        tags.append("传播淫秽物品罪")
    if "贪污" in content:
        tags.append("贪污罪")
    if "贿赂" in content or "受贿" in content or "行贿" in content:
        tags.append("贿赂犯罪")
    if "挪用" in content and "公款" in content:
        tags.append("挪用公款罪")
    if "滥用职权" in content:
        tags.append("滥用职权罪")
    if "玩忽职守" in content:
        tags.append("玩忽职守罪")
    if "重大责任事故" in content:
        tags.append("重大责任事故罪")
    if "危险物品" in content:
        tags.append("危险物品犯罪")
    if "考试" in content and ("作弊" in content or "欺诈" in content):
        tags.append("考试作弊犯罪")
    if "侵犯" in content and "公民个人信息" in content:
        tags.append("侵犯公民个人信息罪")

    # Related links
    related = []
    if any(t in tags for t in ["侵权责任", "生命权", "精神损害赔偿"]):
        related.append("[[concept_侵权责任]]")
    if any(t in tags for t in ["危害公共安全罪", "高空抛物", "危险驾驶罪"]):
        related.append("[[concept_危害公共安全罪]]")
    if any(t in tags for t in ["盗窃罪", "诈骗罪", "帮信罪", "抢夺罪", "抢劫罪", "敲诈勒索罪"]):
        related.append("[[concept_财产犯罪]]")
    if any(t in tags for t in ["故意伤害罪", "故意杀人罪", "过失致人伤亡罪"]):
        related.append("[[concept_人身伤害犯罪]]")
    if any(t in tags for t in ["见义勇为", "正当防卫", "自助行为"]):
        related.append("[[concept_正当防卫]]")
    if any(t in tags for t in ["劳动争议", "工伤"]):
        related.append("[[concept_劳动争议]]")
    if any(t in tags for t in ["贪污罪", "贿赂犯罪", "挪用公款罪"]):
        related.append("[[concept_贪污贿赂罪]]")
    if any(t in tags for t in ["猥亵犯罪", "性侵犯罪", "组织卖淫罪", "强迫卖淫罪"]):
        related.append("[[concept_性犯罪]]")
    if not related:
        related = ["[[concept_民事责任]]"]

    # Clean content
    cleaned = extract_key_content(content)

    # Truncate if too long
    if len(cleaned) > 8000:
        cleaned = cleaned[:8000] + "\n\n...(内容已截断)..."

    tags_str = ', '.join([f'"{t}"' for t in tags])
    related_str = ', '.join(related)

    frontmatter = f"""---
title: {title}
type: summary
category: 诉讼与仲裁
created: 2026-05-11
updated: 2026-05-11
tags: [{tags_str}]
source: "sources/微信公号资料/最高人民法院/最高法-小案大道理-md/{source_file}"
related: {related_str}
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | {source_file} |
| 类型 | 最高人民法院典型案例 |
| 发布领域 | 司法裁判与社会治理 |
| 核心要点 | 见下方裁判要旨 |

## 案情概要

{cleaned}
"""

    return frontmatter

def process_file(md_file):
    """Process a single markdown file"""
    content = md_file.read_text(encoding='utf-8')
    source_name = md_file.name

    # Extract title
    title = extract_title(content)

    # Generate wiki content
    wiki_content = generate_wiki_content(title, content, source_name)

    # Create target filename - clean title for filename
    clean_title = title.replace('"', '').replace('（', '').replace('）', '')
    clean_title = re.sub(r'[^\w一-鿿]', '_', clean_title)
    clean_title = re.sub(r'_+', '_', clean_title).strip('_')
    if len(clean_title) > 80:
        clean_title = clean_title[:80]
    target_name = f"summary_CourtFa_最高法_小案大道理_{clean_title}.md"
    target_path = TARGET_DIR / target_name

    # Handle duplicates
    counter = 1
    while target_path.exists():
        target_name = f"summary_CourtFa_最高法_小案大道理_{clean_title}_{counter}.md"
        target_path = TARGET_DIR / target_name
        counter += 1

    # Write file
    target_path.write_text(wiki_content, encoding='utf-8')
    return target_name

def main():
    md_files = list(SOURCE_DIR.glob("*.md"))
    print(f"Found {len(md_files)} files to process")

    # Clear previous files first
    prev_files = list(TARGET_DIR.glob("summary_CourtFa_最高法_小案大道理_*.md"))
    for f in prev_files:
        f.unlink()
    print(f"Cleared {len(prev_files)} previous files")

    success = 0
    errors = []

    for i, md_file in enumerate(md_files, 1):
        try:
            result = process_file(md_file)
            success += 1
            if i % 20 == 0:
                print(f"Processed {i}/{len(md_files)}: {result}")
        except Exception as e:
            errors.append((md_file.name, str(e)))
            print(f"Error processing {md_file.name}: {e}")

    print(f"\nCompleted: {success}/{len(md_files)}")
    if errors:
        print(f"Errors: {len(errors)}")
        for name, err in errors:
            print(f"  - {name}: {err}")

if __name__ == "__main__":
    main()