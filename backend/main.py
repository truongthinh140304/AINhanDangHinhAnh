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
import cv2
import sys

# Import database
try:
    # Khi chạy theo dạng package: uvicorn backend.main:app
    from .database import get_db, check_database_connection, create_tables
    from .models import RecognitionHistory, User
    from .services.db_service import (
        create_recognition_record,
        get_user_history,
        get_all_history,
        delete_recognition,
        get_user_statistics,
        create_log
    )
    from .modules.nhan_dang_gioi_tinh import nhan_dang_gioi_tinh_tu_anh
    from .modules.nhan_dang_mau_sac import nhan_dang_mau_ao
    from .modules.nhan_dang_thoi_tiet import phan_tich_thoi_tiet
    from .modules.nhan_dang_vat_dung import nhan_dang_vat_dung
except ImportError:
    # Khi chạy trực tiếp trong thư mục backend: uvicorn main:app hoặc python main.py
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

# ==================== HELPERS ====================

def safe_print(*args, **kwargs):
    """In an toàn trên Windows console không hỗ trợ emoji/UTF-8."""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        sanitized_args = []
        for arg in args:
            if isinstance(arg, str):
                try:
                    sanitized_args.append(arg.encode(sys.stdout.encoding or 'ascii', errors='ignore').decode(sys.stdout.encoding or 'ascii'))
                except Exception:
                    sanitized_args.append(arg.encode('ascii', errors='ignore').decode('ascii'))
            else:
                sanitized_args.append(str(arg))
        try:
            print(*sanitized_args, **kwargs)
        except Exception:
            # Nếu vẫn lỗi, bỏ qua để không làm sập server
            pass

