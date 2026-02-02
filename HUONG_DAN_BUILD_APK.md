# HƯỚNG DẪN TẠO APK - TỪNG BƯỚC

## ✅ ĐÃ HOÀN THÀNH
- [x] Tạo code app
- [x] Setup GitHub Actions workflow
- [x] Commit code vào Git

## 🔄 CẦN LÀM TIẾP

### Bước 1: Tạo Repository trên GitHub
1. Mở trình duyệt: https://github.com/new
2. Repository name: **appcomtrua**
3. Chọn **Public**
4. **KHÔNG** tick "Add a README file"
5. Click **Create repository**

### Bước 2: Push Code lên GitHub
Sau khi tạo repo, GitHub sẽ hiển thị hướng dẫn. Chạy 2 lệnh này:

```bash
cd c:\Users\hungnq5\OneDrive\Desktop\Python\Appcomtrua

git remote add origin https://github.com/[USERNAME]/appcomtrua.git
git push -u origin main
```

**Thay [USERNAME] bằng username GitHub của bạn!**

### Bước 3: Đợi GitHub Build APK
1. Vào: https://github.com/[USERNAME]/appcomtrua/actions
2. Đợi 5-10 phút (biểu tượng vòng tròn vàng → chuyển xanh ✓)
3. Click vào build mới nhất
4. Scroll xuống phần **Artifacts**
5. Click download **app-release**
6. Giải nén file ZIP → Có file APK!

### Bước 4: Cài APK lên Android
1. Copy file APK vào điện thoại
2. Mở File Manager → tìm file APK
3. Click vào → Cài đặt
4. (Nếu cần: Bật "Cài từ nguồn không xác định" trong Settings)

---

## ❓ CÂU HỎI THƯỜNG GẶP

**Q: Tôi chưa có GitHub account?**
- Đăng ký miễn phí tại: https://github.com/signup

**Q: Không muốn dùng GitHub?**
- Dùng Termux trên Android để build trực tiếp
- Hoặc chạy app như Web App (không cần cài đặt)

**Q: File APK có an toàn không?**
- Có! Code hoàn toàn do bạn tự build, không có gì nguy hiểm

---

## 📞 CẦN GIÚP?

Cho tôi biết:
- Username GitHub của bạn
- Hoặc bạn gặp lỗi ở bước nào
