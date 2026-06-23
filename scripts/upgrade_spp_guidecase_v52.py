#!/usr/bin/env python3
"""
升级 SPP 指导性案例摘要文件到 v52 格式 - 最终修复版
"""
import re
import os
from pathlib import Path

BASE_DIR = Path(r"D:\AI agent\tkk-library\wiki\summaries")
PATTERN = "summary_SPP_GuideCase_*.md"

# 犯罪类型到 concept 页面的映射
CRIME_TO_CONCEPT = {
    "受贿": "[[受贿罪]]",
    "贪污": "[[贪污罪]]",
    "挪用公款": "[[挪用公款罪]]",
    "绑架": "[[绑架罪]]",
    "聚众斗殴": "[[聚众斗殴罪]]",
    "毒品": "[[贩卖、制造毒品罪]]",
    "贩卖、制造毒品": "[[贩卖、制造毒品罪]]",
    "贩卖毒品": "[[贩卖毒品罪]]",
    "制造毒品": "[[制造毒品罪]]",
    "环境监管失职": "[[环境监管失职罪]]",
    "食品": "[[生产、销售有毒、有害食品罪]]",
    "有毒、有害食品": "[[生产、销售有毒、有害食品罪]]",
    "伪劣产品": "[[生产、销售伪劣产品罪]]",
    "虚假恐怖信息": "[[编造虚假恐怖信息罪]]",
    "恐怖信息": "[[编造虚假恐怖信息罪]]",
    "抢劫": "[[抢劫罪]]",
    "入户抢劫": "[[抢劫罪]]",
    "盗窃": "[[盗窃罪]]",
    "串通投标": "[[串通投标罪]]",
    "串通拍卖": "[[串通投标罪]]",
    "非法经营": "[[非法经营罪]]",
    "骗取贷款": "[[骗取贷款罪]]",
    "贷款诈骗": "[[贷款诈骗罪]]",
    "信用卡诈骗": "[[信用卡诈骗罪]]",
    "集资诈骗": "[[集资诈骗罪]]",
    "走私": "[[走私普通货物、物品罪]]",
    "洗钱": "[[洗钱罪]]",
    "传销": "[[组织、领导传销活动罪]]",
    "电信诈骗": "[[电信诈骗相关]]",
    "非法吸收公众存款": "[[非法吸收公众存款罪]]",
    "职务侵占": "[[职务侵占罪]]",
    "滥用职权": "[[滥用职权罪]]",
    "玩忽职守": "[[玩忽职守罪]]",
    "徇私枉法": "[[徇私枉法罪]]",
    "枉法裁判": "[[民事、行政枉法裁判罪]]",
    "虐待被监管人": "[[虐待被监管人罪]]",
    "敲诈勒索": "[[敲诈勒索罪]]",
    "故意伤害": "[[故意伤害罪]]",
    "故意杀人": "[[故意杀人罪]]",
    "强奸": "[[强奸罪]]",
    "猥亵": "[[猥亵罪]]",
    "拐卖": "[[拐卖妇女、儿童罪]]",
    "收买被拐卖": "[[收买被拐卖的妇女、儿童罪]]",
    "非法采矿": "[[非法采矿罪]]",
    "污染环境": "[[污染环境罪]]",
    "盗伐林木": "[[盗伐林木罪]]",
    "滥伐林木": "[[滥伐林木罪]]",
    "珍贵动物": "[[非法收购、运输、出售珍贵、濒危野生动物、珍贵、濒危野生动物制品罪]]",
    "公益诉讼": "[[公益诉讼]]",
    "行政诉讼监督": "[[行政诉讼监督]]",
    "生效行政裁判监督": "[[生效行政裁判监督]]",
    "工伤认定": "[[工伤保险待遇纠纷]]",
    "工伤保险": "[[工伤保险待遇纠纷]]",
    "利用未公开信息交易": "[[利用未公开信息交易罪]]",
    "违规出具金融票证": "[[违规出具金融票证罪]]",
    "违法发放贷款": "[[违法发放贷款罪]]",
    "非国家工作人员受贿": "[[非国家工作人员受贿罪]]",
    "金融票证": "[[违规出具金融票证罪]]",
    "国有公司人员滥用职权": "[[国有公司人员滥用职权罪]]",
    "非法采矿": "[[非法采矿罪]]",
    "非法占有农用地": "[[非法占用农用地罪]]",
    "非法占用农用地": "[[非法占用农用地罪]]",
    "欺诈": "[[诈骗罪]]",
    "诈骗": "[[诈骗罪]]",
    "合同诈骗": "[[合同诈骗罪]]",
    "组织领导传销": "[[组织、领导传销活动罪]]",
    "传播淫秽物品": "[[传播淫秽物品罪]]",
    "传播淫秽物品牟利": "[[传播淫秽物品牟利罪]]",
    "著作权": "[[侵犯著作权罪]]",
    "侵犯著作权": "[[侵犯著作权罪]]",
    "侵犯商业秘密": "[[侵犯商业秘密罪]]",
    "商业秘密": "[[侵犯商业秘密罪]]",
    "药品": "[[生产、销售假药罪]]",
    "假药": "[[生产、销售假药罪]]",
    "劣药": "[[生产、销售劣药罪]]",
    "非法行医": "[[非法行医罪]]",
    "非法采伐": "[[非法采伐国家重点保护植物罪]]",
    "破坏环境资源保护": "[[破坏环境资源保护罪]]",
    "立案监督": "[[立案监督]]",
    "行政执法": "[[行政执法]]",
    "行政公益诉讼": "[[行政公益诉讼]]",
    "民事公益诉讼": "[[民事公益诉讼]]",
    "未成年人保护": "[[未成年人保护]]",
    "附条件不起诉": "[[附条件不起诉]]",
    "认罪认罚": "[[认罪认罚从宽制度]]",
    "企业合规": "[[企业合规整改]]",
}

