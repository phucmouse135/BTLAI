## Phương Pháp Làm Mịn Dữ Liệu Thời Gian

Hệ thống sử dụng nhiều phương pháp làm mịn dữ liệu thời gian để cải thiện độ chính xác và giảm cảnh báo giả:

### 1. Bộ Lọc Trung Bình Trượt (Moving Average Filter)

Công thức toán học cho bộ lọc trung bình trượt được áp dụng cho các giá trị EAR:

```
EAR_smoothed(t) = (1/N) × Σ[EAR(t-i)] với i từ 0 đến N-1
```

Trong đó:
- `EAR_smoothed(t)` là giá trị EAR đã làm mịn tại thời điểm t
- `EAR(t-i)` là giá trị EAR nguyên bản tại thời điểm t-i
- `N` là kích thước cửa sổ trượt (thông thường N = 5 đến 10 khung)

Bộ lọc này được triển khai trong mã nguồn như sau:

```python
# Cập nhật lịch sử giá trị EAR
self.ear_history.append(ear)
if len(self.ear_history) > self.MAX_EAR_HISTORY:
    self.ear_history.pop(0)
    
# Tính trung bình trượt
if len(self.ear_history) > 0:
    smoothed_ear = sum(self.ear_history) / len(self.ear_history)
else:
    smoothed_ear = ear
```

### 2. Bộ Lọc Median (Median Filter)

Công thức cho bộ lọc median:

```
EAR_median(t) = median[EAR(t-N+1), EAR(t-N+2), ..., EAR(t)]
```

Bộ lọc này đặc biệt hiệu quả trong việc loại bỏ nhiễu đột biến (outliers) trong dữ liệu EAR. Nó ưu tiên giá trị trung vị thay vì giá trị trung bình, giúp hệ thống ổn định hơn khi có các giá trị nhiễu:

```python
# Lấy giá trị trung vị từ N khung gần nhất
def get_median_ear(self):
    if len(self.ear_history) > 0:
        return np.median(self.ear_history)
    return 0
```

### 3. Bộ Lọc Kalman (Kalman Filter)

Công thức cho bộ lọc Kalman một chiều được sử dụng để làm mịn dữ liệu EAR:

```
Dự đoán (Predict):
x̂_k|k-1 = A × x̂_k-1|k-1
P_k|k-1 = A × P_k-1|k-1 × A^T + Q

Cập nhật (Update):
K_k = P_k|k-1 × H^T × (H × P_k|k-1 × H^T + R)^-1
x̂_k|k = x̂_k|k-1 + K_k × (z_k - H × x̂_k|k-1)
P_k|k = (I - K_k × H) × P_k|k-1
```

Trong đó:
- `x̂_k|k-1` là ước tính trạng thái trước khi quan sát
- `x̂_k|k` là ước tính trạng thái sau khi quan sát
- `z_k` là giá trị đo lường (EAR)
- `P_k|k-1` và `P_k|k` là ma trận hiệp phương sai của lỗi ước tính
- `K_k` là hệ số Kalman
- `A` là ma trận chuyển trạng thái (thường bằng 1 cho trường hợp đơn giản)
- `H` là ma trận quan sát (thường bằng 1 cho trường hợp đơn giản)
- `Q` là hiệp phương sai nhiễu quá trình
- `R` là hiệp phương sai nhiễu đo lường

Hệ thống sử dụng bộ lọc Kalman để loại bỏ nhiễu từ giá trị EAR, giúp phát hiện buồn ngủ chính xác hơn, đặc biệt trong điều kiện ánh sáng khó khăn.

### 4. Kỹ Thuật Hysteresis (Hysteresis Technique)

Kỹ thuật này giúp tránh hiện tượng dao động nhanh giữa các trạng thái khi giá trị đo lường dao động xung quanh ngưỡng phát hiện:

```python
# Áp dụng hysteresis để tránh dao động trạng thái
if current_state == "NORMAL":
    # Yêu cầu giá trị thấp hơn ngưỡng đáng kể để chuyển sang trạng thái cảnh báo
    threshold_to_warning = self.EAR_THRESHOLD - 0.02
    
    if ear < threshold_to_warning and consecutive_frames > self.WARNING_THRESHOLD:
        new_state = "WARNING"
elif current_state == "WARNING":
    # Yêu cầu giá trị cao hơn ngưỡng đáng kể để trở về trạng thái bình thường
    threshold_to_normal = self.EAR_THRESHOLD + 0.02
    
    if ear > threshold_to_normal:
        recovery_frames += 1
        if recovery_frames > self.RECOVERY_THRESHOLD:
            new_state = "NORMAL"
            recovery_frames = 0
    # Yêu cầu giá trị thấp hơn ngưỡng đáng kể để chuyển sang trạng thái cảnh báo
    threshold_to_alert = self.EAR_THRESHOLD - 0.05
    
    if ear < threshold_to_alert and consecutive_frames > self.ALERT_THRESHOLD:
        new_state = "ALERT"
```

### 5. Phương Pháp Thống Kê Cửa Sổ (Windowed Statistics)

Phương pháp này phân tích các thống kê khác nhau trong một cửa sổ dữ liệu, không chỉ giá trị trung bình:

```
EAR_variability = σ_EAR / μ_EAR
```

Trong đó:
- `σ_EAR` là độ lệch chuẩn của giá trị EAR trong cửa sổ
- `μ_EAR` là giá trị trung bình của EAR trong cửa sổ

Độ biến thiên này được sử dụng để phát hiện các mẫu nháy mắt (mắt đóng mở nhanh) khác với các mẫu buồn ngủ (mắt nhắm dần và đóng trong thời gian dài).

```python
# Tính độ biến thiên trong cửa sổ
def calculate_ear_variability(self):
    if len(self.ear_history) > 5:  # Cần ít nhất 5 mẫu
        std_dev = np.std(self.ear_history)
        mean_val = np.mean(self.ear_history)
        if mean_val > 0:
            return std_dev / mean_val
    return 0
```

### 6. Tích Hợp Dữ Liệu Đa Cảm Biến (Multi-Sensor Data Fusion)

Công thức để kết hợp dữ liệu từ nhiều nguồn (EAR, vị trí đầu, vị trí tay):

```
drowsiness_score = w₁ × normalized_EAR + w₂ × normalized_head_pose + w₃ × normalized_blink_rate
distraction_score = w₄ × normalized_head_pose + w₅ × normalized_hand_position
```

Trong đó:
- `w₁` đến `w₅` là các trọng số được hiệu chỉnh dựa trên thử nghiệm
- Các giá trị được chuẩn hóa nằm trong khoảng [0, 1]

Điểm số tổng hợp này cung cấp một chỉ báo mạnh mẽ hơn về trạng thái buồn ngủ hoặc mất tập trung, giảm thiểu tác động của nhiễu từ các cảm biến riêng lẻ.
