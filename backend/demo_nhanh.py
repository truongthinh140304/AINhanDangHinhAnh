"""
DEMO NHANH - Nhận dạng đối tượng trên ảnh
Không cần GUI, chạy trực tiếp từ command line
"""

import cv2
import sys
from ultralytics import YOLO
from modules.nhan_dang_gioi_tinh import NhanDangGioiTinh
from modules.nhan_dang_mau_sac import NhanDangMauSac
from modules.nhan_dang_thoi_tiet import NhanDangThoiTiet
from modules.nhan_dang_vat_dung import NhanDangVatDung

def demo(duong_dan_anh):
    """
    Demo nhận dạng nhanh
    
    Args:
        duong_dan_anh: Đường dẫn tới file ảnh
    """
    print("=" * 60)
    print("     DEMO NHẬN DẠNG ĐỐI TƯỢNG TRÊN ẢNH")
    print("=" * 60)
    print()
    
    # Load ảnh
    print(f"📂 Đang tải ảnh: {duong_dan_anh}")
    anh = cv2.imread(duong_dan_anh)
    
    if anh is None:
        print("❌ Lỗi: Không thể đọc ảnh!")
        return
    
    print("✓ Đã tải ảnh thành công")
    print(f"   Kích thước: {anh.shape[1]}x{anh.shape[0]} pixels")
    print()
    
    # Khởi tạo models
    print("🤖 Đang khởi tạo mô hình AI...")
    model_yolo = YOLO('yolov8n.pt')
    nhan_dang_gioi_tinh = NhanDangGioiTinh()
    nhan_dang_mau_sac = NhanDangMauSac()
    nhan_dang_thoi_tiet = NhanDangThoiTiet()
    nhan_dang_vat_dung = NhanDangVatDung()
    print("✓ Đã khởi tạo xong")
    print()
    
    # Nhận dạng
    print("🔍 Đang phân tích ảnh...")
    ket_qua = model_yolo(anh)
    
    # Phân tích kết quả
    boxes = ket_qua[0].boxes
    
    so_nam = 0
    so_nu = 0
    danh_sach_mau_ao = []
    danh_sach_vat_dung = []
    
    anh_ve = anh.copy()
    
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = float(box.conf[0])
        class_id = int(box.cls[0])
        ten_class = ket_qua[0].names[class_id]
        
        if confidence < 0.3:
            continue
        
        if ten_class == 'person':
            # Nhận dạng giới tính
            gioi_tinh = nhan_dang_gioi_tinh.nhan_dang(anh, x1, y1, x2, y2)
            if gioi_tinh == "Nam":
                so_nam += 1
            else:
                so_nu += 1
            
            # Nhận dạng màu áo
            mau_ao = nhan_dang_mau_sac.nhan_dang_mau_ao(anh, x1, y1, x2, y2)
            danh_sach_mau_ao.append(mau_ao)
            
            # Vẽ lên ảnh
            mau = (0, 255, 0)
            cv2.rectangle(anh_ve, (x1, y1), (x2, y2), mau, 2)
            label = f"{gioi_tinh} - {mau_ao}"
            cv2.putText(anh_ve, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.6, mau, 2)
        else:
            danh_sach_vat_dung.append(ten_class)
            
            # Vẽ vật dụng
            mau = (255, 0, 0)
            cv2.rectangle(anh_ve, (x1, y1), (x2, y2), mau, 2)
            ten_viet = nhan_dang_vat_dung.dich_sang_tieng_viet(ten_class)
            cv2.putText(anh_ve, ten_viet, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX,
                       0.6, mau, 2)
    
    # Nhận dạng thời tiết
    thoi_tiet = nhan_dang_thoi_tiet.nhan_dang(anh)
    
    print("✓ Hoàn tất phân tích!")
    print()
    
    # Hiển thị kết quả
    print("=" * 60)
    print("                    KẾT QUẢ")
    print("=" * 60)
    print()
    
    print("👥 NHÂN VẬT:")
    print(f"   • Tổng số: {so_nam + so_nu} người")
    print(f"   • Nam: {so_nam} người")
    print(f"   • Nữ: {so_nu} người")
    print()
    
    if danh_sach_mau_ao:
        print("👔 MÀU ÁO:")
        for i, mau in enumerate(danh_sach_mau_ao, 1):
            print(f"   • Người {i}: {mau}")
        print()
    
    print("🌤️  THỜI TIẾT/PHONG CẢNH:")
    print(f"   • {thoi_tiet}")
    print()
    
    if danh_sach_vat_dung:
        print("🎒 VẬT DỤNG:")
        thong_ke = nhan_dang_vat_dung.thong_ke_vat_dung(danh_sach_vat_dung)
        for vat, so_luong in thong_ke.items():
            print(f"   • {vat}: {so_luong}")
        print()
    
    # Lưu kết quả
    ten_file_ket_qua = duong_dan_anh.rsplit('.', 1)[0] + '_ket_qua.jpg'
    cv2.imwrite(ten_file_ket_qua, anh_ve)
    print(f"💾 Đã lưu kết quả tại: {ten_file_ket_qua}")
    print()
    
    print("=" * 60)
    print("               HOÀN THÀNH!")
    print("=" * 60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Cách sử dụng: python demo_nhanh.py <duong_dan_anh>")
        print("Ví dụ: python demo_nhanh.py anh_test.jpg")
    else:
        demo(sys.argv[1])

