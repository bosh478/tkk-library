#!/usr/bin/env python3
"""
批量更新最高检指导性案例wiki页面
从源文件中提取完整内容，更新对应的SPP_GuideCase_检例第X号.md占位符页面
"""
import re
import os
from pathlib import Path

# 配置路径
BASE_DIR = Path(r"D:\AI agent\tkk-library")
SOURCE_DIR = BASE_DIR / "sources" / "2-案例库" / "最高检-指导性案例"
WIKI_DIR = BASE_DIR / "wiki" / "syntheses"

# 源文件列表（21个）
SOURCE_FILES = [
    "01第一批指导性案例-中华人民共和国最高人民检察院.md",
    "02第二批指导性案例-中华人民共和国最高人民检察院.md",
    "03第三批指导性案例-中华人民共和国最高人民检察院.md",
    "04第四批指导性案例-中华人民共和国最高人民检察院.md",
    "05第五批指导性案例-中华人民共和国最高人民检察院.md",
    "06第六批指导性案例-中华人民共和国最高人民检察院.md",
    "07第七批指导性案例-中华人民共和国最高人民检察院.md",
    "08第八批指导性案例-中华人民共和国最高人民检察院.md",
    "09第九批指导性案例-中华人民共和国最高人民检察院.md",
    "10第十批指导性案例-中华人民共和国最高人民检察院.md",
    "11第十一批指导性案例-中华人民共和国最高人民检察院.md",
    "12第十二批指导性案例-中华人民共和国最高人民检察院.md",
    "13第十三批指导性案例-中华人民共和国最高人民检察院.md",
    "14第十四批指导性案例-中华人民共和国最高人民检察院.md",
    "15最高人民检察院发布第十五批指导性案例-中华人民共和国最高人民检察院.md",
    "16第十六批指导性案例-中华人民共和国最高人民检察院.md",
    "17第十七批指导性案例-中华人民共和国最高人民检察院.md",
    "18第十八批指导性案例-中华人民共和国最高人民检察院.md",
    "19第十九批指导性案例-中华人民共和国最高人民检察院.md",
    "20第二十批指导性案例-中华人民共和国最高人民检察院.md",
    "21第二十一批指导性案例-中华人民共和国最高人民检察院.md",
]

def extract_batch_number(filename):
    """从文件名提取批次号"""
    # 匹配"第一批"、"第二批"等
    match = re.search(r'第([一二三四五六七八九十百]+)批', filename)
    if match:
        batch_map = {
            '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
            '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
            '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15,
            '十六': 16, '十七': 17, '十八': 18, '十九': 19, '二十': 20,
            '二十一': 21, '二十二': 22, '二十三': 23, '二十四': 24, '二十五': 25,
        }
        return batch_map.get(match.group(1), 0)
    return 0

