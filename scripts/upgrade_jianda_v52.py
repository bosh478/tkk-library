#!/usr/bin/env python3
"""
批量升级检答网集萃文件到v52格式
"""
import os
import re
from pathlib import Path
from datetime import datetime

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-检答网集萃-md/")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/summaries/")

def extract_date_from_filename(filename):
    """从文件名提取日期，如 [2020-03-30]"""
    match = re.match(r'\[(\d{4}-\d{2}-\d{2})\]', filename)
    if match:
        return match.group(1)
    return None

def extract_number_from_filename(filename):
    """从文件名提取集萃编号，如 22"""
    match = re.search(r'检答网集萃(\d+)', filename)
    if match:
        return int(match.group(1))
    return None

def extract_qa_topics(content):
    """从内容中提取问答主题和行号"""
    topics = []
    lines = content.split('\n')

    # 查找所有加粗的问答主题（**主题**）
    for i, line in enumerate(lines):
        # 跳过标题行、来源行、往期回顾等
        if '来源：' in line or '往期回顾' in line or '编辑：' in line:
            continue
        # 匹配加粗的问答主题
        match = re.search(r'\*\*(.{2,50}?)\*\*', line)
        if match and '咨询' not in match.group(1) and '解答' not in match.group(1):
            topic = match.group(1).strip()
            # 过滤掉太短的或无意义的
            if len(topic) > 3 and topic not in ['咨询类别', '咨询人', '咨询内容', '解答专家']:
                topics.append((i+1, topic))

    return topics

