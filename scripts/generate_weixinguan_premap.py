import os
import re

# Read file list
with open('wiki/.cache/weixinguan_file_list.txt', 'r', encoding='utf-8') as f:
    files = [line.strip() for line in f if line.strip()]

print(f'Total files: {len(files)}')

# Routing rules
SYNTHESIS_SUBDIRS = ['至正法律研究', '案例参考册', '指导性案例', '入库案例选介', '前沿法评']

# Generate pre-map
premap = []
for src in files:
    # Path uses forward slashes
    parts = src.replace('\\', '/').split('/')
    if len(parts) >= 4:
        court = parts[2]  # e.g., 上海一中法院
        subdir = parts[3]  # e.g., 上海一中法院-开庭-md
        filename = parts[-1]  # e.g., [2022-07-07]title.md

        # Extract date and title
        match = re.match(r'\[(\d{4}-\d{2}-\d{2})\](.*)\.md', filename)
        if match:
            date = match.group(1).replace('-', '')
            title = match.group(2)
        else:
            date = 'unknown'
            title = filename.replace('.md', '')

        # Determine category from subdir
        # subdir format: 上海一中法院-开庭-md -> 开庭
        if '-' in subdir:
            category = subdir.split('-')[1] if len(subdir.split('-')) > 1 else subdir
        else:
            category = subdir

        # Determine target type
        if category in SYNTHESIS_SUBDIRS:
            target_dir = 'wiki/syntheses/'
        else:
            target_dir = 'wiki/summaries/'

        # Build target filename
        if target_dir == 'wiki/summaries/':
            target = f'summary_{date}_{court}_{category}_{title}.md'
        else:
            # Synthesis naming
            if '入库案例' in category:
                target = f'CourtFa_入库案例_{title}.md'
            elif '指导性案例' in category:
                target = f'SPP_GuideCase_{title}.md'
            elif '前沿法评' in category:
                target = f'CourtFa_前沿法评_{title}.md'
            else:
                target = f'Court_{category}_{title}.md'

        premap.append(f'NEW|{src}|{target_dir}{target}')

# Write pre-map
with open('wiki/.cache/weixinguan_premap.csv', 'w', encoding='utf-8') as f:
    f.write('状态|源文件|目标文件\n')
    for line in premap:
        f.write(line + '\n')

print(f'Pre-map generated: {len(premap)} entries')
summary_count = len([l for l in premap if 'wiki/summaries/' in l])
synthesis_count = len([l for l in premap if 'wiki/syntheses/' in l])
print(f'Summary entries: {summary_count}')
print(f'Synthesis entries: {synthesis_count}')
