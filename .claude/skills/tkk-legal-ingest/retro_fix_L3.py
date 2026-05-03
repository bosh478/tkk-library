#!/usr/bin/env python3
"""
retro_fix_L3.py
修复 L3 source 字段缺失和 category 值问题
"""
import sys
import os
from pathlib import Path
import re
from datetime import datetime
# Force UTF-8 mode on Windows
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

WIKI_ROOT = Path("D:/AI agent/tkk-library/wiki")

CATEGORY_VALUES = [
    "诉讼与仲裁", "公司商事与合规", "劳动与社会保障", "医药健康",
    "国际贸易", "婚姻家庭与继承", "建筑工程与房地产", "政府与公共法律服务",
    "生态环境与能源", "知识产权", "金融与财税", "刑事参考"
]

def infer_category(filename: str) -> str:
    """根据文件名推断 category"""
    text = filename.lower()

    if any(k in text for k in ["劳动", "雇佣", "工伤", "社保"]):
        return "劳动与社会保障"
    elif any(k in text for k in ["公司", "股权", "证券", "破产"]):
        return "公司商事与合规"
    elif any(k in text for k in ["建筑", "工程", "房地产", "物业"]):
        return "建筑工程与房地产"
    elif any(k in text for k in ["婚姻", "继承", "家庭", "抚养"]):
        return "婚姻家庭与继承"
    elif any(k in text for k in ["医疗", "药品", "健康"]):
        return "医药健康"
    elif any(k in text for k in ["国际", "外贸", "海关"]):
        return "国际贸易"
    elif any(k in text for k in ["政府", "行政", "信访"]):
        return "政府与公共法律服务"
    elif any(k in text for k in ["环境", "能源", "生态"]):
        return "生态环境与能源"
    elif any(k in text for k in ["知识产权", "商标", "专利", "著作权"]):
        return "知识产权"
    elif any(k in text for k in ["税务", "财务", "会计", "税"]):
        return "金融与财税"
    elif any(k in text for k in ["刑事", "犯罪", "盗窃", "诈骗", "贪污", "受贿"]):
        return "刑事参考"
    else:
        return "诉讼与仲裁"

def fix_file(filepath: Path) -> int:
    """修复文件，返回修复数量"""
    try:
        content = filepath.read_text(encoding="utf-8")
    except:
        return 0

    fixed = 0
    lines = content.split("\n")
    new_lines = []
    source_added = False
    category_fixed = False

    for line in lines:
        new_lines.append(line)

        # 修复 category 值
        if line.startswith("category:"):
            cat_value = line.split(":", 1)[1].strip()
            if cat_value not in CATEGORY_VALUES:
                new_lines[-1] = f"category: {infer_category(filepath.name)}"
                category_fixed = True
                fixed += 1

        # 添加 source 字段
        if not source_added and line.startswith("tags:"):
            new_lines.append(f"source: 〔来源文件不存在〕")
            source_added = True
            fixed += 1

    if fixed > 0:
        new_content = "\n".join(new_lines)
        try:
            filepath.write_text(new_content, encoding="utf-8")
        except:
            return 0

    return fixed

def main():
    fixed = 0
    for subdir in ["summaries", "concepts", "syntheses"]:
        dir_path = WIKI_ROOT / subdir
        if not dir_path.exists():
            continue
        for filepath in dir_path.glob("*.md"):
            if fix_file(filepath):
                fixed += 1

    print(f"已修复 {fixed} 个文件的 L3 问题")

if __name__ == "__main__":
    main()
