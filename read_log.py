import sys

log_file = r'e:\Project_Personal\xianyu_project\xianyu-auto-reply-main\xianyu-auto-reply-main\logs\xianyu_2026-03-14.log'
output_file = r'e:\Project_Personal\xianyu_project\xianyu-auto-reply-main\xianyu-auto-reply-main\log_segment_utf8.txt'
start_pattern = "2026-03-14 12:52"

with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

with open(output_file, 'w', encoding='utf-8') as out:
    found = False
    for i, line in enumerate(lines):
        if start_pattern in line:
            found = True
            start = max(0, i - 10)
            end = min(len(lines), i + 100)
            for j in range(start, end):
                out.write(lines[j])
            break

    if not found:
        out.write(f"Pattern '{start_pattern}' not found.")
