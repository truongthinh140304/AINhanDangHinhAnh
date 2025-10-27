/// Model kết quả nhận dạng từ API
class RecognitionResult {
  final String transactionId;
  final String imageUrl;
  final int peopleCount;
  final List<Gender> genders;
  final List<CustomColor> colors;
  final Weather? weather;
  final List<DetectedObject> objects;
  final double processingTime;
  final String timestamp;
  final String status;

  RecognitionResult({
    required this.transactionId,
    required this.imageUrl,
    required this.peopleCount,
    required this.genders,
    required this.colors,
    this.weather,
    required this.objects,
    required this.processingTime,
    required this.timestamp,
    required this.status,
  });

  factory RecognitionResult.fromJson(Map<String, dynamic> json) {
    return RecognitionResult(
      transactionId: json['transaction_id'] ?? '',
      imageUrl: json['image_url'] ?? '',
      peopleCount: json['people_count'] ?? 0,
      genders:
          (json['genders'] as List?)?.map((e) => Gender.fromJson(e)).toList() ??
              [],
      colors: (json['colors'] as List?)
              ?.map((e) => CustomColor.fromJson(e))
              .toList() ??
          [],
      weather:
          json['weather'] != null ? Weather.fromJson(json['weather']) : null,
      objects: (json['objects'] as List?)
              ?.map((e) => DetectedObject.fromJson(e))
              .toList() ??
          [],
      processingTime: (json['processing_time'] ?? 0).toDouble(),
      timestamp: json['timestamp'] ?? '',
      status: json['status'] ?? 'unknown',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'transaction_id': transactionId,
      'image_url': imageUrl,
      'people_count': peopleCount,
      'genders': genders.map((e) => e.toJson()).toList(),
      'colors': colors.map((e) => e.toJson()).toList(),
      'weather': weather?.toJson(),
      'objects': objects.map((e) => e.toJson()).toList(),
      'processing_time': processingTime,
      'timestamp': timestamp,
      'status': status,
    };
  }
}

/// Model giới tính
class Gender {
  final int personId;
  final String gender;
  final double confidence;
  final List<CarriedItem> carriedItems;

  Gender({
    required this.personId,
    required this.gender,
    required this.confidence,
    required this.carriedItems,
  });

  factory Gender.fromJson(Map<String, dynamic> json) {
    return Gender(
      personId: json['person_id'] ?? 0,
      gender: Gender._normalizeGenderLabel((json['gender'] ?? '').toString()),
      confidence: (json['confidence'] ?? 0).toDouble(),
      carriedItems: (json['carried_items'] as List?)
              ?.map((e) => CarriedItem.fromJson(e))
              .toList() ??
          [],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'person_id': personId,
      'gender': gender,
      'confidence': confidence,
      'carried_items': carriedItems.map((e) => e.toJson()).toList(),
    };
  }

  // Chuẩn hóa nhãn giới tính từ Backend về 'Nam' / 'Nữ' / 'Không xác định'
  static String _normalizeGenderLabel(String raw) {
    final value = raw.trim().toLowerCase();

    const maleLabels = {
      'nam', 'male', 'man', 'm', 'boy', 'anh', 'đàn ông', 'dan ong'
    };
    const femaleLabels = {
      'nữ', 'nu', 'female', 'woman', 'f', 'girl', 'chị', 'phụ nữ', 'phu nu'
    };

    if (maleLabels.contains(value)) return 'Nam';
    if (femaleLabels.contains(value)) return 'Nữ';

    // Thử khớp chứa từ khóa phổ biến
    if (value.contains('male') || value.contains('man')) return 'Nam';
    if (value.contains('female') || value.contains('woman')) return 'Nữ';

    return 'Không xác định';
  }
}

/// Vật dụng cầm theo của từng người (gắn trong đối tượng Gender)
class CarriedItem {
  final String label; // Tên tiếng Việt nếu có, fallback tên class tiếng Anh
  final String? objectClass; // Tên class tiếng Anh gốc
  final double confidence;
  final List<int>? bbox; // [x1,y1,x2,y2]

  CarriedItem({
    required this.label,
    this.objectClass,
    required this.confidence,
    this.bbox,
  });

  factory CarriedItem.fromJson(Map<String, dynamic> json) {
    final String labelVi = (json['ten_tieng_viet'] ?? '').toString().trim();
    final String cls = (json['object_class'] ?? '').toString().trim();
    return CarriedItem(
      label: labelVi.isNotEmpty ? labelVi : (cls.isNotEmpty ? cls : 'Không xác định'),
      objectClass: cls.isNotEmpty ? cls : null,
      confidence: (json['confidence'] ?? 0).toDouble(),
      bbox: (json['bbox'] is List)
          ? List<int>.from((json['bbox'] as List).where((v) => v is num).map((v) => (v as num).toInt()))
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'label': label,
      'object_class': objectClass,
      'confidence': confidence,
      'bbox': bbox,
    };
  }
}

/// Model màu sắc
class CustomColor {
  final int personId;
  final String color;
  final String hex;
  final double confidence;

  CustomColor({
    required this.personId,
    required this.color,
    required this.hex,
    required this.confidence,
  });

  factory CustomColor.fromJson(Map<String, dynamic> json) {
    return CustomColor(
      personId: json['person_id'] ?? 0,
      color: json['color'] ?? 'Không xác định',
      hex: json['hex'] ?? '#000000',
      confidence: (json['confidence'] ?? 0).toDouble(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'person_id': personId,
      'color': color,
      'hex': hex,
      'confidence': confidence,
    };
  }
}

/// Model thời tiết
class Weather {
  final String type;
  final double brightness;
  final String description;

  Weather({
    required this.type,
    required this.brightness,
    required this.description,
  });

  factory Weather.fromJson(Map<String, dynamic> json) {
    return Weather(
      type: json['type'] ?? 'Không xác định',
      brightness: (json['brightness'] ?? 0).toDouble(),
      description: json['description'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'type': type,
      'brightness': brightness,
      'description': description,
    };
  }
}

/// Model vật dụng
class DetectedObject {
  final String name;
  final int count;
  final double confidence;

  DetectedObject({
    required this.name,
    required this.count,
    required this.confidence,
  });

  factory DetectedObject.fromJson(Map<String, dynamic> json) {
    return DetectedObject(
      name: json['name'] ?? 'Không xác định',
      count: json['count'] ?? 0,
      confidence: (json['confidence'] ?? 0).toDouble(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'count': count,
      'confidence': confidence,
    };
  }
}
