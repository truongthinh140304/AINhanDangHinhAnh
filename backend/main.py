"""
Backend API Server - Ứng Dụng Nhận Dạng Đối Tượng
FastAPI RESTful API cho Flutter Frontend
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
import os
import uuid
from datetime import datetime
import shutil

# Import database
from database import get_db, check_database_connection, create_tables
from models import RecognitionHistory, User
from services.db_service import (
    create_recognition_record,
    get_user_history,
    get_all_history,
    delete_recognition,
    get_user_statistics,
    create_log
)

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
async def recognize_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Nhận dạng đối tượng trong ảnh
    
    Args:
        file: File ảnh upload từ Flutter app
        db: Database session
        
    Returns:
        RecognitionResult: Kết quả nhận dạng chi tiết
    """
    start_time = datetime.now()
    temp_path = None
    
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
        
        # Tạo response data
        recognition_data = {
            "transaction_id": transaction_id,
            "image_url": f"/uploads/{temp_filename}",
            "people_count": len(gender_results) if gender_results else 0,
            "genders": gender_results or [],
            "colors": color_results,
            "weather": weather_result or {},
            "objects": object_results or [],
            "processing_time": round(processing_time, 2),
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        
        # ===== LƯU VÀO DATABASE =====
        try:
            db_record = create_recognition_record(
                db=db,
                transaction_id=transaction_id,
                image_filename=temp_filename,
                image_path=temp_path,
                recognition_result=recognition_data,
                user_id=None  # TODO: Lấy từ authentication
            )
            
            # Log success
            create_log(
                db=db,
                level="INFO",
                message=f"Nhận dạng thành công: {transaction_id}",
                module="recognition",
                extra_data={"people_count": recognition_data["people_count"]}
            )
            
            print(f"✅ Saved to database: {db_record.id}")
            
        except Exception as db_error:
            print(f"⚠️ Database save failed: {str(db_error)}")
            # Không throw error, vẫn trả về kết quả nhận dạng
            
        # Tạo response
        result = RecognitionResult(**recognition_data)
        
        return result
        
    except Exception as e:
        # Log lỗi
        print(f"❌ Error processing image: {str(e)}")
        
        # Log vào database
        try:
            create_log(
                db=db,
                level="ERROR",
                message=f"Lỗi xử lý ảnh: {str(e)}",
                module="recognition"
            )
        except:
            pass
        
        # Xóa file tạm nếu có lỗi
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi xử lý ảnh: {str(e)}"
        )

@app.get("/api/history")
async def get_history(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Lấy lịch sử nhận dạng
    
    Args:
        limit: Số records tối đa (default: 50)
        offset: Vị trí bắt đầu (default: 0)
        db: Database session
    
    Returns:
        List[RecognitionHistory]: Danh sách lịch sử
    """
    try:
        # Lấy tất cả history (không filter theo user - dành cho demo)
        # Production: nên có authentication và filter theo user_id
        history = get_all_history(db, limit=limit, offset=offset)
        
        # Convert sang dict
        history_data = [
            {
                "id": record.id,
                "transaction_id": record.transaction_id,
                "image_url": record.image_url,
                "people_count": record.people_count,
                "processing_time": record.processing_time,
                "created_at": record.created_at.isoformat(),
                "status": record.status
            }
            for record in history
        ]
        
        return {
            "status": "success",
            "count": len(history_data),
            "data": history_data
        }
        
    except Exception as e:
        print(f"❌ Error getting history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi lấy lịch sử: {str(e)}"
        )

@app.get("/api/history/{transaction_id}")
async def get_transaction_detail(
    transaction_id: str,
    db: Session = Depends(get_db)
):
    """
    Lấy chi tiết một giao dịch
    
    Args:
        transaction_id: UUID của transaction
        db: Database session
    
    Returns:
        RecognitionHistory: Chi tiết giao dịch
    """
    try:
        from services.db_service import get_recognition_by_transaction_id
        
        record = get_recognition_by_transaction_id(db, transaction_id)
        
        if not record:
            raise HTTPException(
                status_code=404,
                detail="Không tìm thấy giao dịch"
            )
        
        return {
            "status": "success",
            "data": {
                "id": record.id,
                "transaction_id": record.transaction_id,
                "image_url": record.image_url,
                "people_count": record.people_count,
                "genders": record.genders,
                "colors": record.colors,
                "weather": record.weather,
                "objects": record.objects,
                "processing_time": record.processing_time,
                "created_at": record.created_at.isoformat(),
                "status": record.status
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error getting transaction: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi lấy thông tin giao dịch: {str(e)}"
        )

@app.delete("/api/transaction/{transaction_id}")
async def delete_transaction(
    transaction_id: str,
    db: Session = Depends(get_db)
):
    """
    Xóa giao dịch và ảnh
    
    Args:
        transaction_id: UUID của transaction
        db: Database session
    
    Returns:
        Success message
    """
    try:
        # Lấy thông tin record để xóa file
        from services.db_service import get_recognition_by_transaction_id
        
        record = get_recognition_by_transaction_id(db, transaction_id)
        
        if not record:
            raise HTTPException(
                status_code=404,
                detail="Không tìm thấy giao dịch"
            )
        
        # Xóa file ảnh
        if record.image_path and os.path.exists(record.image_path):
            os.remove(record.image_path)
            print(f"✅ Deleted image file: {record.image_path}")
        
        # Xóa record trong database
        success = delete_recognition(db, transaction_id)
        
        if success:
            # Log
            create_log(
                db=db,
                level="INFO",
                message=f"Đã xóa giao dịch: {transaction_id}",
                module="recognition"
            )
            
            return {
                "status": "success",
                "message": f"Đã xóa giao dịch {transaction_id}"
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Không thể xóa giao dịch"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error deleting transaction: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi xóa giao dịch: {str(e)}"
        )

@app.get("/api/statistics")
async def get_statistics(db: Session = Depends(get_db)):
    """
    Lấy thống kê tổng quan
    
    Returns:
        Dict: Thống kê hệ thống
    """
    try:
        # Demo: Lấy thống kê chung (không filter theo user)
        # Production: nên có authentication
        from services.db_service import get_user_statistics
        from sqlalchemy import func
        
        # Đếm tổng số records
        total_records = db.query(func.count(RecognitionHistory.id)).scalar()
        
        # Tính tổng people và objects
        total_people = db.query(func.sum(RecognitionHistory.people_count)).scalar() or 0
        
        # Thời gian xử lý trung bình
        avg_time = db.query(func.avg(RecognitionHistory.processing_time)).scalar() or 0
        
        return {
            "status": "success",
            "data": {
                "total_recognitions": total_records,
                "total_people_detected": int(total_people),
                "avg_processing_time": round(float(avg_time), 2)
            }
        }
        
    except Exception as e:
        print(f"❌ Error getting statistics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi lấy thống kê: {str(e)}"
        )

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
    
    # Kiểm tra kết nối database
    print("\n🔌 Checking database connection...")
    db_connected = check_database_connection()
    
    if db_connected:
        print("✅ Database connected successfully!")
        
        # Tạo tables nếu chưa có (Development only)
        # Production: Sử dụng Alembic migrations
        print("\n📦 Creating database tables...")
        try:
            create_tables()
            print("✅ Database tables ready!")
        except Exception as e:
            print(f"⚠️  Table creation warning: {str(e)}")
            print("💡 Tables might already exist (this is OK)")
    else:
        print("⚠️  Database not connected!")
        print("💡 Server will run but database features disabled")
        print("💡 Check your DATABASE_URL in .env file")
    
    print("=" * 60 + "\n")

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

