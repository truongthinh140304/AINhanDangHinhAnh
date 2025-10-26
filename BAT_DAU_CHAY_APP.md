# 🚀 BẮT ĐẦU CHẠY APP - HƯỚNG DẪN NHANH

## ⚠️ ĐANG GẶP VẤN ĐỀ: PASSWORD POSTGRESQL

**Lỗi hiện tại:**
```
password authentication failed for user "postgres"
```

---

## 🎯 CÁC BƯỚC CẦN LÀM (THEO THỨ TỰ)

### ✅ BƯỚC 1: FIX POSTGRESQL PASSWORD (BẮT BUỘC)

**Bạn có 2 lựa chọn:**

#### OPTION A: Nhớ password PostgreSQL (NHANH NHẤT - 2 phút)

```powershell
# 1. Mở file .env
cd D:\AInhandanghinhanh\backend
notepad .env

# 2. Tìm dòng:
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/nhandanghinhanh
#                                    ^^^^^^^^
#                                    Thay "postgres" bằng password thực của bạn

# Ví dụ nếu password là "myPassword123":
DATABASE_URL=postgresql://postgres:myPassword123@localhost:5432/nhandanghinhanh

# 3. Lưu file (Ctrl+S) và đóng Notepad

# 4. Test ngay:
cd D:\AInhandanghinhanh\backend
.\venv\Scripts\activate
python init_db.py
```

**✅ Nếu thấy `[OK] Database connection successful!` → Bạn đã xong! Chuyển sang BƯỚC 2**

---

#### OPTION B: Quên password → Reset password (10 phút)

**B1: Chạy script tự động (KHUYẾN NGHỊ)**

```powershell
# 1. Mở PowerShell VỚI QUYỀN ADMIN
# Cách: Nhấn chuột phải vào PowerShell → "Run as Administrator"

# 2. Chạy script
cd D:\AInhandanghinhanh
.\RESET_POSTGRESQL_PASSWORD_NHANH.ps1

# Script sẽ tự động:
# - Backup file cấu hình
# - Tạm thời tắt authentication
# - Đổi password
# - Khôi phục lại authentication
# - Test connection

# 3. Nhập password mới khi được hỏi (hoặc Enter để dùng "postgres")
```

**B2: Hoặc làm thủ công (nếu script không chạy)**

Đọc hướng dẫn chi tiết: **`FIX_POSTGRESQL_PASSWORD.md`**

```powershell
# Mở file để xem hướng dẫn
notepad D:\AInhandanghinhanh\FIX_POSTGRESQL_PASSWORD.md
```

---

### ✅ BƯỚC 2: KHỞI TẠO DATABASE (5 phút)

**Sau khi fix password, chạy:**

```powershell
# 1. Vào thư mục backend
cd D:\AInhandanghinhanh\backend

# 2. Activate virtual environment
.\venv\Scripts\activate

# 3. Khởi tạo database tables
python init_db.py

# Kết quả mong đợi:
# [OK] Database connection successful!
# [OK] All tables created successfully!
# [OK] users
# [OK] recognition_history
# [OK] detected_persons
# ...
```

**✅ Nếu thấy `[OK] DATABASE INITIALIZATION COMPLETE!` → Thành công!**

---

### ✅ BƯỚC 3: CHẠY BACKEND (2 phút)

```powershell
# Vẫn trong thư mục backend với venv activated
cd D:\AInhandanghinhanh\backend
.\venv\Scripts\activate

# Chạy server
python main.py

# Kết quả mong đợi:
# INFO: Started server process
# INFO: Uvicorn running on http://127.0.0.1:8000
```

**✅ MỞ BROWSER:**
- API Docs: http://localhost:8000/docs
- API Info: http://localhost:8000

**⚠️ GIỮ TERMINAL NÀY CHẠY!** Mở terminal mới cho Frontend.

---

### ✅ BƯỚC 4: CHẠY FRONTEND (5 phút)

**MỞ TERMINAL MỚI (Giữ backend chạy ở terminal cũ)**

```powershell
# 1. Vào thư mục frontend
cd D:\AInhandanghinhanh\frontend

# 2. Kiểm tra Flutter
flutter doctor

# 3. Cài dependencies (chỉ lần đầu)
flutter pub get

# 4. Kiểm tra thiết bị
flutter devices

# Nếu không có device:
# - Web: flutter run -d chrome (không cần điện thoại!)
# - Emulator: Mở Android Studio → AVD Manager → Start emulator
# - Điện thoại: Cắm USB + Bật USB Debugging
```

**Chạy app:**

```powershell
# OPTION 1: Chạy trên Web (NHANH NHẤT - không cần điện thoại/emulator)
flutter run -d chrome

# OPTION 2: Chạy trên thiết bị/emulator đã kết nối
flutter run

# OPTION 3: Chỉ định thiết bị cụ thể
flutter run -d <device-id>
```

**✅ App sẽ tự động mở!** 🎉

---

## 📋 CHECKLIST TỔNG HỢP

### Backend
- [ ] ✅ PostgreSQL đang chạy
- [ ] ✅ Database `nhandanghinhanh` đã tạo
- [ ] ❌ **File `.env` có password ĐÚNG** ← CẦN FIX!
- [ ] ⏳ Chạy `python init_db.py` thành công
- [ ] ⏳ Chạy `python main.py` → Server running
- [ ] ⏳ http://localhost:8000/docs → Swagger UI hiển thị

