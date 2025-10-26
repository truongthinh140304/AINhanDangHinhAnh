"""
Test PostgreSQL Connection - Nhanh và đơn giản
Script này test kết nối PostgreSQL mà không cần import model phức tạp
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def test_basic_connection():
    """Test kết nối PostgreSQL cơ bản"""
    print("=" * 60)
    print("🐘 POSTGRESQL CONNECTION TEST")
    print("=" * 60)
    
    # Lấy DATABASE_URL từ .env
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/nhandanghinhanh"
    )
    
    print(f"\n📌 Database URL:")
    # Ẩn password khi hiển thị
    safe_url = database_url.replace(":postgres@", ":****@")
    print(f"   {safe_url}")
    
    # Test 1: Import psycopg2
    print("\n1️⃣ Testing psycopg2 import...")
    try:
        import psycopg2
        print("   ✅ psycopg2 imported successfully!")
    except ImportError:
        print("   ❌ psycopg2 not found!")
        print("   💡 Fix: pip install psycopg2-binary")
        return False
    
    # Test 2: Parse DATABASE_URL
    print("\n2️⃣ Parsing database URL...")
    try:
        from urllib.parse import urlparse
        result = urlparse(database_url)
        
        username = result.username
        password = result.password
        host = result.hostname
        port = result.port
        database = result.path[1:]  # Remove leading '/'
        
        print(f"   Host: {host}")
        print(f"   Port: {port}")
        print(f"   Database: {database}")
        print(f"   Username: {username}")
        print(f"   Password: {'*' * len(password) if password else 'None'}")
        print("   ✅ URL parsed successfully!")
        
    except Exception as e:
        print(f"   ❌ Error parsing URL: {str(e)}")
        return False
    
    # Test 3: Connect to PostgreSQL
    print("\n3️⃣ Connecting to PostgreSQL...")
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password
        )
        print("   ✅ Connection established!")
        
        # Test 4: Execute simple query
        print("\n4️⃣ Testing database query...")
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"   PostgreSQL version: {version[0][:50]}...")
        print("   ✅ Query executed successfully!")
        
        # Test 5: List tables
        print("\n5️⃣ Checking tables...")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        if tables:
            print(f"   Found {len(tables)} table(s):")
            for table in tables:
                print(f"   ✅ {table[0]}")
        else:
            print("   ⚠️  No tables found (database is empty)")
            print("   💡 Run: python init_db.py")
        
        # Close connection
        cursor.close()
        conn.close()
        print("\n   ✅ Connection closed!")
        
        # Success
        print("\n" + "=" * 60)
        print("✅ POSTGRESQL CONNECTION TEST: PASSED!")
        print("=" * 60)
        print("\n💡 Next steps:")
        print("   1. Create tables: python init_db.py")
        print("   2. Test full database: python test_db.py")
        print("   3. Run server: python main.py")
        print()
        
        return True
        
    except psycopg2.OperationalError as e:
        print(f"   ❌ Connection failed: {str(e)}")
        print("\n" + "=" * 60)
        print("❌ CONNECTION ERROR - TROUBLESHOOTING")
        print("=" * 60)
        
        if "password authentication failed" in str(e):
            print("\n🔒 Password incorrect!")
            print("   → Check password in .env file")
            print("   → Make sure it matches PostgreSQL password")
            
        elif "database" in str(e) and "does not exist" in str(e):
            print("\n💾 Database does not exist!")
            print("   → Create database: CREATE DATABASE nhandanghinhanh;")
            print("   → Or use pgAdmin to create it")
            
        elif "could not connect" in str(e) or "Connection refused" in str(e):
            print("\n🔌 Cannot connect to PostgreSQL!")
            print("   → Make sure PostgreSQL is running")
            print("   → Windows: services.msc → postgresql → Start")
            print("   → Check if port 5432 is correct")
            
        else:
            print(f"\n❓ Unknown error: {str(e)}")
            print("   → Check DATABASE_URL in .env")
            print("   → Verify PostgreSQL is installed")
        
        print()
        return False
        
    except Exception as e:
        print(f"   ❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_env_file():
    """Kiểm tra file .env có tồn tại không"""
    print("\n🔍 Checking .env file...")
    
    if not os.path.exists(".env"):
        print("   ⚠️  .env file not found!")
        print("\n   💡 Create .env file:")
        print("      1. Copy .env.example to .env")
        print("      2. Update DATABASE_URL with your credentials")
        print()
        
        if os.path.exists(".env.example"):
            print("   📄 Found .env.example - copy it:")
            print("      copy .env.example .env  (Windows)")
            print("      cp .env.example .env    (Mac/Linux)")
        
        return False
    else:
        print("   ✅ .env file found!")
        return True

if __name__ == "__main__":
    # Check .env file first
    env_exists = check_env_file()
    
    if not env_exists:
        print("\n⚠️  Please create .env file first!")
        print("=" * 60)
    else:
        # Run connection test
        test_basic_connection()

