# 🏗️ KIẾN TRÚC HỆ THỐNG - System Architecture

## 📊 Tổng Quan

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                   📱 FLUTTER MOBILE APP                      │ │
│  │                                                              │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │ │
│  │  │  Home    │  │  Camera  │  │  Result  │  │ History  │   │ │
│  │  │  Screen  │  │  Screen  │  │  Screen  │  │  Screen  │   │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │ │
│  │                                                              │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │         STATE MANAGEMENT (Provider)                  │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  │                                                              │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │         API SERVICE LAYER (Dio HTTP Client)          │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └──────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS/REST API
                              │ JSON over HTTP
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         SERVER LAYER                                │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                 🐍 PYTHON FASTAPI BACKEND                    │ │
│  │                                                              │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │              API ENDPOINTS LAYER                     │  │ │
│  │  │                                                      │  │ │
│  │  │  POST /api/recognize    → Nhận dạng ảnh            │  │ │
│  │  │  GET  /api/history      → Lấy lịch sử              │  │ │
│  │  │  GET  /health           → Health check              │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  │                                                              │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │              BUSINESS LOGIC LAYER                    │  │ │
│  │  │                                                      │  │ │
│  │  │  • File Upload Handler                              │  │ │
│  │  │  • Image Validation                                 │  │ │
│  │  │  • Task Queue Manager                               │  │ │
│  │  │  • Result Formatter                                 │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  │                                                              │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │              AI/ML PROCESSING LAYER                  │  │ │
│  │  │                                                      │  │ │
│  │  │  ┌──────────────┐  ┌──────────────┐               │  │ │
│  │  │  │ YOLOv8       │  │ OpenCV       │               │  │ │
│  │  │  │ Detection    │  │ Processing   │               │  │ │
│  │  │  └──────────────┘  └──────────────┘               │  │ │
│  │  │                                                      │  │ │
│  │  │  ┌──────────────────────────────────────────────┐  │  │ │
│  │  │  │ Recognition Modules:                         │  │  │ │
│  │  │  │  • nhan_dang_gioi_tinh.py  (Gender)         │  │  │ │
│  │  │  │  • nhan_dang_mau_sac.py    (Color)          │  │  │ │
│  │  │  │  • nhan_dang_thoi_tiet.py  (Weather)        │  │  │ │
│  │  │  │  • nhan_dang_vat_dung.py   (Objects)        │  │  │ │
│  │  │  └──────────────────────────────────────────────┘  │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  │                                                              │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │              DATA ACCESS LAYER                       │  │ │
│  │  │              (SQLAlchemy ORM)                        │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └──────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │ SQL Queries
                              │ Connection Pool
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                                  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                   🐘 POSTGRESQL DATABASE                     │ │
│  │                                                              │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │ │
│  │  │   users      │  │ transactions │  │  recognition │     │ │
│  │  │   table      │  │   table      │  │  _results    │     │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘     │ │
│  │                                                              │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │              INDEXES & CONSTRAINTS                   │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └──────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │ Backup & Replication
                              ▼
                      ┌────────────────┐
                      │  File Storage  │
                      │  (Images)      │
                      └────────────────┘
```

---

## 🔄 Data Flow

### 1. Image Recognition Flow

```
User Action → Flutter UI → API Call → Backend Processing → Database → Response

1. User chọn/chụp ảnh
   ↓
2. Flutter compress ảnh (max 1920px, quality 85%)
   ↓
3. HTTP POST multipart/form-data
   ↓
4. FastAPI receives file
   ↓
5. Save to temp storage (uploads/)
   ↓
6. Load YOLOv8 model (cached)
   ↓
7. Run AI modules:
   ├─ Gender detection
   ├─ Color detection
   ├─ Weather analysis
   └─ Object detection
   ↓
8. Save results to PostgreSQL
   ↓
9. Format JSON response
   ↓
10. Send back to Flutter
    ↓
11. Parse & display results
    ↓
12. Cache locally (SharedPreferences)
```

### 2. Request/Response Format

**Request:**
```http
POST /api/recognize HTTP/1.1
Host: localhost:8000
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="image.jpg"
Content-Type: image/jpeg

