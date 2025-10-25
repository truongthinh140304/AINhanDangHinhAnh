# ⚡ QUICK REFERENCE - Tham Khảo Nhanh

## 🚀 Chạy Dự Án (1 Phút)

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Server:** http://localhost:8000

### Frontend

```bash
cd frontend
flutter pub get
flutter run
```

---

## 📁 Cấu Trúc Files

```
📦 AInhandanghinhanh/
├─📱 frontend/          ← Flutter mobile app
│  ├─lib/
│  │ ├─main.dart       ← Entry point
│  │ ├─screens/        ← UI screens
│  │ ├─services/       ← API client
│  │ ├─models/         ← Data models
│  │ └─providers/      ← State management
│  ├─pubspec.yaml      ← Dependencies
│  └─README.md
│
├─🐍 backend/          ← Python API server
│  ├─main.py           ← FastAPI server
│  ├─modules/          ← AI modules
│  │ ├─nhan_dang_gioi_tinh.py
│  │ ├─nhan_dang_mau_sac.py
│  │ ├─nhan_dang_thoi_tiet.py
│  │ └─nhan_dang_vat_dung.py
│  ├─utils/            ← Utilities
│  ├─requirements.txt  ← Dependencies
│  └─README.md
│
└─📚 Docs/             ← Documentation
   ├─README.md         ← Tổng quan
   ├─START_HERE.md     ← Bắt đầu
   ├─HUONG_DAN_FULLSTACK.md
   ├─ARCHITECTURE.md
   └─...
```

---

## 🔌 API Endpoints

| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/` | GET | Root |
| `/health` | GET | Health check |
| `/api/recognize` | POST | Nhận dạng ảnh |
| `/api/history` | GET | Lịch sử (TODO) |
| `/docs` | GET | Swagger UI |

### Test API

```bash
# Health check
curl http://localhost:8000/health

# Nhận dạng ảnh
curl -X POST "http://localhost:8000/api/recognize" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@image.jpg"
```

---

## 📱 Flutter Commands

```bash
# Cài dependencies
flutter pub get

# Chạy app
flutter run

# List devices
flutter devices

# Build APK (Android)
flutter build apk --release

# Build iOS (macOS only)
flutter build ios --release

# Clean
flutter clean

# Doctor (check setup)
flutter doctor
```

---

## 🐍 Python Commands

```bash
# Tạo virtual environment
python -m venv venv

# Activate venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

# Cài packages
pip install -r requirements.txt

# Chạy server
python main.py

# hoặc với uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🗄️ PostgreSQL Commands

```bash
# Login PostgreSQL
psql -U postgres

# Tạo database
CREATE DATABASE nhan_dang_db;

# Kết nối database
\c nhan_dang_db

# List tables
\dt

# Describe table
\d table_name

# Thoát
\q
```

---

## 🔧 Troubleshooting Quick Fix

### Backend: Port đã được sử dụng

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

### Flutter: Không tìm thấy devices

```bash
# Android
flutter doctor --android-licenses

# iOS (macOS)
open -a Simulator

# Check devices
flutter devices
```

### Backend: Module not found

```bash
# Kiểm tra venv
which python      # Linux/Mac
where python      # Windows

# Reinstall
pip install -r requirements.txt
```

### Frontend: API connection refused

**Đổi URL trong `lib/main.dart`:**

```dart
// Android Emulator
baseUrl: 'http://10.0.2.2:8000'

// iOS Simulator
baseUrl: 'http://localhost:8000'

// Real Device (cùng WiFi)
baseUrl: 'http://192.168.x.x:8000'  // IP máy tính
```

---

## 📊 Database Schema

```sql
-- users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- transactions
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    transaction_id UUID UNIQUE,
    user_id INTEGER REFERENCES users(id),
    image_url TEXT,
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

-- recognition_results
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

---

## 🔥 Git Commands

```bash
# Clone
git clone <repo-url>

# Status
git status

# Add files
git add .

# Commit
git commit -m "message"

