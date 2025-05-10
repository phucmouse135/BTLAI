# Hệ Thống Phát Hiện Buồn Ngủ và Mất Tập Trung Của Tài Xế

## Mô Tả Dự Án
Dự án này triển khai một hệ thống giám sát tài xế thời gian thực để phát hiện trạng thái buồn ngủ và mất tập trung. Hệ thống sử dụng kỹ thuật thị giác máy tính và học máy để phân tích khuôn mặt, trạng thái mắt, vị trí đầu và vị trí tay của tài xế để xác định xem họ có đang buồn ngủ hoặc mất tập trung hay không. Khi phát hiện hành vi không an toàn, hệ thống sẽ phát ra cảnh báo bằng âm thanh và hình ảnh để nhắc nhở tài xế, giúp ngăn ngừa tai nạn do mệt mỏi hoặc thiếu tập trung.

Các tính năng chính:
- Phát hiện buồn ngủ của tài xế thời gian thực thông qua giám sát trạng thái mắt
- Phát hiện mất tập trung bằng cách theo dõi vị trí đầu và tay
- Hệ thống cảnh báo có thể tùy chỉnh với các cảnh báo liên tục cho đến khi tài xế lái xe an toàn trở lại
- Giao diện thân thiện với người dùng để giám sát và cấu hình
- Công cụ thu thập dữ liệu để huấn luyện mô hình cá nhân hóa
- Theo dõi lịch sử vi phạm để phân tích an toàn

## Các Công Nghệ và Thư Viện Sử Dụng

### Thư Viện Thị Giác Máy Tính và Học Máy
- **OpenCV**: Sử dụng cho xử lý hình ảnh, phát hiện khuôn mặt và các thao tác thị giác máy tính cơ bản
- **MediaPipe**: Cung cấp các giải pháp phát hiện khuôn mặt và tay thời gian thực với độ chính xác cao
- **TensorFlow/Keras**: Framework học sâu được sử dụng để xây dựng và huấn luyện các mô hình phân loại
- **NumPy**: Hỗ trợ tính toán số học hiệu suất cao cho các phép toán ma trận và vector
- **Scikit-learn**: Cung cấp các công cụ phân tích dữ liệu và chia tập dữ liệu huấn luyện/kiểm thử

### Giao Diện Người Dùng và Âm Thanh
- **PyQt5**: Framework giao diện người dùng đồ họa để xây dựng ứng dụng giám sát
- **Matplotlib**: Tạo biểu đồ và trực quan hóa kết quả huấn luyện mô hình
- **PyAudio**: Xử lý phát âm thanh cho các cảnh báo

### Công Cụ Phát Triển và Triển Khai
- **Python 3.8+**: Ngôn ngữ lập trình chính cho toàn bộ dự án
- **Virtualenv/Conda**: Quản lý môi trường ảo để cách ly các phụ thuộc của dự án
- **Git**: Quản lý phiên bản mã nguồn
- **Tqdm**: Hiển thị thanh tiến trình trong quá trình huấn luyện và xử lý dữ liệu

## Chi Tiết Về Các Mô Hình Được Sử Dụng

### 1. Mô Hình Phát Hiện Khuôn Mặt
Dự án sử dụng mô hình phát hiện khuôn mặt của OpenCV dựa trên mạng nơ-ron tích chập sâu (DNN) có sẵn trong tệp `opencv_face_detector_uint8.pb`. Mô hình này:
- Là một mô hình Caffe được huấn luyện trước, được tối ưu hóa cho hiệu suất thời gian thực
- Có khả năng phát hiện khuôn mặt ở nhiều góc độ và điều kiện ánh sáng khác nhau
- Hoạt động hiệu quả ngay cả khi khuôn mặt bị che khuất một phần

