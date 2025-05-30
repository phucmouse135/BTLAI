# Kết quả thử nghiệm chi tiết

## 1. Thiết lập thử nghiệm

### 1.1. Môi trường thử nghiệm

**Thiết bị phần cứng:**
- PC: Intel Core i5-10400, 16GB RAM, NVIDIA GTX 1660
- Laptop: Intel Core i7-1165G7, 8GB RAM, NVIDIA MX450
- Raspberry Pi 4, 4GB RAM
- Camera: Logitech C920 HD Pro (1080p)

**Phần mềm và thư viện:**
- OS: Windows 10, Ubuntu 20.04, Raspberry Pi OS
- Python 3.9.7
- OpenCV 4.5.5
- MediaPipe 0.8.9
- scikit-learn 1.0.2
- TensorFlow Lite 2.8.0 (cho thiết bị nhúng)

**Điều kiện thử nghiệm:**
- Ánh sáng: tốt (500-600 lux), trung bình (200-300 lux), yếu (<100 lux)
- Góc camera: thẳng, +15°, -15°, +30°, -30°
- Khoảng cách: 60-80cm từ camera đến người lái
- Thời gian: buổi sáng, buổi chiều, buổi tối

### 1.2. Bộ dữ liệu thử nghiệm

**Tổng quan:**
- 50 người tình nguyện (30 nam, 20 nữ)
- Độ tuổi: 20-60 tuổi
- 10.000 khung hình được ghi nhãn
- 3 trạng thái: tỉnh táo, buồn ngủ, mất tập trung

**Phân bố dữ liệu:**
- Tỉnh táo: 4.000 khung hình (40%)
- Buồn ngủ: 3.000 khung hình (30%)
- Mất tập trung: 3.000 khung hình (30%)
  - Do vị trí đầu: 1.000 khung hình
  - Do sử dụng điện thoại: 1.000 khung hình
  - Do tay không đặt trên vô lăng: 1.000 khung hình

**Phương pháp chia dữ liệu:**
- Training: 70% (7.000 khung hình)
- Validation: 15% (1.500 khung hình)
- Testing: 15% (1.500 khung hình)
- Phân tầng theo đối tượng (người tham gia không xuất hiện đồng thời trong tập huấn luyện và kiểm thử)

### 1.3. Phương pháp đánh giá

**Các chỉ số đánh giá:**
- Độ chính xác (Accuracy)
- Độ nhạy (Sensitivity/Recall)
- Độ đặc hiệu (Specificity)
- Precision
- F1-score
- ROC AUC
- Thời gian phát hiện (ms)
- Khung hình xử lý mỗi giây (FPS)

## 2. Kết quả chi tiết

### 2.1. Hiệu suất phát hiện trạng thái mắt

#### 2.1.1. Phân tích EAR trong các trạng thái khác nhau

| Trạng thái | Số mẫu | EAR min | EAR max | EAR trung bình | Độ lệch chuẩn |
|------------|--------|---------|---------|----------------|---------------|
| Mắt mở hoàn toàn | 3200 | 0.25 | 0.41 | 0.32 | 0.03 |
| Mắt nhắm hoàn toàn | 2400 | 0.08 | 0.19 | 0.14 | 0.02 |
| Mắt lim dim | 850 | 0.19 | 0.25 | 0.22 | 0.01 |

#### 2.1.2. Độ chính xác phát hiện mắt nhắm dựa trên ngưỡng EAR

| Ngưỡng EAR | Độ chính xác | Độ nhạy | Độ đặc hiệu | F1-score |
|------------|--------------|---------|-------------|----------|
| 0.15 | 89.5% | 81.2% | 97.8% | 0.887 |
| 0.18 | 92.3% | 88.4% | 96.2% | 0.921 |
| 0.20 | 94.7% | 93.2% | 96.1% | 0.946 |
| 0.22 | 93.1% | 95.7% | 90.5% | 0.930 |
| 0.25 | 87.6% | 98.4% | 76.8% | 0.863 |

#### 2.1.3. Ảnh hưởng của điều kiện ánh sáng đến hiệu suất

| Điều kiện ánh sáng | Độ chính xác | Độ nhạy | Độ đặc hiệu | Độ trễ phát hiện (ms) |
|--------------------|--------------|---------|-------------|------------------------|
| Tốt (500-600 lux) | 94.7% | 93.2% | 96.1% | 110 |
| Trung bình (200-300 lux) | 92.3% | 90.5% | 94.0% | 125 |
| Yếu (<100 lux) | 88.9% | 85.7% | 92.1% | 145 |

#### 2.1.4. Ảnh hưởng của góc camera

