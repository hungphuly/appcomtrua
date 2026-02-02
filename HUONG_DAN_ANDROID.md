# Hướng dẫn chạy App Cơm Trưa trên Android

## Cách 1: Sử dụng Termux (app Android)

### Bước 1: Cài Termux
- Tải Termux từ F-Droid: https://f-droid.org/packages/com.termux/
- KHÔNG tải từ Google Play (version cũ)

### Bước 2: Cài Python và Flet trong Termux
Mở Termux và chạy lần lượt:
```bash
pkg update
pkg install python
pip install flet
```

### Bước 3: Copy file main.py vào điện thoại
- Copy file main.py từ máy tính vào thư mục Downloads của điện thoại
- Trong Termux, chạy:
```bash
cd ~/storage/downloads
python main.py
```

App sẽ mở trong trình duyệt trên điện thoại!

---

## Cách 2: Chạy như Web App

### Trên máy tính:
```bash
cd c:\Users\hungnq5\OneDrive\Desktop\Python\Appcomtrua
flet run main.py --web --port 8080
```

### Trên điện thoại:
- Kết nối cùng WiFi với máy tính
- Mở trình duyệt trên điện thoại
- Vào địa chỉ: `http://[IP-may-tinh]:8080`
- (Tìm IP máy tính bằng lệnh `ipconfig` trên Windows)

---

## Cách 3: Build APK trên Linux/Mac (nếu có)

Nếu bạn có máy Linux hoặc Mac:
```bash
cd Appcomtrua
flet build apk --yes
```

File APK sẽ ở: `build/apk/app-release.apk`

---

## Lý do Build APK thất bại

Build APK trên Windows cần:
- Flutter SDK (>1GB)
- Android SDK (>3GB)
- JDK (>500MB)
- Gradle và các công cụ Android

Tổng cần hơn 5GB và cấu hình Android SDK phức tạp.

**Khuyến nghị**: Dùng Cách 1 (Termux) - đơn giản và nhanh nhất!
