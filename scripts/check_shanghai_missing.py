import os

source_dir = r"D:\AI agent\tkk-library\sources\微信公号资料\上海高院\上海高院-案例参考册-md"
wiki_dir = r"D:\AI agent\tkk-library\wiki\syntheses"

# Get source files
source_files = []
for f in os.listdir(source_dir):
    if f.endswith('.md'):
        source_files.append(f)

# Get wiki files (all RefCase_上海市高院_ files)
wiki_files = []
for f in os.listdir(wiki_dir):
    if f.startswith('RefCase_上海市高院_') and f.endswith('.md'):
        wiki_files.append(f)

# Extract titles from source files
def extract_source_title(filename):
    name = filename
    # Remove date prefix like [2022-02-24]
    if name.startswith('['):
        end = name.find(']')
        if end != -1:
            name = name[end+1:].strip()
    # Remove 丨案例参考册 suffix
    name = name.replace('丨案例参考册', '')
    name = name.rstrip('.md')
    return name

# Extract titles from wiki files
def extract_wiki_title(filename):
    name = filename.replace('RefCase_上海市高院_', '').rstrip('.md')
    return name

source_titles = set(extract_source_title(f) for f in source_files)
wiki_titles = set(extract_wiki_title(f) for f in wiki_files)

missing = source_titles - wiki_titles

print(f"Source files: {len(source_files)}")
print(f"Wiki files: {len(wiki_files)}")
print(f"Missing: {len(missing)}")
print()
print("Missing titles:")
for t in sorted(missing):
    print(f"  {t}")