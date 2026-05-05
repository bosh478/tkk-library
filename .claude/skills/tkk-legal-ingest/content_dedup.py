#!/usr/bin/env python3
"""
content_dedup.py
Clippings 去重检测脚本 - 同一篇文章被多次转载时，判断原始来源 vs 转载版本

用法:
    python content_dedup.py <file.md> [file2.md ...]
    python content_dedup.py D:/AI\ agent/tkk-library/Clippings/*.md

处理流程：
1. 读取 Clippings 中的待检测文件
2. 与 wiki/summaries/ 下已有 wiki 页面比对
3. 判断是否为同一篇文章
4. 追溯发布时间和来源
5. 输出决策报告（保留 wiki / 保留 Clippings）

删除操作：
- 保留 wiki：删除 Clippings 中的转载版本
- 保留 Clippings：删除 wiki 中已有的旧页面（转载版）
"""

import os
import sys
import re
import glob
import hashlib
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from datetime import datetime

WIKI_ROOT = Path("D:/AI agent/tkk-library/wiki")
CLIPPINGS_DIR = Path("D:/AI agent/tkk-library/Clippings")
SOURCES_DIR = Path("D:/AI agent/tkk-library/sources")

# 平台权威性评级（数字越大越权威）
CREDIBILITY_RATING = {
    # 官方来源
    "最高人民法院": 100,
    "最高人民检察院": 100,
    "全国人民代表大会": 100,
    "全国人大常委会": 100,
    "国务院": 100,
    "司法部": 95,
    "公安部": 95,
    "法释": 90,  # 司法解释
    "法检联发": 90,
    # 专业来源
    "省高级人民法院": 80,
    "省人民检察院": 80,
    "高级人民法院": 80,
    "人民检察院": 80,
    "中国法学会": 75,
    "中华全国律师协会": 75,
    "律师协会": 70,
    # 一般来源
    "人民法院报": 60,
    "检察日报": 60,
    "法制日报": 60,
    "law": 50,
    "法律": 50,
    # 自媒体/转载
    "公众号": 30,
    "百家号": 20,
    "转载": 10,
    "来自": 5,
}

def extract_text_content(content: str) -> str:
    """提取纯文本内容（去HTML标签、markdown格式）"""
    # 去除 HTML 标签
    text = re.sub(r'<[^>]+>', '', content)
    # 去除 markdown 图片
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # 去除 markdown 链接，保留文字
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    # 去除 frontmatter
    text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)
    # 去除代码块
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    # 去除多余空白
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def compute_content_hash(content: str, length: int = 200) -> str:
    """计算内容指纹（基于前 N 个字符的 hash）"""
    text = extract_text_content(content)
    excerpt = text[:length] if len(text) >= length else text
    return hashlib.md5(excerpt.encode('utf-8')).hexdigest()


def extract_publish_info(content: str) -> Dict[str, str]:
    """提取文章发布时间和来源信息"""
    info = {
        "publish_date": None,
        "source_platform": None,
        "author": None,
        "title": None,
    }

    # 提取标题（从 frontmatter 或第一行 H1）
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        info["title"] = title_match.group(1).strip()

    # 从 frontmatter 提取
    fm_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if fm_match:
        fm = fm_match.group(1)
        date_match = re.search(r'(?:published|created|date)[:：]\s*"?(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?)"?', fm)
        if date_match:
            info["publish_date"] = normalize_date(date_match.group(1))
        source_match = re.search(r'(?:source|from|url)[:：]\s*(.+?)(?:\n|$)', fm)
        if source_match:
            info["source_platform"] = source_match.group(1).strip()
        author_match = re.search(r'(?:author|作者)[:：]\s*(.+?)(?:\n|$)', fm)
        if author_match:
            info["author"] = author_match.group(1).strip()

    # 从正文提取发布日期模式
    if not info["publish_date"]:
        date_patterns = [
            r'(\d{4})年(\d{1,2})月(\d{1,2})日',
            r'(\d{4})-(\d{1,2})-(\d{1,2})',
            r'(\d{4})/(\d{1,2})/(\d{1,2})',
        ]
        for pattern in date_patterns:
            date_match = re.search(pattern, content[:500])
            if date_match:
                info["publish_date"] = f"{date_match.group(1)}-{date_match.group(2).zfill(2)}-{date_match.group(3).zfill(2)}"
                break

    # 从正文提取来源平台
    if not info["source_platform"]:
        platform_patterns = [
            r'来源[:：]\s*([^\n，。]+)',
            r'发布[:：]\s*([^\n，。]+)',
            r'作者[:：]\s*([^\n，。]+)',
        ]
        for pattern in platform_patterns:
            platform_match = re.search(pattern, content[:1000])
            if platform_match:
                info["source_platform"] = platform_match.group(1).strip()
                break

    return info


