# -*- coding: utf-8 -*-
import os, re

clippings = sorted(os.listdir(u'D:/AI agent/tkk-library/Clippings/'))
summaries = sorted(os.listdir(u'D:/AI agent/tkk-library/wiki/summaries/'))

# Normalize clipping filename to match summary filename
def normalize(fname):
    # Remove trailing ".md"
    name = fname[:-3]
    # Remove " - 业务指引 - 业务研究大厅 - 东方律师网"
    name = name.replace(u' - 业务指引 - 业务研究大厅 - 东方律师网', u'')
    # Remove surrounding spaces and parens
    name = name.strip()
    # Replace fullwidth parens with normal
    name = name.replace(u'\uff08', u'（').replace(u'\uff09', u'）')
    # Extract year and title
    m = re.match(r'^(.+?)（(\d{4})）', name)
    if m:
        base, year = m.groups()
        base = base.strip()
        return u'%s%s' % (year, base)
    return name

# Normalize clipping names
clip_norm = {normalize(f): f for f in clippings}

# Normalize summary names
sum_norm = {s[:-3]: s for s in summaries}

new_files = []
for key, fname in sorted(clip_norm.items()):
    # Check if any summary matches
    found = False
    for sk in sum_norm:
        # Direct match
        if key == sk:
            found = True
            break
        # Check if the clipping key is contained in summary key or vice versa
        if key in sk or sk in key:
            found = True
            break
    if not found:
        new_files.append((key, fname))

print(u'Truly new files: %d' % len(new_files))
for key, fname in new_files:
    print(u'  [%s] %s' % (key, fname))
