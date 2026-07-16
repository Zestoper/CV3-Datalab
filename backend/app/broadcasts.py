from datetime import datetime

import httpx

from app.category_map import resolve_lb_category
from app.platform_names import PLATFORM_NAMES

SOURCE_URL = "https://live.ecomm-data.com/api/assignment/list"
WEEKDAY_KR = ["월", "화", "수", "목", "금", "토", "일"]


def _format_datetime(raw: str) -> str:
    # lb: "2607161800" (YYMMDDHHmm), hs: "202607161730" (YYYYMMDDHHmm)
    normalized = raw if len(raw) == 12 else "20" + raw
    dt = datetime.strptime(normalized, "%Y%m%d%H%M")
    return f"{dt.strftime('%y.%m.%d')} ({WEEKDAY_KR[dt.weekday()]}) {dt.strftime('%H:%M')}"


def _normalize_lb(item: dict) -> dict:
    return {
        "id": item["objectID"],
        "platform_name": PLATFORM_NAMES.get(item["platform_id"], item["platform_id"]),
        "title": item["title"],
        "category": resolve_lb_category(item.get("cid")),
        "datetime_start": _format_datetime(item["datetime_start"]),
        "product_cnt": item["product_cnt"],
        "visit_cnt": item["visit_cnt"],
        "sales_cnt": item["sales_cnt"],
        "sales_amt": item["sales_amt"],
    }


def _normalize_hs(item: dict) -> dict:
    return {
        "id": item["hsshow_id"],
        "platform_name": item["platform_name"],
        "title": item["hsshow_title"],
        "category": item["cat"]["cat_name"],
        "datetime_start": _format_datetime(item["hsshow_datetime_start"]),
        "product_cnt": item["item_cnt"],
        "visit_cnt": item["visit_cnt"],
        "sales_cnt": item["sales_cnt"],
        "sales_amt": item["sales_amt"],
    }


async def fetch_broadcasts(broadcast_type: str) -> list[dict]:
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(SOURCE_URL, json={"type": broadcast_type})
        resp.raise_for_status()
        data = resp.json()

    items = data.get("list", [])[:10]
    normalize = _normalize_lb if broadcast_type == "lb" else _normalize_hs
    return [normalize(item) for item in items]
