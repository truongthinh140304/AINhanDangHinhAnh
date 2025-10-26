"""
Module nhận dạng vật dụng
Sử dụng YOLO để phát hiện và dịch sang tiếng Việt
"""

import cv2
import numpy as np

class NhanDangVatDung:
    """
    Class nhận dạng vật dụng trên người và xung quanh
    """
    
    def __init__(self):
        """Khởi tạo module nhận dạng vật dụng"""
        self.tu_dien_tieng_viet = self._tao_tu_dien()
        
    def _tao_tu_dien(self):
        """Tạo từ điển Anh-Việt cho các vật dụng"""
        return {
            'person': 'Người',
            'bicycle': 'Xe đạp',
            'car': 'Ô tô',
            'motorcycle': 'Xe máy',
            'airplane': 'Máy bay',
            'bus': 'Xe buýt',
            'train': 'Tàu hỏa',
            'truck': 'Xe tải',
            'boat': 'Thuyền',
            'traffic light': 'Đèn giao thông',
            'fire hydrant': 'Vòi cứu hỏa',
            'stop sign': 'Biển báo dừng',
            'parking meter': 'Đồng hồ đỗ xe',
            'bench': 'Ghế băng',
            'bird': 'Chim',
            'cat': 'Mèo',
            'dog': 'Chó',
            'horse': 'Ngựa',
            'sheep': 'Cừu',
            'cow': 'Bò',
            'elephant': 'Voi',
            'bear': 'Gấu',
            'zebra': 'Ngựa vằn',
            'giraffe': 'Hươu cao cổ',
            'backpack': 'Ba lô',
            'umbrella': 'Ô, dù',
            'handbag': 'Túi xách',
            'tie': 'Cà vạt',
            'suitcase': 'Va li',
            'frisbee': 'Đĩa bay',
            'skis': 'Ván trượt tuyết',
            'snowboard': 'Ván trượt tuyết',
            'sports ball': 'Bóng thể thao',
            'kite': 'Diều',
            'baseball bat': 'Gậy bóng chày',
            'baseball glove': 'Găng tay bóng chày',
            'skateboard': 'Ván trượt',
            'surfboard': 'Ván lướt sóng',
            'tennis racket': 'Vợt tennis',
            'bottle': 'Chai, lọ',
            'wine glass': 'Ly rượu',
            'cup': 'Cốc, tách',
            'fork': 'Nĩa',
            'knife': 'Dao',
            'spoon': 'Thìa',
            'bowl': 'Bát, tô',
            'banana': 'Chuối',
            'apple': 'Táo',
            'sandwich': 'Bánh sandwich',
            'orange': 'Cam',
            'broccoli': 'Bông cải xanh',
            'carrot': 'Cà rốt',
            'hot dog': 'Bánh hot dog',
            'pizza': 'Pizza',
            'donut': 'Bánh donut',
            'cake': 'Bánh ngọt',
            'chair': 'Ghế',
            'couch': 'Ghế sofa',
            'potted plant': 'Chậu cây',
            'bed': 'Giường',
            'dining table': 'Bàn ăn',
            'toilet': 'Toilet',
            'tv': 'Ti vi',
            'laptop': 'Máy tính xách tay',
            'mouse': 'Chuột máy tính',
            'remote': 'Điều khiển từ xa',
            'keyboard': 'Bàn phím',
            'cell phone': 'Điện thoại di động',
            'microwave': 'Lò vi sóng',
            'oven': 'Lò nướng',
            'toaster': 'Máy nướng bánh mì',
            'sink': 'Bồn rửa',
            'refrigerator': 'Tủ lạnh',
            'book': 'Sách',
            'clock': 'Đồng hồ',
            'vase': 'Bình hoa',
            'scissors': 'Kéo',
            'teddy bear': 'Gấu bông',
            'hair drier': 'Máy sấy tóc',
            'toothbrush': 'Bàn chải đánh răng'
        }
        
    def dich_sang_tieng_viet(self, ten_tieng_anh):
        """
        Dịch tên vật dụng từ tiếng Anh sang tiếng Việt
        
        Args:
            ten_tieng_anh: Tên tiếng Anh
            
        Returns:
            str: Tên tiếng Việt
        """
        return self.tu_dien_tieng_viet.get(ten_tieng_anh, ten_tieng_anh.title())
        
    def kiem_tra_tren_tay(self, vat_dung_bbox, nguoi_bbox):
        """
        Kiểm tra xem vật dụng có trên tay người không
        
        Args:
            vat_dung_bbox: (x1, y1, x2, y2) của vật dụng
            nguoi_bbox: (x1, y1, x2, y2) của người
            
        Returns:
            bool: True nếu vật dụng trên tay
        """
        vx1, vy1, vx2, vy2 = vat_dung_bbox
        nx1, ny1, nx2, ny2 = nguoi_bbox
        
        # Tính trung điểm vật dụng
        vat_x = (vx1 + vx2) / 2
        vat_y = (vy1 + vy2) / 2
        
        # Kiểm tra nằm trong bbox người
        if not (nx1 <= vat_x <= nx2 and ny1 <= vat_y <= ny2):
            return False
            
        # Kiểm tra vị trí tương đối (vùng tay: 30-70% chiều cao từ trên)
        chieu_cao_nguoi = ny2 - ny1
        vi_tri_tuong_doi = (vat_y - ny1) / chieu_cao_nguoi
        
        if 0.3 <= vi_tri_tuong_doi <= 0.7:
            return True
            
        return False
        
    def phan_loai_vat_dung(self, ten_vat_dung):
        """
        Phân loại vật dụng theo nhóm
        
        Returns:
            str: Tên nhóm
        """
        nhom_do_dung_ca_nhan = [
            'backpack', 'umbrella', 'handbag', 'tie', 'suitcase',
            'cell phone', 'book'
        ]
        
        nhom_the_thao = [
            'frisbee', 'skis', 'snowboard', 'sports ball', 'kite',
            'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
            'tennis racket'
        ]
        
        nhom_thuc_pham = [
            'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon',
            'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli',
            'carrot', 'hot dog', 'pizza', 'donut', 'cake'
        ]
        
        nhom_noi_that = [
            'chair', 'couch', 'potted plant', 'bed', 'dining table',
            'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard'
        ]
        
        nhom_xe_co = [
            'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
            'train', 'truck', 'boat'
        ]
        
        nhom_dong_vat = [
            'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
            'elephant', 'bear', 'zebra', 'giraffe'
        ]
        
        if ten_vat_dung in nhom_do_dung_ca_nhan:
            return "Đồ dùng cá nhân"
        elif ten_vat_dung in nhom_the_thao:
            return "Thể thao"
        elif ten_vat_dung in nhom_thuc_pham:
            return "Thực phẩm/Đồ ăn"
        elif ten_vat_dung in nhom_noi_that:
            return "Nội thất"
        elif ten_vat_dung in nhom_xe_co:
            return "Phương tiện"
        elif ten_vat_dung in nhom_dong_vat:
            return "Động vật"
        else:
            return "Khác"
            
    def thong_ke_vat_dung(self, danh_sach_vat_dung):
        """
        Thống kê số lượng vật dụng
        
        Args:
            danh_sach_vat_dung: List tên vật dụng
            
        Returns:
            dict: Thống kê
        """
        thong_ke = {}
        
        for vat in danh_sach_vat_dung:
            ten_viet = self.dich_sang_tieng_viet(vat)
            thong_ke[ten_viet] = thong_ke.get(ten_viet, 0) + 1
            
        return thong_ke
        
    def mo_ta_chi_tiet(self, danh_sach_vat_dung):
        """
        Mô tả chi tiết về các vật dụng phát hiện
        
        Returns:
            str: Mô tả
        """
        if not danh_sach_vat_dung:
            return "Không phát hiện vật dụng đặc biệt."
            
        thong_ke = self.thong_ke_vat_dung(danh_sach_vat_dung)
        
        mo_ta = "Phát hiện: "
        cac_mo_ta = []
        
        for vat, so_luong in thong_ke.items():
            if so_luong == 1:
                cac_mo_ta.append(f"{vat}")
            else:
                cac_mo_ta.append(f"{so_luong} {vat}")
                
        mo_ta += ", ".join(cac_mo_ta)
        
        return mo_ta


