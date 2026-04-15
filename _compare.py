# -*- coding: utf-8 -*-
import os, re

clippings = sorted(os.listdir(u'D:/AI agent/tkk-library/Clippings'))
summaries = sorted(os.listdir(u'D:/AI agent/tkk-library/wiki/summaries'))

# Build known title set from summaries
known_titles = {}
for s in summaries:
    # 20230206_律师从事调解业务操作指引2021.md
    m = re.match(r'^\d{8}_(.+?)(\d{4})\.md$', s)
    if m:
        title_part = m.group(1)  # e.g. 律师从事调解业务操作指引
        year = m.group(2)        # e.g. 2021
        # key = title without year suffix
        known_titles[title_part] = (year, s)

print('Summary count: %d' % len(summaries))
print('Clipping count: %d' % len(clippings))
print()

# Normalize clipping title
def clip_title(c):
    # Remove suffix
    c = c.replace(u' - 业务指引 - 业务研究大厅 - 东方律师网', u'')
    c = c.strip()
    c = c.replace(u'\uff08', u'（').replace(u'\uff09', u'）')
    # Extract title and year: "律师从事调解业务操作指引（2021）" -> title + year
    m = re.match(r'^(.+?)（(\d{4})）', c)
    if m:
        return m.group(1).strip(), m.group(2)
    return c.strip(), u''

new_files = []
for c in clippings:
    title, year = clip_title(c)
    # Check if this title is in known_titles
    if title not in known_titles:
        new_files.append((title, year, c))

print('New (not in summaries): %d' % len(new_files))
for t, y, f in new_files:
    print(u'  [%s] %s' % (y, f))
