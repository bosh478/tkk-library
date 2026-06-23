# -*- coding: utf-8 -*-
import os, sys

sys.stdout.reconfigure(encoding='utf-8')

wiki_dir = 'wiki/syntheses'
wiki_files = set()
for f in os.listdir(wiki_dir):
    if f.startswith('Court_公报案例_') and f.endswith('.md'):
        case_num = f.replace('Court_公报案例_', '').replace('.md', '')
        trans = str.maketrans('１２３４５６７８９０', '1234567890')
        normalized = case_num.translate(trans).replace('（', '(').replace('）', ')')
        wiki_files.add(normalized)

subdir = sys.argv[1] if len(sys.argv) > 1 else '刑事'
src_dir = f'sources/2-案例库/公报案例/{subdir}'
unmatched = []
for f in sorted(os.listdir(src_dir)):
    if not f.endswith('.md'):
        continue
    case_num = f.replace('公报案例 ', '').replace('.md', '')
    trans = str.maketrans('１２３４５６７８９０', '1234567890')
    normalized = case_num.translate(trans).replace('（', '(').replace('）', ')')
    if normalized not in wiki_files:
        unmatched.append(f)

print(f'{subdir}: {len(unmatched)} unmatched files')
for f in unmatched:
    print(f)
