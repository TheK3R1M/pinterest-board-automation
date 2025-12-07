import codecs

with codecs.open('c:\\Users\\kerim\\Desktop\\pinterest-board-automation\\pinterest_saver.py', 'r', 'utf-8') as f:
    lines = f.readlines()

# Find the line with "self.logger.log_info(f"🔍 Searching for board"
search_start = -1
search_end = -1

for i, line in enumerate(lines):
    if 'Searching for board' in line:
        search_start = i
    if search_start != -1 and 'Board selection error' in line:
        search_end = i
        break

if search_start == -1:
    print("Could not find Searching for board line")
else:
    print(f"Found search block: lines {search_start+1} to around {search_end+1 if search_end != -1 else '?'}")
    print("Sample lines:")
    for i in range(search_start, min(search_start+15, len(lines))):
        print(f"{i+1}: {lines[i][:100].rstrip()}")
