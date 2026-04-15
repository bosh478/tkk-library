# -*- coding: utf-8 -*-
# Build precise mapping: clipping filename -> has matching summary
import os, re

CLIPPINGS = 'D:/AI agent/tkk-library/Clippings'
SUMMARIES = 'D:/AI agent/tkk-library/wiki/summaries'

clips = sorted(os.listdir(CLIPPINGS))
sums = sorted(os.listdir(SUMMARIES))

# Read all summary frontmatter titles
def get_frontmatter_title(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                for line in parts[1].split('\n'):
                    if line.startswith('title:'):
                        return line.split(':', 1)[1].strip().strip('"').strip("'")
    except:
        pass
    return None

# Build set of frontmatter titles from summaries
sum_titles = set()
sum_dict = {}
for s in sums:
    fp = os.path.join(SUMMARIES, s)
    t = get_frontmatter_title(fp)
    if t:
        sum_titles.add(t)
        sum_dict[t] = s

# Normalize clipping filename to extract the title
def clip_title(c):
    # Remove the "- 业务指引 - 业务研究大厅 - 东方律师网" suffix
    name = c.replace(' - 业务指引 - 业务研究大厅 - 东方律师网', '').strip()
    name = name.replace('\uff08', '（').replace('\uff09', '）')
    return name

to_delete = []
to_keep = []

for c in clips:
    ct = clip_title(c)
    if ct in sum_titles:
        to_delete.append(c)
    else:
        to_keep.append(c)

print('Clippings total: %d' % len(clips))
print('Summaries total: %d' % len(sums))
print('Unique summary titles: %d' % len(sum_titles))
print()
print('To DELETE (matched): %d' % len(to_delete))
print('To KEEP (new/unmatched): %d' % len(to_keep))
print()
print('=== KEEP (new/unmatched files) ===')
for c in sorted(to_keep):
    print('  %s' % c)
