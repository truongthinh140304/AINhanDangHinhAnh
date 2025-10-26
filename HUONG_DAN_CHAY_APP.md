# 🚀 HƯỚNG DẪN CHẠY BACKEND VÀ FRONTEND

---

## 📋 MỤC LỤC

1. [KIỂM TRA TRƯỚC KHI CHẠY](#kiểm-tra-trước-khi-chạy)
2. [CHẠY BACKEND (FastAPI)](#chạy-backend-fastapi)
3. [CHẠY FRONTEND (Flutter)](#chạy-frontend-flutter)
4. [KIỂM TRA KẾT NỐI](#kiểm-tra-kết-nối)
5. [XỬ LÝ LỖI THƯỜNG GẶP](#xử-lý-lỗi-thường-gặp)

---

## ✅ KIỂM TRA TRƯỚC KHI CHẠY

### 1. Kiểm tra các công cụ đã cài

```powershell
# Python
python --version
# Output mong đợi: Python 3.11.9

# Pip
pip --version
# Output mong đợi: pip 25.2

# Flutter
flutter --version
# Output mong đợi: Flutter 3.35.6

# PostgreSQL (nếu đã thêm vào PATH)
psql --version
# Output mong đợi: psql (PostgreSQL) 18.0
```

### 2. Kiểm tra Database

```powershell
# Kết nối database
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -l

# Phải thấy database "nhandanghinhanh" trong danh sách
```

### 3. Kiểm tra Virtual Environment

```powershell
cd D:\AInhandanghinhanh\backend

# Activate venv (nếu chưa)
.\venv\Scripts\activate

# Kiểm tra packages
pip list | Select-String "fastapi|uvicorn|sqlalchemy"
```

---

## 🔥 CHẠY BACKEND (FastAPI)

### CÁCH 1: Dùng Virtual Environment (KHUYẾN NGHỊ)

```powershell
# 1. Mở PowerShell/Terminal
cd D:\AInhandanghinhanh\backend

# 2. Activate virtual environment
.\venv\Scripts\activate

# 3. Kiểm tra .env file
Get-Content .env | Select-String "DATABASE_URL"
# Phải thấy: DATABASE_URL=postgresql://postgres:postgres@localhost:5432/nhandanghinhanh

# 4. Khởi tạo database tables (chỉ chạy 1 lần đầu)
python init_db.py

# 5. Test kết nối database
python test_db.py

# 6. Chạy server
python main.py
```

**✅ Kết quả mong đợi:**

```
INFO:     Started server process
INFO:     Waiting for application startup.
🔌 Connecting to database...
✅ Database connected successfully!
📊 Tables: users, recognition_history, detected_persons, ...
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

**🌐 Mở browser để test:**

- API Docs (Swagger UI): http://localhost:8000/docs
- API Docs (ReDoc): http://localhost:8000/redoc
- API Info: http://localhost:8000

---

### CÁCH 2: Không Dùng Virtual Environment

```powershell
# 1. Đi đến thư mục backend
cd D:\AInhandanghinhanh\backend

# 2. Chạy trực tiếp
python main.py
```

⚠️ **Lưu ý:** Phải đảm bảo đã cài đầy đủ packages:

```powershell
pip install -r requirements.txt
```

---

## 📱 CHẠY FRONTEND (Flutter)

### BƯỚC 1: Chuẩn bị

```powershell
# 1. Mở PowerShell/Terminal MỚI (giữ backend chạy ở terminal cũ)
cd D:\AInhandanghinhanh\frontend

# 2. Kiểm tra Flutter
flutter doctor

# 3. Cài dependencies
flutter pub get
```

---

### BƯỚC 2: Kết nối thiết bị

#### OPTION A: Chạy trên điện thoại thật (Android)

```powershell
# 1. Cắm dây USB từ điện thoại vào laptop
# 2. Bật USB Debugging trên điện thoại
#    Settings → About Phone → Tap "Build Number" 7 lần
#    Settings → Developer Options → USB Debugging (BẬT)

# 3. Kiểm tra kết nối
flutter devices

# Output mong đợi:
# Android SDK built for x86 (mobile) • emulator-5554 • android-x86 • Android 11 (API 30)
# SM G973F (mobile) • 1234567890ABCDEF • android-arm64 • Android 12 (API 31)
```

#### OPTION B: Chạy trên Emulator (Android Studio)

```powershell
# 1. Mở Android Studio
# 2. Tools → AVD Manager → Create Virtual Device
# 3. Chọn device (ví dụ: Pixel 5) → Next → Download image → Finish
# 4. Nhấn Play ▶️ để start emulator

# 5. Kiểm tra
flutter devices
```

#### OPTION C: Chạy trên trình duyệt (Web) - NHANH NHẤT

```powershell
# Không cần điện thoại hay emulator!
flutter run -d chrome
```

---

### BƯỚC 3: Cấu hình API Endpoint

**Mở file:** `D:\AInhandanghinhanh\frontend\lib\services\api_service.dart`

**Kiểm tra dòng:**

```dart
static const String baseUrl = 'http://10.0.2.2:8000';  // Cho Android emulator
// hoặc
static const String baseUrl = 'http://localhost:8000'; // Cho web/iOS
```

**Thay đổi theo thiết bị:**

| Thiết bị | Base URL |
|----------|----------|
| Android Emulator | `http://10.0.2.2:8000` |
| iOS Simulator | `http://localhost:8000` |
| Web Browser | `http://localhost:8000` |
| Điện thoại thật (qua WiFi) | `http://YOUR_LAPTOP_IP:8000` |

**Tìm IP của laptop (nếu dùng điện thoại thật):**

```powershell
ipconfig
# Tìm IPv4 Address trong mục "Wireless LAN adapter Wi-Fi"
# Ví dụ: 192.168.1.100
```

---

### BƯỚC 4: Chạy App

```powershell
# Chạy trên thiết bị/emulator đang kết nối
flutter run

# Hoặc chỉ định thiết bị cụ thể
flutter run -d chrome           # Web
flutter run -d emulator-5554    # Emulator
flutter run -d YOUR_DEVICE_ID   # Điện thoại thật
```

**✅ Kết quả mong đợi:**

```
Launching lib\main.dart on Chrome in debug mode...
Building application for the web...
Waiting for connection from debug service on Chrome...
Debug service listening on ws://127.0.0.1:xxxxx/
```

**App sẽ tự động mở!** 🎉

---

## 🔗 KIỂM TRA KẾT NỐI

### Test Backend → Database

```powershell
cd D:\AInhandanghinhanh\backend
.\venv\Scripts\activate
python test_postgresql_connection.py
```

**Kết quả OK:**

```
✅ PostgreSQL connection successful!
Database: nhandanghinhanh
Tables: users, recognition_history, ...
```

---

### Test Frontend → Backend

**Trong Flutter app:**

1. Nhấn "Upload Image" (hoặc nút chụp ảnh)
2. Chọn một ảnh bất kỳ
3. Xem kết quả nhận dạng

**Nếu kết nối OK:**
- Ảnh được upload thành công
- Hiển thị kết quả: giới tính, màu áo, vật dụng,...

**Nếu lỗi:**
- Xem [XỬ LÝ LỖI THƯỜNG GẶP](#xử-lý-lỗi-thường-gặp)

---

### Test API bằng Browser

**Mở Swagger UI:** http://localhost:8000/docs

1. Click endpoint **POST `/api/recognize`**
2. Click "Try it out"
3. Upload một ảnh
4. Click "Execute"
5. Xem response

**Response mẫu:**

```json
{
  "success": true,
  "gender": "male",
  "gender_confidence": 0.85,
  "clothing_color": "blue",
  "detected_objects": ["person", "phone", "backpack"],
  "weather_info": {
    "season": "summer",
    "time_of_day": "afternoon"
  }
}
```

---

## ⚡ WORKFLOW NHANH (TÓM TẮT)

### TERMINAL 1 - Backend

```powershell
cd D:\AInhandanghinhanh\backend
.\venv\Scripts\activate
python init_db.py      # Chỉ chạy 1 lần đầu
python main.py         # Chạy server
```

**Giữ terminal này chạy!** ✅

---

### TERMINAL 2 - Frontend

```powershell
cd D:\AInhandanghinhanh\frontend
flutter pub get        # Chỉ chạy 1 lần đầu
flutter run -d chrome  # Chạy trên web (nhanh nhất)
# hoặc
flutter run            # Chạy trên thiết bị/emulator
```

---

## 🆘 XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi 1: `ModuleNotFoundError: No module named 'fastapi'`

**Nguyên nhân:** Chưa cài packages hoặc chưa activate venv

**Giải pháp:**

```powershell
cd D:\AInhandanghinhanh\backend
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

### Lỗi 2: `sqlalchemy.exc.OperationalError: could not connect to server`

**Nguyên nhân:** PostgreSQL chưa chạy hoặc sai thông tin kết nối

**Giải pháp:**

```powershell
# 1. Kiểm tra PostgreSQL đang chạy
Get-Service -Name postgresql*

# 2. Nếu stopped, start nó
Start-Service -Name postgresql-x64-18  # Thay x64-18 bằng tên đúng

# 3. Kiểm tra .env
cd D:\AInhandanghinhanh\backend
Get-Content .env | Select-String "DATABASE_URL"

# 4. Test connection
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d nhandanghinhanh -c "SELECT 1;"
```

---

### Lỗi 3: `Address already in use` (Port 8000 đã dùng)

**Nguyên nhân:** Đã có process khác chạy trên port 8000

**Giải pháp:**

```powershell
# Tìm process đang dùng port 8000
netstat -ano | findstr :8000

# Kill process (thay PID bằng số thực tế)
taskkill /PID <PID> /F

# Hoặc đổi port trong main.py (dòng cuối):
# uvicorn.run(app, host="0.0.0.0", port=8001)  # Đổi 8000 → 8001
```

---

### Lỗi 4: Flutter `DioError [DioErrorType.connectTimeout]`

**Nguyên nhân:** Frontend không kết nối được Backend

**Giải pháp:**

**1. Kiểm tra Backend đang chạy:**

```powershell
# Mở http://localhost:8000 trên browser
# Phải thấy: {"message": "API is running"}
```

**2. Kiểm tra API URL trong Flutter:**

Mở `frontend\lib\services\api_service.dart`:

```dart
// Đảm bảo đúng URL:
static const String baseUrl = 'http://localhost:8000';      // Web/iOS
static const String baseUrl = 'http://10.0.2.2:8000';       // Android emulator
static const String baseUrl = 'http://192.168.1.100:8000';  // Điện thoại thật
```

**3. Test connection từ thiết bị:**

- **Web:** Mở http://localhost:8000/docs trên browser
- **Android emulator:** Mở http://10.0.2.2:8000/docs
- **Điện thoại thật:** Mở http://YOUR_LAPTOP_IP:8000/docs trên điện thoại

---

### Lỗi 5: `flutter: FormatException: Unexpected character`

**Nguyên nhân:** Backend trả về HTML thay vì JSON (thường do sai URL)

**Giải pháp:**

```powershell
# Test API endpoint
curl http://localhost:8000/api/health

# Kết quả đúng (JSON):
{"status":"ok","database":"connected"}

# Kết quả sai (HTML):
<!DOCTYPE html>...
```

Sửa URL trong `api_service.dart`:

```dart
// SAI (thiếu /api/)
static const String recognizeUrl = '/recognize';

// ĐÚNG
static const String recognizeUrl = '/api/recognize';
```

---

### Lỗi 6: `No connected devices!`

**Nguyên nhân:** Không có thiết bị/emulator nào kết nối

**Giải pháp:**

```powershell
# Kiểm tra devices
flutter devices

# Nếu không có device nào:
# OPTION 1: Chạy trên web (không cần thiết bị)
flutter run -d chrome

# OPTION 2: Start emulator
flutter emulators
flutter emulators --launch <emulator_id>

# OPTION 3: Cắm điện thoại + bật USB Debugging
```

---

### Lỗi 7: Database tables không tồn tại

**Nguyên nhân:** Chưa chạy `init_db.py`

**Giải pháp:**

```powershell
cd D:\AInhandanghinhanh\backend
.\venv\Scripts\activate
python init_db.py

# Output mong đợi:
# ✅ All tables created successfully!
# Tables: users, recognition_history, detected_persons, ...
```

---

## 🎯 CHECKLIST HOÀN CHỈNH

### Backend

- [ ] PostgreSQL đang chạy
- [ ] Database `nhandanghinhanh` đã tạo
- [ ] File `.env` đã cấu hình đúng
- [ ] Virtual environment activated (`.\venv\Scripts\activate`)
- [ ] Đã chạy `python init_db.py`
- [ ] `python test_db.py` → ✅ OK
- [ ] `python main.py` → Server đang chạy
- [ ] http://localhost:8000/docs → Swagger UI hiển thị

### Frontend

- [ ] `flutter doctor` → Không có lỗi nghiêm trọng
- [ ] `flutter pub get` → Done
- [ ] Thiết bị/emulator đã kết nối (`flutter devices`)
- [ ] API URL trong `api_service.dart` đúng
- [ ] Backend đang chạy
- [ ] `flutter run` → App khởi động thành công

---

## 📞 CẦN HỖ TRỢ?

**Các lệnh hữu ích:**

```powershell
# Kiểm tra trạng thái tổng quát
cd D:\AInhandanghinhanh
.\check_system.ps1

# Xem log backend
cd backend
Get-Content logs\app.log -Tail 50

# Xem log Flutter
flutter run --verbose

# Kill tất cả process Python (nếu cần)
Get-Process python | Stop-Process -Force

# Reset Flutter cache
flutter clean
flutter pub get
```

---

## 🎊 KẾT QUẢ CUỐI CÙNG

**Khi mọi thứ chạy OK:**

1. ✅ **Backend:** Terminal 1 hiển thị `Uvicorn running on http://127.0.0.1:8000`
2. ✅ **Frontend:** Terminal 2 hiển thị `Flutter run key commands...`
3. ✅ **Browser/App:** Ứng dụng hiển thị giao diện
4. ✅ **Upload ảnh:** Nhận được kết quả nhận dạng

**Demo workflow:**

```
[User] → Upload ảnh → [Flutter App]
                          ↓
                    HTTP POST /api/recognize
                          ↓
                    [FastAPI Backend]
                          ↓
                    AI Models (YOLO, CV)
                          ↓
                    [PostgreSQL Database]
                          ↓
                    JSON Response
                          ↓
                    [Flutter App] → Hiển thị kết quả
```

---

**🚀 CHÚC BẠN THÀNH CÔNG! 🚀**

**Version:** 1.0.0  
**Date:** 26/10/2025  
**Author:** AI Assistant  
**Status:** ✅ Production Ready

