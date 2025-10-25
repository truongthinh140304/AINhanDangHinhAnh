# 📱 Flutter Frontend

Flutter mobile app cho ứng dụng nhận dạng đối tượng trên ảnh.

## 📋 Mục Lục

- [Tính Năng](#tính-năng)
- [Cài Đặt](#cài-đặt)
- [Chạy App](#chạy-app)
- [Cấu Trúc Thư Mục](#cấu-trúc-thư-mục)

## 🎯 Tính Năng

### Chức Năng Chính

- ✅ **Chụp ảnh** từ camera
- ✅ **Chọn ảnh** từ gallery
- ✅ **Upload & nhận dạng** qua API
- ✅ **Hiển thị kết quả** chi tiết
- ✅ **Lưu lịch sử** (TODO)

### UI/UX

- ✅ Material Design 3
- ✅ Responsive layout
- ✅ Loading states
- ✅ Error handling
- ✅ 100% tiếng Việt

## 🚀 Cài Đặt

### Yêu Cầu

- Flutter SDK >= 3.0.0
- Dart >= 3.0.0
- Android Studio / Xcode
- Android SDK / iOS SDK

### 1. Cài Flutter

```bash
# Download Flutter từ: https://flutter.dev/docs/get-started/install

# Kiểm tra
flutter doctor
```

### 2. Cài Dependencies

```bash
cd frontend
flutter pub get
```

### 3. Cấu Hình API Endpoint

Mở `lib/main.dart` và đổi URL:

```dart
Provider<ApiService>(
  create: (_) => ApiService(
    baseUrl: 'http://YOUR_SERVER_IP:8000', // Đổi IP ở đây
  ),
),
```

**Lưu ý:**
- Emulator Android: `http://10.0.2.2:8000`
- Emulator iOS: `http://localhost:8000`
- Real device: `http://YOUR_COMPUTER_IP:8000`

## 🏃 Chạy App

### Development Mode

```bash
# List devices
flutter devices

# Run on specific device
flutter run -d <device-id>

# Run with hot reload
flutter run
```

### Build APK (Android)

```bash
# Debug APK
flutter build apk --debug

# Release APK
flutter build apk --release

# Output: build/app/outputs/flutter-apk/app-release.apk
```

### Build iOS

```bash
# Cần Mac
flutter build ios --release
```

## 📁 Cấu Trúc Thư Mục

```
frontend/
│
├── lib/
│   ├── main.dart                    # Entry point
│   │
│   ├── models/                      # Data models
│   │   └── recognition_result.dart
│   │
│   ├── services/                    # API services
│   │   └── api_service.dart
│   │
│   ├── providers/                   # State management
│   │   └── recognition_provider.dart
│   │
│   └── screens/                     # UI screens
│       ├── home_screen.dart
│       └── result_screen.dart
│
├── pubspec.yaml                     # Dependencies
└── README.md                        # File này
```

## 📦 Dependencies

### Core

- `flutter` - Framework
- `provider` - State management

### API & Network

- `dio` - HTTP client
- `http` - Alternative HTTP

### Image

- `image_picker` - Chọn ảnh
- `camera` - Camera access
- `cached_network_image` - Cache ảnh

### UI

- `flutter_spinkit` - Loading animations

### Storage

- `shared_preferences` - Local storage
- `path_provider` - File paths

## 🔧 Cấu Hình

### Android Permissions

Đã cấu hình trong `android/app/src/main/AndroidManifest.xml`:

```xml
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.CAMERA"/>
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
```

### iOS Permissions

Thêm vào `ios/Runner/Info.plist`:

```xml
<key>NSCameraUsageDescription</key>
<string>Cần camera để chụp ảnh nhận dạng</string>
<key>NSPhotoLibraryUsageDescription</key>
<string>Cần truy cập thư viện để chọn ảnh</string>
```

## 📱 Screens

### 1. Home Screen

- Chọn/Chụp ảnh
- Hiển thị preview
- Button nhận dạng
- Loading state

### 2. Result Screen

- Số người
- Giới tính
- Màu áo
- Thời tiết
- Vật dụng
- Thời gian xử lý

### 3. History Screen (TODO)

- Danh sách lịch sử
- Xem lại kết quả
- Xóa lịch sử

## 🎨 Theme & Colors

```dart
primaryColor: Colors.blue
accentColor: Colors.green
errorColor: Colors.red

// Custom colors
maleColor: Colors.blue
femaleColor: Colors.pink
```

## 🔌 API Integration

### Endpoints Used

| Endpoint | Method | Sử dụng |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/api/recognize` | POST | Nhận dạng ảnh |
| `/api/history` | GET | Lịch sử |

### Request Example

```dart
final result = await apiService.recognizeImage(imageFile);
```

### Response Example

```json
{
  "transaction_id": "uuid",
  "people_count": 2,
  "genders": [...],
  "colors": [...],
  "weather": {...},
  "objects": [...]
}
```

## 🐛 Troubleshooting

### Lỗi: "Unable to load asset"

```bash
flutter clean
flutter pub get
flutter run
```

### Lỗi: "Connection refused"

- Kiểm tra backend đang chạy: `http://localhost:8000/health`
- Đổi IP trong `main.dart`
- Kiểm tra firewall

### Lỗi: Camera/Gallery không hoạt động

- Kiểm tra permissions trong AndroidManifest.xml / Info.plist
- Test trên real device thay vì emulator

## 📊 Performance

| Metric | Value |
|--------|-------|
| Build time | 30-60s |
| App size (release) | ~20MB |
| Memory usage | 50-100MB |
| API call | 1-3s |

## 🚢 Deployment

### Google Play Store

1. Tạo keystore
2. Cấu hình signing
3. Build release APK
4. Upload lên Play Console

### App Store

1. Setup certificates
2. Build iOS release
3. Upload lên App Store Connect

## 📞 Support

- 📖 Flutter Docs: https://flutter.dev/docs
- 🐛 Issues: GitHub Issues
- 💬 Contact: dev@example.com

## 📝 TODO

- [ ] Implement history screen
- [ ] Add authentication
- [ ] Offline mode
- [ ] Dark theme
- [ ] Multi-language
- [ ] Push notifications

---

**Made with ❤️ by Flutter**

