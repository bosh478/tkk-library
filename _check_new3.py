# -*- coding: utf-8 -*-
import os, re

clippings_dir = 'D:/AI agent/tkk-library/Clippings'
summaries_dir = 'D:/AI agent/tkk-library/wiki/summaries'

clippings = sorted(os.listdir(clippings_dir))
summaries_raw = sorted(os.listdir(summaries_dir))
summary_keys = set(s[:-3] for s in summaries_raw)

# Get clipping keys - extract title+year format
def clip_key(c):
    c = c.replace(' - 业务指引 - 业务研究大厅 - 东方律师网', '').strip()
    c = c.replace('\uff08', '（').replace('\uff09', '）')
    m = re.match(r'^(.+?)（(\d{4})）', c)
    if m:
        base, year = m.groups()
        return base.strip() + year
    return c.strip()

# Get title from summary (strip date prefix and year suffix)
def sum_key(s):
    m = re.match(r'^\d{8}_(.+?)(\d{4})$', s)
    if m:
        return m.group(1)
    return s

# Build a dict: sum_title -> sum_key
sum_titles = {}
for s in summary_keys:
    t = sum_key(s)
    sum_titles[t] = s

clip_keys = {clip_key(c): c for c in clippings}

new_files = []
for key, fname in sorted(clip_keys.items()):
    # Try to find match by checking if summary title is substring of clip key
    found = False
    for sum_t, sum_k in sum_titles.items():
        if sum_t in key or key in sum_t:
            found = True
            break
    if not found:
        new_files.append((key, fname))

print('New files: %d' % len(new_files))
for k, f in new_files:
    print('  [%s]' % k)
    print('    %s' % f)
