# 🏗️ DATABASE ARCHITECTURE

## 📊 ENTITY RELATIONSHIP DIAGRAM

```
┌──────────────────────┐
│       users          │
├──────────────────────┤
│ id (PK)             │
│ username            │
│ email               │
│ hashed_password     │
│ is_active           │
│ is_admin            │
│ created_at          │
│ updated_at          │
└──────────────────────┘
           │
           │ 1:N
           ▼
┌──────────────────────────────┐
│   recognition_history        │
├──────────────────────────────┤
│ id (PK)                      │
│ transaction_id (UNIQUE)      │
│ user_id (FK) ◄───────────────┤
│ image_filename               │
│ image_path                   │
│ image_url                    │
│ people_count                 │
│ genders (JSON)               │
│ colors (JSON)                │
│ weather (JSON)               │
│ objects (JSON)               │
│ processing_time              │
│ status                       │
│ created_at                   │
└──────────────────────────────┘
           │
           ├─────────────┬─────────────┐
           │ 1:N         │ 1:N         │
           ▼             ▼             │
┌─────────────────┐  ┌─────────────────┐
│detected_persons │  │detected_objects │
├─────────────────┤  ├─────────────────┤
│ id (PK)        │  │ id (PK)        │
│ recognition_id │  │ recognition_id │
│   (FK)         │  │   (FK)         │
│ person_id      │  │ object_class   │
│ gender         │  │ object_name_vi │
│ confidence     │  │ confidence     │
│ bbox (x,y,w,h) │  │ bbox (x,y,w,h) │
│ clothing_color │  └─────────────────┘
│ color_hex      │
│ color_conf     │
└─────────────────┘

┌─────────────────────────┐
│   daily_statistics      │
├─────────────────────────┤
│ id (PK)                │
│ date                   │
│ total_recognitions     │
│ total_people_detected  │
│ total_objects_detected │
│ avg_processing_time    │
│ male_count             │
│ female_count           │
│ most_common_objects    │
│ created_at             │
└─────────────────────────┘

┌─────────────────────┐
│    system_logs      │
├─────────────────────┤
│ id (PK)            │
│ level              │
│ message            │
│ module             │
│ user_id (FK)       │
│ ip_address         │
│ user_agent         │
│ request_path       │
│ extra_data (JSON)  │
│ created_at         │
└─────────────────────┘
```

---

## 🔄 DATA FLOW

```
┌─────────────┐
│ Flutter App │
└──────┬──────┘
       │
       │ 1. Upload Image
       ▼
┌──────────────────────┐
│   FastAPI Backend    │
├──────────────────────┤
│ • Receive image      │
│ • Save to /uploads   │
│ • Process AI         │
└──────┬───────────────┘
       │
       │ 2. AI Processing
       ▼
┌──────────────────────────┐
│   AI Modules             │
├──────────────────────────┤
│ • Gender detection       │
│ • Color detection        │
│ • Weather analysis       │
│ • Object detection       │
└──────┬───────────────────┘
       │
       │ 3. Save Results
       ▼
┌──────────────────────────────┐
│   PostgreSQL Database        │
├──────────────────────────────┤
│ INSERT INTO                  │
│   recognition_history        │
│ INSERT INTO                  │
│   detected_persons           │
│ INSERT INTO                  │
│   detected_objects           │
│ INSERT INTO                  │
│   system_logs                │
└──────┬───────────────────────┘
       │
       │ 4. Return Response
       ▼
┌──────────────────────┐
│ Flutter App          │
├──────────────────────┤
│ • Display results    │
│ • Show history       │
│ • View statistics    │
└──────────────────────┘
```

---

## 📊 EXAMPLE DATA

### recognition_history