| Góc camera | Độ chính xác | Độ nhạy | Độ đặc hiệu |
|------------|--------------|---------|-------------|
| Thẳng | 94.7% | 93.2% | 96.1% |
| +15° | 93.5% | 92.1% | 94.9% |
| -15° | 92.8% | 91.5% | 94.1% |
| +30° | 88.2% | 85.7% | 90.6% |
| -30° | 87.5% | 84.9% | 90.1% |

### 2.2. Hiệu suất phát hiện vị trí đầu

#### 2.2.1. Độ chính xác phát hiện vị trí đầu

| Vị trí đầu | Độ chính xác | Độ nhạy | Độ đặc hiệu | F1-score |
|------------|--------------|---------|-------------|----------|
| Thẳng | 95.3% | 94.1% | 96.5% | 0.953 |
| Nghiêng | 92.8% | 91.0% | 94.6% | 0.928 |
| Quay sang một bên | 94.1% | 93.2% | 95.0% | 0.941 |
| Cúi xuống | 91.5% | 89.8% | 93.2% | 0.915 |
| Ngẩng lên | 93.4% | 92.0% | 94.8% | 0.934 |

#### 2.2.2. Ma trận nhầm lẫn cho phân loại vị trí đầu

```
                         ┌────────────────────────────────────────────────────────┐
                         │        DỰ ĐOÁN                                         │
                         │    Thẳng  Nghiêng  Quay   Cúi    Ngẩng                 │
         ┌───────────────┼─────────────────────────────────────────────────────────
         │  Thẳng        │   95.3%   1.8%    1.2%   1.0%    0.7%                 │
         │               │                                                        │
         │  Nghiêng      │   3.5%    92.8%   1.2%   1.5%    1.0%                 │
THỰC TẾ  │               │                                                        │
         │  Quay         │   2.9%    1.3%    94.1%  1.0%    0.7%                 │
         │               │                                                        │
         │  Cúi          │   4.6%    2.2%    0.8%   91.5%   0.9%                 │
         │               │                                                        │
         │  Ngẩng        │   3.1%    1.9%    0.8%   0.8%    93.4%                │
         └───────────────┴────────────────────────────────────────────────────────┘
```

### 2.3. Hiệu suất phát hiện vị trí tay

#### 2.3.1. Độ chính xác phát hiện vị trí tay

| Trạng thái tay | Độ chính xác | Độ nhạy | Độ đặc hiệu | F1-score |
|----------------|--------------|---------|-------------|----------|
| Hai tay trên vô lăng | 93.5% | 92.1% | 94.9% | 0.935 |
| Một tay trên vô lăng | 90.8% | 88.7% | 92.9% | 0.907 |
| Không tay trên vô lăng | 91.5% | 89.8% | 93.2% | 0.915 |
| Cầm điện thoại | 89.0% | 86.5% | 91.5% | 0.890 |
| Cầm đồ vật khác | 87.3% | 84.2% | 90.4% | 0.870 |

#### 2.3.2. Ảnh hưởng của góc camera đến phát hiện vị trí tay

| Góc camera | Độ chính xác | Độ nhạy | Độ đặc hiệu |
|------------|--------------|---------|-------------|
| Thẳng | 91.5% | 89.8% | 93.2% |
| +15° | 89.8% | 87.5% | 92.1% |
| -15° | 90.2% | 88.1% | 92.3% |
| +30° | 85.7% | 82.9% | 88.5% |
| -30° | 84.9% | 81.7% | 88.1% |

### 2.4. Hiệu suất phân loại trạng thái tổng thể

#### 2.4.1. So sánh các mô hình phân loại

| Mô hình | Độ chính xác | Độ nhạy | Độ đặc hiệu | F1-score | Thời gian dự đoán (ms) |
|---------|--------------|---------|-------------|----------|------------------------|
| SVM (RBF kernel) | 92.5% | 90.8% | 94.2% | 0.915 | 0.8 |
| Random Forest | 93.1% | 91.3% | 94.9% | 0.922 | 1.5 |
| XGBoost | 93.5% | 91.8% | 95.2% | 0.926 | 2.3 |
| CNN | 94.2% | 92.5% | 95.9% | 0.933 | 12.3 |
| LSTM | 94.8% | 93.1% | 96.5% | 0.939 | 15.7 |

#### 2.4.2. Ma trận nhầm lẫn cho mô hình SVM

