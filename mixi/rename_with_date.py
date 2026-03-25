import os
import re
from pathlib import Path

src = Path("diary_md")

date_re = re.compile(r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})')

for f in src.glob("*.md"):
    text = f.read_text(encoding="utf-8")

    m = date_re.search(text)
    if not m:
        continue

    y, mth, d = m.groups()
    newname = f"{y}-{int(mth):02d}-{int(d):02d}_{f.name}"

    newpath = f.with_name(newname)

    if not newpath.exists():
        f.rename(newpath)
        print("rename:", newname)
