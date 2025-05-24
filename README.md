# Driver Drowsiness and Distraction Detection System

## Project Description
This project implements a real-time driver monitoring system to detect drowsiness and distraction states. The system uses computer vision and machine learning techniques to analyze the driver's face, eye state, head position, and hand position. When unsafe behavior is detected, the system issues audio and visual alerts to remind the driver, helping to prevent accidents caused by fatigue or lack of focus.

Key features:
- Real-time driver drowsiness detection through eye state monitoring
- Distraction detection by tracking head and hand positions
- Customizable alert system with continuous alerts until safe driving is resumed
- User-friendly interface for monitoring and configuration
- Data collection tools for training personalized models
- Violation history tracking for safety analysis

## Documentation
- [Code Explanation](docs/code_explanation.md) - Detailed explanation of algorithms, functions, and formulas
- [User Guide](docs/user_guide.md) - Instructions for using the application
- [Developer Guide](docs/developer_guide.md) - Information for developers extending the system

Các tính năng chính:
- Phát hiện buồn ngủ của tài xế thời gian thực thông qua giám sát trạng thái mắt
- Phát hiện mất tập trung bằng cách theo dõi vị trí đầu và tay
- Hệ thống cảnh báo có thể tùy chỉnh với các cảnh báo liên tục cho đến khi tài xế lái xe an toàn trở lại
- Giao diện thân thiện với người dùng để giám sát và cấu hình
- Công cụ thu thập dữ liệu để huấn luyện mô hình cá nhân hóa
- Theo dõi lịch sử vi phạm để phân tích an toàn

## Technologies and Libraries Used

### Computer Vision and Machine Learning
- **OpenCV**: Image processing and basic face detection
- **MediaPipe**: Face landmark detection (468 points) and hand tracking (21 points per hand)
- **scikit-learn**: SVM classification model
- **NumPy**: High-performance numerical computations

### User Interface and Sound
- **PyQt5**: Graphical user interface framework
- **PyAudio**: Audio alert playback

## Cấu Trúc Mã Nguồn

```
drowsiness_detection/
│
├── assets/             # Static resources for the application
│   └── sounds/         # Alert sound files
│
├── config/             # Configuration files
│
├── data/               # Training data and data collection
│   ├── collect_data.py # Tool for collecting training data
│   ├── distracted/     # Data for distracted driver state
│   ├── eye_state/      # Data for various eye states
│   └── focused/        # Data for focused driver state
│
├── models/             # Model definitions
│   ├── simple_model.py # Lightweight SVM model using scikit-learn
│   └── saved_model.pkl # Trained model weights
│
├── training/           # Model training scripts
│   └── simple_train.py # Script to train scikit-learn model
│
├── ui/                 # User interfaces
│   └── monitoring_app.py # Driver monitoring UI
│
├── utils/              # Utility functions
│   └── helpers.py      # Helper functions for camera, frame annotation, etc.
│
├── main.py             # Main entry point for the application
└── retrain_model.py    # Script to retrain the model with new data
```

## Core Features

### 1. Detection Model (`models/simple_model.py`)

Uses an SVM (Support Vector Machine) model combined with these features:
- **Eye Aspect Ratio (EAR)**: Calculates the openness of eyes to detect drowsiness
- **Head position analysis**: Detects if the head is turned or tilted
- **Hand position detection**: Determines if hands are placed on the steering wheel

Detection pipeline:
1. Face detection in the video frame
2. Detection of 468 facial landmarks using MediaPipe
3. EAR calculation based on eye landmarks
4. Head position analysis based on facial landmarks
5. Hand position detection using MediaPipe Hands
6. Combination of all information to determine driver's state

### 2. Monitoring Interface (`ui/monitoring_app.py`)

User interface built with PyQt5 featuring:
- Real-time video stream display
- Driver status notifications (OK/Drowsy/Distracted)
- Display of metrics: EAR, head position, hand position
- Sensitivity settings (EAR threshold, confidence threshold)
- Sound alerts when dangerous states are detected
- Save and load user configurations

### 3. Data Collection (`data/collect_data.py`)

Training data collection tool that includes:
- Driver face image capture via webcam
- Automatic classification of eye state, head, and hand positions
- Saving of images and metadata (JSON) for training

### 4. Model Training (`training/simple_train.py`)

SVM model training pipeline:
1. Load and preprocess data from the data/ directory
2. Extract HOG and color features
3. Normalize features
4. Train SVM model
5. Evaluate performance with test set
6. Save trained model

## Usage Instructions

### Running the Monitoring Application

```bash
python main.py --mode ui
```

### Collecting Training Data

```bash
python main.py --mode collect_data --data_class focused --samples 200
python main.py --mode collect_data --data_class distracted --samples 200
```

### Training the Model

```bash
python main.py --mode train
```

or

```bash
python retrain_model.py
```

## Key Detection Features

### 1. Drowsiness Detection
- Calculates Eye Aspect Ratio (EAR) from eye landmarks
- Compares against threshold (default 0.2)
- Detects prolonged eye closure

### 2. Distraction Detection
- Analyzes head position (turned to side, tilted)
- Determines hand position (not on steering wheel)
- Combines factors to assess distraction level

## System Configuration
Parameters that can be adjusted in the UI:

- **EAR Threshold**: Adjust sensitivity of drowsiness detection
- **Confidence Threshold**: Adjust confidence of detections
- **Camera Source**: Select which camera to use
- **Sound Alerts**: Enable/disable and customize
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

## Mô Tả Tệp Chi Tiết và Kiến Trúc Mã Nguồn

## Phân Tích Kiến Trúc Mã Nguồn và Mối Quan Hệ Giữa Các Module

