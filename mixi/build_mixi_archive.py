import os
import re
import json
from collections import defaultdict

MD_DIR = "diary_md"

posts = []

for f in os.listdir(MD_DIR):

    if not f.endswith(".md"):
        continue

    path = os.path.join(MD_DIR,f)

    with open(path,encoding="utf-8") as fp:
        text = fp.read()

    title = ""

    m = re.search(r"^# (.+)",text,re.MULTILINE)
    if m:
        title = m.group(1)

    m = re.search(r"(\d{4})-(\d{2})-(\d{2})",f)

    if not m:
        continue

    y,mn,d = m.groups()

    posts.append({
        "file":f,
        "title":title,
        "date":f"{y}-{mn}-{d}",
        "year":y,
        "month":f"{y}-{mn}",
        "text":text
    })

posts.sort(key=lambda x:x["date"],reverse=True)

os.makedirs("year",exist_ok=True)
os.makedirs("month",exist_ok=True)

# ----------------
# index + search
# ----------------

search_data = []

for p in posts:
    search_data.append({
        "file":p["file"],
        "title":p["title"],
        "date":p["date"],
        "text":p["text"][:5000]
    })

html = []

html.append(f"""
<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="style.css">
<title>mixi diary archive</title>
</head>
<body>

<h1>mixi diary archive</h1>

<p>{len(posts)} articles</p>

<input id="search" placeholder="検索 (タイトル / 本文)">

<div id="results"></div>

<ul id="archive">
""")

for p in posts:

    html.append(
        f'<li>{p["date"]} '
        f'<a href="diary_md/{p["file"]}">{p["title"]}</a></li>'
    )

html.append("</ul>")

html.append(f"""
<script>

const posts = {json.dumps(search_data,ensure_ascii=False)};

const search = document.getElementById("search");
const results = document.getElementById("results");
const archive = document.getElementById("archive");

search.addEventListener("input",function(){{

const q = this.value.toLowerCase();

if(q==="") {{
results.innerHTML="";
archive.style.display="block";
return;
}}

archive.style.display="none";

let html="";

posts.forEach(p=>{{
const text=(p.date+" "+p.title+" "+p.text).toLowerCase();

if(text.includes(q)) {{
html+=`<div>${{p.date}} <a href="diary_md/${{p.file}}">${{p.title}}</a></div>`;
}}
}});

results.innerHTML=html;

}});

</script>
""")

html.append("</body></html>")

with open("index.html","w",encoding="utf-8") as f:
    f.write("\n".join(html))

# ----------------
# year
# ----------------

years = defaultdict(list)

for p in posts:
    years[p["year"]].append(p)

for y,plist in years.items():

    html=[]

    html.append(f"""
<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="../style.css">
<title>{y}</title>
</head>
<body>

<h1>{y}</h1>
<ul>
""")

    for p in plist:

        html.append(
            f'<li>{p["date"]} '
            f'<a href="../diary_md/{p["file"]}">{p["title"]}</a></li>'
        )

    html.append("</ul></body></html>")

    with open(f"year/{y}.html","w",encoding="utf-8") as f:
        f.write("\n".join(html))

# ----------------
# month
# ----------------

months = defaultdict(list)

for p in posts:
    months[p["month"]].append(p)

for mth,plist in months.items():

    html=[]

    html.append(f"""
<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="../style.css">
<title>{mth}</title>
</head>
<body>

<h1>{mth}</h1>
<ul>
""")

    for p in plist:

        html.append(
            f'<li>{p["date"]} '
            f'<a href="../diary_md/{p["file"]}">{p["title"]}</a></li>'
        )

    html.append("</ul></body></html>")

    with open(f"month/{mth}.html","w",encoding="utf-8") as f:
        f.write("\n".join(html))

print("mixi archive created")