# Push
git push origin main

# Pull
git pull

# Branch
git checkout -b feature-name
```

---

## 📦 Build & Deploy

### Backend Deploy (Railway)

```bash
# 1. Cài Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Init project
railway init

# 4. Deploy
railway up
```

### Frontend Build

```bash
# Android APK
flutter build apk --release
# Output: build/app/outputs/flutter-apk/app-release.apk

# Android App Bundle (Play Store)
flutter build appbundle --release
# Output: build/app/outputs/bundle/release/app-release.aab

# iOS (cần Mac + Xcode)
flutter build ios --release
```

---

## 🌐 Environment Variables

### Backend (.env)

```env
# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
```

### Flutter (lib/config.dart)

```dart
class Config {
  static const String apiBaseUrl = 'http://localhost:8000';
  static const String apiVersion = 'v1';
  static const int timeout = 30; // seconds
}
```

---

## 📊 Performance Tips

### Backend

```python
# Cache model (đừng load mỗi lần)
model = YOLO('yolov8n.pt')  # Load 1 lần

# Resize ảnh trước khi xử lý
max_size = 1920
if width > max_size or height > max_size:
    image = resize(image, max_size)

# Dùng GPU nếu có
device = 'cuda' if torch.cuda.is_available() else 'cpu'
```

### Frontend

```dart
// Compress ảnh trước upload
final compressed = await FlutterImageCompress.compressWithFile(
  file.path,
  quality: 85,
  minWidth: 1920,
  minHeight: 1080,
);

// Cache ảnh
CachedNetworkImage(
  imageUrl: url,
  placeholder: (context, url) => CircularProgressIndicator(),
);
```

---

## 🎨 UI Colors

```dart
// Flutter theme colors
primaryColor: Colors.blue[700]      // #1976D2
secondaryColor: Colors.green[700]   // #388E3C
errorColor: Colors.red[700]         // #D32F2F
backgroundColor: Colors.grey[100]   // #F5F5F5

// Status colors
success: Colors.green[600]          // #43A047
warning: Colors.orange[600]         // #FB8C00
info: Colors.blue[600]              // #1E88E5
```

---

## 📚 Useful Links

| Resource | URL |
|----------|-----|
| **Flutter Docs** | https://flutter.dev/docs |
| **FastAPI Docs** | https://fastapi.tiangolo.com |
| **YOLOv8 Docs** | https://docs.ultralytics.com |
| **PostgreSQL Docs** | https://www.postgresql.org/docs |
| **Dio Package** | https://pub.dev/packages/dio |
| **Provider Package** | https://pub.dev/packages/provider |

---

## 🔍 Debug Tools

### Backend

```python
# Print debug info
import logging
logging.basicConfig(level=logging.DEBUG)

# FastAPI debug mode
uvicorn main:app --reload --log-level debug

# Check CUDA
import torch
print(torch.cuda.is_available())
```

### Frontend

```dart
// Print debug
print('Debug: $variable');

// DevTools
flutter run --observatory-port=8888

// Logs
flutter logs
```

---

## 📝 Testing

### Backend

```bash
# Install pytest
pip install pytest

# Run tests
pytest

# With coverage
pytest --cov=.
```

### Frontend

```bash
# Run tests
flutter test

# Integration tests
flutter drive --target=test_driver/app.dart
```

---

## 🎯 Checklist

### Before Development

- [ ] Python 3.8+ installed
- [ ] Flutter 3.0+ installed
- [ ] Android Studio / Xcode setup
- [ ] Git installed
- [ ] Code editor (VS Code)

### Before Commit

- [ ] Code formatted
- [ ] No linter errors
- [ ] Tests passed
- [ ] Documentation updated

### Before Deploy

- [ ] Environment variables set
- [ ] Database migrated
- [ ] SSL certificate installed
- [ ] Backups configured
- [ ] Monitoring setup

---

**⚡ Quick Reference v1.0**

**Last Updated:** 25/10/2025

**🚀 Happy Coding!**