### 2. Mô Hình Phân Tích Điểm Mốc Khuôn Mặt
MediaPipe Face Mesh được sử dụng để xác định 468 điểm mốc chi tiết trên khuôn mặt:
- Cung cấp theo dõi thời gian thực các điểm mốc 3D trên khuôn mặt
- Cho phép tính toán chính xác các chỉ số như Tỷ Lệ Khía Cạnh Mắt (EAR)
- Hỗ trợ phát hiện hướng và vị trí đầu thông qua các điểm tham chiếu

### 3. Mô Hình CNN Tùy Chỉnh cho Phân Loại Trạng Thái
`models/detection_model.py` định nghĩa một mô hình CNN tùy chỉnh được thiết kế đặc biệt cho bài toán phát hiện buồn ngủ và mất tập trung:
- Kiến trúc CNN đa lớp với các khối tích chập, gộp và dropout
- Phần đầu ra sử dụng các lớp kết nối đầy đủ với hàm kích hoạt softmax
- Kiến trúc cụ thể:
  - 3 khối tích chập (mỗi khối gồm lớp Conv2D, BatchNormalization, ReLU và MaxPooling)
  - Dropout (0.5) để giảm quá khớp
  - 2 lớp kết nối đầy đủ
  - Lớp đầu ra có 2 nơ-ron (focused/distracted)

### 4. Mô Hình Đơn Giản Hóa cho Thiết Bị Giới Hạn
`models/simple_model.py` cung cấp một mô hình nhẹ hơn cho các thiết bị có tài nguyên tính toán hạn chế:
- Sử dụng ít lớp tích chập hơn để giảm độ phức tạp tính toán
- Áp dụng phép tích chập tách biệt theo chiều sâu (depthwise separable convolution) để giảm số lượng tham số
- Được tối ưu hóa để chạy trên CPU thay vì yêu cầu GPU
- Hiệu suất phân loại giảm nhẹ so với mô hình đầy đủ nhưng đạt được tốc độ suy luận nhanh hơn đáng kể

### 5. Mô Hình Phát Hiện Tay và Phân Tích Tư Thế
MediaPipe Hands được áp dụng để phát hiện và theo dõi vị trí tay:
- Phát hiện 21 điểm mốc 3D trên mỗi bàn tay
- Cho phép nhận dạng các cử chỉ và vị trí tay
- Sử dụng phát hiện nhiều tay để theo dõi đồng thời cả hai tay
- Phân tích khoảng cách giữa các điểm mốc để xác định trạng thái cầm nắm

### Phương Pháp Kết Hợp Mô Hình
Hệ thống sử dụng phương pháp tổng hợp (ensemble method) để kết hợp kết quả từ các mô hình phân tích khác nhau:
- Các đặc trưng từ các mô hình riêng lẻ (mắt, đầu, tay) được kết hợp với trọng số
- Áp dụng cửa sổ trượt thời gian để giảm nhiễu và tăng độ ổn định
- Ngưỡng quyết định có thể điều chỉnh được thông qua giao diện người dùng

## Cấu Trúc Thư Mục
```
drowsiness_detection/
│
├── assets/             # Tài nguyên tĩnh cho ứng dụng
│   └── sounds/         # Các tệp âm thanh cảnh báo
│       ├── distracted_alert.wav
│       └── drowsy_alert.wav
│
├── config/             # Các tệp cấu hình
│
├── data/               # Dữ liệu huấn luyện và xác thực
│   ├── collect_data.py # Công cụ thu thập dữ liệu huấn luyện
│   ├── distracted/     # Hình ảnh và chú thích tài xế mất tập trung
│   ├── eye_state/      # Hình ảnh trạng thái mắt (mở/đóng)
│   ├── focused/        # Hình ảnh tài xế tập trung (trạng thái bình thường)
│   └── hand_position/  # Hình ảnh và chú thích vị trí tay
│
├── models/             # Định nghĩa mô hình và mô hình đã lưu
│   ├── detection_model.py      # Cài đặt mô hình phát hiện cốt lõi
│   ├── simple_model.py         # Mô hình đơn giản hóa để suy luận nhanh hơn
│   ├── saved_model.pkl         # Trọng số mô hình đã huấn luyện
│   └── opencv_face_detector_uint8.pb  # Mô hình phát hiện khuôn mặt
│
├── training/           # Các tập lệnh huấn luyện mô hình
│   ├── simple_train.py  # Tập lệnh huấn luyện cho mô hình đơn giản
│   └── train_model.py   # Tập lệnh huấn luyện chính
│
├── ui/                 # Các thành phần giao diện người dùng
│   └── monitoring_app.py  # Giao diện người dùng chính của ứng dụng giám sát
│
├── utils/              # Các hàm tiện ích
│   └── helpers.py      # Các hàm hỗ trợ được sử dụng trong toàn bộ dự án
│
├── main.py             # Điểm khởi đầu chính cho ứng dụng
├── requirements.txt    # Các gói phụ thuộc Python
└── retrain_model.py    # Tập lệnh để huấn luyện lại mô hình trên dữ liệu mới
```

