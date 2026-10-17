# Zombie TheZone (ZONE Z) – bản đồ mã cho phiên làm việc mới

Đọc file này thay vì đọc lại toàn bộ `index.html` (355 KB, 1.081 dòng; dòng 346 và 664 là ảnh base64 rất dài, đừng in ra).
Bối cảnh kinh doanh, lộ trình, việc còn mở: project claude.ai "TZ zombie", file `claude/00-doc-truoc.md`.

## Tệp
| Tệp | Vai trò |
|---|---|
| `index.html` | Toàn bộ game (HTML + CSS + JS trong một file) |
| `staff.html` | Trang Quầy: tab Quầy (nhân viên) và Quản lý (admin, 5 tab con ov/acc/st/cfg/staff, nhớ ở localStorage `zz.sub`) |
| `tram.html?id=&name=&lv=` | In tấm dán trạm nạp A5, QR tới `/?tram=ID` |
| `firestore.rules` | Luật Firestore, dán tay vào Firebase Console mỗi khi đổi |
| `firebase-config.js` | Cấu hình web Firebase (zonez-b59fe, công khai được) |
| `lib/qrcode.js`, `lib/jsQR.js` | Thư viện QR lưu sẵn (không dùng CDN) |
| `img/home.webp` | Ảnh sảnh 941×1050 (đã xoá icon) |
| `img/nv/<id>-z.webp` / `-h.webp` | Nhân vật zombie / đã chữa, 1024² nền trong. `-za`/`-ha` = ảnh mặt cắt sẵn |
| `.github/workflows/fetch-art.yml` + `ref/urls.txt` | Action tải ảnh từ URL vào `ref/gen` (vì sandbox không tải được CloudFront) |
| `tools/` | Script dựng video, sprite, QR, stub test. Xem `tools/README.md` |

## index.html theo dòng (xấp xỉ)
- 123 CSS màn săn · 315 dữ liệu game: `TIERS, ZOMBIES, SEASONS, TOPPINGS, ICON, QUOTA{5:7,6:5,8:3,10:2,15:1,20:2}, MINORDER, FLASH_MAX=15, REGEN_MS=5 phút`
- 354 trạng thái `S` (localStorage `zonez.v1`, `DEF`), `INFECT_MS=30 phút`, `AVATARS`, `face()`, `regen()`
- 371 âm thanh WebAudio: `growl(d,pan,kind)`, `droneSet`, `heartbeat(v,fast)`, bus nén + reverb
- 439 nhịp gặp: `sampleWait, rollTier, pickZombie`
- 445 các tab: `render, homeHTML` (sảnh, ô tChars/tShop/tBag/nearSt/tStats/tEvent), `charsHTML, eventSheet, bagHTML` (đổi topping), `statsHTML, simHTML, bind`
- 564 mã đổi quà `newCode, redeem` · 578 Shop `SHOP{use,frame,scope,fx}, shopHTML, buy` · 638 `profileSheet`
- 664 màn săn: `SPRITES, HEAD, geom, drawScope, drawShape, walkFrame` (tách chân ở HIP 0.6, thân lắc 12 dải), `drawSprite, spawn, shoot, finish` (bùa chặn cắn), `updateApproach, loop`
- 896 cloud: `CLOUD, loadGameConfig` (config/game), `listenUser` (áp grant từ quầy), `nickLogin, takeQuota, askFriendCure`
- 983 trạm: `STATION_LV{nho:5,vua:10,lon:25}, chargeAt` (GPS rồi transaction), `scanStation` (jsQR)
- 1013 `nearStations` (Trạm nạp gần bạn, có `storeRow` Quầy THEZONE) · 1039 `handleStationLink, handleCureLink`

## Tài khoản và dữ liệu
- Nickname: `nickNorm` = NFC, trim, gộp khoảng trắng, chữ thường. Email = `n` + 20 byte đầu hex SHA-256(nickNorm) + `@nick.zonez.app`, mật khẩu `zonez-` + PIN.
- Firestore: `users, codes, quota/{ngày}, cures, stations, stationUse/{tram_ngày}, config/staff{emails,admins}, config/game`.
- Nhân viên/admin bắt buộc đăng nhập Google. Grant từ quầy: `grantRefill, grantCure, grantTzAt/grantTzAmt, locked`.

## Cách làm việc
- Kiểm thử: `python3 -m http.server 8767` + Playwright (Chromium ở `/opt/pw-browsers/chromium`), stub Firebase trong `tools/test/`. Sandbox không gọi được Firebase thật.
- Ảnh AI (Higgsfield gpt_image_2_5): đẩy ảnh tham khảo lên repo, import bằng URL raw GitHub; kết quả ghi vào `ref/urls.txt`, chạy Action rồi `git pull`.
- Commit tiếng Việt, mô tả thay đổi cho người dùng. Đổi `firestore.rules` thì nhắc Tín dán lại vào Console.
- Không đăng, không gửi gì thay Tín khi chưa hỏi.
