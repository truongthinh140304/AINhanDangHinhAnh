import 'dart:io';
import 'package:flutter/material.dart';
import '../models/recognition_result.dart';
import '../services/api_service.dart';

/// Provider quản lý state cho recognition
class RecognitionProvider with ChangeNotifier {
  final ApiService apiService;

  RecognitionProvider({required this.apiService});

  // State
  bool _isLoading = false;
  String? _error;
  RecognitionResult? _currentResult;
  List<RecognitionResult> _history = [];

  // Getters
  bool get isLoading => _isLoading;
  String? get error => _error;
  RecognitionResult? get currentResult => _currentResult;
  List<RecognitionResult> get history => _history;

  /// Nhận dạng ảnh
  Future<void> recognizeImage(File imageFile) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final result = await apiService.recognizeImage(imageFile);
      _currentResult = result;
      _history.insert(0, result); // Thêm vào đầu danh sách
      _error = null;
    } catch (e) {
      _error = e.toString();
      _currentResult = null;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Load lịch sử từ server
  Future<void> loadHistory() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _history = await apiService.getHistory();
      _error = null;
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Xóa giao dịch
  Future<void> deleteTransaction(String transactionId) async {
    try {
      await apiService.deleteTransaction(transactionId);
      _history.removeWhere((r) => r.transactionId == transactionId);
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      notifyListeners();
    }
  }

  /// Clear error
  void clearError() {
    _error = null;
    notifyListeners();
  }

  /// Clear current result
  void clearResult() {
    _currentResult = null;
    notifyListeners();
  }
}

