# Hệ Thống Phát Hiện Buồn Ngủ: Giải Thích Mã Nguồn

Tài liệu này cung cấp giải thích chi tiết về các hàm quan trọng, mô hình, thư viện và công thức toán học được sử dụng trong hệ thống phát hiện buồn ngủ.

## Thuật Toán Phát Hiện Cốt Lõi

### Tính Toán Tỷ Lệ Khía Cạnh Mắt (EAR)

Tỷ lệ khía cạnh mắt (EAR) là một thông số quan trọng được sử dụng để xác định độ mở của mắt. Công thức toán học cho EAR là:

```
EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
```

Trong đó:
- p1 đến p6 là các điểm mốc khuôn mặt tương ứng với mắt
- ||p1-p4|| đại diện cho khoảng cách Euclidean giữa các điểm p1 và p4

Trong mã nguồn, điều này được triển khai trong `models/simple_model.py`:

```python
def _calculate_improved_ear(self, landmarks, left_eye_indices, right_eye_indices):
    """
    Tính toán Tỷ lệ Khía cạnh Mắt (EAR) cho cả hai mắt sử dụng các điểm mốc khuôn mặt.
    """
    # Trích xuất tọa độ cho mắt trái và phải
    left_eye_points = np.array([landmarks[i] for i in left_eye_indices])
    right_eye_points = np.array([landmarks[i] for i in right_eye_indices])
    
    # Tính toán EAR cho mắt trái
    left_ear = self._calculate_single_ear(left_eye_points)
    
    # Tính toán EAR cho mắt phải
    right_ear = self._calculate_single_ear(right_eye_points)
    
    # Trả về giá trị EAR trung bình cho cả hai mắt
    return (left_ear + right_ear) / 2.0

def _calculate_single_ear(self, eye_points):
    """
    Tính toán EAR cho một mắt đơn.
    Tham khảo: Bài báo của Soukupová và Čech (2016) về phát hiện nháy mắt thời gian thực
    """
    # Tính toán khoảng cách theo chiều dọc
    v1 = np.linalg.norm(eye_points[1] - eye_points[5])
    v2 = np.linalg.norm(eye_points[2] - eye_points[4])
    
    # Tính toán khoảng cách theo chiều ngang
    h = np.linalg.norm(eye_points[0] - eye_points[3])
    
    # Tính toán EAR
    ear = (v1 + v2) / (2.0 * h)
    return ear
```

Khi mắt mở, giá trị EAR thường nằm trong khoảng 0,25-0,35. Khi mắt nhắm, EAR giảm đáng kể, thường xuống dưới 0,2. Hệ thống sử dụng ngưỡng có thể cấu hình (mặc định là 0,2) để xác định khi nào mắt đang nhắm.

### Phát Hiện Vị Trí Đầu

Vị trí đầu được xác định bằng cách phân tích hướng và vị trí của các điểm mốc khuôn mặt so với vị trí tham chiếu:

#### Công Thức Tính Góc Xoay Đầu

Hệ thống sử dụng nhiều phương pháp để xác định góc xoay đầu:

1. **Góc nghiêng (tilt angle/roll)**: Tính toán dựa trên độ nghiêng của đường nối hai mắt

```
angle_rad = arctan2(eye_line[1], eye_line[0])
angle_deg = angle_rad × (180/π)
```

Trong đó:
- `eye_line = right_eye_center - left_eye_center` là vector nối giữa tâm mắt phải và tâm mắt trái
- `arctan2(y, x)` là hàm lượng giác hai tham số trả về góc trong khoảng [-π, π]
- Kết quả góc được chuẩn hóa về khoảng [-90°, 90°]

2. **Góc quay ngang (yaw)**: Xác định bằng phương pháp độ lệch của mũi khỏi trục giữa khuôn mặt

```
nose_deviation = (nose_tip[0] - midpoint_x) / face_width
```

Trong đó:
- `nose_tip[0]` là tọa độ x của điểm mũi
- `midpoint_x` là tọa độ x của điểm giữa hai mắt
- `face_width` là chiều rộng khuôn mặt (khoảng cách lớn nhất theo chiều x)

3. **Công thức xác định trạng thái xoay đầu**:

