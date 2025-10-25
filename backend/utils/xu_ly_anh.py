"""
Module xử lý ảnh - Các hàm tiện ích cho xử lý ảnh
"""

import cv2
import numpy as np
from PIL import Image

class XuLyAnh:
    """
    Class chứa các hàm xử lý ảnh
    """
    
    @staticmethod
    def resize_giu_ty_le(anh, max_width=1920, max_height=1080):
        """
        Resize ảnh giữ nguyên tỷ lệ
        
        Args:
            anh: Ảnh numpy array
            max_width: Chiều rộng tối đa
            max_height: Chiều cao tối đa
            
        Returns:
            numpy array: Ảnh đã resize
        """
        h, w = anh.shape[:2]
        
        # Tính tỷ lệ
        ty_le = min(max_width/w, max_height/h)
        
        if ty_le >= 1:
            return anh  # Không cần resize
            
        # Kích thước mới
        w_moi = int(w * ty_le)
        h_moi = int(h * ty_le)
        
        # Resize
        anh_moi = cv2.resize(anh, (w_moi, h_moi), interpolation=cv2.INTER_LANCZOS4)
        return anh_moi
        
    @staticmethod
    def cat_anh(anh, x1, y1, x2, y2, padding=0):
        """
        Cắt vùng ảnh với padding
        
        Args:
            anh: Ảnh numpy array
            x1, y1, x2, y2: Tọa độ
            padding: Khoảng đệm xung quanh
            
        Returns:
            numpy array: Vùng ảnh đã cắt
        """
        h, w = anh.shape[:2]
        
        # Thêm padding và đảm bảo không vượt biên
        x1 = max(0, x1 - padding)
        y1 = max(0, y1 - padding)
        x2 = min(w, x2 + padding)
        y2 = min(h, y2 + padding)
        
        return anh[y1:y2, x1:x2]
        
    @staticmethod
    def ve_khung(anh, x1, y1, x2, y2, mau=(0, 255, 0), do_day=2):
        """
        Vẽ khung bounding box
        
        Args:
            anh: Ảnh numpy array
            x1, y1, x2, y2: Tọa độ
            mau: Màu (B, G, R)
            do_day: Độ dày đường viền
            
        Returns:
            numpy array: Ảnh đã vẽ khung
        """
        anh_ve = anh.copy()
        cv2.rectangle(anh_ve, (x1, y1), (x2, y2), mau, do_day)
        return anh_ve
        
    @staticmethod
    def ve_nhan(anh, text, x, y, mau_nen=(0, 255, 0), mau_chu=(255, 255, 255)):
        """
        Vẽ nhãn text với background
        
        Args:
            anh: Ảnh numpy array
            text: Nội dung text
            x, y: Vị trí
            mau_nen: Màu nền (B, G, R)
            mau_chu: Màu chữ (B, G, R)
            
        Returns:
            numpy array: Ảnh đã vẽ nhãn
        """
        anh_ve = anh.copy()
        
        # Sử dụng font hỗ trợ tiếng Việt tốt hơn
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        font_thickness = 2
        
        # Lấy kích thước text
        (w, h), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)
        
        # Vẽ background
        cv2.rectangle(anh_ve, (x, y-h-baseline-5), (x+w+5, y), mau_nen, -1)
        
        # Vẽ text
        cv2.putText(anh_ve, text, (x, y-5), font, font_scale, mau_chu, font_thickness)
        
        return anh_ve
        
    @staticmethod
    def tang_do_sang(anh, gia_tri=30):
        """
        Tăng độ sáng ảnh
        
        Args:
            anh: Ảnh numpy array
            gia_tri: Giá trị tăng (0-100)
            
        Returns:
            numpy array: Ảnh đã tăng sáng
        """
        hsv = cv2.cvtColor(anh, cv2.COLOR_BGR2HSV)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] + gia_tri, 0, 255)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
    @staticmethod
    def tang_do_tuong_phan(anh, alpha=1.5):
        """
        Tăng độ tương phản
        
        Args:
            anh: Ảnh numpy array
            alpha: Hệ số tương phản (1.0-3.0)
            
        Returns:
            numpy array: Ảnh đã tăng tương phản
        """
        return cv2.convertScaleAbs(anh, alpha=alpha, beta=0)
        
    @staticmethod
    def lam_mo(anh, kernel_size=5):
        """
        Làm mờ ảnh
        
        Args:
            anh: Ảnh numpy array
            kernel_size: Kích thước kernel (số lẻ)
            
        Returns:
            numpy array: Ảnh đã làm mờ
        """
        return cv2.GaussianBlur(anh, (kernel_size, kernel_size), 0)
        
    @staticmethod
    def lat_ngang(anh):
        """
        Lật ảnh theo chiều ngang
        
        Args:
            anh: Ảnh numpy array
            
        Returns:
            numpy array: Ảnh đã lật
        """
        return cv2.flip(anh, 1)
        
    @staticmethod
    def lat_doc(anh):
        """
        Lật ảnh theo chiều dọc
        
        Args:
            anh: Ảnh numpy array
            
        Returns:
            numpy array: Ảnh đã lật
        """
        return cv2.flip(anh, 0)
        
    @staticmethod
    def xoay(anh, goc):
        """
        Xoay ảnh
        
        Args:
            anh: Ảnh numpy array
            goc: Góc xoay (độ)
            
        Returns:
            numpy array: Ảnh đã xoay
        """
        h, w = anh.shape[:2]
        center = (w // 2, h // 2)
        
        M = cv2.getRotationMatrix2D(center, goc, 1.0)
        return cv2.warpAffine(anh, M, (w, h))
        
    @staticmethod
    def chuyen_sang_gray(anh):
        """
        Chuyển ảnh sang grayscale
        
        Args:
            anh: Ảnh numpy array
            
        Returns:
            numpy array: Ảnh grayscale
        """
        return cv2.cvtColor(anh, cv2.COLOR_BGR2GRAY)
        
    @staticmethod
    def chuyen_sang_hsv(anh):
        """
        Chuyển ảnh sang HSV
        
        Args:
            anh: Ảnh numpy array
            
        Returns:
            numpy array: Ảnh HSV
        """
        return cv2.cvtColor(anh, cv2.COLOR_BGR2HSV)
        
    @staticmethod
    def kiem_tra_anh_hop_le(duong_dan):
        """
        Kiểm tra file ảnh có hợp lệ không
        
        Args:
            duong_dan: Đường dẫn file
            
        Returns:
            bool: True nếu hợp lệ
        """
        try:
            anh = cv2.imread(duong_dan)
            if anh is None:
                return False
            return True
        except:
            return False
            
    @staticmethod
    def lay_kich_thuoc(anh):
        """
        Lấy kích thước ảnh
        
        Args:
            anh: Ảnh numpy array
            
        Returns:
            tuple: (width, height)
        """
        h, w = anh.shape[:2]
        return (w, h)
        
    @staticmethod
    def tinh_dien_tich_bbox(x1, y1, x2, y2):
        """
        Tính diện tích bounding box
        
        Args:
            x1, y1, x2, y2: Tọa độ
            
        Returns:
            int: Diện tích
        """
        return (x2 - x1) * (y2 - y1)
        
    @staticmethod
    def tinh_iou(box1, box2):
        """
        Tính IoU (Intersection over Union) giữa 2 boxes
        
        Args:
            box1: (x1, y1, x2, y2)
            box2: (x1, y1, x2, y2)
            
        Returns:
            float: IoU (0-1)
        """
        x1_1, y1_1, x2_1, y2_1 = box1
        x1_2, y1_2, x2_2, y2_2 = box2
        
        # Tính giao
        x1_giao = max(x1_1, x1_2)
        y1_giao = max(y1_1, y1_2)
        x2_giao = min(x2_1, x2_2)
        y2_giao = min(y2_1, y2_2)
        
        if x2_giao < x1_giao or y2_giao < y1_giao:
            return 0.0
            
        dien_tich_giao = (x2_giao - x1_giao) * (y2_giao - y1_giao)
        
        # Tính hợp
        dien_tich_1 = (x2_1 - x1_1) * (y2_1 - y1_1)
        dien_tich_2 = (x2_2 - x1_2) * (y2_2 - y1_2)
        dien_tich_hop = dien_tich_1 + dien_tich_2 - dien_tich_giao
        
        # IoU
        iou = dien_tich_giao / dien_tich_hop if dien_tich_hop > 0 else 0
        
        return iou

