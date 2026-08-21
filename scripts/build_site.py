import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
SITE_DIR = os.path.join(os.path.dirname(__file__), "..", "site")
LATEST_PATH = os.path.join(DATA_DIR, "latest.json")

TEMPLATE = """<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<title>Auto-News — Tin chứng khoán VN</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 760px; margin: 2rem auto; padding: 0 1rem; }}
  h1 {{ font-size: 1.4rem; }}
  .item {{ padding: .75rem 0; border-bottom: 1px solid #ddd; }}
  .source {{ color: #888; font-size: .8rem; }}
  a {{ text-decoration: none; color: #0b5fff; }}
  .meta {{ color: #999; font-size: .75rem; }}
</style>
</head>
<body>
<h1>Tin chứng khoán Việt Nam</h1>
<p class="meta">Cập nhật lúc: {collected_at} — {count} tin</p>
{items}
</body>
</html>
"""

ITEM_TEMPLATE = """<div class="item">
  <a href="{link}" target="_blank" rel="noopener">{title}</a>
  <div class="source">{source} · {published}</div>
</div>
"""


def main():
    os.makedirs(SITE_DIR, exist_ok=True)
    with open(LATEST_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    items_html = "\n".join(
        ITEM_TEMPLATE.format(
            link=item["link"],
            title=item["title"],
            source=item["source"],
            published=item["published"],
        )
        for item in data["items"]
    )

    html = TEMPLATE.format(
        collected_at=data["collected_at"],
        count=data["count"],
        items=items_html,
    )

    with open(os.path.join(SITE_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    main()