```
is_tilted = |angle_deg| > 20
is_looking_sideways = |nose_deviation| > 0.15
```

Các công thức chi tiết hơn về tính toán góc xoay đầu có thể được tìm thấy trong [formulas.md](formulas.md) (Tiếng Việt) hoặc [formulas_en.md](formulas_en.md) (Tiếng Anh).

```python
def _detect_head_position(self, landmarks):
    """
    Phát hiện vị trí đầu sử dụng các điểm mốc khuôn mặt.
    Trả về: thẳng, nghiêng, hoặc quay sang một bên
    """
    # Chuẩn hóa điểm mốc để loại bỏ ảnh hưởng của khoảng cách từ camera
    normalized_landmarks = self._normalize_landmarks(landmarks)
    
    # Trích xuất các điểm mốc khuôn mặt chính để phân tích hướng
    nose_tip = normalized_landmarks[self.NOSE_TIP_INDEX]
    left_eye = normalized_landmarks[self.LEFT_EYE_CENTER_INDEX]
    right_eye = normalized_landmarks[self.RIGHT_EYE_CENTER_INDEX]
    
    # Tính toán sự xoay của đầu quanh trục Y (quay trái/phải)
    eye_line_vector = right_eye - left_eye
    eye_line_center = (left_eye + right_eye) / 2
    nose_offset = nose_tip - eye_line_center
    
    # Tính toán các chỉ số
    horizontal_angle = np.arctan2(nose_offset[0], nose_offset[2])
    vertical_angle = np.arctan2(nose_offset[1], nose_offset[2])
    
    # Xác định vị trí đầu dựa trên các góc
    if abs(horizontal_angle) > self.HEAD_TURNED_THRESHOLD:
        return "turned_sideways"
    elif abs(vertical_angle) > self.HEAD_TILTED_THRESHOLD:
        return "tilted"
    else:
        return "straight"
```

### Phát Hiện Vị Trí Tay

Hệ thống theo dõi xem tay của người lái xe có được đặt đúng vị trí trên vô lăng hay không:

#### Công Thức Tính Khoảng Cách Tay Với Vô Lăng

Khoảng cách giữa tay và vị trí vô lăng được tính toán sử dụng công thức khoảng cách Euclidean trong không gian 2D:

```
distance = √[(wrist_x - wheel_center_x)² + (wrist_y - wheel_center_y)²]
```

Trong đó:
- `wrist_x, wrist_y` là tọa độ của điểm cổ tay (MediaPipe landmark index 0)
- `wheel_center_x, wheel_center_y` là tọa độ ước tính của trung tâm vô lăng
- Khoảng cách này được so sánh với bán kính ước tính của vô lăng để xác định vị trí tay

Vị trí tay khi sử dụng điện thoại được phát hiện bằng cách phân tích hình dạng tay:

```
finger_spread = σ(finger_coordinates)
tight_grip = mean(finger_spread) < (frame_width × 0.1)
```

Chi tiết đầy đủ về công thức tính khoảng cách tay với vô lăng và phát hiện sử dụng điện thoại có thể được tìm thấy trong [formulas.md](formulas.md) (Tiếng Việt) hoặc [formulas_en.md](formulas_en.md) (Tiếng Anh).

Trong đó:
- `σ(finger_coordinates)` là độ lệch chuẩn của tọa độ các đầu ngón tay
- `frame_width` là chiều rộng khung hình
- `tight_grip` (nắm chặt) là điều kiện khi các ngón tay gần nhau như khi cầm điện thoại

```python
def _detect_hand_position(self, hand_landmarks):
    """
    Phát hiện xem tay có ở trên vô lăng dựa trên các điểm mốc của tay.
    Trả về: on_wheel hoặc not_on_wheel
    """
    if not hand_landmarks or len(hand_landmarks) < 1:
        return "not_on_wheel"
    
    # Xác định khu vực vô lăng (điều này sẽ được hiệu chỉnh cho từng cài đặt xe)
    wheel_center_x = 0.5  # trung tâm khung hình
    wheel_center_y = 0.7  # phần dưới khung hình
    wheel_radius = 0.2    # tương đối so với kích thước khung hình
    
    hands_on_wheel_count = 0
    
    # Kiểm tra từng bàn tay được phát hiện
    for landmarks in hand_landmarks:
        # Sử dụng vị trí cổ tay làm chỉ báo vị trí tay
        wrist_landmark = landmarks[0]
        
        # Tính khoảng cách từ trung tâm vô lăng
        distance = np.sqrt((wrist_landmark[0] - wheel_center_x)**2 + 
                          (wrist_landmark[1] - wheel_center_y)**2)
        
        # Kiểm tra xem tay có ở trên vô lăng không
        if distance <= wheel_radius:
            hands_on_wheel_count += 1
    
    # Ít nhất một tay phải ở trên vô lăng
    if hands_on_wheel_count >= 1:
        return "on_wheel"
    else:
        return "not_on_wheel"
```

