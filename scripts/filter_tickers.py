import json
import os
from datetime import datetime, timezone

import requests

from tickers import TICKERS

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
LATEST_PATH = os.path.join(DATA_DIR, "latest.json")

NTFY_TOPIC_URL = "https://ntfy.sh/investment-opp"


def seen_path(ticker):
    return os.path.join(DATA_DIR, f"{ticker.lower()}_seen.json")


def output_path(ticker):
    return os.path.join(DATA_DIR, f"{ticker.lower()}_news.md")


def load_seen(ticker):
    path = seen_path(ticker)
    if not os.path.exists(path):
        return set()
    with open(path, "r", encoding="utf-8") as f:
        return set(json.load(f))


def save_seen(ticker, seen):
    with open(seen_path(ticker), "w", encoding="utf-8") as f:
        json.dump(sorted(seen), f, ensure_ascii=False, indent=2)


def push_ntfy(ticker, item):
    try:
        requests.post(
            NTFY_TOPIC_URL,
            data=f"{ticker} - {item['title']} ({item['link']})".encode("utf-8"),
            headers={
                "Title": f"Tin {ticker} moi".encode("ascii"),
                "Click": item["link"],
            },
            timeout=10,
        )
    except Exception as exc:
        print(f"[ntfy] failed to push for {ticker}: {exc}")


def process_ticker(ticker, config, items):
    seen = load_seen(ticker)
    matches = [
        item for item in items
        if item["link"] not in seen and config["pattern"].search(item["title"])
    ]

    for item in matches:
        seen.add(item["link"])
        push_ntfy(ticker, item)
    save_seen(ticker, seen)

    now = datetime.now(timezone.utc)
    lines = [f"# Tin {ticker} — cập nhật {now.isoformat()}", ""]
    if matches:
        for item in matches:
            lines.append(f"{ticker} - {item['title']} ({item['link']})")
    else:
        lines.append("(Không có tin mới)")

    with open(output_path(ticker), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"[{ticker}] Found {len(matches)} new items.")


def main():
    with open(LATEST_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for ticker, config in TICKERS.items():
        process_ticker(ticker, config, data["items"])


if __name__ == "__main__":
    main()
