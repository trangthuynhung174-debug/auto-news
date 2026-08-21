import json
import os
import re
from datetime import datetime, timezone

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
LATEST_PATH = os.path.join(DATA_DIR, "latest.json")
PET_SEEN_PATH = os.path.join(DATA_DIR, "pet_seen.json")
PET_OUTPUT_PATH = os.path.join(DATA_DIR, "pet_news.md")

# Petrosetco (PET) — khớp mã "PET" đứng riêng, hoặc tên công ty đầy đủ.
PET_PATTERN = re.compile(
    r"\bPET\b|Petrosetco|Tổng công ty Dịch vụ Tổng hợp Dầu khí",
    re.IGNORECASE,
)


def load_seen():
    if not os.path.exists(PET_SEEN_PATH):
        return set()
    with open(PET_SEEN_PATH, "r", encoding="utf-8") as f:
        return set(json.load(f))


def save_seen(seen):
    with open(PET_SEEN_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted(seen), f, ensure_ascii=False, indent=2)


def main():
    with open(LATEST_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    seen = load_seen()
    matches = [
        item for item in data["items"]
        if item["link"] not in seen and PET_PATTERN.search(item["title"])
    ]

    for item in matches:
        seen.add(item["link"])
    save_seen(seen)

    now = datetime.now(timezone.utc)
    lines = [f"# Tin PET — cập nhật {now.isoformat()}", ""]
    if matches:
        for item in matches:
            lines.append(f"PET - {item['title']} ({item['link']})")
    else:
        lines.append("(Không có tin mới)")

    with open(PET_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Found {len(matches)} new PET items.")


if __name__ == "__main__":
    main()
