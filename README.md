# Hệ Thống Phát Hiện Buồn Ngủ và Mất Tập Trung Cho Người Lái Xe

## Mô Tả Dự Án
Dự án này triển khai một hệ thống giám sát người lái xe thời gian thực để phát hiện trạng thái buồn ngủ và mất tập trung. Hệ thống sử dụng các kỹ thuật thị giác máy tính và học máy để phân tích khuôn mặt, trạng thái mắt, vị trí đầu và vị trí tay của người lái xe. Khi phát hiện hành vi không an toàn, hệ thống sẽ đưa ra cảnh báo bằng âm thanh và hình ảnh để nhắc nhở người lái xe, giúp ngăn ngừa tai nạn do mệt mỏi hoặc thiếu tập trung.

Các tính năng chính:
- Phát hiện buồn ngủ của tài xế thời gian thực thông qua giám sát trạng thái mắt
- Phát hiện mất tập trung bằng cách theo dõi vị trí đầu và tay
- Hệ thống cảnh báo có thể tùy chỉnh với các cảnh báo liên tục cho đến khi lái xe an toàn trở lại
- Giao diện thân thiện với người dùng để giám sát và cấu hình
- Công cụ thu thập dữ liệu để huấn luyện mô hình cá nhân hóa
- Theo dõi lịch sử vi phạm để phân tích an toàn

## Tài Liệu
- [Giải Thích Mã Nguồn](docs/code_explanation_vi.md) - Giải thích chi tiết về thuật toán, hàm và công thức
- [Công Thức Toán Học](docs/formulas_en.md) - Chi tiết về các công thức toán học sử dụng trong hệ thống
- [Phương Pháp Làm Mịn Dữ Liệu](docs/time_smoothing_en.md) - Giải thích về các phương pháp làm mịn dữ liệu thời gian
- [Hướng Dẫn Sử Dụng](docs/user_guide_vi.md) - Hướng dẫn sử dụng ứng dụng
- [Hướng Dẫn Cho Nhà Phát Triển](docs/developer_guide_vi.md) - Thông tin cho nhà phát triển mở rộng hệ thống

## Công Nghệ và Thư Viện Sử Dụng

### Thị Giác Máy Tính và Học Máy
- **OpenCV**: Xử lý hình ảnh và phát hiện khuôn mặt cơ bản
- **MediaPipe**: Phát hiện điểm mốc khuôn mặt (468 điểm) và theo dõi tay (21 điểm trên mỗi bàn tay)
- **scikit-learn**: Mô hình phân loại SVM
- **NumPy**: Tính toán số học hiệu suất cao

### Giao Diện Người Dùng và Âm Thanh
- **PyQt5**: Framework giao diện đồ họa người dùng
- **PyAudio**: Phát lại âm thanh cảnh báo

## Cấu Trúc Mã Nguồn

```
drowsiness_detection/
│
├── assets/             # Tài nguyên tĩnh cho ứng dụng
│   └── sounds/         # Các tệp âm thanh cảnh báo
│
├── config/             # Các tệp cấu hình
│
├── data/               # Dữ liệu huấn luyện và thu thập dữ liệu
│   ├── collect_data.py # Công cụ thu thập dữ liệu huấn luyện
│   ├── distracted/     # Dữ liệu cho trạng thái mất tập trung của người lái
│   ├── eye_state/      # Dữ liệu cho các trạng thái mắt khác nhau
│   └── focused/        # Dữ liệu cho trạng thái tập trung của người lái
│
├── docs/               # Tài liệu
│   ├── code_explanation_vi.md     # Giải thích chi tiết mã nguồn và thuật toán
│   ├── user_guide_vi.md           # Hướng dẫn sử dụng
│   └── developer_guide_vi.md      # Hướng dẫn cho nhà phát triển
│
├── models/             # Định nghĩa mô hình
│   ├── detection_model.py      # Mô hình dựa trên TensorFlow
│   ├── simple_model.py         # Mô hình SVM nhẹ
│   ├── saved_model.pkl         # Trọng số mô hình đã huấn luyện
│   └── opencv_face_detector_uint8.pb  # Mô hình phát hiện khuôn mặt
│
├── training/           # Tập lệnh huấn luyện mô hình
│   ├── simple_train.py  # Tập lệnh huấn luyện mô hình SVM
│   └── train_model.py   # Tập lệnh huấn luyện mô hình TensorFlow
│
├── ui/                 # Giao diện người dùng
│   └── monitoring_app.py # Giao diện giám sát người lái xe
│
├── utils/              # Hàm tiện ích
│   └── helpers.py      # Hàm hỗ trợ cho camera, chú thích, v.v.
│
├── main.py             # Điểm vào chính cho ứng dụng
├── requirements.txt    # Các phụ thuộc Python
└── retrain_model.py    # Tập lệnh để huấn luyện lại mô hình với dữ liệu mới
```

## Tính Năng Cốt Lõi

### 1. Mô Hình Phát Hiện (`models/simple_model.py`)

Sử dụng mô hình SVM (Support Vector Machine) kết hợp với các đặc trưng sau:
- **Tỷ Lệ Khía Cạnh Mắt (EAR)**: Tính toán độ mở của mắt để phát hiện buồn ngủ
- **Phân tích vị trí đầu**: Phát hiện nếu đầu bị xoay hoặc nghiêng
- **Phát hiện vị trí tay**: Xác định xem tay có được đặt trên vô lăng hay không

