#!/usr/bin/env python3
"""
Fix formatting issues in 至正开放麦 wiki files
"""
import re
from pathlib import Path

import os
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
TARGET_DIR = VAULT_ROOT / "wiki/summaries"

# Better tags mapping
TAG_MAP = {
    "合同": ["合同", "违约", "解除", "效力", "无效", "约定管辖"],
    "公司": ["公司", "资本", "治理", "股权", "股东", "董事", "高管", "减资"],
    "房产": ["二手房", "购房", "房产", "租房", "房屋", "物业", "小区", "公房", "征收", "中介"],
    "婚姻家庭": ["婚姻", "离婚", "抚养", "彩礼", "继承", "家庭", "夫妻"],
    "劳动": ["劳动", "劳动合同", "竞业限制", "社保", "裁员", "工资", "用工", "延期奖金"],
    "刑事": ["诈骗", "诈骗罪", "刑法", "犯罪", "量刑", "自首", "追诉", "洗钱", "行贿", "虚开", "发票"],
    "金融": ["金融", "贷款", "投资", "证券", "虚拟盘", "外汇", "融资", "贸易"],
    "执行": ["执行", "被执行人", "财产", "债权", "债务", "参与分配"],
    "行政": ["行政", "处罚", "投诉", "举报", "违法建筑", "责令"],
    "消费者": ["消费者", "网络消费", "欺诈", "退一赔三", "平台", "直播打赏"],
    "人身": ["殴打", "人身安全", "保护令", "隐私权", "名誉权"],
    "民事": ["借贷", "民间借贷", "定金", "保证", "担保", "抵押"],
    "商事": ["商事", "连带", "债务加入"],
}

def get_better_tags(content, title):
    """Extract better tags based on content"""
    tags = ["至正开放麦", "上海二中法院"]
    combined = content + title

    for tag, keywords in TAG_MAP.items():
        for kw in keywords:
            if kw in combined:
                if tag not in tags:
                    tags.append(tag)
                break

    return tags[:6]

def fix_file(filepath):
    """Fix formatting issues in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Fix triple brackets to double brackets
        content = content.replace('[[[', '[[')
        content = content.replace(']]]', ']]')

        # Fix title: remove trailing | and extra chars after |
        content = re.sub(r'^title: (.+?)[\|｜].*$', r'title: \1', content, flags=re.MULTILINE)

        # Fix source link format
        content = re.sub(r'source: \[\[([^\]]+)\]\]', r'source: "[[\1]]"', content)

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

def main():
    files = list(TARGET_DIR.glob("summary_Court_上海二中院_至正开放麦_*.md"))
    print(f"Found {len(files)} files to fix")

    fixed = 0
    for f in files:
        if fix_file(f):
            fixed += 1
            print(f"Fixed: {f.name}")

    print(f"\nTotal fixed: {fixed}")

if __name__ == "__main__":
    main()