## Mô Hình Máy Học

### Phân Loại SVM (simple_model.py)

Hệ thống sử dụng Support Vector Machine (SVM) để phân loại trạng thái của người lái xe:

```python
def _extract_simple_features(self, face_landmarks, hands_landmarks, ear_value, 
                            head_position, hand_position, frame_shape):
    """
    Trích xuất đặc trưng cho phân loại SVM
    """
    features = []
    
    # Đặc trưng EAR
    features.append(ear_value)
    
    # Đặc trưng vị trí đầu - one-hot encoding
    head_pos_features = [0, 0, 0]  # [straight, tilted, turned_sideways]
    if head_position == "straight":
        head_pos_features[0] = 1
    elif head_position == "tilted":
        head_pos_features[1] = 1
    elif head_position == "turned_sideways":
        head_pos_features[2] = 1
    features.extend(head_pos_features)
    
    # Đặc trưng vị trí tay - nhị phân
    hand_pos_feature = 1 if hand_position == "on_wheel" else 0
    features.append(hand_pos_feature)
    
    # Đặc trưng hình học bổ sung từ các điểm mốc
    if face_landmarks is not None:
        # Tính toán góc giữa các điểm mốc cụ thể
        # Thêm khoảng cách được chuẩn hóa giữa các điểm chính
        pass
    
    return np.array(features)
```

Mô hình SVM được huấn luyện sử dụng dữ liệu có nhãn được thu thập từ module thu thập dữ liệu:

```python
def train(self, X_train, y_train):
    """
    Huấn luyện mô hình SVM
    """
    # Chuẩn hóa các đặc trưng
    self.scaler = StandardScaler()
    X_train_normalized = self.scaler.fit_transform(X_train)
    
    # Huấn luyện mô hình SVM
    self.model = SVC(kernel='rbf', C=1.0, gamma='scale', probability=True)
    self.model.fit(X_train_normalized, y_train)
    
    return self.model
```

### Mô Hình CNN (detection_model.py)

Đối với phát hiện nâng cao hơn, một Mạng Nơ-ron Tích chập (CNN) được triển khai:

```python
def _create_model(self):
    """
    Tạo kiến trúc CNN cho phát hiện buồn ngủ
    """
    model = Sequential([
        # Khối tích chập đầu tiên
        Conv2D(32, (3, 3), padding='same', input_shape=(self.img_height, self.img_width, 6)),
        BatchNormalization(),
        Activation('relu'),
        MaxPooling2D(pool_size=(2, 2)),
        
        # Khối tích chập thứ hai
        Conv2D(64, (3, 3), padding='same'),
        BatchNormalization(),
        Activation('relu'),
        MaxPooling2D(pool_size=(2, 2)),
        
        # Khối tích chập thứ ba
        Conv2D(128, (3, 3), padding='same'),
        BatchNormalization(),
        Activation('relu'),
        MaxPooling2D(pool_size=(2, 2)),
        
        # Lớp Dropout để ngăn ngừa quá khớp
        Dropout(0.5),
        
        # Các lớp Flatten và Dense
        Flatten(),
        Dense(128, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        Dense(2, activation='softmax')  # 2 lớp: tập trung/mất tập trung
    ])
    
    # Biên dịch mô hình
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model
```

## Thư Viện và Các Phụ Thuộc

### Thị Giác Máy Tính và Học Máy

1. **OpenCV** (cv2):
   - Dùng cho các thao tác xử lý hình ảnh
   - Xử lý camera và chụp khung hình
   - Phát hiện khuôn mặt cơ bản sử dụng Haar cascade hoặc mô hình DNN
   - Vẽ chú thích trên khung hình

