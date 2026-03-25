import os
import re
from bs4 import BeautifulSoup

INPUT_DIR = "diary"
OUTPUT_DIR = "diary_md"
IMG_DIR = "images"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_date(text):
    m = re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日", text)
    if not m:
        return ""
    y,mn,d = m.groups()
    return f"{y}-{int(mn):02d}-{int(d):02d}"

def extract_body(soup):

    body = (
        soup.find("div", class_="txtconfirmArea")
        or soup.find("div", class_="diaryBody")
        or soup.find("div", id="bodyMainArea")
        or soup.find("div", class_="articleBody")
    )

    return body


def convert_images(body):

    for img in body.find_all("img"):

        src = img.get("src")
        if not src:
            continue

        if "emoji" in src:
            img.decompose()
            continue

        if "photo/diary" not in src:
            img.decompose()
            continue

        filename = src.split("/")[-1]

        # mixiサムネイル → 元画像
        filename = re.sub(r's\.jpg$', '.jpg', filename)

        md = f"\n![](../images/{filename})\n"

        img.replace_with(md)


def convert_youtube(body):

    for iframe in body.find_all("iframe"):

        src = iframe.get("src","")

        m = re.search(r"youtube\.com/embed/([a-zA-Z0-9_-]+)", src)

        if m:
            vid = m.group(1)
            url = f"https://www.youtube.com/watch?v={vid}"
            iframe.replace_with("\n"+url+"\n")


def extract_likes(soup):

    likes = []

    like_area = soup.find(string=re.compile("イイネ"))

    if not like_area:
        return likes

    for a in soup.find_all("a"):

        href = a.get("href","")

        if "show_friend.pl" in href:

            name = a.text.strip()

            if name:
                likes.append(name)

    return list(set(likes))


def extract_comments(soup):

    comments = []

    blocks = soup.find_all("dl")

    for dl in blocks:

        dt = dl.find("dt")
        dd = dl.find("dd")

        if not dt or not dd:
            continue

        user = dt.get_text(strip=True)
        text = dd.get_text("\n",strip=True)

        if text:
            comments.append((user,text))

    return comments


count = 0

for file in os.listdir(INPUT_DIR):

    if not file.endswith(".html"):
        continue

    path = os.path.join(INPUT_DIR,file)

    with open(path,"rb") as f:
        raw = f.read()

    html = None
    for enc in ["utf-8","cp932","shift_jis","euc-jp"]:
        try:
            html = raw.decode(enc)
            break
        except:
            pass

    if not html:
        print("decode error:",file)
        continue

    soup = BeautifulSoup(html,"html.parser")

    title = ""
    if soup.title:
        title = soup.title.text.strip()

    h1 = soup.find("h1")
    if h1:
        title = h1.text.strip()

    date = extract_date(soup.get_text())

    body = extract_body(soup)

    if not body:
        print("body missing:",file)
        continue

    convert_images(body)
    convert_youtube(body)

    text = body.get_text("\n").strip()

    likes = extract_likes(soup)
    comments = extract_comments(soup)

    md = []

    if title:
        md.append(f"# {title}\n")

    if date:
        md.append(f"**作成日:** {date}\n")

    md.append(text)

    if likes:
        md.append("\n---\n")
        md.append(f"## イイネ ({len(likes)})\n")
        for u in likes:
            md.append(f"- {u}")

    if comments:
        md.append("\n---\n")
        md.append("## コメント\n")

        for u,t in comments:
            md.append(f"**{u}**")
            md.append("")
            md.append(t)
            md.append("")

    diary_id = file.replace(".html","")

    if date:
        outname = f"{date}_{diary_id}.md"
    else:
        outname = f"{diary_id}.md"

    outpath = os.path.join(OUTPUT_DIR,outname)

    with open(outpath,"w",encoding="utf-8") as f:
        f.write("\n".join(md))

    count += 1

print("converted:",count)