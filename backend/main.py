"""
Backend API Server - Ứng Dụng Nhận Dạng Đối Tượng
FastAPI RESTful API cho Flutter Frontend
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import os
import uuid
from datetime import datetime
import shutil

# Import các modules nhận dạng
from modules.nhan_dang_gioi_tinh import nhan_dang_gioi_tinh_tu_anh
from modules.nhan_dang_mau_sac import nhan_dang_mau_ao
from modules.nhan_dang_thoi_tiet import phan_tich_thoi_tiet
from modules.nhan_dang_vat_dung import nhan_dang_vat_dung

# Cấu hình
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Khởi tạo FastAPI
app = FastAPI(
    title="API Nhận Dạng Đối Tượng",
    description="Backend API cho ứng dụng nhận dạng đối tượng trên ảnh",
    version="1.0.0"
)

# CORS - Cho phép Flutter app gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production: thay * bằng domain cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== MODELS ====================

class RecognitionResult(BaseModel):
    """Model kết quả nhận dạng"""
    transaction_id: str
    image_url: str
    people_count: int
    genders: List[dict]
    colors: List[dict]
    weather: dict
    objects: List[dict]
    processing_time: float
    timestamp: str
    status: str = "success"

class ErrorResponse(BaseModel):
    """Model response lỗi"""
    status: str = "error"
    message: str
    detail: Optional[str] = None

# ==================== ENDPOINTS ====================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "Nhận Dạng Đối Tượng API",
        "version": "1.0.0",
        "endpoints": {
            "recognize": "/api/recognize",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Kiểm tra server health"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/recognize", response_model=RecognitionResult)
async def recognize_image(file: UploadFile = File(...)):
    """
    Nhận dạng đối tượng trong ảnh
    
    Args:
        file: File ảnh upload từ Flutter app
        
    Returns:
        RecognitionResult: Kết quả nhận dạng chi tiết
    """
    start_time = datetime.now()
    
    try:
        # Kiểm tra file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="File phải là ảnh (jpg, png, ...)"
            )
        
        # Tạo ID duy nhất cho giao dịch
        transaction_id = str(uuid.uuid4())
        
        # Lưu file tạm
        file_extension = os.path.splitext(file.filename)[1]
        temp_filename = f"{transaction_id}{file_extension}"
        temp_path = os.path.join(UPLOAD_DIR, temp_filename)
        
        # Ghi file
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # ===== XỬ LÝ AI =====
        
        # 1. Nhận dạng người và giới tính
        gender_results = nhan_dang_gioi_tinh_tu_anh(temp_path)
        
        # 2. Nhận dạng màu áo
        color_results = []
        if gender_results:  # Nếu có người
            for person in gender_results:
                color = nhan_dang_mau_ao(temp_path, person.get('bbox'))
                color_results.append({
                    "person_id": person.get('person_id'),
                    "color": color.get('ten_mau'),
                    "hex": color.get('ma_hex'),
                    "confidence": color.get('do_tin_cay')
                })
        
        # 3. Nhận dạng thời tiết/phong cảnh
        weather_result = phan_tich_thoi_tiet(temp_path)
        
        # 4. Nhận dạng vật dụng
        object_results = nhan_dang_vat_dung(temp_path)
        
        # Tính thời gian xử lý
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        # Tạo response
        result = RecognitionResult(
            transaction_id=transaction_id,
            image_url=f"/uploads/{temp_filename}",
            people_count=len(gender_results) if gender_results else 0,
            genders=gender_results or [],
            colors=color_results,
            weather=weather_result or {},
            objects=object_results or [],
            processing_time=round(processing_time, 2),
            timestamp=datetime.now().isoformat(),
            status="success"
        )
        
        return result
        
    except Exception as e:
        # Log lỗi
        print(f"Error processing image: {str(e)}")
        
        # Xóa file tạm nếu có lỗi
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi xử lý ảnh: {str(e)}"
        )

@app.get("/api/history")
async def get_history():
    """
    Lấy lịch sử nhận dạng
    TODO: Kết nối với PostgreSQL
    """
    return {
        "status": "success",
        "message": "Chức năng đang phát triển - cần kết nối PostgreSQL",
        "data": []
    }

@app.delete("/api/transaction/{transaction_id}")
async def delete_transaction(transaction_id: str):
    """
    Xóa giao dịch và ảnh
    TODO: Kết nối với PostgreSQL
    """
    return {
        "status": "success",
        "message": f"Đã xóa giao dịch {transaction_id}"
    }

# ==================== ERROR HANDLERS ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Xử lý HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Xử lý các exceptions khác"""
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Lỗi server nội bộ",
            "detail": str(exc)
        }
    )

# ==================== STARTUP/SHUTDOWN ====================

@app.on_event("startup")
async def startup_event():
    """Khởi động server"""
    print("=" * 60)
    print("🚀 Backend API Server Started!")
    print("=" * 60)
    print(f"📍 Server running at: http://localhost:8000")
    print(f"📖 API Documentation: http://localhost:8000/docs")
    print(f"📊 Alternative docs: http://localhost:8000/redoc")
    print("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    """Tắt server"""
    print("🛑 Backend API Server Stopped!")

# ==================== RUN ====================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "=" * 60)
    print("🎯 Starting Backend API Server...")
    print("=" * 60 + "\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload khi code thay đổi
        log_level="info"
    )

