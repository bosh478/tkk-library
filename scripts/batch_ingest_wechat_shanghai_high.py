#!/usr/bin/env python3
"""批量处理 sources/微信公号资料/上海高院/ 案例参考册文件 -> wiki/summaries/"""

import os
import re
import sys
from pathlib import Path

# VAULT_ROOT 多平台兼容（patched 2026-06-23）：
# 1. 优先 TKK_VAULT_ROOT 环境变量
# 2. Windows: "D:/AI agent/tkk-library"
# 3. Linux/WSL: /home/kangkang/tkk-library 等候选按存在性自动探测
_VAULT_CANDIDATES = [
    os.environ.get("TKK_VAULT_ROOT"),
    "D:/AI agent/tkk-library" if os.name == "nt" else None,
    "/home/kangkang/tkk-library",
    "/mnt/d/AI agent/tkk-library",
    "/mnt/c/Users/汤康康/tkk-library",
]
VAULT_ROOT = next(
    (Path(p) for p in _VAULT_CANDIDATES if p and Path(p).exists()),
    Path(os.environ.get("TKK_VAULT_ROOT", "D:/AI agent/tkk-library"))
)
SOURCES_DIR = VAULT_ROOT / "sources/微信公号资料/上海高院"
WIKI_SUMMARIES = VAULT_ROOT / "wiki/summaries"

CATEGORY_MAP = {
    "刑事审判": ["刑事", "交通肇事", "危险驾驶", "故意伤害", "故意杀人", "强奸",
              "猥亵", "抢劫", "贩毒", "毒品", "受贿", "贪污", "挪用公款",
              "走私", "赌博", "敲诈勒索", "绑架", "纵火", "投放危险物质",
              "以危险方法危害公共安全", "诈骗罪", "盗窃罪", "抢夺",
              "醉驾", "酒驾", "逃逸", "涉案财物", "被告人", "被害人",
              "公诉", "缓刑", "自首", "立功", "追诉时效", "刑法",
              "刑事判决", "刑事裁定", "犯罪未遂", "犯罪中止", "共同犯罪"],
    "知识产权": ["知识产权", "专利", "商标", "著作权", "版权", "商业秘密", "不正当竞争",
                "技术秘密", "发明", "实用新型", "外观设计", "知产"],
    "金融与财税": ["证券虚假陈述", "证券", "保险", "基金", "期货", "债券", "信托",
                "融资租赁", "票据", "信用卡", "理财", "虚假陈述", "内幕交易",
                "操纵市场", "信息披露", "上市公司", "金融", "银行"],
    "公司商事与合规": ["公司", "商事", "合伙", "投资", "并购", "重组", "对赌",
                   "股东", "董事", "高管", "公司治理", "公司章程", "增资", "减资",
                   "解散", "清算", "破产", "合同僵局", "违约", "合同解除",
                   "股权转让", "股权激励", "有限责任"],
    "婚姻家庭与继承": ["婚姻", "离婚", "继承", "抚养", "赡养", "收养", "亲子关系",
                   "彩礼", "嫁妆", "家暴", "家庭暴力", "夫妻", "婚前", "婚后",
                   "财产分割", "抚养费", "探望权", "代孕"],
    "建筑工程与房地产": ["建筑", "房地产", "工程", "物业", "房屋", "装修",
                    "施工", "发包", "承包", "竣工", "验收", "期房", "二手房",
                    "商品房", "预售"],
    "劳动与社会保障": ["劳动", "工伤", "工资", "社保", "劳动合同", "加班", "辞退",
                   "解雇", "经济补偿", "赔偿金", "竞业限制", "劳务派遣"],
    "侵权与人格权": ["侵权", "名誉", "隐私", "肖像", "人身损害", "安全保障义务",
                  "消费者权益", "产品责任", "医疗损害", "交通事故", "网络侵权",
                  "平台责任", "电子商务", "网购", "生命权", "健康权"],
    "执行与其他": ["执行", "强制执行", "被执行人", "申请执行", "虚拟财产", "比特币",
                 "生态环境", "能源", "污染", "排放"],
}

def extract_date(fname):
    """从文件名提取日期"""
    m = re.match(r'\[(\d{4}-\d{2}-\d{2})\]', fname)
    return m.group(1) if m else None

def extract_title(fname):
    """从文件名提取标题"""
    m = re.match(r'\[\d{4}-\d{2}-\d{2}\](.+?)\.md$', fname)
    if m:
        title = m.group(1).strip()
        # 去掉末尾的 丨案例参考册 等后缀
        title = re.sub(r'[|｜]案例参考册$', '', title).strip()
        return title
    return fname.replace('.md', '')