### Tổng Quan Kiến Trúc Hệ Thống
Hệ thống phát hiện buồn ngủ và mất tập trung sử dụng kiến trúc module hóa cao, với các thành phần tách biệt nhưng liên kết chặt chẽ. Mỗi module có trách nhiệm cụ thể và giao tiếp thông qua API rõ ràng. Dưới đây là phân tích chi tiết về kiến trúc và luồng thực thi của hệ thống:

#### Sơ Đồ Luồng Dữ Liệu
```
[Camera Input] → [Frame Processing] → [Face Detection] → [Landmark Analysis] → [Feature Extraction] → [Classification] → [Alerting]
```

### Module Chính và Mối Quan Hệ

#### 1. Module Giao Diện (`ui/`)
- **Vai trò**: Hiển thị giao diện người dùng, điều khiển camera, hiển thị phản hồi và cấu hình hệ thống.
- **Quan hệ**:
  - Gọi module Mô Hình (`models/`) để xử lý và phân tích các khung hình
  - Sử dụng các tiện ích từ module Helpers (`utils/`) để khởi tạo camera và chú thích khung hình
  - Lưu và tải cấu hình từ module Cấu Hình (`config/`)

#### 2. Module Mô Hình (`models/`)
- **Vai trò**: Phân tích các khung hình, phát hiện đặc trưng và phân loại trạng thái tài xế.
- **Quan hệ**:
  - Gửi kết quả phân tích đến module Giao Diện để hiển thị
  - Sử dụng trọng số được tạo bởi module Huấn Luyện (`training/`)
  - Sử dụng các hàm tiện ích từ `utils/helpers.py`

#### 3. Module Tiện Ích (`utils/`)
- **Vai trò**: Cung cấp các hàm tiện ích chung cho toàn bộ hệ thống.
- **Quan hệ**:
  - Được sử dụng bởi hầu hết các module khác
  - Quản lý các nhiệm vụ như khởi tạo camera, chú thích khung hình, tính toán FPS, quản lý cấu hình

#### 4. Module Huấn Luyện (`training/`)
- **Vai trò**: Huấn luyện và đánh giá các mô hình phân loại.
- **Quan hệ**:
  - Tiêu thụ dữ liệu từ module Thu Thập Dữ Liệu (`data/`)
  - Tạo ra các mô hình được lưu trong `models/`
  - Sử dụng các hàm từ `utils/helpers.py` cho tiền xử lý và trực quan hóa

#### 5. Module Thu Thập Dữ Liệu (`data/`)
- **Vai trò**: Thu thập, gán nhãn và lưu trữ dữ liệu huấn luyện.
- **Quan hệ**:
  - Cung cấp dữ liệu cho module Huấn Luyện
  - Sử dụng các công cụ từ `utils/` để xử lý khung hình và trích xuất đặc trưng

### Luồng Điều Khiển và Thực Thi Chi Tiết

#### 1. Khởi Động Hệ Thống (`main.py`)
```python
# Chuỗi thực thi chính
main.py
 ├── Nhập DriverMonitoringUI từ ui/monitoring_app.py
 ├── Khởi tạo ứng dụng QApplication
 ├── Tạo và hiển thị giao diện người dùng
 └── Chạy vòng lặp sự kiện Qt
```

#### 2. Khởi tạo Giao Diện Người Dùng (`ui/monitoring_app.py`)
```python
# Quá trình khởi tạo UI
DriverMonitoringUI.__init__()
 ├── Tải cấu hình từ load_config() trong utils/helpers.py
 ├── Khởi tạo mô hình từ SimpleSafetyModel trong models/simple_model.py
 ├── Thiết lập giao diện với các thành phần PyQt5
 └── Kết nối các tín hiệu và khe cắm (signals/slots) cho tính tương tác
```

#### 3. Bắt Đầu Camera và Xử Lý Khung Hình
```python
# Luồng xử lý khung hình
DriverMonitoringUI.start_camera() 
 ├── Khởi tạo camera qua initialize_camera() từ utils/helpers.py
 ├── Thiết lập QTimer để định kỳ gọi update_frame()
 └── Bắt đầu QTimer

DriverMonitoringUI.update_frame()
 ├── Đọc khung hình từ camera
 ├── Gửi khung hình đến mô hình để xử lý: model.process_frame(frame)
 ├── Chú thích khung hình dựa trên kết quả: annotate_frame() từ utils/helpers.py
 ├── Cập nhật các chỉ số hiển thị: update_status_indicators()
 ├── Kiểm tra và kích hoạt cảnh báo nếu cần: check_and_trigger_alerts()
 └── Hiển thị khung hình đã chú thích
```

#### 4. Xử Lý và Phân Tích Khung Hình (`models/simple_model.py` hoặc `models/detection_model.py`)
```python
# Luồng phân tích khung hình
SimpleSafetyModel.process_frame(frame)
 ├── Chuyển đổi frame sang định dạng RGB
 ├── Phát hiện khuôn mặt
 ├── Phát hiện và phân tích điểm mốc khuôn mặt sử dụng MediaPipe Face Mesh
 │   ├── Tính toán EAR (Eye Aspect Ratio) thông qua _calculate_improved_ear()
 │   └── Xác định vị trí đầu thông qua _detect_head_position()
 ├── Phát hiện và phân tích vị trí tay sử dụng MediaPipe Hands
 │   └── Xác định vị trí tay thông qua _detect_hand_position()
 ├── Trích xuất đặc trưng để phân loại: _extract_simple_features()
 ├── Phân loại trạng thái sử dụng mô hình đã huấn luyện
 └── Trả về kết quả phân tích và phát hiện 
```

