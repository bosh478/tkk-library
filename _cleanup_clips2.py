# -*- coding: utf-8 -*-
import os, re

CLIPPINGS = 'D:/AI agent/tkk-library/Clippings'
SUMMARIES = 'D:/AI agent/tkk-library/wiki/summaries'

clips = sorted(os.listdir(CLIPPINGS))
sums = sorted(os.listdir(SUMMARIES))

def get_title(fp):
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            c = f.read()
        if c.startswith('---'):
            parts = c.split('---', 2)
            if len(parts) >= 3:
                for line in parts[1].split('\n'):
                    if line.startswith('title:'):
                        return line.split(':', 1)[1].strip().strip('"').strip("'")
    except:
        pass
    return None

sum_titles = {}
for s in sums:
    t = get_title(os.path.join(SUMMARIES, s))
    if t:
        t = t.strip()  # Strip trailing spaces (e.g. "指引 （2012）" -> "指引 （2012）")
        sum_titles[t] = s

def clip_title(c):
    name = c.replace(' - 业务指引 - 业务研究大厅 - 东方律师网', '').strip()
    name = name.replace('\uff08', '（').replace('\uff09', '）')
    return name.strip()

to_delete = []
to_keep = []

for c in clips:
    ct = clip_title(c)
    if ct in sum_titles:
        to_delete.append(c)
    else:
        to_keep.append(c)

# Write results to file (not terminal, to avoid encoding issues)
with open('D:/AI agent/tkk-library/_cleanup_result.txt', 'w', encoding='utf-8') as f:
    f.write('Clippings total: %d\n' % len(clips))
    f.write('Summaries total: %d\n' % len(sums))
    f.write('Unique summary titles: %d\n' % len(sum_titles))
    f.write('To DELETE: %d\n' % len(to_delete))
    f.write('To KEEP: %d\n' % len(to_keep))
    f.write('\n=== TO DELETE ===\n')
    for c in sorted(to_delete):
        f.write(c + '\n')
    f.write('\n=== TO KEEP ===\n')
    for c in sorted(to_keep):
        f.write(c + '\n')
