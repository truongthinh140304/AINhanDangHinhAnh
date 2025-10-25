# 🚀 BẮT ĐẦU TẠI ĐÂY - START HERE

## 👋 Chào Mừng!

Đây là dự án **Full-Stack Application** - Ứng dụng nhận dạng đối tượng trên ảnh.

**Kiến trúc:** `Flutter Mobile App` + `Python FastAPI Backend` + `PostgreSQL Database`

---

## 📁 Cấu Trúc Dự Án

```
AInhandanghinhanh/
│
├── 📱 frontend/              ← Flutter mobile app (Android/iOS)
│   ├── lib/                 ← Source code Dart
│   ├── pubspec.yaml         ← Dependencies
│   └── README.md            ← Hướng dẫn frontend
│
├── 🐍 backend/              ← Python FastAPI backend
│   ├── main.py             ← Server chính
│   ├── modules/            ← AI modules
│   ├── requirements.txt    ← Dependencies
│   └── README.md           ← Hướng dẫn backend
│
└── 📚 Tài liệu/             ← Documentation
    ├── README.md           ← Hướng dẫn tổng quan
    ├── HUONG_DAN_FULLSTACK.md  ← Hướng dẫn chi tiết
    ├── ARCHITECTURE.md     ← Kiến trúc hệ thống
    └── ...
```

---

## 🎯 Bạn Muốn Làm Gì?

### 1️⃣ Chạy Ứng Dụng Nhanh (Development)

```bash
# BƯỚC 1: Chạy Backend
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python main.py

# BƯỚC 2: Chạy Frontend (terminal mới)
cd frontend
flutter pub get
flutter run
```

**→ Xem chi tiết:** [HUONG_DAN_FULLSTACK.md](HUONG_DAN_FULLSTACK.md)

---

### 2️⃣ Tìm Hiểu Kiến Trúc

**Kiến trúc đơn giản:**

```
📱 Flutter App  →  🐍 FastAPI  →  🐘 PostgreSQL
   (Mobile)        (REST API)     (Database)
```

**→ Xem chi tiết:** [ARCHITECTURE.md](ARCHITECTURE.md)

---

### 3️⃣ Phát Triển Backend (Python)

```bash
cd backend
# Xem README.md trong thư mục backend/
```

**Files quan trọng:**
- `main.py` - FastAPI server
- `modules/` - AI recognition modules
- `requirements.txt` - Dependencies

**→ Xem chi tiết:** [backend/README.md](backend/README.md)

---

### 4️⃣ Phát Triển Frontend (Flutter)

```bash
cd frontend
# Xem README.md trong thư mục frontend/
```

**Files quan trọng:**
- `lib/main.dart` - Entry point
- `lib/screens/` - UI screens
- `lib/services/api_service.dart` - API client

**→ Xem chi tiết:** [frontend/README.md](frontend/README.md)

---

### 5️⃣ Tìm Hiểu Thuật Toán AI

Dự án sử dụng **YOLOv8** để nhận dạng đối tượng.

**Chức năng:**
- 👤 Nhận dạng người & giới tính (75-95%)
- 🎨 Nhận dạng màu áo (85%)
- ☀️ Nhận dạng thời tiết (80%)
- 🎒 Nhận dạng vật dụng (90%)

**→ Xem chi tiết:** [PHAN_TICH_THUAT_TOAN.md](PHAN_TICH_THUAT_TOAN.md)

---

### 6️⃣ Tìm Hiểu API Reference

**API Endpoints:**
- `POST /api/recognize` - Nhận dạng ảnh
- `GET /api/history` - Lịch sử
- `GET /health` - Health check

**→ Xem chi tiết:** [TAI_LIEU_PHAT_TRIEN.md](TAI_LIEU_PHAT_TRIEN.md)

**→ API Docs:** `http://localhost:8000/docs` (khi backend chạy)

---

### 7️⃣ Deploy Production

**Backend:**
- DigitalOcean / Railway / Heroku
- Setup SSL certificate
- Configure PostgreSQL

**Frontend:**
- Build APK: `flutter build apk --release`
- Upload to Google Play Store / App Store