#### 5. Cảnh Báo và Thông Báo (`ui/monitoring_app.py`)
```python
# Luồng xử lý cảnh báo
DriverMonitoringUI.check_and_trigger_alerts()
 ├── Phân tích kết quả phát hiện
 ├── Nếu phát hiện trạng thái nguy hiểm (buồn ngủ hoặc mất tập trung)
 │   ├── Hiển thị cảnh báo trên giao diện
 │   ├── Nếu cảnh báo âm thanh được bật, gọi play_alert_sound() 
 │   └── Nếu cảnh báo liên tục được bật, đặt hẹn giờ cho cảnh báo tiếp theo
 └── Ghi nhận sự kiện vào lịch sử vi phạm thông qua save_violation_record()
```

### Module và Chức Năng Chi Tiết

#### DriverMonitoringUI (ui/monitoring_app.py)
```
Lớp quản lý giao diện người dùng:
├── start_camera(): Khởi động luồng camera
├── stop_camera(): Dừng luồng camera
├── update_frame(): Cập nhật và hiển thị khung hình từ camera
├── update_status_indicators(): Hiển thị trạng thái tài xế
├── check_and_trigger_alerts(): Kiểm tra và kích hoạt cảnh báo
├── play_alert_sound(): Phát âm thanh cảnh báo
├── save_settings(): Lưu cấu hình người dùng
├── load_settings(): Tải cấu hình người dùng
├── update_violation_history(): Cập nhật lịch sử vi phạm
└── export_report(): Xuất báo cáo vi phạm
```

#### SimpleSafetyModel (models/simple_model.py)
```
Mô hình phân loại nhẹ sử dụng scikit-learn:
├── __init__(): Khởi tạo mô hình và các thành phần MediaPipe
├── load_model(): Tải mô hình đã huấn luyện từ tệp
├── process_frame(): Xử lý khung hình để phân loại trạng thái
├── _calculate_improved_ear(): Tính toán tỷ lệ khía cạnh mắt cải tiến
├── _detect_head_position(): Phân tích vị trí đầu từ điểm mốc
├── _detect_drowsiness(): Phát hiện buồn ngủ dựa trên EAR
├── _detect_hand_position(): Phát hiện vị trí tay
├── _extract_simple_features(): Trích xuất đặc trưng cho phân loại
└── _normalize_landmarks(): Chuẩn hóa các điểm mốc khuôn mặt
```

#### SafetyMonitoringModel (models/detection_model.py)
```
Mô hình phát hiện mạnh mẽ sử dụng TensorFlow:
├── __init__(): Khởi tạo mô hình CNN và các thành phần MediaPipe
├── _create_model(): Tạo kiến trúc mạng CNN
├── load_model(): Tải trọng số đã huấn luyện
├── save_model(): Lưu trọng số mô hình
├── process_frame(): Xử lý và phân tích khung hình
├── train(): Huấn luyện mô hình trên dữ liệu được cung cấp
├── _calculate_eye_aspect_ratio(): Tính EAR từ điểm mốc
├── _detect_head_position(): Phát hiện vị trí và hướng đầu
├── _detect_hand_position(): Phát hiện và phân loại vị trí tay
└── _extract_features(): Trích xuất các đặc trưng từ khung hình
```

#### SimpleModelTrainer (training/simple_train.py)
```
Huấn luyện mô hình đơn giản sử dụng scikit-learn:
├── __init__(): Khởi tạo lớp huấn luyện
├── load_and_preprocess_data(): Tải và tiền xử lý hình ảnh đầu vào
├── extract_features(): Trích xuất đặc trưng HOG và màu sắc từ hình ảnh
├── train(): Huấn luyện SVM trên đặc trưng đã trích xuất
├── evaluate(): Đánh giá mô hình trên tập kiểm thử
├── save_model(): Lưu mô hình và bộ chuẩn hóa
└── plot_confusion_matrix(): Vẽ ma trận nhầm lẫn để trực quan hóa hiệu suất
```

#### ModelTrainer (training/train_model.py)
```
Huấn luyện mô hình CNN sử dụng TensorFlow/Keras:
├── __init__(): Khởi tạo lớp huấn luyện với các tham số
├── load_dataset(): Tải hình ảnh từ thư mục dữ liệu
├── preprocess_data(): Tiền xử lý hình ảnh cho huấn luyện
├── create_data_augmentation(): Tạo chuỗi tăng cường dữ liệu
├── build_model(): Xây dựng kiến trúc CNN
├── train(): Huấn luyện mô hình CNN trên dữ liệu
├── save_model(): Lưu mô hình đã huấn luyện
├── evaluate(): Đánh giá mô hình
└── plot_training_history(): Vẽ đồ thị quá trình huấn luyện
```

#### Helpers (utils/helpers.py)
```
Các hàm tiện ích được sử dụng trong toàn dự án:
├── initialize_camera(): Khởi tạo và cấu hình thiết bị camera
├── annotate_frame(): Thêm chú thích lên khung hình dựa trên kết quả phát hiện
├── calculate_fps(): Tính toán và hiển thị FPS
├── save_config(): Lưu cấu hình người dùng vào file JSON
├── load_config(): Tải cấu hình người dùng từ file JSON
├── crop_eye_region(): Cắt vùng mắt từ hình ảnh khuôn mặt
├── normalize_landmarks(): Chuẩn hóa điểm mốc để xử lý nhất quán
├── save_violation_record(): Lưu và quản lý lịch sử vi phạm
├── create_dir_if_not_exists(): Tạo thư mục nếu chưa tồn tại
└── log_error(): Ghi nhật ký lỗi để gỡ lỗi
```

