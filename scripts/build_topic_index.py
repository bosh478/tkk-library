#!/usr/bin/env python3
"""一次性构建 topic_index.json：扫描 sources/ + wiki/，用种子关键词建立映射。

用法：
    python scripts/build_topic_index.py
    python scripts/build_topic_index.py --keywords "受贿罪,贪污罪,盗窃罪"
"""

import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = VAULT_ROOT / "sources"
WIKI_DIR = VAULT_ROOT / "wiki"
OUTPUT_FILE = WIKI_DIR / "topics" / "topic_index.json"

# 种子关键词：罪名 + 制度 + 程序 + 重要法律
SEED_KEYWORDS = [
    # === 刑法罪名（贪腐类）===
    "受贿罪", "贪污罪", "行贿罪", "挪用公款罪", "巨额财产来源不明罪",
    "私分国有资产罪", "利用影响力受贿罪", "对有影响力的人行贿罪",
    # 刑法罪名（暴力类）
    "故意杀人罪", "故意伤害罪", "抢劫罪", "绑架罪", "强奸罪",
    "非法拘禁罪", "寻衅滋事罪", "聚众斗殴罪", "故意毁坏财物罪",
    # 刑法罪名（经济类）
    "盗窃罪", "诈骗罪", "抢夺罪", "敲诈勒索罪", "职务侵占罪",
    "挪用资金罪", "拒不支付劳动报酬罪", "合同诈骗罪",
    "非法吸收公众存款罪", "集资诈骗罪", "信用卡诈骗罪",
    # 刑法罪名（安全类）
    "交通肇事罪", "危险驾驶罪", "重大责任事故罪",
    "污染环境罪", "非法采矿罪",
    # 刑法罪名（其他）
    "侵犯公民个人信息罪", "掩饰隐瞒犯罪所得罪", "帮助信息网络犯罪活动罪",
    "走私罪", "逃税罪", "假冒注册商标罪", "侵犯著作权罪",
    "侵犯商业秘密罪", "串通投标罪", "非法经营罪",
    "组织卖淫罪", "贩卖毒品罪", "容留他人吸毒罪",
    "赌博罪", "开设赌场罪",
    # === 民事制度 ===
    "正当防卫", "紧急避险", "见义勇为",
    "善意取得", "表见代理", "合同解除", "违约责任", "缔约过失",
    "不当得利", "无因管理", "侵权责任", "精神损害赔偿",
    "惩罚性赔偿", "产品责任", "医疗损害责任", "环境污染责任",
    "饲养动物损害责任", "高空抛物",
    "物权变动", "抵押权", "质权", "留置权",
    "夫妻共同债务", "遗产继承", "遗嘱效力",
    "公司设立", "股东出资", "股权转让", "公司解散", "公司人格否认",
    "破产重整", "破产清算", "破产和解",
    # === 刑事程序 ===
    "认罪认罚从宽", "刑事和解", "附条件不起诉", "不起诉",
    "取保候审", "监视居住", "逮捕", "刑事拘留",
    "管辖", "回避", "证据规则", "非法证据排除",
    "上诉不加刑", "死刑复核", "审判监督",
    "社区矫正", "假释", "减刑", "暂予监外执行",
    # === 民事程序 ===
    "民事诉讼", "管辖权异议", "第三人撤销之诉",
    "执行异议", "执行异议之诉", "财产保全", "行为保全",
    "仲裁", "调解", "人民调解", "司法确认",
    "公益诉讼", "生态环境损害赔偿",
    # === 行政法 ===
    "行政处罚", "行政许可", "行政强制", "行政复议", "行政诉讼",
    "政府信息公开", "国家赔偿",
    # === 重要法律 ===
    "刑法", "民法典", "刑事诉讼法", "民事诉讼法", "行政诉讼法",
    "公司法", "劳动法", "劳动合同法", "消费者权益保护法",
    "反不正当竞争法", "反垄断法", "环境保护法", "食品安全法",
    "药品管理法", "数据安全法", "个人信息保护法",
    "商标法", "专利法", "著作权法",
    # === 知识产权 ===
    "著作权", "专利权", "商标权", "商业秘密",
    "不正当竞争", "知识产权",
    # === 其他重要概念 ===
    "法律适用", "法律解释", "司法解释", "指导性案例",
    "法律援助", "法律职业资格", "律师执业",
]


def grep_keyword(keyword: str, sources_dir: Path) -> list[dict]:
    """用 grep 在 sources/ 中搜索关键词，返回匹配的文件列表。"""
    results = []
    try:
        proc = subprocess.run(
            ["grep", "-rl", "--include=*.md", keyword, str(sources_dir)],
            capture_output=True, timeout=30
        )
        stdout = proc.stdout.decode('utf-8', errors='replace') if proc.stdout else ""
        for line in stdout.strip().split('\n'):
            if line:
                rel = os.path.relpath(line.strip(), str(VAULT_ROOT))
                results.append({"path": rel, "relevance": "high"})
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return results


def find_wiki_pages(keyword: str, wiki_dir: Path) -> list[str]:
    """在 wiki/ 中查找包含关键词的页面。"""
    results = []
    for subdir in ["entities", "summaries", "syntheses"]:
        dir_path = wiki_dir / subdir
        if not dir_path.exists():
            continue
        for f in dir_path.glob("*.md"):
            try:
                content = f.read_text(encoding='utf-8')
            except Exception:
                continue
            if keyword in content:
                rel = os.path.relpath(str(f), str(VAULT_ROOT))
                results.append(rel)
    return results


def main():
    custom_keywords = None
    if len(sys.argv) > 1 and sys.argv[1] == "--keywords":
        custom_keywords = sys.argv[2].split(",")

    keywords = custom_keywords or SEED_KEYWORDS
    print(f"Building topic index for {len(keywords)} keywords...")

    topics = {}
    for i, kw in enumerate(keywords, 1):
        if i % 20 == 0:
            print(f"  Progress: {i}/{len(keywords)}")

        source_files = grep_keyword(kw, SOURCES_DIR)
        wiki_pages = find_wiki_pages(kw, WIKI_DIR)

        if source_files:
            topics[kw] = {
                "source_files": source_files,
                "wiki_pages": wiki_pages,
                "source_count": len(source_files),
            }

    # 确保输出目录存在
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    index = {
        "version": "1.0",
        "generated": str(date.today()),
        "total_topics": len(topics),
        "topics": topics,
    }

    OUTPUT_FILE.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\nDone! {len(topics)} topics indexed -> {OUTPUT_FILE}")
    print(f"Top 10 topics by source count:")
    sorted_topics = sorted(topics.items(), key=lambda x: -x[1]['source_count'])
    for kw, data in sorted_topics[:10]:
        print(f"  {kw}: {data['source_count']} source files, {len(data['wiki_pages'])} wiki pages")


if __name__ == "__main__":
    main()
