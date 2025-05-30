## Kiến trúc tổng thể của hệ thống

```
┌───────────────────┐
│   Input Video     │
└─────────┬─────────┘
          ▼
┌───────────────────┐    ┌───────────────────┐
│  Face Detection   │───▶│  Face Landmarks   │
└─────────┬─────────┘    └─────────┬─────────┘
          │                        │
          │                        ▼
          │              ┌───────────────────┐    ┌───────────────────┐
          │              │  Eye State (EAR)  │───▶│  Drowsiness       │
          │              └───────────────────┘    │  Detection        │
          │                                       └─────────┬─────────┘
          │                                                 │
          ▼                                                 │
┌───────────────────┐    ┌───────────────────┐             │
│  Hand Detection   │───▶│  Hand Landmarks   │             │
└─────────┬─────────┘    └─────────┬─────────┘             │
          │                        │                       │
          │                        ▼                       │
          │              ┌───────────────────┐             │
          └────────────▶│  Hand Position    │             │
                        └─────────┬─────────┘             │
                                  │                       │
                                  ▼                       ▼
                        ┌───────────────────┐    ┌───────────────────┐
                        │  Distraction      │───▶│  State Classifier │
                        │  Detection        │    │  (SVM)            │
                        └───────────────────┘    └─────────┬─────────┘
                                                           │
                                                           ▼
                                                ┌───────────────────┐
                                                │  Alert System     │
                                                └───────────────────┘
                                                           │
                                                           ▼
                                                ┌───────────────────┐
                                                │  User Interface   │
                                                └───────────────────┘
```

## Luồng xử lý dữ liệu từng bước

1. **Thụ đắc hình ảnh** → Nhận khung hình từ camera
2. **Phát hiện khuôn mặt** → Xác định vùng khuôn mặt trong khung hình
3. **Phát hiện điểm mốc khuôn mặt** → 468 điểm mốc với MediaPipe Face Mesh
4. **Phát hiện tay** → Xác định vùng tay trong khung hình
5. **Phát hiện điểm mốc tay** → 21 điểm trên mỗi bàn tay với MediaPipe Hands
6. **Tính toán EAR** → Đánh giá trạng thái mắt
7. **Phân tích vị trí đầu** → Đánh giá góc nghiêng và quay đầu
8. **Phân tích vị trí tay** → Đánh giá vị trí tay trên vô lăng
9. **Làm mịn dữ liệu** → Áp dụng bộ lọc để giảm nhiễu
10. **Phân loại trạng thái** → Kết hợp các đặc trưng để xác định trạng thái người lái
11. **Đưa ra cảnh báo** → Phát cảnh báo khi phát hiện trạng thái nguy hiểm
12. **Hiển thị giao diện** → Cập nhật thông tin trạng thái người lái xe

## Thiết kế module chi tiết

### Module Phát Hiện Khuôn Mặt và Điểm Mốc

- **Input**: Khung hình từ camera (H x W x 3)
- **Xử lý**: 
  1. Phát hiện khuôn mặt với MediaPipe Face Detection
  2. Trích xuất 468 điểm mốc khuôn mặt với MediaPipe Face Mesh
- **Output**: Ma trận (468 x 3) chứa tọa độ 3D của các điểm mốc

### Module Phát Hiện Tay và Điểm Mốc

- **Input**: Khung hình từ camera (H x W x 3)
- **Xử lý**:
  1. Phát hiện tay với MediaPipe Hands
  2. Trích xuất 21 điểm mốc cho mỗi bàn tay
- **Output**: Danh sách các ma trận (21 x 3) chứa tọa độ 3D của các điểm mốc

### Module Phân Tích Trạng Thái Mắt

- **Input**: Các điểm mốc của mắt từ Face Mesh
- **Xử lý**:
  1. Tính toán EAR cho mắt trái và phải
  2. Tính EAR trung bình
  3. Áp dụng bộ lọc trung bình trượt
- **Output**: Giá trị EAR đã làm mịn và trạng thái mắt (mở/nhắm)

### Module Phân Tích Vị Trí Đầu