def is_v52_complete(content):
    """检查是否是完整v52格式（无重复章节，有related链接）"""
    # 检查是否有重复的知识网络章节
    if content.count("## 📚 知识网络") > 1:
        return False
    if content.count("## ⚠️ 知识缺口") > 1:
        return False
    # 检查related是否为空
    related_match = re.search(r'^related:\s*\[\]$', content, re.MULTILINE)
    if related_match:
        return False
    return True

def extract_case_info(content):
    """从文件内容提取案件编号和关键词"""
    case_refs = []
    case_pattern = re.compile(r'检例第(\d+)号|（检例第(\d+)号）')
    for match in case_pattern.finditer(content):
        num = match.group(1) or match.group(2)
        ref = f"检例第{num}号"
        if ref not in case_refs:
            case_refs.append(ref)

    keywords = []
    kw_pattern = re.compile(r'【关键词】\s*\n?\s*(.+?)(?:\n\s*\*\*|【基本案情】|【相关立法】|【诉讼过程】)')
    for match in kw_pattern.finditer(content):
        kw_text = match.group(1).strip()
        for kw in re.split(r'[\s,，、]+', kw_text):
            kw = kw.strip().strip('*').strip()
            if kw and len(kw) > 1:
                keywords.append(kw)

    return case_refs, keywords

def extract_published_date(content, filename):
    """提取发布日期"""
    pub_match = re.search(r'^published:\s*(\d{4}-\d{2}-\d{2})', content, re.MULTILINE)
    if pub_match:
        return pub_match.group(1)

    date_match = re.search(r'\[(\d{4}-\d{2}-\d{2})\]', filename)
    if date_match:
        return date_match.group(1)

    return "2026-05-07"

def get_related_concepts(keywords, content):
    """根据关键词获取关联的concept页面"""
    related = set()
    # 先从关键词匹配
    for kw in keywords:
        for crime, concept in CRIME_TO_CONCEPT.items():
            if crime in kw:
                related.add(concept)
    # 再从内容匹配（更广泛的搜索）
    if not related:
        for crime, concept in CRIME_TO_CONCEPT.items():
            if crime in content:
                related.add(concept)
    return list(related)[:5]

def extract_title(content, filename):
    """提取标题"""
    title_match = re.search(r'^title:\s*(.+?)$', content, re.MULTILINE)
    if title_match:
        return title_match.group(1).strip()

    name = Path(filename).stem
    name = re.sub(r'^summary_SPP_GuideCase_\d+', '', name)
    name = re.sub(r'^\d+\[.*?\]\s*', '', name)
    name = name.replace('-中华人民共和国最高人民检察院', '').replace('_中华人民共和国最高人民检察院', '')
    return name.strip()

def detect_category(content):
    """检测文档类型"""
    if any(kw in content for kw in ['公益诉讼', '行政公益诉讼', '民事公益诉讼', '南四湖']):
        return "生态环境与能源"
    if any(kw in content for kw in ['行政诉讼监督', '行政裁判', '工伤认定', '行政复议', '征收补偿']):
        return "诉讼与仲裁"
    if any(kw in content for kw in ['金融', '银行', '期货', '证券', '资产管理', '股票', '债券']):
        return "金融与财税"
    if any(kw in content for kw in ['未成年人', '附条件不起诉', '未成年']):
        return "婚姻家庭与继承"
    return "诉讼与仲裁"

