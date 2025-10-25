"""
Module nhận dạng giới tính
Sử dụng thuật toán phân tích tỷ lệ chiều cao/rộng và đặc trưng hình ảnh
"""

import cv2
import numpy as np

class NhanDangGioiTinh:
    """
    Class nhận dạng giới tính từ vùng ảnh người
    """
    
    def __init__(self):
        """Khởi tạo module nhận dạng giới tính"""
        self.phuong_phap = "Phân tích tỷ lệ và màu sắc"
        
    def nhan_dang(self, anh, x1, y1, x2, y2):
        """
        Nhận dạng giới tính từ bounding box
        
        Args:
            anh: Ảnh gốc (numpy array)
            x1, y1, x2, y2: Tọa độ bounding box
            
        Returns:
            str: "Nam" hoặc "Nữ"
        """
        try:
            # Tính tỷ lệ chiều cao/rộng
            chieu_cao = y2 - y1
            chieu_rong = x2 - x1
            
            if chieu_rong == 0:
                return "Không xác định"
                
            ty_le = chieu_cao / chieu_rong
            
            # Crop vùng người
            vung_nguoi = anh[y1:y2, x1:x2]
            
            if vung_nguoi.size == 0:
                return "Không xác định"
            
            # Phân tích đặc trưng
            diem_so = 0
            
            # 1. Tỷ lệ chiều cao/rộng (Nam thường cao hơn)
            if ty_le > 2.0:
                diem_so += 2  # Có thể là Nam
            elif ty_le > 1.7:
                diem_so += 1
            else:
                diem_so -= 1  # Có thể là Nữ
                
            # 2. Phân tích màu sắc vùng đầu (tóc)
            chieu_cao_dau = int(chieu_cao * 0.15)
            vung_dau = vung_nguoi[0:chieu_cao_dau, :]
            
            if vung_dau.size > 0:
                # Chuyển sang HSV
                vung_dau_hsv = cv2.cvtColor(vung_dau, cv2.COLOR_BGR2HSV)
                
                # Độ sáng trung bình (tóc dài thường tối hơn)
                do_sang_tb = np.mean(vung_dau_hsv[:, :, 2])
                
                if do_sang_tb < 80:
                    diem_so -= 1  # Tóc dài, có thể là Nữ
                    
            # 3. Phân tích vùng thân dưới (váy/quần)
            chieu_cao_than = int(chieu_cao * 0.4)
            y_bat_dau = y1 + chieu_cao - chieu_cao_than
            vung_than_duoi = anh[y_bat_dau:y2, x1:x2]
            
            if vung_than_duoi.size > 0:
                # Phát hiện váy (có độ tương phản cao giữa 2 chân)
                gray = cv2.cvtColor(vung_than_duoi, cv2.COLOR_BGR2GRAY)
                
                # Chia đôi trái phải
                giua = gray.shape[1] // 2
                trai = gray[:, :giua]
                phai = gray[:, giua:]
                
                if trai.size > 0 and phai.size > 0:
                    # Tính độ khác biệt
                    khac_biet = np.abs(np.mean(trai) - np.mean(phai))
                    
                    if khac_biet < 20:
                        diem_so -= 2  # Có thể đang mặc váy (Nữ)
                        
            # Quyết định cuối cùng
            if diem_so > 0:
                return "Nam"
            else:
                return "Nữ"
                
        except Exception as e:
            print(f"Lỗi nhận dạng giới tính: {e}")
            return "Không xác định"
            
    def nhan_dang_chi_tiet(self, anh, x1, y1, x2, y2):
        """
        Nhận dạng giới tính với thông tin chi tiết
        
        Returns:
            dict: {
                'gioi_tinh': str,
                'do_tin_cay': float,
                'chi_tiet': dict
            }
        """
        gioi_tinh = self.nhan_dang(anh, x1, y1, x2, y2)
        
        return {
            'gioi_tinh': gioi_tinh,
            'do_tin_cay': 0.75,  # Độ tin cậy ước lượng
            'chi_tiet': {
                'phuong_phap': self.phuong_phap,
                'toa_do': (x1, y1, x2, y2)
            }
        }

