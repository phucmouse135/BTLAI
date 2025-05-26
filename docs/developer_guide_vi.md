# Hệ Thống Phát Hiện Buồn Ngủ: Hướng Dẫn Cho Nhà Phát Triển

Hướng dẫn này cung cấp thông tin kỹ thuật cho các nhà phát triển muốn mở rộng, sửa đổi hoặc tích hợp với Hệ Thống Phát Hiện Buồn Ngủ.

## Mục Lục
- [Tổng Quan Kiến Trúc](#tổng-quan-kiến-trúc)
- [Cấu Trúc Mã Nguồn](#cấu-trúc-mã-nguồn)
- [Các Lớp và Phương Thức Cốt Lõi](#các-lớp-và-phương-thức-cốt-lõi)
- [Thêm Tính Năng Mới](#thêm-tính-năng-mới)
- [Huấn Luyện và Đánh Giá Mô Hình](#huấn-luyện-và-đánh-giá-mô-hình)
- [Điểm Tích Hợp](#điểm-tích-hợp)
- [Các Thực Hành Tốt Nhất](#các-thực-hành-tốt-nhất)

## Tổng Quan Kiến Trúc

Hệ thống tuân theo kiến trúc mô-đun với sự phân tách rõ ràng các mối quan tâm:

![Sơ đồ Kiến trúc](assets/images/architecture.png)

### Thành Phần Cốt Lõi

1. **Động Cơ Phát Hiện**
   - Phát hiện khuôn mặt và điểm mốc
   - Trích xuất đặc trưng
   - Phân loại trạng thái

2. **Giao Diện Người Dùng**
   - Hiển thị nguồn cấp dữ liệu camera
   - Chỉ báo trạng thái
   - Điều khiển cấu hình

3. **Quản Lý Dữ Liệu**
   - Thu thập dữ liệu
   - Huấn luyện mô hình
   - Lưu trữ cấu hình

4. **Hệ Thống Cảnh Báo**
   - Cảnh báo trực quan
   - Thông báo âm thanh
   - Ghi nhật ký cảnh báo

### Luồng Dữ Liệu

```
Camera Đầu Vào → Thu Nhận Khung Hình → Phát Hiện Khuôn Mặt → Phát Hiện Điểm Mốc → 
Trích Xuất Đặc Trưng → Phân Loại Trạng Thái → Tạo Cảnh Báo → Giao Diện Người Dùng
```

## Cấu Trúc Mã Nguồn

Mã nguồn được tổ chức thành các module logic:

### Các Module Chính

| Module | Đường Dẫn | Mô Tả |
|--------|------|-------------|
| Điểm Vào Chính | `main.py` | Điểm vào ứng dụng với phân tích đối số |
| Mô Hình Phát Hiện | `models/` | Thuật toán và mô hình phát hiện |
| Giao Diện Người Dùng | `ui/` | Thành phần giao diện người dùng dựa trên PyQt5 |
| Thu Thập Dữ Liệu | `data/` | Công cụ thu thập dữ liệu huấn luyện |
| Huấn Luyện | `training/` | Tập lệnh huấn luyện mô hình |
| Tiện Ích | `utils/` | Hàm tiện ích và tiện ích dùng chung |

### Các Tệp Chính và Vai Trò

- `main.py`: Điểm vào, phân tích dòng lệnh, chọn chế độ
- `models/simple_model.py`: Mô hình phát hiện nhẹ dựa trên SVM
- `models/detection_model.py`: Mô hình phát hiện nâng cao hơn dựa trên CNN
- `ui/monitoring_app.py`: Triển khai giao diện giám sát chính
- `training/simple_train.py`: Triển khai huấn luyện mô hình SVM
- `training/train_model.py`: Triển khai huấn luyện mô hình CNN
- `data/collect_data.py`: Công cụ thu thập dữ liệu
- `utils/helpers.py`: Các hàm tiện ích dùng chung

## Các Lớp và Phương Thức Cốt Lõi

### SimpleSafetyModel (`models/simple_model.py`)

Mô hình phát hiện cốt lõi sử dụng phân loại SVM:

```python
class SimpleSafetyModel:
    """
    Mô hình nhẹ cho phát hiện buồn ngủ và mất tập trung sử dụng SVM.
    
    Các phương thức chính:
    - process_frame(frame): Xử lý khung hình video và trả về kết quả phát hiện
    - _calculate_improved_ear(landmarks, left_eye_indices, right_eye_indices): Tính toán EAR
    - _detect_head_position(landmarks): Phát hiện hướng đầu
    - _detect_hand_position(hand_landmarks): Kiểm tra xem tay có đặt trên vô lăng không
    - _extract_simple_features(...): Trích xuất đặc trưng cho phân loại
    - load_model(model_path): Tải một mô hình đã huấn luyện
    """
```

#### Các Phương Thức Chính

```python
def process_frame(self, frame):
    """
    Xử lý khung hình video và phát hiện buồn ngủ/mất tập trung.
    
    Đối số:
        frame: Hình ảnh BGR từ camera
        
    Trả về:
        dict: Kết quả phát hiện bao gồm:
            - drowsy (bool): Liệu tài xế có vẻ buồn ngủ không
            - distracted (bool): Liệu tài xế có vẻ mất tập trung không
            - ear (float): Giá trị EAR hiện tại
            - ear_threshold (float): Ngưỡng EAR hiện tại
            - head_position (str): Vị trí đầu được phát hiện
            - hand_position (str): Vị trí tay được phát hiện
            - confidence (float): Độ tin cậy phát hiện
            - face_detected (bool): Liệu khuôn mặt có được phát hiện hay không
    """
```

### DriverMonitoringUI (`ui/monitoring_app.py`)

Lớp giao diện người dùng chính:

```python
class DriverMonitoringUI(QMainWindow):
    """
    Giao diện giám sát chính sử dụng PyQt5.
    
    Các phương thức chính:
    - start_camera(): Bắt đầu nguồn cấp dữ liệu camera
    - stop_camera(): Dừng nguồn cấp dữ liệu camera
    - update_frame(): Xử lý và hiển thị khung hình camera
    - check_and_trigger_alerts(): Kiểm tra kết quả phát hiện và phát cảnh báo
    - save_settings(): Lưu cấu hình người dùng vào tệp
    - load_settings(): Tải cấu hình người dùng từ tệp
    """
```

### SimpleModelTrainer (`training/simple_train.py`)

Lớp huấn luyện mô hình:

```python
class SimpleModelTrainer:
    """
    Huấn luyện mô hình SVM cho phát hiện buồn ngủ và mất tập trung.
    
    Các phương thức chính:
    - load_and_preprocess_data(): Tải hình ảnh huấn luyện và tiền xử lý
    - extract_features(): Trích xuất đặc trưng từ hình ảnh
    - train(): Huấn luyện SVM trên các đặc trưng đã trích xuất
    - evaluate(): Đánh giá hiệu suất mô hình
    - save_model(): Lưu mô hình đã huấn luyện vào tệp
    """
```

## Thêm Tính Năng Mới

### Thêm Phương Thức Phát Hiện Mới

Để thêm phương thức phát hiện mới (ví dụ: phát hiện ngáp):

1. **Mở rộng lớp mô hình**:

```python
def _detect_yawning(self, landmarks):
    """
    Phát hiện ngáp dựa trên các điểm mốc miệng
    
    Đối số:
        landmarks: Các điểm mốc khuôn mặt từ MediaPipe
        
    Trả về:
        bool: True nếu phát hiện ngáp
    """
    # Trích xuất các điểm mốc miệng
    mouth_landmarks = [landmarks[i] for i in self.MOUTH_INDICES]
    
    # Tính toán tỷ lệ khía cạnh miệng (tương tự như EAR)
    mar = self._calculate_mouth_aspect_ratio(mouth_landmarks)
    
    # Trả về true nếu MAR vượt quá ngưỡng
    return mar > self.YAWNING_THRESHOLD
```

2. **Cập nhật phương thức process_frame**:

```python
def process_frame(self, frame):
    # Mã nguồn hiện tại...
    
    # Thêm phát hiện mới
    is_yawning = False
    if face_landmarks is not None:
        is_yawning = self._detect_yawning(face_landmarks)
    
    # Cập nhật từ điển kết quả
    results = {
        # Các trường hiện tại...
        'yawning': is_yawning
    }
    
    return results
```

3. **Cập nhật UI để hiển thị phát hiện mới**:

```python
def update_status_indicators(self):
    # Mã nguồn hiện tại...
    
    # Thêm chỉ báo ngáp
    if self.detection_results.get('yawning', False):
        self.yawning_label.setText("Ngáp: CÓ")
        self.yawning_label.setStyleSheet("color: red;")
    else:
        self.yawning_label.setText("Ngáp: KHÔNG")
        self.yawning_label.setStyleSheet("color: green;")
```

### Tạo Mô Hình Mới

Để triển khai một mô hình phát hiện hoàn toàn mới:

1. **Tạo một tệp mới** trong thư mục `models/`:

```python
# models/advanced_model.py
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

class AdvancedSafetyModel:
    """
    Mô hình nâng cao cho phát hiện trạng thái người lái xe sử dụng học sâu
    """
    
    def __init__(self, **kwargs):
        """Khởi tạo mô hình với các tham số"""
        self.model = self._create_model()
        # ...
    
    def _create_model(self):
        """Tạo và biên dịch kiến trúc mô hình"""
        # ...
    
    def process_frame(self, frame):
        """Xử lý khung hình và trả về kết quả phát hiện"""
        # Logic phát hiện
        # ...
        
        # Trả về kết quả ở cùng định dạng với SimpleSafetyModel
        # để tương thích với UI hiện tại
        return results
```

2. **Cập nhật `main.py` để hỗ trợ mô hình mới**:

```python
def initialize_model(model_type, **kwargs):
    """Khởi tạo mô hình dựa trên loại"""
    if model_type == 'simple':
        from models.simple_model import SimpleSafetyModel
        return SimpleSafetyModel(**kwargs)
    elif model_type == 'advanced':
        from models.advanced_model import AdvancedSafetyModel
        return AdvancedSafetyModel(**kwargs)
    else:
        raise ValueError(f"Loại mô hình không xác định: {model_type}")
```

3. **Thêm hỗ trợ dòng lệnh**:

```python
parser.add_argument('--model_type', type=str, default='simple',
                    choices=['simple', 'advanced'],
                    help='Loại mô hình phát hiện để sử dụng')
```

## Huấn Luyện và Đánh Giá Mô Hình

### Huấn Luyện Mô Hình Mới

Để huấn luyện một mô hình tùy chỉnh:

1. **Thu thập dữ liệu** sử dụng công cụ thu thập dữ liệu:

```bash
python main.py --mode collect_data --data_class focused --samples 200
python main.py --mode collect_data --data_class distracted --samples 200
python main.py --mode collect_data --data_class drowsy --samples 200
```

2. **Tạo một tập lệnh huấn luyện** hoặc sử dụng các tập lệnh hiện có:

```python
from training.simple_train import SimpleModelTrainer

# Khởi tạo huấn luyện viên
trainer = SimpleModelTrainer(
    data_dir='data',
    test_size=0.2,
    random_state=42
)

# Tải và xử lý dữ liệu
X_train, X_test, y_train, y_test = trainer.load_and_preprocess_data()

# Huấn luyện mô hình
model = trainer.train(X_train, y_train)

# Đánh giá mô hình
accuracy, precision, recall, f1 = trainer.evaluate(model, X_test, y_test)
print(f"Độ chính xác: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"Điểm F1: {f1:.4f}")

# Lưu mô hình
trainer.save_model('models/my_custom_model.pkl')
```

3. **Sử dụng mô hình đã huấn luyện** trong ứng dụng:

```bash
python main.py --mode ui --model_path models/my_custom_model.pkl
```

### Đánh Giá Mô Hình

Để đánh giá đúng các mô hình của bạn:

```python
def evaluate_model(model_path, test_data_dir):
    """Đánh giá một mô hình trên dữ liệu kiểm thử"""
    # Tải mô hình
    model = SimpleSafetyModel()
    model.load_model(model_path)
    
    # Tải dữ liệu kiểm thử
    test_frames, test_labels = load_test_data(test_data_dir)
    
    # Đánh giá
    results = []
    for frame, true_label in zip(test_frames, test_labels):
        detection = model.process_frame(frame)
        predicted_label = 'drowsy' if detection['drowsy'] else 'distracted' if detection['distracted'] else 'focused'
        results.append((true_label, predicted_label))
    
    # Tính toán chỉ số
    accuracy, confusion_matrix = calculate_metrics(results)
    
    # Hiển thị kết quả
    print(f"Độ chính xác: {accuracy:.4f}")
    print("Ma trận nhầm lẫn:")
    print(confusion_matrix)
    
    # Tùy chọn: Vẽ đường cong ROC, đường cong precision-recall, v.v.
```

## Điểm Tích Hợp

### Tích Hợp với Hệ Thống Bên Ngoài

Hệ thống cung cấp một số điểm tích hợp:

1. **Chế độ API**:
   - Sử dụng `--mode api` để khởi động hệ thống như một máy chủ API
   - Nhận kết quả phát hiện thông qua các điểm cuối HTTP

2. **Event Hooks**:
   - Đăng ký hàm gọi lại cho các sự kiện phát hiện
   - Ví dụ:
   
   ```python
   def on_drowsiness_detected(detection_data):
       # Hành động tùy chỉnh khi phát hiện buồn ngủ
       external_system.send_alert(detection_data)
   
   # Đăng ký hàm gọi lại
   model.register_callback('drowsy', on_drowsiness_detected)
   ```

3. **Tệp Đầu Ra**:
   - Cấu hình hệ thống để ghi nhật ký phát hiện vào tệp
   - Các ứng dụng khác có thể theo dõi tệp này để biết các sự kiện
   
   ```json
   "logging": {
     "enabled": true,
     "file": "logs/detections.json",
     "format": "json"
   }
   ```

### Nhúng trong Ứng Dụng Khác

Để sử dụng chức năng phát hiện trong một ứng dụng khác:

```python
from models.simple_model import SimpleSafetyModel

class YourApplication:
    def __init__(self):
        # Khởi tạo mô hình phát hiện
        self.detection_model = SimpleSafetyModel(
            eye_aspect_ratio_threshold=0.2,
            confidence_threshold=0.7
        )
        self.detection_model.load_model('models/saved_model.pkl')
        
    def process_video_frame(self, frame):
        # Lấy kết quả phát hiện
        results = self.detection_model.process_frame(frame)
        
        # Sử dụng kết quả trong ứng dụng của bạn
        if results['drowsy']:
            self.handle_drowsy_driver()
        elif results['distracted']:
            self.handle_distracted_driver()
```

## Các Thực Hành Tốt Nhất

### Phong Cách Mã Nguồn

Tuân theo các hướng dẫn sau để đảm bảo tính nhất quán của mã nguồn:

- Sử dụng hướng dẫn kiểu PEP 8
- Viết tài liệu cho tất cả các hàm và lớp bằng docstrings
- Thêm gợi ý kiểu dữ liệu nơi thích hợp
- Viết unit test cho chức năng mới

### Tối Ưu Hóa Hiệu Suất

Khi làm việc với xử lý video thời gian thực:

1. **Tối Ưu Xử Lý Khung Hình**:
   - Thay đổi kích thước khung hình xuống kích thước tối thiểu khả thi
   - Xử lý mỗi khung hình thứ n nếu không cần FPS đầy đủ
   - Sử dụng đa luồng để song song hóa phát hiện và hiển thị

2. **Tối Ưu Mô Hình**:
   - Cân nhắc các mô hình lượng tử hóa để sử dụng CPU thấp hơn
   - Lập hồ sơ mã nguồn của bạn để xác định điểm nghẽn
   - Triển khai bộ nhớ đệm cho các tính toán tốn kém

3. **Quản Lý Bộ Nhớ**:
   - Giải phóng tài nguyên đúng cách khi không sử dụng
   - Theo dõi việc sử dụng bộ nhớ trong các phiên chạy dài
   - Triển khai dọn dẹp thích hợp trong các trình xử lý sự kiện

### Kiểm Thử

Luôn kiểm thử kỹ các tính năng mới:

1. **Kiểm Thử Đơn Vị**:
   - Viết các bài kiểm thử cho từng thành phần
   - Ví dụ:
   
   ```python
   def test_ear_calculation():
       model = SimpleSafetyModel()
       landmarks = create_test_landmarks()
       ear = model._calculate_improved_ear(
           landmarks, model.LEFT_EYE_INDICES, model.RIGHT_EYE_INDICES
       )
       assert 0.15 < ear < 0.4
   ```

2. **Kiểm Thử Tích Hợp**:
   - Kiểm thử cách các thành phần làm việc cùng nhau
   - Xác minh UI cập nhật chính xác dựa trên kết quả mô hình

3. **Kiểm Thử Hiệu Suất**:
   - Đo lường và xác minh FPS
   - Kiểm thử trên phần cứng mục tiêu
   - Đảm bảo hiệu suất ổn định theo thời gian
