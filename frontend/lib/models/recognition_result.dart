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

  Gender({
    required this.personId,
    required this.gender,
    required this.confidence,
  });

  factory Gender.fromJson(Map<String, dynamic> json) {
    return Gender(
      personId: json['person_id'] ?? 0,
      gender: json['gender'] ?? 'Không xác định',
      confidence: (json['confidence'] ?? 0).toDouble(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'person_id': personId,
      'gender': gender,
      'confidence': confidence,
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