### Ưu Điểm của Kiến Trúc

1. **Mô-đun hóa cao**: Mỗi thành phần có trách nhiệm riêng biệt, cho phép phát triển và thử nghiệm độc lập.

2. **Khả năng mở rộng**: Kiến trúc cho phép dễ dàng thêm các tính năng mới, ví dụ như:
   - Thêm mô hình phát hiện mới (chỉ cần triển khai phương thức process_frame())
   - Tích hợp các nguồn camera bổ sung
   - Thêm các loại cảnh báo mới

3. **Tính linh hoạt**: Cung cấp các tùy chọn mô hình nhẹ (simple_model.py) hoặc mô hình đầy đủ (detection_model.py) tùy thuộc vào nhu cầu hiệu suất.

4. **Khả năng bảo trì**: Các module được tách riêng với giao diện rõ ràng, dễ dàng cho việc gỡ lỗi và bảo trì.

5. **Hiệu quả về tài nguyên**: Tối ưu hóa việc sử dụng bộ nhớ và CPU bằng cách cho phép tùy chỉnh độ phức tạp của mô hình.

### Tóm Tắt Luồng Dữ Liệu

1. Camera thu nhập khung hình (`initialize_camera()` → `cap.read()`)
2. Khung hình được gửi đến mô hình để phân tích (`model.process_frame()`)

## Cơ Chế Tích Hợp Và Phương Pháp Phát Hiện Chi Tiết

### Điểm Tích Hợp Giữa Các Module

#### Tích Hợp UI và Mô Hình
Giao diện người dùng (`ui/monitoring_app.py`) và mô hình phát hiện (`models/simple_model.py` hoặc `models/detection_model.py`) tích hợp thông qua một giao diện đơn giản nhưng mạnh mẽ:

```python
# Trong ui/monitoring_app.py
class DriverMonitoringUI:
    def __init__(self):
        # ...
        self.model = SimpleSafetyModel(
            eye_aspect_ratio_threshold=self.config['ear_threshold'],
            confidence_threshold=self.config['confidence_threshold'],
            model_path=self.config['model_path']
        )
    
    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret or frame is None:
            return
        
        # Interface with the model
        results = self.model.process_frame(frame)
        
        # Use results for UI updates and alerts
        # ...
```

Mô hình cung cấp một cấu trúc kết quả tiêu chuẩn để UI có thể hiển thị và đưa ra cảnh báo phù hợp:

```python
# Cấu trúc kết quả tiêu chuẩn
results = {
    'drowsy': bool,            # Trạng thái buồn ngủ
    'distracted': bool,        # Trạng thái mất tập trung
    'ear': float,              # Giá trị EAR hiện tại
    'ear_threshold': float,    # Ngưỡng đã cấu hình
    'head_position': str,      # Vị trí đầu (straight, tilted, turned_sideways)
    'hand_position': str,      # Vị trí tay (on_wheel, not_on_wheel)
    'confidence': float,       # Độ tin cậy của phát hiện
    'face_detected': bool      # Cho biết nếu phát hiện được khuôn mặt
}
```

#### Tích Hợp Huấn Luyện và Mô Hình
Module huấn luyện (`training/`) và module mô hình (`models/`) tích hợp thông qua việc lưu trữ và tải mô hình:

```python
# Trong training/simple_train.py
def save_model(self, model_path):
    """Lưu mô hình và bộ chuẩn hóa vào tệp pickle"""
    model_data = {
        'model': self.model,
        'scaler': self.scaler,
        'ear_threshold': self.ear_threshold
    }
    with open(model_path, 'wb') as f:
        pickle.dump(model_data, f)

# Trong models/simple_model.py
def load_model(self, model_path):
    """Tải mô hình đã huấn luyện từ tệp pickle"""
    with open(model_path, 'rb') as f:
        model_data = pickle.load(f)
        
    self.model = model_data['model']
    self.scaler = model_data['scaler']
    # Có thể cập nhật ngưỡng từ mô hình đã huấn luyện nếu cần
    if 'ear_threshold' in model_data:
        self.eye_aspect_ratio_threshold = model_data['ear_threshold']
```

#### Tích Hợp Thu Thập Dữ Liệu và Huấn Luyện
Module thu thập dữ liệu (`data/collect_data.py`) tạo ra dữ liệu được gắn nhãn mà module huấn luyện (`training/`) sử dụng:

```python
# Cấu trúc dữ liệu thu thập - data/distracted/*.json
{
    "filename": "distracted_20250429_191554_631693_0.jpg",
    "class": "distracted",
    "eye_aspect_ratio": 0.285,
    "eye_state": "open",
    "head_position": "turned_sideways",
    "hand_position": "not_on_wheel",
    "timestamp": "2025-04-29 19:15:54"
}

# Trong training/train_model.py hoặc training/simple_train.py
def load_and_preprocess_data(self, img_size=(100, 100), test_split=0.2):
    for class_name in ['focused', 'distracted']:
        class_path = os.path.join(self.data_dir, class_name)
        for img_file in os.listdir(class_path):
            if img_file.endswith('.jpg') or img_file.endswith('.png'):
                # Tải hình ảnh và json metadata tương ứng
                # ...
```

### Phương Pháp Phát Hiện Chi Tiết

#### 1. Phát Hiện Buồn Ngủ

Hệ thống sử dụng một phương pháp kết hợp để phát hiện trạng thái buồn ngủ của tài xế:

1. **Tính toán Eye Aspect Ratio (EAR)**:
   - Được mô tả bởi công thức: EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
   - Giá trị EAR thấp chỉ ra rằng mắt có thể đang nhắm

