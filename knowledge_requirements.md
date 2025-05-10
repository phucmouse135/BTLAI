# Các Kiến Thức Cần Học Để Nắm Vững Dự Án Phát Hiện Buồn Ngủ và Mất Tập Trung Của Tài Xế

## 1. Kiến Thức Nền Tảng

### 1.1 Lập Trình Python
- **Cú pháp cơ bản**: Biến, điều kiện, vòng lặp, hàm
- **Xử lý tệp và thư mục**: Đọc/ghi tệp, làm việc với đường dẫn
- **Lập trình hướng đối tượng**: Lớp, kế thừa, phương thức
- **Xử lý ngoại lệ**: Try/except, xử lý lỗi
- **Thư viện tiêu chuẩn**: os, sys, time, datetime, argparse

### 1.2 Toán Học Cơ Bản
- **Đại số tuyến tính**: Vector, ma trận, phép nhân ma trận
- **Xác suất và thống kê**: Phân phối, trung bình, độ lệch chuẩn
- **Giải tích**: Đạo hàm, độ dốc, cực tiểu hóa hàm số
- **Hình học cơ bản**: Góc, khoảng cách, tọa độ không gian

## 2. Thị Giác Máy Tính

### 2.1 Xử Lý Hình Ảnh Cơ Bản
- **Biểu diễn hình ảnh số**: Pixel, kênh màu (RGB, BGR, Grayscale)
- **Tiền xử lý hình ảnh**: Thay đổi kích thước, cắt, lọc, chuẩn hóa
- **Không gian màu**: Chuyển đổi giữa RGB, HSV, và grayscale
- **Phép biến đổi hình ảnh**: Xoay, lật, cắt, thay đổi kích thước

### 2.2 OpenCV
- **Đọc/ghi/hiển thị hình ảnh và video**: Làm việc với camera và tệp video
- **Xử lý hình ảnh**: Lọc, phân ngưỡng, phát hiện cạnh
- **Phát hiện đối tượng**: Bộ phát hiện khuôn mặt Haar Cascade và DNN
- **Theo dõi đối tượng**: Optical flow, trackers
- **Vẽ và chú thích**: Vẽ hình, thêm văn bản, hiển thị kết quả

### 2.3 MediaPipe
- **Face Mesh**: Phát hiện 468 điểm mốc khuôn mặt
- **Hands**: Phát hiện 21 điểm mốc trên bàn tay
- **Luồng đồ thị MediaPipe**: Hiểu cách xây dựng quy trình xử lý
- **Làm việc với các điểm mốc**: Tính toán khoảng cách, góc, và tỷ lệ

## 3. Học Máy và Học Sâu

### 3.1 Học Máy Cơ Bản
- **Phân loại và hồi quy**: Các loại bài toán học máy
- **Đặc trưng và nhãn**: Cấu trúc dữ liệu học máy
- **Chia tập dữ liệu**: Huấn luyện, xác thực, kiểm thử
- **Đánh giá mô hình**: Độ chính xác, precision, recall, F1-score

### 3.2 Mạng Nơ-ron Tích Chập (CNN)
- **Kiến trúc CNN**: Lớp tích chập, gộp, kích hoạt, kết nối đầy đủ
- **Bộ lọc và kênh**: Cách CNN trích xuất đặc trưng từ hình ảnh
- **Các loại lớp**: Conv2D, MaxPooling, BatchNormalization, Dropout
- **Transfer learning**: Sử dụng mô hình đã huấn luyện trước

### 3.3 TensorFlow/Keras
- **Xây dựng mô hình**: Định nghĩa kiến trúc mô hình CNN
- **Huấn luyện mô hình**: Epochs, batch size, callbacks
- **Đánh giá và dự đoán**: Sử dụng mô hình đã huấn luyện
- **Tăng cường dữ liệu**: Augmentation API và ImageDataGenerator

## 4. Xử Lý Dữ Liệu

### 4.1 Thu Thập và Tiền Xử Lý Dữ Liệu
- **Thu thập dữ liệu**: Cách ghi và gắn nhãn dữ liệu từ webcam
- **Tiền xử lý hình ảnh**: Thay đổi kích thước, chuẩn hóa, tăng cường
- **Gắn nhãn dữ liệu**: Tạo metadata và chú thích
- **Cân bằng dữ liệu**: Xử lý vấn đề mất cân bằng lớp

### 4.2 Tăng Cường Dữ Liệu
- **Biến đổi hình ảnh**: Lật, xoay, phóng to/thu nhỏ
- **Điều chỉnh ánh sáng**: Thay đổi độ sáng, độ tương phản
- **Thêm nhiễu**: Nhiễu Gaussian, mờ, làm méo
- **Tăng cường theo thời gian thực**: Sử dụng augmentation trong quá trình huấn luyện

## 5. Giao Diện Người Dùng và Tích Hợp Hệ Thống

### 5.1 Giao Diện Đồ Họa với PyQt5
- **Các thành phần UI**: Cửa sổ, nút, nhãn, thanh trượt
- **Bố cục và thiết kế**: Tổ chức giao diện người dùng
- **Xử lý sự kiện**: Kết nối nút và hành động
- **Hiển thị hình ảnh và video**: Tích hợp OpenCV và PyQt