2. **MediaPipe**:
   - Face mesh để phát hiện 468 điểm mốc khuôn mặt
   - Theo dõi tay để phát hiện 21 điểm trên mỗi bàn tay
   - Cung cấp tọa độ 3D để phân tích không gian chính xác hơn

3. **scikit-learn**:
   - Triển khai SVM để phân loại
   - Chuẩn hóa đặc trưng với StandardScaler
   - Các chỉ số đánh giá mô hình (độ chính xác, precision, recall)

4. **NumPy**:
   - Thao tác mảng hiệu quả cho xử lý điểm mốc
   - Tính toán toán học cho EAR và các chỉ số khác
   - Xử lý vector đặc trưng

### Giao Diện Người Dùng và Âm Thanh

1. **PyQt5**:
   - Cửa sổ ứng dụng chính
   - Hiển thị video thời gian thực
   - Điều khiển cấu hình
   - Hiển thị chỉ báo trạng thái và số liệu

2. **PyAudio**:
   - Phát âm thanh cảnh báo
   - Thu âm cho lệnh thoại (phát triển trong tương lai)

## Quy Trình Phát Hiện

Toàn bộ quy trình phát hiện có thể được tóm tắt như sau:

1. **Lấy Khung Hình**:
   - Chụp khung hình từ camera sử dụng OpenCV

2. **Phát Hiện Khuôn Mặt**:
   - Phát hiện khuôn mặt trong khung hình sử dụng MediaPipe Face Detection

3. **Phát Hiện Điểm Mốc**:
   - Trích xuất 468 điểm mốc khuôn mặt sử dụng MediaPipe Face Mesh
   - Trích xuất điểm mốc tay nếu tay hiển thị

4. **Trích Xuất Đặc Trưng**:
   - Tính toán EAR từ các điểm mốc mắt
   - Xác định vị trí đầu từ các điểm mốc khuôn mặt
   - Phát hiện vị trí tay tương đối với khu vực vô lăng

5. **Phân Loại Trạng Thái**:
   - Trích xuất vector đặc trưng
   - Chuẩn hóa đặc trưng
   - Áp dụng mô hình SVM hoặc CNN cho phân loại

6. **Làm Mịn Thời Gian**:
   - Áp dụng cửa sổ trượt để giảm kết quả dương tính giả
   - Yêu cầu phát hiện liên tiếp để kích hoạt cảnh báo
   - Xem thêm chi tiết các phương pháp làm mịn dữ liệu trong [time_smoothing.md](time_smoothing.md) (Tiếng Việt) hoặc [time_smoothing_en.md](time_smoothing_en.md) (Tiếng Anh)

7. **Hệ Thống Cảnh Báo**:
   - Cảnh báo trực quan trên UI
   - Cảnh báo âm thanh cho các trạng thái được phát hiện
   - Ghi lại vi phạm để phân tích sau này

> **Ghi chú**: Các công thức tính toán chi tiết cho các ngưỡng phát hiện và điều kiện trạng thái có thể được tìm thấy trong tài liệu [formulas.md](formulas.md) (Tiếng Việt) hoặc [formulas_en.md](formulas_en.md) (Tiếng Anh).

## Logic Máy Trạng Thái

Hệ thống triển khai một máy trạng thái đơn giản để quản lý trạng thái của người lái xe:

```
TRẠNG_THÁI_BÌNH_THƯỜNG ⟷ TRẠNG_THÁI_CẢNH_BÁO ⟷ TRẠNG_THÁI_BÁO_ĐỘNG
```

Chuyển đổi giữa các trạng thái được quản lý dựa trên độ tin cậy phát hiện và thời lượng:

```python
def update_driver_state(self, drowsy, distracted):
    """
    Cập nhật trạng thái người lái xe dựa trên kết quả phát hiện
    """
    # Logic chuyển đổi trạng thái
    if drowsy or distracted:
        self.consecutive_detections += 1
        
        if self.state == "NORMAL" and self.consecutive_detections >= self.WARNING_THRESHOLD:
            self.state = "WARNING"
            
        elif self.state == "WARNING" and self.consecutive_detections >= self.ALERT_THRESHOLD:
            self.state = "ALERT"
            return True  # Kích hoạt cảnh báo
    else:
        self.consecutive_detections = 0
        
        if self.state != "NORMAL":
            self.recovery_frames += 1
            if self.recovery_frames >= self.RECOVERY_THRESHOLD:
                self.state = "NORMAL"
                self.recovery_frames = 0
                
    return False  # Không cần cảnh báo
```

