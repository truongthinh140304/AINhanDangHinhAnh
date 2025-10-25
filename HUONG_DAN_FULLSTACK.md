# 🚀 HƯỚNG DẪN FULLSTACK - Flutter + Python + PostgreSQL

## 📋 Tổng Quan

Dự án được tách thành 2 phần độc lập:

```
📱 FRONTEND (Flutter)  ←→  🐍 BACKEND (Python FastAPI)  ←→  🐘 DATABASE (PostgreSQL)
    Mobile App              REST API Server                  Data Storage
```

---

## 🎯 BƯỚC 1: CHẠY BACKEND (Python)

### 1.1. Cài Đặt Backend

```bash
# Di chuyển vào thư mục backend
cd backend

# Tạo virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Tạo virtual environment (Linux/Mac)
python3 -m venv venv
source venv/bin/activate

# Cài dependencies (mất 5-10 phút)
pip install -r requirements.txt
```

### 1.2. Chạy Backend Server

```bash
# Trong thư mục backend/
python main.py
```

**Output:**
```
🚀 Backend API Server Started!
📍 Server running at: http://localhost:8000
📖 API Documentation: http://localhost:8000/docs
```

### 1.3. Test Backend

Mở browser, truy cập:
- Health check: `http://localhost:8000/health`
- API docs: `http://localhost:8000/docs`

Hoặc dùng curl:
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-25T..."
}
```

✅ **Backend đã sẵn sàng!**

---

## 📱 BƯỚC 2: CHẠY FRONTEND (Flutter)

### 2.1. Cài Đặt Flutter

**Nếu chưa có Flutter:**

1. Download Flutter: https://flutter.dev/docs/get-started/install
2. Giải nén vào thư mục (VD: `C:\flutter`)
3. Thêm vào PATH: `C:\flutter\bin`
4. Kiểm tra: `flutter doctor`

### 2.2. Cài Dependencies

```bash
# Di chuyển vào thư mục frontend
cd frontend

# Cài packages
flutter pub get
```

### 2.3. Cấu Hình API URL

**QUAN TRỌNG:** Đổi API URL trong `frontend/lib/main.dart`

Mở file `lib/main.dart`, tìm dòng:

```dart
Provider<ApiService>(
  create: (_) => ApiService(baseUrl: 'http://localhost:8000'),
),
```

**Đổi URL theo trường hợp:**

| Trường hợp | URL |
|------------|-----|
| Android Emulator | `http://10.0.2.2:8000` |
| iOS Simulator | `http://localhost:8000` |
| Real Device (cùng WiFi) | `http://YOUR_COMPUTER_IP:8000` |

**Tìm IP máy tính:**

```bash
# Windows
ipconfig
# Tìm "IPv4 Address" (VD: 192.168.1.100)

# Linux/Mac
ifconfig
# Tìm "inet" (VD: 192.168.1.100)
```

### 2.4. Chạy Flutter App

**Option A: Chạy trên Emulator/Simulator**

```bash
# Kiểm tra devices có sẵn
flutter devices

# Chạy app
flutter run
```

**Option B: Chạy trên Real Device**

1. Bật Developer Mode trên điện thoại:
   - **Android**: Settings → About Phone → Build Number (nhấn 7 lần)
   - **iOS**: Xcode → Window → Devices and Simulators

2. Kết nối USB

3. Kiểm tra device:
```bash
flutter devices
```

4. Chạy:
```bash
flutter run
```

**Option C: Build APK**

```bash
# Build release APK
flutter build apk --release

# File output tại:
# build/app/outputs/flutter-apk/app-release.apk

# Cài lên điện thoại Android
```

✅ **Frontend đã chạy!**

---

## 🎬 BƯỚC 3: SỬ DỤNG ỨNG DỤNG

### 3.1. Workflow

```
1. Mở app trên điện thoại
   ↓
2. Nhấn "Chọn Ảnh" hoặc "Chụp Ảnh"
   ↓
3. Chọn/Chụp ảnh
   ↓
4. Nhấn "Nhận Dạng"
   ↓
5. Đợi 1-3 giây
   ↓
6. Xem kết quả chi tiết:
   - Số người
   - Giới tính
   - Màu áo
   - Thời tiết
   - Vật dụng
```

### 3.2. Screenshot Flow

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Home Screen  │ →  │ Select Image │ →  │ Result Screen│
│              │    │              │    │              │
│ [Chọn Ảnh]   │    │ [Preview]    │    │ [Details]    │
│ [Chụp Ảnh]   │    │ [Nhận Dạng]  │    │ [Save/Share] │
└──────────────┘    └──────────────┘    └──────────────┘
```

---

## 🗄️ BƯỚC 4 (OPTIONAL): SETUP DATABASE

**Nếu muốn lưu lịch sử vào PostgreSQL:**

### 4.1. Cài PostgreSQL

**Windows:**
1. Download: https://www.postgresql.org/download/windows/
2. Chạy installer
3. Ghi nhớ password cho user `postgres`

**Linux:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

**Mac:**
```bash
brew install postgresql
```

### 4.2. Tạo Database

```bash
# Mở PostgreSQL shell
psql -U postgres

# Tạo database
CREATE DATABASE nhan_dang_db;

# Tạo user (optional)
CREATE USER your_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE nhan_dang_db TO your_user;

# Thoát
\q
```

### 4.3. Cấu Hình Backend

Tạo file `backend/.env`:

```bash
# Copy file mẫu
cd backend
copy .env.example .env
```

Chỉnh sửa `.env`:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/nhan_dang_db
```

