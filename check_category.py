import re
import json
import urllib.request

cid = 50000008

url = f"https://live.ecomm-data.com/report/category/{cid}"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req).read().decode("utf-8")

m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
data = json.loads(m.group(1))
print(json.dumps(data, ensure_ascii=False, indent=2))