2. **Theo dõi theo thời gian**:
   - Theo dõi EAR qua nhiều khung hình liên tiếp
   - Phát hiện các mẫu như chớp mắt chậm hoặc mắt nhắm kéo dài

3. **Ngưỡng động**:
   - Điều chỉnh ngưỡng EAR dựa trên điều kiện ánh sáng và người dùng cụ thể
   - Sử dụng các kỹ thuật chuẩn hóa để xử lý các biến thể giữa các cá nhân

Mã nguồn phát hiện buồn ngủ cốt lõi:

```python
def _detect_drowsiness(self, ear_value, consecutive_frames=3):
    """
    Phát hiện buồn ngủ dựa trên EAR và số khung hình liên tiếp
    """
    # Thêm giá trị EAR hiện tại vào bộ đệm
    self.ear_buffer.append(ear_value)
    if len(self.ear_buffer) > self.buffer_size:
        self.ear_buffer.pop(0)
    
    # Tính giá trị EAR trung bình trong cửa sổ thời gian
    avg_ear = sum(self.ear_buffer) / len(self.ear_buffer)
    
    # Tính số khung hình liên tiếp dưới ngưỡng
    below_threshold = 0
    for i in range(1, min(consecutive_frames + 1, len(self.ear_buffer) + 1)):
        if self.ear_buffer[-i] < self.eye_aspect_ratio_threshold:
            below_threshold += 1
    
    # Phát hiện trạng thái buồn ngủ
    is_drowsy = below_threshold >= consecutive_frames
    
    return {
        'drowsy': is_drowsy,
        'ear': ear_value,
        'avg_ear': avg_ear,
        'ear_threshold': self.eye_aspect_ratio_threshold
    }
```

#### 2. Phát Hiện Mất Tập Trung

Phát hiện mất tập trung dựa trên một kết hợp của các dấu hiệu:

1. **Phân tích vị trí đầu**:
   - Theo dõi hướng của đầu để xác định khi tài xế không tập trung vào đường
   - Tính toán độ lệch của điểm mốc mũi so với vị trí tham chiếu

2. **Theo dõi vị trí tay**:
   - Xác định xem tay của tài xế có đặt trên vô lăng không
   - Phát hiện các hoạt động như sử dụng điện thoại hoặc ăn uống

3. **Kết hợp đa yếu tố**:
   - Kết hợp các phát hiện từ đầu và tay để xác định mức độ mất tập trung
   - Áp dụng bộ lọc thời gian để loại bỏ các phát hiện giả tạm thời

```python
def _detect_distraction(self, head_position, hand_position):
    """
    Phát hiện mất tập trung dựa trên vị trí đầu và tay
    """
    # Thêm kết quả hiện tại vào bộ đệm
    self.head_position_buffer.append(head_position)
    self.hand_position_buffer.append(hand_position)
    
    # Duy trì kích thước bộ đệm
    if len(self.head_position_buffer) > self.buffer_size:
        self.head_position_buffer.pop(0)
    if len(self.hand_position_buffer) > self.buffer_size:
        self.hand_position_buffer.pop(0)
    
    # Đếm số lần vị trí đầu không thẳng
    head_not_straight = self.head_position_buffer.count("turned_sideways") + \
                        self.head_position_buffer.count("tilted")
    
    # Đếm số lần tay không trên vô lăng
    hands_not_on_wheel = self.hand_position_buffer.count("not_on_wheel")
    
    # Xác định mất tập trung dựa trên tỷ lệ trong bộ đệm
    head_distracted = head_not_straight / len(self.head_position_buffer) > 0.7
    hands_distracted = hands_not_on_wheel / len(self.hand_position_buffer) > 0.7
    
    # Tài xế được coi là mất tập trung nếu đầu hoặc tay có dấu hiệu mất tập trung
    is_distracted = head_distracted or hands_distracted
    
    return {
        'distracted': is_distracted,
        'head_distracted': head_distracted,
        'hands_distracted': hands_distracted,
        'head_position': head_position,
        'hand_position': hand_position
    }
```

#### 3. Phân Loại Sử Dụng Học Máy

Ngoài các phương pháp dựa trên ngưỡng, hệ thống còn sử dụng các kỹ thuật học máy để phát hiện trạng thái tài xế:

1. **Trích xuất đặc trưng**:
   ```python
   def _extract_simple_features(self, face_landmarks, hands_landmarks, ear_value, 
                              head_position, hand_position, frame_shape):
       """
       Trích xuất đặc trưng cho phân loại
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
       
       # Đặc trưng vị trí tay - binary
       hand_pos_feature = 1 if hand_position == "on_wheel" else 0
       features.append(hand_pos_feature)
       
       # Thêm đặc trưng hình học từ điểm mốc nếu có
       if face_landmarks:
           # Tính góc nghiêng đầu
           # ...
           
       # Trả về vector đặc trưng
       return np.array(features)
   ```

2. **Phân loại sử dụng SVM** (trong `simple_model.py`):
   ```python
   # Chuẩn hóa đặc trưng
   features_normalized = self.scaler.transform([features])
   
   # Dự đoán trạng thái tài xế
   prediction = self.model.predict(features_normalized)[0]
   probability = self.model.predict_proba(features_normalized)[0]
   
   # Áp dụng ngưỡng độ tin cậy
   is_distracted = prediction == 1 and probability[1] > self.confidence_threshold
   ```

