"""
Module nhận dạng màu sắc áo
Sử dụng K-Means clustering trong không gian màu HSV
"""

import cv2
import numpy as np
from sklearn.cluster import KMeans

class NhanDangMauSac:
    """
    Class nhận dạng màu áo từ vùng ảnh người
    """
    
    def __init__(self):
        """Khởi tạo module nhận dạng màu sắc"""
        self.so_cum = 3  # Số cụm K-Means
        
        # Định nghĩa khoảng màu trong HSV
        self.bang_mau = {
            'Đỏ': [(0, 10), (170, 180)],
            'Cam': [(10, 25)],
            'Vàng': [(25, 35)],
            'Xanh lá': [(35, 85)],
            'Xanh dương': [(85, 130)],
            'Tím': [(130, 150)],
            'Hồng': [(150, 170)]
        }
        
    def nhan_dang_mau_ao(self, anh, x1, y1, x2, y2):
        """
        Nhận dạng màu áo từ bounding box
        
        Args:
            anh: Ảnh gốc (numpy array)
            x1, y1, x2, y2: Tọa độ bounding box
            
        Returns:
            str: Tên màu tiếng Việt
        """
        try:
            # Crop vùng thân trên (30-60% chiều cao từ trên xuống)
            chieu_cao = y2 - y1
            y_bat_dau = y1 + int(chieu_cao * 0.3)
            y_ket_thuc = y1 + int(chieu_cao * 0.6)
            
            vung_ao = anh[y_bat_dau:y_ket_thuc, x1:x2]
            
            if vung_ao.size == 0:
                return "Không xác định"
                
            # Chuyển sang HSV
            vung_ao_hsv = cv2.cvtColor(vung_ao, cv2.COLOR_BGR2HSV)
            
            # Reshape để clustering
            pixels = vung_ao_hsv.reshape(-1, 3)
            
            # K-means để tìm màu chủ đạo
            kmeans = KMeans(n_clusters=self.so_cum, random_state=42, n_init=10)
            kmeans.fit(pixels)
            
            # Lấy màu có số lượng pixel nhiều nhất
            labels = kmeans.labels_
            counts = np.bincount(labels)
            mau_chu_dao_idx = np.argmax(counts)
            mau_chu_dao = kmeans.cluster_centers_[mau_chu_dao_idx]
            
            # Chuyển về tên màu tiếng Việt
            ten_mau = self.chuyen_hsv_sang_ten_mau(mau_chu_dao)
            return ten_mau
            
        except Exception as e:
            print(f"Lỗi nhận dạng màu: {e}")
            return "Không xác định"
            
    def chuyen_hsv_sang_ten_mau(self, hsv):
        """
        Chuyển giá trị HSV sang tên màu tiếng Việt
        
        Args:
            hsv: Mảng [H, S, V]
            
        Returns:
            str: Tên màu
        """
        h = hsv[0]
        s = hsv[1]
        v = hsv[2]
        
        # Xử lý màu không bão hòa (Trắng, Xám, Đen)
        if s < 30:
            if v < 50:
                return "Đen"
            elif v < 150:
                return "Xám"
            else:
                return "Trắng"
        
        # Phân loại màu dựa trên Hue
        if h < 10 or h > 170:
            return "Đỏ"
        elif h < 25:
            return "Cam"
        elif h < 35:
            return "Vàng"
        elif h < 85:
            return "Xanh lá"
        elif h < 130:
            return "Xanh dương"
        elif h < 150:
            return "Tím"
        else:
            return "Hồng"
            
    def lay_mau_rgb(self, ten_mau):
        """
        Lấy giá trị RGB từ tên màu
        
        Args:
            ten_mau: Tên màu tiếng Việt
            
        Returns:
            tuple: (R, G, B)
        """
        bang_rgb = {
            'Đỏ': (255, 0, 0),
            'Cam': (255, 165, 0),
            'Vàng': (255, 255, 0),
            'Xanh lá': (0, 255, 0),
            'Xanh dương': (0, 0, 255),
            'Tím': (128, 0, 128),
            'Hồng': (255, 192, 203),
            'Trắng': (255, 255, 255),
            'Xám': (128, 128, 128),
            'Đen': (0, 0, 0),
            'Không xác định': (100, 100, 100)
        }
        
        return bang_rgb.get(ten_mau, (128, 128, 128))
        
    def phan_tich_chi_tiet(self, anh, x1, y1, x2, y2):
        """
        Phân tích chi tiết màu sắc
        
        Returns:
            dict: Thông tin chi tiết về màu
        """
        ten_mau = self.nhan_dang_mau_ao(anh, x1, y1, x2, y2)
        rgb = self.lay_mau_rgb(ten_mau)
        
        return {
            'ten_mau': ten_mau,
            'rgb': rgb,
            'vi_tri': 'Áo thân trên',
            'phuong_phap': 'K-Means Clustering'
        }

