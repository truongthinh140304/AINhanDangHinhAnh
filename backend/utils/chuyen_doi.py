"""
Module chuyển đổi - Các hàm tiện ích cho chuyển đổi dữ liệu
"""

import cv2
import numpy as np
from PIL import Image

class ChuyenDoi:
    """
    Class chứa các hàm chuyển đổi định dạng
    """
    
    @staticmethod
    def cv2_sang_pil(anh_cv2):
        """
        Chuyển ảnh OpenCV sang PIL
        
        Args:
            anh_cv2: Ảnh numpy array (BGR)
            
        Returns:
            PIL.Image: Ảnh PIL
        """
        anh_rgb = cv2.cvtColor(anh_cv2, cv2.COLOR_BGR2RGB)
        return Image.fromarray(anh_rgb)
        
    @staticmethod
    def pil_sang_cv2(anh_pil):
        """
        Chuyển ảnh PIL sang OpenCV
        
        Args:
            anh_pil: PIL.Image
            
        Returns:
            numpy array: Ảnh OpenCV (BGR)
        """
        anh_rgb = np.array(anh_pil)
        return cv2.cvtColor(anh_rgb, cv2.COLOR_RGB2BGR)
        
    @staticmethod
    def bgr_sang_rgb(anh_bgr):
        """
        Chuyển BGR sang RGB
        
        Args:
            anh_bgr: Ảnh BGR
            
        Returns:
            numpy array: Ảnh RGB
        """
        return cv2.cvtColor(anh_bgr, cv2.COLOR_BGR2RGB)
        
    @staticmethod
    def rgb_sang_bgr(anh_rgb):
        """
        Chuyển RGB sang BGR
        
        Args:
            anh_rgb: Ảnh RGB
            
        Returns:
            numpy array: Ảnh BGR
        """
        return cv2.cvtColor(anh_rgb, cv2.COLOR_RGB2BGR)
        
    @staticmethod
    def hsv_sang_ten_mau(h, s, v):
        """
        Chuyển giá trị HSV sang tên màu tiếng Việt
        
        Args:
            h: Hue (0-180)
            s: Saturation (0-255)
            v: Value (0-255)
            
        Returns:
            str: Tên màu
        """
        # Xử lý màu không bão hòa
        if s < 30:
            if v < 50:
                return "Đen"
            elif v < 150:
                return "Xám"
            else:
                return "Trắng"
        
        # Phân loại màu theo Hue
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
            
    @staticmethod
    def rgb_sang_ten_mau(r, g, b):
        """
        Chuyển RGB sang tên màu tiếng Việt
        
        Args:
            r, g, b: Giá trị RGB (0-255)
            
        Returns:
            str: Tên màu
        """
        # Chuyển sang HSV trước
        rgb = np.uint8([[[b, g, r]]])
        hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)
        h, s, v = hsv[0][0]
        
        return ChuyenDoi.hsv_sang_ten_mau(h, s, v)
        
    @staticmethod
    def hex_sang_rgb(hex_color):
        """
        Chuyển mã hex sang RGB
        
        Args:
            hex_color: Mã màu hex (vd: "#FF0000")
            
        Returns:
            tuple: (R, G, B)
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
    @staticmethod
    def rgb_sang_hex(r, g, b):
        """
        Chuyển RGB sang hex
        
        Args:
            r, g, b: Giá trị RGB (0-255)
            
        Returns:
            str: Mã hex (vd: "#FF0000")
        """
        return "#{:02x}{:02x}{:02x}".format(r, g, b)
        
    @staticmethod
    def chuoi_sang_bbox(chuoi):
        """
        Chuyển chuỗi sang bounding box
        
        Args:
            chuoi: "x1,y1,x2,y2"
            
        Returns:
            tuple: (x1, y1, x2, y2)
        """
        parts = chuoi.split(',')
        return tuple(map(int, parts))
        
    @staticmethod
    def bbox_sang_chuoi(x1, y1, x2, y2):
        """
        Chuyển bounding box sang chuỗi
        
        Args:
            x1, y1, x2, y2: Tọa độ
            
        Returns:
            str: "x1,y1,x2,y2"
        """
        return f"{x1},{y1},{x2},{y2}"
        
    @staticmethod
    def bbox_xywh_sang_xyxy(x, y, w, h):
        """
        Chuyển bbox từ định dạng xywh sang xyxy
        
        Args:
            x, y: Tọa độ góc trên trái
            w, h: Chiều rộng, chiều cao
            
        Returns:
            tuple: (x1, y1, x2, y2)
        """
        return (x, y, x + w, y + h)
        
    @staticmethod
    def bbox_xyxy_sang_xywh(x1, y1, x2, y2):
        """
        Chuyển bbox từ định dạng xyxy sang xywh
        
        Args:
            x1, y1, x2, y2: Tọa độ 2 góc
            
        Returns:
            tuple: (x, y, w, h)
        """
        return (x1, y1, x2 - x1, y2 - y1)
        
    @staticmethod
    def chuyen_doi_so_thanh_chu(so):
        """
        Chuyển số sang chữ tiếng Việt (1-100)
        
        Args:
            so: Số nguyên
            
        Returns:
            str: Chữ số
        """
        don_vi = ["", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
        chuc = ["", "mười", "hai mươi", "ba mươi", "bốn mươi", "năm mươi", 
                "sáu mươi", "bảy mươi", "tám mươi", "chín mươi"]
        
        if so == 0:
            return "không"
        elif so < 10:
            return don_vi[so]
        elif so == 10:
            return "mười"
        elif so < 20:
            return "mười " + don_vi[so - 10]
        elif so < 100:
            hang_chuc = so // 10
            hang_don_vi = so % 10
            if hang_don_vi == 0:
                return chuc[hang_chuc]
            else:
                return chuc[hang_chuc] + " " + don_vi[hang_don_vi]
        else:
            return str(so)
            
    @staticmethod
    def dinh_dang_thoi_gian(giay):
        """
        Định dạng thời gian từ giây
        
        Args:
            giay: Số giây
            
        Returns:
            str: Thời gian định dạng (vd: "1 phút 30 giây")
        """
        if giay < 60:
            return f"{giay:.1f} giây"
        elif giay < 3600:
            phut = int(giay // 60)
            giay_con_lai = int(giay % 60)
            return f"{phut} phút {giay_con_lai} giây"
        else:
            gio = int(giay // 3600)
            phut = int((giay % 3600) // 60)
            return f"{gio} giờ {phut} phút"
            
    @staticmethod
    def dinh_dang_kich_thuoc_file(bytes):
        """
        Định dạng kích thước file
        
        Args:
            bytes: Số bytes
            
        Returns:
            str: Kích thước định dạng (vd: "1.5 MB")
        """
        if bytes < 1024:
            return f"{bytes} B"
        elif bytes < 1024 * 1024:
            return f"{bytes / 1024:.1f} KB"
        elif bytes < 1024 * 1024 * 1024:
            return f"{bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{bytes / (1024 * 1024 * 1024):.1f} GB"

