#!/usr/bin/env python3
"""处理检答网集萃36-70转换为V52格式"""

import os
import re
import glob

SOURCE_DIR = r"D:\AI agent\tkk-library\sources\微信公号资料\最高人民检察院\最高检-检答网集萃-md"
TARGET_DIR = r"D:\AI agent\tkk-library\wiki\summaries"

def process_file(filepath):
    """处理单个文件"""
    filename = os.path.basename(filepath)

    # 提取日期 [YYYY-MM-DD]
    date_match = re.search(r'\[(\d{4}-\d{2}-\d{2})\]', filename)
    date = date_match.group(1) if date_match else "2021-01-01"

    # 提取集萃编号
    num_match = re.search(r'检答网集萃(\d+)', filename)
    num = num_match.group(1) if num_match else "36"

    # 提取标题（去除日期前缀和.md后缀）
    title_raw = re.sub(r'^\[[\d-]+\]', '', filename)  # 去除日期
    title_raw = re.sub(r'^检答网集萃\d+', '', title_raw)  # 去除集萃编号
    title_raw = title_raw.replace('.md', '').strip()  # 去除.md

    # 读取源文件内容
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取咨询类别
    category_match = re.search(r'咨询类别：\s*(.+?)(?=\n|咨询人)', content, re.DOTALL)
    category = category_match.group(1).strip() if category_match else "法律政策"

    # 提取咨询人
    consultant_match = re.search(r'咨询人：\s*(.+?)(?=\n|咨询内容)', content, re.DOTALL)
    consultant = consultant_match.group(1).strip() if consultant_match else ""

    # 提取咨询内容
    consult_content_match = re.search(r'咨询内容：(.+?)(?=个人意见|$)', content, re.DOTALL)
    consult_content = consult_content_match.group(1).strip() if consult_content_match else ""

    # 提取个人意见
    personal_match = re.search(r'个人意见（理由和依据）：(.+?)(?=解答专家|$)', content, re.DOTALL)
    personal_opinion = personal_match.group(1).strip() if personal_match else ""

    # 提取解答专家
    expert_match = re.search(r'解答专家[^\n]*\n*(.+?)(?=往期回顾|$)', content, re.DOTALL)
    expert_response = expert_match.group(1).strip() if expert_match else ""

    # 清理内容（去除多余空白、链接等）
    def clean_text(text):
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # 去掉链接
        text = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', text)  # 去掉加粗标记
        text = re.sub(r'\n{3,}', '\n\n', text)  # 压缩多余换行
        text = re.sub(r'^[\s]+', '', text, flags=re.MULTILINE)  # 去除行首空白
        text = text.strip()
        return text

    consult_content = clean_text(consult_content)
    personal_opinion = clean_text(personal_opinion)
    expert_response = clean_text(expert_response)

    # 构建目标文件内容
    qa_summary = f"""咨询类别：{category}
咨询人：{consultant}

**咨询内容：**
{consult_content}

**个人意见：**
{personal_opinion}

**解答专家意见：**
{expert_response}"""

    output_content = f"""---
title: 检答网集萃{num} {title_raw}
type: summary
created: 2026-05-07
updated: 2026-05-07
tags: [检察业务]
category: 诉讼与仲裁
source: {filename}
---

## 📋 文档概览

| 字段 | 内容 |
|------|------|
| 来源 | {filename} |
| 类型 | 检察业务咨询 |
| 发布日期 | {date} |
| 关键词 | 检察业务/法律咨询 |
| 核心要点 | 详见下方问答摘要 |

## 问答摘要
{qa_summary}
"""

    # 目标文件名
    target_filename = f"summary_检答网集萃{num}_{title_raw}.md"
    target_path = os.path.join(TARGET_DIR, target_filename)

    # 写入文件
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(output_content)

    return target_filename, None

def main():
    # 确保目标目录存在
    os.makedirs(TARGET_DIR, exist_ok=True)

    # 获取所有源文件
    all_files = os.listdir(SOURCE_DIR)

    # 筛选36-70的文件
    pattern = re.compile(r'检答网集萃([3-6]\d|70)')
    files = [f for f in all_files if pattern.search(f)]

    # 排序
    files.sort()

    success = 0
    failed = []
    results = []

    for filename in files:
        filepath = os.path.join(SOURCE_DIR, filename)
        try:
            target_name, _ = process_file(filepath)
            success += 1
            results.append(f"[OK] {filename} -> {target_name}")
        except Exception as e:
            failed.append(filename)
            results.append(f"[FAIL] {filename}: {str(e)}")

    # 输出结果
    print("=" * 60)
    print(f"处理完成！成功: {success}, 失败: {len(failed)}")
    print("=" * 60)
    for r in results:
        print(r)

    if failed:
        print("\n失败的文件:")
        for f in failed:
            print(f"  - {f}")

if __name__ == "__main__":
    main()