def extract_related_concepts(topic):
    """根据问答主题提取相关概念页面链接"""
    related = []

    # 基于关键词映射相关概念
    keyword_map = {
        '凶器': ['寻衅滋事罪', '抢劫罪'],
        '缓刑': ['缓刑', '管辖', '数罪并罚'],
        '异地': ['管辖', '数罪并罚'],
        '自首': ['自首', '刑法第67条'],
        '犯罪': ['管辖', '数罪并罚'],
        '拘留': ['刑事拘留', '强制措施'],
        '国境外': ['管辖', '司法协助'],
        '没收': ['违法所得', '没收'],
        '立功': ['立功', '刑法第68条'],
        '假释': ['假释', '减刑'],
        '减刑': ['减刑', '假释'],
        '管辖': ['管辖'],
        '渎职': ['渎职罪'],
        '贪污': ['贪污罪'],
        '受贿': ['受贿罪'],
        '挪用': ['挪用公款罪'],
        '盗窃': ['盗窃罪'],
        '诈骗': ['诈骗罪'],
        '毒品': ['毒品犯罪'],
        '醉驾': ['危险驾驶罪'],
        '醉酒': ['危险驾驶罪'],
        '抢劫': ['抢劫罪'],
        '抢夺': ['抢夺罪'],
        '敲诈勒索': ['敲诈勒索罪'],
        '寻衅滋事': ['寻衅滋事罪'],
        '故意伤害': ['故意伤害罪'],
        '强奸': ['强奸罪'],
        '猥亵': ['强制猥亵罪'],
        '拐卖': ['拐卖妇女、儿童罪'],
        '非法': ['非法经营罪'],
        '非法占用': ['非法占用农用地罪'],
        '非法采矿': ['非法采矿罪'],
        '污染': ['污染环境罪'],
        '虚开': ['虚开增值税专用发票罪'],
        '偷逃': ['逃税罪'],
        '走私': ['走私罪'],
        '逃税': ['逃税罪'],
        '骗税': ['骗取出口退税罪'],
        '非法集资': ['非法吸收公众存款罪'],
        '组织领导': ['组织、领导传销活动罪'],
        '黑社会': ['组织、领导、参加黑社会性质组织罪'],
        '恶势力': ['恶势力犯罪'],
        '套路贷': ['诈骗罪'],
        '正当防卫': ['正当防卫', '刑法第20条'],
        '防卫过当': ['正当防卫'],
        '紧急避险': ['紧急避险', '刑法第21条'],
        '坦白': ['坦白', '刑法第67条第三款'],
        '累犯': ['累犯', '刑法第65条'],
        '数罪并罚': ['数罪并罚', '刑法第69条'],
        '管制': ['管制', '刑法第38条'],
        '拘役': ['拘役', '刑法第42条'],
        '无期': ['无期徒刑'],
        '死缓': ['死刑缓期执行'],
        '不起诉': ['不起诉', '刑事诉讼法'],
        '撤回起诉': ['撤回起诉'],
        '附条件不起诉': ['附条件不起诉'],
        '核准追诉': ['核准追诉'],
        '追诉时效': ['追诉时效', '刑法第87条'],
        '社区矫正': ['社区矫正'],
        '监外执行': ['暂予监外执行'],
        '逮捕': ['逮捕', '刑事诉讼法'],
        '取保候审': ['取保候审'],
        '监视居住': ['监视居住'],
        '刑事拘留': ['刑事拘留'],
        '留置': ['留置'],
        '搜查': ['搜查'],
        '扣押': ['扣押'],
        '冻结': ['冻结'],
        '查封': ['查封'],
        '涉案财物': ['涉案财物'],
        '违法所得': ['违法所得'],
        '罚金': ['罚金'],
        '赔偿': ['国家赔偿'],
        '司法救助': ['司法救助'],
        '羁押': ['羁押'],
        '超期羁押': ['超期羁押'],
        '投诉': ['投诉'],
        '申诉': ['申诉'],
        '信访': ['信访'],
        '检察建议': ['检察建议'],
        '抗诉': ['抗诉'],
        '二审': ['第二审程序'],
        '一审': ['第一审程序'],
        '再审': ['审判监督程序'],
        '简易程序': ['简易程序'],
        '认罪认罚': ['认罪认罚从宽'],
        '听证': ['听证'],
        '公开听证': ['听证'],
        '公益诉讼': ['公益诉讼'],
        '民事公益诉讼': ['民事公益诉讼'],
        '行政公益诉讼': ['行政公益诉讼'],
        '刑事附带民事': ['刑事附带民事诉讼'],
        '未成年人': ['未成年人犯罪'],
        '犯罪记录封存': ['犯罪记录封存'],
        '强制医疗': ['强制医疗'],
        '精神病人': ['强制医疗'],
        '食品安全': ['食品安全犯罪'],
        '药品': ['药品犯罪'],
        '环境': ['环境污染犯罪'],
        '生态': ['生态保护'],
        '野生动物': ['野生动物保护'],
        '土地': ['土地资源保护'],
        '矿产': ['矿产资源保护'],
        '林木': ['林木资源保护'],
        '渔业': ['渔业资源保护'],
        '水资源': ['水资源保护'],
        '文物': ['文物犯罪'],
        '赌博': ['赌博罪'],
        '开设赌场': ['开设赌场罪'],
        '卖淫': ['组织卖淫罪'],
        '嫖宿': ['嫖宿幼女罪'],
        '淫秽': ['传播淫秽物品罪'],
        '网络': ['网络犯罪'],
        '电信诈骗': ['电信诈骗'],
        '侵犯公民个人信息': ['侵犯公民个人信息罪'],
        '帮助信息网络犯罪': ['帮助信息网络犯罪活动罪'],
        '非法利用信息网络': ['非法利用信息网络罪'],
        '计算机': ['计算机犯罪'],
        '信用卡': ['信用卡诈骗罪'],
        '贷款诈骗': ['贷款诈骗罪'],
        '保险诈骗': ['保险诈骗罪'],
        '税务': ['税务犯罪'],
        '发票': ['发票犯罪'],
        '审计': ['审计'],
        '会计': ['会计'],
        '鉴定': ['司法鉴定'],
        '伤残': ['人体损伤程度鉴定'],
        '伤情鉴定': ['人体损伤程度鉴定'],
        '精神病鉴定': ['精神病鉴定'],
    }

    for keyword, concepts in keyword_map.items():
        if keyword in topic:
            for c in concepts:
                if c not in related:
                    related.append(c)

    return related