### 5.2 Tích Hợp Hệ Thống
- **Luồng dữ liệu camera**: Xử lý khung hình thời gian thực
- **Đa luồng**: Xử lý song song cho hiệu suất tốt hơn
- **Cơ chế cảnh báo**: Âm thanh và trực quan
- **Ghi nhật ký và sự kiện**: Theo dõi và ghi lại hành vi

## 6. Các Thuật Toán Cụ Thể Cho Dự Án

### 6.1 Phát Hiện Trạng Thái Mắt
- **Tỷ Lệ Khía Cạnh Mắt (EAR)**: Công thức và tính toán
- **Ngưỡng phát hiện mắt đóng**: Hiệu chỉnh và tối ưu hóa
- **Theo dõi theo thời gian**: Cửa sổ trượt để giảm nhiễu
- **Phát hiện nháy mắt**: Phân biệt giữa nháy mắt và mắt đóng do buồn ngủ

### 6.2 Phát Hiện Vị Trí Đầu
- **Estimation từ điểm mốc**: Xác định hướng đầu từ các điểm mốc
- **Giám sát hướng nhìn**: Xác định khi tài xế không nhìn vào đường
- **Phân tích độ lệch**: Tính toán độ nghiêng và quay đầu
- **Bù trừ chuyển động camera**: Xử lý rung lắc phương tiện

### 6.3 Phân Tích Vị Trí Tay
- **Phát hiện vị trí tay**: Xác định vị trí tay liên quan đến vô lăng
- **Nhận dạng cử chỉ**: Phát hiện khi tài xế cầm đồ vật
- **Theo dõi đa tay**: Theo dõi đồng thời hai tay
- **Xác định vùng vô lăng**: Thiết lập vùng an toàn cho tay

## 7. Tối Ưu Hóa Hiệu Suất

### 7.1 Tối Ưu Hóa Mô Hình
- **Đơn giản hóa mô hình**: Giảm kích thước mô hình
- **Lượng tử hóa**: Giảm độ chính xác của trọng số
- **Cắt tỉa và nén**: Loại bỏ các kết nối không cần thiết
- **Tối ưu hóa suy luận**: Tăng tốc độ dự đoán

### 7.2 Tối Ưu Hóa Hệ Thống
- **Xử lý khung hình hiệu quả**: Giảm độ phân giải, tỷ lệ khung hình
- **Kỹ thuật buffering**: Quản lý bộ nhớ và khung hình
- **Lập lịch quy trình**: Ưu tiên các tác vụ quan trọng
- **Giám sát tài nguyên**: CPU, bộ nhớ, hiệu suất hệ thống

## 8. Ứng Dụng Thực Tế và Đánh Giá

### 8.1 Kiểm Thử Thực Tế
- **Quy trình kiểm thử**: Thiết lập thử nghiệm thực tế
- **Thu thập và phân tích dữ liệu**: Đánh giá hiệu suất trong môi trường thực
- **Điều chỉnh ngưỡng**: Tối ưu hóa cho độ nhạy và độ đặc hiệu
- **Phản hồi người dùng**: Thu thập và áp dụng phản hồi

### 8.2 Đánh Giá An Toàn
- **Mức độ cảnh báo**: Cân bằng giữa độ nhạy và cảnh báo sai
- **Thời gian phản ứng**: Đo lường độ trễ của hệ thống
- **Độ tin cậy**: Đánh giá tỷ lệ lỗi và ổn định
- **Các tình huống cạnh**: Xử lý các trường hợp đặc biệt

## 9. Kiến Thức Nâng Cao Cho Phát Triển Tương Lai

### 9.1 Học Sâu Nâng Cao
- **Mạng Recurrent (RNN/LSTM)**: Phân tích chuỗi thời gian của hành vi tài xế
- **Mô hình chú ý (Attention)**: Tập trung vào các vùng quan trọng
- **Mô hình dự đoán**: Dự báo buồn ngủ trước khi xảy ra
- **Mô hình cá nhân hóa**: Điều chỉnh theo từng tài xế cụ thể

### 9.2 Triển Khai và Mở Rộng
- **Triển khai trên thiết bị nhúng**: Raspberry Pi, thiết bị di động
- **Tối ưu hóa tài nguyên**: Giảm tiêu thụ năng lượng và bộ nhớ
- **Tích hợp xe hơi**: Kết nối với hệ thống xe
- **Phát triển API**: Giao diện cho các hệ thống bên thứ ba

## 10. Kỹ Năng Mềm Và Vận Hành

### 10.1 Quản Lý Dự Án
- **Lập kế hoạch phát triển**: Roadmap và các cột mốc
- **Kiểm soát phiên bản**: Sử dụng Git hiệu quả
- **Tài liệu**: Viết tài liệu kỹ thuật rõ ràng
- **Kiểm thử và đảm bảo chất lượng**: Quy trình tự động và thủ công

### 10.2 Đạo Đức và Quy Định
- **Quyền riêng tư dữ liệu**: Xử lý hình ảnh người lái xe
- **Tiêu chuẩn an toàn**: Tuân thủ các quy định cho hệ thống ADAS
- **Trách nhiệm AI**: Hiểu được hạn chế của hệ thống
- **Thông báo và đồng ý**: Thông báo người dùng về khả năng và giới hạn
