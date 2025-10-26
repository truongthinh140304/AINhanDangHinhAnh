================================================================================
                     HUONG DAN CHAY BACKEND VA FRONTEND
                              NHANH - 5 PHUT
================================================================================

TRANG THAI HIEN TAI:
[OK] Python 3.11.9
[OK] Flutter 3.35.6
[OK] PostgreSQL 18
[OK] Database 'nhandanghinhanh' da tao
[X]  LOI: Password PostgreSQL khong dung!

================================================================================
                           FIX LOI PASSWORD NGAY!
================================================================================

CACH 1: NEU NHO PASSWORD (2 PHUT)
-----------------------------------

1. Mo file .env:
   cd D:\AInhandanghinhanh\backend
   notepad .env

2. Tim dong:
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/nhandanghinhanh
                                       ^^^^^^^^
                                       Thay "postgres" bang password thuc

3. Vi du password la "mypass123":
   DATABASE_URL=postgresql://postgres:mypass123@localhost:5432/nhandanghinhanh

4. Luu file (Ctrl+S) va dong Notepad

5. Test:
   cd D:\AInhandanghinhanh\backend
   .\venv\Scripts\activate
   python init_db.py


CACH 2: QUEN PASSWORD → RESET (10 PHUT)
----------------------------------------

1. Mo PowerShell VOI QUYEN ADMIN
   (Nhan chuot phai → "Run as Administrator")

2. Chay script tu dong:
   cd D:\AInhandanghinhanh
   .\RESET_POSTGRESQL_PASSWORD_NHANH.ps1

3. Lam theo huong dan cua script
   (Nhap password moi hoac Enter de dung "postgres")

4. Update file .env voi password moi


SAU KHI FIX PASSWORD → CHAY BACKEND VA FRONTEND
================================================

TERMINAL 1 - BACKEND
--------------------
cd D:\AInhandanghinhanh\backend
.\venv\Scripts\activate
python init_db.py          # Lan dau tien
python main.py             # Chay server

→ MO BROWSER: http://localhost:8000/docs


TERMINAL 2 - FRONTEND (MO TERMINAL MOI)
----------------------------------------
cd D:\AInhandanghinhanh\frontend
flutter pub get            # Lan dau tien
flutter run -d chrome      # Chay tren web (nhanh nhat!)

HOAC:
flutter run                # Chay tren dien thoai/emulator


KET QUA MONG DOI
================
- Backend: http://localhost:8000/docs hien thi Swagger UI
- Frontend: App mo tu dong, co the upload anh
- Upload anh → Nhan dien thanh cong


TAI LIEU THAM KHAO
==================
1. BAT_DAU_CHAY_APP.md              - Huong dan chi tiet (FILE HAY NHAT!)
2. FIX_POSTGRESQL_PASSWORD.md       - Fix loi password day du
3. RESET_POSTGRESQL_PASSWORD_NHANH.ps1 - Script tu dong reset password
4. HUONG_DAN_CHAY_APP.md            - Huong dan full workflow


CAN HO TRO?
===========
Chay lenh nay va gui ket qua:

Get-Service -Name postgresql* | Format-Table -AutoSize
cd D:\AInhandanghinhanh\backend
Get-Content .env | Select-String "DATABASE"


================================================================================
                           HANH DONG NGAY BAY GIO!
================================================================================

1. Mo file: BAT_DAU_CHAY_APP.md (Doc chi tiet)
2. Fix password PostgreSQL (Chon CACH 1 hoac CACH 2)
3. Chay backend (python main.py)
4. Chay frontend (flutter run -d chrome)

THAT LA DON GIAN! 🚀

Version: 1.0.0
Date: 26/10/2025

