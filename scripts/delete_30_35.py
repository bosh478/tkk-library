#!/usr/bin/env python3
"""删除检答网集萃30-35的文件"""

import os

TARGET_DIR = r"D:\AI agent\tkk-library\wiki\summaries"

files_to_delete = [
    "summary_检答网集萃30_检察长作为独任检察官或主办检察官办案的几个问题.md",
    "summary_检答网集萃31_容留介绍卖淫罪的入罪标准.md",
    "summary_检答网集萃32_销售伪劣产品的犯罪数额问题.md",
    "summary_检答网集萃33_公安侦查阶段执行取保或监视居住已获人大许可检察环节是否还需重报.md",
    "summary_检答网集萃34_留置人员立案后如何采取强制措施.md",
    "summary_检答网集萃35_对于作出不起诉决定的案件作为证据使用的作案工具如何处理.md",
]

for f in files_to_delete:
    path = os.path.join(TARGET_DIR, f)
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted: {f}")
    else:
        print(f"Not found: {f}")

print("\nDone.")