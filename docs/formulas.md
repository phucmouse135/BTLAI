# Công Thức Toán Học Trong Hệ Thống Phát Hiện Buồn Ngủ

Tài liệu này mô tả chi tiết các công thức toán học được sử dụng trong hệ thống phát hiện buồn ngủ và mất tập trung.

## I. Công Thức Tính Góc Xoay Đầu

### 1. Góc Nghiêng Đầu (Tilt Angle/Roll)

Góc nghiêng của đầu được tính dựa trên độ nghiêng của đường nối giữa hai mắt so với trục ngang:

```
eye_line = right_eye_center - left_eye_center
angle_rad = arctan2(eye_line[1], eye_line[0])
angle_deg = angle_rad × (180/π)
```

Trong đó:
- `right_eye_center` là tọa độ trung bình các điểm mốc của mắt phải `[x_right, y_right]`
- `left_eye_center` là tọa độ trung bình các điểm mốc của mắt trái `[x_left, y_left]` 
- `arctan2(y, x)` là hàm lượng giác hai tham số trả về góc trong khoảng [-π, π]
- Góc được chuyển từ radian sang độ bằng cách nhân với (180/π)

Sau đó, góc được chuẩn hóa về khoảng từ -90° đến 90°:

```
if angle_deg > 90:
    angle_deg = angle_deg - 180
elif angle_deg < -90:
    angle_deg = angle_deg + 180
```

### 2. Góc Quay Ngang (Yaw)

Góc quay ngang của đầu được xác định dựa trên độ lệch của mũi so với mặt phẳng giữa hai mắt:

```
face_center = (left_eye_center + right_eye_center) / 2
midpoint_x = (left_eye_center[0] + right_eye_center[0]) / 2
nose_deviation = (nose_tip[0] - midpoint_x) / face_width
```

Trong đó:
- `nose_tip` là tọa độ điểm mũi `[nose_x, nose_y]`
- `midpoint_x` là hoành độ của điểm giữa hai mắt
- `face_width` là chiều rộng khuôn mặt (khoảng cách lớn nhất giữa các điểm mốc theo chiều ngang)
- `nose_deviation` là độ lệch chuẩn hóa của mũi so với trục giữa mặt, giá trị dương khi quay phải, âm khi quay trái

### 3. Công Thức Phát Hiện Trạng Thái Xoay Đầu

```
is_tilted = |angle_deg| > 20
is_looking_sideways = |nose_deviation| > 0.15
```

Trong đó:
- `is_tilted` là cờ đánh dấu đầu nghiêng (TRUE nếu góc nghiêng vượt quá 20°)
- `is_looking_sideways` là cờ đánh dấu đầu quay ngang (TRUE nếu độ lệch của mũi vượt quá 15% chiều rộng mặt)

## II. Công Thức Tính Khoảng Cách Tay Với Vô Lăng

### 1. Khoảng Cách Euclidean Từ Tay Đến Vô Lăng

```
distance = √[(wrist_x - wheel_center_x)² + (wrist_y - wheel_center_y)²]
```

Trong đó:
- `wrist_x, wrist_y` là tọa độ của điểm cổ tay (MediaPipe landmark index 0) đã được chuẩn hóa trong khoảng [0, 1]
- `wheel_center_x, wheel_center_y` là tọa độ ước tính của trung tâm vô lăng (thường là `[0.5, 0.7]` trong không gian chuẩn hóa)
- `distance` là khoảng cách Euclidean đã chuẩn hóa từ cổ tay đến trung tâm vô lăng

### 2. Phát Hiện Vị Trí Tay Trên Vô Lăng

```
is_hand_on_wheel = distance ≤ wheel_radius
```

Trong đó:
- `wheel_radius` là bán kính ước tính của vô lăng (thông thường khoảng 0.2 trong không gian chuẩn hóa)
- `is_hand_on_wheel` là cờ đánh dấu tay đặt trên vô lăng

### 3. Phát Hiện Cầm Điện Thoại Dựa Trên Hình Dạng Bàn Tay

