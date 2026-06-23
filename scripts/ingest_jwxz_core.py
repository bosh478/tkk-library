#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
监外执行专题 ingest 批量处理脚本
处理 sources/1-专题研究/监外执行/ 下的核心文件，生成 entity 页面
"""
import os
import re
import sys
from pathlib import Path

VAULT = Path(r'D:\AI agent\tkk-library')
SRC_DIR = VAULT / 'sources' / '1-专题研究' / '监外执行'
WIKI_ENTITIES = VAULT / 'wiki' / 'entities'
WIKI_CONCEPTS = VAULT / 'wiki' / 'concepts'
TODAY = '2026-06-09'

# 跳过 EXISTS 文件（wiki 已有对应页面）
EXISTS_FILES = {
    '20140623_最高人民检察院关于对职务犯罪罪犯减刑、假释、暂予监外执行案件实行备案审查的规定.txt',
    '20191230_人民检察院刑事诉讼规则（2019）.txt',
    '20200701_中华人民共和国社区矫正法.txt',
    '关于进一步加强社区矫正工作衔接配合管理的意见.md',
}

# 核心专题文件 → entity 文件名映射
CORE_MAPPING = {
    # 暂予监外执行核心
    '20141201_最高人民法院、最高人民检察院、公安部、司法部、国家卫生计生委关于印发《暂予监外执行规定》的通知.txt': {
        'entity': 'entity_暂予监外执行规定（2014年）.md',
        'type': '司法解释',
        'wenhao': '司发通〔2014〕112号',
        'date': '2014-10-24',
    },
    '20161001_司法部关于印发《监狱暂予监外执行程序规定》的通知.txt': {
        'entity': 'entity_监狱暂予监外执行程序规定（2016年）.md',
        'type': '部门规章',
        'wenhao': '司发通〔2016〕78号',
        'date': '2016-08-22',
    },
    '20230701_最高人民法院、最高人民检察院、公安部、国家安全部、司法部、国家卫生健康委关于印发《关于进一步规范暂予监外执行工作的意见》的通知.txt': {
        'entity': 'entity_关于进一步规范暂予监外执行工作的意见（2023年）.md',
        'type': '司法指导性文件',
        'wenhao': '',
        'date': '2023-07-01',
    },
    '20140404_司法部关于贯彻中政委〔2014〕5号文件精神严格规范减刑、假释、暂予监外执行工作的通知.txt': {
        'entity': 'entity_司法部关于贯彻中政委〔2014〕5号文件严格规范减刑假释暂予监外执行的通知.md',
        'type': '部门规范性文件',
        'wenhao': '司发通〔2014〕38号',
        'date': '2014-04-04',
    },
    '20080323_人民检察院监外执行检察办法.txt': {
        'entity': 'entity_人民检察院监外执行检察办法.md',
        'type': '司法解释',
        'wenhao': '',
        'date': '2008-03-23',
    },
    '20090625_中央社会治安综合治理委员会办公室、最高人民法院、最高人民检察院等关于印发《关于加强和规范监外执行工作的意见》的通知.txt': {
        'entity': 'entity_关于加强和规范监外执行工作的意见.md',
        'type': '司法指导性文件',
        'wenhao': '',
        'date': '2009-06-25',
    },
    '20070803_最高人民检察院关于印发《最高人民检察院关于加强对监外执行罪犯脱管、漏管检察监督的意见》的通知.txt': {
        'entity': 'entity_最高人民检察院关于加强对监外执行罪犯脱管漏管检察监督的意见.md',
        'type': '司法解释',
        'wenhao': '',
        'date': '2007-08-03',
    },
    '20141201_保外就医严重疾病范围.txt': {
        'entity': 'entity_保外就医严重疾病范围（2014年）.md',
        'type': '附件',
        'wenhao': '',
        'date': '2014-12-01',
    },
    '20160726_最高人民法院关于印发《罪犯生活不能自理鉴别标准》的通知.txt': {
        'entity': 'entity_罪犯生活不能自理鉴别标准.md',
        'type': '司法解释',
        'wenhao': '',
        'date': '2016-07-26',
    },
    '附件：罪犯生活不能自理鉴别标准.md': {
        'entity': 'entity_罪犯生活不能自理鉴别标准（附件）.md',
        'type': '附件',
        'wenhao': '',
        'date': '2016-07-26',
    },
    '20140601_最高人民法院关于减刑、假释案件审理程序的规定.txt': {
        'entity': 'entity_最高人民法院关于减刑假释案件审理程序的规定（2014年）.md',
        'type': '司法解释',
        'wenhao': '法释〔2014〕5号',
        'date': '2014-06-01',
    },
    '20141211_最高人民法院关于罪犯交付执行前暂予监外执行组织诊断工作有关问题的通知.txt': {
        'entity': 'entity_关于罪犯交付执行前暂予监外执行组织诊断工作的通知.md',
        'type': '司法解释',
        'wenhao': '法〔2014〕253号',
        'date': '2014-12-11',
    },
    '20161001_司法部关于印发《监狱暂予监外执行程序规定》的通知.txt': {
        'entity': 'entity_监狱暂予监外执行程序规定.md',
        'type': '部门规章',
        'wenhao': '司发通〔2016〕78号',
        'date': '2016-10-01',
    },
    '19980311_最高人民法院赔偿委员会关于保外就医期间国家不承担赔偿责任的批复.txt': {
        'entity': 'entity_最高人民法院赔偿委员会关于保外就医期间国家不承担赔偿责任的批复.md',
        'type': '司法解释',
        'wenhao': '[1998]赔他字第5号',
        'date': '1998-03-11',
    },
    '20061027_公安部第三局关于被监外执行人员恢复户口有关问题的批复.txt': {
        'entity': 'entity_公安部第三局关于被监外执行人员恢复户口有关问题的批复.md',
        'type': '部门规章',
        'wenhao': '公治〔2006〕325号',
        'date': '2006-10-27',
    },
    '20100726_最高人民法院、最高人民检察院、公安部等关于印发《关于对司法工作人员在诉讼活动中的渎职行为加强法律监督的若干规定(试行)》的通知.txt': {
        'entity': 'entity_关于对司法工作人员在诉讼活动中的渎职行为加强法律监督的若干规定（试行）.md',
        'type': '司法解释',
        'wenhao': '',
        'date': '2010-07-26',
    },
    '20131123_看守所留所执行刑罚罪犯管理办法(2013年修订).txt': {
        'entity': 'entity_看守所留所执行刑罚罪犯管理办法（2013年修订）.md',
        'type': '部门规章',
        'wenhao': '公监管〔2013〕227号',
        'date': '2013-11-23',
    },
    '20080323_人民检察院看守所检察办法.txt': {
        'entity': 'entity_人民检察院看守所检察办法.md',
        'type': '司法解释',
        'wenhao': '',
        'date': '2008-03-23',
    },
    '20211208_最高人民检察院关于印发《人民检察院巡回检察工作规定》的通知.txt': {
        'entity': 'entity_人民检察院巡回检察工作规定.md',
        'type': '司法解释',
        'wenhao': '高检发监字〔2021〕62号',
        'date': '2021-12-08',
    },
    '20211001_司法部关于印发《监狱计分考核罪犯工作规定》的通知.txt': {
        'entity': 'entity_监狱计分考核罪犯工作规定.md',
        'type': '部门规章',
        'wenhao': '司规〔2021〕3号',
        'date': '2021-10-01',
    },
    '20150302_最高人民法院、最高人民检察院、公安部、司法部印发《关于依法办理家庭暴力犯罪案件的意见》的通知.txt': {
        'entity': 'entity_关于依法办理家庭暴力犯罪案件的意见.md',
        'type': '司法指导性文件',
        'wenhao': '',
        'date': '2015-03-02',
    },
    '20151130_最高人民检察院、中国残疾人联合会关于印发《最高人民检察院、中国残疾人联合会关于在检察工作中切实维护残疾人合法权益的意见》的通知.txt': {
        'entity': 'entity_关于在检察工作中切实维护残疾人合法权益的意见.md',
        'type': '司法指导性文件',
        'wenhao': '',
        'date': '2015-11-30',
    },
    '20160501_最高人民法院关于人民法院办理接收在台湾地区服刑的大陆居民回大陆服刑案件的规定.txt': {
        'entity': 'entity_关于人民法院办理接收在台湾地区服刑的大陆居民回大陆服刑案件的规定.md',
        'type': '司法解释',
        'wenhao': '法释〔2016〕11号',
        'date': '2016-05-01',
    },
    '20180421_最高人民检察院关于在全国检察机关开展“监督维护在押人员合法权益专项活动”的通知.txt': {
        'entity': 'entity_关于在全国检察机关开展监督维护在押人员合法权益专项活动的通知.md',
        'type': '司法指导性文件',
        'wenhao': '',
        'date': '2018-04-21',
    },
    '20220107_就业服务与就业管理规定（2022年修订）.txt': {
        'entity': 'entity_就业服务与就业管理规定（2022年修订）.md',
        'type': '部门规章',
        'wenhao': '',
        'date': '2022-01-07',
    },
    '20220905_最高人民法院、最高人民检察院、公安部、国家安全部关于印发《关于取保候审若干问题的规定》的通知（2022年修订）.txt': {
        'entity': 'entity_关于取保候审若干问题的规定（2022年修订）.md',
        'type': '司法解释',
        'wenhao': '法发〔2022〕15号',
        'date': '2022-09-05',
    },
    '20240704_最高人民检察院关于印发《人民检察院司法责任追究条例》的通知（2024年修订）.txt': {
        'entity': 'entity_人民检察院司法责任追究条例（2024年修订）.md',
        'type': '司法解释',
        'wenhao': '高检发办字〔2024〕61号',
        'date': '2024-07-04',
    },
    '20260221_最高人民法院、最高人民检察院、公安部、司法部印发《关于进一步加强社区矫正工作衔接配合管理的意见》的通知.txt': {
        'entity': 'entity_司发通2026_8号_关于进一步加强社区矫正工作衔接配合管理的意见.md',
        'type': '司法指导性文件',
        'wenhao': '司发通〔2026〕8号',
        'date': '2026-02-21',
    },
    # 案例
    '20190521_最高人民检察院关于印发最高人民检察院第十四批指导性案例的通知.txt': {
        'entity': 'synthesis_最高检第十四批指导性案例.md',
        'type': '指导性案例',
        'wenhao': '高检发办字〔2019〕31号',
        'date': '2019-05-21',
    },
    '20200228_最高人民检察院关于印发最高人民检察院第十九批指导性案例的通知.txt': {
        'entity': 'synthesis_最高检第十九批指导性案例.md',
        'type': '指导性案例',
        'wenhao': '高检发办字〔2020〕3号',
        'date': '2020-02-28',
    },
    '20220130_最高人民检察院关于印发最高人民检察院第三十三批指导性案例的通知.txt': {
        'entity': 'synthesis_最高检第三十三批指导性案例.md',
        'type': '指导性案例',
        'wenhao': '高检发办字〔2022〕16号',
        'date': '2022-01-30',
    },
    '20250925_最高人民检察院关于印发《刑罚变更执行监督典型案例》的通知.txt': {
        'entity': 'synthesis_刑罚变更执行监督典型案例（2025年）.md',
        'type': '典型案例',
        'wenhao': '',
        'date': '2025-09-25',
    },
    '20211201_最高人民法院、最高人民检察院、公安部、司法部印发《关于加强减刑、假释案件实质化审理的意见》的通知.txt': {
        'entity': 'entity_关于加强减刑假释案件实质化审理的意见.md',
        'type': '司法指导性文件',
        'wenhao': '法发〔2021〕31号',
        'date': '2021-12-01',
    },
}


def parse_metadata(content):
    """解析【文章属性】元数据"""
    meta = {}
    # 找到"文章属性"部分
    m = re.search(r'文章属性(.*?)(?=\n\s*正文|\Z)', content, re.DOTALL)
    if not m:
        return meta
    text = m.group(1)
    # 提取每个字段
    patterns = {
        'title': r'标题\s*[:：]?\s*(.+?)(?:\n|$)',
        'issuer': r'【制定机关】\s*(.+?)(?:\n|$)',
        'date': r'【公布日期】\s*(.+?)(?:\n|$)',
        'wenhao': r'【文\s*号】\s*(.+?)(?:\n|$)',
        'effective': r'【施行日期】\s*(.+?)(?:\n|$)',
        'level': r'【效力等级】\s*(.+?)(?:\n|$)',
        'status': r'【时效性】\s*(.+?)(?:\n|$)',
        'category': r'【主题分类】\s*(.+?)(?:\n|$)',
    }
    for k, p in patterns.items():
        m2 = re.search(p, text)
        if m2:
            meta[k] = m2.group(1).strip()
    return meta


def extract_content(content, max_chars=30000):
    """提取正文内容"""
    # 移除元数据部分
    m = re.search(r'\n\s*正文\s*\n(.*)', content, re.DOTALL)
    if m:
        body = m.group(1).strip()
    else:
        body = content
    return body[:max_chars]


def extract_key_sections(body):
    """提取关键章节"""
    # 找到所有标题
    lines = body.split('\n')
    sections = []
    cur = {'title': '', 'content': ''}
    for line in lines:
        s = line.strip()
        if s.startswith('第') and ('章' in s or '条' in s) and len(s) < 50:
            if cur['title']:
                sections.append(cur)
            cur = {'title': s, 'content': ''}
        else:
            cur['content'] += line + '\n'
    if cur['title']:
        sections.append(cur)
    return sections


def make_entity_page(src_filename, meta, body, target_filename):
    """生成 entity 页面"""
    title = meta.get('title', src_filename.replace('.txt', '').replace('.md', ''))
    issuer = meta.get('issuer', '')
    date = meta.get('date', '')
    wenhao = meta.get('wenhao', '')
    effective = meta.get('effective', '')
    level = meta.get('level', '')
    status = meta.get('status', '现行有效')
    category = meta.get('category', '')

    # 提取关键章节（用于"主要内容"部分）
    sections = extract_key_sections(body)
    section_summary = ''
    if sections:
        section_summary = '## 主要内容\n\n'
        for i, s in enumerate(sections[:8]):
            section_summary += f'### {s["title"]}\n\n{s["content"][:500]}...\n\n' if len(s['content']) > 500 else f'### {s["title"]}\n\n{s["content"]}\n\n'

    # frontmatter
    tags = ['监外执行', '暂予监外执行']
    if category:
        tags.append(category)
    if level:
        tags.append(level)
    if '减刑' in title or '减刑' in wenhao:
        tags.append('减刑')
    if '假释' in title or '假释' in wenhao:
        tags.append('假释')
    if '社区矫正' in title:
        tags.append('社区矫正')
    if '保外就医' in title:
        tags.append('保外就医')
    if '监狱' in title and '监外' not in title:
        tags.append('监狱管理')
    if '检察' in title:
        tags.append('检察监督')
    if '社区矫正法' in title:
        tags.append('社区矫正法')
    if '刑事诉讼' in title:
        tags.append('刑事诉讼')

    tags_str = ', '.join(sorted(set(tags)))

    frontmatter = f"""---
