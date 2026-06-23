#!/usr/bin/env python3
"""Batch update SPP GuideCase wiki pages with full content from source files."""

import re
import os

VAULT = r"D:\AI agent\tkk-library"

# Map: case_number -> (source_filename, batch_name, case_name)
CASE_MAP = {
    127: ("32第三十二批指导性案例-中华人民共和国最高人民检察院.md", "第三十二批", "白静贪污违法所得没收案"),
    129: ("32第三十二批指导性案例-中华人民共和国最高人民检察院.md", "第三十二批", "黄艳兰贪污违法所得没收案"),
    133: ("33第三十三批指导性案例-中华人民共和国最高人民检察院.md", "第三十三批", "社区矫正对象王某减刑监督案"),
    137: ("34第三十四批指导性案例-中华人民共和国最高人民检察院.md", "第三十四批", "郎某、何某诽谤案"),
    138: ("34第三十四批指导性案例-中华人民共和国最高人民检察院.md", "第三十四批", "岳某侮辱案"),
    140: ("34第三十四批指导性案例-中华人民共和国最高人民检察院.md", "第三十四批", "柯某侵犯公民个人信息案"),
    154: ("38 关于印发最高人民检察院第三十八批指导性案例的通知.md", "第三十八批", "李某荣等七人与李某云民间借贷纠纷抗诉案"),
    155: ("38 关于印发最高人民检察院第三十八批指导性案例的通知.md", "第三十八批", "某小额贷款公司与某置业公司借款合同纠纷抗诉案"),
    157: ("38 关于印发最高人民检察院第三十八批指导性案例的通知.md", "第三十八批", "陈某与向某贵房屋租赁合同纠纷抗诉案"),
    167: ("42 最高检第四十二批指导性案例.md", "第四十二批", "陈某诉江苏省某市人社局撤销退休审批检察监督案"),
    168: ("42 最高检第四十二批指导性案例.md", "第四十二批", "志某诉湖南省甲县公安局确认执法信息录入行政行为违法检察监督案"),
    169: ("42 最高检第四十二批指导性案例.md", "第四十二批", "浙江省杭州市某区人民检察院督促治理虚假登记市场主体检察监督案"),
    170: ("42 最高检第四十二批指导性案例.md", "第四十二批", "广东省某市人民检察院督促住房和城乡建设行政主管部门依法履行监管职责检察监督案"),
    171: ("43 关于印发最高人民检察院第四十三批指导性案例的通知.md", "第四十三批", "防止未成年人滥用药物综合司法保护案"),
    172: ("43 关于印发最高人民检察院第四十三批指导性案例的通知.md", "第四十三批", "阻断性侵犯罪未成年被害人感染艾滋病风险综合司法保护案"),
    173: ("43 关于印发最高人民检察院第四十三批指导性案例的通知.md", "第四十三批", "惩治组织未成年人进行违反治安管理活动犯罪综合司法保护案"),
    174: ("43 关于印发最高人民检察院第四十三批指导性案例的通知.md", "第四十三批", "未成年人网络民事权益综合司法保护案"),
    176: ("44 关于印发最高人民检察院第四十四批指导性案例的通知.md", "第四十四批", "郭四记、徐维伦等人伪造货币案"),
    177: ("44 关于印发最高人民检察院第四十四批指导性案例的通知.md", "第四十四批", "孙旭东非法经营案"),
    178: ("45 关于印发最高人民检察院第四十五批指导性案例的通知.md", "第四十五批", "王某等人故意伤害等犯罪二审抗诉案"),
    179: ("45 关于印发最高人民检察院第四十五批指导性案例的通知.md", "第四十五批", "刘某某贩卖毒品二审抗诉案"),
    180: ("45 关于印发最高人民检察院第四十五批指导性案例的通知.md", "第四十五批", "李某抢劫、强奸、强制猥亵二审抗诉案"),
    181: ("45 关于印发最高人民检察院第四十五批指导性案例的通知.md", "第四十五批", "孟某某等人组织、领导、参加黑社会性质组织、寻衅滋事等犯罪再审抗诉案"),
    182: ("45 关于印发最高人民检察院第四十五批指导性案例的通知.md", "第四十五批", "宋某某危险驾驶二审、再审抗诉案"),
    183: ("46 关于印发最高人民检察院第四十六批指导性案例的通知.md", "第四十六批", "浙江省嵊州市人民检察院督促规范成品油领域税收监管秩序行政公益诉讼案"),
    184: ("46 关于印发最高人民检察院第四十六批指导性案例的通知.md", "第四十六批", "江苏省扬州经济技术开发区人民检察院督促整治闲置国有土地行政公益诉讼案"),
    185: ("46 关于印发最高人民检察院第四十六批指导性案例的通知.md", "第四十六批", "湖南省长沙市检察机关督促追回违法支出国有土地使用权出让收入行政公益诉讼案"),
    187: ("47 关于印发最高人民检察院第四十七批指导性案例的通知.md", "第四十七批", "沈某某、郑某某贪污案"),
    189: ("47 关于印发最高人民检察院第四十七批指导性案例的通知.md", "第四十七批", "李某等人挪用公款案"),
    190: ("47 关于印发最高人民检察院第四十七批指导性案例的通知.md", "第四十七批", "宋某某违规出具金融票证、违法发放贷款、非国家工作人员受贿案"),
    192: ("48 关于印发最高人民检察院第四十八批指导性案例的通知.md", "第四十八批", "周某某与项某某、李某某著作权权属、侵权纠纷等系列虚假诉讼监督案"),
    193: ("48 关于印发最高人民检察院第四十八批指导性案例的通知.md", "第四十八批", "梁永平、王正航等十五人侵犯著作权案"),
    194: ("48 关于印发最高人民检察院第四十八批指导性案例的通知.md", "第四十八批", "上海某公司、许林、陶伟侵犯著作权案"),
}

