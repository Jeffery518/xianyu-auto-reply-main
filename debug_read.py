import sys

file_path = r'e:\Project_Personal\xianyu_project\xianyu-auto-reply-main\xianyu-auto-reply-main\XianyuAutoAsync.py'

try:
    with open(file_path, 'rb') as f:
        lines = f.readlines()

    start = 1300
    end = 1500

    for i in range(start, min(end, len(lines))):
        line = lines[i]
        try:
            print(f"{i+1:4}: {line.decode('utf-8').rstrip()}")
        except Exception:
            print(f"{i+1:4}: [BINARY/MANGLED] {repr(line)}")
except Exception as e:
    print(f"ERROR: {e}")
