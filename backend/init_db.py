# -*- coding: utf-8 -*-
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
    print("[*] DATABASE INITIALIZATION")
    print("=" * 60)
    
    # Kiểm tra kết nối
    print("\n[1] Checking database connection...")
    if not check_database_connection():
        print("[X] Cannot connect to database!")
        print("\n[!] Troubleshooting:")
        print("  1. Make sure PostgreSQL is running")
        print("  2. Check .env file for correct DATABASE_URL")
        print("  3. Verify username, password, and database name")
        sys.exit(1)
    
    print("[OK] Database connection OK!")
    
    # Tạo tables
    print("\n[2] Creating tables...")
    try:
        create_tables()
        print("[OK] All tables created successfully!")
        
        print("\n[+] Created tables:")
        print("  [OK] users")
        print("  [OK] recognition_history")
        print("  [OK] detected_persons")
        print("  [OK] detected_objects")
        print("  [OK] daily_statistics")
        print("  [OK] system_logs")
        
    except Exception as e:
        print(f"[X] Error creating tables: {str(e)}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("[OK] DATABASE INITIALIZATION COMPLETE!")
    print("=" * 60)
    print("\n[!] Next steps:")
    print("  1. Run backend server: python main.py")
    print("  2. Test API: http://localhost:8000/docs")
    print("=" * 60 + "\n")

def reset_database():
    """
    XÓA và tạo lại tất cả tables
    [!] CANH BAO: Se XOA TAT CA DU LIEU!
    """
    print("=" * 60)
    print("[!] DATABASE RESET")
    print("=" * 60)
    print("\n[!!] WARNING: This will DELETE ALL DATA!")
    
    confirm = input("\nType 'YES' to confirm: ")
    
    if confirm != "YES":
        print("[X] Reset cancelled")
        return
    
    print("\n[1] Dropping all tables...")
    try:
        drop_tables()
        print("[OK] All tables dropped!")
    except Exception as e:
        print(f"[X] Error dropping tables: {str(e)}")
        sys.exit(1)
    
    print("\n[2] Creating tables...")
    try:
        create_tables()
        print("[OK] All tables created!")
    except Exception as e:
        print(f"[X] Error creating tables: {str(e)}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("[OK] DATABASE RESET COMPLETE!")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_database()
    else:
        init_database()

