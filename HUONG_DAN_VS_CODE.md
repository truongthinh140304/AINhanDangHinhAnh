# 🎯 HƯỚNG DẪN SỬ DỤNG VS CODE

## 📋 MỤC LỤC

1. [Yêu Cầu](#yêu-cầu)
2. [Cài Đặt Extensions](#cài-đặt-extensions)
3. [Chạy Backend](#chạy-backend)
4. [Chạy Frontend](#chạy-frontend)
5. [Debug](#debug)
6. [Shortcuts Hữu Ích](#shortcuts-hữu-ích)
7. [Troubleshooting](#troubleshooting)

---

## ✅ Yêu Cầu

### Đã Cài Đặt
- ✅ VS Code (đã có)
- ✅ Flutter SDK (đã có)
- ✅ Python 3.8+ (cần kiểm tra)
- ✅ Android SDK (đã có)

### Cần Cài Thêm
Khi mở project lần đầu, VS Code sẽ tự động suggest các extension cần thiết.

---

## 🔌 Cài Đặt Extensions

### Cách 1: Tự Động (Khuyên Dùng ⭐)

Khi mở project trong VS Code:

1. **Nhấn `Ctrl + Shift + P`**
2. Gõ: `Extensions: Show Recommended Extensions`
3. Click **"Install All"**

### Cách 2: Thủ Công

Nhấn `Ctrl + Shift + X` và cài các extension sau:

#### 🎯 BẮT BUỘC

1. **Flutter** (`Dart-Code.flutter`)
   - Hỗ trợ Flutter development
   - Tự động cài luôn Dart extension

2. **Python** (`ms-python.python`)
   - Hỗ trợ Python development
   
3. **Pylance** (`ms-python.vscode-pylance`)
   - IntelliSense cho Python

#### 💡 TÙY CHỌN (Nên Cài)

4. **Prettier** - Code formatter
5. **IntelliCode** - AI code suggestions

---

## 🐍 Chạy Backend

### Cách 1: Dùng Debug Panel (Khuyên Dùng ⭐)

1. **Nhấn `F5`** hoặc click vào icon **Run and Debug** (Ctrl + Shift + D)
2. Chọn: **"🐍 Python: Backend FastAPI"**
3. Nhấn **Play** ▶️

✅ Server sẽ chạy tại: http://localhost:8000

### Cách 2: Dùng Terminal

```bash
# Mở Terminal trong VS Code: Ctrl + `
cd backend
python main.py
```

### Cách 3: Dùng Tasks

1. **Nhấn `Ctrl + Shift + P`**
2. Gõ: `Tasks: Run Task`
3. Chọn: **"🐍 Start Backend Server"**

---

## 📱 Chạy Frontend (Flutter)

### Bước 1: Kết Nối Thiết Bị

#### Option A: Điện Thoại Android Thật

**Setup lần đầu:**

1. **Bật Developer Options** trên điện thoại:
   - Vào **Settings** → **About Phone**
   - Nhấn **Build Number** 7 lần
   
2. **Bật USB Debugging:**
   - Vào **Settings** → **Developer Options**
   - Bật **USB Debugging**

3. **Kết nối USB:**
   - Cắm dây USB vào máy tính
   - Điện thoại sẽ hỏi "Allow USB debugging?" → Chọn **OK**

4. **Kiểm tra kết nối:**
   ```bash
   flutter devices
   ```
   
   Sẽ thấy điện thoại của bạn trong danh sách!

#### Option B: Android Emulator

```bash
# Liệt kê emulators
flutter emulators

# Chạy emulator
flutter emulators --launch <emulator_id>
```

#### Option C: Windows Desktop (Test Nhanh)

Không cần thiết bị, chạy ngay trên Windows!

### Bước 2: Chạy App

#### Cách 1: Dùng Debug Panel (Khuyên Dùng ⭐)

1. **Nhấn `F5`**
2. Chọn:
   - **"📱 Flutter: Run on Device"** - Chạy trên thiết bị đang kết nối
   - **"🪟 Flutter: Run on Windows"** - Chạy trên Windows
   - **"🌐 Flutter: Run on Chrome"** - Chạy trên web

3. Nhấn **Play** ▶️

#### Cách 2: Dùng Terminal

```bash
cd frontend

# Chạy trên thiết bị đang kết nối
flutter run

# Hoặc chỉ định thiết bị cụ thể
flutter run -d <device_id>

# Chạy trên Windows
flutter run -d windows

# Chạy trên Chrome
flutter run -d chrome
```

#### Cách 3: Nhấn `F5` Trực Tiếp

Mở file `frontend/lib/main.dart` và nhấn `F5` → Flutter sẽ tự chạy!

---

## 🚀 Chạy Full Stack (Backend + Frontend)

### Cách 1: Dùng Compound Launch

1. **Nhấn `F5`**
2. Chọn: **"🚀 Full Stack (Backend + Flutter)"**
3. Nhấn **Play** ▶️

✅ Backend và Frontend sẽ chạy đồng thời!

### Cách 2: Mở 2 Terminals

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
flutter run
```

---

## 🐛 Debug

### Debug Backend (Python)

1. Đặt **breakpoint**: Click vào lề trái của dòng code (xuất hiện chấm đỏ)
2. Nhấn `F5` → Chọn **"🐍 Python: Backend FastAPI"**
3. Gọi API → Code sẽ dừng tại breakpoint
4. Dùng:
   - `F10` - Step Over
   - `F11` - Step Into
   - `Shift + F11` - Step Out
   - `F5` - Continue

### Debug Flutter

1. Đặt **breakpoint** trong file `.dart`
2. Nhấn `F5` → Chọn **"📱 Flutter: Run on Device"**
3. Tương tác với app → Code sẽ dừng tại breakpoint
4. Xem:
   - **Variables** - Biến hiện tại
   - **Call Stack** - Stack trace
   - **Debug Console** - In log

### Hot Reload (Flutter)

Khi app đang chạy:
- **`r`** - Hot reload (giữ state)
- **`R`** - Hot restart (reset state)
- **`q`** - Quit

Hoặc trong VS Code:
- ⚡ **Hot Reload**: `Ctrl + F5`
- 🔄 **Hot Restart**: `Ctrl + Shift + F5`

---

## ⌨️ Shortcuts Hữu Ích

### General

| Shortcut | Chức Năng |
|----------|-----------|
| `Ctrl + P` | Quick Open file |
| `Ctrl + Shift + P` | Command Palette |
| `Ctrl + `` | Toggle Terminal |
| `Ctrl + \` | Split Editor |
| `Ctrl + B` | Toggle Sidebar |
| `F5` | Start Debugging |
| `Ctrl + F5` | Run Without Debugging |

### Editing

| Shortcut | Chức Năng |
|----------|-----------|
| `Ctrl + D` | Select next occurrence |
| `Ctrl + Shift + L` | Select all occurrences |
| `Alt + Click` | Add cursor |
| `Ctrl + /` | Toggle comment |
| `Shift + Alt + F` | Format Document |
| `Ctrl + .` | Quick Fix |

### Flutter Specific

| Shortcut | Chức Năng |
|----------|-----------|
| `Ctrl + Shift + R` | Refactor |
| `Ctrl + Space` | Trigger Suggest |
| `F2` | Rename Symbol |
| `F12` | Go to Definition |
| `Shift + F12` | Find References |

---

## 🎯 Tasks (Ctrl + Shift + P → Tasks: Run Task)

Đã tạo sẵn các tasks hữu ích:

| Task | Mục Đích |
|------|----------|
| **🐍 Start Backend Server** | Chạy FastAPI server |
| **📱 Flutter: Get Packages** | Cài packages (pub get) |
| **📱 Flutter: Run on Device** | Chạy app |
| **🧹 Clean All** | Clean Flutter project |
| **🔧 Setup Backend** | Cài Python requirements |

---

## 🔧 Troubleshooting

### ❌ "Python interpreter not found"

**Giải pháp:**
1. Tạo virtual environment:
   ```bash
   cd backend
   python -m venv venv
   ```

2. Trong VS Code:
   - `Ctrl + Shift + P`
   - Gõ: `Python: Select Interpreter`
   - Chọn: `./backend/venv/Scripts/python.exe`

### ❌ "Flutter SDK not found"

**Giải pháp:**
1. `Ctrl + Shift + P`
2. Gõ: `Flutter: Change SDK`
3. Chọn đường dẫn Flutter SDK của bạn

Hoặc set trong settings:
```json
"dart.flutterSdkPath": "C:\\flutter"
```

### ❌ "No device found"

**Giải pháp:**
```bash
# Kiểm tra devices
flutter devices

# Nếu không thấy Android device:
adb devices

# Nếu không thấy gì:
adb kill-server
adb start-server
```

### ❌ Port 8000 đã được sử dụng

**Giải pháp:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Hoặc đổi port trong backend/main.py:
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### ❌ "Module not found" (Python)

**Giải pháp:**
```bash
cd backend
pip install -r requirements.txt
```

### ❌ Flutter packages error

**Giải pháp:**
```bash
cd frontend
flutter clean
flutter pub get
```

---

## 📱 Kết Nối Điện Thoại Chi Tiết

### Android

#### 1. Bật Developer Mode
- **Samsung:** Settings → About Phone → Software Information → Tap "Build Number" 7 times
- **Xiaomi/Redmi:** Settings → About Phone → Tap "MIUI Version" 7 times
- **Oppo/Realme:** Settings → About Phone → Tap "Version" 7 times
- **Generic:** Settings → About Phone → Tap "Build Number" 7 times

#### 2. Bật USB Debugging
- Settings → Developer Options → USB Debugging → ON
- Settings → Developer Options → Install via USB → ON (nếu có)

#### 3. Kết Nối
1. Cắm USB vào máy tính
2. Điện thoại hiện popup "Allow USB debugging?" → **Always allow from this computer** → OK
3. Chọn USB mode: **File Transfer / MTP**

#### 4. Kiểm Tra
```bash
# Trong VS Code terminal
flutter devices

# Hoặc
adb devices
```

Sẽ thấy:
```
Found 4 devices:
  SM G973F (mobile) • XXXXXX • android-arm64 • Android 12 (API 31)
  Windows (desktop) • windows • windows-x64 • Microsoft Windows
  ...
```

### iOS (Nếu có Mac)

1. Connect iPhone via USB
2. Trust computer on iPhone
3. Run: `flutter devices`

### Wireless Debugging (Android 11+)

1. **Cùng WiFi** với máy tính
2. **Settings → Developer Options → Wireless Debugging** → ON
3. Trong VS Code:
   ```bash
   adb pair <IP:PORT>  # Nhập mã pairing
   adb connect <IP:PORT>
   ```

---

## 🎨 Customization

### Theme & Icons

**Khuyên dùng:**
- **Theme:** Dracula Official, One Dark Pro
- **Icons:** Material Icon Theme

### Settings Sync

Bật **Settings Sync** để đồng bộ extensions và settings:
1. `Ctrl + Shift + P`
2. `Settings Sync: Turn On`
3. Login with GitHub/Microsoft

---

## 📚 Tài Liệu Tham Khảo

- [VS Code Flutter Docs](https://docs.flutter.dev/tools/vs-code)
- [VS Code Python Docs](https://code.visualstudio.com/docs/python/python-tutorial)
- [Flutter Debugging](https://docs.flutter.dev/testing/debugging)
- [VS Code Shortcuts PDF](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf)

---

## 🎯 Next Steps

✅ Extensions đã cài → Đọc [HUONG_DAN_FULLSTACK.md](HUONG_DAN_FULLSTACK.md)

✅ Chạy Backend → Nhấn `F5` → Chọn "🐍 Python: Backend FastAPI"

✅ Chạy Flutter → Kết nối thiết bị → Nhấn `F5` → Chọn "📱 Flutter: Run on Device"

✅ Debug → Đặt breakpoints → Nhấn `F5`

---

## 🆘 Cần Trợ Giúp?

1. **Đọc Troubleshooting** phía trên
2. **Check Flutter Doctor:** `flutter doctor -v`
3. **Check Python:** `python --version`
4. **View logs:** Terminal trong VS Code

---

**Chúc bạn code vui vẻ! 🎉**

**Made with ❤️ for VS Code Users**

