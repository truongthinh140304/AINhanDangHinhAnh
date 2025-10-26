# 🐘 HƯỚNG DẪN CÀI ĐẶT & KẾT NỐI POSTGRESQL

## 📋 MỤC LỤC

1. [Cài Đặt PostgreSQL](#1-cài-đặt-postgresql)
2. [Cấu Hình Database](#2-cấu-hình-database)
3. [Kết Nối Backend](#3-kết-nối-backend)
4. [Chạy Migrations](#4-chạy-migrations)
5. [Test Connection](#5-test-connection)
6. [Troubleshooting](#6-troubleshooting)

---

## 1. CÀI ĐẶT POSTGRESQL

### 🪟 Windows

#### Cách 1: Download Installer (Khuyên Dùng)

1. **Download PostgreSQL:**
   ```
   https://www.postgresql.org/download/windows/
   ```
   - Chọn version mới nhất (PostgreSQL 16)
   - Download installer (.exe)

2. **Chạy Installer:**
   - Double-click file `.exe`
   - Click "Next" → "Next"
   
3. **Chọn Components:**
   - ✅ PostgreSQL Server (BẮT BUỘC)
   - ✅ pgAdmin 4 (Recommended - GUI tool)
   - ✅ Command Line Tools
   - ⬜ Stack Builder (Optional)

4. **Chọn Data Directory:**
   ```
   C:\Program Files\PostgreSQL\16\data
   ```
   (Giữ mặc định)

5. **Đặt Password cho superuser (postgres):**
   ```
   Nhập password: postgres
   (Hoặc password bạn muốn - NHỚ PASSWORD NÀY!)
   ```

6. **Chọn Port:**
   ```
   Port: 5432
   ```
   (Giữ mặc định)

7. **Locale:**
   ```
   Default locale
   ```

8. **Click "Next" → "Install"**

9. **Đợi cài đặt (3-5 phút)**

10. **✅ Hoàn thành!**

#### Cách 2: Chocolatey (Nhanh Hơn)

```powershell
# Mở PowerShell as Administrator
choco install postgresql

# Đặt password
# Mặc định username: postgres, password: postgres
```

#### Kiểm Tra Cài Đặt

```bash
# Mở Command Prompt hoặc PowerShell
psql --version

# Kết quả mong đợi:
# psql (PostgreSQL) 16.x
```

---

## 2. CẤU HÌNH DATABASE

### Bước 1: Tạo Database

#### Cách 1: Dùng pgAdmin 4 (GUI - Dễ Nhất)

1. **Mở pgAdmin 4:**
   - Start Menu → pgAdmin 4

2. **Connect to Server:**
   - Servers → PostgreSQL 16
   - Nhập password bạn đã đặt khi cài

3. **Tạo Database:**
   - Right-click "Databases" → Create → Database
   - **Database name:** `nhandanghinhanh`
   - **Owner:** postgres
   - Click "Save"

4. **✅ Database đã được tạo!**

#### Cách 2: Command Line

```bash
# Mở Command Prompt

# Connect to PostgreSQL
psql -U postgres

# Nhập password khi được hỏi

# Tạo database
CREATE DATABASE nhandanghinhanh;

# Kiểm tra
\l

# Thoát
\q
```

### Bước 2: Tạo User (Optional - Recommended)

```sql
-- Connect to PostgreSQL
psql -U postgres

-- Tạo user mới
CREATE USER aiapp WITH PASSWORD 'your_secure_password';

-- Grant quyền
GRANT ALL PRIVILEGES ON DATABASE nhandanghinhanh TO aiapp;

-- Thoát
\q
```

---

## 3. KẾT NỐI BACKEND

### Bước 1: Tạo File .env

```bash
# Trong thư mục backend/
cd backend

# Tạo file .env (copy từ .env.example)
copy .env.example .env
```

### Bước 2: Cấu Hình Database URL

Mở file `backend/.env` và chỉnh sửa:

```ini
# ============================================
# DATABASE CONFIGURATION
# ============================================

# Format: postgresql://username:password@host:port/database_name

# Option 1: Dùng user postgres (mặc định)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/nhandanghinhanh

# Option 2: Dùng user riêng (nếu đã tạo)
# DATABASE_URL=postgresql://aiapp:your_secure_password@localhost:5432/nhandanghinhanh

DB_HOST=localhost
DB_PORT=5432
DB_NAME=nhandanghinhanh
DB_USER=postgres
DB_PASSWORD=postgres
```

**⚠️ LƯU Ý:**
- Thay `postgres` (sau `//:`) bằng username của bạn
- Thay `postgres` (sau `:`) bằng password của bạn
- Thay `nhandanghinhanh` bằng tên database bạn đã tạo

### Bước 3: Cài Đặt Python Packages

```bash
# Trong thư mục backend/
cd backend

# Activate virtual environment (nếu có)
venv\Scripts\activate

# Cài packages
pip install -r requirements.txt
```

**Packages quan trọng:**
- `psycopg2-binary` - PostgreSQL adapter
- `sqlalchemy` - ORM
- `alembic` - Database migrations

---

## 4. CHẠY MIGRATIONS

### Cách 1: Auto Migration (Khuyên Dùng cho Development)

```bash
cd backend

# Chạy server - sẽ tự động tạo tables
python main.py
```

**Output mong đợi:**
```
============================================================
🚀 Backend API Server Started!
============================================================
📍 Server running at: http://localhost:8000
📖 API Documentation: http://localhost:8000/docs
📊 Alternative docs: http://localhost:8000/redoc
============================================================

🔌 Checking database connection...
✅ Database connection successful!

📦 Creating database tables...
✅ Database tables ready!
============================================================
```

### Cách 2: Manual Migration Script

```bash
cd backend

# Chạy script khởi tạo database
python init_db.py
```

**Output:**
```
============================================================
🔧 DATABASE INITIALIZATION
============================================================

1️⃣ Checking database connection...
✅ Database connection OK!

2️⃣ Creating tables...
✅ All tables created successfully!

📋 Created tables:
  ✅ users
  ✅ recognition_history
  ✅ detected_persons
  ✅ detected_objects
  ✅ daily_statistics
  ✅ system_logs

============================================================
✅ DATABASE INITIALIZATION COMPLETE!
============================================================
```

### Cách 3: Reset Database (Xóa Tất Cả Dữ Liệu)

```bash
cd backend

# ⚠️ CẢNH BÁO: Sẽ XÓA TẤT CẢ DỮ LIỆU!
python init_db.py --reset
```

---

## 5. TEST CONNECTION

### Test 1: Chạy Test Script

```bash
cd backend

# Chạy test database
python test_db.py
```

**Output mong đợi:**
```
============================================================
🧪 DATABASE TESTS
============================================================

🔌 Testing database connection...
✅ Connection successful!

👤 Testing User CRUD...
✅ Created user: testuser (ID: 1)
✅ Found user: test@example.com
✅ User CRUD test passed!

📸 Testing Recognition History CRUD...
✅ Created recognition record (ID: 1)
✅ Found 1 records in history
✅ Total records in database: 1
✅ Recognition CRUD test passed!

============================================================
✅ ALL TESTS COMPLETED!
============================================================
```

### Test 2: Truy Cập API Documentation

```bash
# Chạy server
cd backend
python main.py
```

Mở browser:
```
http://localhost:8000/docs
```

Test các endpoints:
- `POST /api/recognize` - Upload và nhận dạng ảnh
- `GET /api/history` - Xem lịch sử
- `GET /api/statistics` - Xem thống kê
- `DELETE /api/transaction/{id}` - Xóa giao dịch

### Test 3: Kiểm Tra Database Bằng pgAdmin

1. Mở **pgAdmin 4**
2. Connect to **PostgreSQL 16**
3. Databases → `nhandanghinhanh` → Schemas → public → Tables
4. Xem các tables:
   - `users`
   - `recognition_history`
   - `detected_persons`
   - `detected_objects`
   - `daily_statistics`
   - `system_logs`

---

## 6. TROUBLESHOOTING

### ❌ Error: "psycopg2 not installed"

**Giải pháp:**
```bash
pip install psycopg2-binary
```

### ❌ Error: "connection refused"

**Nguyên nhân:** PostgreSQL server không chạy

**Giải pháp:**

#### Windows:
```bash
# Kiểm tra service
services.msc

# Tìm "postgresql-x64-16"
# Right-click → Start

# Hoặc dùng command:
net start postgresql-x64-16
```

#### Linux/Mac:
```bash
# Start PostgreSQL
sudo systemctl start postgresql

# Hoặc
brew services start postgresql
```

### ❌ Error: "password authentication failed"

**Nguyên nhân:** Password sai trong `.env`

**Giải pháp:**

1. Kiểm tra password trong `.env`
2. Reset password nếu quên:

```bash
# Windows: Mở pgAdmin → Right-click server → Properties → Connection
# Đặt lại password

# Hoặc command line:
psql -U postgres
ALTER USER postgres WITH PASSWORD 'new_password';
\q
```

### ❌ Error: "database does not exist"

**Giải pháp:**
```bash
# Tạo database
psql -U postgres
CREATE DATABASE nhandanghinhanh;
\q
```

### ❌ Error: "relation does not exist"

**Nguyên nhân:** Tables chưa được tạo

**Giải pháp:**
```bash
cd backend
python init_db.py
```

### ❌ Port 5432 đã được sử dụng

**Giải pháp:**

1. **Tìm process:**
```bash
netstat -ano | findstr :5432
```

2. **Kill process:**
```bash
taskkill /PID <PID> /F
```

3. **Hoặc đổi port trong PostgreSQL:**
```bash
# File: C:\Program Files\PostgreSQL\16\data\postgresql.conf
port = 5433
```

Sau đó update `.env`:
```ini
DB_PORT=5433
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/nhandanghinhanh
```

### ❌ Too many connections

**Giải pháp:**

Tăng `max_connections` trong `postgresql.conf`:
```ini
# File: C:\Program Files\PostgreSQL\16\data\postgresql.conf
max_connections = 100
```

Restart PostgreSQL service.

---

## 📊 DATABASE SCHEMA

### Table: users

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| username | String(50) | Unique |
| email | String(100) | Unique |
| full_name | String(100) | |
| hashed_password | String(255) | |
| is_active | Boolean | Default: True |
| is_admin | Boolean | Default: False |
| created_at | DateTime | Auto |
| updated_at | DateTime | Auto |

### Table: recognition_history

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| transaction_id | String(100) | Unique UUID |
| user_id | Integer | Foreign key (nullable) |
| image_filename | String(255) | |
| image_path | String(500) | |
| image_url | String(500) | |
| people_count | Integer | |
| genders | JSON | List of genders |
| colors | JSON | List of colors |
| weather | JSON | Weather info |
| objects | JSON | List of objects |
| processing_time | Float | Seconds |
| status | String(20) | success/failed |
| created_at | DateTime | Auto |

### Table: detected_persons

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| recognition_id | Integer | Foreign key |
| person_id | Integer | Person number in image |
| gender | String(20) | male/female/unknown |
| gender_confidence | Float | 0.0 - 1.0 |
| bbox_x | Float | Bounding box X |
| bbox_y | Float | Bounding box Y |
| bbox_width | Float | Bounding box width |
| bbox_height | Float | Bounding box height |
| clothing_color | String(50) | Color name |
| clothing_color_hex | String(10) | Hex code |
| color_confidence | Float | 0.0 - 1.0 |

### Table: detected_objects

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| recognition_id | Integer | Foreign key |
| object_class | String(100) | Object class |
| object_name_vi | String(100) | Vietnamese name |
| confidence | Float | 0.0 - 1.0 |
| bbox_x | Float | Bounding box X |
| bbox_y | Float | Bounding box Y |
| bbox_width | Float | Bounding box width |
| bbox_height | Float | Bounding box height |

---

## 🎯 WORKFLOW HOÀN CHỈNH

### Setup Lần Đầu

```bash
# 1. Cài PostgreSQL
# Download từ postgresql.org và cài đặt

# 2. Tạo database
psql -U postgres
CREATE DATABASE nhandanghinhanh;
\q

# 3. Cấu hình backend
cd backend
copy .env.example .env
# Chỉnh sửa .env với thông tin database

# 4. Cài packages
pip install -r requirements.txt

# 5. Khởi tạo database
python init_db.py

# 6. Test connection
python test_db.py

# 7. Chạy server
python main.py
```

### Development Workflow

```bash
# 1. Start PostgreSQL service (nếu chưa chạy)
# Windows: services.msc → postgresql-x64-16 → Start

# 2. Chạy backend
cd backend
python main.py

# 3. Test API
# http://localhost:8000/docs

# 4. Xem database
# pgAdmin 4 → nhandanghinhanh
```

---

## 💡 TIPS & BEST PRACTICES

### 1. Backup Database

```bash
# Backup
pg_dump -U postgres -d nhandanghinhanh > backup.sql

# Restore
psql -U postgres -d nhandanghinhanh < backup.sql
```

### 2. Performance Tuning

```sql
-- Tạo indexes cho queries nhanh hơn
CREATE INDEX idx_transaction_id ON recognition_history(transaction_id);
CREATE INDEX idx_user_id ON recognition_history(user_id);
CREATE INDEX idx_created_at ON recognition_history(created_at);
```

### 3. Connection Pooling

Trong `database.py` đã cấu hình:
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=10,      # 10 connections
    max_overflow=20    # Thêm 20 nếu cần
)
```

### 4. Monitoring

```sql
-- Xem active connections
SELECT * FROM pg_stat_activity;

-- Xem database size
SELECT pg_size_pretty(pg_database_size('nhandanghinhanh'));

-- Xem table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

---

## 🔐 SECURITY

### Production Checklist

- [ ] Đổi password mặc định
- [ ] Tạo user riêng (không dùng postgres)
- [ ] Restrict network access
- [ ] Bật SSL connection
- [ ] Regular backups
- [ ] Update PostgreSQL thường xuyên

### Connection String cho Production

```ini
# Development
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/nhandanghinhanh

# Production (SSL enabled)
DATABASE_URL=postgresql://user:password@host:5432/dbname?sslmode=require
```

---

## 📚 TÀI LIỆU THAM KHẢO

- [PostgreSQL Official Docs](https://www.postgresql.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [pgAdmin Documentation](https://www.pgadmin.org/docs/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)

---

## 🆘 CẦN TRỢ GIÚP?

### Check Connection

```bash
cd backend
python -c "from database import check_database_connection; check_database_connection()"
```

### View Logs

```bash
# PostgreSQL logs
# Windows: C:\Program Files\PostgreSQL\16\data\log\

# Backend logs
# Terminal output khi chạy python main.py
```

### Common Commands

```bash
# Connect to database
psql -U postgres -d nhandanghinhanh

# List databases
\l

# List tables
\dt

# Describe table
\d table_name

# View data
SELECT * FROM recognition_history LIMIT 10;

# Quit
\q
```

---

**✅ HOÀN THÀNH! Bây giờ bạn có thể sử dụng PostgreSQL với backend!**

**🚀 Next Steps:**
1. Chạy backend: `python main.py`
2. Test API: http://localhost:8000/docs
3. Upload ảnh và xem dữ liệu trong database!

---

**Version:** 1.0.0  
**Last Updated:** 26/10/2025  
**Author:** AI Assistant  