## Phương Pháp Kiểm Thử

Các chiến lược kiểm thử được triển khai trong hệ thống:

### Kiểm Thử Đơn Vị

Các thành phần riêng lẻ được kiểm thử một cách độc lập:

```python
def test_eye_aspect_ratio():
    model = SimpleSafetyModel()
    
    # Kiểm thử với điểm mốc mắt mở
    open_eye_landmarks = load_test_landmarks("open_eyes.json")
    open_ear = model._calculate_improved_ear(
        open_eye_landmarks, 
        model.LEFT_EYE_INDICES, 
        model.RIGHT_EYE_INDICES
    )
    
    # Kiểm thử với điểm mốc mắt nhắm
    closed_eye_landmarks = load_test_landmarks("closed_eyes.json")
    closed_ear = model._calculate_improved_ear(
        closed_eye_landmarks, 
        model.LEFT_EYE_INDICES, 
        model.RIGHT_EYE_INDICES
    )
    
    # Xác minh kết quả
    assert open_ear > 0.25, f"EAR mắt mở phải >0.25, nhận được {open_ear}"
    assert closed_ear < 0.2, f"EAR mắt nhắm phải <0.2, nhận được {closed_ear}"
    assert open_ear > closed_ear, "EAR mắt mở phải lớn hơn EAR mắt nhắm"
```

### Kiểm Thử Tích Hợp

Kiểm thử cách các thành phần hoạt động cùng nhau:

```python
def test_full_detection_pipeline():
    # Khởi tạo mô hình
    model = SimpleSafetyModel()
    
    # Kiểm thử với các hình ảnh mẫu khác nhau
    for test_case in ["normal.jpg", "drowsy.jpg", "distracted.jpg"]:
        # Tải hình ảnh kiểm thử
        frame = cv2.imread(f"test_data/{test_case}")
        
        # Xử lý khung hình
        results = model.process_frame(frame)
        
        # Kiểm tra kết quả dựa trên trường hợp kiểm thử
        if "normal" in test_case:
            assert not results["drowsy"] and not results["distracted"]
        elif "drowsy" in test_case:
            assert results["drowsy"] and not results["distracted"]
        elif "distracted" in test_case:
            assert not results["drowsy"] and results["distracted"]
```

### Kiểm Thử Hiệu Suất

Đảm bảo hệ thống có thể hoạt động trong thời gian thực:

```python
def test_processing_speed():
    model = SimpleSafetyModel()
    
    # Tải khung hình kiểm thử
    frame = cv2.imread("test_data/benchmark.jpg")
    
    # Khởi động
    model.process_frame(frame)
    
    # Đánh giá hiệu năng
    iterations = 100
    start_time = time.time()
    
    for _ in range(iterations):
        model.process_frame(frame)
        
    total_time = time.time() - start_time
    avg_time = total_time / iterations
    
    # Khẳng định xử lý đủ nhanh để hoạt động thời gian thực
    assert avg_time < 0.05, f"Thời gian xử lý trung bình quá chậm: {avg_time:.4f}s"
```

## Hướng Phát Triển Trong Tương Lai

Các cải tiến tiềm năng cho hệ thống:

1. **Cải Tiến Deep Learning**:
   - Thay thế SVM bằng các mô hình học sâu tinh vi hơn
   - Triển khai các cơ chế chú ý (attention mechanisms) để trích xuất đặc trưng tốt hơn
   - Sử dụng các mô hình thời gian (LSTM/GRU) để phân tích chuỗi thời gian tốt hơn

2. **Tính Năng Phát Hiện Bổ Sung**:
   - Theo dõi ánh nhìn để phát hiện sự tập trung chú ý của người lái xe
   - Phát hiện ngáp như một chỉ báo buồn ngủ bổ sung
   - Phát hiện sử dụng điện thoại để giám sát mất tập trung

