import os
import re
import yaml
from pathlib import Path

SOURCE_DIR = Path("D:/AI agent/tkk-library/sources/微信公号资料/最高人民检察院/最高检-检答网集萃-md")
TARGET_DIR = Path("D:/AI agent/tkk-library/wiki/summaries")

def extract_title_and_topics(content, source_filename, collection_num):
    """从源文件内容中提取标题和问答主题"""
    title = None
    topics = []

    # 方法1：从文件名提取标题（格式：[YYYY-MM-DD]检答网集萃N标题.md）
    filename_match = re.search(r'检答网集萃(\d+)(.*)\.md$', source_filename)
    if filename_match:
        raw_title = filename_match.group(2).strip()
        if raw_title:
            title = f"检答网集萃{collection_num} {raw_title}"
            topics.append(f"问答1：{raw_title[:50]}")
            return title, topics

    # 方法2：匹配第一个粗体内容
    bold_matches = re.findall(r'\*\*([^\*]+)\*\*', content, re.DOTALL)
    if bold_matches:
        first_bold = bold_matches[0]
        clean_title = first_bold.replace('\n', ' ').replace('\r', ' ').strip()
        clean_title = re.sub(r'\*+$', '', clean_title).strip()
        clean_title = clean_title.rstrip('？?').strip()
        if clean_title and len(clean_title) > 3:
            title = f"检答网集萃{collection_num} {clean_title}"
            topics.append(f"问答1：{clean_title[:50]}")
            return title, topics

    # 默认值
    title = f"检答网集萃{collection_num}"
    topics = ["问答1：内容见原文"]
    return title, topics

def find_target_file(collection_num):
    """找到对应的summary文件"""
    for f in TARGET_DIR.glob(f"summary_检答网集萃{collection_num}_*.md"):
        return f
    return None

def find_source_file(collection_num):
    """找到对应的源文件"""
    for f in SOURCE_DIR.glob(f"*集萃{collection_num}*.md"):
        return f
    return None

def determine_related(content, collection_num):
    """根据内容确定相关集萃"""
    related = []

    keywords_map = {
        "贪污": ["12", "13"],
        "挪用公款": ["12"],
        "羁押": ["2", "14"],
        "减刑": ["11"],
        "假释": ["11"],
        "公益诉讼": ["28", "38", "42"],
        "交通": ["1", "4"],
        "抢夺方向盘": ["1", "4"],
        "毒品": ["17"],
        "强奸": ["3"],
        "猥亵": ["3"],
        "抢劫": ["8"],
        "入户": ["8"],
        "非法经营": ["32"],
        "伪劣": ["32", "88"],
        "寻衅滋事": ["22", "27"],
        "强迫交易": ["27", "116"],
        "未成年人": ["45", "90", "99", "100", "108"],
        "醉驾": ["93"],
        "酒精": ["93"],
        "国家赔偿": ["76", "79", "95"],
        "司法救助": ["75", "102", "106"],
        "正当防卫": ["79"],
        "取保": ["15", "50", "80"],
        "监视居住": ["33"],
        "不起诉": ["36", "45", "68", "108"],
        "认罪认罚": ["36", "96"],
        "简易程序": ["96"],
        "管辖": ["23", "55"],
        "立功": ["26"],
        "食品药品": ["38"],
        "环境": ["42"],
        "虚假诉讼": ["65", "91"],
        "执行": ["48", "81"],
        "缓刑": ["23", "81"],
    }

    content_lower = content.lower()
    found = set()

    for keyword, related_list in keywords_map.items():
        if keyword in content_lower:
            for num_str in related_list:
                num = int(num_str)
                if num != collection_num and num not in found:
                    found.add(num)

    for num in sorted(found)[:5]:
        related.append(f"[[检答网集萃{num}]]")

    return related

def fix_file(target_file, source_file, collection_num):
    """修复单个文件"""
    if not target_file or not target_file.exists():
        return False, "目标文件不存在"

    if not source_file or not source_file.exists():
        return False, "源文件不存在"

    try:
        content = source_file.read_text(encoding='utf-8')
        target_content = target_file.read_text(encoding='utf-8')

        # 解析现有frontmatter
        if not target_content.startswith('---'):
            return False, "文件无有效frontmatter"

        parts = target_content.split('---', 2)
        if len(parts) < 3:
            return False, "frontmatter格式错误"

        frontmatter_str = parts[1]
        body = parts[2]

        try:
            frontmatter = yaml.safe_load(frontmatter_str) or {}
        except:
            frontmatter = {}

        # 提取标题和问答主题
        title, topics = extract_title_and_topics(content, source_file.name, collection_num)
        related = determine_related(content, collection_num)

        # 更新frontmatter的各个字段
        frontmatter['title'] = title
        frontmatter['type'] = 'summary'
        frontmatter['created'] = '2026-05-07'
        frontmatter['updated'] = '2026-05-07'
        frontmatter['tags'] = ['检察业务']
        frontmatter['category'] = '诉讼与仲裁'
        frontmatter['line-refs'] = topics
        frontmatter['related'] = related

        # 尝试从现有frontmatter获取source
        if 'source' not in frontmatter or not frontmatter['source']:
            frontmatter['source'] = f"[[{source_file.name}]]"

        # 移除已存在的知识网络和知识缺口section
        body = re.sub(r'\n## 📚 知识网络\n.*?(?=\n## |\Z)', '', body, flags=re.DOTALL)
        body = re.sub(r'\n## ⚠️ 知识缺口\n.*', '', body, flags=re.DOTALL)
        body = body.rstrip()

        # 生成知识网络section
        knowledge_network = "\n## 📚 知识网络\n\n| 知识点 | 原文引用 | 相关知识 |\n|--------|----------|----------|\n"
        for i, topic in enumerate(topics, 1):
            related_links = ", ".join(related[:3]) if related else "其他检答网集萃"
            knowledge_network += f"| {topic} | L{i*5}-L{i*5+3} | {related_links} |\n"

        knowledge_gap = "\n## ⚠️ 知识缺口\n\n> [!gap]+\n> 发现：本集萃涉及的法律问题可能存在后续司法解释或指导意见更新，建议核实相关规定的最新版本。"

        # 使用yaml.safe_dump生成frontmatter
        new_frontmatter = yaml.dump(frontmatter, allow_unicode=True, default_flow_style=False, sort_keys=False)

        # 重组文件
        new_content = f"---\n{new_frontmatter}---{body}\n{knowledge_network}{knowledge_gap}\n"

        target_file.write_text(new_content, encoding='utf-8')
        return True, f"成功添加line-refs({len(topics)})和related({len(related)})"

    except Exception as e:
        return False, str(e)

def main():
    success = 0
    failed = 0
    skipped = 0

    for num in range(22, 118):  # 22-117
        target_file = find_target_file(num)
        source_file = find_source_file(num)

        if not target_file:
            print(f"集萃{num}: 目标文件不存在")
            failed += 1
            continue

        ok, msg = fix_file(target_file, source_file, num)
        if ok:
            if "跳过" in msg:
                skipped += 1
            else:
                success += 1
            print(f"集萃{num}: {msg}")
        else:
            failed += 1
            print(f"集萃{num}: 失败 - {msg}")

    print(f"\n完成：成功{success}个，跳过{skipped}个，失败{failed}个")

if __name__ == "__main__":
    main()