import json
import os
import sys
import time
from datetime import datetime, timezone

import feedparser
import requests

from feeds import FEEDS

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
LATEST_PATH = os.path.join(DATA_DIR, "latest.json")
ARCHIVE_DIR = os.path.join(DATA_DIR, "archive")

HEADERS = {"User-Agent": "Mozilla/5.0 (Auto-News collector)"}

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def fetch_feed(feed):
    try:
        resp = requests.get(feed["url"], headers=HEADERS, timeout=15)
        resp.raise_for_status()
        parsed = feedparser.parse(resp.content)
    except Exception as exc:
        print(f"[skip] {feed['name']}: {exc}")
        return []

    items = []
    for entry in parsed.entries:
        items.append({
            "source": feed["name"],
            "title": entry.get("title", "").strip(),
            "link": entry.get("link", "").strip(),
            "published": entry.get("published", entry.get("updated", "")),
        })
    return items


def load_existing_links():
    if not os.path.exists(LATEST_PATH):
        return set()
    with open(LATEST_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {item["link"] for item in data.get("items", [])}


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    all_items = []
    for feed in FEEDS:
        all_items.extend(fetch_feed(feed))
        time.sleep(1)

    seen = set()
    deduped = []
    for item in all_items:
        if item["link"] and item["link"] not in seen:
            seen.add(item["link"])
            deduped.append(item)

    now = datetime.now(timezone.utc)
    result = {
        "collected_at": now.isoformat(),
        "count": len(deduped),
        "items": deduped,
    }

    with open(LATEST_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    archive_path = os.path.join(ARCHIVE_DIR, f"{now.strftime('%Y-%m-%d')}.json")
    existing_archive = []
    if os.path.exists(archive_path):
        with open(archive_path, "r", encoding="utf-8") as f:
            existing_archive = json.load(f).get("items", [])

    archive_links = {item["link"] for item in existing_archive}
    new_for_archive = existing_archive + [i for i in deduped if i["link"] not in archive_links]

    with open(archive_path, "w", encoding="utf-8") as f:
        json.dump({"date": now.strftime("%Y-%m-%d"), "items": new_for_archive}, f, ensure_ascii=False, indent=2)

    print(f"Collected {len(deduped)} items from {len(FEEDS)} feeds.")


if __name__ == "__main__":
    main()
