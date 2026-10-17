# Zombie TheZone (ZONE Z)

Game bắt zombie bằng camera của THEZONE (Phú Tân, An Giang). Chạy trên trình duyệt điện thoại, không cần cài app.

- Chơi: https://zonezgame.github.io/
- Trang Quầy (nhân viên, quản lý): https://zonezgame.github.io/staff.html
- Bản đồ mã cho người sửa: `CLAUDE.md`. Script phụ trợ: `tools/`.

## Firebase (dự án zonez-b59fe)
1. Authentication: bật Email/Password (nickname), Anonymous (chơi thử), Google (nhân viên). Authorized domains có `zonezgame.github.io`.
2. Firestore → Rules: dán toàn bộ `firestore.rules` → Publish (làm lại mỗi khi file này đổi).
3. `config/staff`: `admins` (email quản lý), `emails` (email nhân viên). Thêm nhân viên trong trang Quầy → Quản lý → Nhân viên.

Khách đăng nhập bằng nickname tự do + PIN 4 số; quên PIN thì tạo nickname mới. Chưa có mạng thì game vẫn chạy, dữ liệu lưu trên máy.