def _detect_people_simple(image_path: str):
    """Phát hiện nhiều người bằng HOG+SVM (OpenCV) để lấy danh sách bbox.
    Trả về: List[dict] với khóa "bbox" (x1,y1,x2,y2) và "confidence" ~0.6-0.9.
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            return []

        # Chuẩn bị detector HOG người
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        # Resize nhẹ để tăng tốc nhưng giữ tỉ lệ
        height, width = img.shape[:2]
        scale = 640.0 / max(height, width)
        scale = min(1.0, scale)
        resized = cv2.resize(img, (int(width * scale), int(height * scale))) if scale < 1.0 else img

        # Phát hiện
        rects, weights = hog.detectMultiScale(
            resized,
            winStride=(8, 8),
            padding=(8, 8),
            scale=1.05
        )

        results = []
        for (x, y, w, h), conf in zip(rects, weights):
            # Map to toạ độ ảnh gốc
            if scale < 1.0:
                x1 = int(x / scale)
                y1 = int(y / scale)
                x2 = int((x + w) / scale)
                y2 = int((y + h) / scale)
            else:
                x1, y1, x2, y2 = int(x), int(y), int(x + w), int(y + h)

            # Lọc bbox nhỏ bất thường
            if (x2 - x1) * (y2 - y1) < 0.005 * (width * height):
                continue

            results.append({
                "bbox": [max(0, x1), max(0, y1), min(width - 1, x2), min(height - 1, y2)],
                "confidence": float(min(0.99, max(0.6, conf)))
            })

        # Nếu không phát hiện được người nào, fallback về bbox trung tâm để không làm trống kết quả demo
        if not results:
            margin_x = int(width * 0.1)
            margin_y = int(height * 0.05)
            x1 = max(0, margin_x)
            y1 = max(0, margin_y)
            x2 = min(width - 1, width - margin_x)
            y2 = min(height - 1, height - margin_y)
            if x2 > x1 and y2 > y1:
                results = [{"bbox": [x1, y1, x2, y2], "confidence": 0.5}]

        return results
    except Exception:
        return []

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
        # Kiểm tra file type (an toàn với trường hợp client không gửi content_type)
        content_type = getattr(file, "content_type", None)
        if content_type:
            if not content_type.startswith("image/"):
                raise HTTPException(
                    status_code=400,
                    detail="File phải là ảnh (jpg, png, ...)"
                )
        else:
            # Fallback: kiểm tra theo phần mở rộng tên file
            ext = os.path.splitext(file.filename or "")[1].lower()
            allowed_exts = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tif", ".tiff"}
            if ext not in allowed_exts:
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
        
        # 1. Phát hiện người (bbox đơn giản) và nhận dạng giới tính
        people_boxes = _detect_people_simple(temp_path)
        gender_results = nhan_dang_gioi_tinh_tu_anh(temp_path, people_boxes)

        # 2. Nhận dạng màu áo dựa trên cùng bbox danh sách
        color_results = nhan_dang_mau_ao(temp_path, people_boxes)
        
        # 3. Nhận dạng thời tiết/phong cảnh
        weather_result = phan_tich_thoi_tiet(temp_path)
        
        # 4. Nhận dạng vật dụng
        object_results = nhan_dang_vat_dung(temp_path)

        # 4.2 Gán vật dụng theo từng người (carried_by_person) dựa trên giao cắt bbox
        try:
            def iou(a, b):
                ax1, ay1, ax2, ay2 = a
                bx1, by1, bx2, by2 = b
                inter_x1 = max(ax1, bx1)
                inter_y1 = max(ay1, by1)
                inter_x2 = min(ax2, bx2)
                inter_y2 = min(ay2, by2)
                if inter_x2 <= inter_x1 or inter_y2 <= inter_y1:
                    return 0.0
                inter = (inter_x2 - inter_x1) * (inter_y2 - inter_y1)
                area_a = max(0, ax2 - ax1) * max(0, ay2 - ay1)
                area_b = max(0, bx2 - bx1) * max(0, by2 - by1)
                union = area_a + area_b - inter
                return float(inter / union) if union > 0 else 0.0

            carried_set = {"umbrella", "handbag", "backpack", "tie", "suitcase", "cell phone", "book"}

            # Chuẩn bị map người
            person_map = {}
            for p in gender_results or []:
                pid = p.get("person_id")
                if pid is None:
                    continue
                person_map[pid] = {
                    "bbox": p.get("bbox"),
                    "items": []
                }

            # Gán vật dụng
            for obj in object_results or []:
                cls = str(obj.get("object_class", "")).lower()
                if cls not in carried_set:
                    continue
                obox = obj.get("bbox") or [0, 0, 0, 0]
                best_pid = None
                best_score = 0.0
                for pid, info in person_map.items():
                    pb = info.get("bbox") or [0, 0, 0, 0]
                    score = iou(obox, pb)
                    if score > best_score:
                        best_score = score
                        best_pid = pid
                # Ngưỡng IOU thấp để chấp nhận bên trong bbox
                if best_pid is not None and best_score > 0.01:
                    person_map[best_pid]["items"].append(obj)

            # Nhúng vào gender_results (giữ nguyên API hiện tại, thêm khóa mới)
            for p in gender_results or []:
                pid = p.get("person_id")
                items = person_map.get(pid, {}).get("items", [])
                if items:
                    p["carried_items"] = [
                        {
                            "object_class": it.get("object_class"),
                            "ten_tieng_viet": it.get("ten_tieng_viet"),
                            "confidence": it.get("confidence"),
                            "bbox": it.get("bbox"),
                        }
                        for it in items
                    ]
        except Exception:
            pass

        # 4.1 Gắn thông tin vật dụng cầm theo vào phần thời tiết (nếu có)
        try:
            carried_keywords = {
                "umbrella", "handbag", "backpack", "tie", "suitcase", "cell phone", "book"
            }
            # Dựa trên tên class tiếng Anh, dùng tên tiếng Việt để hiển thị
            summary_counts = {}
            for obj in (object_results or []):
                cls = str(obj.get("object_class", "")).lower()
                if cls in carried_keywords:
                    name_vi = obj.get("ten_tieng_viet") or cls
                    summary_counts[name_vi] = summary_counts.get(name_vi, 0) + 1

            carried_items_list = [
                {"name": name, "count": count} for name, count in summary_counts.items()
            ]

            if isinstance(weather_result, dict):
                weather_result["carried_items"] = carried_items_list
                if carried_items_list:
                    parts = [
                        f"{item['count']} {item['name']}" if item['count'] > 1 else item['name']
                        for item in carried_items_list
                    ]
                    weather_result["carried_summary"] = ", ".join(parts)
                else:
                    weather_result["carried_summary"] = ""
        except Exception:
            # Không chặn pipeline nếu phần tổng hợp vật dụng lỗi
            pass
        
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
    safe_print("=" * 60)
    safe_print("Backend API Server Started!")
    safe_print("=" * 60)
    safe_print(f"Server running at: http://localhost:8000")
    safe_print(f"API Documentation: http://localhost:8000/docs")
    safe_print(f"Alternative docs: http://localhost:8000/redoc")
    safe_print("=" * 60)
    
    # Kiểm tra kết nối database
    safe_print("\nChecking database connection...")
    db_connected = check_database_connection()
    
    if db_connected:
        safe_print("Database connected successfully!")
        
        # Tạo tables nếu chưa có (Development only)
        # Production: Sử dụng Alembic migrations
        safe_print("\nCreating database tables...")
        try:
            create_tables()
            safe_print("Database tables ready!")
        except Exception as e:
            safe_print(f"Table creation warning: {str(e)}")
            safe_print("Tables might already exist (this is OK)")
    else:
        safe_print("Database not connected!")
        safe_print("Server will run but database features disabled")
        safe_print("Check your DATABASE_URL in .env file")
    
    safe_print("=" * 60 + "\n")

@app.on_event("shutdown")
async def shutdown_event():
    """Tắt server"""
    safe_print("Backend API Server Stopped!")

# ==================== RUN ====================

if __name__ == "__main__":
    import uvicorn
    
    safe_print("\n" + "=" * 60)
    safe_print("Starting Backend API Server...")
    safe_print("=" * 60 + "\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload khi code thay đổi
        log_level="info"
    )