def remove_duplicate_sections(content):
    """移除重复的知识网络和知识缺口章节"""
    # 找第一个 ## 📚 知识网络 的位置
    first_kn = content.find("## 📚 知识网络")
    if first_kn == -1:
        return content

    # 找第二个 ## 📚 知识网络（如果有）
    second_kn = content.find("## 📚 知识网络", first_kn + 1)
    if second_kn != -1:
        # 找到下一个 ## 标题（在第二个知识网络之前的）
        next_header = content.find("\n## ", first_kn + 1)
        if next_header != -1 and next_header < second_kn:
            # 保留到 next_header 之前的内容
            content = content[:first_kn] + content[next_header:]

    # 类似处理 ## ⚠️ 知识缺口
    first_kg = content.find("## ⚠️ 知识缺口")
    if first_kg != -1:
        second_kg = content.find("## ⚠️ 知识缺口", first_kg + 1)
        if second_kg != -1:
            next_header = content.find("\n## ", first_kg + 1)
            if next_header != -1 and next_header < second_kg:
                content = content[:first_kg] + content[next_header:]

    return content

def extract_body_content(content):
    """提取正文内容"""
    related_link_match = re.search(r'\n## 相关链接', content)
    if related_link_match:
        body = content[:related_link_match.start()]
    else:
        sources_match = re.search(r'\n---\nsources:', content)
        if sources_match:
            body = content[:sources_match.start()]
        else:
            body = content

    first_header = re.search(r'\n## ', body)
    if first_header:
        body = body[first_header.start():]

    return body.strip()

def upgrade_to_v52(content, filename):
    """将文件内容升级到v52格式"""
    # 检查是否已经是完整v52格式
    if is_v52_complete(content):
        return None  # 跳过

    # 提取信息
    case_refs, keywords = extract_case_info(content)
    published_date = extract_published_date(content, filename)
    related = get_related_concepts(keywords, content)
    title = extract_title(content, filename)
    category = detect_category(content)

    # 构建frontmatter
    new_frontmatter = f"""---
title: {title}
type: summary
created: {published_date}
updated: 2026-05-07
tags: [检察业务, 指导性案例]
category: {category}
source: [{filename}]
line-refs:
"""

    for ref in case_refs:
        new_frontmatter += f'  - "{ref}"\n'

    if related:
        new_frontmatter += "related:\n"
        for rel in related:
            new_frontmatter += f"  - {rel}\n"
    else:
        new_frontmatter += "related: []\n"

    new_frontmatter += "---\n"

    # 提取正文并移除重复章节
    body = extract_body_content(content)
    body = remove_duplicate_sections(body)

    # 构建知识网络
    knowledge_network = "\n\n## 📚 知识网络\n| 知识点 | 原文引用 | 相关知识 |\n|--------|----------|----------|\n"

    sample_points = list(keywords[:6])
    if case_refs:
        case_nums = [ref.replace("检例第", "").replace("号", "") for ref in case_refs]
        if case_nums:
            sample_points.append(f"检例第{case_nums[0]}号涉及情形")

    for pt in sample_points[:6]:
        related_kw = ', '.join(related[:2]) if related else '待关联'
        knowledge_network += f"| {pt} | 【关键词】{pt} | {related_kw} |\n"

    if not sample_points:
        knowledge_network += "| 指导性案例 | 本批次指导性案例 | [[相关罪名]] |\n"

    # 知识缺口
    knowledge_gap = "\n## ⚠️ 知识缺口\n> [!gap]+\n"
    gaps_found = []

    if not related:
        gaps_found.append("缺少关联罪名 concept 页面，需建立相关罪名页面并补充链接")
    if len(case_refs) <= 1 and len(keywords) == 0:
        gaps_found.append("本批次案例信息提取较少，可能存在内容截断，建议核查原文")
    if not keywords:
        gaps_found.append("未提取到关键词信息，line-refs 可能不完整")

    if gaps_found:
        for gap in gaps_found:
            knowledge_gap += f"> 发现：{gap}\n"
    else:
        knowledge_gap += "> 发现：本批次指导性案例内容完整，暂无明显知识缺口\n"

    return new_frontmatter + "\n" + body + knowledge_network + knowledge_gap

def process_file(filepath):
    """处理单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = upgrade_to_v52(content, filepath.name)

        if new_content is None:
            return True, "SKIPPED"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True, None
    except Exception as e:
        return False, str(e)

def main():
    files = list(BASE_DIR.glob(PATTERN))
    print(f"找到 {len(files)} 个文件")

    success = 0
    skipped = 0
    failed = 0
    errors = []

    for filepath in sorted(files):
        ok, err = process_file(filepath)
        if ok:
            if err == "SKIPPED":
                skipped += 1
                print(f"[SKIP] {filepath.name}")
            else:
                success += 1
                print(f"[OK] {filepath.name}")
        else:
            failed += 1
            errors.append((filepath.name, err))
            print(f"[FAIL] {filepath.name}: {err}")

    print(f"\n完成: 成功 {success} 个, 跳过 {skipped} 个, 失败 {failed} 个")
    if errors:
        print("\n失败文件:")
        for name, err in errors:
            print(f"  - {name}: {err}")

if __name__ == "__main__":
    main()
