# -*- coding: utf-8 -*-
import os, re

CLIPPINGS = 'D:/AI agent/tkk-library/Clippings'
SUMMARIES = 'D:/AI agent/tkk-library/wiki/summaries'

clips = sorted(os.listdir(CLIPPINGS))
sums = sorted(os.listdir(SUMMARIES))

# Get normalized title from summary frontmatter
def sum_norm(s):
    with open(os.path.join(SUMMARIES, s), 'r', encoding='utf-8') as f:
        c = f.read()
    if c.startswith('---'):
        parts = c.split('---', 2)
        for line in parts[1].split('\n'):
            if line.startswith('title:'):
                t = line.split(':', 1)[1].strip().strip('"').strip("'").strip()
                # Remove trailing year in parentheses or bare year at end
                t = re.sub(r'（[^）]*）\s*$', '', t).strip()
                t = re.sub(r'\d{4}\s*$', '', t).strip()
                return t
    return None

# Get normalized title from clipping filename
def clip_norm(c):
    name = c.replace(' - 业务指引 - 业务研究大厅 - 东方律师网', '').strip()
    name = name.replace('\uff08', '（').replace('\uff09', '）')
    # Remove parenthetical years
    name = re.sub(r'（[^）]*）', '', name).strip()
    # Remove bare year at end
    name = re.sub(r'\d{4}$', '', name).strip()
    return name

# Build summary normalized titles
sum_norms = set()
for s in sums:
    n = sum_norm(s)
    if n:
        sum_norms.add(n)

deleted = []
kept = []
for c in clips:
    cn = clip_norm(c)
    matched = False
    for sn in sum_norms:
        if cn == sn or cn in sn or sn in cn:
            # Delete this clipping
            fp = os.path.join(CLIPPINGS, c)
            os.remove(fp)
            deleted.append(c)
            matched = True
            break
    if not matched:
        kept.append(c)

with open('D:/AI agent/tkk-library/_clip_delete_result.txt', 'w', encoding='utf-8') as f:
    f.write('Deleted: %d\n' % len(deleted))
    f.write('Kept: %d\n\n')
    for c in deleted:
        f.write('DEL: %s\n' % c)
    f.write('\n')
    for c in kept:
        f.write('KEEP: %s\n' % c)
print('Done. Deleted: %d, Kept: %d' % (len(deleted), len(kept)))