title: {title}
type: entity
created: {TODAY}
updated: {TODAY}
tags: [{tags_str}]
related:
  - [[concept_暂予监外执行]]
  - [[concept_社区矫正]]
  - [[concept_减刑]]
  - [[concept_假释]]
"""

    # 添加到相关法条
    if '《刑事诉讼法》' in body or '刑事诉讼法' in title:
        frontmatter += '  - [[concept_中华人民共和国刑事诉讼法]]\n'
    if '《监狱法》' in body or '监狱法' in title:
        frontmatter += '  - [[concept_中华人民共和国监狱法]]\n'
    if '《社区矫正法》' in body or '社区矫正法' in title:
        frontmatter += '  - [[concept_中华人民共和国社区矫正法]]\n'

    frontmatter += f"source: '[[{src_filename}]]'\n---\n\n"

    # 正文
    body_section = f"""## 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{src_filename}]] |
| 类型 | {level or '司法解释/部门规章'} |
| 制定机关 | {issuer} |
| 公布日期 | {date} |
| 文号 | {wenhao} |
| 施行日期 | {effective} |
| 时效性 | {status} |
| 主题分类 | {category or '监外执行'} |

## 核心要点

{extract_key_points(body)}

## 主要内容

{body[:15000]}

"""

    if len(body) > 15000:
        body_section += f"\n> 注：原文超过 15000 字，此处仅展示前 15000 字。完整内容见源文件 [[{src_filename}]]。\n"

    body_section += f"\n## 相关\n\n- [[concept_暂予监外执行]]\n- [[concept_社区矫正]]\n- [[concept_减刑]]\n- [[concept_假释]]\n"

    return frontmatter + body_section


def extract_key_points(body):
    """提取核心要点（首段 + 关键句）"""
    lines = [l.strip() for l in body.split('\n') if l.strip()]
    if not lines:
        return '（无内容）'
    # 第一段
    first_para = lines[0]
    points = [f'**首段要点**：{first_para[:300]}']
    # 寻找关键词
    keywords = ['暂予监外执行', '保外就医', '生活不能自理', '减刑', '假释', '社区矫正', '监外执行', '审查', '批准', '决定', '交付执行', '人民检察院', '监狱']
    seen = set()
    for kw in keywords:
        for line in lines:
            if kw in line and line not in seen and len(line) < 200:
                points.append(f'- {line[:200]}')
                seen.add(line)
                if len(points) >= 10:
                    break
        if len(points) >= 10:
            break
    return '\n'.join(points)


def make_synthesis_page(src_filename, meta, body, target_filename):
    """生成 synthesis 页面（用于指导性案例）"""
    title = meta.get('title', src_filename.replace('.txt', '').replace('.md', ''))
    issuer = meta.get('issuer', '')
    date = meta.get('date', '')
    wenhao = meta.get('wenhao', '')
    level = meta.get('level', '')

    frontmatter = f"""---