def extract_title_from_content(content):
    """从内容第一行提取标题"""
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('#'):
            title = re.sub(r'^#+\s*', '', line).strip()
            title = re.sub(r'[|｜]案例参考册$', '', title).strip()
            # 去掉前后空格和特殊字符
            title = title.strip(' \t\n\r')
            if title:
                return title
    return None

def detect_category(content):
    """根据内容判断分类"""
    scores = {}
    for cat, keywords in CATEGORY_MAP.items():
        score = sum(1 for kw in keywords if kw in content)
        if score > 0:
            scores[cat] = score
    if scores:
        return max(scores, key=scores.get)
    return "诉讼与仲裁"

def extract_key_points(content, max_points=5):
    """提取核心要点"""
    points = []

    # 1. 尝试提取裁判要旨/裁判要点区域
    # 匹配从"裁判要旨"或"裁判要点"到下一个section标题
    for section_name in ['裁判要旨', '裁判要点', '裁判思路']:
        m = re.search(
            rf'\*\*\s*{section_name}\s*\*\*\s*\n(.*?)(?=\n\*\*\s*[一二三四五六七八九十]|'
            rf'\n\*\*\s*(?:法官解读|基本案情|案例解读|裁判结果|裁判理由|相关法条|案情介绍)\s*\*\*|'
            rf'\n#{2,}|\Z)',
            content, re.DOTALL
        )
        if m:
            section_text = m.group(1).strip()
            # 清理 **0** **1** 编号模式
            section_text = re.sub(r'\*\*\d+\*\*\s*\n?', '', section_text)
            section_text = re.sub(r'\d+\\\.\s*', '', section_text)
            # 按段落分割
            paragraphs = [p.strip() for p in section_text.split('\n') if p.strip()]
            for p in paragraphs:
                clean = re.sub(r'\*+', '', p).strip()
                clean = clean.strip(' \t\n\r')
                if clean and len(clean) > 10:
                    # 限制单条长度
                    if len(clean) > 300:
                        clean = clean[:300].rstrip() + "..."
                    points.append(clean)
            if points:
                return points[:max_points]

    # 2. 尝试简单的正则匹配
    for pattern in [r'裁判要[旨点]\s*[：:]\s*(.*?)(?=\n\n|\n\*\*)',
                    r'核心要点\s*[：:]\s*(.*?)(?=\n\n)']:
        m = re.search(pattern, content, re.DOTALL)
        if m:
            text = m.group(1).strip()
            items = re.split(r'[；;\n]', text)
            for item in items:
                item = re.sub(r'\*+', '', item).strip()
                if item and len(item) > 10:
                    points.append(item[:300])
            if points:
                return points[:max_points]

    # 3. 从关键词提取
    m = re.search(r'关键词\s*\n(.*?)(?=\n\n|\n\*\*)', content, re.DOTALL)
    if m:
        kws = m.group(1).strip().replace('\n', ' / ')
        kws = re.sub(r'\*+', '', kws).strip()
        if kws:
            points.append(f"关键词：{kws}")

    # 4. 提取裁判理由的第一段作为要点
    m = re.search(r'裁判理由\s*\*\*\s*\n(.*?)(?=\n\n|\n\*\*)', content, re.DOTALL)
    if m and not points:
        text = m.group(1).strip()
        clean = re.sub(r'\*+', '', text).strip()
        if clean and len(clean) > 20:
            points.append(clean[:300])

    # 5. 如果还是没找到，取前3段非空段落
    if not points:
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and not p.strip().startswith('#')]
        for p in paragraphs[1:4]:
            clean = re.sub(r'\*+', '', p).strip()
            if clean and len(clean) > 20:
                points.append(clean[:200])
            if len(points) >= 3:
                break

    return points[:max_points]

def extract_keywords(content):
    """提取关键词"""
    # 匹配 **关键词** 后面的内容
    m = re.search(r'\*\*\s*关键词\s*\*\*\s*\n(.*?)(?=\n\n|\n\*\*\s*[裁判基本案例法官]|$)', content, re.DOTALL)
    if m:
        text = m.group(1).strip()
        # 清理格式
        text = re.sub(r'\*+', '', text)
        text = text.replace('\n', ' / ')
        text = re.sub(r'\s*/\s*', ' / ', text)
        text = text.strip(' /')
        if text:
            return text
    return ""

def build_tags(category, content):
    """构建标签列表"""
    tags = ["上海高院", "案例参考册"]
    if category not in tags:
        tags.append(category)
    # 从内容提取额外标签
    extra_tags = {
        "刑事审判": ["刑事", "犯罪", "被告人", "被害人"],
        "民事审判": ["民事", "原告", "被告"],
        "执行": ["执行", "强制执行", "被执行人"],
        "商事审判": ["商事", "公司", "股权"],
        "金融审判": ["金融", "证券", "保险"],
    }
    for tag, kws in extra_tags.items():
        if tag not in tags and any(kw in content for kw in kws):
            tags.append(tag)
    return tags

