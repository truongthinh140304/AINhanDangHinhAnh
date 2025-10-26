# ✅ CHECKLIST SETUP POSTGRESQL

## 📋 CHECKLIST - Làm theo thứ tự

### ☐ BƯỚC 1: Cài đặt PostgreSQL (10 phút)

**Downloads:**
- 🌐 Windows: https://www.postgresql.org/download/windows/
- 🍎 Mac: `brew install postgresql`
- 🐧 Linux: `sudo apt install postgresql postgresql-contrib`

**Cài đặt (Windows):**
```
1. Download PostgreSQL 16 Installer
2. Run file .exe
3. Click Next → Next → Next
4. ĐẶT PASSWORD: postgres (hoặc password khác - NHỚ LẠI!)
5. Port: 5432 (mặc định)
6. Click Next → Install
7. Đợi 5-10 phút
8. ✅ Done!
```

**Kiểm tra:**
```bash
psql --version
# Kết quả: psql (PostgreSQL) 16.x
```

---

### ☐ BƯỚC 2: Tạo Database (2 phút)

**Cách 1: pgAdmin (Dễ nhất ⭐)**
```
1. Start Menu → pgAdmin 4
2. Nhập password: postgres (password bạn đã đặt)
3. Right-click "Databases"
4. Create → Database
5. Database name: nhandanghinhanh
6. Click Save
7. ✅ Done!
```

**Cách 2: Command Line**
```bash
# Mở Command Prompt hoặc PowerShell
psql -U postgres

# Nhập password khi được hỏi

# Tạo database
CREATE DATABASE nhandanghinhanh;

# Kiểm tra
\l

# Thoát
\q
```

---

### ☐ BƯỚC 3: Cấu hình Backend (1 phút)

**Tạo file .env:**
```bash
cd backend
copy .env.example .env
```

**Chỉnh sửa file .env:**

Mở `backend/.env` trong Notepad hoặc VS Code:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/nhandanghinhanh
DB_HOST=localhost
DB_PORT=5432
DB_NAME=nhandanghinhanh
DB_USER=postgres
DB_PASSWORD=YOUR_PASSWORD
```

⚠️ **QUAN TRỌNG:** Thay `YOUR_PASSWORD` bằng password bạn đã đặt!

---

### ☐ BƯỚC 4: Test Connection (30 giây)

```bash
cd backend
python test_postgresql_connection.py
```

**Kết quả mong đợi:**
```
🐘 POSTGRESQL CONNECTION TEST
============================================================
✅ psycopg2 imported successfully!
✅ URL parsed successfully!
✅ Connection established!
✅ Query executed successfully!
✅ POSTGRESQL CONNECTION TEST: PASSED!
```

**Nếu lỗi:**
- ❌ `psycopg2 not found` → `pip install psycopg2-binary`
- ❌ `password authentication failed` → Kiểm tra password trong .env
- ❌ `database does not exist` → Quay lại BƯỚC 2
- ❌ `connection refused` → PostgreSQL chưa chạy (xem BƯỚC 5)

---

### ☐ BƯỚC 5: Khởi động PostgreSQL Service

**Windows:**
```
1. Win + R
2. Gõ: services.msc
3. Enter
4. Tìm: postgresql-x64-16 (hoặc tên tương tự)
5. Right-click → Start
6. Right-click → Properties → Startup type: Automatic
7. ✅ Done!
```

**Mac:**
```bash
brew services start postgresql
```

**Linux:**
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

---

### ☐ BƯỚC 6: Tạo Tables (30 giây)

```bash
cd backend
python init_db.py
```

**Kết quả mong đợi:**
```
🔧 DATABASE INITIALIZATION
============================================================
✅ Database connection OK!
✅ All tables created successfully!

📋 Created tables:
  ✅ users
  ✅ recognition_history
  ✅ detected_persons
  ✅ detected_objects
  ✅ daily_statistics
  ✅ system_logs

✅ DATABASE INITIALIZATION COMPLETE!
```

---

### ☐ BƯỚC 7: Test Database Operations (30 giây)

```bash
cd backend
python test_db.py
```

**Kết quả mong đợi:**
```
🧪 DATABASE TESTS
============================================================
✅ Connection successful!
✅ Created user: testuser (ID: 1)
✅ Found user: test@example.com
✅ User CRUD test passed!

✅ Created recognition record (ID: 1)
✅ Found 1 records in history
✅ Total records in database: 1
✅ Recognition CRUD test passed!

✅ ALL TESTS COMPLETED!
```

---

### ☐ BƯỚC 8: Chạy Backend (30 giây)

```bash
cd backend
python main.py
```

**Kết quả mong đợi:**
```
INFO:     Started server process
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Kiểm tra API:**
- 🌐 http://localhost:8000 - API info
- 📚 http://localhost:8000/docs - Swagger docs

---

### ☐ BƯỚC 9: Test API với Database (1 phút)