Quy trình phát hiện:
1. Phát hiện khuôn mặt trong khung hình video
2. Phát hiện 468 điểm mốc khuôn mặt sử dụng MediaPipe Face Mesh
3. Tính toán EAR dựa trên các điểm mốc mắt
4. Phân tích vị trí đầu dựa trên các điểm mốc khuôn mặt
5. Phát hiện vị trí tay sử dụng MediaPipe Hands
6. Kết hợp tất cả thông tin để xác định trạng thái của người lái xe

### 2. Giao Diện Giám Sát (`ui/monitoring_app.py`)

Giao diện người dùng được xây dựng với PyQt5 với các tính năng:
- Hiển thị luồng video thời gian thực
- Thông báo trạng thái người lái xe (OK/BuồnNgủ/MấtTậpTrung)
- Hiển thị các chỉ số: EAR, vị trí đầu, vị trí tay
- Cài đặt độ nhạy (ngưỡng EAR, ngưỡng độ tin cậy)
- Cảnh báo âm thanh khi phát hiện trạng thái nguy hiểm
- Lưu và tải cấu hình người dùng

### 3. Thu Thập Dữ Liệu (`data/collect_data.py`)

Công cụ thu thập dữ liệu huấn luyện bao gồm:
- Chụp hình khuôn mặt người lái xe qua webcam
- Phân loại tự động trạng thái mắt, vị trí đầu và tay
- Lưu hình ảnh và metadata (JSON) cho huấn luyện

### 4. Huấn Luyện Mô Hình (`training/simple_train.py`)

Quy trình huấn luyện mô hình SVM:
1. Tải và tiền xử lý dữ liệu từ thư mục data/
2. Trích xuất đặc trưng (EAR, vị trí đầu, vị trí tay)
3. Chuẩn hóa đặc trưng
4. Huấn luyện mô hình SVM
5. Đánh giá hiệu suất với tập kiểm thử
6. Lưu mô hình đã huấn luyện

## Hướng Dẫn Sử Dụng

### Chạy Ứng Dụng Giám Sát

```bash
python main.py --mode ui
```

### Thu Thập Dữ Liệu Huấn Luyện

```bash
python main.py --mode collect_data --data_class focused --samples 200
python main.py --mode collect_data --data_class distracted --samples 200
```

### Huấn Luyện Mô Hình

```bash
python main.py --mode train
```

hoặc

```bash
python retrain_model.py
```

## Tính Năng Phát Hiện Chính

### 1. Phát Hiện Buồn Ngủ
- Tính toán Tỷ Lệ Khía Cạnh Mắt (EAR) từ các điểm mốc mắt
- So sánh với ngưỡng (mặc định là 0.2)
- Phát hiện mắt nhắm kéo dài

### 2. Phát Hiện Mất Tập Trung
- Phân tích vị trí đầu (quay sang một bên, nghiêng)
- Xác định vị trí tay (không ở trên vô lăng)
- Kết hợp các yếu tố để đánh giá mức độ mất tập trung

## Cấu Hình Hệ Thống

Các tham số có thể được điều chỉnh trong giao diện người dùng:
- **Ngưỡng EAR**: Điều chỉnh độ nhạy phát hiện buồn ngủ
- **Ngưỡng Độ Tin Cậy**: Điều chỉnh độ tin cậy của phát hiện
- **Nguồn Camera**: Chọn camera để sử dụng
- **Cảnh Báo Âm Thanh**: Bật/tắt và tùy chỉnh

## Phương Pháp Kiểm Thử và Định Hướng Phát Triển

Hệ thống áp dụng một chiến lược kiểm thử toàn diện:

1. **Kiểm Thử Đơn Vị**: Kiểm thử các thành phần riêng lẻ một cách độc lập
2. **Kiểm Thử Tích Hợp**: Kiểm thử cách các thành phần hoạt động cùng nhau
3. **Kiểm Thử Hiệu Suất**: Đảm bảo khả năng hoạt động thời gian thực
4. **Kiểm Thử Đa Điều Kiện**: Kiểm thử dưới các điều kiện ánh sáng và người dùng khác nhau
5. **Kiểm Thử Hồi Quy**: Đảm bảo các thay đổi mới không phá vỡ chức năng hiện có

## Hướng Phát Triển Trong Tương Lai

1. **Kiến Trúc Microservices**: Chia hệ thống thành các dịch vụ nhỏ hơn, chuyên biệt
2. **Kiến Trúc Dựa Trên Sự Kiện**: Triển khai mô hình publish-subscribe để giảm sự phụ thuộc
3. **Học Sâu Nâng Cao**: Triển khai các mô hình theo thời gian (LSTM/RNN) để phân tích chuỗi tốt hơn
4. **Lai Edge-Cloud**: Phân phối xử lý giữa thiết bị cạnh và cơ sở hạ tầng đám mây

## Giấy Phép

Dự án này được cấp phép theo Giấy phép MIT - xem tệp LICENSE để biết chi tiết.

## Lời Cảm Ơn

- Tính toán EAR dựa trên công trình của Soukupová và Čech (2016)
- Đội MediaPipe vì thư viện thị giác tuyệt vời của họ
- Những người đóng góp và người kiểm thử đã giúp cải thiện hệ thống
