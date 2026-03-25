import os
import re

HTML_DIR = "html"

for file in os.listdir(HTML_DIR):

    if not file.endswith(".html"):
        continue

    path = os.path.join(HTML_DIR, file)

    with open(path, encoding="utf-8") as f:
        html = f.read()

    # サムネ
    html = re.sub(
        r'src="https://livedoor\.blogimg\.jp/.+?/([^"/]+-s\.(jpg|jpeg|png|gif|JPG|JPEG|PNG|GIF))"',
        r'src="../images/\1"',
        html
    )

    # 元画像
    html = re.sub(
        r'href="https://livedoor\.blogimg\.jp/.+?/([^"/]+\.(jpg|jpeg|png|gif|JPG|JPEG|PNG|GIF))"',
        r'href="../images_full/\1"',
        html
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    print("fixed:", file)