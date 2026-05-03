#!/usr/bin/env python3
"""
retro_fix_L1_category.py
修复 L1 category 字段缺失问题
"""
import sys
import os
from pathlib import Path
import re
from datetime import datetime

WIKI_ROOT = Path("D:/AI agent/tkk-library/wiki")
TODAY = datetime.now().strftime("%Y-%m-%d")

# category 映射规则
CATEGORY_KEYWORDS = {
    "诉讼与仲裁": ["劳动争议", "合同纠纷", "侵权", "赔偿", "仲裁", "民事", "执行", "拍卖", "强制执行", "排除执行", "相邻关系", "物业", "离婚", "继承", "抚养"],
    "公司商事与合规": ["公司", "股权", "股东", "证券", "破产", "投资", "合伙", "企业", "营商", "商业", "公司治理", "清算"],
    "劳动与社会保障": ["劳动", "雇佣", "工伤", "社保", "养老金", "工资", "劳动合同", "竞业限制", "开除", "辞职"],
    "建筑工程与房地产": ["建筑", "工程", "房地产", "物业", "施工", "装修", "租房", "买房", "业主", "电梯", "充电"],
    "婚姻家庭与继承": ["婚姻", "离婚", "继承", "家庭", "抚养", "收养", "夫妻", "子女"],
    "医药健康": ["医疗", "药品", "健康", "医院", "医生", "手术", "疾病", "药店"],
    "国际贸易": ["国际", "外贸", "海关", "出口", "进口", "跨境", "关税"],
    "政府与公共法律服务": ["政府", "行政", "信访", "公共", "规划", "许可", "审批", "监管"],
    "生态环境与能源": ["环境", "能源", "生态", "污染", "绿色", "碳"],
    "知识产权": ["知识产权", "商标", "专利", "著作权", "版权", "发明", "不正当竞争", "商业秘密"],
    "金融与财税": ["税务", "财务", "会计", "税", "发票", "逃税", "贪污", "贿赂", "挪用"],
    "刑事参考": ["刑事", "犯罪", "盗窃", "诈骗", "贪污", "受贿", "杀人", "伤害", "贩毒", "走私", "洗钱", "毒品", "醉驾", "交通肇事", "正当防卫", "强制医疗", "偷越", "妨害兴奋剂", "信息网络"],
}

def infer_category(filename: str, content: str = "") -> str:
    """根据文件名和内容推断 category"""
    text = (filename + " " + (content or "")).lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return category

    # 默认
    return "诉讼与仲裁"

def fix_file(filepath: Path) -> bool:
    """修复单个文件，返回是否修复成功"""
    try:
        content = filepath.read_text(encoding="utf-8")
    except:
        return False

    # 检查是否已有 category
    if "category:" in content and "category: []" not in content:
        return False

    # 推断 category
    category = infer_category(filepath.name, content)

    # 添加 category
    if "---" in content:
        lines = content.split("\n")
        new_lines = []
        category_added = False
        for i, line in enumerate(lines):
            new_lines.append(line)
            if not category_added and line.startswith("tags:"):
                # 在 tags 后添加 category
                new_lines.append(f"category: {category}")
                category_added = True
        if not category_added:
            # 在 frontmatter 末尾添加
            fm_end = 0
            for i, line in enumerate(lines):
                if line == "---" and i > 0:
                    fm_end = i
                    break
            if fm_end > 0:
                new_lines.insert(fm_end + 1, f"category: {category}")

        new_content = "\n".join(new_lines)
        try:
            filepath.write_text(new_content, encoding="utf-8")
            return True
        except:
            return False

    return False

def main():
    fixed = 0
    skipped = 0
    errors = 0

    for subdir in ["summaries"]:
        dir_path = WIKI_ROOT / subdir
        if not dir_path.exists():
            continue
        for filepath in dir_path.glob("*.md"):
            result = fix_file(filepath)
            if result is True:
                fixed += 1
            elif result is False:
                skipped += 1
            else:
                errors += 1

    print(f"=== L1 category 修复报告 ===")
    print(f"已修复: {fixed} 个")
    print(f"跳过: {skipped} 个")
    print(f"错误: {errors} 个")

if __name__ == "__main__":
    main()
