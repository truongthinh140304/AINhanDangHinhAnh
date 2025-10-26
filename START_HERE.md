# 🚀 BẮT ĐẦU TẠI ĐÂY!

## ❌ BẠN VỪA GẶP LỖI?

```
ImportError: cannot import name 'nhan_dang_gioi_tinh_tu_anh'
```

**✅ ĐÃ SỬA XONG!** Làm theo hướng dẫn dưới đây.

---

## 📋 QUICK START - 3 BƯỚC (5 PHÚT)

### BƯỚC 1: Test Module Structure (30 giây)

```bash
cd backend
python test_quick.py
```

**✅ Xem tất cả file đã có đầy đủ chưa**

---

### BƯỚC 2: Cài Dependencies (5 phút)

```bash
pip install -r requirements.txt
```

**⏱️ Có thể mất 5-10 phút (tùy tốc độ mạng)**

**Packages:** fastapi, numpy, opencv, torch, sqlalchemy, etc.

---

### BƯỚC 3: Chạy Backend (30 giây)

```bash
python main.py
```

**✅ Mở browser:** http://localhost:8000/docs

---

## 🎯 WORKFLOW FULL

```
1. Test structure  →  python test_quick.py
2. Cài packages   →  pip install -r requirements.txt
3. Test imports   →  python test_imports.py
4. Chạy server    →  python main.py
5. Test API       →  http://localhost:8000/docs
```

---

## 📚 TÀI LIỆU CHI TIẾT

| File | Mục Đích | Thời Gian |
|------|----------|-----------|
| **`FIX_IMPORT_ERROR.md`** | Fix lỗi import chi tiết | 5 phút |
| **`POSTGRESQL_QUICK_START.txt`** | Setup database | 10 phút |
| **`HUONG_DAN_POSTGRESQL.md`** | Database đầy đủ | 30 phút |
| **`SUMMARY_POSTGRESQL.txt`** | Tổng kết | 2 phút |

---

## 🔥 QUICK COMMANDS

```bash
# Test module structure (không cần cài packages)
cd backend
python test_quick.py

# Cài dependencies
pip install -r requirements.txt

# Test imports (sau khi cài xong)
python test_imports.py

# Khởi tạo database (optional - nếu dùng PostgreSQL)
python init_db.py

# Test database (optional)
python test_db.py

# Chạy server
python main.py
```

---

## ✅ CHECKLIST

### Trước Khi Chạy Backend

- [ ] Python 3.8+ installed
- [ ] Ở trong thư mục `backend`
- [ ] Chạy `python test_quick.py` → OK
- [ ] Chạy `pip install -r requirements.txt` → Done
- [ ] Chạy `python test_imports.py` → All ✅

### Chạy Backend

- [ ] `python main.py`
- [ ] Server started: http://localhost:8000
- [ ] API docs: http://localhost:8000/docs

### Database (Optional - Nếu Muốn Lưu Dữ Liệu)

- [ ] PostgreSQL installed
- [ ] Database created: `nhandanghinhanh`
- [ ] `.env` configured
- [ ] `python init_db.py` → Tables created
- [ ] `python test_db.py` → Connection OK

---

## 🆘 NẾU GẶP VẤN ĐỀ

### Lỗi 1: Import Error

**Đọc:** `FIX_IMPORT_ERROR.md`

### Lỗi 2: Database Connection

**Đọc:** `POSTGRESQL_QUICK_START.txt`

### Lỗi 3: Module Not Found

```bash
pip install -r requirements.txt
# hoặc
pip install fastapi uvicorn numpy opencv-python scikit-learn
```

### Lỗi 4: Port Already in Use

```bash
# Đổi port trong main.py
# hoặc kill process đang dùng port 8000
```

---

## 📁 STRUCTURE TỔNG QUAN

```
D:\AInhandanghinhanh\
├── backend/                    ← BẠN Ở ĐÂY!
│   ├── main.py                ← API server
│   ├── database.py            ← Database config
│   ├── models.py              ← Table schemas
│   ├── requirements.txt       ← Dependencies
│   ├── test_quick.py          ← Test structure
│   ├── test_imports.py        ← Test imports
│   ├── test_db.py             ← Test database
│   ├── init_db.py             ← Init database
│   ├── modules/               ← AI modules
│   │   ├── nhan_dang_gioi_tinh.py  ✅
│   │   ├── nhan_dang_mau_sac.py    ✅
│   │   ├── nhan_dang_thoi_tiet.py  ✅
│   │   └── nhan_dang_vat_dung.py   ✅
│   └── services/
│       └── db_service.py      ← CRUD operations
│
├── frontend/                   ← Flutter app
│
└── Documentation/
    ├── START_HERE.md          ← FILE NÀY!
    ├── FIX_IMPORT_ERROR.md    ← Fix lỗi
    ├── POSTGRESQL_QUICK_START.txt
    ├── HUONG_DAN_POSTGRESQL.md
    └── SUMMARY_POSTGRESQL.txt
```

---

## 🎯 MỤC TIÊU CỦA DỰ ÁN

**Ứng Dụng Nhận Dạng Đối Tượng**

- ✅ **Flutter Frontend** - Mobile app
- ✅ **FastAPI Backend** - REST API
- ✅ **PostgreSQL Database** - Lưu trữ dữ liệu
- ✅ **AI/ML** - YOLOv8, Computer Vision

**Tính năng:**
- Upload ảnh → Nhận dạng người, giới tính, màu áo
- Phân tích thời tiết, nhận dạng vật dụng
- Lưu lịch sử vào database
- Xem thống kê

---

## 💡 TIPS

### Virtual Environment (Recommended)

```bash
# Tạo venv
python -m venv venv

# Activate
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

# Cài packages
pip install -r requirements.txt
```

### Skip Heavy Packages (For Quick Testing)

```bash
# Nếu không cần YOLO ngay (torch rất nặng ~2GB)
pip install fastapi uvicorn numpy opencv-python scikit-learn sqlalchemy psycopg2-binary python-dotenv pydantic aiofiles
```

### Check Python Version

```bash
python --version   # Cần >= 3.8
```

---

## 🎊 KẾT QUẢ MONG ĐỢI

**Sau khi hoàn thành 3 bước:**

```bash
$ python main.py

INFO:     Started server process
INFO:     Waiting for application startup.
🔌 Connecting to database...
✅ Database connected successfully!
📊 Tables: users, recognition_history, detected_persons, ...
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

**Mở browser:**
- http://localhost:8000 → API info
- http://localhost:8000/docs → Swagger UI (interactive API docs)
- http://localhost:8000/redoc → ReDoc (alternative docs)

**Test API:**
- POST `/api/recognize` → Upload ảnh
- GET `/api/history` → Xem lịch sử
- GET `/api/statistics` → Thống kê

---

## 📞 HỖ TRỢ

**Lỗi thường gặp:**
1. Import error → Đọc `FIX_IMPORT_ERROR.md`
2. Database error → Đọc `POSTGRESQL_QUICK_START.txt`
3. Module not found → `pip install -r requirements.txt`
4. Port in use → Đổi port hoặc kill process

**Files hỗ trợ:**
- `FIX_IMPORT_ERROR.md` - Fix lỗi import
- `POSTGRESQL_QUICK_START.txt` - Setup database nhanh
- `HUONG_DAN_POSTGRESQL.md` - Hướng dẫn database đầy đủ

---

**🚀 CHÚC BẠN THÀNH CÔNG! 🚀**

**Next:** Sau khi backend chạy OK → Setup database (optional) → Connect Flutter app

**Version:** 1.0.0  
**Date:** 26/10/2025  
**Status:** ✅ Ready to Run!
