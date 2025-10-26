"""
Quick test - kiểm tra nhanh module structure
Không cần cài đầy đủ dependencies
"""

import os
import sys

# Fix encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

print("=" * 60)
print("  QUICK TEST - MODULE STRUCTURE")
print("=" * 60)

# Check current directory
print(f"\nCurrent directory: {os.getcwd()}")

# Check Python version
print(f"Python version: {sys.version.split()[0]}")

# Check backend folder exists
backend_exists = os.path.exists("modules")
print(f"\nBackend/modules folder: {'OK' if backend_exists else 'ERROR'}")

if not backend_exists:
    print("WARNING: Ban can chay tu thu muc 'backend'!")
    print("   cd backend")
    print("   python test_quick.py")
    sys.exit(1)

# Check module files
print("\nModule files:")
module_files = [
    "modules/__init__.py",
    "modules/nhan_dang_gioi_tinh.py",
    "modules/nhan_dang_mau_sac.py",
    "modules/nhan_dang_thoi_tiet.py",
    "modules/nhan_dang_vat_dung.py"
]

for file in module_files:
    exists = os.path.exists(file)
    print(f"  {file}: {'OK' if exists else 'ERROR'}")

# Check if functions exist in files
print("\nChecking function definitions:")

functions_to_check = [
    ("modules/nhan_dang_gioi_tinh.py", "def nhan_dang_gioi_tinh_tu_anh"),
    ("modules/nhan_dang_mau_sac.py", "def nhan_dang_mau_ao"),
    ("modules/nhan_dang_thoi_tiet.py", "def phan_tich_thoi_tiet"),
    ("modules/nhan_dang_vat_dung.py", "def nhan_dang_vat_dung")
]

all_ok = True
for file, func_def in functions_to_check:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            has_func = func_def in content
            func_name = func_def.replace("def ", "").replace("(", "")
            print(f"  {func_name}: {'OK' if has_func else 'ERROR'}")
            if not has_func:
                all_ok = False
    else:
        print(f"  {file}: ERROR - File not found")
        all_ok = False

# Check main files
print("\nMain backend files:")
main_files = [
    "main.py",
    "database.py",
    "models.py",
    "requirements.txt"
]

for file in main_files:
    exists = os.path.exists(file)
    print(f"  {file}: {'OK' if exists else 'ERROR'}")

# Summary
print("\n" + "=" * 60)
if all_ok:
    print("  MODULE STRUCTURE: OK!")
    print("=" * 60)
    print("\nNEXT STEPS:")
    print("  1. Cai dependencies:")
    print("     pip install -r requirements.txt")
    print("\n  2. Test imports:")
    print("     python test_imports.py")
    print("\n  3. Chay backend:")
    print("     python main.py")
else:
    print("  MODULE STRUCTURE: ERRORS FOUND!")
    print("=" * 60)
    print("\nWARNING: Mot so functions bi thieu!")
    print("   Vui long doc file FIX_IMPORT_ERROR.md")

print()

