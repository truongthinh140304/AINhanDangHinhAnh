"""
Script khởi tạo database
Chạy file này để tạo tất cả tables trong PostgreSQL
"""

from database import create_tables, check_database_connection, drop_tables
from models import *  # Import tất cả models
import sys

def init_database():
    """Khởi tạo database"""
    print("=" * 60)
    print("🔧 DATABASE INITIALIZATION")
    print("=" * 60)
    
    # Kiểm tra kết nối
    print("\n1️⃣ Checking database connection...")
    if not check_database_connection():
        print("❌ Cannot connect to database!")
        print("\n💡 Troubleshooting:")
        print("  1. Make sure PostgreSQL is running")
        print("  2. Check .env file for correct DATABASE_URL")
        print("  3. Verify username, password, and database name")
        sys.exit(1)
    
    print("✅ Database connection OK!")
    
    # Tạo tables
    print("\n2️⃣ Creating tables...")
    try:
        create_tables()
        print("✅ All tables created successfully!")
        
        print("\n📋 Created tables:")
        print("  ✅ users")
        print("  ✅ recognition_history")
        print("  ✅ detected_persons")
        print("  ✅ detected_objects")
        print("  ✅ daily_statistics")
        print("  ✅ system_logs")
        
    except Exception as e:
        print(f"❌ Error creating tables: {str(e)}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ DATABASE INITIALIZATION COMPLETE!")
    print("=" * 60)
    print("\n💡 Next steps:")
    print("  1. Run backend server: python main.py")
    print("  2. Test API: http://localhost:8000/docs")
    print("=" * 60 + "\n")

def reset_database():
    """
    XÓA và tạo lại tất cả tables
    ⚠️ CẢNH BÁO: Sẽ XÓA TẤT CẢ DỮ LIỆU!
    """
    print("=" * 60)
    print("⚠️  DATABASE RESET")
    print("=" * 60)
    print("\n🚨 WARNING: This will DELETE ALL DATA!")
    
    confirm = input("\nType 'YES' to confirm: ")
    
    if confirm != "YES":
        print("❌ Reset cancelled")
        return
    
    print("\n1️⃣ Dropping all tables...")
    try:
        drop_tables()
        print("✅ All tables dropped!")
    except Exception as e:
        print(f"❌ Error dropping tables: {str(e)}")
        sys.exit(1)
    
    print("\n2️⃣ Creating tables...")
    try:
        create_tables()
        print("✅ All tables created!")
    except Exception as e:
        print(f"❌ Error creating tables: {str(e)}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ DATABASE RESET COMPLETE!")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_database()
    else:
        init_database()

