import sys

log_file = r'e:\Project_Personal\xianyu_project\xianyu-auto-reply-main\xianyu-auto-reply-main\logs\xianyu_2026-03-14.log'
output_file = r'e:\Project_Personal\xianyu_project\xianyu-auto-reply-main\xianyu-auto-reply-main\log_segment_utf8_part3.txt'
search_text = "检测到Session过期，停止自动确认发货"

with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

with open(output_file, 'w', encoding='utf-8') as out:
    found = False
    for i, line in enumerate(lines):
        if search_text in line:
            found = True
            # Print next 100 lines
            start = i
            end = min(len(lines), i + 200)
            for j in range(start, end):
                out.write(lines[j])
            # Only process first occurrence for now
            break

    if not found:
        out.write(f"Pattern '{search_text}' not found.")
