# 🚀 SETUP POSTGRESQL - 5 PHÚT

## ⚡ QUICK START (Cho người bận)

### Bước 1: Cài PostgreSQL (10 phút)
```
Download: https://www.postgresql.org/download/windows/
Run installer → Password: postgres → Port: 5432 → Install
```

### Bước 2: Tạo Database (2 phút)
```
pgAdmin 4 → Databases → Create → Name: nhandanghinhanh → Save
```

### Bước 3: Config Backend (1 phút)
```bash
cd backend
ren env_example_copy.txt .env
# Mở .env và sửa password nếu cần
```

### Bước 4: Test (30 giây)
```bash
python test_postgresql_connection.py
```

### Bước 5: Init Database (30 giây)
```bash
python init_db.py
```

### Bước 6: Test Database (30 giây)
```bash
python test_db.py
```

### Bước 7: Chạy Server (30 giây)
```bash
python main.py
```

**✅ XONG! Vào http://localhost:8000/docs để test!**

---

## 📋 CHI TIẾT TỪNG BƯỚC

### BƯỚC 1: CÀI POSTGRESQL

**Windows:**
1. Download: https://www.postgresql.org/download/windows/
2. Chọn PostgreSQL 16 (latest)
3. Chạy file `.exe`
4. Click Next qua các bước
5. **Đặt password:** `postgres` (hoặc password khác nhưng phải nhớ!)
6. Port: `5432` (mặc định)
7. Install
8. Đợi 5-10 phút

**Kiểm tra:**
```bash
psql --version
# Output: psql (PostgreSQL) 16.x
```

---

### BƯỚC 2: TẠO DATABASE

**Cách 1: pgAdmin (Dễ nhất)**
```
1. Start Menu → pgAdmin 4
2. Nhập password: postgres
3. Right-click "Databases"
4. Create → Database
5. Name: nhandanghinhanh
6. Save
✅ Done!
```

**Cách 2: Command Line**
```bash
psql -U postgres
# Nhập password
CREATE DATABASE nhandanghinhanh;
\q
```

---

### BƯỚC 3: CONFIG BACKEND

**Tạo file .env:**
```bash
cd backend
ren env_example_copy.txt .env
```

**Chỉnh sửa .env:**

Mở file `backend/.env` và sửa dòng này:
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/nhandanghinhanh
DB_PASSWORD=YOUR_PASSWORD
```

⚠️ Thay `YOUR_PASSWORD` = password bạn đã đặt ở Bước 1!

---

### BƯỚC 4: TEST CONNECTION

```bash
cd backend
python test_postgresql_connection.py
```

**Kết quả thành công:**
```
🐘 POSTGRESQL CONNECTION TEST
============================================================
✅ psycopg2 imported successfully!
✅ Connection established!
✅ Query executed successfully!
✅ POSTGRESQL CONNECTION TEST: PASSED!
```

**Nếu lỗi:**

| Lỗi | Fix |
|------|-----|
| `psycopg2 not found` | `pip install psycopg2-binary` |
| `password authentication failed` | Kiểm tra password trong .env |
| `database does not exist` | Quay lại Bước 2 |
| `connection refused` | Start PostgreSQL service |

**Start PostgreSQL Service (nếu cần):**
```
Win + R → services.msc → Tìm "postgresql" → Start
```

---

### BƯỚC 5: KHỞI TẠO DATABASE

```bash
cd backend
python init_db.py
```

**Kết quả:**
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
```

---

### BƯỚC 6: TEST DATABASE

```bash
python test_db.py
```

**Kết quả:**
```
🧪 DATABASE TESTS
============================================================
✅ Connection successful!
✅ User CRUD test passed!
✅ Recognition CRUD test passed!
✅ ALL TESTS COMPLETED!
```

---

### BƯỚC 7: CHẠY BACKEND

```bash
python main.py
```

**Kết quả:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Kiểm tra:**
- Mở browser: http://localhost:8000/docs
- Thử endpoint **POST /api/recognize** - Upload ảnh
- Thử endpoint **GET /api/history** - Xem lịch sử
- ✅ Thấy dữ liệu trong history = Thành công!

---

## 🎯 VERIFY THÀNH CÔNG

Checklist:
- [ ] PostgreSQL đã cài và chạy
- [ ] Database `nhandanghinhanh` đã tạo
- [ ] File `.env` đã tạo với đúng password
- [ ] Test connection thành công
- [ ] Tables đã được tạo (6 tables)
- [ ] Test database thành công
- [ ] Backend server chạy
- [ ] API docs hiển thị
- [ ] Upload ảnh thành công
- [ ] Xem history thấy dữ liệu

---

## 📊 CẤU TRÚC DATABASE

**6 Tables:**
```
1. users              → Người dùng
2. recognition_history → Lịch sử nhận dạng ảnh
3. detected_persons   → Người trong ảnh (giới tính, màu áo)
4. detected_objects   → Vật dụng trong ảnh
5. daily_statistics   → Thống kê
6. system_logs        → Logs
```

