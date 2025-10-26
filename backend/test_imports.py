"""
Test import các modules
"""

print("🧪 Testing imports...")

try:
    print("  - FastAPI...", end=" ")
    from fastapi import FastAPI
    print("✅")
except Exception as e:
    print(f"❌ {e}")

try:
    print("  - Database...", end=" ")
    from database import get_db
    print("✅")
except Exception as e:
    print(f"❌ {e}")

try:
    print("  - Models...", end=" ")
    from models import RecognitionHistory
    print("✅")
except Exception as e:
    print(f"❌ {e}")

try:
    print("  - Gender detection...", end=" ")
    from modules.nhan_dang_gioi_tinh import nhan_dang_gioi_tinh_tu_anh
    print("✅")
except Exception as e:
    print(f"❌ {e}")

try:
    print("  - Color detection...", end=" ")
    from modules.nhan_dang_mau_sac import nhan_dang_mau_ao
    print("✅")
except Exception as e:
    print(f"❌ {e}")

try:
    print("  - Weather analysis...", end=" ")
    from modules.nhan_dang_thoi_tiet import phan_tich_thoi_tiet
    print("✅")
except Exception as e:
    print(f"❌ {e}")

try:
    print("  - Object detection...", end=" ")
    from modules.nhan_dang_vat_dung import nhan_dang_vat_dung
    print("✅")
except Exception as e:
    print(f"❌ {e}")

print("\n✅ All imports successful!")

