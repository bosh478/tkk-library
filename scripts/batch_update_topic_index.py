#!/usr/bin/env python3
"""Batch update topic_index for source files"""
import json
import subprocess
import sys
from pathlib import Path
import os
from datetime import date

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
TOPIC_INDEX = VAULT_ROOT / "wiki/topics/topic_index.json"

SEED_KEYWORDS = [
    "受贿罪", "贪污罪", "行贿罪", "挪用公款罪", "巨额财产来源不明罪",
    "私分国有资产罪", "利用影响力受贿罪", "对有影响力的人行贿罪",
    "故意杀人罪", "故意伤害罪", "抢劫罪", "绑架罪", "强奸罪",
    "非法拘禁罪", "寻衅滋事罪", "聚众斗殴罪", "故意毁坏财物罪",
    "盗窃罪", "诈骗罪", "抢夺罪", "敲诈勒索罪", "职务侵占罪",
    "挪用资金罪", "拒不支付劳动报酬罪", "合同诈骗罪",
    "非法吸收公众存款罪", "集资诈骗罪", "信用卡诈骗罪",
    "交通肇事罪", "危险驾驶罪", "重大责任事故罪",
    "污染环境罪", "非法采矿罪",
    "侵犯公民个人信息罪", "掩饰隐瞒犯罪所得罪", "帮助信息网络犯罪活动罪",
    "走私罪", "逃税罪", "假冒注册商标罪", "侵犯著作权罪",
    "侵犯商业秘密罪", "串通投标罪", "非法经营罪",
    "组织卖淫罪", "贩卖毒品罪", "容留他人吸毒罪",
    "赌博罪", "开设赌场罪",
    "正当防卫", "紧急避险", "见义勇为",
    "善意取得", "表见代理", "合同解除", "违约责任", "缔约过失",
    "不当得利", "无因管理", "侵权责任", "精神损害赔偿",
    "惩罚性赔偿", "产品责任", "医疗损害责任", "环境污染责任",
    "饲养动物损害责任", "高空抛物",
    "物权变动", "抵押权", "质权", "留置权",
    "夫妻共同债务", "遗产继承", "遗嘱效力",
    "公司设立", "股东出资", "股权转让", "公司解散", "公司人格否认",
    "破产重整", "破产清算", "破产和解",
    "认罪认罚从宽", "刑事和解", "附条件不起诉", "不起诉",
    "取保候审", "监视居住", "逮捕", "刑事拘留",
    "管辖", "回避", "证据规则", "非法证据排除",
    "上诉不加刑", "死刑复核", "审判监督",
    "社区矫正", "假释", "减刑", "暂予监外执行",
    "民事诉讼", "管辖权异议", "第三人撤销之诉",
    "执行异议", "执行异议之诉", "财产保全", "行为保全",
    "仲裁", "调解", "人民调解", "司法确认",
    "公益诉讼", "生态环境损害赔偿",
    "行政处罚", "行政许可", "行政强制", "行政复议", "行政诉讼",
    "政府信息公开", "国家赔偿",
    "刑法", "民法典", "刑事诉讼法", "民事诉讼法", "行政诉讼法",
    "公司法", "劳动法", "劳动合同法", "消费者权益保护法",
    "反不正当竞争法", "反垄断法", "环境保护法", "食品安全法",
    "药品管理法", "数据安全法", "个人信息保护法",
    "商标法", "专利法", "著作权法",
    "著作权", "专利权", "商标权", "商业秘密",
    "不正当竞争", "知识产权",
    "法律适用", "法律解释", "司法解释", "指导性案例",
    "法律援助", "法律职业资格", "律师执业",
]

def grep_keyword(keyword, file_path):
    try:
        proc = subprocess.run(
            ["grep", "-q", keyword, file_path],
            capture_output=True, timeout=10
        )
        return proc.returncode == 0
    except:
        return False

def main():
    if not TOPIC_INDEX.exists():
        print("topic_index.json not found")
        sys.exit(1)

    index = json.loads(TOPIC_INDEX.read_text(encoding='utf-8'))
    topics = index.get("topics", {})

    # Get list of source files from command line
    if len(sys.argv) < 2:
        print("Usage: python batch_update_topic_index.py <file_list>")
        sys.exit(1)

    file_list = sys.argv[1]
    files = Path(file_list).read_text(encoding='utf-8').strip().split("\n")
    total = len(files)
    print(f"Updating {total} files...")

    for i, rel_path in enumerate(files, 1):
        abs_path = str(VAULT_ROOT / rel_path)
        if not Path(abs_path).exists():
            continue

        matched = []
        for kw in SEED_KEYWORDS:
            if grep_keyword(kw, abs_path):
                matched.append(kw)

        for kw in matched:
            if kw not in topics:
                topics[kw] = {"source_files": [], "wiki_pages": [], "source_count": 0}

            entry = topics[kw]
            existing_paths = [sf["path"] for sf in entry.get("source_files", [])]
            if rel_path not in existing_paths:
                entry.setdefault("source_files", []).append({"path": rel_path, "relevance": "high"})
                entry["source_count"] = len(entry["source_files"])

        if i % 100 == 0:
            print(f"  Progress: {i}/{total}")

    index["topics"] = topics
    index["generated"] = str(date.today())
    TOPIC_INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Done! {len(topics)} topics, {sum(t['source_count'] for t in topics.values())} source files indexed")

if __name__ == "__main__":
    main()