**Flow:**
```
Upload ảnh → API → Backend xử lý → Lưu vào PostgreSQL
                → Trả kết quả về → Flutter app hiển thị
                
Xem lịch sử → API → Query PostgreSQL → Trả dữ liệu
```

---

## 🔧 XỬ LÝ LỖI

### Lỗi 1: Connection Refused
```
❌ could not connect to server
```
**Fix:**
```bash
# Windows
Win + R → services.msc → postgresql → Start

# Mac
brew services start postgresql

# Linux
sudo systemctl start postgresql
```

### Lỗi 2: Password Failed
```
❌ password authentication failed
```
**Fix:**
- Mở `backend/.env`
- Sửa `DB_PASSWORD=YOUR_ACTUAL_PASSWORD`
- Save và test lại

### Lỗi 3: Database Not Exist
```
❌ database "nhandanghinhanh" does not exist
```
**Fix:**
```bash
psql -U postgres
CREATE DATABASE nhandanghinhanh;
\q
```

### Lỗi 4: psycopg2 Not Found
```
❌ No module named 'psycopg2'
```
**Fix:**
```bash
pip install psycopg2-binary
```

### Lỗi 5: Tables Not Exist
```
❌ relation "users" does not exist
```
**Fix:**
```bash
cd backend
python init_db.py
```

---

## 💡 COMMANDS HỮU ÍCH

```bash
# Test connection nhanh
cd backend
python test_postgresql_connection.py

# Tạo tables
python init_db.py

# Test CRUD operations
python test_db.py

# Chạy server
python main.py

# Reset database (XÓA TẤT CẢ - cẩn thận!)
python init_db.py --reset

# Kiểm tra PostgreSQL version
psql --version

# Connect vào database
psql -U postgres -d nhandanghinhanh

# Xem tất cả tables
psql -U postgres -d nhandanghinhanh -c "\dt"

# Xem dữ liệu trong table
psql -U postgres -d nhandanghinhanh -c "SELECT * FROM recognition_history;"
```

---

## 📖 FILES QUAN TRỌNG

```
backend/
├── .env                          ← Config (tạo từ env_example_copy.txt)
├── env_example_copy.txt          ← Template config
├── database.py                   ← Database setup
├── models.py                     ← Database schema (tables)
├── init_db.py                    ← Script tạo tables
├── test_db.py                    ← Script test database
├── test_postgresql_connection.py ← Script test connection nhanh
└── main.py                       ← Backend server

Docs:
├── POSTGRESQL_QUICK_START.txt    ← Hướng dẫn nhanh 5 phút
├── POSTGRESQL_NHANH.md           ← File này
├── POSTGRESQL_SETUP_CHECKLIST.md ← Checklist chi tiết
├── HUONG_DAN_POSTGRESQL.md       ← Hướng dẫn đầy đủ
└── SUMMARY_POSTGRESQL.txt        ← Tóm tắt
```

---

## 🚀 WORKFLOW HÀNG NGÀY

### Morning Routine:
```bash
# 1. Check PostgreSQL
services.msc → postgresql → Running ✅

# 2. Start backend
cd backend
python main.py

# 3. Verify
http://localhost:8000/docs → API working ✅
```

### Development:
```bash
# Upload ảnh → Check history
POST /api/recognize     → Upload
GET /api/history        → Verify data saved

# Check database
pgAdmin 4 → nhandanghinhanh → Tables → View data
```

### Troubleshooting:
```bash
# Connection issues
python test_postgresql_connection.py

# Database issues
python test_db.py

# Reset everything
python init_db.py --reset
```

---

## 🎉 KẾT QUẢ SAU KHI HOÀN THÀNH

✅ PostgreSQL server chạy  
✅ Database `nhandanghinhanh` sẵn sàng  
✅ 6 tables được tạo  
✅ Backend kết nối thành công  
✅ API lưu dữ liệu vào database  
✅ Có thể xem lịch sử nhận dạng  
✅ Có thể query và phân tích dữ liệu  

**Giờ bạn có thể:**
- Upload ảnh qua API
- Xem lịch sử trong `/api/history`
- Query dữ liệu trong pgAdmin
- Phân tích thống kê
- Backup/restore database

---

## 📞 SUPPORT

**Nếu gặp vấn đề:**
1. Đọc phần "XỬ LÝ LỖI" ở trên
2. Chạy `python test_postgresql_connection.py`
3. Kiểm tra error message
4. Google error message + "postgresql"
5. Check PostgreSQL logs

**Files hỗ trợ:**
- `POSTGRESQL_QUICK_START.txt` - Quick guide
- `HUONG_DAN_POSTGRESQL.md` - Detailed guide
- `POSTGRESQL_SETUP_CHECKLIST.md` - Step-by-step checklist

---

**Version:** 1.0.0  
**Last Updated:** 26/10/2025  
**Total Setup Time:** ~15 phút  
**Status:** ✅ Production Ready

---

🎉 **SETUP THÀNH CÔNG - BẮT ĐẦU CODE NGAY!** 🎉

