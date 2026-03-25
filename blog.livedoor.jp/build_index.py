import os
import re
import json
from bs4 import BeautifulSoup
from collections import defaultdict

HTML_DIR="html"

posts={}
search_data=[]

print("scan html...")

for f in os.listdir(HTML_DIR):

    if not f.endswith(".html"):
        continue

    post_id=f.split(".")[0]

    if post_id in posts:
        continue

    path=os.path.join(HTML_DIR,f)

    with open(path,encoding="utf-8",errors="ignore") as r:
        html=r.read()

    soup=BeautifulSoup(html,"html.parser")

    title=soup.title.string.strip() if soup.title else f

    # タイトル整理
    title=re.sub(r".*?:","",title)
    title=re.sub(r" - livedoor Blog.*","",title)

    text=soup.get_text()

    # livedoor形式
    m=re.search(r"(20\d\d)年(\d{1,2})月(\d{1,2})日",text)

    if not m:
        continue

    y,mn,d=m.groups()

    date=f"{y}-{int(mn):02}-{int(d):02}"
    month=f"{y}-{int(mn):02}"

    body=" ".join(text.split())

    posts[post_id]={
        "title":title.strip(),
        "file":f,
        "date":date,
        "month":month,
        "body":body
    }

print("articles:",len(posts))

months=defaultdict(list)

for p in posts.values():
    months[p["month"]].append(p)

sorted_months=sorted(months.keys(),reverse=True)

for p in posts.values():
    search_data.append({
        "title":p["title"],
        "date":p["date"],
        "file":p["file"],
        "body":p["body"][:5000]
    })

with open("index.html","w",encoding="utf-8") as w:

    w.write(f"""
<meta charset="UTF-8">

<style>

body{{
font-family:-apple-system,BlinkMacSystemFont,Helvetica;
max-width:900px;
margin:auto;
padding:40px;
background:#fafafa;
}}

h1{{border-bottom:2px solid #ddd;padding-bottom:10px}}

.month{{font-size:22px;margin-top:30px;border-bottom:1px solid #ddd}}

.post{{margin:6px 0}}

input{{width:100%;padding:8px;font-size:16px;margin-bottom:20px}}

a{{text-decoration:none;color:#0366d6}}

a:hover{{text-decoration:underline}}

.count{{color:#666;margin-bottom:20px}}

</style>

<h1>Livedoor Blog Archive</h1>

<div class="count">{len(posts)} articles</div>

<input id="search" placeholder="検索 (タイトル / 本文)">

<div id="results"></div>

<div id="archive">
""")

    for m in sorted_months:

        w.write(f'<div class="month">{m}</div>\n')

        posts_sorted=sorted(
            months[m],
            key=lambda x:x["date"],
            reverse=True
        )

        for p in posts_sorted:

            line=f'{p["date"]}:{p["title"]}'

            w.write(
                f'<div class="post"><a href="html/{p["file"]}">{line}</a></div>\n'
            )

    w.write("</div>")

    w.write(f"""
<script>

const posts={json.dumps(search_data,ensure_ascii=False)};

const search=document.getElementById("search");
const results=document.getElementById("results");
const archive=document.getElementById("archive");

search.addEventListener("input",function(){{

const q=this.value.toLowerCase();

if(q===""){{
results.innerHTML="";
archive.style.display="block";
return;
}}

archive.style.display="none";

let html="";

posts.forEach(p=>{{
const text=(p.date+" "+p.title+" "+p.body).toLowerCase();

if(text.includes(q)){{
html+=`<div><a href="html/${{p.file}}">${{p.date}}:${{p.title}}</a></div>`;
}}
}});

results.innerHTML=html;

}});
</script>
""")

print("index.html created")