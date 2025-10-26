import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/recognition_provider.dart';
import '../models/recognition_result.dart';

class ResultScreen extends StatelessWidget {
  const ResultScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Kết Quả Nhận Dạng'),
      ),
      body: Consumer<RecognitionProvider>(
        builder: (context, provider, child) {
          final result = provider.currentResult;

          if (result == null) {
            return const Center(
              child: Text('Không có kết quả'),
            );
          }

          return SingleChildScrollView(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Tổng quan
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      children: [
                        const Icon(
                          Icons.check_circle,
                          color: Colors.green,
                          size: 64,
                        ),
                        const SizedBox(height: 8),
                        const Text(
                          'Nhận Dạng Thành Công!',
                          style: TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'Thời gian xử lý: ${result.processingTime}s',
                          style: const TextStyle(color: Colors.grey),
                        ),
                      ],
                    ),
                  ),
                ),

                const SizedBox(height: 16),

                // Số người
                _buildSection(
                  icon: Icons.person,
                  title: 'Số Người',
                  content: Text(
                    '${result.peopleCount} người',
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),

                // Giới tính
                if (result.genders.isNotEmpty) ...[
                  _buildSection(
                    icon: Icons.people,
                    title: 'Giới Tính',
                    content: Column(
                      children: result.genders.map((gender) {
                        return ListTile(
                          leading: Icon(
                            gender.gender == 'Nam' ? Icons.man : Icons.woman,
                            color: gender.gender == 'Nam'
                                ? Colors.blue
                                : Colors.pink,
                          ),
                          title: Text(
                              'Người ${gender.personId}: ${gender.gender}'),
                          trailing: Text(
                            '${(gender.confidence * 100).toStringAsFixed(0)}%',
                            style: const TextStyle(
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        );
                      }).toList(),
                    ),
                  ),
                ],

                // Màu áo
                if (result.colors.isNotEmpty) ...[
                  _buildSection(
                    icon: Icons.palette,
                    title: 'Màu Áo',
                    content: Column(
                      children: result.colors.map((color) {
                        return ListTile(
                          leading: Container(
                            width: 40,
                            height: 40,
                            decoration: BoxDecoration(
                              color: _hexToColor(color.hex),
                              borderRadius: BorderRadius.circular(8),
                              border: Border.all(color: Colors.grey),
                            ),
                          ),
                          title:
                              Text('Người ${color.personId}: ${color.color}'),
                          trailing: Text(
                            '${(color.confidence * 100).toStringAsFixed(0)}%',
                            style: const TextStyle(
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        );
                      }).toList(),
                    ),
                  ),
                ],

                // Thời tiết
                if (result.weather != null) ...[
                  _buildSection(
                    icon: Icons.wb_sunny,
                    title: 'Thời Tiết/Phong Cảnh',
                    content: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        ListTile(
                          title: Text(
                            result.weather!.type,
                            style: const TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          subtitle: Text(result.weather!.description),
                          trailing: Text(
                            'Độ sáng: ${(result.weather!.brightness * 100).toStringAsFixed(0)}%',
                          ),
                        ),
                      ],
                    ),
                  ),
                ],

                // Vật dụng
                if (result.objects.isNotEmpty) ...[
                  _buildSection(
                    icon: Icons.shopping_bag,
                    title: 'Vật Dụng',
                    content: Column(
                      children: result.objects.map((obj) {
                        return ListTile(
                          leading: const Icon(Icons.check_circle_outline),
                          title: Text(obj.name),
                          subtitle: Text(
                            '${(obj.confidence * 100).toStringAsFixed(0)}% độ tin cậy',
                          ),
                          trailing: Text(
                            'x${obj.count}',
                            style: const TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        );
                      }).toList(),
                    ),
                  ),
                ],

                const SizedBox(height: 16),

                // Buttons
                Row(
                  children: [
                    Expanded(
                      child: ElevatedButton.icon(
                        onPressed: () {
                          Navigator.pop(context);
                        },
                        icon: const Icon(Icons.arrow_back),
                        label: const Text('Quay Lại'),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: ElevatedButton.icon(
                        onPressed: () {
                          // TODO: Save to history
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(
                              content: Text('Đã lưu vào lịch sử'),
                            ),
                          );
                        },
                        icon: const Icon(Icons.save),
                        label: const Text('Lưu'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.green,
                          foregroundColor: Colors.white,
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildSection({
    required IconData icon,
    required String title,
    required Widget content,
  }) {
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                Icon(icon, size: 28),
                const SizedBox(width: 12),
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
          const Divider(height: 1),
          Padding(
            padding: const EdgeInsets.all(8),
            child: content,
          ),
        ],
      ),
    );
  }

  Color? _hexToColor(String hexString) {
    final buffer = StringBuffer();
    if (hexString.length == 6 || hexString.length == 7) buffer.write('ff');
    buffer.write(hexString.replaceFirst('#', ''));
    try {
      return Color(int.parse(buffer.toString(), radix: 16));
    } catch (e) {
      return null; // Return null if parsing fails
    }
  }
}