3. **Phân loại sử dụng CNN** (trong `detection_model.py`):
   ```python
   # Trích xuất vùng mắt và điều chỉnh kích thước
   left_eye = self._extract_eye_region(frame, landmarks, self.LEFT_EYE_INDICES)
   right_eye = self._extract_eye_region(frame, landmarks, self.RIGHT_EYE_INDICES)
   
   # Tiền xử lý hình ảnh
   left_eye = cv2.resize(left_eye, (24, 24)) / 255.0
   right_eye = cv2.resize(right_eye, (24, 24)) / 255.0
   
   # Tạo đầu vào cho mô hình
   eye_input = np.concatenate([left_eye, right_eye], axis=-1)
   eye_input = np.expand_dims(eye_input, axis=0)
   
   # Dự đoán sử dụng mô hình CNN
   predictions = self.model.predict(eye_input)
   ```

### Cơ Chế Giảm Thiểu Báo Động Giả

Hệ thống tích hợp nhiều cơ chế để giảm thiểu báo động giả và tăng độ tin cậy của phát hiện:

1. **Bộ lọc trung bình động**:
   - Duy trì một cửa sổ trượt các giá trị phát hiện
   - Chỉ báo động khi nhiều khung hình liên tiếp cho thấy trạng thái nguy hiểm

2. **Ngưỡng độ tin cậy có thể điều chỉnh**:
   - Cho phép người dùng tinh chỉnh độ nhạy hệ thống
   - Ngăn các báo động do nhiễu tạm thời

3. **Xác thực chéo đa nguồn**:
   - Kết hợp nhiều dấu hiệu (EAR, vị trí đầu, vị trí tay) trước khi đưa ra cảnh báo
   - Giảm thiểu phụ thuộc vào một chỉ số duy nhất

4. **Phát hiện điều kiện ánh sáng**:
   - Điều chỉnh các thuật toán phát hiện dựa trên điều kiện ánh sáng môi trường
   - Tự động điều chỉnh độ sáng và độ tương phản của hình ảnh đầu vào

```python
def _validate_detection(self, drowsy, distracted, consecutive_frames=5):
    """
    Xác thực phát hiện thông qua nhiều khung hình để giảm báo động giả
    """
    # Thêm kết quả hiện tại vào bộ đệm
    self.drowsy_buffer.append(drowsy)
    self.distracted_buffer.append(distracted)
    
    # Duy trì kích thước bộ đệm
    if len(self.drowsy_buffer) > self.buffer_size:
        self.drowsy_buffer.pop(0)
    if len(self.distracted_buffer) > self.buffer_size:
        self.distracted_buffer.pop(0)
    
    # Tính số lượng khung hình dương tính liên tiếp
    drowsy_count = 0
    distracted_count = 0
    
    for i in range(1, min(consecutive_frames + 1, len(self.drowsy_buffer) + 1)):
        if self.drowsy_buffer[-i]:
            drowsy_count += 1
        if self.distracted_buffer[-i]:
            distracted_count += 1
    
    # Xác nhận phát hiện chỉ khi có đủ khung hình liên tiếp
    validated_drowsy = drowsy_count >= consecutive_frames
    validated_distracted = distracted_count >= consecutive_frames
    
    return validated_drowsy, validated_distracted
```

### Tổng Hợp Và Giá Trị Trạng Thái Cốt Lõi

Vận hành tổng thể của hệ thống phát hiện có thể được tóm tắt qua các trạng thái cốt lõi mà hệ thống theo dõi và phản hồi:

1. **Tài xế tỉnh táo và tập trung**:
   - EAR cao (mắt mở đầy đủ)
   - Đầu hướng thẳng về phía trước
   - Tay đặt trên vô lăng
   - → Không cần cảnh báo

2. **Tài xế buồn ngủ**:
   - EAR thấp kéo dài (mắt nhắm hoặc nửa mở)
   - Có thể có dấu hiệu gật đầu
   - → Kích hoạt cảnh báo buồn ngủ

3. **Tài xế mất tập trung - nhìn sang một bên**:
   - EAR bình thường (mắt mở)
   - Đầu xoay sang trái hoặc phải
   - → Kích hoạt cảnh báo mất tập trung

4. **Tài xế mất tập trung - tay khỏi vô lăng**:
   - Tay không nằm trên vùng vô lăng
   - Có thể đang sử dụng điện thoại hoặc thực hiện các hoạt động khác
   - → Kích hoạt cảnh báo mất tập trung

5. **Không phát hiện tài xế**:
   - Không tìm thấy khuôn mặt hoặc không đủ điểm mốc để phân tích
   - → Hiển thị cảnh báo "Không tìm thấy tài xế"

## Phương Pháp Kiểm Thử và Định Hướng Phát Triển Kiến Trúc

### Phương Pháp Kiểm Thử Hệ Thống

Hệ thống phát hiện buồn ngủ và mất tập trung cần được kiểm thử kỹ lưỡng để đảm bảo độ tin cậy trong các tình huống thực tế. Dưới đây là các phương pháp kiểm thử được áp dụng:

#### 1. Kiểm Thử Đơn Vị

Mỗi thành phần chính trong hệ thống được kiểm thử một cách độc lập:

- **Kiểm thử hàm phát hiện**:
  ```python
  def test_eye_aspect_ratio_calculation():
      """Kiểm thử hàm tính toán EAR"""
      # Tạo các điểm mốc thử nghiệm
      test_landmarks = create_test_landmarks()
      # Tính EAR
      ear = model._calculate_eye_aspect_ratio(test_landmarks, eye_indices)
      # Kiểm tra kết quả
      assert 0.15 < ear < 0.4  # Phạm vi hợp lệ cho mắt mở
  ```

