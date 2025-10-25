"""
Module nhận dạng thời tiết và phong cảnh
Phân tích độ sáng, bão hòa màu và các đặc trưng môi trường
"""

import cv2
import numpy as np

class NhanDangThoiTiet:
    """
    Class nhận dạng thời tiết và điều kiện phong cảnh
    """
    
    def __init__(self):
        """Khởi tạo module nhận dạng thời tiết"""
        self.cac_loai_thoi_tiet = [
            "Nắng đẹp, trời quang",
            "Nhiều mây, ánh sáng dịu",
            "U ám, có thể mưa",
            "Tối, buổi tối hoặc trong nhà",
            "Sáng sủa, có mây nhẹ",
            "Sương mù",
            "Trời xanh rất đẹp"
        ]
        
    def nhan_dang(self, anh):
        """
        Nhận dạng thời tiết từ ảnh
        
        Args:
            anh: Ảnh gốc (numpy array)
            
        Returns:
            str: Mô tả thời tiết
        """
        try:
            # Chuyển sang HSV
            hsv = cv2.cvtColor(anh, cv2.COLOR_BGR2HSV)
            
            # Phân tích các đặc trưng
            do_sang_tb = np.mean(hsv[:, :, 2])  # Value
            do_bao_hoa_tb = np.mean(hsv[:, :, 1])  # Saturation
            
            # Phân tích vùng trời (30% phía trên ảnh)
            chieu_cao = anh.shape[0]
            vung_troi = hsv[0:int(chieu_cao*0.3), :]
            
            do_sang_troi = np.mean(vung_troi[:, :, 2])
            do_bao_hoa_troi = np.mean(vung_troi[:, :, 1])
            hue_troi = np.mean(vung_troi[:, :, 0])
            
            # Phân loại thời tiết
            thoi_tiet = self._phan_loai_thoi_tiet(
                do_sang_tb, 
                do_bao_hoa_tb,
                do_sang_troi,
                do_bao_hoa_troi,
                hue_troi
            )
            
            return thoi_tiet
            
        except Exception as e:
            print(f"Lỗi nhận dạng thời tiết: {e}")
            return "Không xác định"
            
    def _phan_loai_thoi_tiet(self, do_sang, bao_hoa, do_sang_troi, bao_hoa_troi, hue_troi):
        """
        Phân loại thời tiết dựa trên các đặc trưng
        
        Returns:
            str: Mô tả thời tiết
        """
        
        # Trời xanh rất đẹp (Hue trong khoảng xanh dương, độ sáng cao)
        if 85 < hue_troi < 130 and bao_hoa_troi > 80 and do_sang_troi > 150:
            return "Trời xanh rất đẹp, nắng ráo"
            
        # Nắng đẹp
        if do_sang > 180 and bao_hoa > 100:
            return "Nắng đẹp, trời quang"
            
        # Sáng sủa
        if do_sang > 180 and bao_hoa < 100:
            if do_sang_troi > 200:
                return "Sáng sủa, có mây nhẹ"
            else:
                return "Nhiều mây, ánh sáng dịu"
                
        # Nhiều mây
        if 120 < do_sang <= 180:
            if bao_hoa < 60:
                return "Trời nhiều mây"
            else:
                return "Nắng nhẹ, có mây"
                
        # U ám
        if 80 < do_sang <= 120:
            if bao_hoa < 50:
                return "U ám, có thể mưa"
            else:
                return "Trời âm u"
                
        # Sương mù
        if bao_hoa < 30 and 100 < do_sang < 180:
            return "Sương mù hoặc không khí ẩm"
            
        # Tối
        if do_sang <= 80:
            if do_sang < 40:
                return "Rất tối, có thể ban đêm"
            else:
                return "Tối, buổi tối hoặc trong nhà"
                
        return "Điều kiện ánh sáng trung bình"
        
    def phan_tich_chi_tiet(self, anh):
        """
        Phân tích chi tiết thời tiết và môi trường
        
        Returns:
            dict: Thông tin chi tiết
        """
        thoi_tiet = self.nhan_dang(anh)
        
        # Tính các chỉ số
        hsv = cv2.cvtColor(anh, cv2.COLOR_BGR2HSV)
        do_sang = np.mean(hsv[:, :, 2])
        do_bao_hoa = np.mean(hsv[:, :, 1])
        
        return {
            'thoi_tiet': thoi_tiet,
            'do_sang': round(do_sang, 2),
            'do_bao_hoa': round(do_bao_hoa, 2),
            'chat_luong_anh_sang': self._danh_gia_anh_sang(do_sang),
            'mau_sac_tong_the': self._mau_sac_tong_the(do_bao_hoa)
        }
        
    def _danh_gia_anh_sang(self, do_sang):
        """Đánh giá chất lượng ánh sáng"""
        if do_sang > 180:
            return "Rất tốt"
        elif do_sang > 120:
            return "Tốt"
        elif do_sang > 80:
            return "Trung bình"
        else:
            return "Kém"
            
    def _mau_sac_tong_the(self, bao_hoa):
        """Đánh giá màu sắc tổng thể"""
        if bao_hoa > 100:
            return "Rất sặc sỡ"
        elif bao_hoa > 60:
            return "Màu sắc tươi"
        elif bao_hoa > 30:
            return "Màu sắc nhạt"
        else:
            return "Ít màu sắc"