def sanitize_filename(title):
    """清理标题用于文件名"""
    # 替换文件系统不允许的字符
    title = re.sub(r'[<>:"/\\|?*]', '', title)
    title = title.replace('"', '').replace('"', '').replace("'", "").replace("'", "")
    title = title.replace('，', '，').replace('。', '。')
    title = title.strip('. ')
    # 限制长度
    if len(title) > 80:
        title = title[:80].rstrip()
    return title

def generate_wiki_page(fname, subdir, content, date_str, title):
    """生成 wiki summary 页面"""
    # 从内容提取更准确的标题
    content_title = extract_title_from_content(content)
    if content_title and len(content_title) > len(title):
        title = content_title

    category = detect_category(content)
    key_points = extract_key_points(content)
    keywords = extract_keywords(content)
    tags = build_tags(category, content)

    date_compact = date_str.replace('-', '')
    safe_title = sanitize_filename(title)
    wiki_name = f"summary_{date_compact}_上海高院_案例参考册_{safe_title}.md"

    # 构建关键词字符串
    if not keywords:
        keywords = " / ".join(tags)

    # 构建核心要点
    if key_points:
        points_text = "\n".join(f"- {p}" for p in key_points)
        points_desc = f"{len(key_points)}条（见下方）"
    else:
        points_text = "- （详见原文）"
        points_desc = "见正文"

    # 构建 source 路径
    source_path = f"sources/微信公号资料/上海高院/{subdir}/{fname}"

    page = f"""---
title: {title}
type: summary
published: {date_str}
created: 2026-05-27
updated: 2026-05-27
tags: [{', '.join(tags)}]
source: "[[{source_path}]]"
category: {category}
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | [[{fname}]] |
| 类型 | 上海高院-案例参考册 |
| 发布日期 | {date_str} |
| 关键词 | {keywords} |
| 核心要点 | {points_desc} |

## 核心要点

{points_text}

## 相关

- [[index]] — 返回索引
"""
    return wiki_name, page

def main():
    processed = 0
    skipped = 0
    errors = []

    # 处理所有子目录
    for subdir in ["上海高院-案例参考册-md", "上海高院-办案心法-md"]:
        src_dir = SOURCES_DIR / subdir
        if not src_dir.exists():
            print(f"[WARN] 目录不存在: {src_dir}")
            continue

        files = sorted([f for f in os.listdir(src_dir) if f.endswith('.md')])
        print(f"\n[{subdir}] 共 {len(files)} 个文件")

        for fname in files:
            date_str = extract_date(fname)
            if not date_str:
                print(f"  [SKIP] {fname} - 无法提取日期")
                errors.append(f"无法提取日期: {fname}")
                continue

            title = extract_title(fname)
            date_compact = date_str.replace('-', '')
            safe_title = sanitize_filename(title)
            wiki_name = f"summary_{date_compact}_上海高院_案例参考册_{safe_title}.md"
            wiki_path = WIKI_SUMMARIES / wiki_name

            # 检查是否已存在（通过日期和关键词模糊匹配）
            existing = list(WIKI_SUMMARIES.glob(f"summary_{date_compact}_上海高院_*"))
            if existing:
                skipped += 1
                if skipped <= 3:
                    print(f"  [SKIP] {fname} - 已存在 {existing[0].name}")
                continue

            # 读取源文件
            src_path = src_dir / fname
            try:
                content = src_path.read_text(encoding='utf-8')
            except Exception as e:
                print(f"  [ERROR] {fname} - {e}")
                errors.append(f"读取失败: {fname}: {e}")
                continue

            # 生成 wiki 页面
            try:
                wiki_name, page_content = generate_wiki_page(fname, subdir, content, date_str, title)
                wiki_path = WIKI_SUMMARIES / wiki_name
                wiki_path.write_text(page_content, encoding='utf-8')
                processed += 1
                if processed % 20 == 0:
                    print(f"  [PROGRESS] 已处理 {processed} 个文件")
            except Exception as e:
                print(f"  [ERROR] {fname} - {e}")
                errors.append(f"生成失败: {fname}: {e}")

    print(f"\n=== 完成 ===")
    print(f"已处理: {processed}")
    print(f"已跳过(已存在): {skipped}")
    print(f"错误: {len(errors)}")
    if errors:
        print("错误详情:")
        for e in errors[:10]:
            print(f"  - {e}")

if __name__ == "__main__":
    main()
