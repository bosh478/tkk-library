# -*- coding: utf-8 -*-
import os

# Read clipping filenames directly from filesystem
clippings_dir = u'D:/AI agent/tkk-library/Clippings'
clippings = sorted(os.listdir(clippings_dir))

# Read summary filenames
summaries_dir = u'D:/AI agent/tkk-library/wiki/summaries'
summaries_raw = sorted(os.listdir(summaries_dir))
# summary keys = filename without .md
summary_keys = set(s[:-3] for s in summaries_raw)

# Print all summaries for debugging
print('Summary count:', len(summary_keys))
print()

# The key insight: clipping filenames have different format than summaries
# Clipping: "律师代理政府信息公开法律业务操作指引（2021） - 业务指引..."
# Summary:  "20210624_律师代理政府信息公开法律业务操作指引2021.md"

# We need to match by core title. Extract core title from summary
def summary_core_title(s):
    # Remove date prefix and year suffix
    import re
    m = re.match(r'^\d{8}_(.+?)(\d{4})$', s)
    if m:
        return m.group(1)
    return s

summary_cores = {summary_core_title(s): s for s in summary_keys}

# Extract core title from clipping
def clipping_core_title(c):
    import re
    # Remove the "- 业务指引 - 业务研究大厅 - 东方律师网" suffix
    c = c.replace(' - 业务指引 - 业务研究大厅 - 东方律师网', '').strip()
    # Handle fullwidth parens
    c = c.replace('\uff08', '（').replace('\uff09', '）')
    # Extract year from （YYYY）
    m = re.match(r'^(.+?)（(\d{4})）', c)
    if m:
        base, year = m.groups()
        return base.strip() + year
    # No year found
    return c.strip()

new_in_clippings = []
for c in clippings:
    core = clipping_core_title(c)
    if core not in summary_cores:
        new_in_clippings.append(c)

print('New files in Clippings (not yet in summaries):', len(new_in_clippings))
for f in new_in_clippings:
    print(' ', f)