### 4.4. Tạo Tables

```sql
-- Run trong PostgreSQL
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    transaction_id UUID UNIQUE,
    user_id INTEGER REFERENCES users(id),
    image_url TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE recognition_results (
    id SERIAL PRIMARY KEY,
    transaction_id UUID,
    people_count INTEGER,
    genders JSONB,
    colors JSONB,
    weather JSONB,
    objects JSONB,
    processing_time FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

✅ **Database ready!**

---

## 🐛 TROUBLESHOOTING

### ❌ Backend: "ModuleNotFoundError"

```bash
# Kiểm tra virtual environment
which python  # Linux/Mac
where python  # Windows

# Nếu không trong venv, activate:
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Cài lại
pip install -r requirements.txt
```

### ❌ Backend: "Port 8000 already in use"

```bash
# Tìm process đang dùng port 8000
netstat -ano | findstr :8000  # Windows
lsof -i :8000  # Linux/Mac

# Kill process (Windows)
taskkill /PID <PID> /F

# Hoặc đổi port trong main.py:
uvicorn.run("main:app", port=8001)
```

### ❌ Flutter: "Unable to locate Android SDK"

```bash
# Download Android Studio
# https://developer.android.com/studio

# Setup trong Android Studio:
# Tools → SDK Manager → Install SDK

# Flutter config:
flutter config --android-sdk /path/to/android/sdk
```

### ❌ Flutter: "Connection refused" khi gọi API

**Kiểm tra:**

1. Backend đang chạy?
```bash
curl http://localhost:8000/health
```

2. URL đúng chưa?
   - Android emulator: `http://10.0.2.2:8000`
   - Real device: `http://YOUR_IP:8000`

3. Firewall?
```bash
# Windows: Tắt firewall tạm thời
# Settings → Firewall → Turn off
```

4. Cùng WiFi không?
   - Computer và phone phải cùng mạng WiFi

### ❌ Flutter: Camera/Gallery không hoạt động

**Android:**

Thêm vào `android/app/src/main/AndroidManifest.xml`:

```xml
<uses-permission android:name="android.permission.CAMERA"/>
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
```

**iOS:**

Thêm vào `ios/Runner/Info.plist`:

```xml
<key>NSCameraUsageDescription</key>
<string>Cần camera để chụp ảnh</string>
<key>NSPhotoLibraryUsageDescription</key>
<string>Cần truy cập thư viện ảnh</string>
```

Sau đó:
```bash
flutter clean
flutter pub get
flutter run
```

---

## 📊 KIỂM TRA HỆ THỐNG

### ✅ Checklist

**Backend:**
- [ ] Python 3.8+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Server running at :8000
- [ ] Health check returns OK
- [ ] API docs accessible

**Frontend:**
- [ ] Flutter SDK installed
- [ ] flutter doctor all green
- [ ] Dependencies installed (flutter pub get)
- [ ] API URL configured correctly
- [ ] Device connected/emulator running
- [ ] App launches successfully

**Database (Optional):**
- [ ] PostgreSQL installed
- [ ] Database created
- [ ] Tables created
- [ ] Backend can connect

---

## 🎯 WORKFLOW TÓM TẮT

### Development Workflow

```bash
# Terminal 1: Backend
cd backend
venv\Scripts\activate
python main.py

# Terminal 2: Frontend
cd frontend
flutter run

# Browser: API Docs
http://localhost:8000/docs

# Phone: App running
```

### Production Workflow

```bash
# Backend: Deploy to VPS/Cloud
# - DigitalOcean/Railway/Heroku
# - Setup domain + SSL

# Frontend: Build & Publish
flutter build apk --release
# Upload to Google Play Store

flutter build ios --release
# Upload to App Store
```

---

## 📚 TÀI LIỆU THAM KHẢO

| Docs | Link |
|------|------|
| Backend README | [backend/README.md](backend/README.md) |
| Frontend README | [frontend/README.md](frontend/README.md) |
| Phân tích thuật toán | [PHAN_TICH_THUAT_TOAN.md](PHAN_TICH_THUAT_TOAN.md) |
| API Reference | [TAI_LIEU_PHAT_TRIEN.md](TAI_LIEU_PHAT_TRIEN.md) |
| Swagger Docs | http://localhost:8000/docs |

---

## 💡 TIPS & TRICKS

### Performance Tips

1. **Backend:**
   - Dùng GPU nếu có: `CUDA_VISIBLE_DEVICES=0`
   - Resize ảnh trước khi xử lý
   - Cache models

2. **Frontend:**
   - Compress ảnh trước upload
   - Cache kết quả offline
   - Lazy load images

3. **Database:**
   - Index các cột thường query
   - Regular VACUUM
   - Connection pooling

### Development Tips

1. **Hot Reload:**
   - Flutter: Ctrl+S auto reload
   - Backend: `--reload` flag

2. **Debug:**
   - Flutter: DevTools (flutter run --observatory-port)
   - Backend: Print logs, breakpoints

3. **Testing:**
   - Backend: pytest
   - Frontend: flutter test
   - API: Postman/Thunder Client

---

## 🎉 HOÀN THÀNH!

Bạn đã setup thành công Full-Stack Application!

**Next Steps:**
- [ ] Customize UI
- [ ] Add authentication
- [ ] Implement history screen
- [ ] Setup PostgreSQL
- [ ] Deploy to production
- [ ] Publish to app stores

**Chúc bạn coding vui vẻ! 🚀**

---

**Made with ❤️ by Flutter + Python + PostgreSQL**

