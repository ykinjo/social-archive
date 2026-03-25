import json

with open("search.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("search_data.js", "w", encoding="utf-8") as f:
    f.write("const SEARCH_DATA = ")
    json.dump(data, f, ensure_ascii=False, indent=2)