[binary image data]
------WebKitFormBoundary--
```

**Response:**
```json
{
  "transaction_id": "550e8400-e29b-41d4-a716-446655440000",
  "image_url": "/uploads/550e8400.jpg",
  "people_count": 2,
  "genders": [
    {
      "person_id": 1,
      "gender": "Nam",
      "confidence": 0.85
    }
  ],
  "colors": [
    {
      "person_id": 1,
      "color": "Đỏ",
      "hex": "#FF0000",
      "confidence": 0.9
    }
  ],
  "weather": {
    "type": "Nắng",
    "brightness": 0.85,
    "description": "Trời nắng đẹp"
  },
  "objects": [
    {
      "name": "Ba lô",
      "count": 1,
      "confidence": 0.92
    }
  ],
  "processing_time": 1.23,
  "timestamp": "2025-10-25T15:30:00Z",
  "status": "success"
}
```

---

## 🎨 Frontend Architecture (Flutter)

### Layer Structure

```
┌─────────────────────────────────────┐
│         Presentation Layer          │
│         (UI Components)             │
│                                     │
│  • Screens                          │
│  • Widgets                          │
│  • Themes                           │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│        State Management             │
│        (Provider/ChangeNotifier)    │
│                                     │
│  • RecognitionProvider              │
│  • UserProvider                     │
│  • HistoryProvider                  │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│         Business Logic              │
│         (Services)                  │
│                                     │
│  • ApiService                       │
│  • ImageService                     │
│  • StorageService                   │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│         Data Layer                  │
│         (Models & DTOs)             │
│                                     │
│  • RecognitionResult                │
│  • Gender, Color, Weather, Object   │
└─────────────────────────────────────┘
```

### Directory Structure

```
lib/
├── main.dart                 # Entry point
│
├── screens/                  # UI Screens
│   ├── home_screen.dart
│   ├── result_screen.dart
│   └── history_screen.dart
│
├── widgets/                  # Reusable widgets
│   ├── image_picker_widget.dart
│   └── result_card.dart
│
├── providers/                # State management
│   └── recognition_provider.dart
│
├── services/                 # Business logic
│   ├── api_service.dart
│   └── storage_service.dart
│
├── models/                   # Data models
│   └── recognition_result.dart
│
└── utils/                    # Utilities
    ├── constants.dart
    └── helpers.dart
```

---

## 🐍 Backend Architecture (Python)

### Layer Structure

```
┌─────────────────────────────────────┐
│         API Layer                   │
│         (FastAPI Endpoints)         │
│                                     │
│  • Route handlers                   │
│  • Request validation               │
│  • Response formatting              │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│         Service Layer               │
│         (Business Logic)            │
│                                     │
│  • ImageProcessingService           │
│  • RecognitionService               │
│  • HistoryService                   │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│         AI/ML Layer                 │
│         (Recognition Modules)       │
│                                     │
│  • Gender detection                 │
│  • Color detection                  │
│  • Weather analysis                 │
│  • Object detection                 │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│         Data Layer                  │
│         (Database Access)           │
│                                     │
│  • SQLAlchemy models                │
│  • CRUD operations                  │
│  • Query builders                   │
└─────────────────────────────────────┘
```

### Directory Structure

```
backend/
├── main.py                   # FastAPI app
│
├── api/                      # API endpoints
│   ├── routes/
│   │   ├── recognition.py
│   │   └── history.py
│   └── dependencies.py
│
├── services/                 # Business logic
│   ├── recognition_service.py
│   └── image_service.py
│
├── modules/                  # AI modules
│   ├── nhan_dang_gioi_tinh.py
│   ├── nhan_dang_mau_sac.py
│   ├── nhan_dang_thoi_tiet.py
│   └── nhan_dang_vat_dung.py
│
├── models/                   # Database models
│   ├── user.py
│   ├── transaction.py
│   └── result.py
│
├── schemas/                  # Pydantic schemas
│   └── recognition.py
│
├── utils/                    # Utilities
│   ├── xu_ly_anh.py
│   └── chuyen_doi.py
│
└── db/                       # Database
    ├── database.py
    └── migrations/
