import sys

file_path = r'e:\Project_Personal\xianyu_project\xianyu-auto-reply-main\xianyu-auto-reply-main\XianyuAutoAsync.py'

with open(file_path, 'rb') as f:
    content = f.read()

# Let's find line boundaries manually to be sure
lines = content.splitlines(keepends=True)

start = 1320
end = 1360

for i in range(start, min(end, len(lines))):
    line = lines[i]
    try:
        decoded = line.decode('utf-8').rstrip()
        print(f"LINE_{i+1:04}|{decoded}")
    except:
        print(f"LINE_{i+1:04}|MANGLED:{repr(line)}")
