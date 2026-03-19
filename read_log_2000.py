import sys

log_file = r'e:\Project_Personal\xianyu_project\xianyu-auto-reply-main\xianyu-auto-reply-main\logs\xianyu_2026-03-14.log'
output_file = r'e:\Project_Personal\xianyu_project\xianyu-auto-reply-main\xianyu-auto-reply-main\log_segment_2000.txt'
search_text = "2026-03-14 20:00"

with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

with open(output_file, 'w', encoding='utf-8') as out:
    found = False
    for i, line in enumerate(lines):
        if search_text in line:
            found = True
            # Print 100 lines before and 300 lines after
            start = max(0, i - 100)
            end = min(len(lines), i + 300)
            for j in range(start, end):
                out.write(lines[j])
            break

    if not found:
        # If specific minute not found, search for the hour
        search_text_hour = "2026-03-14 20:"
        for i, line in enumerate(lines):
            if search_text_hour in line:
                found = True
                start = max(0, i)
                end = min(len(lines), i + 400)
                for j in range(start, end):
                    out.write(lines[j])
                break
        if not found:
            out.write(f"Pattern '{search_text_hour}' not found.")
