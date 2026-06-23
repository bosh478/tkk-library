# -*- coding: utf-8 -*-
"""Fix GuideCase_ pages' related field based on content keywords."""
import os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

WIKI_DIR = 'D:/AI agent/tkk-library/wiki/syntheses'

# Keyword -> concept mapping
KEYWORD_MAP = [
    ('借款合同', '借款合同纠纷'),
    ('借贷', '借款合同纠纷'),
    ('买卖合同', '买卖合同纠纷'),
    ('买卖', '买卖合同纠纷'),
    ('租赁合同', '租赁合同纠纷'),
    ('租赁', '租赁合同纠纷'),
    ('不正当竞争', '不正当竞争'),
    ('商标', '商标权纠纷'),
    ('专利', '专利权纠纷'),
    ('著作权', '著作权纠纷'),
    ('版权', '著作权纠纷'),
    ('侵权', '侵权责任纠纷'),
    ('建设工程', '建设工程合同纠纷'),
    ('工程', '建设工程合同纠纷'),
    ('房屋', '房屋买卖合同纠纷'),
    ('房产', '房屋买卖合同纠纷'),
    ('保险', '保险合同纠纷'),
    ('劳动', '劳动争议'),
    ('工伤', '劳动争议'),
    ('股权', '公司股权纠纷'),
    ('股东', '公司股权纠纷'),
    ('继承', '继承纠纷'),
    ('遗嘱', '继承纠纷'),
    ('离婚', '婚姻家庭纠纷'),
    ('婚姻', '婚姻家庭纠纷'),
    ('担保', '担保纠纷'),
    ('抵押', '担保纠纷'),
    ('合伙', '合伙纠纷'),
    ('运输', '运输合同纠纷'),
    ('技术合同', '技术合同纠纷'),
    ('技术秘密', '技术合同纠纷'),
    ('海事', '海事纠纷'),
    ('海商', '海事纠纷'),
    ('票据', '票据纠纷'),
    ('证券', '证券纠纷'),
    ('期货', '期货纠纷'),
    ('破产', '破产纠纷'),
    ('清算', '公司清算'),
    ('国有土地', '土地使用权纠纷'),
    ('土地', '土地使用权纠纷'),
    ('拆迁', '拆迁补偿纠纷'),
    ('征收', '征收补偿纠纷'),
    ('环境', '环境污染责任纠纷'),
    ('污染', '环境污染责任纠纷'),
    ('产品责任', '产品责任纠纷'),
    ('医疗', '医疗损害责任纠纷'),
    ('名誉', '名誉权纠纷'),
    ('肖像', '肖像权纠纷'),
    ('人格', '人格权纠纷'),
    ('物权', '物权确认纠纷'),
    ('所有权', '物权确认纠纷'),
    ('使用权', '物权确认纠纷'),
]

def extract_related(content, source_path):
    """Extract related concepts from file content."""
    body = content.split('---')[-1] if '---' in content else content

    # Find matching keywords (limit to top 3)
    matched = []
    for keyword, concept in KEYWORD_MAP:
        if keyword in body and concept not in matched:
            matched.append(concept)
        if len(matched) >= 3:
            break

    # If no keyword matched, use broad category from source path
    if not matched:
        if '刑事' in source_path:
            matched = ['刑事案件']
        elif '行政' in source_path:
            matched = ['行政案件']
        elif '执行' in source_path:
            matched = ['执行案件']
        elif '民事' in source_path:
            matched = ['民事案件']

    return matched

def update_file(filepath):
    """Update the related field in a GuideCase_ file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Only process files with template related field
    if '[[民间借贷], [合同纠纷]]' not in content and 'related: [[民间借贷]' not in content:
        return False

    # Extract source path
    source_m = re.search(r'source:\s*"([^"]+)"', content)
    source_path = source_m.group(1) if source_m else ''

    # Extract related concepts
    related = extract_related(content, source_path)
    if not related:
        return False

    # Build related field
    if len(related) == 1:
        related_str = f'related: [[concept_{related[0]}]]'
    else:
        related_lines = '\n'.join(f'  - [[concept_{r}]]' for r in related)
        related_str = f'related:\n{related_lines}'

    # Replace old related field
    # Match: related: [[民间借贷], [合同纠纷]] or related:\n  - [[民间借贷], [合同纠纷]]
    old_patterns = [
        r'related:\s*\[\[民间借贷\],\s*\[合同纠纷\]\]',
        r'related:\n\s*-\s*\[\[民间借贷\],\s*\[合同纠纷\]\]',
    ]
    new_content = content
    for pattern in old_patterns:
        new_content, count = re.subn(pattern, related_str, new_content)
        if count > 0:
            break

    if new_content == content:
        return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

# Main
updated = 0
skipped = 0
errors = 0
for fname in sorted(os.listdir(WIKI_DIR)):
    if not (fname.startswith('GuideCase_') and fname.endswith('.md')):
        continue
    filepath = os.path.join(WIKI_DIR, fname)
    try:
        if update_file(filepath):
            updated += 1
        else:
            skipped += 1
    except Exception as e:
        errors += 1
        print(f'ERROR: {fname}: {e}')

print(f'\nDone: {updated} updated, {skipped} skipped, {errors} errors')