- **Input**: Các điểm mốc khuôn mặt từ Face Mesh
- **Xử lý**:
  1. Tính góc nghiêng dựa trên đường nối hai mắt
  2. Tính độ lệch mũi so với trung tâm khuôn mặt
  3. Áp dụng bộ lọc Kalman để làm mịn kết quả
- **Output**: Góc nghiêng, độ lệch mũi, và trạng thái vị trí đầu

### Module Phân Tích Vị Trí Tay

- **Input**: Các điểm mốc của tay từ MediaPipe Hands
- **Xử lý**:
  1. Tính khoảng cách từ cổ tay đến vùng vô lăng
  2. Phân tích hình dạng tay để phát hiện cầm đồ vật
  3. Áp dụng bộ lọc loại bỏ nhiễu và làm mịn kết quả
- **Output**: Trạng thái tay (trên vô lăng/không trên vô lăng/cầm đồ vật)

### Module Xử Lý Thời Gian Thực

- **Input**: Luồng video từ camera và kết quả từ các module phân tích
- **Xử lý**:
  1. Phân tách luồng video thành các khung hình (30 FPS)
  2. Xử lý song song với threading hoặc multiprocessing nếu cần thiết
  3. Bộ đệm hình ảnh để giảm độ trễ khi xử lý các khung hình phức tạp
  4. Tối ưu hóa hiệu suất với các kỹ thuật như resize hình ảnh trước khi xử lý
- **Output**: Luồng dữ liệu đã xử lý với tốc độ ổn định (>=25 FPS)

### Module Phân Loại Trạng Thái SVM

- **Input**: Vector đặc trưng từ các module phân tích
- **Xử lý**:
  1. Chuẩn hóa vector đặc trưng với StandardScaler
  2. Áp dụng mô hình SVM với kernel RBF để phân loại trạng thái
  3. Áp dụng kỹ thuật hysteresis để loại bỏ dao động giữa các trạng thái
  4. Theo dõi trạng thái theo thời gian để phát hiện mẫu hình dài hạn
- **Output**: Trạng thái người lái (tỉnh táo/buồn ngủ/mất tập trung) và độ tin cậy

### Module Cảnh Báo

- **Input**: Trạng thái người lái và độ tin cậy từ module phân loại
- **Xử lý**:
  1. Đánh giá mức độ nguy hiểm dựa trên trạng thái và thời gian duy trì
  2. Chọn loại cảnh báo phù hợp (trực quan/âm thanh) dựa trên mức độ nguy hiểm
  3. Kiểm soát tần suất cảnh báo để tránh gây phiền nhiễu
- **Output**: Tín hiệu cảnh báo (hình ảnh/âm thanh) và thông tin trạng thái

## Luồng dữ liệu chi tiết

```
Camera (30 FPS) → Buffer (5-10 frames) → Image Processor
                                           ↓
                   ┌─────────────────┐     │
                   │  Model Results  │ ← Face/Eye/Hand Detection
                   └─────────────────┘     │
                         ↓                 ↓
EAR Time Series → [Moving Average Filter] → Feature Vector
Head Position   →                            ↓
Hand Position   →                         [SVM Model]
                                            ↓
Alert History → [Hysteresis Filter] → [Alert Decision] → User Interface
                                            ↓
                                      [State History]
                                            ↓
                                      [Long-term Analysis]
```

## Mã nguồn xử lý luồng video trong thời gian thực

