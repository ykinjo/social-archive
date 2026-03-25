from bs4 import BeautifulSoup

file = "diary/998239751.html"   # 実在するHTMLに合わせて変更

with open(file, encoding="euc-jp", errors="ignore") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

print("TITLE:", soup.title.text)

print("\n---- TEXT PREVIEW ----\n")

text = soup.get_text("\n")

print(text[:2000])