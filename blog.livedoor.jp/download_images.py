import os
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings()

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0"

os.makedirs("images_full", exist_ok=True)

for file in os.listdir("html"):

    if not file.endswith(".html"):
        continue

    path = os.path.join("html", file)

    with open(path, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    for a in soup.find_all("a", href=True):

        url = a["href"]

        if "livedoor.blogimg.jp" not in url:
            continue

        filename = url.split("/")[-1]
        save = os.path.join("images_full", filename)

        if os.path.exists(save):
            continue

        print("download:", url)

        try:
            r = session.get(url, verify=False, timeout=30)

            if r.status_code == 200:
                with open(save, "wb") as w:
                    w.write(r.content)

        except Exception as e:
            print("failed:", url)