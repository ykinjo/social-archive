import time
import os
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


OWNER_ID = "773882"


# Chrome設定
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)


print("Opening mixi...")
driver.get("https://mixi.jp")

input("mixiにログインしたら Enter を押してください")


# -----------------------------
# 日記URL収集
# -----------------------------

diary_ids = set()

page = 1

print("Collecting diary URLs...")

while True:

    url = f"https://mixi.jp/list_diary.pl?owner_id={OWNER_ID}&page={page}"

    driver.get(url)

    time.sleep(2)

    html = driver.page_source

    # 空ページ検出
    if "nothing.gif" in html:

        print("Reached last page.")
        break

    links = driver.find_elements(By.TAG_NAME, "a")

    found = 0

    for l in links:

        href = l.get_attribute("href")

        if not href:
            continue

        if "view_diary.pl" not in href:
            continue

        m = re.search(r"id=(\d+)", href)

        if not m:
            continue

        diary_id = m.group(1)

        if diary_id not in diary_ids:

            diary_ids.add(diary_id)

            found += 1

    print(f"page {page}  found {found}  total {len(diary_ids)}")

    page += 1


print("Total diaries:", len(diary_ids))


# -----------------------------
# 保存フォルダ
# -----------------------------

os.makedirs("diary", exist_ok=True)


# -----------------------------
# 日記ダウンロード
# -----------------------------

print("Downloading diaries...")


for i, diary_id in enumerate(sorted(diary_ids)):

    url = f"https://mixi.jp/view_diary.pl?id={diary_id}&owner_id={OWNER_ID}"

    try:

        driver.get(url)

        time.sleep(2)

        html = driver.page_source

        filename = f"diary/{diary_id}.html"

        with open(filename, "w", encoding="utf-8") as f:

            f.write(html)

        print(f"{i+1}/{len(diary_ids)} saved {filename}")

    except Exception as e:

        print("ERROR:", url)

        print(e)


print("DONE")

driver.quit()