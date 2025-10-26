/// API Configuration
class ApiConfig {
  // Địa chỉ Backend API
  // Development: Dùng IP máy tính (không dùng localhost khi test trên thiết bị thật)
  // Production: Thay bằng domain thật (vd: https://api.yourdomain.com)
  static const String baseUrl = 'http://172.19.82.237:8000';
  
  // Timeouts
  static const Duration connectTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 30);
  
  // Endpoints
  static const String recognizeEndpoint = '/api/recognize';
  static const String historyEndpoint = '/api/history';
  static const String healthEndpoint = '/health';
}