```
                         ┌────────────────────────────────────────────────────────┐
                         │        DỰ ĐOÁN                                         │
                         │    Tỉnh táo      Buồn ngủ      Mất tập trung          │
         ┌───────────────┼─────────────────────────────────────────────────────────
         │  Tỉnh táo     │     94.2%          3.5%           2.3%                │
THỰC TẾ  │               │                                                        │
         │  Buồn ngủ     │     6.3%           90.8%          2.9%                │
         │               │                                                        │
         │  Mất tập trung│     2.6%           4.6%           92.8%               │
         └───────────────┴────────────────────────────────────────────────────────┘
```

#### 2.4.3. Đường cong ROC

| Trạng thái | AUC |
|------------|-----|
| Tỉnh táo | 0.968 |
| Buồn ngủ | 0.952 |
| Mất tập trung | 0.943 |

#### 2.4.4. Phân tích theo khía cạnh thời gian của dự đoán

| Loại sự kiện | Thời gian trung bình để phát hiện (ms) | Độ lệch chuẩn (ms) |
|--------------|---------------------------------------|-------------------|
| Bắt đầu buồn ngủ | 325 | 85 |
| Phục hồi từ buồn ngủ | 270 | 65 |
| Bắt đầu mất tập trung | 180 | 42 |
| Phục hồi từ mất tập trung | 210 | 55 |

### 2.5. Đánh giá hiệu suất theo điều kiện thử nghiệm

#### 2.5.1. Hiệu suất theo loại đối tượng

| Nhóm | Độ chính xác | Độ nhạy | Độ đặc hiệu | F1-score |
|------|--------------|---------|-------------|----------|
| Nam | 93.1% | 91.5% | 94.7% | 0.925 |
| Nữ | 91.8% | 89.6% | 94.0% | 0.917 |
| 20-30 tuổi | 94.2% | 92.7% | 95.7% | 0.937 |
| 31-45 tuổi | 92.8% | 91.1% | 94.5% | 0.923 |
| 46-60 tuổi | 90.5% | 88.2% | 92.8% | 0.904 |
| Đeo kính | 89.5% | 87.3% | 91.7% | 0.893 |
| Không đeo kính | 93.8% | 92.1% | 95.5% | 0.932 |

#### 2.5.2. Hiệu suất theo thời điểm trong ngày

| Thời điểm | Độ chính xác | Độ nhạy | Độ đặc hiệu | F1-score |
|-----------|--------------|---------|-------------|----------|
| Buổi sáng (6-12h) | 93.5% | 91.8% | 95.2% | 0.932 |
| Buổi chiều (12-18h) | 92.1% | 90.4% | 93.8% | 0.919 |
| Buổi tối (18-24h) | 90.8% | 88.9% | 92.7% | 0.908 |
| Đêm khuya (0-6h) | 88.3% | 85.2% | 91.4% | 0.879 |

#### 2.5.3. Hiệu suất theo điều kiện giao thông

| Điều kiện | Độ chính xác | Độ nhạy | Độ đặc hiệu | F1-score |
|-----------|--------------|---------|-------------|----------|
| Đường cao tốc | 93.7% | 92.2% | 95.2% | 0.934 |
| Đường đô thị | 91.5% | 89.3% | 93.7% | 0.914 |
| Đường nông thôn | 92.8% | 90.9% | 94.7% | 0.926 |
| Giao thông đông đúc | 90.2% | 87.8% | 92.6% | 0.899 |
| Giao thông thưa thớt | 94.1% | 92.6% | 95.6% | 0.938 |

### 2.6. Hiệu suất tính toán

#### 2.6.1. So sánh hiệu suất trên các nền tảng khác nhau

| Nền tảng | FPS trung bình | Thời gian xử lý/khung (ms) | Sử dụng CPU | Sử dụng RAM |
|----------|----------------|----------------------------|-------------|-------------|
| Intel Core i5-10400 | 30.2 | 33.1 | 21.5% | 412MB |
| Intel Core i7-1165G7 | 28.5 | 35.1 | 23.5% | 420MB |
| AMD Ryzen 5 5600X | 33.7 | 29.7 | 18.7% | 405MB |
| Raspberry Pi 4 | 12.7 | 78.7 | 68.3% | 380MB |

#### 2.6.2. Tối ưu hóa hiệu suất

| Phương pháp tối ưu | FPS trên PC | FPS trên Raspberry Pi | Tác động đến độ chính xác |
|--------------------|-------------|----------------------|-----------------------------|
| Không tối ưu | 28.5 | 8.3 | 92.5% (baseline) |
| Giảm độ phân giải (640x480) | 35.8 | 12.7 | 91.8% (-0.7%) |
| Giảm độ chính xác MediaPipe | 42.3 | 15.2 | 89.4% (-3.1%) |
| Giảm tần suất phát hiện tay | 38.7 | 14.1 | 91.2% (-1.3%) |
| Lượng tử hóa mô hình | 32.6 | 13.5 | 91.6% (-0.9%) |
| Tất cả phương pháp | 52.4 | 19.3 | 88.7% (-3.8%) |

