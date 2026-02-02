# App Cơm Trưa 🍱

App điểm danh ăn trưa đơn giản cho 4 người.

## Tính năng
- Điểm danh hàng ngày cho 4 người
- Báo cáo tháng tự động
- Tính tiền: 40,000 VND/bữa

## Cài đặt APK

### Cách 1: Download APK từ GitHub (Khuyên dùng)
1. Vào tab **Actions** trên GitHub
2. Click vào build mới nhất (màu xanh ✓)
3. Scroll xuống phần **Artifacts**
4. Download file `app-release`
5. Giải nén và cài file APK vào Android

### Cách 2: Chạy trên máy
```bash
pip install flet
flet run main.py
```

## Hướng dẫn Push lên GitHub

```bash
# Trong thư mục Appcomtrua
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/hungphuly/appcomtrua.git
git push -u origin main
```

Sau khi push, GitHub Actions sẽ tự động build APK!