```python
def process_video_stream(camera_source=0):
    """Xử lý luồng video từ camera và phát hiện trạng thái người lái."""
    
    # Khởi tạo camera
    cap = cv2.VideoCapture(camera_source)
    
    # Khởi tạo MediaPipe
    mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    mp_hands = mp.solutions.hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )
    
    # Biến theo dõi trạng thái
    eye_closed_frames = 0
    drowsy_state = False
    distracted_state = False
    ear_values = deque(maxlen=30)  # Lưu 30 giá trị EAR gần nhất
    
    # Bộ lọc Kalman cho góc đầu
    kalman_filter = KalmanFilter1D(process_noise=0.01, measurement_noise=0.1)
    
    while True:
        success, frame = cap.read()
        if not success:
            break
            
        # Xử lý khung hình
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb.flags.writeable = False
        
        # Phát hiện khuôn mặt và điểm mốc
        face_results = mp_face_mesh.process(frame_rgb)
        
        # Phát hiện tay
        hand_results = mp_hands.process(frame_rgb)
        
        # Phân tích trạng thái mắt, đầu và tay
        if face_results.multi_face_landmarks:
            landmarks = face_results.multi_face_landmarks[0].landmark
            
            # Tính toán EAR
            left_ear = calculate_ear(landmarks, LEFT_EYE_INDICES)
            right_ear = calculate_ear(landmarks, RIGHT_EYE_INDICES)
            ear = (left_ear + right_ear) / 2.0
            ear_values.append(ear)
            
            # Áp dụng bộ lọc trung bình trượt
            smoothed_ear = sum(ear_values) / len(ear_values)
            
            # Phân tích vị trí đầu
            head_pose = analyze_head_position(landmarks)
            
            # Áp dụng bộ lọc Kalman cho góc nghiêng
            filtered_angle = kalman_filter.update(head_pose['angle'])
            
            # Phát hiện trạng thái buồn ngủ
            if smoothed_ear < EAR_THRESHOLD:
                eye_closed_frames += 1
                if eye_closed_frames > DROWSY_FRAMES:
                    drowsy_state = True
            else:
                eye_closed_frames = max(0, eye_closed_frames - 1)
                if eye_closed_frames < RECOVERY_FRAMES:
                    drowsy_state = False
            
            # Phát hiện mất tập trung do vị trí đầu
            if abs(filtered_angle) > HEAD_ANGLE_THRESHOLD or abs(head_pose['nose_deviation']) > NOSE_DEVIATION_THRESHOLD:
                distracted_state = True
            else:
                distracted_state = False
            
        # Phát hiện vị trí tay
        hand_on_wheel = False
        holding_object = False
        
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                # Phân tích vị trí tay và trạng thái cầm nắm
                hand_status = analyze_hand_position(hand_landmarks.landmark)
                
                if hand_status['on_wheel']:
                    hand_on_wheel = True
                if hand_status['holding_object']:
                    holding_object = True
        
        # Tổng hợp kết quả và hiển thị
        display_results(frame, drowsy_state, distracted_state, hand_on_wheel, holding_object)
        
        # Hiển thị khung hình
        cv2.imshow('Driver Monitoring', frame)
        
        if cv2.waitKey(5) & 0xFF == 27:  # Nhấn ESC để thoát
            break
    
    # Giải phóng tài nguyên
    cap.release()
    mp_face_mesh.close()
    mp_hands.close()
    cv2.destroyAllWindows()
```
- **Output**: Trạng thái vị trí tay (trên vô lăng, không trên vô lăng, cầm đồ vật)

### Module Phân Loại Trạng Thái

- **Input**: EAR, vị trí đầu, vị trí tay
- **Xử lý**:
  1. Tính toán vector đặc trưng
  2. Chuẩn hóa dữ liệu
  3. Sử dụng mô hình SVM để phân loại
  4. Áp dụng kỹ thuật hysteresis để tránh dao động trạng thái
- **Output**: Trạng thái người lái (tỉnh táo, buồn ngủ, mất tập trung)

### Module Cảnh Báo

- **Input**: Trạng thái người lái
- **Xử lý**:
  1. Xác định mức độ cảnh báo
  2. Chọn loại cảnh báo phù hợp
- **Output**: Tín hiệu cảnh báo (âm thanh, hình ảnh)

### Module Giao Diện Người Dùng

- **Input**: Khung hình, trạng thái người lái, thông số EAR, vị trí đầu, vị trí tay
- **Xử lý**: 
  1. Hiển thị video với các chú thích
  2. Hiển thị thông số và chỉ báo trạng thái
  3. Hiển thị cảnh báo nếu cần
- **Output**: Giao diện đồ họa với thông tin trực quan
