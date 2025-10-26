"""
Database Models - SQLAlchemy ORM
Định nghĩa cấu trúc tables trong PostgreSQL
"""

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, 
    Boolean, Text, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from database import Base

# ==================== USER MODEL ====================

class User(Base):
    """
    Model người dùng
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100))
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    recognition_history = relationship(
        "RecognitionHistory",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

# ==================== RECOGNITION HISTORY MODEL ====================

class RecognitionHistory(Base):
    """
    Lịch sử nhận dạng ảnh
    Lưu tất cả các lần người dùng upload và nhận dạng ảnh
    """
    __tablename__ = "recognition_history"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(100), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Nullable nếu cho phép anonymous
    
    # Thông tin ảnh
    image_filename = Column(String(255), nullable=False)
    image_path = Column(String(500), nullable=False)
    image_url = Column(String(500))
    image_size_kb = Column(Float)  # Kích thước file (KB)
    image_width = Column(Integer)  # Độ rộng ảnh
    image_height = Column(Integer)  # Độ cao ảnh
    
    # Kết quả nhận dạng
    people_count = Column(Integer, default=0)
    genders = Column(JSON)  # Lưu danh sách giới tính
    colors = Column(JSON)  # Lưu danh sách màu áo
    weather = Column(JSON)  # Thông tin thời tiết/phong cảnh
    objects = Column(JSON)  # Danh sách vật dụng
    
    # Metadata
    processing_time = Column(Float)  # Thời gian xử lý (seconds)
    status = Column(String(20), default="success")  # success, failed, processing
    error_message = Column(Text)  # Lỗi nếu có
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="recognition_history")
    detected_persons = relationship(
        "DetectedPerson",
        back_populates="recognition",
        cascade="all, delete-orphan"
    )
    detected_objects = relationship(
        "DetectedObject",
        back_populates="recognition",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<RecognitionHistory(id={self.id}, transaction_id='{self.transaction_id}')>"

# ==================== DETECTED PERSON MODEL ====================

class DetectedPerson(Base):
    """
    Chi tiết người được nhận dạng trong ảnh
    """
    __tablename__ = "detected_persons"
    
    id = Column(Integer, primary_key=True, index=True)
    recognition_id = Column(
        Integer,
        ForeignKey("recognition_history.id"),
        nullable=False
    )
    
    # Thông tin người
    person_id = Column(Integer)  # ID người trong ảnh (person 1, 2, 3...)
    gender = Column(String(20))  # male, female, unknown
    gender_confidence = Column(Float)  # Độ tin cậy
    
    # Bounding box
    bbox_x = Column(Float)
    bbox_y = Column(Float)
    bbox_width = Column(Float)
    bbox_height = Column(Float)
    
    # Màu áo
    clothing_color = Column(String(50))  # Tên màu
    clothing_color_hex = Column(String(10))  # Mã hex
    color_confidence = Column(Float)
    
    # Relationship
    recognition = relationship("RecognitionHistory", back_populates="detected_persons")
    
    def __repr__(self):
        return f"<DetectedPerson(id={self.id}, gender='{self.gender}')>"

# ==================== DETECTED OBJECT MODEL ====================

class DetectedObject(Base):
    """
    Chi tiết vật dụng được nhận dạng trong ảnh
    """
    __tablename__ = "detected_objects"
    
    id = Column(Integer, primary_key=True, index=True)
    recognition_id = Column(
        Integer,
        ForeignKey("recognition_history.id"),
        nullable=False
    )
    
    # Thông tin vật dụng
    object_class = Column(String(100))  # Loại vật dụng (chair, table, phone...)
    object_name_vi = Column(String(100))  # Tên tiếng Việt
    confidence = Column(Float)  # Độ tin cậy
    
    # Bounding box
    bbox_x = Column(Float)
    bbox_y = Column(Float)
    bbox_width = Column(Float)
    bbox_height = Column(Float)
    
    # Relationship
    recognition = relationship("RecognitionHistory", back_populates="detected_objects")
    
    def __repr__(self):
        return f"<DetectedObject(id={self.id}, object_class='{self.object_class}')>"

# ==================== STATISTICS MODEL ====================

class DailyStatistics(Base):
    """
    Thống kê hàng ngày
    Lưu số lượng nhận dạng, thời gian xử lý trung bình, etc.
    """
    __tablename__ = "daily_statistics"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Thống kê
    total_recognitions = Column(Integer, default=0)
    total_people_detected = Column(Integer, default=0)
    total_objects_detected = Column(Integer, default=0)
    avg_processing_time = Column(Float)  # Seconds
    
    # Breakdown
    male_count = Column(Integer, default=0)
    female_count = Column(Integer, default=0)
    most_common_objects = Column(JSON)  # Top 10 vật dụng phổ biến
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<DailyStatistics(date={self.date}, total={self.total_recognitions})>"

# ==================== SYSTEM LOG MODEL ====================

class SystemLog(Base):
    """
    Log hệ thống
    Lưu lại các hoạt động, lỗi, cảnh báo
    """
    __tablename__ = "system_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20), index=True)  # INFO, WARNING, ERROR, CRITICAL
    message = Column(Text, nullable=False)
    module = Column(String(100))  # Module gây ra log
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    ip_address = Column(String(50))
    user_agent = Column(String(500))
    request_path = Column(String(500))
    
    # Metadata
    extra_data = Column(JSON)  # Thông tin thêm
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<SystemLog(id={self.id}, level='{self.level}')>"