### Frontend
- [ ] ✅ Flutter đã cài (`flutter --version`)
- [ ] ⏳ Chạy `flutter pub get`
- [ ] ⏳ Có thiết bị/emulator hoặc dùng Web
- [ ] ⏳ Chạy `flutter run` → App khởi động

---

## 🔥 WORKFLOW NHANH (Sau khi fix password)

```powershell
# TERMINAL 1 - Backend
cd D:\AInhandanghinhanh\backend
.\venv\Scripts\activate
python init_db.py      # Chỉ chạy 1 lần đầu
python main.py         # Giữ chạy

# TERMINAL 2 - Frontend (MỞ TERMINAL MỚI)
cd D:\AInhandanghinhanh\frontend
flutter pub get        # Chỉ chạy 1 lần đầu
flutter run -d chrome  # Hoặc flutter run
```

---

## 🆘 NẾU GẶP LỖI

### Lỗi 1: `ModuleNotFoundError: No module named 'fastapi'`

**Giải pháp:**
```powershell
cd D:\AInhandanghinhanh\backend
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

### Lỗi 2: `password authentication failed`

**Giải pháp:** Xem lại **BƯỚC 1** ở trên!

File tham khảo: `FIX_POSTGRESQL_PASSWORD.md`

---

### Lỗi 3: `Port 8000 already in use`

**Giải pháp:**
```powershell
# Tìm process đang dùng port 8000
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F
```

---

### Lỗi 4: Flutter không kết nối Backend

**Kiểm tra:**
1. Backend đang chạy? (http://localhost:8000/docs)
2. API URL đúng trong `frontend\lib\services\api_service.dart`?

**Sửa API URL:**
- Web/iOS Simulator: `http://localhost:8000`
- Android Emulator: `http://10.0.2.2:8000`
- Điện thoại thật: `http://YOUR_LAPTOP_IP:8000`

---

## 📚 TÀI LIỆU THAM KHẢO

| File | Mục Đích | Khi Nào Dùng |
|------|----------|--------------|
| **`BAT_DAU_CHAY_APP.md`** | Hướng dẫn nhanh (FILE NÀY) | Đọc đầu tiên |
| **`FIX_POSTGRESQL_PASSWORD.md`** | Fix lỗi password chi tiết | Khi gặp lỗi authentication |
| **`RESET_POSTGRESQL_PASSWORD_NHANH.ps1`** | Script reset password | Chạy khi quên password |
| **`HUONG_DAN_CHAY_APP.md`** | Hướng dẫn đầy đủ | Tham khảo chi tiết |
| **`START_HERE.md`** | Quick start | Cấu trúc project |

---

## 🎯 TRẠNG THÁI HIỆN TẠI

```
[✅] Python 3.11.9 installed
[✅] Flutter 3.35.6 installed
[✅] PostgreSQL 18 installed
[✅] Database 'nhandanghinhanh' created
[✅] Virtual environment setup
[✅] Backend code ready
[✅] Frontend code ready
[❌] Database password incorrect ← CẦN FIX NGAY!
[⏳] Database tables not created
[⏳] Backend not running
[⏳] Frontend not running
```

---

## 💡 BẠN ĐANG Ở BƯỚC NÀO?

### Bước Hiện Tại: **FIX PASSWORD POSTGRESQL**

```
Timeline:
[✅] 1. Cài Python
[✅] 2. Cài Flutter
[✅] 3. Cài PostgreSQL
[✅] 4. Tạo database
[❌] 5. Fix password ← BẠN Ở ĐÂY!
[⏳] 6. Khởi tạo tables
[⏳] 7. Chạy Backend
[⏳] 8. Chạy Frontend
[⏳] 9. Test app
```

---

## 🚀 HÀNH ĐỘNG NGAY BÂY GIỜ

### Nếu BẠN NHỚ PASSWORD:

```powershell
# 1. Update .env
cd D:\AInhandanghinhanh\backend
notepad .env
# Sửa dòng DATABASE_URL với password đúng

# 2. Test & Run
.\venv\Scripts\activate
python init_db.py
python main.py
```

### Nếu BẠN QUÊN PASSWORD:

```powershell
# 1. Chạy script reset (với Admin)
cd D:\AInhandanghinhanh
.\RESET_POSTGRESQL_PASSWORD_NHANH.ps1

# 2. Làm theo hướng dẫn của script
```

---

## ⏱️ THỜI GIAN ƯỚC TÍNH (Sau khi fix password)

| Bước | Thời Gian |
|------|-----------|
| Fix password | 2-10 phút |
| Khởi tạo database | 1 phút |
| Chạy backend | 30 giây |
| Chạy frontend | 2-3 phút |
| Test app | 1 phút |
| **TỔNG** | **~7-15 phút** |

---

## 📞 CẦN HỖ TRỢ?

**Gửi kết quả của lệnh này:**

```powershell
# Kiểm tra trạng thái PostgreSQL
Get-Service -Name postgresql* | Format-Table -AutoSize

# Kiểm tra file .env
cd D:\AInhandanghinhanh\backend
Get-Content .env | Select-String "DATABASE"

# Test connection
.\venv\Scripts\activate
python test_postgresql_connection.py
```

Tôi sẽ giúp debug! 🚀

---

**🎊 SAU KHI FIX PASSWORD, MỌI THỨ SẼ CHẠY NHANH THÔI! 🎊**

**Version:** 1.0.0  
**Date:** 26/10/2025  
**Status:** ⚠️ Waiting for Password Fix

