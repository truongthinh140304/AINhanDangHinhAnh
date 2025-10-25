# 📱 HƯỚNG DẪN KẾT NỐI ĐIỆN THOẠI

## 🎯 MỤC LỤC

1. [Yêu Cầu](#yêu-cầu)
2. [Android - Kết Nối USB](#android---kết-nối-usb)
3. [Android - Kết Nối Wireless](#android---kết-nối-wireless)
4. [iOS - Kết Nối](#ios---kết-nối)
5. [Emulator](#emulator)
6. [Troubleshooting](#troubleshooting)

---

## ✅ Yêu Cầu

- ✅ Flutter SDK đã cài đặt
- ✅ Android SDK / Xcode (cho iOS)
- ✅ USB Cable hoặc WiFi cùng mạng
- ✅ Điện thoại Android 5.0+ hoặc iOS 11+

---

## 📱 ANDROID - KẾT NỐI USB

### Bước 1: Bật Developer Mode

#### 🟦 Samsung

1. Mở **Settings** (Cài đặt)
2. Vào **About Phone** (Giới thiệu điện thoại)
3. Vào **Software Information** (Thông tin phần mềm)
4. **Nhấn "Build Number" 7 lần**
5. Nhập mật khẩu/PIN nếu hỏi
6. ✅ Thấy thông báo "You are now a developer!"

#### 🟧 Xiaomi / Redmi / POCO

1. Mở **Settings** (Cài đặt)
2. Vào **About Phone** (Giới thiệu điện thoại)
3. **Nhấn "MIUI Version" 7 lần**
4. Nhập mật khẩu/PIN nếu hỏi
5. ✅ Thấy thông báo "Developer mode enabled"

#### 🟨 Oppo / Realme

1. Mở **Settings** (Cài đặt)
2. Vào **About Phone** (Giới thiệu điện thoại)
3. **Nhấn "Version" hoặc "Build Number" 7 lần**
4. Nhập mật khẩu/PIN nếu hỏi
5. ✅ Thấy thông báo "Developer options enabled"

#### 🟩 Vivo

1. Mở **Settings** (Cài đặt)
2. Vào **About Phone** (Giới thiệu điện thoại)
3. **Nhấn "Software Version" 7 lần**
4. Nhập mật khẩu/PIN nếu hỏi
5. ✅ Developer options enabled

#### 🟪 Huawei / Honor

1. Mở **Settings**
2. Vào **About Phone**
3. **Nhấn "Build Number" 7 lần**
4. Nhập mật khẩu/PIN
5. ✅ Developer mode activated

#### ⬜ Android Generic / Stock

1. **Settings** → **About Phone**
2. **Nhấn "Build Number" 7 lần**
3. ✅ Developer mode on!

---

### Bước 2: Bật USB Debugging

#### 🔧 Tất cả hãng Android

1. Mở **Settings** (Cài đặt)
2. Tìm **Developer Options** hoặc **Developer Settings**
   - Samsung: Settings → Developer Options
   - Xiaomi: Settings → Additional Settings → Developer Options
   - Oppo/Realme: Settings → Additional Settings → Developer Options
   - Khác: Settings → System → Developer Options

3. Bật các tùy chọn sau:

```
✅ USB Debugging                    (BẮT BUỘC)
✅ Install via USB                  (nếu có)
✅ USB debugging (Security settings) (nếu có)
❌ Verify apps over USB             (TẮT đi cho dễ)
```

4. ✅ Xong! USB Debugging đã bật

---

### Bước 3: Kết Nối USB

#### 🔌 Cắm Dây USB

1. **Cắm USB** từ điện thoại vào máy tính

2. **Điện thoại sẽ hỏi "Allow USB debugging?"**
   ```
   The computer's RSA key fingerprint is:
   XX:XX:XX:XX:XX...
   
   ☑ Always allow from this computer
   
   [Cancel]  [OK]
   ```
   
   → ✅ Chọn **"Always allow from this computer"**
   → ✅ Nhấn **"OK"**

3. **Chọn USB Mode:**
   
   Kéo thanh thông báo xuống → Nhấn vào USB notification → Chọn:
   - **"File Transfer"** hoặc
   - **"MTP (Media Transfer Protocol)"** hoặc
   - **"Transferring files"**
   
   ❌ KHÔNG chọn "Charging only"

---

### Bước 4: Kiểm Tra Kết Nối

#### 🖥️ Trên Máy Tính

Mở **Terminal / PowerShell / CMD** trong VS Code (`Ctrl + \``) và chạy:

```bash
# Kiểm tra với ADB
adb devices
```

**✅ Kết Quả Thành Công:**
```
List of devices attached
R58M60EZNXH     device
```

**❌ Nếu thấy "unauthorized":**
```
List of devices attached
R58M60EZNXH     unauthorized
```

→ Quay lại điện thoại, chấp nhận "Allow USB debugging" popup

**❌ Nếu không thấy gì:**
```
List of devices attached

```

→ Xem [Troubleshooting](#troubleshooting) phía dưới

---

#### 📱 Kiểm Tra với Flutter

```bash
flutter devices
```

**✅ Kết Quả Thành Công:**
```
Found 4 devices:
  SM G973F (mobile)       • R58M60EZNXH • android-arm64  • Android 12 (API 31)
  Windows (desktop)       • windows     • windows-x64    • Microsoft Windows
  Chrome (web)            • chrome      • web-javascript • Google Chrome
  Edge (web)              • edge        • web-javascript • Microsoft Edge
```

✅ Thấy điện thoại của bạn trong danh sách → **THÀNH CÔNG!**

---

### Bước 5: Chạy App

```bash
cd frontend
flutter run
```

Hoặc trong VS Code:
- **Nhấn `F5`**
- Chọn: **"📱 Flutter: Run on Device"**

✅ App sẽ được cài đặt và chạy trên điện thoại!

---

## 📡 ANDROID - KẾT NỐI WIRELESS (Không Dây)

### Yêu Cầu

- ✅ Android 11+ (API 30+)
- ✅ Điện thoại và máy tính **cùng mạng WiFi**
- ✅ Đã bật Developer Options

---

### Cách 1: Wireless Debugging (Android 11+)

#### 📱 Trên Điện Thoại

1. **Settings** → **Developer Options**
2. Bật **"Wireless Debugging"**
3. Nhấn vào **"Wireless Debugging"**
4. Nhấn **"Pair device with pairing code"**

   Sẽ thấy:
   ```
   Wi-Fi pairing code:    123456
   IP address & Port:     192.168.1.100:35847
   ```

#### 🖥️ Trên Máy Tính

```bash
# Pair với code
adb pair 192.168.1.100:35847
# Nhập code: 123456

# Kết nối (dùng port khác, xem trong Wireless Debugging)
adb connect 192.168.1.100:35845
```

**✅ Kết Quả:**
```
Successfully paired to 192.168.1.100:35847
Connected to 192.168.1.100:35845
```

#### Kiểm Tra

```bash
adb devices
```

```
List of devices attached
192.168.1.100:35845    device
```

✅ Xong! Giờ có thể rút dây USB!

---

### Cách 2: ADB over TCP/IP (Android 5+)

#### Bước 1: Kết nối USB lần đầu

```bash
# Kết nối USB trước
adb devices

# Chuyển sang TCP/IP mode
adb tcpip 5555
```

#### Bước 2: Tìm IP của điện thoại

**Trên điện thoại:**
- **Settings** → **About Phone** → **Status** → **IP Address**

Hoặc từ máy tính:
```bash
adb shell ip addr show wlan0
```

Giả sử IP: `192.168.1.100`

#### Bước 3: Kết nối không dây

```bash
# Rút dây USB
# Kết nối qua WiFi
adb connect 192.168.1.100:5555
```

**✅ Kết Quả:**
```
connected to 192.168.1.100:5555
```

#### Bước 4: Kiểm tra

```bash
adb devices
flutter devices
```

✅ Thấy điện thoại với IP address → Thành công!

---

## 🍎 iOS - KẾT NỐI

### Yêu Cầu

- ✅ macOS
- ✅ Xcode đã cài đặt
- ✅ iPhone/iPad
- ✅ USB Cable (Lightning/USB-C)

### Kết Nối

1. **Cắm iPhone vào Mac**

2. **Mở Xcode** (lần đầu)
   - Xcode sẽ cài các components cần thiết

3. **Trust Computer trên iPhone:**
   ```
   "Trust This Computer?"
   [Don't Trust]  [Trust]
   ```
   → Chọn **"Trust"**
   → Nhập passcode iPhone

4. **Kiểm tra:**
   ```bash
   flutter devices
   ```
   
   Sẽ thấy:
   ```
   iPhone 13 (mobile) • 00008030-001234567890001E • ios • iOS 16.0
   ```

5. **Chạy app:**
   ```bash
   cd frontend
   flutter run
   ```
   
   Lần đầu sẽ hỏi mã code signing → Cấu hình trong Xcode

✅ App chạy trên iPhone!

---

## 📲 EMULATOR

### Android Emulator

#### Kiểm tra emulators có sẵn

```bash
flutter emulators
```

Kết quả:
```
Available emulators:
  Pixel_3a_API_33 • Pixel 3a API 33 • Google • android
  Pixel_5_API_31  • Pixel 5 API 31  • Google • android
```

#### Chạy emulator

```bash
flutter emulators --launch Pixel_3a_API_33
```

Hoặc mở Android Studio → AVD Manager → Play ▶️

#### Chạy app trên emulator

```bash
cd frontend
flutter run
```

Flutter sẽ tự detect emulator!

---

### iOS Simulator (chỉ trên Mac)

```bash
# Mở simulator
open -a Simulator

# Hoặc
flutter emulators --launch apple_ios_simulator

# Chạy app
cd frontend
flutter run
```

---

## 🔧 TROUBLESHOOTING

### ❌ `adb devices` không thấy gì

**Nguyên nhân:**
- USB Debugging chưa bật
- Driver chưa cài (Windows)
- Cable bị hỏng
- USB port bị lỗi

**Giải pháp:**

1. **Kiểm tra USB Debugging đã bật**

2. **Restart ADB:**
   ```bash
   adb kill-server
   adb start-server
   adb devices
   ```

3. **Thử cable USB khác**

4. **Thử USB port khác**

5. **Windows: Cài USB Driver**
   - Tải driver cho hãng điện thoại:
     - Samsung: Samsung USB Driver
     - Xiaomi: MI USB Driver
     - Generic: Google USB Driver (trong Android SDK)

6. **Restart điện thoại**

---

### ❌ Thấy "unauthorized"

```
List of devices attached
R58M60EZNXH     unauthorized
```

**Giải pháp:**

1. **Revoke USB debugging authorizations:**
   - Điện thoại: **Developer Options** → **Revoke USB debugging authorizations**

2. **Rút dây USB, cắm lại**

3. **Chấp nhận popup "Allow USB debugging?"** trên điện thoại
   - ✅ Tick "Always allow from this computer"

4. **Chạy lại:**
   ```bash
   adb devices
   ```

---

### ❌ `flutter devices` không thấy điện thoại (nhưng `adb devices` thấy)

**Giải pháp:**

```bash
# Restart Flutter
flutter doctor

# Kiểm tra lại
flutter devices

# Nếu vẫn không được, chỉ định cụ thể device ID:
flutter run -d <device_id>
```

---

### ❌ Wireless debugging không connect được

**Giải pháp:**

1. **Kiểm tra cùng WiFi:**
   - Máy tính và điện thoại phải cùng mạng WiFi
   - Không dùng VPN

2. **Firewall:**
   - Tắt firewall tạm thời để test
   - Hoặc allow ADB qua firewall

3. **IP Address đổi:**
   - Nếu IP thay đổi, phải pair lại

4. **Quay lại USB:**
   ```bash
   adb usb
   adb devices
   ```

---

### ❌ "Insufficient Permissions" (Linux)

**Giải pháp:**

```bash
# Thêm user vào plugdev group
sudo usermod -aG plugdev $USER

# Tạo udev rules
sudo apt install android-sdk-platform-tools-common

# Logout và login lại
```

---

### ❌ Điện thoại sạc nhưng không connect

**Nguyên nhân:**
- Cable chỉ có dây sạc, không có dây data
- USB port máy tính không hỗ trợ data

**Giải pháp:**
- Thử cable khác (cable chính hãng tốt nhất)
- Thử USB port khác (USB 3.0 tốt hơn USB 2.0)
- Đừng dùng USB hub

---

### ❌ "More than one device/emulator"

```bash
# Liệt kê devices
flutter devices

# Chọn device cụ thể
flutter run -d <device_id>

# Ví dụ:
flutter run -d R58M60EZNXH
```

---

## 📊 SO SÁNH CÁC CÁCH KẾT NỐI

| Cách | Ưu Điểm | Nhược Điểm | Khuyên Dùng |
|------|---------|------------|-------------|
| **USB** | • Nhanh nhất<br>• Ổn định<br>• Dễ setup | • Cần cable<br>• Bất tiện di chuyển | ⭐⭐⭐⭐⭐<br>Dùng hàng ngày |
| **Wireless (Android 11+)** | • Không dây<br>• Tự động pairing | • Chỉ Android 11+<br>• Hơi chậm | ⭐⭐⭐⭐<br>Nếu Android 11+ |
| **ADB TCP/IP** | • Không dây<br>• Android 5+ | • Cần USB lần đầu<br>• IP đổi phải setup lại | ⭐⭐⭐<br>Backup option |
| **Emulator** | • Không cần thiết bị<br>• Dễ test nhiều thiết bị | • Chậm<br>• Tốn RAM<br>• Không test được hardware | ⭐⭐⭐<br>Cho testing |

---

## 🎯 CHECKLIST SETUP

### Lần Đầu Setup

- [ ] Bật Developer Mode (nhấn Build Number 7 lần)
- [ ] Bật USB Debugging
- [ ] Cắm USB, chấp nhận "Allow USB debugging"
- [ ] Chạy `adb devices` → Thấy device
- [ ] Chạy `flutter devices` → Thấy device
- [ ] Chạy `flutter run` → App cài lên điện thoại

### Hàng Ngày

- [ ] Cắm USB (hoặc connect wireless)
- [ ] `flutter devices` - Kiểm tra
- [ ] `flutter run` - Chạy app
- [ ] Hot reload: `r` - Dev nhanh

---

## 💡 TIPS & TRICKS

### 1. Alias cho nhanh (Windows PowerShell)

Thêm vào `$PROFILE`:

```powershell
function adbdevices { adb devices }
function flutterdevices { flutter devices }
function flutterrun { cd frontend; flutter run }

Set-Alias ad adbdevices
Set-Alias fd flutterdevices
Set-Alias fr flutterrun
```

Dùng:
```powershell
ad  # Thay vì adb devices
fd  # Thay vì flutter devices
fr  # Thay vì cd frontend; flutter run
```

### 2. Giữ điện thoại không sleep

Developer Options → **"Stay awake"** → ON

### 3. Show touches khi demo

Developer Options → **"Show taps"** → ON

### 4. Animation scale (cho nhanh)

Developer Options:
- Window animation scale: 0.5x
- Transition animation scale: 0.5x
- Animator duration scale: 0.5x

### 5. Multiple devices

```bash
# Chạy trên device cụ thể
flutter run -d <device_id>

# Chạy đồng thời trên nhiều devices
flutter run -d all
```

---

## 📚 Tài Liệu Tham Khảo

- [Flutter Device Setup](https://docs.flutter.dev/get-started/install)
- [ADB Documentation](https://developer.android.com/studio/command-line/adb)
- [Android USB Driver](https://developer.android.com/studio/run/oem-usb)

---

## 🎓 Video Hướng Dẫn (Khuyên Xem)

- [Enable USB Debugging - All Android](https://www.youtube.com/results?search_query=enable+usb+debugging+android)
- [Flutter on Real Device](https://www.youtube.com/results?search_query=flutter+run+on+real+device)

---

**✅ Xong! Bạn đã biết cách kết nối điện thoại với Flutter!**

**🎯 Next:** Quay lại [HUONG_DAN_VS_CODE.md](HUONG_DAN_VS_CODE.md) để chạy app!

---

**Made with ❤️ for Mobile Developers**