**Mở Swagger UI:**
```
http://localhost:8000/docs
```

**Test endpoints:**

1. **POST /api/recognize** - Upload ảnh
   - Click "Try it out"
   - Choose file
   - Execute
   - ✅ Xem response

2. **GET /api/history** - Xem lịch sử
   - Click "Try it out"
   - Execute
   - ✅ Thấy ảnh vừa upload

3. **GET /api/history/{transaction_id}** - Chi tiết
   - Copy transaction_id từ bước 1
   - Paste vào field
   - Execute
   - ✅ Xem chi tiết kết quả

---

### ☐ BƯỚC 10: Xem Database trong pgAdmin (Optional)

```
1. pgAdmin 4
2. Servers → PostgreSQL → Databases → nhandanghinhanh
3. Schemas → public → Tables
4. Right-click table → View/Edit Data → All Rows
5. ✅ Thấy dữ liệu!
```

---

## 🎉 HOÀN THÀNH!

Checklist summary:
- [x] PostgreSQL installed ✅
- [x] Database created ✅
- [x] .env configured ✅
- [x] Connection tested ✅
- [x] Tables created ✅
- [x] CRUD operations tested ✅
- [x] Backend running ✅
- [x] API working ✅

---

## 📊 CẤU TRÚC DATABASE

**Tables:**
```
users                 → Người dùng
recognition_history   → Lịch sử nhận dạng ảnh
detected_persons      → Người được phát hiện (giới tính, màu áo)
detected_objects      → Vật dụng được phát hiện
daily_statistics      → Thống kê theo ngày
system_logs           → Logs hệ thống
```

**Relationships:**
```
User (1) ─────── (Many) RecognitionHistory
RecognitionHistory (1) ─────── (Many) DetectedPerson
RecognitionHistory (1) ─────── (Many) DetectedObject
```

---

## 🔧 TROUBLESHOOTING

### Lỗi 1: `connection refused`
```
❌ Lỗi: could not connect to server
✅ Fix: Start PostgreSQL service (xem BƯỚC 5)
```

### Lỗi 2: `password authentication failed`
```
❌ Lỗi: password authentication failed
✅ Fix: Kiểm tra password trong .env file
```

### Lỗi 3: `database does not exist`
```
❌ Lỗi: database "nhandanghinhanh" does not exist
✅ Fix: Tạo database (xem BƯỚC 2)
```

### Lỗi 4: `psycopg2 not found`
```
❌ Lỗi: No module named 'psycopg2'
✅ Fix: pip install psycopg2-binary
```

### Lỗi 5: `relation does not exist`
```
❌ Lỗi: relation "users" does not exist
✅ Fix: python init_db.py (xem BƯỚC 6)
```

### Lỗi 6: Port 5432 đã được dùng
```
❌ Lỗi: Port 5432 is already in use
✅ Fix 1: Dừng process đang dùng port
✅ Fix 2: Đổi port trong .env (5433, 5434, etc.)
```

---

## 💡 QUICK COMMANDS

```bash
# Test connection
cd backend
python test_postgresql_connection.py

# Init database
python init_db.py

# Test database
python test_db.py

# Run server
python main.py

# Reset database (XÓA TẤT CẢ)
python init_db.py --reset
```

---

## 📖 FILES CÓ ÍCH

```
POSTGRESQL_QUICK_START.txt        ← Hướng dẫn nhanh 5 phút
HUONG_DAN_POSTGRESQL.md           ← Hướng dẫn chi tiết đầy đủ
POSTGRESQL_SETUP_CHECKLIST.md     ← Checklist này
backend/.env.example              ← Template config
backend/database.py               ← Database config
backend/models.py                 ← Database schema
backend/init_db.py                ← Setup script
backend/test_db.py                ← Test script
backend/test_postgresql_connection.py  ← Quick connection test
```

---

## 🚀 WORKFLOW HÀNG NGÀY

```bash
# 1. Kiểm tra PostgreSQL chạy
services.msc → postgresql → Running

# 2. Chạy backend
cd backend
python main.py

# 3. Upload ảnh qua Flutter app hoặc API

# 4. Xem dữ liệu
# - API: http://localhost:8000/api/history
# - pgAdmin: Databases → nhandanghinhanh → Tables
```

---

## 🎯 KẾT QUẢ SAU KHI HOÀN THÀNH

✅ PostgreSQL server chạy  
✅ Database "nhandanghinhanh" được tạo  
✅ 6 tables được tạo và sẵn sàng  
✅ Backend kết nối thành công  
✅ API lưu dữ liệu vào PostgreSQL  
✅ Có thể xem lịch sử nhận dạng  
✅ Có thể query và phân tích dữ liệu  

---

**Version:** 1.0.0  
**Last Updated:** 26/10/2025  
**Status:** ✅ Complete Guide

---

🎉 **CHÚC BẠN SETUP THÀNH CÔNG!** 🎉

