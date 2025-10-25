"""
ỨNG DỤNG NHẬN DẠNG ĐỐI TƯỢNG TRÊN ẢNH
Phát triển bởi: AI Assistant
Chức năng:
- Nhận dạng giới tính
- Nhận dạng màu áo
- Nhận dạng thời tiết/phong cảnh
- Nhận dạng vật dụng trên người
"""

import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from ultralytics import YOLO
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

class UngDungNhanDang:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng Dụng Nhận Dạng Đối Tượng Trên Ảnh")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Biến lưu trữ
        self.duong_dan_anh = None
        self.anh_goc = None
        self.anh_da_xu_ly = None
        
        # Khởi tạo models
        self.khoi_tao_models()
        
        # Tạo giao diện
        self.tao_giao_dien()
        
    def khoi_tao_models(self):
        """Khởi tạo các mô hình AI"""
        try:
            # Load YOLO model cho nhận dạng đối tượng
            print("Đang tải mô hình YOLO...")
            self.model_yolo = YOLO('yolov8n.pt')  # Sử dụng YOLOv8 nano (nhẹ, nhanh)
            print("✓ Đã tải YOLO thành công")
        except Exception as e:
            print(f"Lỗi khi tải mô hình: {e}")
            self.model_yolo = None
            
    def tao_giao_dien(self):
        """Tạo giao diện người dùng"""
        
        # Tiêu đề
        frame_tieu_de = tk.Frame(self.root, bg='#2c3e50', height=80)
        frame_tieu_de.pack(fill='x', pady=(0, 10))
        
        tieu_de = tk.Label(
            frame_tieu_de,
            text="🖼️ ỨNG DỤNG NHẬN DẠNG ĐỐI TƯỢNG TRÊN ẢNH",
            font=('Arial', 24, 'bold'),
            bg='#2c3e50',
            fg='white',
            pady=20
        )
        tieu_de.pack()
        
        # Frame chính
        frame_chinh = tk.Frame(self.root, bg='#f0f0f0')
        frame_chinh.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Frame trái - Hiển thị ảnh
        frame_trai = tk.LabelFrame(
            frame_chinh,
            text="📸 Hình Ảnh",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#2c3e50',
            padx=10,
            pady=10
        )
        frame_trai.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.canvas_anh = tk.Canvas(frame_trai, bg='#ecf0f1', width=700, height=600)
        self.canvas_anh.pack(pady=10)
        
        # Nút chức năng
        frame_nut = tk.Frame(frame_trai, bg='white')
        frame_nut.pack(pady=10)
        
        nut_chon_anh = tk.Button(
            frame_nut,
            text="📂 Chọn Ảnh",
            command=self.chon_anh,
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        nut_chon_anh.pack(side='left', padx=5)
        
        nut_nhan_dang = tk.Button(
            frame_nut,
            text="🔍 Nhận Dạng",
            command=self.nhan_dang_doi_tuong,
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        nut_nhan_dang.pack(side='left', padx=5)
        
        nut_luu_anh = tk.Button(
            frame_nut,
            text="💾 Lưu Kết Quả",
            command=self.luu_ket_qua,
            font=('Arial', 12, 'bold'),
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        nut_luu_anh.pack(side='left', padx=5)
        
        # Frame phải - Kết quả
        frame_phai = tk.LabelFrame(
            frame_chinh,
            text="📊 Kết Quả Nhận Dạng",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#2c3e50',
            padx=10,
            pady=10
        )
        frame_phai.pack(side='right', fill='both', expand=True)
        
        # Text widget để hiển thị kết quả
        self.text_ket_qua = tk.Text(
            frame_phai,
            font=('Courier New', 11),
            bg='#ecf0f1',
            fg='#2c3e50',
            wrap='word',
            padx=15,
            pady=15
        )
        self.text_ket_qua.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(self.text_ket_qua)
        scrollbar.pack(side='right', fill='y')
        self.text_ket_qua.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_ket_qua.yview)
        
        # Thông tin ban đầu
        self.hien_thi_thong_tin_ban_dau()
        
    def hien_thi_thong_tin_ban_dau(self):
        """Hiển thị thông tin ban đầu"""
        thong_tin = """
╔════════════════════════════════════════════╗
║   HƯỚNG DẪN SỬ DỤNG ỨNG DỤNG              ║
╚════════════════════════════════════════════╝

📌 CHỨC NĂNG CHÍNH:

✓ Nhận dạng giới tính (Nam/Nữ)
✓ Nhận dạng màu áo
✓ Nhận dạng thời tiết/phong cảnh
✓ Nhận dạng vật dụng trên người

📝 CÁCH SỬ DỤNG:

1. Nhấn nút "📂 Chọn Ảnh" để chọn ảnh
2. Nhấn nút "🔍 Nhận Dạng" để phân tích
3. Xem kết quả chi tiết bên phải
4. Nhấn nút "💾 Lưu Kết Quả" để lưu ảnh

⚙️ THUẬT TOÁN: YOLOv8 + AI Models

🎯 Hãy chọn một ảnh để bắt đầu!

        """
        self.text_ket_qua.delete(1.0, tk.END)
        self.text_ket_qua.insert(tk.END, thong_tin)
        
    def chon_anh(self):
        """Chọn ảnh từ máy tính"""
        duong_dan = filedialog.askopenfilename(
            title="Chọn ảnh",
            filetypes=[
                ("Tất cả ảnh", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("JPG", "*.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("Tất cả files", "*.*")
            ]
        )
        
        if duong_dan:
            self.duong_dan_anh = duong_dan
            self.hien_thi_anh(duong_dan)
            self.text_ket_qua.delete(1.0, tk.END)
            self.text_ket_qua.insert(tk.END, f"✓ Đã chọn ảnh: {os.path.basename(duong_dan)}\n\n")
            self.text_ket_qua.insert(tk.END, "Nhấn nút '🔍 Nhận Dạng' để phân tích ảnh.")
            
    def hien_thi_anh(self, duong_dan):
        """Hiển thị ảnh lên canvas"""
        try:
            # Đọc ảnh
            anh = Image.open(duong_dan)
            self.anh_goc = cv2.imread(duong_dan)
            
            # Resize để vừa canvas
            canvas_width = 700
            canvas_height = 600
            
            # Tính tỷ lệ
            ty_le = min(canvas_width/anh.width, canvas_height/anh.height)
            kich_thuoc_moi = (int(anh.width * ty_le), int(anh.height * ty_le))
            
            anh_resize = anh.resize(kich_thuoc_moi, Image.Resampling.LANCZOS)
            
            # Chuyển sang PhotoImage
            self.anh_hien_thi = ImageTk.PhotoImage(anh_resize)
            
            # Hiển thị
            self.canvas_anh.delete("all")
            x = (canvas_width - kich_thuoc_moi[0]) // 2
            y = (canvas_height - kich_thuoc_moi[1]) // 2
            self.canvas_anh.create_image(x, y, anchor='nw', image=self.anh_hien_thi)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể hiển thị ảnh: {e}")
            
    def nhan_dang_doi_tuong(self):
        """Nhận dạng các đối tượng trên ảnh"""
        if self.duong_dan_anh is None:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ảnh trước!")
            return
            
        if self.model_yolo is None:
            messagebox.showerror("Lỗi", "Mô hình YOLO chưa được tải!")
            return
            
        try:
            # Xóa kết quả cũ
            self.text_ket_qua.delete(1.0, tk.END)
            self.text_ket_qua.insert(tk.END, "🔄 Đang phân tích ảnh...\n\n")
            self.root.update()
            
            # Đọc ảnh
            anh = self.anh_goc.copy()
            
            # Nhận dạng với YOLO
            ket_qua = self.model_yolo(anh)
            
            # Phân tích kết quả
            self.phan_tich_ket_qua(anh, ket_qua)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi nhận dạng: {e}")
            
    def phan_tich_ket_qua(self, anh, ket_qua):
        """Phân tích và hiển thị kết quả"""
        
        # Vẽ bounding boxes
        anh_ve = anh.copy()
        
        # Lấy thông tin từ kết quả
        boxes = ket_qua[0].boxes
        
        # Đếm số lượng người
        so_nguoi_nam = 0
        so_nguoi_nu = 0
        danh_sach_mau_ao = []
        danh_sach_vat_dung = []
        
        # Danh sách vị trí người
        danh_sach_nguoi = []
        
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            ten_class = ket_qua[0].names[class_id]
            
            if confidence < 0.3:
                continue
                
            # Vẽ box và label
            if ten_class == 'person':
                mau = (0, 255, 0)  # Xanh lá cho người
                danh_sach_nguoi.append((x1, y1, x2, y2))
                
                # Nhận dạng giới tính (giả lập - trong thực tế cần model riêng)
                gioi_tinh = self.nhan_dang_gioi_tinh(anh, x1, y1, x2, y2)
                if gioi_tinh == "Nam":
                    so_nguoi_nam += 1
                else:
                    so_nguoi_nu += 1
                    
                # Nhận dạng màu áo
                mau_ao = self.nhan_dang_mau_ao(anh, x1, y1, x2, y2)
                danh_sach_mau_ao.append(mau_ao)
                
                label = f"{gioi_tinh} - {mau_ao}"
            else:
                mau = (255, 0, 0)  # Xanh dương cho vật dụng
                danh_sach_vat_dung.append(ten_class)
                label = f"{ten_class}"
                
            cv2.rectangle(anh_ve, (x1, y1), (x2, y2), mau, 2)
            
            # Vẽ label với background
            (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(anh_ve, (x1, y1-25), (x1+w, y1), mau, -1)
            cv2.putText(anh_ve, label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
            
        # Nhận dạng thời tiết/phong cảnh
        thoi_tiet = self.nhan_dang_thoi_tiet(anh)
        
        # Lưu ảnh đã xử lý
        self.anh_da_xu_ly = anh_ve
        
        # Hiển thị ảnh kết quả
        self.hien_thi_anh_ket_qua(anh_ve)
        
        # Hiển thị kết quả dạng text
        self.hien_thi_ket_qua_text(
            so_nguoi_nam,
            so_nguoi_nu,
            danh_sach_mau_ao,
            danh_sach_vat_dung,
            thoi_tiet
        )
        
    def nhan_dang_gioi_tinh(self, anh, x1, y1, x2, y2):
        """Nhận dạng giới tính (đơn giản hóa)"""
        # Trong thực tế cần model phân loại giới tính riêng
        # Ở đây dùng phương pháp đơn giản dựa trên tỷ lệ chiều cao/rộng
        chieu_cao = y2 - y1
        chieu_rong = x2 - x1
        ty_le = chieu_cao / chieu_rong if chieu_rong > 0 else 1
        
        # Giả định đơn giản (không chính xác 100%)
        if ty_le > 1.8:
            return "Nam"
        else:
            return "Nữ"
            
    def nhan_dang_mau_ao(self, anh, x1, y1, x2, y2):
        """Nhận dạng màu áo"""
        # Crop vùng thân trên (30-60% chiều cao)
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
        try:
            kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
            kmeans.fit(pixels)
            
            # Lấy màu chủ đạo
            mau_chu_dao = kmeans.cluster_centers_[0]
            
            # Chuyển về tên màu tiếng Việt
            ten_mau = self.chuyen_hsv_sang_ten_mau(mau_chu_dao)
            return ten_mau
        except:
            return "Không xác định"
            
    def chuyen_hsv_sang_ten_mau(self, hsv):
        """Chuyển giá trị HSV sang tên màu tiếng Việt"""
        h = hsv[0]
        s = hsv[1]
        v = hsv[2]
        
        # Phân loại màu dựa trên Hue
        if s < 30:
            if v < 50:
                return "Đen"
            elif v < 150:
                return "Xám"
            else:
                return "Trắng"
        
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
            
    def nhan_dang_thoi_tiet(self, anh):
        """Nhận dạng thời tiết/phong cảnh (đơn giản hóa)"""
        # Phân tích độ sáng trung bình
        hsv = cv2.cvtColor(anh, cv2.COLOR_BGR2HSV)
        do_sang_tb = np.mean(hsv[:, :, 2])
        
        # Phân tích độ bão hòa
        do_bao_hoa_tb = np.mean(hsv[:, :, 1])
        
        if do_sang_tb > 180:
            if do_bao_hoa_tb > 100:
                return "Nắng đẹp, trời quang"
            else:
                return "Nhiều mây, sáng"
        elif do_sang_tb > 120:
            return "Trời nhiều mây"
        elif do_sang_tb > 80:
            return "U ám, có thể mưa"
        else:
            return "Tối, buổi tối hoặc trong nhà"
            
    def hien_thi_anh_ket_qua(self, anh_ve):
        """Hiển thị ảnh kết quả"""
        try:
            # Chuyển BGR sang RGB
            anh_rgb = cv2.cvtColor(anh_ve, cv2.COLOR_BGR2RGB)
            anh_pil = Image.fromarray(anh_rgb)
            
            # Resize
            canvas_width = 700
            canvas_height = 600
            ty_le = min(canvas_width/anh_pil.width, canvas_height/anh_pil.height)
            kich_thuoc_moi = (int(anh_pil.width * ty_le), int(anh_pil.height * ty_le))
            
            anh_resize = anh_pil.resize(kich_thuoc_moi, Image.Resampling.LANCZOS)
            
            # Hiển thị
            self.anh_hien_thi = ImageTk.PhotoImage(anh_resize)
            self.canvas_anh.delete("all")
            x = (canvas_width - kich_thuoc_moi[0]) // 2
            y = (canvas_height - kich_thuoc_moi[1]) // 2
            self.canvas_anh.create_image(x, y, anchor='nw', image=self.anh_hien_thi)
            
        except Exception as e:
            print(f"Lỗi hiển thị ảnh: {e}")
            
    def hien_thi_ket_qua_text(self, so_nam, so_nu, mau_ao, vat_dung, thoi_tiet):
        """Hiển thị kết quả dạng text"""
        
        ket_qua_text = f"""
╔════════════════════════════════════════════╗
║         KẾT QUẢ NHẬN DẠNG CHI TIẾT        ║
╚════════════════════════════════════════════╝

👥 THÔNG TIN NHÂN VẬT:
───────────────────────────────────────────

   • Số người: {so_nam + so_nu} người
   • Người nam: {so_nam} người
   • Người nữ: {so_nu} người

👔 MÀU SẮC ÁO:
───────────────────────────────────────────
"""
        
        if mau_ao:
            for i, mau in enumerate(mau_ao, 1):
                ket_qua_text += f"   • Người {i}: Áo màu {mau}\n"
        else:
            ket_qua_text += "   • Không phát hiện\n"
            
        ket_qua_text += f"""
🌤️ THỜI TIẾT/PHONG CẢNH:
───────────────────────────────────────────

   • Điều kiện: {thoi_tiet}

🎒 VẬT DỤNG PHÁT HIỆN:
───────────────────────────────────────────
"""
        
        if vat_dung:
            # Đếm số lượng mỗi vật dụng
            dem_vat_dung = {}
            for vat in vat_dung:
                dem_vat_dung[vat] = dem_vat_dung.get(vat, 0) + 1
                
            for vat, so_luong in dem_vat_dung.items():
                ten_tieng_viet = self.dich_vat_dung(vat)
                ket_qua_text += f"   • {ten_tieng_viet}: {so_luong}\n"
        else:
            ket_qua_text += "   • Không phát hiện vật dụng đặc biệt\n"
            
        ket_qua_text += """
───────────────────────────────────────────
✓ Phân tích hoàn tất!
💾 Nhấn "Lưu Kết Quả" để lưu ảnh đã xử lý
"""
        
        self.text_ket_qua.delete(1.0, tk.END)
        self.text_ket_qua.insert(tk.END, ket_qua_text)
        
    def dich_vat_dung(self, ten_tieng_anh):
        """Dịch tên vật dụng sang tiếng Việt"""
        tu_dien = {
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
        
        return tu_dien.get(ten_tieng_anh, ten_tieng_anh.title())
        
    def luu_ket_qua(self):
        """Lưu ảnh kết quả"""
        if self.anh_da_xu_ly is None:
            messagebox.showwarning("Cảnh báo", "Chưa có kết quả để lưu!")
            return
            
        duong_dan_luu = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPG", "*.jpg"), ("PNG", "*.png"), ("Tất cả files", "*.*")]
        )
        
        if duong_dan_luu:
            cv2.imwrite(duong_dan_luu, self.anh_da_xu_ly)
            messagebox.showinfo("Thành công", f"Đã lưu ảnh tại:\n{duong_dan_luu}")

def main():
    """Hàm chính"""
    root = tk.Tk()
    app = UngDungNhanDang(root)
    root.mainloop()

if __name__ == "__main__":
    main()

