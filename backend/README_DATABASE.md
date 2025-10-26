# 🐘 DATABASE INTEGRATION - README

## 📋 TỔNG QUAN

Backend đã được tích hợp **PostgreSQL** để lưu trữ:
- 👤 Thông tin người dùng
- 📸 Lịch sử nhận dạng ảnh
- 👥 Chi tiết người được phát hiện
- 📦 Chi tiết vật dụng được phát hiện
- 📊 Thống kê hàng ngày
- 📝 System logs

---

## 🗂️ CẤU TRÚC FILES

```
backend/
├── database.py              ← Database config & connection
├── models.py                ← SQLAlchemy models (tables)
├── services/
│   └── db_service.py       ← CRUD operations & business logic
├── init_db.py              ← Script khởi tạo database
├── test_db.py              ← Script test database
├── .env                     ← Environment variables (GIT IGNORE)
├── .env.example            ← Template for .env
└── main.py                  ← FastAPI app (đã tích hợp DB)
```

---

## 🚀 QUICK START

### 1. Setup Database

```bash
# Tạo database trong PostgreSQL
psql -U postgres
CREATE DATABASE nhandanghinhanh;
\q
```

### 2. Cấu hình .env

```bash
# Copy template
cp .env.example .env

# Edit .env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/nhandanghinhanh
```

### 3. Cài Packages

```bash
pip install -r requirements.txt
```

### 4. Khởi tạo Tables

```bash
python init_db.py
```

### 5. Test Connection

```bash
python test_db.py
```

### 6. Run Server

```bash
python main.py
```

---

## 📊 DATABASE SCHEMA

