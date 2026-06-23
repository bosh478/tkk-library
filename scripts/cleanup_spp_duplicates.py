#!/usr/bin/env python3
"""
清理 SPP 指导性案例文件中的重复章节
"""
import re
from pathlib import Path

BASE_DIR = Path(r"D:\AI agent\tkk-library\wiki\summaries")
PATTERN = "summary_SPP_GuideCase_*.md"

def cleanup_file(filepath):
    """清理文件中的重复章节"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # 移除所有知识网络和知识缺口章节（因为它们是重复添加的）
        # 找到第一个 ## 📚 知识网络
        first_kn = content.find("## 📚 知识网络")
        if first_kn != -1:
            # 找到下一个 ## 标题
            next_header = content.find("\n## ", first_kn + 1)
            if next_header != -1:
                # 截断从 next_header 之后的内容
                content = content[:first_kn]

        # 同样处理 ## ⚠️ 知识缺口
        first_kg = content.find("## ⚠️ 知识缺口")
        if first_kg != -1:
            # 找到下一个 ## 标题
            next_header = content.find("\n## ", first_kg + 1)
            if next_header != -1 and next_header < first_kg if first_kg > 0 else True:
                pass

        # 如果有多个 ## 📚 知识网络，移除从第二个开始到最后一个知识缺口之后的内容
        kn_count = content.count("## 📚 知识网络")
        kg_count = content.count("## ⚠️ 知识缺口")

        if kn_count > 1 or kg_count > 1:
            # 找到所有知识网络的位置
            positions = []
            start = 0
            while True:
                pos = content.find("## 📚 知识网络", start)
                if pos == -1:
                    break
                positions.append(pos)
                start = pos + 1

            if len(positions) > 1:
                # 找到第二个知识网络之后到文件末尾的内容
                second_kn = positions[1]
                # 找到最后一个知识缺口之后的位置
                last_kg = content.rfind("## ⚠️ 知识缺口")
                if last_kg != -1:
                    # 找到知识缺口之后的下一个 ## 标题
                    end_pos = content.find("\n## ", last_kg + 1)
                    if end_pos == -1:
                        end_pos = len(content)
                else:
                    end_pos = len(content)

                # 移除第二个知识网络到末尾的内容
                content = content[:positions[0]] + content[end_pos:]

        # 移除末尾可能残留的空行
        content = content.rstrip()

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        return False

def main():
    files = list(BASE_DIR.glob(PATTERN))
    print(f"找到 {len(files)} 个文件")

    fixed = 0
    unchanged = 0

    for filepath in sorted(files):
        if cleanup_file(filepath):
            print(f"[FIXED] {filepath.name}")
            fixed += 1
        else:
            unchanged += 1

    print(f"\n完成: 修复 {fixed} 个, 无变化 {unchanged} 个")

if __name__ == "__main__":
    main()
