#!/usr/bin/env python3

import re
import os
import sys
import html
import glob
import requests
from http.cookiejar import MozillaCookieJar


if len(sys.argv) < 3:
    print("usage: python extract_all_mixi_diary_images.py diary_dir cookies.txt")
    sys.exit(1)

diary_dir = sys.argv[1]
cookie_file = sys.argv[2]

# cookies
cj = MozillaCookieJar()
cj.load(cookie_file, ignore_discard=True, ignore_expires=True)

session = requests.Session()
session.cookies = cj
session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://mixi.jp/"
})

all_images = set()

html_files = sorted(glob.glob(os.path.join(diary_dir, "*.html")))

print("found diary html:", len(html_files))
print()

for file in html_files:

    print("processing:", file)

    html_text = open(file, encoding="utf-8").read()

    links = re.findall(
        r"/show_diary_picture\.pl\?owner_id=\d+&amp;id=\d+&amp;number=\d+",
        html_text
    )

    links = sorted(set(links))

    image_urls = []

    for link in links:

        link = html.unescape(link)
        url = "https://mixi.jp" + link

        r = session.get(url)

        imgs = re.findall(
            r"https://classic-imagecluster\.img\.mixi\.jp[^\"']+\.jpg",
            r.text
        )

        for img in imgs:
            image_urls.append(img)
            all_images.add(img)

    image_urls = sorted(set(image_urls))

    print("  images:", len(image_urls))

    if image_urls:

        name = os.path.basename(file).replace(".html", "_images.txt")
        path = os.path.join(diary_dir, name)

        with open(path, "w") as f:
            for u in image_urls:
                f.write(u + "\n")

print()

print("total unique images:", len(all_images))

with open(os.path.join(diary_dir, "ALL_images.txt"), "w") as f:
    for u in sorted(all_images):
        f.write(u + "\n")

print("saved:", os.path.join(diary_dir, "ALL_images.txt"))