- **Kiểm thử với dữ liệu giả**:
  ```python
  def test_drowsiness_detection():
      """Kiểm thử thuật toán phát hiện buồn ngủ"""
      model = SimpleSafetyModel()
      # Tạo EAR thấp giả lập (mắt nhắm)
      result = model._detect_drowsiness(0.1, consecutive_frames=3)
      assert result['drowsy'] == True
      
      # Tạo EAR cao giả lập (mắt mở)
      result = model._detect_drowsiness(0.35, consecutive_frames=3)
      assert result['drowsy'] == False
  ```

#### 2. Kiểm Thử Tích Hợp

Các thành phần khác nhau của hệ thống được kiểm thử cùng nhau để đảm bảo chúng hoạt động đúng:

```python
def test_model_integration():
    """Kiểm thử tích hợp giữa mô hình và UI"""
    # Khởi tạo mô hình
    model = SimpleSafetyModel()
    
    # Tải một hình ảnh kiểm thử
    frame = cv2.imread("test_data/drowsy_driver.jpg")
    
    # Xử lý khung hình bằng mô hình
    results = model.process_frame(frame)
    
    # Kiểm tra kết quả
    assert isinstance(results, dict)
    assert 'drowsy' in results
    assert 'distracted' in results
```

#### 3. Kiểm Thử Hiệu Suất

Đo lường hiệu suất của hệ thống để đảm bảo nó có thể chạy trong thời gian thực:

```python
def test_performance():
    """Kiểm thử hiệu suất xử lý thời gian thực"""
    model = SimpleSafetyModel()
    frame = cv2.imread("test_data/normal_driver.jpg")
    
    # Đo thời gian xử lý
    start_time = time.time()
    for _ in range(100):  # Chạy 100 lần để có kết quả đáng tin cậy
        model.process_frame(frame)
    end_time = time.time()
    
    avg_time = (end_time - start_time) / 100
    assert avg_time < 0.05  # Xử lý phải hoàn thành trong 50ms
```

#### 4. Kiểm Thử Đa Điều Kiện

Hệ thống được kiểm thử trong nhiều điều kiện khác nhau để đảm bảo độ mạnh mẽ:

- Điều kiện ánh sáng khác nhau (sáng, tối, chói)
- Các cá nhân có đặc điểm khuôn mặt khác nhau
- Các góc camera khác nhau
- Các tư thế và trạng thái tài xế khác nhau

#### 5. Kiểm Thử Hồi Quy

Bộ kiểm thử tự động được chạy để đảm bảo các thay đổi mới không ảnh hưởng đến chức năng hiện có:

```python
def regression_test_suite():
    """Chạy bộ kiểm thử hồi quy đầy đủ"""
    test_eye_aspect_ratio_calculation()
    test_drowsiness_detection()
    test_head_position_detection()
    test_hand_position_detection()
    test_model_integration()
    # ...
```

### Định Hướng Phát Triển Kiến Trúc

Dựa trên kiến trúc hiện tại, dưới đây là một số định hướng phát triển trong tương lai để cải thiện hệ thống:

#### 1. Kiến Trúc Microservices

Chuyển đổi từ ứng dụng đơn sang kiến trúc microservices để cải thiện khả năng mở rộng:

```
                        ┌───────────────────┐
                        │   API Gateway     │
                        └───────┬───────────┘
                                │
         ┌────────────┬─────────┼───────────┬─────────────┐
         │            │         │           │             │
         ▼            ▼         ▼           ▼             ▼
┌─────────────┐ ┌─────────┐ ┌──────────┐ ┌────────┐ ┌────────────┐
│ Camera      │ │ Face    │ │ Drowsy   │ │ Alert  │ │ Analytics  │
│ Service     │ │ Detect  │ │ Detect   │ │ Service│ │ Service    │
└─────────────┘ └─────────┘ └──────────┘ └────────┘ └────────────┘
```

Mỗi dịch vụ sẽ có trách nhiệm riêng biệt và giao tiếp thông qua API:

- **Camera Service**: Xử lý đầu vào hình ảnh
- **Face Detection Service**: Xác định và phân tích khuôn mặt
- **Drowsiness Detection Service**: Phân tích trạng thái tài xế
- **Alert Service**: Quản lý và phát cảnh báo
- **Analytics Service**: Thu thập và phân tích dữ liệu về an toàn tài xế

#### 2. Kiến Trúc Dựa Trên Sự Kiện

Chuyển đổi sang mô hình giao tiếp dựa trên sự kiện để giảm sự phụ thuộc giữa các thành phần:

```python
# Hệ thống phát sự kiện
class EventBus:
    def __init__(self):
        self.subscribers = {}
    
    def subscribe(self, event_type, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
    
    def publish(self, event_type, data):
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                callback(data)

# Ví dụ sử dụng
event_bus = EventBus()

# UI đăng ký sự kiện cảnh báo
event_bus.subscribe('drowsiness_detected', ui.show_drowsiness_alert)
event_bus.subscribe('distraction_detected', ui.show_distraction_alert)

# Mô hình phát sự kiện khi phát hiện trạng thái
def process_frame(frame):
    # ... phân tích khung hình
    if is_drowsy:
        event_bus.publish('drowsiness_detected', {'ear': ear_value, 'confidence': 0.92})
    
    if is_distracted:
        event_bus.publish('distraction_detected', {'type': 'head_turned', 'confidence': 0.87})
```

#### 3. Tích Hợp Học Sâu Nâng Cao

Cải thiện khả năng phát hiện bằng cách áp dụng các mô hình học sâu tiên tiến hơn:

- **Mạng thần kinh hồi quy (RNN/LSTM)** để phát hiện các mẫu thời gian trong hành vi tài xế
- **Mạng nơ-ron tích chập 3D** để phân tích các chuỗi khung hình thay vì từng khung hình đơn lẻ
- **Mô hình đa đầu vào (Multi-Input)** kết hợp dữ liệu từ nhiều nguồn (hình ảnh, âm thanh, cảm biến phương tiện)

