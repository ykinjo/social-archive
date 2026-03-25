import json
import glob
import re
from pathlib import Path

posts = []

def clean_html(html):

    html = re.sub("<script.*?</script>", "", html, flags=re.S)
    html = re.sub("<style.*?</style>", "", html, flags=re.S)
    html = re.sub("<.*?>", "", html)

    return html.strip()


# ----------------
# mixi (markdown)
# ----------------
for f in glob.glob("mixi/diary_md/*.md"):

    path = Path(f)
    name = path.stem

    date = name.split("_")[0]

    with open(f) as fp:
        text = fp.read()

    lines = text.splitlines()

    title = ""
    for l in lines:
        if l.startswith("#"):
            title = l.replace("#","").strip()
            break

    if not title:
        title = lines[0]

    # ★ mixi重複除去
    title = re.sub(r'^\s*\[mixi\]\s*', '', title, flags=re.I)

    posts.append({
        "date": date,
        "title": title,
        "text": text,
        "url": f,        # ← mdそのまま
        "source": "mixi"
    })


# ----------------
# twitter (JSON)
# ----------------

with open("twitter/output/all_posts.json") as fp:
    tweets = json.load(fp)

for t in tweets:

    text = t.get("text","").strip()
    if not text:
        continue

    # 日付取得（複数パターン対応）
    date = ""

    if "created_at" in t and t["created_at"]:
        date = t["created_at"][:10]

    elif "date" in t and t["date"]:
        date = t["date"][:10]

    elif "timestamp" in t and t["timestamp"]:
        date = t["timestamp"][:10]

    # フォールバック（保険）
    if not date:
        date = "1970-01-01"

    year = date[:4]

    url = f"twitter/output/{year}/{date}.html"

    posts.append({
    "date": date,
    "title": text[:120],
    "text": text,
    "url": url,
    "source": "twitter"
    })


# ----------------
# livedoor blog
# ----------------

for f in glob.glob("blog.livedoor.jp/html/**/*.html", recursive=True):

    with open(f) as fp:
        html = fp.read()

    # タイトル取得
    m = re.search("<title>(.*?)</title>", html)

    if not m:
        continue

    title = m.group(1)

    # ブログ名削除
    title = re.sub(r".*?:", "", title)

    # livedoor表記削除
    title = re.sub(r" - livedoor Blog.*", "", title)

    # --------
    # 日付取得
    # --------

    date = ""

    # パターン1
    m = re.search(r'(\d{4}-\d{2}-\d{2})T', html)
    if m:
        date = m.group(1)

    # パターン2
    if not date:
        m = re.search(r'(\d{4})年(\d{2})月(\d{2})日', html)
        if m:
            date = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"

    posts.append({
        "date": date,
        "title": title.strip(),
        "text": clean_html(html)[:2000],
        "url": f,
        "source": "blog"
    })

# ソート
posts.sort(key=lambda x: x["date"])

with open("search.json","w") as f:
    json.dump(posts, f, ensure_ascii=False)

print("posts:", len(posts))