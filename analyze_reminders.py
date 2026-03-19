import re
import json

log_file = r'e:\Project_Personal\xianyu_project\xianyu-auto-reply-main\xianyu-auto-reply-main\logs\xianyu_2026-03-14.log'
output_file = r'e:\Project_Personal\xianyu_project\xianyu-auto-reply-main\xianyu-auto-reply-main\reminders.txt'

with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Find all occurrences of redReminder
reminders = re.findall(r"'redReminder': '(.*?)'", content)
unique_reminders = sorted(list(set(reminders)))

with open(output_file, 'w', encoding='utf-8') as out:
    out.write("Unique redReminders found in log:\n")
    for r in unique_reminders:
        out.write(f"- {r}\n")

    # Also find all reminderTitle
    titles = re.findall(r"'reminderTitle': '(.*?)'", content)
    unique_titles = sorted(list(set(titles)))
    out.write("\nUnique reminderTitles found in log:\n")
    for t in unique_titles:
        out.write(f"- {t}\n")
        
    # Also find all reminderContent
    contents = re.findall(r"'reminderContent': '(.*?)'", content)
    unique_contents = sorted(list(set(contents)))
    out.write("\nUnique reminderContents found in log:\n")
    for c in unique_contents:
        out.write(f"- {c}\n")