def extract_crime_tags(case_name, content):
    """从案例名称和内容提取案由标签"""
    crime_keywords = [
        "聚众斗殴罪", "绑架罪", "徇私舞弊暂予监外执行罪",
        "环境监管失职罪", "滥用职权罪", "徇私舞弊不移交刑事案件罪",
        "玩忽职守罪", "徇私枉法罪", "受贿罪",
        "编造虚假恐怖信息罪", "编造、故意传播虚假恐怖信息罪",
        "敲诈勒索罪", "故意杀人罪", "故意伤害罪",
        "抢劫罪", "强奸罪", "盗窃罪", "诈骗罪",
        "贩卖毒品罪", "运输毒品罪", "非法持有毒品罪",
        "走私罪", "贪污罪", "挪用公款罪",
        "行贿罪", "单位受贿罪", "对单位行贿罪",
        "介绍贿赂罪", "巨额财产来源不明罪",
        "私分国有资产罪", "食品监管渎职罪",
        "非法经营罪", "合同诈骗罪",
        "以危险方法危害公共安全罪", "交通肇事罪",
        "危险驾驶罪", "重大责任事故罪",
        "污染环境罪", "非法采矿罪",
        "生产、销售假药罪", "生产、销售有毒、有害食品罪",
        "侵犯著作权罪", "侵犯商业秘密罪",
        "非法吸收公众存款罪", "集资诈骗罪",
        "信用卡诈骗罪", "保险诈骗罪",
        "组织领导传销活动罪", "非法拘禁罪",
        "非法侵入住宅罪", "侮辱罪", "诽谤罪",
        "刑讯逼供罪", "暴力取证罪",
        "虐待被监管人罪", "私放在押人员罪",
        "失职致使在押人员脱逃罪",
        "帮助犯罪分子逃避处罚罪",
        "放纵走私罪", "商检徇私舞弊罪",
        "动植物检疫徇私舞弊罪",
        "放纵制售伪劣商品犯罪行为罪",
        "违法发放林木采伐许可证罪",
        "非法批准征收、征用、占用土地罪",
        "非法低价出让国有土地使用权罪",
        "传染病防治失职罪",
        "非法行医罪", "非法进行节育手术罪",
        "逃避商检罪",
        "组织他人偷越国（边）境罪",
        "骗取出境证件罪",
        "提供伪造、变造的出入境证件罪",
        "偷越国（边）境罪",
        "倒卖文物罪",
        "盗掘古文化遗址、古墓葬罪",
        "非法猎捕、杀害珍贵、濒危野生动物罪",
        "非法收购、运输、出售珍贵、濒危野生动物制品罪",
        "非法占用农用地罪",
        "非法采伐、毁坏国家重点保护植物罪",
        "盗伐林木罪", "滥伐林木罪",
        "走私、贩卖、运输、制造毒品罪",
        "容留他人吸毒罪",
        "引诱、教唆、欺骗他人吸毒罪",
        "强迫他人吸毒罪",
        "包庇毒品犯罪分子罪",
        "窝藏、转移、隐瞒毒品、毒赃罪",
        "组织卖淫罪", "强迫卖淫罪",
        "引诱、容留、介绍卖淫罪",
        "引诱幼女卖淫罪",
        "传播性病罪",
        "嫖宿幼女罪",
        "制作、复制、出版、贩卖、传播淫秽物品牟利罪",
        "传播淫秽物品罪",
        "组织播放淫秽音像制品罪",
        "为他人提供书号出版淫秽书刊罪",
        "战时违抗命令罪",
        "隐瞒、谎报军情罪",
        "拒传、假传军令罪",
        "投降罪",
        "战时临阵脱逃罪",
        "擅离、玩忽军事职守罪",
        "阻碍执行军事职务罪",
        "指使部属违反职责罪",
        "违令作战消极罪",
        "拒不救援友邻部队罪",
        "军人叛逃罪",
        "非法获取军事秘密罪",
        "为境外窃取、刺探、收买、非法提供军事秘密罪",
        "故意泄露军事秘密罪",
        "过失泄露军事秘密罪",
        "战时造谣惑众罪",
        "战时自伤罪",
        "逃离部队罪",
        "武器装备肇事罪",
        "擅自改变武器装备编配用途罪",
        "盗窃、抢夺武器装备、军用物资罪",
        "非法出卖、转让武器装备罪",
        "遗弃武器装备罪",
        "遗失武器装备罪",
        "擅自出卖、转让军队房地产罪",
        "虐待部下罪",
        "遗弃伤病军人罪",
        "战时拒不救治伤病军人罪",
        "战时残害居民、掠夺居民财物罪",
        "私放俘虏罪",
        "虐待俘虏罪",
    ]

    tags = []
    for crime in crime_keywords:
        if crime in case_name or crime in content[:2000]:
            tags.append(crime)

    # 如果没有匹配到，尝试从案名推断
    if not tags:
        if "案" in case_name:
            # 提取案名中的罪名
            name_part = case_name.replace("案", "")
            # 尝试匹配常见模式
            for crime in crime_keywords:
                if any(k in name_part for k in crime.split("、")):
                    tags.append(crime)
                    break

    return tags if tags else ["刑事"]

