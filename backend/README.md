# 🐍 Backend API Server

Backend Python FastAPI cho ứng dụng nhận dạng đối tượng trên ảnh.

## 📋 Mục Lục

- [Tính Năng](#tính-năng)
- [Cài Đặt](#cài-đặt)
- [Chạy Server](#chạy-server)
- [API Documentation](#api-documentation)
- [Cấu Trúc Thư Mục](#cấu-trúc-thư-mục)

## 🎯 Tính Năng

### API Endpoints

| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/` | GET | Health check |
| `/health` | GET | Server status |
| `/api/recognize` | POST | Nhận dạng ảnh |
| `/api/history` | GET | Lịch sử (TODO) |
| `/docs` | GET | API Documentation (Swagger) |

### Chức Năng Nhận Dạng

- ✅ **Nhận dạng người & giới tính** (Nam/Nữ)
- ✅ **Nhận dạng màu áo** (10+ màu)
- ✅ **Nhận dạng thời tiết/phong cảnh**
- ✅ **Nhận dạng vật dụng** (80+ loại)

## 🚀 Cài Đặt

### 1. Tạo Virtual Environment (Khuyến nghị)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. Cài Đặt Dependencies

```bash
pip install -r requirements.txt
```

⏳ Quá trình này mất 5-10 phút (download PyTorch, YOLOv8...)

### 3. Cấu Hình Environment

```bash
# Copy file .env.example
copy .env.example .env

# Chỉnh sửa .env với thông tin của bạn
```

## 🏃 Chạy Server

### Development Mode (Auto-reload)

```bash
python main.py
```

Hoặc:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Server sẽ chạy tại: `http://localhost:8000`

## 📖 API Documentation

### Swagger UI (Interactive)

```
http://localhost:8000/docs
```

### ReDoc (Alternative)

```
http://localhost:8000/redoc
```

## 📁 Cấu Trúc Thư Mục

```
backend/
│
├── main.py                     # FastAPI server chính
├── requirements.txt            # Dependencies
├── .env.example               # Environment variables mẫu
├── README.md                   # File này
│
├── modules/                    # AI Modules
│   ├── __init__.py
│   ├── nhan_dang_gioi_tinh.py
│   ├── nhan_dang_mau_sac.py
│   ├── nhan_dang_thoi_tiet.py
│   └── nhan_dang_vat_dung.py
│
├── utils/                      # Utilities
│   ├── __init__.py
│   ├── xu_ly_anh.py
│   └── chuyen_doi.py
│
├── uploads/                    # Upload directory (auto-created)
│
└── data/                       # Test data
    └── anh_mau/
```

## 🔌 Sử Dụng API

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-25T15:30:00"
}
```

### 2. Nhận Dạng Ảnh

```bash
curl -X POST "http://localhost:8000/api/recognize" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@image.jpg"
```

Response:
```json
{
  "transaction_id": "uuid-here",
  "image_url": "/uploads/uuid.jpg",
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
  "timestamp": "2025-10-25T15:30:00",
  "status": "success"
}
```

## 🗄️ PostgreSQL Database (TODO)

### Schema

```sql
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    transaction_id UUID UNIQUE,
    user_id INTEGER,
    image_url TEXT,
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE recognition_results (
    id SERIAL PRIMARY KEY,
    transaction_id UUID REFERENCES transactions(transaction_id),
    people_count INTEGER,
    genders JSONB,
    colors JSONB,
    weather JSONB,
    objects JSONB,
    processing_time FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Kết Nối Database

```python
# Uncomment trong main.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
```

## 🔧 Troubleshooting

### Lỗi: "ModuleNotFoundError"

```bash
# Kiểm tra virtual environment đã activate chưa
# Cài lại dependencies
pip install -r requirements.txt
```

### Lỗi: "Port 8000 already in use"

```bash
# Đổi port
uvicorn main:app --port 8001

# Hoặc kill process đang dùng port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Lỗi: CUDA/GPU

```bash
# Server sẽ tự động fallback về CPU
# Để dùng GPU, cài PyTorch với CUDA:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

## 📊 Performance

| Metric | CPU | GPU |
|--------|-----|-----|
| Load model | 2-3s | 1s |
| Process image | 1-2s | 0.2-0.5s |
| API response | < 3s | < 1s |

## 🚢 Deployment

### Option 1: DigitalOcean

```bash
# 1. Tạo Droplet (Ubuntu 22.04)
# 2. SSH vào server
ssh root@your-server-ip

# 3. Clone repo & setup
git clone your-repo
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Chạy với systemd hoặc supervisor
```

### Option 2: Docker

```dockerfile
# TODO: Tạo Dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📞 Support

- 📖 Docs: `/docs` endpoint
- 🐛 Issues: GitHub Issues
- 💬 Contact: dev@example.com

## 📝 License

MIT License - Free to use

---

**Made with ❤️ by Python & FastAPI**

