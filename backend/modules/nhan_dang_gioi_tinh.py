"""
Module nhận dạng giới tính
Ưu tiên dùng DeepFace nếu có, fallback sang heuristic phân tích tỷ lệ và đặc trưng hình ảnh
"""

import cv2
import numpy as np

# DeepFace là optional dependency. Nếu không có, hệ thống vẫn chạy với heuristic.
try:
    from deepface import DeepFace  # type: ignore
    _DEEPFACE_AVAILABLE = True
except Exception:
    DeepFace = None  # type: ignore
    _DEEPFACE_AVAILABLE = False

class NhanDangGioiTinh:
    """
    Class nhận dạng giới tính từ vùng ảnh người
    """
    
    def __init__(self):
        """Khởi tạo module nhận dạng giới tính"""
        self.phuong_phap = "DeepFace -> Heuristic"
        self.deepface_available = _DEEPFACE_AVAILABLE
        # Haar cascade để crop mặt (có sẵn trong OpenCV)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        # Dự phòng: mặt nhìn nghiêng
        try:
            self.profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")
        except Exception:
            self.profile_cascade = None

    def _crop_largest_face(self, image_bgr):
        """Trả về (face_roi, (x, y, w, h)) nếu tìm thấy, ngược lại (None, None)."""
        try:
            gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
            # Thử nhiều tham số để bắt thêm mặt trong đám đông
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=3, minSize=(24, 24)
            )
            if len(faces) == 0:
                # Thử cascade mặt nghiêng nếu có
                if self.profile_cascade is not None:
                    faces = self.profile_cascade.detectMultiScale(
                        gray, scaleFactor=1.1, minNeighbors=3, minSize=(24, 24)
                    )
            if len(faces) == 0:
                # Thử lại chỉ trên nửa trên của vùng (thường có mặt)
                h = gray.shape[0]
                upper = gray[0:int(h * 0.6), :]
                faces = self.face_cascade.detectMultiScale(
                    upper, scaleFactor=1.1, minNeighbors=3, minSize=(24, 24)
                )
                if len(faces) > 0:
                    # Map lại toạ độ vào toàn vùng
                    areas = [(w * h, (x, y, w, h)) for (x, y, w, h) in faces]
                    _, (x, y, w, h) = max(areas, key=lambda t: t[0])
                    y0 = int(y)
                    return image_bgr[y0:y0 + h, x:x + w], (x, y0, w, h)
                return None, None
            # Lấy mặt lớn nhất
            areas = [(w * h, (x, y, w, h)) for (x, y, w, h) in faces]
            _, (x, y, w, h) = max(areas, key=lambda t: t[0])
            return image_bgr[y:y + h, x:x + w], (x, y, w, h)
        except Exception:
            return None, None

    def _predict_gender_deepface(self, face_bgr):
        """Dùng DeepFace để dự đoán giới tính. Trả về (label_vi, confidence)."""
        if not self.deepface_available or face_bgr is None or face_bgr.size == 0:
            return None, 0.0
        try:
            # DeepFace nhận ảnh BGR/RGB; enforce_detection=False để không ném lỗi khi không thấy mặt rõ
            result = DeepFace.analyze(face_bgr, actions=["gender"], enforce_detection=False)
            # DeepFace trả về dict hoặc list tùy phiên bản
            output = result[0] if isinstance(result, (list, tuple)) else result
            gender_label = output.get("gender")
            # Một số phiên bản trả về dict score: {'Woman': p1, 'Man': p2}
            if isinstance(gender_label, dict):
                man_score = float(gender_label.get("Man", 0.0))
                woman_score = float(gender_label.get("Woman", 0.0))
                if man_score >= woman_score:
                    return "Nam", man_score / max(man_score + woman_score, 1e-6)
                else:
                    return "Nữ", woman_score / max(man_score + woman_score, 1e-6)
            # Hoặc trả về chuỗi "Man"/"Woman" và có key "gender"/"dominant_gender"
            label = output.get("dominant_gender") or output.get("gender")
            if isinstance(label, str):
                label_lower = label.lower()
                if label_lower in ("man", "male"):
                    # confidence nếu có
                    conf = float(output.get("gender_confidence", output.get("face_confidence", 0.9)) or 0.9)
                    return "Nam", max(0.0, min(1.0, conf))
                if label_lower in ("woman", "female"):
                    conf = float(output.get("gender_confidence", output.get("face_confidence", 0.9)) or 0.9)
                    return "Nữ", max(0.0, min(1.0, conf))
            return None, 0.0
        except Exception:
            return None, 0.0
        
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
            # Crop vùng người
            vung_nguoi = anh[y1:y2, x1:x2]

            if vung_nguoi.size == 0:
                return "Không xác định"

            # 1) Ưu tiên DeepFace nếu có
            face_roi, _ = self._crop_largest_face(vung_nguoi)
            nhan_df, conf_df = self._predict_gender_deepface(face_roi if face_roi is not None else vung_nguoi)
            if nhan_df is not None and conf_df >= 0.5:
                return nhan_df

            # 2) Heuristic fallback được tinh chỉnh
            chieu_cao = max(1, y2 - y1)
            chieu_rong = max(1, x2 - x1)
            ty_le = chieu_cao / chieu_rong

            diem_so = 0

            # Tỷ lệ chiều cao/rộng (nam thường cao hơn với bbox người đứng thẳng)
            if ty_le > 2.2:
                diem_so += 2
            elif ty_le > 1.8:
                diem_so += 1
            else:
                diem_so -= 1

            # Phân tích vùng đầu (tóc): độ sáng thấp và biên độ cạnh cao => tóc dài tối (nghiêng nữ)
            chieu_cao_dau = max(1, int(chieu_cao * 0.2))
            vung_dau = vung_nguoi[0:chieu_cao_dau, :]
            if vung_dau.size > 0:
                v_hsv = cv2.cvtColor(vung_dau, cv2.COLOR_BGR2HSV)
                do_sang_tb = float(np.mean(v_hsv[:, :, 2]))
                edges = cv2.Canny(cv2.cvtColor(vung_dau, cv2.COLOR_BGR2GRAY), 50, 150)
                mat_do_canh = float(np.mean(edges > 0))
                if do_sang_tb < 90 and mat_do_canh > 0.12:
                    diem_so -= 2

            # Phân tích thân dưới: độ tương phản trái-phải nhỏ hàm ý váy
            chieu_cao_than = max(1, int(chieu_cao * 0.45))
            y_bat_dau = max(y1, y2 - chieu_cao_than)
            vung_than_duoi = anh[y_bat_dau:y2, x1:x2]
            if vung_than_duoi.size > 0:
                gray = cv2.cvtColor(vung_than_duoi, cv2.COLOR_BGR2GRAY)
                giua = gray.shape[1] // 2
                if giua > 0:
                    trai = gray[:, :giua]
                    phai = gray[:, giua:]
                    if trai.size > 0 and phai.size > 0:
                        khac_biet = abs(float(np.mean(trai)) - float(np.mean(phai)))
                        if khac_biet < 15:
                            diem_so -= 2

            # Nếu điểm số không đủ chênh lệch, dùng tie-breaker theo tỷ lệ hình thể
            if abs(diem_so) <= 1:
                return "Nam" if ty_le >= 1.95 else "Nữ"
            return "Nam" if diem_so > 0 else "Nữ"
                
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
        # Thử dùng DeepFace để có confidence, fallback sang heuristic với ước lượng
        vung_nguoi = anh[y1:y2, x1:x2]
        face_roi, _ = self._crop_largest_face(vung_nguoi) if vung_nguoi.size > 0 else (None, None)
        nhan_df, conf_df = self._predict_gender_deepface(face_roi if face_roi is not None else vung_nguoi)
        if nhan_df is not None and conf_df > 0:
            return {
                'gioi_tinh': nhan_df,
                'do_tin_cay': round(float(conf_df), 2),
                'chi_tiet': {
                    'phuong_phap': 'DeepFace',
                    'toa_do': (x1, y1, x2, y2)
                }
            }

        gioi_tinh = self.nhan_dang(anh, x1, y1, x2, y2)
        return {
            'gioi_tinh': gioi_tinh,
            'do_tin_cay': 0.65 if gioi_tinh in ("Nam", "Nữ") else 0.5,
            'chi_tiet': {
                'phuong_phap': 'Heuristic',
                'toa_do': (x1, y1, x2, y2)
            }
        }