```python
def create_temporal_model(sequence_length=20):
    """Tạo mô hình thời gian sử dụng LSTM để phát hiện mẫu hành vi theo thời gian"""
    # Đầu vào: Chuỗi các vector đặc trưng
    input_features = Input(shape=(sequence_length, num_features))
    
    # Các lớp LSTM để phát hiện mẫu thời gian
    x = LSTM(64, return_sequences=True)(input_features)
    x = LSTM(32)(x)
    
    # Phân loại trạng thái
    outputs = Dense(2, activation='softmax')(x)
    
    model = Model(inputs=input_features, outputs=outputs)
    return model
```

#### 4. Kiến Trúc Edge-Cloud Hybrid

Phân phối xử lý giữa thiết bị cạnh (trong phương tiện) và đám mây để cân bằng giữa phản hồi thời gian thực và tính phức tạp tính toán:

- **Edge Component**:
  - Chạy mô hình nhẹ cho phát hiện thời gian thực
  - Xử lý các cảnh báo khẩn cấp
  - Hoạt động ngay cả khi mất kết nối

- **Cloud Component**:
  - Chạy mô hình phức tạp hơn cho phân tích nâng cao
  - Lưu trữ và phân tích dữ liệu lịch sử
  - Cung cấp cập nhật và điều chỉnh mô hình

```python
class HybridSafetySystem:
    def __init__(self):
        self.edge_model = SimpleSafetyModel()  # Mô hình nhẹ cho xử lý cạnh
        self.cloud_service = CloudAnalyticsService()  # Dịch vụ đám mây
        self.is_connected = True  # Trạng thái kết nối
    
    def process_frame(self, frame):
        # Luôn thực hiện phát hiện cạnh thời gian thực
        edge_results = self.edge_model.process_frame(frame)
        
        # Khởi tạo kết quả ban đầu từ edge
        results = edge_results
        
        # Nếu có kết nối, gửi dữ liệu đến đám mây để phân tích nâng cao
        if self.is_connected:
            try:
                # Gửi bất đồng bộ để không chặn phát hiện thời gian thực
                self.cloud_service.process_async(frame, callback=self.on_cloud_results)
            except ConnectionError:
                self.is_connected = False
        
        return results
    
    def on_cloud_results(self, cloud_results):
        """Callback khi nhận được kết quả từ đám mây"""
        # Cập nhật mô hình cạnh với thông tin từ đám mây
        if 'model_update' in cloud_results:
            self.edge_model.update_parameters(cloud_results['model_update'])
        
        # Cập nhật các đánh giá dài hạn (mệt mỏi, chú ý kéo dài)
        if 'long_term_assessment' in cloud_results:
            notify_driver(cloud_results['long_term_assessment'])
```

#### 5. Kiến Trúc Dựa Trên Plugin

Chuyển đổi sang kiến trúc dựa trên plugin để cho phép mở rộng dễ dàng không cần sửa đổi mã nguồn gốc:

```python
class PluginManager:
    def __init__(self):
        self.detection_plugins = []
        self.alert_plugins = []
        self.visualization_plugins = []
    
    def register_detection_plugin(self, plugin):
        self.detection_plugins.append(plugin)
    
    def register_alert_plugin(self, plugin):
        self.alert_plugins.append(plugin)
    
    def register_visualization_plugin(self, plugin):
        self.visualization_plugins.append(plugin)
    
    def process_frame(self, frame):
        results = {}
        
        # Chạy tất cả plugin phát hiện
        for plugin in self.detection_plugins:
            plugin_result = plugin.detect(frame)
            results.update(plugin_result)
        
        # Kích hoạt plugin cảnh báo dựa trên kết quả
        for plugin in self.alert_plugins:
            plugin.check_and_alert(results)
        
        # Áp dụng các plugin trực quan hóa
        for plugin in self.visualization_plugins:
            frame = plugin.annotate(frame, results)
        
        return results, frame

# Ví dụ plugin
class EyeStateDetector:
    def detect(self, frame):
        # Phát hiện trạng thái mắt
        ear = self._calculate_ear(frame)
        is_drowsy = ear < 0.2
        return {'ear': ear, 'drowsy': is_drowsy}

class SoundAlert:
    def check_and_alert(self, results):
        if results.get('drowsy', False):
            self._play_alert_sound('drowsy_alert.wav')
```

### Tổng Kết

Hệ thống phát hiện buồn ngủ và mất tập trung là một ứng dụng phức tạp kết hợp nhiều công nghệ và kỹ thuật. Kiến trúc hiện tại cung cấp một nền tảng vững chắc với sự tách biệt rõ ràng giữa các thành phần chính, cho phép phát triển và bảo trì độc lập.

Với việc áp dụng các mẫu thiết kế hiệu quả và chiến lược tích hợp thông minh, hệ thống duy trì sự cân bằng giữa hiệu suất thời gian thực và tính chính xác phát hiện. Các cơ chế giảm thiểu báo động giả và khả năng tùy chỉnh đảm bảo hệ thống có thể hoạt động hiệu quả trong nhiều điều kiện khác nhau.

Các định hướng phát triển đề xuất - bao gồm kiến trúc microservices, giao tiếp dựa trên sự kiện, học sâu nâng cao, giải pháp hybrid edge-cloud và kiến trúc dựa trên plugin - cung cấp một lộ trình rõ ràng để cải thiện hệ thống trong tương lai mà không cần thiết kế lại hoàn toàn.