def read_source(filename):
    path = os.path.join(VAULT, "sources", "2-案例库", "最高检-指导性案例", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_wiki(case_num):
    path = os.path.join(VAULT, "wiki", "syntheses", f"SPP_GuideCase_检例第{case_num}号.md")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_section(text, section_name, alt_names=None):
    """Extract content between 【section_name】 and the next 【 or end."""
    names = [section_name]
    if alt_names:
        names.extend(alt_names)
    for name in names:
        # Handle potential whitespace variations in section markers
        pattern = rf"【{name}】\s*\n(.*?)(?=\n【|\n（检例第\d+号）|$)"
        m = re.search(pattern, text, re.DOTALL)
        if m:
            return m.group(1).strip()
        # Also try with flexible spacing in the marker itself
        escaped = name.replace(" ", r"\s*")
        pattern2 = rf"【{escaped}】\s*\n(.*?)(?=\n【|\n（检例第\d+号）|$)"
        m2 = re.search(pattern2, text, re.DOTALL)
        if m2:
            return m2.group(1).strip()
    return ""

def extract_case_block(source_text, case_num):
    """Extract the full block for a specific case number from source text."""
    # Find start: （检例第X号）
    start_pattern = rf"（检例第{case_num}号）"
    start_match = re.search(start_pattern, source_text)
    if not start_match:
        return None

    start_pos = start_match.start()

    # Find the case name (bolded text before the case number)
    # Look backwards for **text** or just text before （检例第X号）
    before_text = source_text[:start_pos].rstrip()
    # Try to find case name - it's usually on the line(s) before
    lines_before = before_text.split('\n')
    case_name_lines = []
    for line in reversed(lines_before):
        line = line.strip()
        if not line:
            break
        if line.startswith('【') or line.startswith('---'):
            break
        case_name_lines.insert(0, line)
    case_name = ' '.join(case_name_lines).strip()

    # Find end: next （检例第Y号） or end of text
    end_pattern = r"（检例第\d+号）"
    remaining = source_text[start_match.end():]
    end_match = re.search(end_pattern, remaining)
    if end_match:
        end_pos = start_match.end() + end_match.start()
    else:
        end_pos = len(source_text)

    block = source_text[start_match.end():end_pos]
    return case_name, block

def extract_keywords(block):
    return extract_section(block, "关键词")

def extract_summary(block):
    return extract_section(block, "要旨", alt_names=["要 旨", "要  旨"])

def extract_legislation(block):
    return extract_section(block, "相关立法", alt_names=["相关规定"])

def extract_facts(block):
    return extract_section(block, "基本案情")

def extract_process(block):
    # Try multiple section names
    result = extract_section(block, "诉讼过程")
    if not result:
        result = extract_section(block, "检察履职情况")
    if not result:
        result = extract_section(block, "检察机关履职过程")
    if not result:
        result = extract_section(block, "检察履职过程")
    return result

def get_keywords_tags(keywords_text):
    """Extract individual keywords for tags."""
    # Split by common separators
    kws = re.split(r'[ \s]+', keywords_text.strip())
    return [k.strip() for k in kws if k.strip()]

def get_related(case_name, keywords_text):
    """Generate related concept references based on case content."""
    related = []
    # Common crime/concept mappings
    crime_keywords = {
        "贪污": "concept_贪污罪",
        "受贿": "concept_受贿罪",
        "挪用公款": "concept_挪用公款罪",
        "诽谤": "concept_诽谤罪",
        "侮辱": "concept_侮辱罪",
        "侵犯公民个人信息": "concept_侵犯公民个人信息罪",
        "民间借贷": "concept_民间借贷",
        "借款合同": "concept_借款合同",
        "房屋租赁": "concept_房屋租赁合同",
        "退休": "concept_退休",
        "社区矫正": "concept_社区矫正",
        "违法所得没收": "concept_违法所得没收程序",
        "伪造货币": "concept_伪造货币罪",
        "非法经营": "concept_非法经营罪",
        "故意伤害": "concept_故意伤害罪",
        "贩卖毒品": "concept_贩卖毒品罪",
        "抢劫": "concept_抢劫罪",
        "强奸": "concept_强奸罪",
        "黑社会": "concept_黑社会性质组织犯罪",
        "危险驾驶": "concept_危险驾驶罪",
        "公益诉讼": "concept_行政公益诉讼",
        "知识产权": "concept_知识产权保护",
        "著作权": "concept_著作权",
        "商标": "concept_商标权",
        "贪污": "concept_贪污罪",
        "滥用职权": "concept_国有公司人员滥用职权罪",
        "金融票证": "concept_违规出具金融票证罪",
        "违法发放贷款": "concept_违法发放贷款罪",
    }
    combined = case_name + " " + keywords_text
    for keyword, concept in crime_keywords.items():
        if keyword in combined:
            related.append(f"  - [[{concept}]]")
    if not related:
        related.append("  - []")
    return related

def build_wiki_page(case_num, case_name, batch, keywords, summary, legislation, facts, process):
    """Build the full wiki page content."""
    tags_list = ["指导性案例", "最高人民检察院", f"检例第{case_num}号"]
    kw_tags = get_keywords_tags(keywords)
    tags_list.extend(kw_tags)

    related = get_related(case_name, keywords)
    related_str = "\n".join(related)

    # Get source filename
    source_file = CASE_MAP[case_num][0]

    # Generate problem awareness
    problem = summary[:80] + "..." if len(summary) > 80 else summary

    page = f"""---
title: {case_name}
type: synthesis
created: 2026-05-09
updated: 2026-05-27
tags: [{', '.join(tags_list)}]
source: "sources/2-案例库/最高检-指导性案例/{source_file}"
related:
{related_str}
案例分级: ⭐⭐⭐⭐⭐
问题意识: {problem}
---

## 📋 案例信息

| 字段 | 内容 |
|------|------|
| 案例编号 | 检例第{case_num}号 |
| 案例名称 | {case_name} |
| 发布机关 | 最高人民检察院 |
| 发布批次 | {batch} |
| 关键词 | {keywords} |

## 要旨

{summary}

## 相关立法

{legislation}

## 基本案情

{facts}

## 诉讼过程

{process}
"""
    return page

def write_wiki(case_num, content):
    path = os.path.join(VAULT, "wiki", "syntheses", f"SPP_GuideCase_检例第{case_num}号.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    # Group by source file
    source_groups = {}
    for case_num, (src, batch, name) in CASE_MAP.items():
        if src not in source_groups:
            source_groups[src] = []
        source_groups[src].append((case_num, batch, name))

    updated = 0
    errors = []

    for source_filename, cases in source_groups.items():
        print(f"\n=== Processing source: {source_filename} ===")
        source_text = read_source(source_filename)

        for case_num, batch, case_name in cases:
            print(f"  Processing 检例第{case_num}号: {case_name}")
            result = extract_case_block(source_text, case_num)
            if not result:
                print(f"    ERROR: Could not find case block for 检例第{case_num}号")
                errors.append(case_num)
                continue

            extracted_name, block = result
            # Use extracted name if available, otherwise use predefined
            if extracted_name and len(extracted_name) > 2:
                # Clean up the name
                case_name = extracted_name.strip().strip("**").strip()

            keywords = extract_keywords(block)
            summary = extract_summary(block)
            legislation = extract_legislation(block)
            facts = extract_facts(block)
            process = extract_process(block)

            if not keywords:
                print(f"    WARNING: No keywords found")
                keywords = "（未在原文中标注）"
            if not summary:
                print(f"    WARNING: No summary found")
                summary = "（未在原文中标注）"
            if not legislation:
                print(f"    WARNING: No legislation found")
                legislation = "（未在原文中标注）"
            if not facts:
                print(f"    WARNING: No facts found")
                facts = "（未在原文中标注）"
            if not process:
                print(f"    WARNING: No process found")
                process = "（未在原文中标注）"

            content = build_wiki_page(case_num, case_name, batch, keywords, summary, legislation, facts, process)
            write_wiki(case_num, content)
            updated += 1
            print(f"    OK: Updated with {len(content)} chars")

    print(f"\n=== SUMMARY ===")
    print(f"Updated: {updated}")
    print(f"Errors: {len(errors)}")
    if errors:
        print(f"Error cases: {errors}")

if __name__ == "__main__":
    main()