def normalize_date(date_str: str) -> Optional[str]:
    """标准化日期格式为 YYYY-MM-DD"""
    if not date_str:
        return None
    # 去除年月日和日字符
    date_str = re.sub(r'[年/月/日]', '-', date_str)
    date_str = date_str.rstrip('-')
    # 尝试解析
    try:
        parts = date_str.split('-')
        if len(parts) == 3:
            year, month, day = parts[0], parts[1].zfill(2), parts[2].zfill(2)
            return f"{year}-{month}-{day}"
    except:
        pass
    return date_str if date_str else None


def get_platform_credibility(platform: str) -> int:
    """获取平台权威性评分"""
    if not platform:
        return 0
    max_cred = 0
    for keyword, rating in CREDIBILITY_RATING.items():
        if keyword in platform:
            max_cred = max(max_cred, rating)
    return max_cred


def compare_articles(clippings_content: str, wiki_content: str) -> Tuple[bool, float, Dict]:
    """
    比较两篇文章是否为同一篇
    返回: (是否相似, 相似度分数, 详细信息)
    """
    details = {
        "clippings_hash": compute_content_hash(clippings_content),
        "wiki_hash": compute_content_hash(wiki_content),
        "hash_match": False,
        "title_similarity": 0.0,
        "publish_date_match": False,
    }

    # 1. 内容指纹比对
    clips_hash = details["clippings_hash"]
    wiki_hash = details["wiki_hash"]
    details["hash_match"] = (clips_hash == wiki_hash)

    # 2. 标题相似度（简单 word overlap）
    clips_title = re.search(r'^#\s+(.+)$', clippings_content, re.MULTILINE)
    wiki_title = re.search(r'^#\s+(.+)$', wiki_content, re.MULTILINE)
    if clips_title and wiki_title:
        c_words = set(clips_title.group(1).split())
        w_words = set(wiki_title.group(1).split())
        if c_words and w_words:
            overlap = len(c_words & w_words) / len(c_words | w_words)
            details["title_similarity"] = overlap

    # 3. 发布时间是否相同
    clips_info = extract_publish_info(clippings_content)
    wiki_info = extract_publish_info(wiki_content)
    if clips_info["publish_date"] and wiki_info["publish_date"]:
        details["publish_date_match"] = (clips_info["publish_date"] == wiki_info["publish_date"])
        details["clippings_date"] = clips_info["publish_date"]
        details["wiki_date"] = wiki_info["publish_date"]
    else:
        details["clippings_date"] = clips_info["publish_date"]
        details["wiki_date"] = wiki_info["publish_date"]

    details["clippings_platform"] = clips_info.get("source_platform")
    details["wiki_platform"] = wiki_info.get("source_platform")

    # 计算总体相似度
    similarity = 0.0
    if details["hash_match"]:
        similarity = 1.0
    elif details["title_similarity"] >= 0.7:
        similarity = details["title_similarity"] * 0.8
    elif details["title_similarity"] >= 0.5:
        similarity = details["title_similarity"] * 0.6

    return similarity >= 0.7, similarity, details


def find_matching_wiki_pages(clippings_file: Path) -> List[Tuple[Path, float, Dict]]:
    """在 wiki/summaries/ 中查找与 Clippings 文件相似的页面"""
    matches = []

    try:
        clippings_content = clippings_file.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[ERROR] 无法读取文件 {clippings_file}: {e}")
        return matches

    # 遍历 wiki/summaries/ 下所有 md 文件
    if not (WIKI_ROOT / "summaries").exists():
        return matches

    for wiki_file in (WIKI_ROOT / "summaries").glob("*.md"):
        try:
            wiki_content = wiki_file.read_text(encoding="utf-8")
            is_similar, score, details = compare_articles(clippings_content, wiki_content)
            if is_similar:
                matches.append((wiki_file, score, details))
        except Exception as e:
            continue

    # 按相似度排序
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches


def make_decision(details: Dict, clippings_cred: int, wiki_cred: int) -> Tuple[str, str]:
    """
    判断应该保留哪个版本
    返回: (决策, 原因)
    """
    decision = "KEEP_CLIPPINGS"  # 默认保留 Clippings（假设更早/更权威）
    reason = ""

    # 1. 发布时间判断
    clippings_date = details.get("clippings_date")
    wiki_date = details.get("wiki_date")

    if clippings_date and wiki_date:
        if clippings_date < wiki_date:
            decision = "KEEP_CLIPPINGS"
            reason = f"Clippings 发布时间更早 ({clippings_date} < {wiki_date})"
        elif clippings_date > wiki_date:
            decision = "KEEP_WIKI"
            reason = f"Wiki 来源发布时间更早 ({wiki_date} < {clippings_date})"
        else:
            # 同一天，看权威性
            reason = f"发布时间相同 ({clippings_date})，"
    elif clippings_date:
        decision = "KEEP_CLIPPINGS"
        reason = f"Clippings 有明确发布时间 ({clippings_date})"
    elif wiki_date:
        decision = "KEEP_WIKI"
        reason = f"Wiki 来源有明确发布时间 ({wiki_date})"
    else:
        reason = "均无明确发布时间，"

    # 2. 平台权威性判断
    if decision == "KEEP_CLIPPINGS":
        reason += f"，Clippings 平台权威性评分 {clippings_cred}"
        if clippings_cred < wiki_cred and wiki_cred > 50:
            decision = "KEEP_WIKI"
            reason = f"Wiki 平台权威性更高 ({wiki_cred} > {clippings_cred})"
    else:
        reason += f"，Wiki 平台权威性评分 {wiki_cred}"
        if clippings_cred > wiki_cred and clippings_cred > 50:
            decision = "KEEP_CLIPPINGS"
            reason = f"Clippings 平台权威性更高 ({clippings_cred} > {wiki_cred})"

    return decision, reason


def process_file(clippings_file: Path) -> Optional[Dict]:
    """处理单个 Clippings 文件"""
    result = {
        "file": str(clippings_file),
        "status": "NEW",  # NEW / DUPLICATE / ERROR
        "match": None,
        "decision": None,
        "reason": None,
    }

    matches = find_matching_wiki_pages(clippings_file)

    if not matches:
        result["status"] = "NEW"
        return result

    # 取最相似的匹配
    best_match, score, details = matches[0]
    result["status"] = "DUPLICATE"
    result["match"] = {
        "wiki_file": str(best_match.relative_to(WIKI_ROOT)),
        "similarity": score,
        "details": details,
    }

    # 获取权威性评分
    clips_cred = get_platform_credibility(details.get("clippings_platform", ""))
    wiki_cred = get_platform_credibility(details.get("wiki_platform", ""))

    # 做决策
    decision, reason = make_decision(details, clips_cred, wiki_cred)
    result["decision"] = decision
    result["reason"] = reason

    return result


def delete_file(filepath: Path) -> bool:
    """删除文件"""
    try:
        if filepath.exists():
            filepath.unlink()
            return True
    except Exception as e:
        print(f"[ERROR] 删除失败 {filepath}: {e}")
    return False


def main():
    if len(sys.argv) < 2:
        print("用法: python content_dedup.py <file.md> 或 python content_dedup.py <dir/*.md>")
        sys.exit(1)

    # 解析输入文件
    input_path = sys.argv[1]
    if '*' in input_path:
        files = glob.glob(input_path)
    elif os.path.isdir(input_path):
        files = glob.glob(os.path.join(input_path, '*.md'))
    else:
        files = [input_path]

    if not files:
        print(f"未找到文件: {input_path}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print("Clippings 去重检测报告")
    print(f"{'='*60}\n")

    results = []
    for filepath in files:
        clippings_file = Path(filepath)
        if not clippings_file.exists():
            continue
        result = process_file(clippings_file)
        if result:
            results.append(result)

    # 输出报告
    new_count = 0
    duplicate_count = 0

    for result in results:
        filename = Path(result["file"]).name
        print(f"[{result['status']}] {filename}")

        if result["status"] == "NEW":
            new_count += 1
            print(f"  → 全新内容，进入 ingest 流程")
        elif result["status"] == "DUPLICATE":
            duplicate_count += 1
            print(f"  → 重复内容，匹配到: {result['match']['wiki_file']}")
            print(f"  → 相似度: {result['match']['similarity']:.1%}")
            print(f"  → 决策: {result['decision']}")
            print(f"  → 原因: {result['reason']}")

            # 执行删除操作
            if result['decision'] == 'KEEP_WIKI':
                # 删除 Clippings 文件
                if delete_file(Path(result['file'])):
                    print(f"  → 已删除 Clippings: {filename}")
            elif result['decision'] == 'KEEP_CLIPPINGS':
                # 删除 wiki 旧页面
                wiki_file = WIKI_ROOT / result['match']['wiki_file']
                if delete_file(wiki_file):
                    print(f"  → 已删除 wiki 旧页面: {result['match']['wiki_file']}")
        print()

    # 汇总
    print(f"{'='*60}")
    print(f"汇总: {len(results)} 个文件")
    print(f"  - 全新内容: {new_count} 个 → 进入 ingest 流程")
    print(f"  - 重复内容: {duplicate_count} 个 → 已处理")

    # 如果有重复，提示需要重新执行 ingest
    if duplicate_count > 0:
        print(f"\n⚠️ 注意: 有 {duplicate_count} 个重复文件被处理")
        print("   如果保留了 Clippings 文件，请手动触发 ingest 流程")

    sys.exit(0 if duplicate_count == 0 else 1)


if __name__ == "__main__":
    main()