3. **Cải Tiến Hệ Thống**:
   - Tối ưu hóa xử lý cạnh (edge processing) để triển khai nhúng
   - Thiết lập đa camera để phạm vi phủ sóng người lái xe tốt hơn
   - Tích hợp với dữ liệu viễn thông xe cho xe thương mại

4. **Trải Nghiệm Người Dùng**:
   - Ngưỡng cảnh báo được cá nhân hóa dựa trên lịch sử người lái
   - Cảnh báo và tương tác bằng giọng nói
   - Tích hợp bảng điều khiển cho xe thương mại

## Ngưỡng Phát Hiện Trạng Thái

Hệ thống xác định các trạng thái người lái xe dựa trên một số ngưỡng quan trọng:

### Công Thức Tính Ngưỡng Phát Hiện Trạng Thái

#### 1. Ngưỡng Phát Hiện Buồn Ngủ

Trạng thái buồn ngủ được xác định khi:

```
is_drowsy = (avg_ear < EAR_THRESHOLD) && (drowsy_frame_counter ≥ DROWSY_CONSEC_FRAMES)
```

Trong đó:
- `avg_ear` là giá trị EAR trung bình của hai mắt
- `EAR_THRESHOLD` là ngưỡng EAR (mặc định: 0.2)
- `drowsy_frame_counter` là số khung hình liên tiếp có giá trị EAR dưới ngưỡng
- `DROWSY_CONSEC_FRAMES` là số khung hình tối thiểu để xác nhận trạng thái buồn ngủ (mặc định: 20)

#### 2. Ngưỡng Phát Hiện Mất Tập Trung Do Vị Trí Đầu

Mất tập trung do vị trí đầu được xác định khi:

```
is_head_distracted = (is_tilted || is_looking_sideways) && (distracted_frame_counter ≥ DISTRACTED_CONSEC_FRAMES)
```

Trong đó:
- `is_tilted` là cờ đánh dấu đầu nghiêng (|angle_deg| > 20°)
- `is_looking_sideways` là cờ đánh dấu đầu quay ngang (|nose_deviation| > 0.15)
- `distracted_frame_counter` là số khung hình liên tiếp phát hiện đầu nghiêng/quay
- `DISTRACTED_CONSEC_FRAMES` là số khung hình tối thiểu để xác nhận mất tập trung (mặc định: 25)

#### 3. Ngưỡng Phát Hiện Mất Tập Trung Do Sử Dụng Điện Thoại

Mất tập trung do sử dụng điện thoại được xác định khi:

```
is_phone_distracted = is_holding_phone && (distracted_head_hands_counter ≥ DISTRACTED_HEAD_HANDS_CONSEC_FRAMES)
```

Trong đó:
- `is_holding_phone` là cờ đánh dấu phát hiện tay cầm điện thoại
- `distracted_head_hands_counter` là số khung hình liên tiếp phát hiện cầm điện thoại
- `DISTRACTED_HEAD_HANDS_CONSEC_FRAMES` là số khung hình tối thiểu để xác nhận mất tập trung do điện thoại (mặc định: 20)

#### 4. Ngưỡng Phát Hiện Đầu Ra Khỏi Khung Hình

```
head_out_of_frame = (head_out_of_frame_counter ≥ HEAD_OUT_OF_FRAME_CONSEC_FRAMES)
```

Trong đó:
- `head_out_of_frame_counter` là số khung hình liên tiếp không phát hiện được khuôn mặt
- `HEAD_OUT_OF_FRAME_CONSEC_FRAMES` là số khung hình tối thiểu để xác nhận đầu ra khỏi khung hình (mặc định: 10)

#### 5. Công Thức Điều Chỉnh Ngưỡng Động

Hệ thống còn bao gồm cơ chế điều chỉnh ngưỡng động dựa trên điều kiện ánh sáng và các yếu tố môi trường:

```
adjusted_ear_threshold = base_ear_threshold × (1 + light_compensation_factor)
```

Trong đó:
- `base_ear_threshold` là ngưỡng EAR cơ bản (mặc định: 0.2)
- `light_compensation_factor` là hệ số điều chỉnh dựa trên điều kiện ánh sáng (phạm vi: -0.1 đến +0.1)