```json
{
  "id": 1,
  "transaction_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": null,
  "image_filename": "550e8400.jpg",
  "image_path": "/uploads/550e8400.jpg",
  "image_url": "http://localhost:8000/uploads/550e8400.jpg",
  "people_count": 2,
  "genders": [
    {
      "person_id": 1,
      "gender": "male",
      "confidence": 0.95,
      "bbox": [100, 100, 200, 400]
    },
    {
      "person_id": 2,
      "gender": "female",
      "confidence": 0.92,
      "bbox": [300, 100, 200, 400]
    }
  ],
  "colors": [
    {
      "person_id": 1,
      "color": "Xanh dương",
      "hex": "#0000FF",
      "confidence": 0.88
    },
    {
      "person_id": 2,
      "color": "Đỏ",
      "hex": "#FF0000",
      "confidence": 0.85
    }
  ],
  "weather": {
    "condition": "sunny",
    "confidence": 0.9
  },
  "objects": [
    {
      "class": "chair",
      "ten_tieng_viet": "Ghế",
      "confidence": 0.87,
      "bbox": [50, 200, 100, 150]
    },
    {
      "class": "table",
      "ten_tieng_viet": "Bàn",
      "confidence": 0.82,
      "bbox": [200, 300, 300, 200]
    }
  ],
  "processing_time": 1.23,
  "status": "success",
  "created_at": "2025-10-26T10:30:00+07:00"
}
```

### detected_persons

```sql
id | recognition_id | person_id | gender | confidence | bbox_x | bbox_y | bbox_width | bbox_height | clothing_color | color_hex | color_conf
---|----------------|-----------|--------|------------|--------|--------|------------|-------------|----------------|-----------|------------
1  | 1              | 1         | male   | 0.95       | 100    | 100    | 200        | 400         | Xanh dương     | #0000FF   | 0.88
2  | 1              | 2         | female | 0.92       | 300    | 100    | 200        | 400         | Đỏ             | #FF0000   | 0.85
```

### detected_objects

```sql
id | recognition_id | object_class | object_name_vi | confidence | bbox_x | bbox_y | bbox_width | bbox_height
---|----------------|--------------|----------------|------------|--------|--------|------------|-------------
1  | 1              | chair        | Ghế            | 0.87       | 50     | 200    | 100        | 150
2  | 1              | table        | Bàn            | 0.82       | 200    | 300    | 300        | 200
```

---

## 🔍 SQL QUERIES

### Get Full Recognition Details

```sql
-- Lấy thông tin nhận dạng với chi tiết người và vật dụng
SELECT 
    rh.*,
    (
        SELECT json_agg(dp.*)
        FROM detected_persons dp
        WHERE dp.recognition_id = rh.id
    ) AS persons_detail,
    (
        SELECT json_agg(do.*)
        FROM detected_objects do
        WHERE do.recognition_id = rh.id
    ) AS objects_detail
FROM recognition_history rh
WHERE rh.transaction_id = '550e8400-e29b-41d4-a716-446655440000';
```

### Statistics Queries

```sql
-- Tổng số nhận dạng
SELECT COUNT(*) FROM recognition_history;

-- Trung bình thời gian xử lý
SELECT AVG(processing_time) FROM recognition_history;

-- Tổng số người phát hiện
SELECT SUM(people_count) FROM recognition_history;

-- Top 10 vật dụng phổ biến
SELECT 
    object_class,
    COUNT(*) as count
FROM detected_objects
GROUP BY object_class
ORDER BY count DESC
LIMIT 10;

-- Thống kê theo ngày
SELECT 
    DATE(created_at) as date,
    COUNT(*) as total_recognitions,
    SUM(people_count) as total_people,
    AVG(processing_time) as avg_time
FROM recognition_history
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

### Recent Activity

```sql
-- 10 nhận dạng gần nhất
SELECT 
    transaction_id,
    people_count,
    processing_time,
    created_at
FROM recognition_history
ORDER BY created_at DESC
LIMIT 10;

-- Lỗi gần đây
SELECT * FROM system_logs
WHERE level = 'ERROR'
ORDER BY created_at DESC
LIMIT 20;
```

---

## 🔐 INDEXES & PERFORMANCE

### Indexes (Auto-created by SQLAlchemy)

```sql
-- Primary keys
CREATE INDEX pk_users ON users(id);
CREATE INDEX pk_recognition_history ON recognition_history(id);
CREATE INDEX pk_detected_persons ON detected_persons(id);
CREATE INDEX pk_detected_objects ON detected_objects(id);

-- Unique constraints
CREATE UNIQUE INDEX idx_username ON users(username);
CREATE UNIQUE INDEX idx_email ON users(email);
CREATE UNIQUE INDEX idx_transaction_id ON recognition_history(transaction_id);

-- Foreign keys
CREATE INDEX idx_rh_user_id ON recognition_history(user_id);
CREATE INDEX idx_dp_recognition_id ON detected_persons(recognition_id);
CREATE INDEX idx_do_recognition_id ON detected_objects(recognition_id);