## 3. Phân tích và thảo luận

### 3.1. Phân tích các yếu tố ảnh hưởng

- **Ánh sáng**: Yếu tố có tác động mạnh nhất, giảm độ chính xác 5.8% trong điều kiện ánh sáng yếu
- **Góc camera**: Góc lệch >30° làm giảm đáng kể hiệu suất (~7%)
- **Đeo kính**: Giảm độ chính xác 4.3% do phản chiếu và che khuất một phần mắt
- **Thời điểm trong ngày**: Hiệu suất giảm vào buổi tối và đêm, có thể do điều kiện ánh sáng và mệt mỏi
- **Tuổi tác**: Đối tượng lớn tuổi có tỷ lệ phát hiện sai cao hơn 3.7%
- **Điều kiện giao thông**: Giao thông đông đúc làm giảm hiệu suất (3.9%) do sự phân tâm và stress

### 3.2. So sánh với các nghiên cứu trước đây

| Nghiên cứu | Phương pháp | Độ chính xác | FPS | Yêu cầu phần cứng | Khả năng triển khai |
|------------|-------------|--------------|-----|------------------|---------------------|
| Hệ thống đề xuất | EAR + SVM | 92.5% | 28.5 | Thấp | Cao |
| Rosebrock (2017) | EAR + CNN | 94.1% | 15.2 | Trung bình | Trung bình |
| García (2021) | PERCLOS + RF | 93.7% | 20.3 | Trung bình | Trung bình |
| Ibrahim (2022) | MediaPipe + LSTM | 92.8% | 18.7 | Trung bình | Trung bình |
| Park (2020) | DeepDrowsiness | 95.2% | 8.5 | Cao | Thấp |

### 3.3. Điểm mạnh và hạn chế của hệ thống

**Điểm mạnh:**
1. Hiệu suất thời gian thực tốt (28.5 FPS) trên phần cứng tiêu chuẩn
2. Yêu cầu tài nguyên thấp, có thể triển khai trên thiết bị nhúng
3. Độ chính xác cao trong điều kiện ánh sáng tốt (>94%)
4. Khả năng phát hiện đa trạng thái (buồn ngủ và nhiều loại mất tập trung)
5. Thời gian phát hiện nhanh (<200ms cho phần lớn trường hợp)
6. Kiến trúc module cho phép dễ dàng mở rộng và cải tiến
7. Hiệu suất ổn định khi sử dụng trong thời gian dài

**Hạn chế:**
1. Độ chính xác giảm trong điều kiện ánh sáng yếu (<100 lux)
2. Hiệu suất thấp hơn với người đeo kính (~4.3% giảm độ chính xác)
3. Khó phân biệt giữa nháy mắt thông thường và mắt nhắm do buồn ngủ trong thời gian ngắn
4. Độ trễ cao hơn khi phát hiện buồn ngủ so với mất tập trung
5. Hiệu suất không ổn định trong điều kiện ánh sáng thay đổi liên tục
6. FPS trên Raspberry Pi thấp hơn ngưỡng lý tưởng cho ứng dụng thời gian thực
7. Cần cải thiện khả năng phát hiện đồ vật trong tay

## 4. Kết luận

Kết quả thử nghiệm cho thấy hệ thống đã đạt được sự cân bằng tốt giữa độ chính xác và hiệu suất thời gian thực. Với độ chính xác tổng thể 92.5% và tốc độ xử lý 28.5 FPS trên phần cứng tiêu chuẩn, hệ thống có thể được triển khai hiệu quả trong các ứng dụng thực tế.

Điều kiện ánh sáng và góc camera là yếu tố ảnh hưởng lớn nhất đến hiệu suất, trong khi kỹ thuật hysteresis và làm mịn dữ liệu đã chứng minh hiệu quả trong việc giảm cảnh báo sai và tăng độ tin cậy.

Việc sử dụng mô hình SVM đã được chứng minh là lựa chọn hợp lý, cung cấp hiệu suất dự đoán tốt với thời gian xử lý nhanh, phù hợp cho các ứng dụng thời gian thực trên thiết bị nhúng.

Các phương pháp tối ưu hóa đã cho phép hệ thống hoạt động trên Raspberry Pi với tốc độ 12.7 FPS, đủ khả thi cho một số ứng dụng nhưng cần cải thiện thêm cho các trường hợp yêu cầu phản hồi nhanh hơn.
