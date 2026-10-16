# ZONE Z

Game bắt zombie bằng camera của THEZONE (Phú Tân, An Giang). Bản test trên điện thoại.

- Chơi: https://zonezgame.github.io/
- Một file `index.html`, không cần cài đặt. Dữ liệu chơi lưu trên máy người chơi.
- Cần mở qua https để điện thoại cho dùng camera và cảm biến xoay.

## Tài khoản (Firebase)
1. Dán `firebaseConfig` vào `firebase-config.js` (thay `null`).
2. Firestore → Rules: dán toàn bộ `firestore.rules` → Publish.
3. Firestore → tạo collection `config`, document `staff`, field `emails` (array) chứa email Google của nhân viên.
4. Nhân viên mở `staff.html` để quét mã tại quầy.

Khách đăng nhập bằng nickname tự do (có dấu, ký tự đặc biệt) + PIN 4 số; quên PIN thì tạo nickname mới (cần bật Email/Password và Anonymous trong Authentication). Nhân viên dùng Google cho trang quầy.

Chưa có cấu hình thì game vẫn chạy, dữ liệu lưu trên máy.
