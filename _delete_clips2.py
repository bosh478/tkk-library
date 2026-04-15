# -*- coding: utf-8 -*-
import os, re

CLIPPINGS = 'D:/AI agent/tkk-library/Clippings'
SUMMARIES = 'D:/AI agent/tkk-library/wiki/summaries'

clips = sorted(os.listdir(CLIPPINGS))
sums = sorted(os.listdir(SUMMARIES))

# Get title from summary frontmatter
def get_title(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()
    if c.startswith('---'):
        parts = c.split('---', 2)
        for line in parts[1].split('\n'):
            if line.startswith('title:'):
                return line.split(':', 1)[1].strip().strip('"').strip("'").strip()
    return None

# Normalize clipping: remove suffix, convert fullwidth parens, remove "（试行）" and extra spaces
def clip_norm(c):
    name = c.replace(' - 业务指引 - 业务研究大厅 - 东方律师网', '').strip()
    name = name.replace('\uff08', '（').replace('\uff09', '）')
    # Remove space before （
    name = re.sub(r'\s+（', '（', name)
    # Extract year in parentheses
    yr_m = re.search(r'（(\d{4})）', name)
    yr = yr_m.group(1) if yr_m else ''
    # Remove all parenthetical content
    name = re.sub(r'（[^）]*）', '', name).strip()
    if yr:
        name = name + yr
    return name

# Normalize summary title: keep year in parentheses as-is
def sum_norm(title):
    # Summary title: has year in parentheses, maybe （试行） too
    t = title.strip()
    # Remove space before （
    t = re.sub(r'\s+（', '（', t)
    # Extract year in parentheses (e.g. 2025)
    yr_m = re.search(r'（(\d{4})）', t)
    yr = yr_m.group(1) if yr_m else ''
    # Remove all parenthetical content
    t = re.sub(r'（[^）]*）', '', t).strip()
    # Add year back at end
    if yr:
        t = t + yr
    return t

# Build summary lookup: normalized_title -> filename
sum_lookup = {}
for s in sums:
    t = get_title(os.path.join(SUMMARIES, s))
    if t:
        n = sum_norm(t)
        sum_lookup[n] = s

deleted = []
kept = []

for c in clips:
    cn = clip_norm(c)
    if cn in sum_lookup:
        fp = os.path.join(CLIPPINGS, c)
        os.remove(fp)
        deleted.append(c)
    else:
        kept.append(c)

with open('D:/AI agent/tkk-library/_clip_result2.txt', 'w', encoding='utf-8') as f:
    f.write('Deleted: %d\n' % len(deleted))
    f.write('Kept: %d\n\n')
    for c in deleted:
        f.write('DEL: %s\n' % c)
    f.write('\n=== KEEP ===\n')
    for c in kept:
        f.write('KEEP: %s\n' % c)

print('Done. Deleted: %d, Kept: %d' % (len(deleted), len(kept)))
