# -*- coding: utf-8 -*-
import os, re, json
sys_path = 'D:/AI agent/tkk-library'
src_dir = os.path.join(sys_path, 'sources/2-案例库/最高检-指导性案例')

# Placeholder case numbers (from previous check)
placeholders = [42, 43, 44, 45, 46, 47, 48, 51, 60, 61, 67, 70, 71, 72, 74, 75, 95, 97, 100, 101, 102, 103, 104, 106, 107, 108, 110, 127, 129, 133, 137, 138, 140, 154, 155, 157, 167, 168, 169, 170, 171, 172, 173, 174, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 187, 189, 190, 192, 193, 194, 195, 196, 197, 198, 199, 201, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237]

# Build mapping: source file -> list of case numbers it contains
file_cases = {}
for fname in sorted(os.listdir(src_dir)):
    if not fname.endswith('.md'):
        continue
    fpath = os.path.join(src_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Find all 检例第X号 patterns
    case_nums = [int(m) for m in re.findall(r'检例第(\d+)号', content)]
    if case_nums:
        file_cases[fname] = sorted(set(case_nums))

# Map placeholder case numbers to source files
case_to_file = {}
for fname, cases in file_cases.items():
    for c in cases:
        case_to_file[c] = fname

# Group placeholder cases by source file
file_to_placeholders = {}
for c in placeholders:
    if c in case_to_file:
        fname = case_to_file[c]
        if fname not in file_to_placeholders:
            file_to_placeholders[fname] = []
        file_to_placeholders[fname].append(c)
    else:
        print(f"WARNING: Case {c} not found in any source file!")

print(f"\nSource files containing placeholder cases:")
for fname in sorted(file_to_placeholders.keys()):
    cases = file_to_placeholders[fname]
    print(f"  {fname}: {len(cases)} cases -> {cases}")
print(f"\nTotal files to process: {len(file_to_placeholders)}")
print(f"Total cases to process: {sum(len(v) for v in file_to_placeholders.values())}")
