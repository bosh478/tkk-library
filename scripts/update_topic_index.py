#!/usr/bin/env python3
"""增量更新 topic_index.json：ingest 后调用，将新文件添加到索引。

用法：
    python scripts/update_topic_index.py --file "sources/0-现行规范库/xxx.md"
    python scripts/update_topic_index.py --dir "sources/微信公号资料/"   # 重扫整个子目录
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
TOPIC_INDEX = WIKI_DIR / "topics" / "topic_index.json"

# 与 build_topic_index.py 保持一致的种子关键词
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


def grep_keyword(keyword: str, file_path: str) -> bool:
    """检查单个文件是否包含关键词。"""
    try:
        proc = subprocess.run(
            ["grep", "-q", keyword, file_path],
            capture_output=True, timeout=10
        )
        return proc.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


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


def update_index_for_file(rel_path: str, index: dict) -> dict:
    """为单个文件更新 topic_index。返回更新后的 index。"""
    abs_path = str(VAULT_ROOT / rel_path)
    if not os.path.exists(abs_path):
        return index

    topics = index.get("topics", {})
    matched_keywords = []

    for kw in SEED_KEYWORDS:
        if grep_keyword(kw, abs_path):
            matched_keywords.append(kw)

    for kw in matched_keywords:
        if kw not in topics:
            topics[kw] = {
                "source_files": [],
                "wiki_pages": [],
                "source_count": 0,
            }

        entry = topics[kw]
        # 避免重复添加
        existing_paths = [sf["path"] for sf in entry["source_files"]]
        if rel_path not in existing_paths:
            entry["source_files"].append({"path": rel_path, "relevance": "high"})
            entry["source_count"] = len(entry["source_files"])

    # 更新 wiki_pages（全局刷新一次即可）
    if matched_keywords:
        for kw in matched_keywords:
            if kw in topics:
                topics[kw]["wiki_pages"] = find_wiki_pages(kw, WIKI_DIR)

    index["topics"] = topics
    index["generated"] = str(date.today())
    return index


def main():
    if not TOPIC_INDEX.exists():
        print(f"Error: {TOPIC_INDEX} not found. Run build_topic_index.py first.")
        sys.exit(1)

    index = json.loads(TOPIC_INDEX.read_text(encoding='utf-8'))

    if len(sys.argv) > 2 and sys.argv[1] == "--file":
        rel_path = sys.argv[2]
        # 确保是相对路径
        if os.path.isabs(rel_path):
            rel_path = os.path.relpath(rel_path, str(VAULT_ROOT))
        print(f"Updating index for: {rel_path}")
        index = update_index_for_file(rel_path, index)

    elif len(sys.argv) > 2 and sys.argv[1] == "--dir":
        target_dir = sys.argv[2]
        if os.path.isabs(target_dir):
            target_dir = os.path.relpath(target_dir, str(VAULT_ROOT))
        dir_path = VAULT_ROOT / target_dir
        if not dir_path.exists():
            print(f"Error: {dir_path} not found.")
            sys.exit(1)
        files = list(dir_path.glob("**/*.md"))
        print(f"Re-scanning {len(files)} files in {target_dir}...")
        for i, f in enumerate(files, 1):
            rel = os.path.relpath(str(f), str(VAULT_ROOT))
            if i % 10 == 0:
                print(f"  Progress: {i}/{len(files)}")
            index = update_index_for_file(rel, index)
    else:
        print("Usage:")
        print("  python scripts/update_topic_index.py --file <relative_path>")
        print("  python scripts/update_topic_index.py --dir <relative_dir>")
        sys.exit(1)

    TOPIC_INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Updated {TOPIC_INDEX} ({len(index.get('topics', {}))} topics)")


if __name__ == "__main__":
    main()
