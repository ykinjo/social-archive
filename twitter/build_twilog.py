import json
import shutil
import calendar
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# ----------------------------
# 初期化
# ----------------------------
shutil.rmtree("output", ignore_errors=True)

data = []

for file in sorted(Path("input").glob("tweets*.js")):
    raw = file.read_text(encoding="utf-8")
    part = json.loads(raw.split("=", 1)[1])
    data.extend(part)

print("tweets loaded:", len(data))

posts_by_day = defaultdict(list)
all_posts = []

from datetime import timezone, timedelta
JST = timezone(timedelta(hours=9))

for i, item in enumerate(data):
    t = item["tweet"]
    dt = datetime.strptime(
        t["created_at"],
        "%a %b %d %H:%M:%S %z %Y"
    ).astimezone(JST)

    day = dt.strftime("%Y-%m-%d")
    year = dt.strftime("%Y")

    post_data = {
        "date": day,
        "time": dt.strftime("%H:%M"),
        "text": t["full_text"]
    }

    posts_by_day[day].append({
        "time": post_data["time"],
        "text": post_data["text"],
        "media": t.get("extended_entities", {}).get("media", [])
    })

    all_posts.append(post_data)

out = Path("output")
out.mkdir(exist_ok=True)

# ----------------------------
# twilog風CSS
# ----------------------------
CSS = """
<style>
body {
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    max-width: 800px;
    margin: 40px auto;
    background: #f5f8fa;
    line-height: 1.6;
}
h1 { border-bottom: 2px solid #ddd; padding-bottom: 10px; }
p {
    background: white;
    padding: 10px 14px;
    border-radius: 8px;
    margin: 8px 0;
}
strong { color: #657786; font-size: 0.9em; }
table {
    background: white;
    border-collapse: collapse;
    margin-top: 20px;
}
th, td { padding: 6px 10px; text-align: center; }
a { text-decoration: none; color: #1da1f2; }
a:hover { text-decoration: underline; }
img { margin-top: 6px; border-radius: 8px; }
input {
    width: 100%;
    padding: 10px;
    margin: 15px 0;
    border-radius: 6px;
    border: 1px solid #ccc;
}
#results p { margin: 6px 0; }
</style>
"""

# ----------------------------
# 全投稿JSON出力
# ----------------------------
with (out / "all_posts.json").open("w", encoding="utf-8") as fp:
    json.dump(all_posts, fp, ensure_ascii=False)

# ----------------------------
# 日別ページ生成
# ----------------------------
for day in sorted(posts_by_day.keys()):
    year = day[:4]
    ydir = out / year
    ydir.mkdir(parents=True, exist_ok=True)

    f = ydir / f"{day}.html"

    with f.open("w", encoding="utf-8") as fp:
        fp.write("""<!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    """)
        fp.write(CSS)
        fp.write("</head><body>\n")

        fp.write('<a href="../index.html">← Index</a>')

        for post in sorted(posts_by_day[day], key=lambda x: x["time"]):
            fp.write(
                f"<p><strong>{post['time']}</strong> {post['text']}</p>\n"
            )

            for media in post["media"]:
                url = media["media_url_https"]
                filename = url.split("/")[-1]
                local_path = Path("data/tweets_media") / filename

                if local_path.exists():
                    img_src = f"../../data/tweets_media/{filename}"
                else:
                    img_src = url

                fp.write(f'<img src="{img_src}" style="max-width:400px;"><br>')

            fp.write("</body></html>")


# ----------------------------
# 年→月構造
# ----------------------------
months_by_year = defaultdict(set)
for day in posts_by_day:
    months_by_year[day[:4]].add(day[:7])

# ----------------------------
# 年・月ごとの投稿数集計
# ----------------------------
year_counts = {}
month_counts = {}

for day, posts in posts_by_day.items():
    year = day[:4]
    month = day[:7]

    year_counts[year] = year_counts.get(year, 0) + len(posts)
    month_counts[month] = month_counts.get(month, 0) + len(posts)

for year in sorted(months_by_year):
    for month in sorted(months_by_year[year]):

        ydir = out / year
        month_path = ydir / f"{month}.html"

        y, m = map(int, month.split("-"))
        cal = calendar.monthcalendar(y, m)

        with month_path.open("w", encoding="utf-8") as fp:
            fp.write("""<!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        """)
            fp.write(CSS)
            fp.write("</head><body>\n")
            fp.write(f"<h1>{month}</h1>\n")
            fp.write(f"<p>投稿数: {month_counts.get(month, 0)}件</p>\n")
            fp.write('<a href="../index.html">← Index</a>')
            fp.write('<table border="1">')

            fp.write("<tr>")
            for d in ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]:
                fp.write(f"<th>{d}</th>")
            fp.write("</tr>")

            for week in cal:
                fp.write("<tr>")
                for day_num in week:
                    if day_num == 0:
                        fp.write("<td></td>")
                    else:
                        day_str = f"{year}-{m:02d}-{day_num:02d}"
                        if day_str in posts_by_day:
                            fp.write(
                                f'<td><a href="{day_str}.html">{day_num}</a></td>'
                            )
                        else:
                            fp.write(f"<td>{day_num}</td>")
                fp.write("</tr>")

            fp.write("</table>")
            fp.write("</body></html>")


# ----------------------------
# Index + 検索（完成版）
# ----------------------------
index_path = out / "index.html"

with index_path.open("w", encoding="utf-8") as fp:

    fp.write("""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Twitter Archive</title>
""")

    fp.write(CSS)

    # 投稿データを直接埋め込み
    fp.write("<script>\n")
    fp.write("const ALL_POSTS = ")
    json.dump(all_posts, fp, ensure_ascii=False)
    fp.write(";\n")

    fp.write(r"""
function searchAll() {
    const raw = document.getElementById("search").value.toLowerCase();
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    if (!raw.trim()) return;

    const keywords = raw.split(/\s+/);

    ALL_POSTS.forEach(p => {
        const text = p.text.toLowerCase();
        const match = keywords.every(k => text.includes(k));

        if (match) {
            const el = document.createElement("p");
            el.innerHTML =
                `<a href="${p.date.slice(0,4)}/${p.date}.html">
                 ${p.date} ${p.time}
                 </a> — ${p.text}`;
            resultsDiv.appendChild(el);
        }
    });
}
""")

    fp.write("</script>")
    fp.write("</head><body>")

    fp.write("<h1>Twitter Archive Index</h1>")

    # 🔎 検索窓（ここ重要）
    fp.write('<input id="search" onkeyup="searchAll()" placeholder="全年検索...">')
    fp.write('<div id="results"></div>')

    fp.write("<h2>Years</h2>")
    fp.write("<ul>")

    for year in sorted(months_by_year):
        fp.write(
            f"<li><strong>{year} ({year_counts.get(year,0)}件)</strong>"
        )
        fp.write("<ul>")

        for month in sorted(months_by_year[year]):
            fp.write(
                f'<li><a href="{year}/{month}.html">'
                f'{month} ({month_counts.get(month,0)}件)'
                f'</a></li>'
            )

        fp.write("</ul></li>")

    fp.write("</ul>")
    fp.write("</body></html>")

print("✔ twilog風アーカイブ + 全年検索 完成")