def process_file(filepath):
    """处理单个源文件，返回v52格式的内容"""
    filename = filepath.name
    content = filepath.read_text(encoding='utf-8')

    # 提取日期和编号
    date_str = extract_date_from_filename(filename)
    number = extract_number_from_filename(filename)

    # 提取问答主题
    topics = extract_qa_topics(content)

    # 生成标题
    # 从文件名提取标题部分
    title_match = re.search(r'检答网集萃\d+(.+)\.md', filename)
    if title_match:
        raw_title = title_match.group(1).replace('.md', '')
        # 清理标题中的多余字符
        title = f"检答网集萃{number} {raw_title}"
    else:
        title = filename.replace('.md', '')

    # 构建front matter
    created_date = date_str if date_str else "2020-01-01"
    source_name = filename.replace('.md', '')

    # 构建line-refs - 使用YAML列表格式
    line_refs_list = []
    for line_num, topic in topics:
        line_refs_list.append(f'  - "{topic}"')
    line_refs_str = '\n'.join(line_refs_list)

    # 构建related链接
    all_related = []
    for line_num, topic in topics:
        related = extract_related_concepts(topic)
        all_related.extend(related)

    # 去重
    all_related = list(dict.fromkeys(all_related))[:10]  # 最多10个
    related_list = []
    for r in all_related:
        related_list.append(f'  - [[concept_{r}]]')
    related_str = '\n'.join(related_list)

    # 构建frontmatter
    frontmatter = f'''---
title: {title}
type: summary
created: {created_date}
updated: 2026-05-07
tags: [检察业务]
category: 诉讼与仲裁
source: [{source_name}]
line-refs:
{line_refs_str}
related:
{related_str}
---'''

    # 构建知识网络表格
    knowledge_network = "## 📚 知识网络\n"
    knowledge_network += "| 知识点 | 原文引用 | 相关知识 |\n"
    knowledge_network += "|--------|----------|----------|\n"

    for line_num, topic in topics:
        related = extract_related_concepts(topic)
        related_str = " / ".join([f"[[concept_{r}]]" for r in related[:5]])
        knowledge_network += f"| {topic} | 第{line_num}行 | {related_str} |\n"

    # 提取正文内容（去掉往期回顾部分）
    body = content
    # 找到往期回顾的位置并截断
    if '**往期回顾**' in body:
        body = body.split('**往期回顾**')[0]

    # 构建最终内容
    result = f"{frontmatter}\n\n## ❓ 问答主题\n\n"
    for line_num, topic in topics:
        result += f"- 问答{line_num}：{topic}\n"

    result += f"\n{knowledge_network}\n"

    # 添加原始正文内容（清理后）
    result += "\n## 📖 正文\n\n"
    # 移除往期回顾、编辑信息等
    clean_body = body
    lines = clean_body.split('\n')
    clean_lines = []
    for line in lines:
        if '来源：' in line or '编辑：' in line or '预览时标签不可点' in line or '阅读原文' in line:
            continue
        if line.strip().startswith('__'):
            continue
        clean_lines.append(line)

    result += '\n'.join(clean_lines)

    return result, title

def main():
    # 获取源目录所有md文件
    source_files = list(SOURCE_DIR.glob("*.md"))
    print(f"找到 {len(source_files)} 个源文件")

    # 获取已存在的目标文件数量
    existing = list(TARGET_DIR.glob("*SPP_JianDaWang*.md"))
    print(f"已存在 {len(existing)} 个目标文件")

    # 处理编号22及之后的文件（跳过1-21）
    processed = 0
    skipped = 0
    errors = []

    for filepath in sorted(source_files):
        number = extract_number_from_filename(filepath.name)

        if number is None:
            print(f"跳过（无法提取编号）: {filepath.name}")
            skipped += 1
            continue

        # 跳过1-21
        if number <= 21:
            skipped += 1
            continue

        try:
            result, title = process_file(filepath)

            # 生成目标文件名
            target_filename = f"summary_SPP_JianDaWang_{filepath.name.replace('[', '').replace(']', '')}"
            target_path = TARGET_DIR / target_filename

            # 写入文件
            target_path.write_text(result, encoding='utf-8')

            print(f"处理成功 ({number}): {title[:40]}...")
            processed += 1

        except Exception as e:
            errors.append((filepath.name, str(e)))
            print(f"处理失败: {filepath.name} - {e}")

    print(f"\n处理完成: {processed} 个成功, {skipped} 个跳过, {len(errors)} 个错误")
    if errors:
        print("\n错误列表:")
        for name, err in errors:
            print(f"  - {name}: {err}")

if __name__ == "__main__":
    main()