### Table: users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
```

### Table: recognition_history
```sql
CREATE TABLE recognition_history (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(100) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES users(id),
    image_filename VARCHAR(255) NOT NULL,
    image_path VARCHAR(500) NOT NULL,
    image_url VARCHAR(500),
    people_count INTEGER DEFAULT 0,
    genders JSONB,
    colors JSONB,
    weather JSONB,
    objects JSONB,
    processing_time FLOAT,
    status VARCHAR(20) DEFAULT 'success',
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Table: detected_persons
```sql
CREATE TABLE detected_persons (
    id SERIAL PRIMARY KEY,
    recognition_id INTEGER REFERENCES recognition_history(id) ON DELETE CASCADE,
    person_id INTEGER,
    gender VARCHAR(20),
    gender_confidence FLOAT,
    bbox_x FLOAT,
    bbox_y FLOAT,
    bbox_width FLOAT,
    bbox_height FLOAT,
    clothing_color VARCHAR(50),
    clothing_color_hex VARCHAR(10),
    color_confidence FLOAT
);
```

### Table: detected_objects
```sql
CREATE TABLE detected_objects (
    id SERIAL PRIMARY KEY,
    recognition_id INTEGER REFERENCES recognition_history(id) ON DELETE CASCADE,
    object_class VARCHAR(100),
    object_name_vi VARCHAR(100),
    confidence FLOAT,
    bbox_x FLOAT,
    bbox_y FLOAT,
    bbox_width FLOAT,
    bbox_height FLOAT
);
```

---

## 🔌 API ENDPOINTS

### POST /api/recognize
Upload ảnh và nhận dạng, tự động lưu vào database

**Request:**
```bash
curl -X POST "http://localhost:8000/api/recognize" \
  -F "file=@image.jpg"
```

**Response:**
```json
{
  "transaction_id": "uuid-here",
  "image_url": "/uploads/uuid.jpg",
  "people_count": 2,
  "genders": [...],
  "colors": [...],
  "weather": {...},
  "objects": [...],
  "processing_time": 1.23,
  "status": "success"
}
```

### GET /api/history
Lấy lịch sử nhận dạng

**Request:**
```bash
curl "http://localhost:8000/api/history?limit=50&offset=0"
```

**Response:**
```json
{
  "status": "success",
  "count": 10,
  "data": [
    {
      "id": 1,
      "transaction_id": "uuid",
      "image_url": "/uploads/uuid.jpg",
      "people_count": 2,
      "processing_time": 1.23,
      "created_at": "2025-10-26T10:30:00",
      "status": "success"
    }
  ]
}
```

### GET /api/history/{transaction_id}
Lấy chi tiết một giao dịch

**Request:**
```bash
curl "http://localhost:8000/api/history/uuid-here"
```

### DELETE /api/transaction/{transaction_id}
Xóa giao dịch và ảnh

**Request:**
```bash
curl -X DELETE "http://localhost:8000/api/transaction/uuid-here"
```

### GET /api/statistics
Lấy thống kê tổng quan

**Request:**
```bash
curl "http://localhost:8000/api/statistics"
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "total_recognitions": 100,
    "total_people_detected": 250,
    "avg_processing_time": 1.45
  }
}
```

---

## 💻 CODE EXAMPLES

### Import Database Session

```python
from database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

@app.get("/example")
def example_endpoint(db: Session = Depends(get_db)):
    # Use db here
    pass
```

### Query Records

```python
from models import RecognitionHistory
from sqlalchemy.orm import Session

def get_recent_records(db: Session, limit: int = 10):
    return db.query(RecognitionHistory)\
        .order_by(RecognitionHistory.created_at.desc())\
        .limit(limit)\
        .all()
```

### Create Record

```python
from services.db_service import create_recognition_record

record = create_recognition_record(
    db=db,
    transaction_id="uuid",
    image_filename="image.jpg",
    image_path="/uploads/image.jpg",
    recognition_result={
        "people_count": 2,
        "genders": [...],
        "colors": [...],
        # ...
    }
)
```

### Get Statistics

```python
from services.db_service import get_user_statistics

stats = get_user_statistics(db, user_id=1)
print(stats["total_recognitions"])
```

---

## 🔧 MAINTENANCE

### Backup Database

```bash
pg_dump -U postgres -d nhandanghinhanh > backup.sql
```

### Restore Database

```bash
psql -U postgres -d nhandanghinhanh < backup.sql
```

### Reset Database

```bash
python init_db.py --reset
```

### View Logs

```python
from services.db_service import get_recent_logs

logs = get_recent_logs(db, limit=100, level="ERROR")
for log in logs:
    print(f"{log.created_at}: {log.message}")
```

---

## 🐛 TROUBLESHOOTING

### Connection Error

```bash
# Check PostgreSQL is running
services.msc → postgresql → Start

# Test connection
python -c "from database import check_database_connection; check_database_connection()"
```

### Tables Not Created

```bash
# Run initialization script
python init_db.py
```

### Data Not Saving

Check logs in terminal when running `python main.py`:
- `✅ Saved to database: X` - Success
- `⚠️ Database save failed: ...` - Error (but API still works)

---

## 📈 PERFORMANCE

### Current Settings

```python
# In database.py
engine = create_engine(
    DATABASE_URL,
    pool_size=10,       # Connection pool
    max_overflow=20,    # Extra connections
    pool_pre_ping=True  # Check before use
)
```

### Indexes

```sql
-- Already created automatically by SQLAlchemy
CREATE INDEX idx_transaction_id ON recognition_history(transaction_id);
CREATE INDEX idx_user_id ON recognition_history(user_id);
CREATE INDEX idx_created_at ON recognition_history(created_at);
```

---

## 🔐 SECURITY

### Production Checklist

- [ ] Change default password
- [ ] Use environment variables
- [ ] Enable SSL connection
- [ ] Restrict network access
- [ ] Regular backups
- [ ] Update PostgreSQL

### SSL Connection

```ini
# In .env
DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require
```

---

## 📚 DOCUMENTATION

- **Full Guide:** [HUONG_DAN_POSTGRESQL.md](../HUONG_DAN_POSTGRESQL.md)
- **Quick Start:** [POSTGRESQL_QUICK_START.txt](../POSTGRESQL_QUICK_START.txt)
- **SQLAlchemy Docs:** https://docs.sqlalchemy.org/
- **PostgreSQL Docs:** https://www.postgresql.org/docs/

---

## ✅ CHECKLIST

### Initial Setup
- [ ] Install PostgreSQL
- [ ] Create database `nhandanghinhanh`
- [ ] Configure `.env` file
- [ ] Install packages: `pip install -r requirements.txt`
- [ ] Run: `python init_db.py`
- [ ] Test: `python test_db.py`

### Daily Use
- [ ] Check PostgreSQL is running
- [ ] Run backend: `python main.py`
- [ ] Upload images via API
- [ ] View data in pgAdmin or API

---

**✅ Database integration complete and ready to use!**

**Questions?** Check [HUONG_DAN_POSTGRESQL.md](../HUONG_DAN_POSTGRESQL.md)

