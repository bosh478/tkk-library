# -*- coding: utf-8 -*-
# Compare Clippings vs Summaries by extracting comparable title from each
import os, re

CLIPPINGS = u'D:/AI agent/tkk-library/Clippings'
SUMMARIES = u'D:/AI agent/tkk-library/wiki/summaries'

clippings = sorted(os.listdir(CLIPPINGS))
summaries_list = sorted(os.listdir(SUMMARIES))
summary_keys = set(s[:-3] for s in summaries_list)

def normalize_title(s):
    """Remove date prefix, year suffix, and parenthetical year markers."""
    # Summary: 20240327_律师办理物流快递外卖企业合规业务指引_2024
    # Clip: 律师从事国际贸易合同（出口）业务操作指引（2024） - 业务指引...
    s = s.replace(u'_', u'')
    # Remove digits from start
    s = re.sub(r'^\d+', u'', s)
    # Remove year at end
    s = re.sub(r'\d{4}$', u'', s)
    # Remove parenthetical years like （出口）
    s = re.sub(u'（[^）]+）', u'', s)
    # Remove common suffix
    s = s.replace(u'业务操作指引', u'').replace(u'业务指引', u'').replace(u'操作指引', u'')
    return s.strip()

# Build a set of normalized summary titles
norm_sums = set(normalize_title(s) for s in summary_keys)

# Check each clipping
new_clips = []
for c in clippings:
    # Skip mp.weixin duplicates
    if c.startswith(u'广东高院'):
        continue
    norm = normalize_title(c)
    if norm not in norm_sums:
        new_clips.append(c)

print(u'New clips: %d' % len(new_clips))
for c in new_clips:
    print(norm_sums)
    print(u'  %s' % c)
