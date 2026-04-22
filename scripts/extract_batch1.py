#!/usr/bin/env python3
"""Extract first batch of topics from 裁判要旨精选"""

import re

source_file = r"D:\AI agent\tkk-library\sources\司法观点、案例\《最高人民法院裁判要旨精选》中 最高法审管办 202504.md"

# Read the source file
with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Define topic patterns and extract boundaries
# Topics to extract for batch 1 (20 topics)
topics_batch1 = [
    "借款合同、民间借贷",
    "金融借款合同",
    "金融不良债权转让、追偿合同",
    "租赁合同",
    "融资租赁合同",
    "保理合同",
    "建设工程合同",
    "其他合同纠纷",
    "合伙",
    "股东资格确认",
    "请求变更公司登记",
    "股东出资",
    "股权转让",
    "股东知情权",
    "公司决议",
    "盈余分配",
    "损害公司利益责任",
    "人格混同及损害债权人利益",
    "公司减资",
    "公司解散",
]

# Find the start of 民商事篇 section
civil_section_match = re.search(r'## 民商事篇', content)
if not civil_section_match:
    print("Cannot find 民商事篇 section")
    exit(1)

civil_start = civil_section_match.start()
print(f"民商事篇 starts at position {civil_start}")

# Find the end marker (next major section or end of content)
# Look for ## 环境资源篇 or other section markers
next_section_match = re.search(r'\n## 环境资源篇', content)
if next_section_match:
    civil_end = next_section_match.start()
else:
    civil_end = len(content)

print(f"民商事篇 ends at position {civil_end}")

# Extract civil section
civil_section = content[civil_start:civil_end]

# Find all topic positions using the table of contents pattern
# The table of contents shows: 主题名……页码
toc_pattern = re.compile(r'([^……\n]+)……\s*(\d+)')

# Find all ## headers in the section
header_pattern = re.compile(r'^## ●(.+)$|^## (.+)$', re.MULTILINE)

# For now, let's find topics by looking for numbered cases
# Pattern: # N 主题名 or ## ●主题名

# First, let's identify where each topic section is by looking at the table of contents
# which appears at the beginning (lines ~15-108 based on earlier reading)

# Look for the actual content sections (not the table of contents)
# Content sections appear to start with ## 【裁判要旨】 or # case titles

# Let's look for the pattern: topics start with a line that looks like "## 主题名" followed by cases

# Define our batch 1 extraction
# We'll extract cases starting from specific markers

output_dir = r"D:\AI agent\tkk-library\wiki\syntheses"

# Function to extract case content
def extract_case_content(case_text):
    """Extract and format case content"""
    lines = case_text.strip().split('\n')
    formatted = []
    for line in lines:
        line = line.strip()
        if line:
            formatted.append(line)
    return '\n'.join(formatted)

# For the first batch, we need to identify content around specific case numbers
# Based on the table of contents, topics are around:
# 借款合同、民间借贷 - page 217
# But the actual content starts later in the file

# Let me check for actual content markers
# Cases seem to start with patterns like:
# # N 案例名称 (案号)
# ## 【裁判要旨】

print("\nSearching for case content patterns...")

# Find case content starting points
case_pattern = re.compile(r'^# \d+ (.+?)(?:申请再审案|再审案|上诉案|纠纷案|确认案)', re.MULTILINE)
matches = case_pattern.findall(civil_section)
print(f"Found {len(matches)} case titles in civil section")

# Let's print first 30 to understand structure
print("\nFirst 30 case titles found:")
for i, m in enumerate(matches[:30]):
    print(f"  {i+1}: {m[:60]}...")