#!/usr/bin/env python3
"""
retro_fix_L1.py
修复 L1 硬性阻断问题：frontmatter 缺失字段 + 编码问题
"""
import sys
import os
from pathlib import Path
import re
import yaml
from datetime import datetime
from typing import Dict, Tuple, List
# Force UTF-8 mode on Windows
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

WIKI_ROOT = Path("D:/AI agent/tkk-library/wiki")
TODAY = datetime.now().strftime("%Y-%m-%d")

def parse_frontmatter(content: str) -> Tuple[Dict, str]:
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return {}, content
    try:
        fields = yaml.safe_load(match.group(1)) or {}
        body = content[match.end():]
        return fields, body
    except:
        return {}, content

def detect_type_from_filename(filename: str, content: str) -> str:
    """根据文件名和内容检测文件类型"""
    fname_lower = filename.lower()

    # 根据目录检测
    if "_concept_" in filename or filename.startswith("concept_"):
        return "concept"
    if "_entity_" in filename or filename.startswith("entity_"):
        return "entity"
    if "_synthesis_" in filename or filename.startswith("synthesis_"):
        return "synthesis"
    if "_summary_" in filename or filename.startswith("summary_"):
        return "summary"

    # 根据内容检测
    if "司解释" in content or "法释[" in content or "法释〔" in content:
        if "条文" in content or "第xx条" in content.lower():
            return "entity"
    if "理解与适用" in content or "司法解释全书" in content:
        return "concept"
    if "律师办理" in content and ("指引" in content or "操作指引" in content):
        return "summary"
    if "指导性案例" in content or "检例" in content:
        return "synthesis"
    if "审判指导" in content or "审判参考" in content:
        return "synthesis"

    return "summary"  # 默认

def fix_file(filepath: Path) -> List[str]:
    """修复单个文件，返回修复的问题列表"""
    fixes = []
    try:
        content = filepath.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            content = filepath.read_text(encoding="gbk")
            fixes.append("使用GBK编码读取")
        except:
            fixes.append("无法读取编码，跳过")
            return fixes

    # 检测编码问题
    if "\\u" in content or "\\x" in content:
        fixes.append("存在Unicode转义序列")

    fields, body = parse_frontmatter(content)

    # 检测缺失的frontmatter
    if not fields.get("type"):
        detected_type = detect_type_from_filename(filepath.name, content)
        fields["type"] = detected_type
        fixes.append(f"添加type={detected_type}")

    if not fields.get("created"):
        # 尝试从文件名提取日期
        date_match = re.search(r'(\d{4})[_-]?(\d{2})[_-]?(\d{2})', filepath.name)
        if date_match:
            fields["created"] = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
        else:
            fields["created"] = TODAY
        fixes.append(f"添加created={fields['created']}")

    if not fields.get("title"):
        title = filepath.stem
        # 去除类型前缀
        for prefix in ["concept_", "entity_", "synthesis_", "summary_"]:
            if title.startswith(prefix):
                title = title[len(prefix):]
                break
        # 去除日期前缀
        title = re.sub(r'^\d{8}[_-]?', '', title)
        title = re.sub(r'^\[\d{4}-\d{2}-\d{2}\]\s*', '', title)
        title = title.replace('_', ' ').replace('-', ' ')
        fields["title"] = title
        fixes.append(f"添加title={fields['title']}")

    if not fields.get("updated"):
        fields["updated"] = TODAY
        fixes.append(f"添加updated={fields['updated']}")

    # 对于 summaries 类型，检测 category
    if fields.get("type") == "summary" and not fields.get("category"):
        # 根据文件名推测 category
        fname = filepath.name.lower()
        if any(k in fname for k in ["劳动", "雇佣", "工伤", "社保"]):
            fields["category"] = "劳动与社会保障"
        elif any(k in fname for k in ["公司", "股权", "证券", "破产", "投资"]):
            fields["category"] = "公司商事与合规"
        elif any(k in fname for k in ["建筑", "工程", "房地产", "物业"]):
            fields["category"] = "建筑工程与房地产"
        elif any(k in fname for k in ["婚姻", "继承", "家庭", "抚养"]):
            fields["category"] = "婚姻家庭与继承"
        elif any(k in fname for k in ["医疗", "药品", "健康", "医院"]):
            fields["category"] = "医药健康"
        elif any(k in fname for k in ["国际", "外贸", "海关", "出口", "进口"]):
            fields["category"] = "国际贸易"
        elif any(k in fname for k in ["政府", "行政", "信访", "公共"]):
            fields["category"] = "政府与公共法律服务"
        elif any(k in fname for k in ["环境", "能源", "生态", "污染"]):
            fields["category"] = "生态环境与能源"
        elif any(k in fname for k in ["知识产权", "商标", "专利", "著作权", "版权"]):
            fields["category"] = "知识产权"
        elif any(k in fname for k in ["税务", "财务", "会计", "税"]):
            fields["category"] = "金融与财税"
        elif any(k in fname for k in ["刑事", "犯罪", "盗窃", "诈骗", "贪污", "受贿", "杀人", "伤害"]):
            fields["category"] = "刑事参考"
        else:
            fields["category"] = "诉讼与仲裁"  # 默认
        fixes.append(f"添加category={fields['category']}")

    if not fields.get("tags"):
        fields["tags"] = ["待分类"]
        fixes.append("添加tags=待分类")

    # 如果有修复，重写文件
    if fixes:
        new_frontmatter = "---\n"
        for key, value in fields.items():
            if isinstance(value, list):
                new_frontmatter += f"{key}: [{', '.join(str(v) for v in value)}]\n"
            else:
                new_frontmatter += f"{key}: {value}\n"
        new_frontmatter += "---\n"
        new_content = new_frontmatter + body

        # 跳过 Unicode 转义修复（由 Phase 2 处理）

        try:
            filepath.write_text(new_content, encoding="utf-8")
        except:
            fixes.append("写入失败")

    return fixes

def main():
    results = {"fixed": [], "skipped": [], "errors": []}
    total = 0

    for subdir in ["concepts", "entities", "summaries", "syntheses"]:
        dir_path = WIKI_ROOT / subdir
        if not dir_path.exists():
            continue
        for filepath in dir_path.glob("*.md"):
            total += 1
            fixes = fix_file(filepath)
            if fixes:
                if "跳过" in fixes or "失败" in fixes[-1] if fixes else False:
                    results["skipped"].append(f"{subdir}/{filepath.name}: {', '.join(fixes)}")
                else:
                    results["fixed"].append(f"{subdir}/{filepath.name}: {', '.join(fixes)}")

    print(f"=== L1 修复报告 ===")
    print(f"总计检查: {total} 个文件")
    print(f"已修复: {len(results['fixed'])} 个")
    print(f"跳过/错误: {len(results['skipped'])} 个")
    print()

    if results["fixed"]:
        print(f"--- 已修复 (前30项) ---")
        for item in results["fixed"][:30]:
            print(f"  [+] {item}")
        if len(results["fixed"]) > 30:
            print(f"  ... 还有 {len(results['fixed'])-30} 项")
        print()

    if results["skipped"]:
        print(f"--- 跳过/错误 (前20项) ---")
        for item in results["skipped"][:20]:
            print(f"  [!] {item}")
        print()

if __name__ == "__main__":
    main()