**→ Xem chi tiết:** [HUONG_DAN_FULLSTACK.md](HUONG_DAN_FULLSTACK.md#deployment)

---

## 📚 Danh Sách Tài Liệu Đầy Đủ

| File | Mô Tả | Đối Tượng |
|------|-------|-----------|
| **README.md** | Tổng quan dự án | Tất cả |
| **START_HERE.md** | File này - Bắt đầu nhanh | Tất cả |
| **HUONG_DAN_FULLSTACK.md** | Hướng dẫn chi tiết từng bước | Developer |
| **ARCHITECTURE.md** | Kiến trúc hệ thống | Developer/Architect |
| **backend/README.md** | Hướng dẫn backend | Backend Dev |
| **frontend/README.md** | Hướng dẫn frontend | Frontend Dev |
| **PHAN_TICH_THUAT_TOAN.md** | So sánh thuật toán | AI/ML Engineer |
| **TAI_LIEU_PHAT_TRIEN.md** | API Reference | Developer |
| **GIOI_THIEU.txt** | Giới thiệu tổng quan | Người dùng |
| **TOM_TAT_DU_AN.md** | Tóm tắt dự án | Quản lý |
| **CHANGELOG.md** | Lịch sử phát triển | Tất cả |

---

## ⚡ Quick Start (TL;DR)

```bash
# 1. Backend
cd backend && python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt && python main.py

# 2. Frontend (terminal mới)
cd frontend && flutter pub get && flutter run

# 3. Mở browser: http://localhost:8000/docs
```

---

## 🆘 Cần Giúp Đỡ?

### Troubleshooting

| Vấn đề | Giải pháp |
|--------|-----------|
| Backend không chạy | Xem [backend/README.md](backend/README.md#troubleshooting) |
| Flutter không build | Xem [frontend/README.md](frontend/README.md#troubleshooting) |
| API connection error | Xem [HUONG_DAN_FULLSTACK.md](HUONG_DAN_FULLSTACK.md#troubleshooting) |
| Database error | Xem [HUONG_DAN_FULLSTACK.md](HUONG_DAN_FULLSTACK.md#database) |

### Support

- 📖 **Docs**: Xem các file .md trong thư mục
- 🐛 **Issues**: GitHub Issues
- 💬 **Email**: dev@example.com

---

## 📊 Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Frontend** | Flutter | 3.0+ |
| **Backend** | Python + FastAPI | 3.8+ / 0.109+ |
| **AI/ML** | YOLOv8 + OpenCV | 8.0+ / 4.8+ |
| **Database** | PostgreSQL | 12+ |
| **State Mgmt** | Provider | 6.1+ |
| **HTTP Client** | Dio | 5.4+ |

---

## 🎓 Học Tập

Dự án này phù hợp cho:

✓ **Sinh viên** học AI/Computer Vision
✓ **Developer** học Flutter + Python
✓ **Researcher** nghiên cứu Object Detection
✓ **Startup** muốn tích hợp AI vào app

---

## 🗺️ Roadmap

### ✅ Phase 1: MVP (Hoàn thành)
- [x] Backend API với YOLOv8
- [x] Flutter UI cơ bản
- [x] Nhận dạng 4 chức năng chính
- [x] Tài liệu đầy đủ

### ⏳ Phase 2: Enhancement (Đang phát triển)
- [ ] PostgreSQL integration
- [ ] Authentication & Authorization
- [ ] History screen
- [ ] Offline mode

### 🔮 Phase 3: Advanced (Tương lai)
- [ ] Real-time video processing
- [ ] Cloud storage (AWS S3)
- [ ] Web dashboard
- [ ] Mobile push notifications

---

## 📝 License

MIT License - Free to use for learning and commercial projects

---

## 🙏 Credits

- **YOLOv8**: Ultralytics
- **Flutter**: Google
- **FastAPI**: Sebastián Ramírez
- **PostgreSQL**: PostgreSQL Global Development Group

---

## 🎉 Bắt Đầu Ngay!

1. **Đọc nhanh:** [README.md](README.md)
2. **Follow guide:** [HUONG_DAN_FULLSTACK.md](HUONG_DAN_FULLSTACK.md)
3. **Start coding:** `cd backend && python main.py`

**Chúc bạn coding vui vẻ! 🚀**

---

**🇻🇳 Made with ❤️ in Vietnam 🇻🇳**

**Version:** 1.0.0

**Last Updated:** 25/10/2025

