"""
Script test database connection và CRUD operations
"""

from database import SessionLocal, check_database_connection
from services.db_service import (
    create_user,
    get_user_by_username,
    create_recognition_record,
    get_all_history,
    get_user_statistics
)
from datetime import datetime
import json

def test_connection():
    """Test database connection"""
    print("🔌 Testing database connection...")
    if check_database_connection():
        print("✅ Connection successful!\n")
        return True
    else:
        print("❌ Connection failed!\n")
        return False

def test_user_crud():
    """Test User CRUD operations"""
    print("👤 Testing User CRUD...")
    db = SessionLocal()
    
    try:
        # Create user
        user = create_user(
            db=db,
            username="testuser",
            email="test@example.com",
            hashed_password="hashed_password_here",
            full_name="Test User"
        )
        print(f"✅ Created user: {user.username} (ID: {user.id})")
        
        # Get user
        found_user = get_user_by_username(db, "testuser")
        print(f"✅ Found user: {found_user.email}")
        
        # Delete user (cleanup)
        db.delete(user)
        db.commit()
        print("✅ User CRUD test passed!\n")
        
    except Exception as e:
        print(f"❌ User CRUD test failed: {str(e)}\n")
    finally:
        db.close()

def test_recognition_crud():
    """Test Recognition History CRUD operations"""
    print("📸 Testing Recognition History CRUD...")
    db = SessionLocal()
    
    try:
        # Sample recognition result
        recognition_data = {
            "transaction_id": "test-123-456",
            "image_url": "/uploads/test.jpg",
            "people_count": 2,
            "genders": [
                {"person_id": 1, "gender": "male", "confidence": 0.95, "bbox": [100, 100, 200, 400]},
                {"person_id": 2, "gender": "female", "confidence": 0.92, "bbox": [300, 100, 200, 400]}
            ],
            "colors": [
                {"person_id": 1, "color": "Xanh dương", "hex": "#0000FF", "confidence": 0.88},
                {"person_id": 2, "color": "Đỏ", "hex": "#FF0000", "confidence": 0.85}
            ],
            "weather": {"condition": "sunny", "confidence": 0.9},
            "objects": [
                {"class": "chair", "ten_tieng_viet": "Ghế", "confidence": 0.87, "bbox": [50, 200, 100, 150]},
                {"class": "table", "ten_tieng_viet": "Bàn", "confidence": 0.82, "bbox": [200, 300, 300, 200]}
            ],
            "processing_time": 1.23,
            "status": "success"
        }
        
        # Create record
        record = create_recognition_record(
            db=db,
            transaction_id="test-123-456",
            image_filename="test.jpg",
            image_path="/uploads/test.jpg",
            recognition_result=recognition_data,
            user_id=None
        )
        print(f"✅ Created recognition record (ID: {record.id})")
        
        # Get history
        history = get_all_history(db, limit=10)
        print(f"✅ Found {len(history)} records in history")
        
        # Get statistics
        from models import RecognitionHistory
        from sqlalchemy import func
        
        total = db.query(func.count(RecognitionHistory.id)).scalar()
        print(f"✅ Total records in database: {total}")
        
        # Delete record (cleanup)
        db.delete(record)
        db.commit()
        print("✅ Recognition CRUD test passed!\n")
        
    except Exception as e:
        print(f"❌ Recognition CRUD test failed: {str(e)}\n")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🧪 DATABASE TESTS")
    print("=" * 60 + "\n")
    
    if not test_connection():
        print("❌ Cannot proceed without database connection")
        return
    
    test_user_crud()
    test_recognition_crud()
    
    print("=" * 60)
    print("✅ ALL TESTS COMPLETED!")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    run_all_tests()