# ============================================================================
# FUNCTION CHO API - Wrapper để dễ sử dụng
# ============================================================================

def nhan_dang_vat_dung(anh_path_or_array, ket_qua_yolo=None):
    """
    Nhận dạng vật dụng từ ảnh (sử dụng YOLO hoặc mock data)
    
    Args:
        anh_path_or_array: Đường dẫn ảnh hoặc numpy array
        ket_qua_yolo: (Optional) Kết quả từ YOLO model
                     Format: [{"class": str, "confidence": float, "bbox": [x1,y1,x2,y2]}, ...]
    
    Returns:
        List[dict]: Kết quả nhận dạng vật dụng
        [
            {
                "object_class": "backpack",
                "ten_tieng_viet": "Ba lô",
                "confidence": float,
                "bbox": [x1, y1, x2, y2],
                "category": "Đồ dùng cá nhân"
            },
            ...
        ]
    """
    try:
        # Load ảnh
        if isinstance(anh_path_or_array, str):
            anh = cv2.imread(anh_path_or_array)
            if anh is None:
                raise ValueError(f"Không thể đọc ảnh: {anh_path_or_array}")
        else:
            anh = anh_path_or_array
        
        # Khởi tạo module
        module = NhanDangVatDung()
        
        # Kết quả
        ket_qua = []
        
        # Nếu có kết quả YOLO
        if ket_qua_yolo and len(ket_qua_yolo) > 0:
            for item in ket_qua_yolo:
                ten_class = item.get("class", "unknown")
                
                # Bỏ qua person (đã xử lý riêng)
                if ten_class.lower() == "person":
                    continue
                
                ten_viet = module.dich_sang_tieng_viet(ten_class)
                nhom = module.phan_loai_vat_dung(ten_class)
                
                ket_qua.append({
                    "object_class": ten_class,
                    "ten_tieng_viet": ten_viet,
                    "confidence": round(item.get("confidence", 0.0), 2),
                    "bbox": item.get("bbox", [0, 0, 0, 0]),
                    "category": nhom
                })
        
        # Nếu không có kết quả YOLO, return empty
        # (Production: integrate với YOLO model thực tế)
        
        return ket_qua
        
    except Exception as e:
        print(f"❌ Lỗi nhận dạng vật dụng: {e}")
        return []