```
finger_coords = [[landmark[i].x, landmark[i].y] for i in finger_points]
finger_spread = std(finger_coords)
tight_grip = mean(finger_spread) < (frame_width × 0.1)

thumb_tip = [hand_landmarks.landmark[4].x, hand_landmarks.landmark[4].y]
middle_tip = [hand_landmarks.landmark[12].x, hand_landmarks.landmark[12].y]
pinch_distance = ||thumb_tip - middle_tip||
pinch_detected = pinch_distance < (frame_width × 0.05)

hand_center_y = mean(palm_coords[:, 1])
at_face_level = hand_center_y < wheel_region_y

is_holding_phone = ((tight_grip && palm_vertical) || pinch_detected) && at_face_level
```

Trong đó:
- `finger_points` là các chỉ số của điểm mốc đầu ngón tay `[8, 12, 16, 20]`
- `finger_spread` là độ lệch chuẩn của các tọa độ đầu ngón tay
- `tight_grip` là cờ đánh dấu các ngón tay gần nhau
- `pinch_detected` là cờ đánh dấu ngón cái và ngón trỏ chụm lại
- `at_face_level` là cờ đánh dấu tay nâng lên ngang mặt
- `is_holding_phone` là kết quả phát hiện cầm điện thoại

## III. Ngưỡng Phát Hiện Trạng Thái

### 1. Ngưỡng Phát Hiện Buồn Ngủ

Trạng thái buồn ngủ được xác định khi:

```
is_drowsy = (avg_ear < EAR_THRESHOLD) && (drowsy_frame_counter ≥ DROWSY_CONSEC_FRAMES)
```

Trong đó:
- `avg_ear` là giá trị EAR trung bình của hai mắt
- `EAR_THRESHOLD` là ngưỡng EAR (mặc định: 0.2)
- `drowsy_frame_counter` là số khung hình liên tiếp có giá trị EAR dưới ngưỡng
- `DROWSY_CONSEC_FRAMES` là số khung hình tối thiểu để xác nhận trạng thái buồn ngủ (mặc định: 20)

### 2. Ngưỡng Phát Hiện Mất Tập Trung Do Vị Trí Đầu

Mất tập trung do vị trí đầu được xác định khi:

```
is_head_distracted = (is_tilted || is_looking_sideways) && (distracted_frame_counter ≥ DISTRACTED_CONSEC_FRAMES)
```

Trong đó:
- `is_tilted` là cờ đánh dấu đầu nghiêng (|angle_deg| > 20°)
- `is_looking_sideways` là cờ đánh dấu đầu quay ngang (|nose_deviation| > 0.15)
- `distracted_frame_counter` là số khung hình liên tiếp phát hiện đầu nghiêng/quay
- `DISTRACTED_CONSEC_FRAMES` là số khung hình tối thiểu để xác nhận mất tập trung (mặc định: 25)

### 3. Ngưỡng Phát Hiện Mất Tập Trung Do Sử Dụng Điện Thoại

Mất tập trung do sử dụng điện thoại được xác định khi:

```
is_phone_distracted = is_holding_phone && (distracted_head_hands_counter ≥ DISTRACTED_HEAD_HANDS_CONSEC_FRAMES)
```

Trong đó:
- `is_holding_phone` là cờ đánh dấu phát hiện tay cầm điện thoại
- `distracted_head_hands_counter` là số khung hình liên tiếp phát hiện cầm điện thoại
- `DISTRACTED_HEAD_HANDS_CONSEC_FRAMES` là số khung hình tối thiểu để xác nhận mất tập trung do điện thoại (mặc định: 20)

### 4. Ngưỡng Phát Hiện Đầu Ra Khỏi Khung Hình

```
head_out_of_frame = (head_out_of_frame_counter ≥ HEAD_OUT_OF_FRAME_CONSEC_FRAMES)
```

Trong đó:
- `head_out_of_frame_counter` là số khung hình liên tiếp không phát hiện được khuôn mặt
- `HEAD_OUT_OF_FRAME_CONSEC_FRAMES` là số khung hình tối thiểu để xác nhận đầu ra khỏi khung hình (mặc định: 10)

### 5. Công Thức Điều Chỉnh Ngưỡng Động

Hệ thống còn bao gồm cơ chế điều chỉnh ngưỡng động dựa trên điều kiện ánh sáng và các yếu tố môi trường:

```
adjusted_ear_threshold = base_ear_threshold × (1 + light_compensation_factor)
```

Trong đó:
- `base_ear_threshold` là ngưỡng EAR cơ bản (mặc định: 0.2)
- `light_compensation_factor` là hệ số điều chỉnh dựa trên điều kiện ánh sáng (phạm vi: -0.1 đến +0.1)