```

---

## 🗄️ Database Schema

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Transactions table
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    transaction_id UUID UNIQUE NOT NULL,
    user_id INTEGER REFERENCES users(id),
    image_path VARCHAR(255),
    image_url TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    processed_at TIMESTAMP
);

-- Recognition results table
CREATE TABLE recognition_results (
    id SERIAL PRIMARY KEY,
    transaction_id UUID REFERENCES transactions(transaction_id),
    people_count INTEGER,
    genders JSONB,          -- [{"person_id": 1, "gender": "Nam", ...}]
    colors JSONB,           -- [{"person_id": 1, "color": "Đỏ", ...}]
    weather JSONB,          -- {"type": "Nắng", "brightness": 0.85, ...}
    objects JSONB,          -- [{"name": "Ba lô", "count": 1, ...}]
    processing_time FLOAT,
    model_version VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_transactions_user_id ON transactions(user_id);
CREATE INDEX idx_transactions_created_at ON transactions(created_at);
CREATE INDEX idx_results_transaction_id ON recognition_results(transaction_id);
```

---

## 🔐 Security Architecture

### Authentication Flow (TODO)

```
1. User login → POST /api/auth/login
   ↓
2. Backend validates credentials
   ↓
3. Generate JWT token
   ↓
4. Return token to Flutter
   ↓
5. Flutter stores token (SecureStorage)
   ↓
6. Include token in API requests
   ↓
7. Backend validates token (middleware)
   ↓
8. Grant/Deny access
```

### Security Measures

- ✅ **HTTPS**: SSL/TLS encryption
- ✅ **CORS**: Restrict origins
- ✅ **File validation**: Check file types
- ✅ **Size limits**: Max 10MB per upload
- ⏳ **JWT Authentication**: TODO
- ⏳ **Rate limiting**: TODO
- ⏳ **Input sanitization**: TODO

---

## 📊 Performance & Scalability

### Current Performance

| Metric | CPU | GPU | Target |
|--------|-----|-----|--------|
| Model load time | 2-3s | 1s | < 2s |
| Image processing | 1-2s | 0.2-0.5s | < 1s |
| API response time | 2-4s | 1-2s | < 3s |
| Concurrent users | 10-20 | 50-100 | 100+ |

### Scaling Strategy

**Horizontal Scaling:**
```
Load Balancer
    ├─ Backend Server 1 (GPU)
    ├─ Backend Server 2 (GPU)
    └─ Backend Server 3 (GPU)
```

**Caching Strategy:**
```
┌──────────────┐
│   Redis      │  ← Cache recent results
└──────────────┘
       │
       ▼
┌──────────────┐
│   Backend    │  ← Process if not cached
└──────────────┘
       │
       ▼
┌──────────────┐
│  PostgreSQL  │  ← Permanent storage
└──────────────┘
```

---

## 🚀 Deployment Architecture

### Development

```
Developer Machine
├─ Backend: localhost:8000
├─ Frontend: Flutter run
└─ Database: Local PostgreSQL
```

### Staging

```
Cloud Server (Staging)
├─ Backend: staging.api.com
├─ Database: Managed PostgreSQL
└─ Frontend: TestFlight/Internal Testing
```

### Production

```
┌────────────────────────────────────────┐
│           CDN (Images)                 │
└────────────────────────────────────────┘
                │
                ▼
┌────────────────────────────────────────┐
│       Load Balancer (HTTPS)            │
└────────────────────────────────────────┘
                │
        ┌───────┴───────┐
        ▼               ▼
┌──────────────┐ ┌──────────────┐
│  Backend 1   │ │  Backend 2   │
│  (Docker)    │ │  (Docker)    │
└──────────────┘ └──────────────┘
        │               │
        └───────┬───────┘
                ▼
┌────────────────────────────────────────┐
│   PostgreSQL (Managed/RDS)             │
└────────────────────────────────────────┘
                │
                ▼
┌────────────────────────────────────────┐
│   S3/Cloud Storage (Images)            │
└────────────────────────────────────────┘
```

---

## 🔄 CI/CD Pipeline

```
Developer Push
    │
    ▼
GitHub/GitLab
    │
    ├─ Backend Pipeline
    │  ├─ Lint (flake8)
    │  ├─ Test (pytest)
    │  ├─ Build Docker image
    │  ├─ Push to registry
    │  └─ Deploy to server
    │
    └─ Frontend Pipeline
       ├─ Lint (flutter analyze)
       ├─ Test (flutter test)
       ├─ Build APK/IPA
       └─ Upload to stores
```

---

**📝 Document Version:** 1.0.0
**📅 Last Updated:** 25/10/2025
**✍️ Author:** AI Development Team