def parse_cases_from_source(filepath):
    """从源文件中解析出所有案例"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 移除YAML frontmatter
    if content.startswith('---'):
        end_idx = content.find('---', 3)
        if end_idx != -1:
            content = content[end_idx + 3:].strip()

    cases = []

    # 使用"检例第X号"作为分隔符来切分案例
    # 支持两种格式：**（检例第X号）** 和 （检例第X号）
    case_pattern = r'[（(]检例第(\d+)号[）)]'
    case_matches = list(re.finditer(case_pattern, content))

    for i, match in enumerate(case_matches):
        case_number = int(match.group(1))
        match_start = match.start()

        # 往前找当前案例的名称行
        lines_before = content[:match_start].split('\n')
        name_start = match_start
        for j in range(len(lines_before) - 1, -1, -1):
            line = lines_before[j].strip()
            # 跳过空行、分隔符和单独的**标记
            if line == '' or line == '---' or line.startswith('>') or line == '**':
                continue
            # 检查是否是案例名称行（**开头 或 纯文本行）
            if '检例' not in line and '【' not in line:
                # 找到案例名称行的起始位置
                name_start = content.rfind(line, max(0, match_start - 1000), match_start)
                if name_start == -1:
                    name_start = content.find(line, max(0, match_start - 1000))
                break

        # 案例内容的结束位置：到下一个案例的名称行或文件末尾
        if i + 1 < len(case_matches):
            # 找到下一个案例的名称行
            next_match_start = case_matches[i + 1].start()
            next_lines_before = content[:next_match_start].split('\n')
            end = next_match_start
            for j in range(len(next_lines_before) - 1, -1, -1):
                line = next_lines_before[j].strip()
                if line == '' or line == '---' or line.startswith('>') or line == '**':
                    continue
                if '检例' not in line and '【' not in line:
                    end = content.rfind(line, max(0, next_match_start - 1000), next_match_start)
                    if end == -1:
                        end = next_match_start
                    break
        else:
            end = len(content)

        case_content = content[name_start:end].strip()

        # 提取案例名称
        # 支持两种格式：**案例名称**\n**（检例第X号）** 和 案例名称\n（检例第X号）
        case_name_match = re.search(r'\*\*(.+?)\*\*\s*\n\s*\**[（(]检例第\d+号[）)]', case_content)
        if not case_name_match:
            # 尝试不带**的格式
            case_name_match = re.search(r'^(.+?)\s*\n\s*[（(]检例第\d+号[）)]', case_content, re.MULTILINE)
        case_name = case_name_match.group(1).strip() if case_name_match else f"检例第{case_number}号案例"

        # 提取关键词（支持**【关键词】**格式，也支持带全角空格的格式）
        keyword_match = re.search(r'[\s　]*\**【关键词】\**\s*\n\s*(.+?)(?=\n\s*[\s　]*\**【|$)', case_content, re.DOTALL)
        keywords = keyword_match.group(1).strip() if keyword_match else ""

        # 提取要旨
        yaoshi_match = re.search(r'[\s　]*\**【要旨】\**\s*\n\s*(.+?)(?=\n\s*[\s　]*\**【|$)', case_content, re.DOTALL)
        yaoshi = yaoshi_match.group(1).strip() if yaoshi_match else ""

        # 提取相关立法
        legislation_match = re.search(r'[\s　]*\**【相关立法】\**\s*\n\s*(.+?)(?=\n\s*[\s　]*\**【|$)', case_content, re.DOTALL)
        legislation = legislation_match.group(1).strip() if legislation_match else ""

        # 提取基本案情
        facts_match = re.search(r'[\s　]*\**【基本案情】\**\s*\n\s*(.+?)(?=\n\s*[\s　]*\**【|$)', case_content, re.DOTALL)
        facts = facts_match.group(1).strip() if facts_match else ""

        # 提取诉讼过程（可能有多种名称）
        process_match = re.search(r'[\s　]*\**【诉讼过程】\**\s*\n\s*(.+?)(?=\n\s*[\s　]*\**【|$)', case_content, re.DOTALL)
        if not process_match:
            # 尝试"指控与证明犯罪"
            process_match = re.search(r'[\s　]*\**【指控与证明犯罪】\**\s*\n\s*(.+?)(?=\n\s*[\s　]*\**【|$)', case_content, re.DOTALL)
        process = process_match.group(1).strip() if process_match else ""

        # 提取指导意义（如果有的话）
        significance_match = re.search(r'[\s　]*\**【指导意义】\**\s*\n\s*(.+?)(?=\n\s*[\s　]*\**【|$)', case_content, re.DOTALL)
        significance = significance_match.group(1).strip() if significance_match else ""

        # 提取相关规定
        regulations_match = re.search(r'[\s　]*\**【相关规定】\**\s*\n\s*(.+?)$', case_content, re.DOTALL)
        regulations = regulations_match.group(1).strip() if regulations_match else ""

        cases.append({
            'number': case_number,
            'name': case_name,
            'keywords': keywords,
            'yaoshi': yaoshi,
            'legislation': legislation,
            'facts': facts,
            'process': process,
            'significance': significance,
            'regulations': regulations,
            'full_content': case_content,
        })

    return cases

def generate_wiki_content(case, batch_number, source_filename):
    """生成wiki页面内容"""

    # 提取案由标签
    crime_tags = extract_crime_tags(case['name'], case['full_content'])

    # 构建tags
    tags_list = crime_tags + ["最高检", "指导性案例", f"检例第{case['number']}号"]
    tags_str = ", ".join(tags_list)

    # 构建related链接
    related_links = []
    for tag in crime_tags:
        if tag != "刑事":
            related_links.append(f"[[concept_{tag}]]")
    related_str = ", ".join(related_links) if related_links else "[[刑事]]"

    # 处理关键词
    keywords_display = case['keywords'] if case['keywords'] else "（见要旨）"

    # 构建wiki内容
    wiki_content = f"""---
