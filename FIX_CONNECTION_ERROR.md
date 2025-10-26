# 🔧 FIX: Connection Refused Error

## ❌ VẤN ĐỀ

Frontend trên điện thoại hiển thị lỗi:
```
Lỗi kết nối: The connection errored: Connection refused
```

## 🔍 NGUYÊN NHÂN

Frontend đang gọi `http://localhost:8000` nhưng:
- `localhost` trên điện thoại → chỉ điện thoại
- `localhost` KHÔNG phải máy tính!
- → Backend trên máy tính không thể truy cập

## ✅ GIẢI PHÁP

**Thay `localhost` bằng địa chỉ IP máy tính**

### Bước 1: Lấy IP máy tính

Chạy PowerShell:
```powershell
# Lấy IP WiFi/Ethernet
Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi*","Ethernet*" | Where-Object {$_.IPAddress -notlike "169.254.*" -and $_.IPAddress -ne "127.0.0.1"} | Select-Object IPAddress
```

Ví dụ kết quả: `172.19.82.237`

### Bước 2: Cập nhật Frontend

**File: `frontend/lib/config/api_config.dart`**

```dart
class ApiConfig {
  // Thay IP này bằng IP máy tính của bạn
  static const String baseUrl = 'http://172.19.82.237:8000';
  // ☝️ THAY 172.19.82.237 BẰNG IP CỦA BẠN
}
```

### Bước 3: Stop và Rebuild App

**Cách 1: Stop từ Terminal**
```bash
# Trong terminal đang chạy Flutter, nhấn:
q

# Rồi chạy lại:
flutter run -d <device-name>
```

**Cách 2: Stop từ điện thoại**
```
1. Swipe close app hoàn toàn
2. Terminal Flutter sẽ tự động phát hiện
3. Chạy lại: flutter run -d <device-name>
```

**Cách 3: Hot Restart (nhanh nhất)**
```
# Trong terminal Flutter đang chạy, nhấn:
R    # (Shift + R) = Hot Restart
```

### Bước 4: Kiểm tra Backend

Trên máy tính, mở browser:
```
http://172.19.82.237:8000
http://172.19.82.237:8000/docs
```

Phải thấy Backend API documentation!

### Bước 5: Test trên điện thoại

Trên điện thoại:
1. Mở browser (Chrome/Safari)
2. Truy cập: `http://172.19.82.237:8000`
3. Nếu thấy trang Backend → **KẾT NỐI OK!**
4. Nếu không load → Kiểm tra Firewall

---

## 🔥 LƯU Ý QUAN TRỌNG

### 1. ⚠️ Backend PHẢI chạy với `0.0.0.0`

**File: `backend/main.py`** (dòng 514)
```python
uvicorn.run(
    "main:app",
    host="0.0.0.0",  # ✅ CHO PHÉP TRUY CẬP TỪ BÊN NGOÀI
    port=8000,
    reload=True
)
```

**KHÔNG DÙNG:**
```python
host="127.0.0.1"  # ❌ CHỈ LOCALHOST
host="localhost"  # ❌ CHỈ LOCALHOST
```

### 2. 🛡️ Windows Firewall

Nếu vẫn không kết nối được, tắt Firewall hoặc thêm rule:

```powershell
# Thêm rule cho port 8000
New-NetFirewallRule -DisplayName "Python Backend API" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

### 3. 📱 Điện thoại và Máy tính phải cùng WiFi

- Kiểm tra cả 2 đều kết nối cùng WiFi
- KHÔNG dùng VPN
- KHÔNG dùng Hotspot

### 4. 🔄 IP có thể thay đổi

Nếu ngắt WiFi rồi kết nối lại, IP có thể đổi!

**Cách fix nhanh:**
1. Lấy IP mới (Bước 1)
2. Sửa `api_config.dart`
3. Hot restart app (nhấn `R` trong terminal Flutter)

---

## 📝 KIỂM TRA TROUBLESHOOTING

### Test 1: Backend có chạy không?
```powershell
curl http://localhost:8000
# Kết quả: JSON với "status": "running"
```

### Test 2: Backend có mở cổng không?
```powershell
Test-NetConnection -ComputerName localhost -Port 8000
# Kết quả: TcpTestSucceeded: True
```

### Test 3: Firewall có chặn không?
```powershell
Get-NetFirewallRule | Where-Object {$_.LocalPort -eq 8000}
```

### Test 4: Từ điện thoại ping được không?
```bash
# Trên điện thoại Android (cài Termux):
ping 172.19.82.237

# Hoặc mở browser trên điện thoại:
http://172.19.82.237:8000
```

---

## 🎯 ĐÃ FIX GÌ?

| File | Thay đổi |
|------|----------|
| `frontend/lib/config/api_config.dart` | ✅ Tạo mới - Chứa IP config |
| `frontend/lib/main.dart` | ✅ Đổi từ `localhost` → `ApiConfig.baseUrl` |
| `backend/main.py` | ✅ Đã sẵn `host="0.0.0.0"` |

---

## 📊 WORKFLOW SAU KHI FIX

```
1. Backend (Terminal 1):
   cd backend
   .\venv\Scripts\activate
   python main.py
   → Chạy trên http://0.0.0.0:8000

2. Frontend (Terminal 2):
   cd frontend
   flutter run -d <device>
   → App kết nối http://172.19.82.237:8000

3. Upload ảnh trên app
   → Backend nhận request
   → Xử lý AI
   → Trả kết quả cho app
   → ✅ THÀNH CÔNG!
```

---

## 🆘 VẪN LỖI?

### Lỗi: "Connection timed out"
- Backend không chạy → Khởi động backend
- IP sai → Lấy lại IP
- Firewall chặn → Tắt firewall test

### Lỗi: "Network unreachable"
- Không cùng WiFi → Kết nối cùng WiFi
- VPN bật → Tắt VPN

### Lỗi: "Host lookup failed"
- DNS lỗi → Dùng IP thay vì domain
- Typo → Kiểm tra lại IP

---

## ✅ KẾT QUẢ MONG ĐỢI

Sau khi fix:
1. ✅ Backend chạy ổn định
2. ✅ Frontend kết nối được Backend
3. ✅ Upload ảnh thành công
4. ✅ Nhận dạng hoạt động
5. ✅ Kết quả hiển thị trên app

**🎉 APP HOẠT ĐỘNG HOÀN HẢO!**

---

## 📱 DEMO THỬ NGHIỆM

1. Mở app trên điện thoại
2. Chụp ảnh hoặc chọn từ thư viện
3. Nhấn nút "Nhận Dạng"
4. Đợi 2-3 giây
5. Xem kết quả:
   - 👤 Giới tính
   - 🎨 Màu sắc áo
   - ☀️ Thời tiết
   - 📦 Vật dụng

**GHI CHÚ:** IP `172.19.82.237` là ví dụ. Thay bằng IP thật của máy bạn!

