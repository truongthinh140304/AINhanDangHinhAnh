import 'dart:io';
import 'package:dio/dio.dart';
import '../models/recognition_result.dart';

/// Service để gọi API Backend
class ApiService {
  final Dio _dio;
  final String baseUrl;

  ApiService({required this.baseUrl}) : _dio = Dio(
    BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(seconds: 30),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    ),
  ) {
    // Add interceptors for logging
    _dio.interceptors.add(
      LogInterceptor(
        requestBody: true,
        responseBody: true,
      ),
    );
  }

  /// Health check
  Future<Map<String, dynamic>> healthCheck() async {
    try {
      final response = await _dio.get('/health');
      return response.data;
    } catch (e) {
      throw _handleError(e);
    }
  }

  /// Nhận dạng ảnh
  Future<RecognitionResult> recognizeImage(File imageFile) async {
    try {
      // Tạo FormData với file
      final formData = FormData.fromMap({
        'file': await MultipartFile.fromFile(
          imageFile.path,
          filename: imageFile.path.split('/').last,
        ),
      });

      // Gửi request
      final response = await _dio.post(
        '/api/recognize',
        data: formData,
        options: Options(
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        ),
      );

      // Parse response
      return RecognitionResult.fromJson(response.data);
      
    } catch (e) {
      throw _handleError(e);
    }
  }

  /// Lấy lịch sử (TODO: implement when backend ready)
  Future<List<RecognitionResult>> getHistory() async {
    try {
      final response = await _dio.get('/api/history');
      final List<dynamic> data = response.data['data'] ?? [];
      return data.map((e) => RecognitionResult.fromJson(e)).toList();
    } catch (e) {
      throw _handleError(e);
    }
  }

  /// Xóa giao dịch (TODO: implement when backend ready)
  Future<void> deleteTransaction(String transactionId) async {
    try {
      await _dio.delete('/api/transaction/$transactionId');
    } catch (e) {
      throw _handleError(e);
    }
  }

  /// Xử lý lỗi
  String _handleError(dynamic error) {
    if (error is DioException) {
      switch (error.type) {
        case DioExceptionType.connectionTimeout:
        case DioExceptionType.sendTimeout:
        case DioExceptionType.receiveTimeout:
          return 'Timeout: Không thể kết nối đến server';
        
        case DioExceptionType.badResponse:
          final statusCode = error.response?.statusCode;
          final message = error.response?.data['message'] ?? 'Lỗi server';
          return 'Lỗi $statusCode: $message';
        
        case DioExceptionType.cancel:
          return 'Request bị hủy';
        
        default:
          return 'Lỗi kết nối: ${error.message}';
      }
    }
    
    return 'Lỗi không xác định: $error';
  }
}

