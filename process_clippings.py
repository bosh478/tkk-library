#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理东方律师网Clippings文件的脚本
"""
import os
import re

CLIPPINGS_DIR = "D:/AI agent/tkk-library/Clippings"
SOURCES_DIR = "D:/AI agent/tkk-library/sources/网络文章"
SUMMARIES_DIR = "D:/AI agent/tkk-library/wiki/summaries"

FILES = [
    ("律师从事关税法律业务操作指引（2025）（试行） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2025-05-13", "律师从事关税法律业务操作指引（2025）（试行）", "https://www.lawyers.org.cn/info/07e2655265534a46ae31d5f329d94b88"),
    ("律师从事劳动争议调解业务操作指引（2024） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2024-03-27", "律师从事劳动争议调解业务操作指引（2024）", "https://www.lawyers.org.cn/info/1c76fa42b7be4ff69dba61aaf4c4a30d"),
    ("律师从事国际贸易合同（出口）业务操作指引（2024） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2024-03-27", "律师从事国际贸易合同（出口）业务操作指引（2024）", "https://www.lawyers.org.cn/info/2182d5480d194c4e824c8e88cc1febf2"),
    ("律师从事婚姻家事案件调解业务操作指引（2024） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2024-03-27", "律师从事婚姻家事案件调解业务操作指引（2024）", "https://www.lawyers.org.cn/info/84b2758a4c2545a1aa8b7f0298af610d"),
    ("律师从事物业服务费催收业务操作指引（2022） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2022-01-05", "律师从事物业服务费催收业务操作指引（2022）", "https://www.lawyers.org.cn/info/2f67e8c2d7794899899034c30767fb27"),
    ("律师从事物业服务费催收业务操作指引（2025）（试行） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2025-01-01", "律师从事物业服务费催收业务操作指引（2025）（试行）", "https://www.lawyers.org.cn/info/5116351d578242c5a9166e3cc4b45696"),
    ("律师从事调解业务操作指引（2021） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2021-06-24", "律师从事调解业务操作指引（2021）", "https://www.lawyers.org.cn/info/390710fa42494d729c76893037f82fd5"),
    ("律师从事金融（消费）纠纷案件调解 业务操作指引（2024） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2024-03-27", "律师从事金融（消费）纠纷案件调解业务操作指引（2024）", "https://www.lawyers.org.cn/info/5f02f6697a98469dba3ba18f9f8ae447"),
    ("律师代理临时仲裁案件业务指引（2024） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2024-12-17", "律师代理临时仲裁案件业务指引（2024）", "https://www.lawyers.org.cn/info/3e1fe5988dc64039ab226c0709a32ff1"),
    ("律师代理劳动人事争议诉讼案件操作指引（2020） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2020-12-30", "律师代理劳动人事争议诉讼案件操作指引（2020）", "https://www.lawyers.org.cn/info/3f9655f7c4f5402681a07f874a775e1a"),
    ("律师代理医保行政处罚案件操作指引（2025）（试行） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2025-08-13", "律师代理医保行政处罚案件操作指引（2025）（试行）", "https://www.lawyers.org.cn/info/b72e5ec29cdf4a43906dc09dc829ee09"),
    ("律师代理医疗机构行政处罚案件操作指引（2022） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2022-01-05", "律师代理医疗机构行政处罚案件操作指引（2022）", "https://www.lawyers.org.cn/info/e96dd790624949d38f8007253d4f368f"),
    ("律师代理医疗科技成果转化业务操作指引（2024） - 业务指引 - 业务研究大厅 - 东方律师网.md", "2024-03-27", "律师代理医疗科技成果转化业务操作指引（2024）", "https://www.lawyers.org.cn/info/638f41cb8d99433aba1da5b179883147"),
]

def clean_content(content):
    """清洗内容，删除面包屑、委员会链接块、编辑信息"""
    # Remove frontmatter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    # Remove breadcrumb (starts with '当前位置：')
    content = re.sub(r'^当前位置：.*?(?=\n\- \[|$)', '', content, flags=re.DOTALL)
    # Remove committee links block
    content = re.sub(r'^\| ESG \|.*?(?=##\s+|$)', '', content, flags=re.MULTILINE | re.DOTALL)
    # Remove editor info at end
    content = re.sub(r'\*\*策划：\*\*.*', '', content, flags=re.DOTALL)
    content = re.sub(r'\*\*执笔：\*\*.*', '', content, flags=re.DOTALL)
    content = re.sub(r'^\s*执笔：.*', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*策划：.*', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*统筹人：.*', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*策划人：.*', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*执笔人：.*', '', content, flags=re.MULTILINE)
    # Remove trailing notification and tools sections
    content = re.sub(r'\[更多\].*', '', content, flags=re.DOTALL)
    content = re.sub(r'常用工具.*', '', content, flags=re.DOTALL)
    # Remove navigation links at end
    lines = content.split('\n')
    cleaned_lines = []
    skip_section = False
    for line in lines:
        if '[更多]' in line:
            skip_section = True
            continue
        if skip_section:
            continue
        if line.strip().startswith('- [') and 'http' in line:
            continue
        if any(x in line for x in ['城市地图查询', '城市天气查询', '统计局数据公布', '万年历查询', '法院在线服务平台', '法院开庭信息检索', '诉讼费计算器']):
            continue
        cleaned_lines.append(line)
    content = '\n'.join(cleaned_lines)
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content.strip()


def process_file(source_file, published, core_title, source_url):
    """处理单个文件"""
    source_path = os.path.join(CLIPPINGS_DIR, source_file)

    if not os.path.exists(source_path):
        return False, f"文件不存在: {source_file}"

    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"读取失败: {e}"

    # Find title from H2
    title_match = re.search(r'^##\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else core_title

    # Clean content
    cleaned = clean_content(content)

    # Build output
    output_path = os.path.join(SOURCES_DIR, f"{published}_{core_title}.md")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f'''---
title: "{title}"
source: "{source_url}"
author:
published: {published}
created: 2026-04-14
description:
tags: ["clippings"]
---

''')
            f.write(cleaned)
    except Exception as e:
        return False, f"写入失败: {e}"

    # Generate summary page
    summary_content = f'''---
title: {title}
type: summary
created: 2026-04-14
updated: 2026-04-14
tags: [律师业务指引]
source: [[{published}_{core_title}.md]]
---

## 关键要点

（需要手动填写）

## 相关链接

- [[{published}_{core_title}.md]]
'''

    summary_path = os.path.join(SUMMARIES_DIR, f"{published}_{core_title}.md")
    try:
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)
    except Exception as e:
        return False, f"写入摘要失败: {e}"

    return True, f"成功: {published}_{core_title}.md"


def main():
    os.makedirs(SOURCES_DIR, exist_ok=True)
    os.makedirs(SUMMARIES_DIR, exist_ok=True)

    results = []
    for source_file, published, core_title, source_url in FILES:
        success, message = process_file(source_file, published, core_title, source_url)
        results.append((source_file, success, message))
        print(f"{'OK' if success else 'FAIL'}: {message}")

    print("\n" + "="*50)
    print(f"处理完成: {sum(1 for _, s, _ in results if s)}/{len(results)} 成功")
    failed = [(f, m) for f, s, m in results if not s]
    if failed:
        print(f"失败列表:")
        for f, m in failed:
            print(f"  - {f}: {m}")


if __name__ == "__main__":
    main()