title: {case['name']}
type: synthesis
created: 2026-05-09
updated: 2026-05-27
tags: [{tags_str}]
source: "[[{source_filename}]]"
related: {related_str}
---

## 📋 案例信息

| 字段 | 内容 |
|------|------|
| 案例编号 | 检例第{case['number']}号 |
| 案例名称 | {case['name']} |
| 发布机关 | 最高人民检察院 |
| 发布批次 | 第{batch_number}批 |
| 关键词 | {keywords_display} |

## 要旨

{case['yaoshi']}

## 相关立法

{case['legislation']}

## 基本案情

{case['facts']}

## 诉讼过程

{case['process']}
"""

    # 如果有指导意义，添加到内容中
    if case.get('significance'):
        wiki_content += f"""
## 指导意义

{case['significance']}
"""

    # 如果有相关规定，添加到内容中
    if case.get('regulations'):
        wiki_content += f"""
## 相关规定

{case['regulations']}
"""

    # 添加关键词
    wiki_content += f"""
## 关键词

{case['keywords']}
"""

    return wiki_content

def process_source_file(source_filename):
    """处理单个源文件"""
    filepath = SOURCE_DIR / source_filename

    if not filepath.exists():
        print(f"  [SKIP] Source not found: {source_filename}")
        return []

    batch_number = extract_batch_number(source_filename)
    cases = parse_cases_from_source(filepath)

    results = []
    for case in cases:
        wiki_filename = f"SPP_GuideCase_检例第{case['number']}号.md"
        wiki_filepath = WIKI_DIR / wiki_filename

        if not wiki_filepath.exists():
            print(f"  [SKIP] Wiki page not found: {wiki_filename}")
            continue

        # 生成新的wiki内容
        new_content = generate_wiki_content(case, batch_number, source_filename)

        # 写入文件
        with open(wiki_filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        results.append({
            'number': case['number'],
            'name': case['name'],
            'wiki_file': wiki_filename,
        })

    return results

def main():
    """主函数"""
    print("=" * 60)
    print("SPP Guide Cases Wiki Batch Update")
    print("=" * 60)

    total_cases = 0
    updated_cases = 0

    for source_filename in SOURCE_FILES:
        print(f"\nProcessing: {source_filename}")
        results = process_source_file(source_filename)

        if results:
            for r in results:
                # 清理名称中的特殊字符用于显示
                display_name = r['name'].replace(' ', ' ').replace(' ', ' ')
                print(f"  [OK] Case {r['number']}: {display_name}")
                updated_cases += 1
            total_cases += len(results)
        else:
            print(f"  (No cases or all skipped)")

    print("\n" + "=" * 60)
    print(f"Done: Updated {updated_cases} case pages")
    print("=" * 60)

if __name__ == "__main__":
    main()
