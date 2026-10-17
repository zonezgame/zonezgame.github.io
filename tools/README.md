# tools/ – script phụ trợ (không phải phần của game)

Đường dẫn trong script là đường dẫn tuyệt đối của phiên cũ (`/home/claude/...`, thư mục scratchpad). Sửa biến đầu file trước khi chạy.

| Thư mục | Tệp | Dùng để |
|---|---|---|
| `video/` | `rec3.js` (rec2 là bản trước) | Quay từng khung cảnh chơi bằng Playwright, thời gian ảo |
| | `audio.js` | Dựng nhạc nền + gầm gừ + tim đập bằng OfflineAudioContext ra `promo.wav` |
| | `make.py` | Ghép video 60s 1080×1920 (PIL → ffmpeg), loudnorm, ghép tiếng. Bản an toàn TikTok: không QR, không máu, CTA "Link chơi ở bio" |
| `sprites/` | `isnet.py, cut.py, refine.py, harden.py, clean.py, compose.py, build.py` | Tách nền nhân vật (ISNet onnx + GrabCut), làm sạch viền, ghép thẻ. Đã được thay bằng ảnh AI nền trong, giữ để tham khảo |
| `qr/` | `mkqr.js` | Tạo QR SVG (dùng `lib/qrcode.js`), mức Q |
| | `qrcheck.js` | Giải mã thử QR bằng jsQR trong Chromium |
| `icons/` | `icons.py, render.js` | Bộ icon 19 topping |
| | `zombie-chars-v2.py` | Bộ nhân vật chibi vector v2 (sticker, thẻ trước/sau) |
| `test/` | `fbstub.js, gamestub.js, gamestub2.js` | Giả lập Firebase để test game và trang Quầy không cần mạng |