# ============================================================================
# FUNCTION CHO API - Wrapper để dễ sử dụng
# ============================================================================

def nhan_dang_gioi_tinh_tu_anh(anh_path_or_array, ket_qua_nguoi):
    """
    Nhận dạng giới tính cho tất cả người trong ảnh
    
    Args:
        anh_path_or_array: Đường dẫn ảnh hoặc numpy array
        ket_qua_nguoi: List các bounding box người từ YOLO
                      Format: [{"bbox": [x1, y1, x2, y2], "confidence": float}, ...]
    
    Returns:
        List[dict]: Kết quả giới tính cho từng người
        [
            {
                "person_id": 1,
                "gender": "male" / "female",
                "confidence": float,
                "bbox": [x1, y1, x2, y2]
            },
            ...
        ]
    """
    try:
        # Load ảnh nếu là đường dẫn
        if isinstance(anh_path_or_array, str):
            anh = cv2.imread(anh_path_or_array)
            if anh is None:
                raise ValueError(f"Không thể đọc ảnh: {anh_path_or_array}")
        else:
            anh = anh_path_or_array
        
        # Khởi tạo module
        nhan_dang = NhanDangGioiTinh()
        
        # Kết quả
        ket_qua = []
        
        # Xử lý từng người
        for idx, nguoi in enumerate(ket_qua_nguoi):
            bbox = nguoi.get("bbox", [])
            if len(bbox) != 4:
                continue
            
            x1, y1, x2, y2 = map(int, bbox)
            
            # Nhận dạng giới tính (ưu tiên kết quả chi tiết để lấy confidence thực)
            chi_tiet = nhan_dang.nhan_dang_chi_tiet(anh, x1, y1, x2, y2)
            gioi_tinh_vi = chi_tiet.get('gioi_tinh', 'Không xác định')
            confidence = float(chi_tiet.get('do_tin_cay', 0.6))

            # Chuyển sang tiếng Anh (giữ unknown khi không chắc chắn)
            if gioi_tinh_vi == "Nam":
                gioi_tinh_en = "male"
            elif gioi_tinh_vi == "Nữ":
                gioi_tinh_en = "female"
            else:
                gioi_tinh_en = "unknown"

            ket_qua.append({
                "person_id": idx + 1,
                "gender": gioi_tinh_en,
                "confidence": round(confidence, 2),
                "bbox": [x1, y1, x2, y2]
            })
        
        return ket_qua
        
    except Exception as e:
        print(f"❌ Lỗi nhận dạng giới tính: {e}")
        return []
