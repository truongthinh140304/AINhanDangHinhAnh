# -*- coding: utf-8 -*-
"""
Database Configuration và Session Management
Sử dụng SQLAlchemy ORM với PostgreSQL
"""

from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL từ environment variable
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/nhandanghinhanh"
)

# Tạo engine
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries (tắt trong production)
    pool_pre_ping=True,  # Kiểm tra connection trước khi dùng
    pool_size=10,  # Số connection trong pool
    max_overflow=20  # Số connection tối đa khi pool đầy
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class cho models
Base = declarative_base()

# Dependency để lấy database session
def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency để lấy database session
    
    Yields:
        Session: Database session
        
    Example:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            users = db.query(User).all()
            return users
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Hàm kiểm tra kết nối database
def check_database_connection() -> bool:
    """
    Kiểm tra kết nối database
    
    Returns:
        bool: True nếu kết nối thành công
    """
    try:
        # Thử tạo session và query đơn giản
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        print("[OK] Database connection successful!")
        return True
    except Exception as e:
        print(f"[X] Database connection failed: {str(e)}")
        return False

# Hàm tạo tables
def create_tables():
    """
    Tạo tất cả tables trong database
    Chỉ dùng cho development, production nên dùng Alembic migrations
    """
    try:
        Base.metadata.create_all(bind=engine)
        print("[OK] All tables created successfully!")
    except Exception as e:
        print(f"[X] Error creating tables: {str(e)}")

# Hàm xóa tất cả tables (cẩn thận!)
def drop_tables():
    """
    XÓA tất cả tables trong database
    [!] CANH BAO: Chi dung cho development!
    """
    try:
        Base.metadata.drop_all(bind=engine)
        print("[OK] All tables dropped!")
    except Exception as e:
        print(f"[X] Error dropping tables: {str(e)}")

