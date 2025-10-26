"""
Database Service Layer
CRUD operations và business logic cho database
"""

from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from models import (
    User, RecognitionHistory, DetectedPerson,
    DetectedObject, DailyStatistics, SystemLog
)
import json

# ==================== USER CRUD ====================

def create_user(
    db: Session,
    username: str,
    email: str,
    hashed_password: str,
    full_name: Optional[str] = None
) -> User:
    """Tạo user mới"""
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        full_name=full_name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Lấy user theo username"""
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Lấy user theo email"""
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Lấy user theo ID"""
    return db.query(User).filter(User.id == user_id).first()

# ==================== RECOGNITION HISTORY CRUD ====================

def create_recognition_record(
    db: Session,
    transaction_id: str,
    image_filename: str,
    image_path: str,
    recognition_result: Dict[str, Any],
    user_id: Optional[int] = None
) -> RecognitionHistory:
    """
    Tạo record lịch sử nhận dạng
    
    Args:
        db: Database session
        transaction_id: UUID của transaction
        image_filename: Tên file ảnh
        image_path: Đường dẫn file
        recognition_result: Kết quả nhận dạng từ API
        user_id: ID người dùng (optional)
    
    Returns:
        RecognitionHistory: Record đã tạo
    """
    record = RecognitionHistory(
        transaction_id=transaction_id,
        user_id=user_id,
        image_filename=image_filename,
        image_path=image_path,
        image_url=recognition_result.get('image_url'),
        people_count=recognition_result.get('people_count', 0),
        genders=recognition_result.get('genders', []),
        colors=recognition_result.get('colors', []),
        weather=recognition_result.get('weather', {}),
        objects=recognition_result.get('objects', []),
        processing_time=recognition_result.get('processing_time'),
        status=recognition_result.get('status', 'success')
    )
    
    db.add(record)
    db.commit()
    db.refresh(record)
    
    # Tạo các records chi tiết
    _create_detected_persons(db, record.id, recognition_result)
    _create_detected_objects(db, record.id, recognition_result)
    
    return record

def _create_detected_persons(
    db: Session,
    recognition_id: int,
    recognition_result: Dict[str, Any]
):
    """Tạo records cho người được phát hiện"""
    genders = recognition_result.get('genders', [])
    colors = recognition_result.get('colors', [])
    
    for gender_info in genders:
        # Tìm màu tương ứng
        color_info = next(
            (c for c in colors if c.get('person_id') == gender_info.get('person_id')),
            {}
        )
        
        person = DetectedPerson(
            recognition_id=recognition_id,
            person_id=gender_info.get('person_id'),
            gender=gender_info.get('gender'),
            gender_confidence=gender_info.get('confidence'),
            bbox_x=gender_info.get('bbox', [None])[0],
            bbox_y=gender_info.get('bbox', [None, None])[1] if len(gender_info.get('bbox', [])) > 1 else None,
            bbox_width=gender_info.get('bbox', [None, None, None])[2] if len(gender_info.get('bbox', [])) > 2 else None,
            bbox_height=gender_info.get('bbox', [None, None, None, None])[3] if len(gender_info.get('bbox', [])) > 3 else None,
            clothing_color=color_info.get('color'),
            clothing_color_hex=color_info.get('hex'),
            color_confidence=color_info.get('confidence')
        )
        db.add(person)
    
    db.commit()

def _create_detected_objects(
    db: Session,
    recognition_id: int,
    recognition_result: Dict[str, Any]
):
    """Tạo records cho vật dụng được phát hiện"""
    objects = recognition_result.get('objects', [])
    
    for obj_info in objects:
        obj = DetectedObject(
            recognition_id=recognition_id,
            object_class=obj_info.get('class'),
            object_name_vi=obj_info.get('ten_tieng_viet'),
            confidence=obj_info.get('confidence'),
            bbox_x=obj_info.get('bbox', [None])[0],
            bbox_y=obj_info.get('bbox', [None, None])[1] if len(obj_info.get('bbox', [])) > 1 else None,
            bbox_width=obj_info.get('bbox', [None, None, None])[2] if len(obj_info.get('bbox', [])) > 2 else None,
            bbox_height=obj_info.get('bbox', [None, None, None, None])[3] if len(obj_info.get('bbox', [])) > 3 else None
        )
        db.add(obj)
    
    db.commit()

def get_recognition_by_transaction_id(
    db: Session,
    transaction_id: str
) -> Optional[RecognitionHistory]:
    """Lấy recognition record theo transaction ID"""
    return db.query(RecognitionHistory).filter(
        RecognitionHistory.transaction_id == transaction_id
    ).first()

def get_user_history(
    db: Session,
    user_id: int,
    limit: int = 50,
    offset: int = 0
) -> List[RecognitionHistory]:
    """
    Lấy lịch sử nhận dạng của user
    
    Args:
        db: Database session
        user_id: ID người dùng
        limit: Số records tối đa
        offset: Vị trí bắt đầu
    
    Returns:
        List[RecognitionHistory]: Danh sách lịch sử
    """
    return db.query(RecognitionHistory)\
        .filter(RecognitionHistory.user_id == user_id)\
        .order_by(RecognitionHistory.created_at.desc())\
        .limit(limit)\
        .offset(offset)\
        .all()

def get_all_history(
    db: Session,
    limit: int = 50,
    offset: int = 0
) -> List[RecognitionHistory]:
    """
    Lấy tất cả lịch sử nhận dạng (admin)
    
    Args:
        db: Database session
        limit: Số records tối đa
        offset: Vị trí bắt đầu
    
    Returns:
        List[RecognitionHistory]: Danh sách lịch sử
    """
    return db.query(RecognitionHistory)\
        .order_by(RecognitionHistory.created_at.desc())\
        .limit(limit)\
        .offset(offset)\
        .all()

def delete_recognition(db: Session, transaction_id: str) -> bool:
    """
    Xóa recognition record
    
    Args:
        db: Database session
        transaction_id: UUID của transaction
    
    Returns:
        bool: True nếu xóa thành công
    """
    record = get_recognition_by_transaction_id(db, transaction_id)
    if record:
        db.delete(record)
        db.commit()
        return True
    return False

# ==================== STATISTICS ====================

def get_user_statistics(db: Session, user_id: int) -> Dict[str, Any]:
    """
    Lấy thống kê của user
    
    Returns:
        Dict với:
        - total_recognitions: Tổng số lần nhận dạng
        - total_people: Tổng số người phát hiện
        - total_objects: Tổng số vật dụng
        - avg_processing_time: Thời gian xử lý trung bình
        - most_common_objects: Top 10 vật dụng phổ biến
    """
    records = db.query(RecognitionHistory).filter(
        RecognitionHistory.user_id == user_id
    ).all()
    
    if not records:
        return {
            "total_recognitions": 0,
            "total_people": 0,
            "total_objects": 0,
            "avg_processing_time": 0,
            "most_common_objects": []
        }
    
    total_people = sum(r.people_count for r in records)
    total_objects = sum(len(r.objects) if r.objects else 0 for r in records)
    avg_time = sum(r.processing_time for r in records if r.processing_time) / len(records)
    
    # Đếm vật dụng phổ biến
    object_counter = {}
    for record in records:
        if record.objects:
            for obj in record.objects:
                obj_class = obj.get('class', 'unknown')
                object_counter[obj_class] = object_counter.get(obj_class, 0) + 1
    
    most_common = sorted(
        object_counter.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]
    
    return {
        "total_recognitions": len(records),
        "total_people": total_people,
        "total_objects": total_objects,
        "avg_processing_time": round(avg_time, 2),
        "most_common_objects": [
            {"object": obj, "count": count}
            for obj, count in most_common
        ]
    }

def update_daily_statistics(db: Session, date: datetime):
    """
    Cập nhật thống kê hàng ngày
    
    Args:
        db: Database session
        date: Ngày cần thống kê
    """
    # Lấy tất cả records trong ngày
    start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = start_date + timedelta(days=1)
    
    records = db.query(RecognitionHistory).filter(
        RecognitionHistory.created_at >= start_date,
        RecognitionHistory.created_at < end_date
    ).all()
    
    if not records:
        return
    
    # Tính toán
    total_recognitions = len(records)
    total_people = sum(r.people_count for r in records)
    total_objects = sum(len(r.objects) if r.objects else 0 for r in records)
    avg_time = sum(r.processing_time for r in records if r.processing_time) / len(records)
    
    # Đếm giới tính
    male_count = 0
    female_count = 0
    for record in records:
        if record.genders:
            for gender_info in record.genders:
                if gender_info.get('gender') == 'male':
                    male_count += 1
                elif gender_info.get('gender') == 'female':
                    female_count += 1
    
    # Vật dụng phổ biến
    object_counter = {}
    for record in records:
        if record.objects:
            for obj in record.objects:
                obj_class = obj.get('class', 'unknown')
                object_counter[obj_class] = object_counter.get(obj_class, 0) + 1
    
    most_common = sorted(
        object_counter.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]
    
    # Tạo hoặc update record
    stat = db.query(DailyStatistics).filter(
        DailyStatistics.date == start_date
    ).first()
    
    if stat:
        # Update
        stat.total_recognitions = total_recognitions
        stat.total_people_detected = total_people
        stat.total_objects_detected = total_objects
        stat.avg_processing_time = avg_time
        stat.male_count = male_count
        stat.female_count = female_count
        stat.most_common_objects = [
            {"object": obj, "count": count}
            for obj, count in most_common
        ]
    else:
        # Create
        stat = DailyStatistics(
            date=start_date,
            total_recognitions=total_recognitions,
            total_people_detected=total_people,
            total_objects_detected=total_objects,
            avg_processing_time=avg_time,
            male_count=male_count,
            female_count=female_count,
            most_common_objects=[
                {"object": obj, "count": count}
                for obj, count in most_common
            ]
        )
        db.add(stat)
    
    db.commit()

# ==================== SYSTEM LOG ====================

def create_log(
    db: Session,
    level: str,
    message: str,
    module: Optional[str] = None,
    user_id: Optional[int] = None,
    extra_data: Optional[Dict] = None
) -> SystemLog:
    """
    Tạo system log
    
    Args:
        db: Database session
        level: INFO, WARNING, ERROR, CRITICAL
        message: Nội dung log
        module: Module gây ra log
        user_id: ID người dùng
        extra_data: Dữ liệu thêm
    """
    log = SystemLog(
        level=level,
        message=message,
        module=module,
        user_id=user_id,
        extra_data=extra_data
    )
    db.add(log)
    db.commit()
    return log

def get_recent_logs(
    db: Session,
    limit: int = 100,
    level: Optional[str] = None
) -> List[SystemLog]:
    """
    Lấy logs gần đây
    
    Args:
        db: Database session
        limit: Số logs tối đa
        level: Lọc theo level (optional)
    
    Returns:
        List[SystemLog]: Danh sách logs
    """
    query = db.query(SystemLog)
    
    if level:
        query = query.filter(SystemLog.level == level)
    
    return query.order_by(SystemLog.created_at.desc()).limit(limit).all()