title: {title}
type: synthesis
created: {TODAY}
updated: {TODAY}
tags: [指导性案例, 监外执行, 暂予监外执行, 案例分析]
related:
  - [[concept_暂予监外执行]]
  - [[concept_社区矫正]]
source: '[[{src_filename}]]'
---

## 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{src_filename}]] |
| 类型 | 最高人民检察院指导性案例 |
| 制定机关 | {issuer} |
| 公布日期 | {date} |
| 文号 | {wenhao} |
| 时效性 | 现行有效 |

## 案例要点

{body[:8000]}

## 相关

- [[concept_暂予监外执行]]
- [[concept_社区矫正]]
- [[concept_减刑]]
- [[concept_假释]]
"""
    if len(body) > 8000:
        frontmatter += f"\n> 注：原文超过 8000 字，此处仅展示前 8000 字。完整内容见源文件 [[{src_filename}]]。\n"
    return frontmatter


def process_core():
    """处理核心文件"""
    processed = 0
    skipped = 0
    errors = []
    for src_name, config in CORE_MAPPING.items():
        src_path = SRC_DIR / src_name
        if not src_path.exists():
            errors.append(f'文件不存在: {src_name}')
            continue
        target_name = config['entity']
        # 决定是 entity 还是 synthesis
        if target_name.startswith('synthesis_'):
            target_path = VAULT / 'wiki' / 'syntheses' / target_name
        else:
            target_path = WIKI_ENTITIES / target_name
        if target_path.exists():
            skipped += 1
            continue
        # 读取源文件
        try:
            with open(src_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(src_path, 'r', encoding='gbk') as f:
                content = f.read()
        meta = parse_metadata(content)
        body = extract_content(content)
        # 合并手动配置
        if not meta.get('date') and config.get('date'):
            meta['date'] = config['date']
        if not meta.get('wenhao') and config.get('wenhao'):
            meta['wenhao'] = config['wenhao']
        # 生成页面
        if target_name.startswith('synthesis_'):
            page = make_synthesis_page(src_name, meta, body, target_name)
        else:
            page = make_entity_page(src_name, meta, body, target_name)
        # 写入
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(page)
        processed += 1
        print(f'[OK] {target_name}')
    print(f'\n处理完成: 成功 {processed} 个，跳过 {skipped} 个，错误 {len(errors)} 个')
    if errors:
        for e in errors:
            print(f'  [ERR] {e}')


if __name__ == '__main__':
    process_core()
