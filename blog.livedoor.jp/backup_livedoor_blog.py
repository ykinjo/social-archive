import requests
from bs4 import BeautifulSoup
import os
import re
import urllib3
from urllib.parse import urljoin

urllib3.disable_warnings()

BASE = "https://blog.livedoor.jp/barchetta/"

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0"

os.makedirs("html", exist_ok=True)
os.makedirs("images", exist_ok=True)

article_links = set()

page = 1

while True:

    url = BASE + f"?p={page}"
    print("scan:", url)

    r = session.get(url, verify=False)

    if r.status_code != 200:
        break

    soup = BeautifulSoup(r.text, "html.parser")

    found = 0

    for a in soup.find_all("a", href=True):

        if re.search(r"/archives/\d+\.html", a["href"]):

            link = urljoin(BASE, a["href"])

            if link not in article_links:
                article_links.add(link)
                found += 1

    if found == 0:
        break

    page += 1

print("found articles:", len(article_links))

for url in sorted(article_links):

    print("fetch:", url)

    r = session.get(url, verify=False)

    html = r.text
    name = url.split("/")[-1]

    with open("html/" + name, "w", encoding="utf8") as f:
        f.write(html)

    soup = BeautifulSoup(html, "html.parser")

    for img in soup.find_all("img", src=True):

        src = img["src"]

        if "blogimg.jp" not in src:
            continue

        img_url = urljoin(url, src)

        img_name = img_url.split("/")[-1]
        path = "images/" + img_name

        if os.path.exists(path):
            continue

        print("  image:", img_url)

        try:
            ir = session.get(img_url, verify=False, timeout=30)

            with open(path, "wb") as f:
                f.write(ir.content)

        except:
            print("  failed:", img_url)