import re
from pathlib import Path

src = Path("diary_md")

for f in src.glob("*.md"):

    text = f.read_text(encoding="utf-8")

    # URL途中改行を除去
    text = re.sub(r'http://\s+', 'http://', text)
    text = re.sub(r'https://\s+', 'https://', text)

    text = re.sub(r'http://([^\s]+)\s+([^\s]+)', r'http://\1\2', text)
    text = re.sub(r'https://([^\s]+)\s+([^\s]+)', r'https://\1\2', text)

    # URL内改行削除
    text = re.sub(r'(https?://[^\s]+)\n([^\s]+)', r'\1\2', text)

    f.write_text(text, encoding="utf-8")

print("URL repair finished")