## Mô Tả Tệp

### Thư Mục Gốc
- **main.py**: Điểm khởi đầu của ứng dụng. Khởi tạo và chạy hệ thống giám sát tài xế.
- **requirements.txt**: Liệt kê tất cả các gói phụ thuộc Python cần thiết cho dự án.
- **retrain_model.py**: Một tập lệnh tiện ích để huấn luyện lại mô hình trên dữ liệu mới mà không cần bắt đầu từ đầu.

### Thu Thập và Quản Lý Dữ Liệu
- **data/collect_data.py**: Một tập lệnh sử dụng webcam để thu thập và gắn nhãn dữ liệu huấn luyện cho các trạng thái khác nhau (buồn ngủ, mất tập trung, tập trung, v.v.).
- **data/distracted/**, **data/eye_state/**, **data/focused/**, **data/hand_position/**: Các thư mục chứa dữ liệu được gắn nhãn để huấn luyện, bao gồm cả hình ảnh và tệp chú thích JSON.

### Mô Hình
- **models/detection_model.py**: Định nghĩa kiến trúc mô hình phát hiện cốt lõi được sử dụng để nhận diện buồn ngủ và mất tập trung.
- **models/simple_model.py**: Một mô hình đơn giản hóa, hiệu quả hơn để suy luận thời gian thực với yêu cầu tính toán thấp hơn.
- **models/saved_model.pkl**: Trọng số mô hình đã huấn luyện, sẵn sàng cho suy luận.
- **models/opencv_face_detector_uint8.pb**: Mô hình phát hiện khuôn mặt OpenCV đã huấn luyện trước được sử dụng để xác định vị trí khuôn mặt tài xế trong mỗi khung hình.

### Huấn Luyện
- **training/simple_train.py**: Tập lệnh để huấn luyện phiên bản mô hình đơn giản hóa.
- **training/train_model.py**: Tập lệnh huấn luyện chính xử lý việc tải dữ liệu, tăng cường, huấn luyện mô hình và đánh giá.

### Giao Diện Người Dùng
- **ui/monitoring_app.py**: Triển khai giao diện người dùng đồ họa dựa trên PyQt5 cho ứng dụng giám sát, bao gồm hiển thị luồng camera, trực quan hóa cảnh báo và tùy chọn cấu hình.

### Tiện Ích
- **utils/helpers.py**: Chứa các hàm tiện ích cho xử lý video, phát hiện và trực quan hóa được sử dụng trong toàn bộ dự án.

## Các Mô Hình Được Sử Dụng
Dự án này tận dụng một số mô hình thị giác máy tính và học máy:

1. **Mô Hình Phát Hiện Khuôn Mặt**: Sử dụng mô hình phát hiện khuôn mặt được huấn luyện trước của OpenCV để xác định vị trí khuôn mặt tài xế trong mỗi khung hình.

2. **Bộ Phân Loại Trạng Thái Mắt**: Phát hiện xem mắt tài xế đang mở hay đóng bằng cách phân tích vùng mắt. Sử dụng cách tiếp cận ngưỡng Tỷ Lệ Khía Cạnh Mắt (EAR) kết hợp với các đặc trưng học máy.

3. **Bộ Theo Dõi Vị Trí Đầu**: Giám sát vị trí và hướng đầu của tài xế để phát hiện khi họ không nhìn vào đường.

4. **Bộ Phát Hiện Vị Trí Tay**: Xác định khi tay tài xế không ở đúng vị trí trên vô lăng.

5. **Mô Hình An Toàn Đơn Giản**: Một mô hình nhẹ kết hợp tất cả các thành phần phát hiện để giám sát thời gian thực hiệu quả trên các hệ thống có tài nguyên tính toán hạn chế.

## Quy Trình Thu Thập Dữ Liệu Chi Tiết

### 1. Thiết Lập Cấu Trúc Thư Mục
Quá trình thu thập dữ liệu bắt đầu bằng việc thiết lập một cấu trúc thư mục được tổ chức tốt để lưu trữ các loại dữ liệu khác nhau:

- **Các lớp chính**: `focused` (tập trung) và `distracted` (mất tập trung)
- **Các lớp chi tiết**:
  - `eye_state`: Trạng thái mắt (mở, nửa mở, đóng)
  - `head_position`: Vị trí đầu (thẳng, nghiêng, quay sang một bên)
  - `hand_position`: Vị trí tay (trên vô lăng, không trên vô lăng, cầm đồ vật)

### 2. Phân Tích Khuôn Mặt và Trích Xuất Đặc Trưng

Trong quá trình thu thập dữ liệu, hệ thống thực hiện một số phân tích thời gian thực:

#### Phân Tích Trạng Thái Mắt
- Sử dụng MediaPipe Face Mesh để xác định các điểm mốc trên khuôn mặt
- Tính toán Tỷ Lệ Khía Cạnh Mắt (EAR) bằng cách đo khoảng cách giữa các điểm mốc quanh mắt
- Phân loại trạng thái mắt dựa trên EAR:
  - EAR < 0.15: Mắt đóng
  - EAR < 0.25: Mắt nửa mở
  - EAR ≥ 0.25: Mắt mở

#### Phân Tích Vị Trí Đầu
- Sử dụng điểm mũi làm tham chiếu để xác định hướng đầu
- Tính toán độ lệch từ tâm để xác định nếu đầu đang quay sang một bên
- Phân tích khoảng cách dọc giữa trán và cằm để phát hiện nghiêng đầu

#### Phân Tích Vị Trí Tay
- Sử dụng MediaPipe Hands để phát hiện và theo dõi tay
- Xác định vị trí của tay liên quan đến khu vực vô lăng (được giả định là nằm ở phần dưới giữa khung hình)
- Phân tích khoảng cách giữa ngón cái và ngón trỏ để phát hiện cầm nắm

### 3. Thu Thập Dữ Liệu và Ghi Lại Thông Tin
- Dữ liệu được thu thập trong chế độ thời gian thực thông qua webcam
- Người dùng có thể bắt đầu/tạm dừng quá trình thu thập bằng phím 's'
- Mỗi hình ảnh có thể được ghi lại trong thư mục chính (focused/distracted) và trong các thư mục con chi tiết
- Hình ảnh được lưu với mốc thời gian độc nhất để tránh trùng lặp
- Mỗi hình ảnh đi kèm với một tệp metadata JSON chứa:
  - Tên tập tin
  - Lớp chính (focused/distracted)
  - Tỷ lệ khía cạnh mắt (EAR)
  - Trạng thái mắt (mở/nửa mở/đóng)
  - Vị trí đầu (thẳng/nghiêng/quay sang một bên)
  - Vị trí tay (trên vô lăng/không trên vô lăng/cầm đồ vật)
  - Mốc thời gian

### 4. Đặc Điểm Thu Thập Nâng Cao
- **Thu thập có hướng dẫn**: Hệ thống hiển thị các chỉ số thời gian thực để người thu thập có thể điều chỉnh tư thế
- **Thu thập có mục tiêu**: Có thể chỉ tập trung vào một đặc điểm cụ thể (ví dụ: chỉ thu thập dữ liệu về mắt đóng)
- **Kiểm tra tư thế**: Khi thu thập dữ liệu cho một lớp cụ thể, hệ thống kiểm tra xem tư thế hiện tại có phù hợp không

## Quy Trình Huấn Luyện Mô Hình Chi Tiết

### 1. Tải và Tiền Xử Lý Dữ Liệu
- Hình ảnh được tải từ các thư mục lớp (focused/distracted)
- Mỗi hình ảnh được:
  - Chuyển đổi từ BGR sang RGB
  - Thay đổi kích thước thành 100x100 pixel
  - Chuẩn hóa giá trị pixel chia cho 255
- Nhãn được mã hóa one-hot (0 = focused, 1 = distracted)
- Dữ liệu được chia thành tập huấn luyện (80%) và tập kiểm thử (20%)

### 2. Tăng Cường Dữ Liệu
Để cải thiện khả năng khái quát hóa của mô hình, các kỹ thuật tăng cường dữ liệu được áp dụng:
- Lật ngang ngẫu nhiên
- Xoay nhẹ (±0.1 radian)
- Phóng to/thu nhỏ ngẫu nhiên (±10%)
- Điều chỉnh độ sáng ngẫu nhiên (±10%)
- Điều chỉnh độ tương phản ngẫu nhiên (±10%)

Việc tăng cường được thực hiện trên-the-fly sử dụng API Dataset của TensorFlow, giúp quá trình huấn luyện hiệu quả hơn về bộ nhớ.

### 3. Kiến Trúc Mô Hình
Mô hình được định nghĩa trong `models/detection_model.py` và thiết kế để phát hiện cả trạng thái buồn ngủ và mất tập trung. Cấu trúc mô hình chính bao gồm:
- Các lớp tích chập (Convolutional layers) để trích xuất đặc trưng
- Các lớp gộp (Pooling layers) để giảm kích thước không gian
- Dropout để ngăn ngừa quá khớp
- Các lớp kết nối đầy đủ (Fully connected layers) cho việc phân loại cuối cùng

### 4. Quá Trình Huấn Luyện
- Mô hình được huấn luyện qua nhiều epoch (mặc định là 20)
- Kích thước batch mặc định là 32
- Quá trình huấn luyện theo dõi độ chính xác và mất mát trên cả tập huấn luyện và tập xác thực
- Các kết quả và trọng số mô hình tốt nhất được lưu lại
- Hệ thống tạo ra các biểu đồ hiển thị tiến trình huấn luyện

### 5. Đánh Giá Mô Hình
- Mô hình được đánh giá trên tập kiểm thử chưa được sử dụng trong quá trình huấn luyện
- Các số liệu chính bao gồm độ chính xác, mất mát và các chỉ số khác
- Kết quả đánh giá được lưu và hiển thị thông qua các biểu đồ

### 6. Lưu Trữ và Sử Dụng Mô Hình
- Mô hình được lưu vào `models/saved_model.pkl`
- Quá trình lưu trữ bao gồm cả kiến trúc mô hình và trọng số đã huấn luyện
- Lưu lại các tham số tiền xử lý để đảm bảo tính nhất quán giữa huấn luyện và suy luận

## Hướng Dẫn Thực Hành

### Thu Thập Dữ Liệu Mới
```bash
# Thu thập dữ liệu cho lớp focused (tập trung)
python data/collect_data.py --class focused --samples 200

# Thu thập dữ liệu cho lớp distracted (mất tập trung)
python data/collect_data.py --class distracted --samples 200

# Thu thập dữ liệu cụ thể cho trạng thái mắt đóng
python data/collect_data.py --class eyes_closed --samples 100

# Thu thập dữ liệu cho vị trí tay trên vô lăng
python data/collect_data.py --class hands_on_wheel --samples 100
```

Khi thu thập dữ liệu:
1. Ngồi ở vị trí tương tự như khi lái xe
2. Thay đổi điều kiện ánh sáng để đảm bảo mô hình hoạt động ổn định
3. Quay góc khác nhau của khuôn mặt để mô hình có khả năng nhận diện tốt hơn
4. Thu thập dữ liệu trong các khoảng thời gian khác nhau trong ngày
5. Đối với dữ liệu "mất tập trung", hãy mô phỏng các hành vi thực tế như nhìn điện thoại, điều chỉnh radio, nói chuyện với hành khách

### Các Mẹo Để Có Mô Hình Tốt Hơn
1. **Cân bằng dữ liệu**: Đảm bảo số lượng mẫu giữa các lớp tương đối bằng nhau
2. **Đa dạng hóa môi trường**: Thu thập dữ liệu trong nhiều điều kiện ánh sáng, góc camera và môi trường khác nhau
3. **Tăng cường dữ liệu phức tạp hơn**: Thêm các kỹ thuật tăng cường dữ liệu nâng cao như thay đổi độ bão hòa, thêm nhiễu, thay đổi tỷ lệ khía cạnh
4. **Tinh chỉnh siêu tham số**: Thử nghiệm với các tốc độ học khác nhau, kích thước batch và số lượng epoch
5. **Thêm dữ liệu cạnh biên**: Thêm nhiều mẫu cho các trường hợp khó phân biệt (như mắt nửa mở)

## Hướng Dẫn Đầy Đủ: Từ Phát Triển đến Triển Khai

### 1. Thiết Lập Môi Trường
```bash
# Clone repository (nếu áp dụng)
git clone https://your-repository-url/drowsiness_detection.git
cd drowsiness_detection

# Tạo môi trường ảo (tùy chọn nhưng được khuyến nghị)
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Cài đặt các gói phụ thuộc
pip install -r requirements.txt
```

### 2. Quy Trình Thu Thập Dữ Liệu
```bash
# # Chạy tập lệnh thu thập dữ liệu
# python data/collect_data.py

# Thu thập dữ liệu cho trạng thái tập trung
python data/collect_data.py --class focused --samples 200

# Thu thập dữ liệu cho trạng thái mất tập trung
python data/collect_data.py --class distracted --samples 200

# Thu thập dữ liệu cho trạng thái mắt đóng
python data/collect_data.py --class eyes_closed --samples 100
```
Trong quá trình thu thập dữ liệu:
1. Làm theo hướng dẫn trên màn hình để chụp hình ảnh cho các trạng thái khác nhau
2. Đối với mỗi trạng thái (buồn ngủ, tập trung, mất tập trung), cố gắng thu thập ít nhất 100-200 mẫu
3. Thử thay đổi điều kiện ánh sáng, vị trí và góc để huấn luyện mạnh mẽ
4. Đảm bảo chụp cả ví dụ tích cực và tiêu cực cho mỗi trạng thái

Tập lệnh sẽ tự động lưu hình ảnh với dấu thời gian và tạo các tệp chú thích JSON.

### 3. Huấn Luyện Mô Hình

#### Huấn Luyện Cơ Bản
```bash
# Huấn luyện mô hình sử dụng dữ liệu đã thu thập
python training/train_model.py
```

#### Tùy Chọn Huấn Luyện Nâng Cao
```bash
# Huấn luyện với các tham số tùy chỉnh
python training/train_model.py --epochs 50 --batch_size 32 --learning_rate 0.001
```

Quy trình huấn luyện:
1. Tải và tiền xử lý các hình ảnh và chú thích đã thu thập
2. Chia dữ liệu thành tập huấn luyện và tập xác thực
3. Tăng cường dữ liệu huấn luyện để cải thiện độ mạnh mẽ của mô hình
4. Huấn luyện mô hình sử dụng kiến trúc CNN
5. Đánh giá hiệu suất trên tập xác thực
6. Lưu mô hình hoạt động tốt nhất vào `models/saved_model.pkl`

#### Huấn Luyện Lại Mô Hình Hiện Có
```bash
# Huấn luyện lại với dữ liệu mới trong khi tận dụng trọng số mô hình hiện có
python retrain_model.py --model_path models/saved_model.pkl --new_data_path data/new_samples/
```

### 4. Chạy Hệ Thống Giám Sát
```bash
# Khởi động ứng dụng giám sát tài xế
python main.py
```

Sử dụng ứng dụng:
1. Chọn camera của bạn từ menu thả xuống
2. Nhấp "Bắt Đầu Camera" để bắt đầu giám sát
3. Cấu hình độ nhạy phát hiện bằng thanh trượt nếu cần
4. Chọn giữa các chế độ "Tất Cả Tính Năng", "Chỉ Buồn Ngủ" hoặc "Chỉ Mất Tập Trung"
5. Bật/tắt cảnh báo âm thanh và cảnh báo liên tục theo mong muốn
6. Hệ thống sẽ hiển thị trạng thái thời gian thực và ghi lại các vi phạm

### 5. Đánh Giá và Tinh Chỉnh
1. Xem lại lịch sử vi phạm để xác định mô hình và điều chỉnh độ nhạy
2. Tinh chỉnh ngưỡng trong bảng cài đặt để có hiệu suất tối ưu
3. Nếu các trường hợp dương tính giả/âm tính giả xảy ra thường xuyên, thu thập thêm dữ liệu huấn luyện có mục tiêu và huấn luyện lại

## Hướng Phát Triển Tương Lai

1. **Phát Hiện Đa Người Dùng**: Mở rộng hệ thống để giám sát nhiều người trong một phương tiện, bao gồm cả sự mất tập trung của hành khách.

2. **Tích Hợp với Hệ Thống Phương Tiện**: Phát triển giao diện để kết nối với hệ thống phương tiện cho các phản hồi tự động (ví dụ: điều chỉnh kiểm soát hành trình thích ứng, hỗ trợ giữ làn đường).

3. **Phiên Bản Ứng Dụng Di Động**: Tạo phiên bản ứng dụng di động có thể gắn trên bảng điều khiển để sử dụng trong các phương tiện không có hệ thống giám sát tích hợp.

4. **Cải Thiện Khả Năng Thích Ứng Môi Trường**: Nâng cao hiệu suất trong các điều kiện ánh sáng khác nhau, bao gồm lái xe ban đêm và môi trường ánh sáng thay đổi nhanh chóng.

5. **Mở Rộng Phát Hiện Mất Tập Trung**: Thêm phát hiện cho các nguồn mất tập trung bổ sung như sử dụng điện thoại di động, ăn uống hoặc hút thuốc.

6. **Tích Hợp Đám Mây**: Triển khai đồng bộ hóa đám mây cho các ứng dụng quản lý đội xe để theo dõi sự tỉnh táo của tài xế trên nhiều phương tiện.

7. **Cảnh Báo Dự Đoán**: Phát triển các thuật toán để dự đoán khởi đầu của buồn ngủ trước khi đạt đến ngưỡng tới hạn, dựa trên các mẫu hành vi vi mô.

8. **Mô Hình Cá Nhân Hóa**: Triển khai hiệu chuẩn theo người dùng cụ thể để tính đến sự khác biệt cá nhân trong biểu hiện khuôn mặt và hành vi cơ bản.

9. **Tăng Tốc Phần Cứng**: Tối ưu hóa các mô hình để triển khai trên phần cứng chuyên dụng (GPU, TPU hoặc ASIC chuyên dụng) để cải thiện hiệu suất và giảm tiêu thụ năng lượng.

10. **Tuân Thủ Quy Định**: Điều chỉnh phát triển theo các tiêu chuẩn và quy định an toàn giao thông mới cho hệ thống giám sát tài xế.