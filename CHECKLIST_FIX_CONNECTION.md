# ✅ CHECKLIST FIX CONNECTION ERROR

## 📋 DANH SÁCH KIỂM TRA

### ✅ 1. Backend có chạy không?

```powershell
# Test từ máy tính
curl http://localhost:8000
```

**Kết quả mong đợi:**
```json
{
  "status": "running",
  "service": "Nhận Dạng Đối Tượng API",
  "version": "1.0.0"
}
```

---

### ✅ 2. Backend chạy với IP nào?

```powershell
# Lấy IP máy tính
Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi*","Ethernet*" | Where-Object {$_.IPAddress -notlike "169.254.*" -and $_.IPAddress -ne "127.0.0.1"} | Select-Object IPAddress
```

**IP hiện tại:** `172.19.82.237`

---

### ✅ 3. Frontend đã cập nhật IP chưa?

**File: `frontend/lib/config/api_config.dart`**

```dart
static const String baseUrl = 'http://172.19.82.237:8000';
                                    ☝️ PHẢI ĐÚNG IP
```

✅ **ĐÃ CẬP NHẬT**

---

### ✅ 4. App đã restart chưa?

**QUAN TRỌNG:** Thay đổi config PHẢI restart app!

- [ ] Nhấn `R` trong terminal Flutter (Hot Restart)
- [ ] Hoặc nhấn `q` rồi `flutter run` lại
- [ ] Hoặc đóng app trên điện thoại rồi mở lại

---

### ✅ 5. Điện thoại và máy tính cùng WiFi?

- [ ] Kiểm tra WiFi trên máy tính
- [ ] Kiểm tra WiFi trên điện thoại
- [ ] PHẢI CÙNG MẠNG!

---

### ✅ 6. Test Backend từ điện thoại

**Mở browser trên điện thoại, truy cập:**
```
http://172.19.82.237:8000
```

**Nếu thấy trang Backend:**
✅ **KẾT NỐI OK!** → App sẽ hoạt động!

**Nếu không load:**
❌ **Có vấn đề!** → Kiểm tra Firewall

---

### ✅ 7. Firewall có chặn không?

**Cách 1: Tạo rule Firewall**
```powershell
# Chạy PowerShell với quyền Administrator
.\THEM_FIREWALL_RULE.ps1
```

**Cách 2: Tắt Firewall tạm (TEST ONLY!)**
```powershell
# Chỉ để test, NHỚ BẬT LẠI SAU!
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False
```

---

### ✅ 8. Test upload ảnh

1. Mở app trên điện thoại (đã restart)
2. Chụp ảnh hoặc chọn từ thư viện
3. Nhấn nút "Nhận Dạng"
4. Đợi 2-3 giây
5. Xem kết quả

**Nếu thành công:**
- ✅ Hiển thị kết quả nhận dạng
- ✅ Có giới tính, màu sắc, thời tiết, vật dụng

**Nếu vẫn lỗi:**
- ❌ Xem logs Backend trong terminal
- ❌ Xem FIX_CONNECTION_ERROR.md

---

## 🔍 TROUBLESHOOTING NHANH

### Lỗi: "Connection refused"
→ Backend không chạy hoặc Frontend chưa restart
→ **Fix:** Khởi động Backend, restart Frontend

### Lỗi: "Connection timeout"
→ Firewall chặn hoặc không cùng WiFi
→ **Fix:** Tắt Firewall test, kiểm tra WiFi

### Lỗi: "Host not found"
→ IP sai hoặc không tồn tại
→ **Fix:** Lấy lại IP máy tính, cập nhật `api_config.dart`

### App không có phản ứng
→ App chưa restart sau khi đổi IP
→ **Fix:** Nhấn `R` trong terminal Flutter

### Backend trả về lỗi 500
→ Lỗi xử lý AI hoặc thiếu dependencies
→ **Fix:** Xem logs Backend, kiểm tra modules

---

## 📊 TRẠNG THÁI HIỆN TẠI

| Component | Status | URL/Path |
|-----------|--------|----------|
| Backend | ✅ Running | http://172.19.82.237:8000 |
| Frontend Config | ✅ Updated | `frontend/lib/config/api_config.dart` |
| Firewall | ⚠️ Chưa có rule | Chạy `THEM_FIREWALL_RULE.ps1` |
| App Restart | ❓ Cần kiểm tra | Nhấn `R` trong terminal Flutter |

---

## 🎯 CÁC BƯỚC CẦN LÀM NGAY

1. ✅ **ĐÃ FIX CODE** (Không cần làm gì)
2. ❗ **RESTART APP** (Quan trọng nhất!)
   ```
   Trong terminal Flutter: Nhấn R
   ```
3. 🔥 **THÊM FIREWALL RULE** (Nếu cần)
   ```
   Chạy: THEM_FIREWALL_RULE.ps1
   (Với quyền Administrator)
   ```
4. 📱 **TEST TRÊN ĐIỆN THOẠI**
   ```
   Browser: http://172.19.82.237:8000
   App: Upload ảnh → Nhận dạng
   ```

---

## ✨ KẾT QUẢ MONG ĐỢI

Sau khi hoàn thành tất cả:

1. ✅ Backend hiển thị trong browser điện thoại
2. ✅ App kết nối được Backend
3. ✅ Upload ảnh thành công
4. ✅ Nhận dạng trả về kết quả
5. ✅ Hiển thị: giới tính, màu sắc, thời tiết, vật dụng

**🎉 HOÀN TẤT!**

---

## 📚 TÀI LIỆU THAM KHẢO

- `FIX_CONNECTION_ERROR.md` - Hướng dẫn chi tiết
- `THEM_FIREWALL_RULE.ps1` - Script tạo Firewall rule
- `frontend/lib/config/api_config.dart` - Cấu hình API
- `BAT_DAU_CHAY_APP.md` - Hướng dẫn chạy app

---

**GHI CHÚ:** Nếu IP máy tính thay đổi (ngắt kết nối WiFi rồi kết nối lại), cần:
1. Lấy IP mới
2. Cập nhật `api_config.dart`
3. Restart app (nhấn `R`)

