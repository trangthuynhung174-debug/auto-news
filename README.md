# Auto-News

Thu thập tự động tin tức thị trường chứng khoán Việt Nam từ các nguồn RSS, lưu vào `data/`, và publish một trang tin tĩnh qua GitHub Pages. Chạy định kỳ bằng GitHub Actions (`.github/workflows/collect.yml`).

## Cấu trúc
- `scripts/feeds.py` — danh sách nguồn RSS. **Kiểm tra và cập nhật lại các URL này** trước khi chạy thật — đây là danh sách gợi ý, một số nguồn có thể đã đổi URL feed hoặc chặn bot.
- `scripts/collect_news.py` — tải các feed, khử trùng lặp, ghi ra `data/latest.json` và lưu lịch sử theo ngày trong `data/archive/`.
- `scripts/build_site.py` — dựng trang HTML tĩnh từ `data/latest.json` vào `site/index.html`.
- `.github/workflows/collect.yml` — chạy 3 lần/ngày (giờ VN), commit dữ liệu mới và deploy `site/` lên GitHub Pages.

## Chạy thử ở local
```bash
pip install -r requirements.txt
python scripts/collect_news.py
python scripts/build_site.py
```
Mở `site/index.html` để xem kết quả.

## Deploy lên GitHub
1. Tạo repo mới trên GitHub (public hoặc private).
2. Trong repo Settings → Pages, chọn source = "GitHub Actions".
3. Push code lên nhánh `main`.
4. Workflow sẽ tự chạy theo lịch, hoặc bấm "Run workflow" thủ công (tab Actions) để chạy ngay.

## Tuỳ chỉnh
- Đổi lịch chạy: sửa dòng `cron` trong `collect.yml` (giờ UTC).
- Thêm/bớt nguồn tin: sửa `scripts/feeds.py`.
