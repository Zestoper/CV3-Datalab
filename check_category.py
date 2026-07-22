import json
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))
from app.category_map import CATEGORY_TITLES

SITEMAP_URL = "https://live.ecomm-data.com/sitemaps/sitemap_category.xml"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req).read().decode("utf-8")


def discover_cids() -> list[int]:
    xml = fetch(SITEMAP_URL)
    return sorted({int(m) for m in re.findall(r"/report/category/(\d+)", xml)})


def fetch_title(cid: int) -> str | None:
    html = fetch(f"https://live.ecomm-data.com/report/category/{cid}")
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    category = json.loads(m.group(1))["props"]["pageProps"]["_category"]
    return category["title"] if category.get("exists") else None


def main() -> None:
    cids = discover_cids()
    missing = [cid for cid in cids if cid not in CATEGORY_TITLES]
    print(f"sitemap cids: {len(cids)}, already mapped: {len(cids) - len(missing)}, missing: {len(missing)}")
    for cid in missing:
        title = fetch_title(cid)
        if title is None:
            print(f"  {cid}: (404 / no category)")
            continue
        print(f'    {cid}: "{title}",')


if __name__ == "__main__":
    main()