-- Query optimization
CREATE INDEX idx_created_at ON recognition_history(created_at);
CREATE INDEX idx_status ON recognition_history(status);
```

### Performance Tips

```sql
-- Use EXPLAIN to analyze queries
EXPLAIN ANALYZE
SELECT * FROM recognition_history
WHERE created_at > NOW() - INTERVAL '7 days';

-- Vacuum & analyze regularly
VACUUM ANALYZE;

-- Monitor index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

---

## 🧮 TABLE SIZES

```sql
-- Check table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
    pg_total_relation_size(schemaname||'.'||tablename) AS bytes
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY bytes DESC;

-- Database size
SELECT pg_size_pretty(pg_database_size('nhandanghinhanh'));
```

**Expected Sizes (per 1000 records):**
- `recognition_history`: ~500 KB
- `detected_persons`: ~100 KB
- `detected_objects`: ~150 KB
- **Total**: ~750 KB per 1000 recognitions

---

## 🔄 RELATIONSHIPS

```python
# SQLAlchemy Relationships in models.py

class User(Base):
    recognition_history = relationship(
        "RecognitionHistory",
        back_populates="user",
        cascade="all, delete-orphan"  # Delete history when user deleted
    )

class RecognitionHistory(Base):
    user = relationship("User", back_populates="recognition_history")
    detected_persons = relationship(
        "DetectedPerson",
        back_populates="recognition",
        cascade="all, delete-orphan"  # Delete persons when recognition deleted
    )
    detected_objects = relationship(
        "DetectedObject",
        back_populates="recognition",
        cascade="all, delete-orphan"  # Delete objects when recognition deleted
    )

class DetectedPerson(Base):
    recognition = relationship("RecognitionHistory", back_populates="detected_persons")

class DetectedObject(Base):
    recognition = relationship("RecognitionHistory", back_populates="detected_objects")
```

**Cascade Effects:**
- Delete `User` → Deletes all `RecognitionHistory` của user đó
- Delete `RecognitionHistory` → Deletes all `DetectedPerson` và `DetectedObject` liên quan

---

## 📈 SCALING CONSIDERATIONS

### Current Setup (Single Server)

```
Flutter App → FastAPI → PostgreSQL
```

**Limits:**
- ~100 concurrent connections
- ~1000 requests/minute
- Storage: depends on disk

### Future Scaling Options

```
                    ┌──────────────┐
                    │ Load Balancer│
                    └──────┬───────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
  ┌──────────┐      ┌──────────┐      ┌──────────┐
  │ FastAPI 1│      │ FastAPI 2│      │ FastAPI 3│
  └─────┬────┘      └─────┬────┘      └─────┬────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
                    ┌──────────────┐
                    │  PgPool-II   │  (Connection pooling)
                    └──────┬───────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
  ┌──────────┐      ┌──────────┐      ┌──────────┐
  │PostgreSQL│      │PostgreSQL│      │PostgreSQL│
  │  Master  │ ───► │  Replica │      │  Replica │
  └──────────┘      └──────────┘      └──────────┘
        │
        ▼
  ┌──────────┐
  │ Backups  │
  └──────────┘
```

---

## 🔧 MAINTENANCE

### Daily Tasks

```bash
# Check connections
psql -U postgres -d nhandanghinhanh -c "SELECT count(*) FROM pg_stat_activity;"

# Check table sizes
psql -U postgres -d nhandanghinhanh -c "\dt+"
```

### Weekly Tasks

```bash
# Backup database
pg_dump -U postgres nhandanghinhanh > backup_$(date +%Y%m%d).sql

# Vacuum
psql -U postgres -d nhandanghinhanh -c "VACUUM ANALYZE;"
```

### Monthly Tasks

```bash
# Archive old data (older than 6 months)
psql -U postgres -d nhandanghinhanh -c "
    DELETE FROM recognition_history
    WHERE created_at < NOW() - INTERVAL '6 months';
"

# Update statistics
psql -U postgres -d nhandanghinhanh -c "ANALYZE;"
```

---

## 📚 REFERENCE

- **PostgreSQL Docs:** https://www.postgresql.org/docs/
- **SQLAlchemy ORM:** https://docs.sqlalchemy.org/
- **FastAPI + DB:** https://fastapi.tiangolo.com/tutorial/sql-databases/

---

**✅ Architecture documented and production-ready!**

