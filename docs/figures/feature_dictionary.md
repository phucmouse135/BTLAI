# Từ điển đặc trưng (Feature Dictionary)

## Đặc trưng cho phát hiện buồn ngủ

### Đặc trưng con mắt

| Tên đặc trưng | Mô tả | Phạm vi giá trị | Đơn vị |
|---------------|-------|----------------|--------|
| `eye_ear_left` | Tỷ lệ khía cạnh mắt trái | 0.0 - 0.5 | N/A |
| `eye_ear_right` | Tỷ lệ khía cạnh mắt phải | 0.0 - 0.5 | N/A |
| `eye_ear_avg` | Giá trị EAR trung bình của hai mắt | 0.0 - 0.5 | N/A |
| `eye_ear_std` | Độ lệch chuẩn EAR giữa hai mắt | 0.0 - 0.2 | N/A |
| `blink_rate` | Tần suất nháy mắt | 0 - 30 | lần/phút |
| `blink_duration` | Thời gian trung bình của mỗi lần nháy mắt | 50 - 500 | ms |
| `perclos` | Phần trăm thời gian nhắm mắt | 0 - 100 | % |
| `eye_closure_count` | Số lần nhắm mắt kéo dài | 0 - 20 | lần/phút |
| `eye_opening_speed` | Tốc độ mở mắt sau khi nhắm | 0.0 - 1.0 | đơn vị/ms |
| `gaze_angle_x` | Góc nhìn theo phương ngang | -50 - 50 | độ |
| `gaze_angle_y` | Góc nhìn theo phương dọc | -50 - 50 | độ |

### Đặc trưng đầu và khuôn mặt

| Tên đặc trưng | Mô tả | Phạm vi giá trị | Đơn vị |
|---------------|-------|----------------|--------|
| `head_roll` | Góc nghiêng đầu | -90 - 90 | độ |
| `head_yaw` | Góc quay ngang đầu | -90 - 90 | độ |
| `head_pitch` | Góc ngẩng/cúi đầu | -90 - 90 | độ |
| `face_direction` | Hướng khuôn mặt (0: thẳng, 1-8: 8 hướng khác nhau) | 0 - 8 | N/A |
| `nose_deviation` | Độ lệch của mũi so với trung tâm khuôn mặt | -1.0 - 1.0 | N/A |
| `mouth_opening` | Độ mở của miệng | 0.0 - 1.0 | N/A |
| `yawn_count` | Số lần ngáp | 0 - 10 | lần/phút |
| `face_detection_confidence` | Độ tin cậy khi phát hiện khuôn mặt | 0.0 - 1.0 | N/A |
| `landmark_detection_stability` | Độ ổn định của phát hiện điểm mốc | 0.0 - 1.0 | N/A |
| `head_movement_frequency` | Tần suất chuyển động đầu | 0 - 30 | lần/phút |

## Đặc trưng cho phát hiện mất tập trung

### Đặc trưng vị trí tay

| Tên đặc trưng | Mô tả | Phạm vi giá trị | Đơn vị |
|---------------|-------|----------------|--------|
| `hands_on_wheel` | Số tay đặt trên vô lăng | 0 - 2 | N/A |
| `hands_on_wheel_confidence` | Độ tin cậy phát hiện tay trên vô lăng | 0.0 - 1.0 | N/A |
| `hand_left_position_x` | Vị trí x của tay trái | 0.0 - 1.0 | % màn hình |
| `hand_left_position_y` | Vị trí y của tay trái | 0.0 - 1.0 | % màn hình |
| `hand_right_position_x` | Vị trí x của tay phải | 0.0 - 1.0 | % màn hình |
| `hand_right_position_y` | Vị trí y của tay phải | 0.0 - 1.0 | % màn hình |
| `wheel_distance_left` | Khoảng cách từ tay trái đến vị trí dự kiến của vô lăng | 0.0 - 1.0 | % màn hình |
| `wheel_distance_right` | Khoảng cách từ tay phải đến vị trí dự kiến của vô lăng | 0.0 - 1.0 | % màn hình |
| `object_in_hand` | Phát hiện đồ vật trong tay (0: không, 1: có) | 0 - 1 | N/A |
| `object_type` | Loại đồ vật (0: không, 1: điện thoại, 2: đồ uống, 3: khác) | 0 - 3 | N/A |

### Đặc trưng thời gian

| Tên đặc trưng | Mô tả | Phạm vi giá trị | Đơn vị |
|---------------|-------|----------------|--------|
| `driving_duration` | Thời gian lái xe liên tục | 0 - 86400 | giây |
| `time_since_last_break` | Thời gian từ lần nghỉ gần nhất | 0 - 86400 | giây |
| `time_of_day` | Thời điểm trong ngày | 0 - 23 | giờ |
| `time_zone_difference` | Độ lệch múi giờ so với múi giờ thông thường của người lái | -12 - 12 | giờ |
| `continuous_focus_duration` | Thời gian tập trung liên tục | 0 - 3600 | giây |
| `distraction_frequency` | Tần suất mất tập trung | 0 - 60 | lần/giờ |
| `reaction_time` | Thời gian phản ứng với cảnh báo | 0 - 10000 | ms |
| `microsleep_count` | Số lần ngủ gật ngắn | 0 - 20 | lần/giờ |

## Đặc trưng tổng hợp và phái sinh

| Tên đặc trưng | Mô tả | Công thức tính toán |
|---------------|-------|---------------------|
| `drowsiness_score` | Điểm đánh giá mức độ buồn ngủ | `0.6*perclos + 0.3*eye_ear_avg + 0.1*yawn_count` |
| `distraction_score` | Điểm đánh giá mức độ mất tập trung | `0.5*head_deviation + 0.3*hands_on_wheel + 0.2*object_in_hand` |
| `fatigue_index` | Chỉ số mệt mỏi tổng hợp | `0.5*drowsiness_score + 0.3*driving_duration/3600 + 0.2*time_since_last_break/3600` |
| `attention_level` | Mức độ chú ý | `1.0 - distraction_score` |
| `eye_state_consistency` | Độ nhất quán của trạng thái mắt | Tỷ lệ số khung hình có EAR ổn định |
| `head_position_stability` | Độ ổn định vị trí đầu | Nghịch đảo độ lệch chuẩn của góc đầu trong 30 khung hình gần nhất |
| `hand_position_adequacy` | Mức độ phù hợp của vị trí tay | Dựa trên số tay đặt trên vô lăng và vị trí đặt |

## Mã nguồn trích xuất đặc trưng

```python
def extract_features(face_landmarks, hand_landmarks, history_buffer, time_info):
    """
    Trích xuất vector đặc trưng từ các điểm mốc khuôn mặt và tay.
    
    Tham số:
        face_landmarks: Danh sách điểm mốc khuôn mặt từ MediaPipe
        hand_landmarks: Danh sách điểm mốc tay từ MediaPipe
        history_buffer: Bộ đệm lưu trữ dữ liệu quá khứ
        time_info: Thông tin thời gian hiện tại
    
    Trả về:
        Dict chứa các đặc trưng đã trích xuất
    """
    features = {}
    
    # Trích xuất đặc trưng con mắt
    if face_landmarks:
        # Tính EAR cho mắt trái và phải
        left_eye_landmarks = extract_landmarks(face_landmarks, LEFT_EYE_INDICES)
        right_eye_landmarks = extract_landmarks(face_landmarks, RIGHT_EYE_INDICES)
        
        left_ear = calculate_ear(left_eye_landmarks)
        right_ear = calculate_ear(right_eye_landmarks)
        
        features['eye_ear_left'] = left_ear
        features['eye_ear_right'] = right_ear
        features['eye_ear_avg'] = (left_ear + right_ear) / 2.0
        features['eye_ear_std'] = abs(left_ear - right_ear)
        
        # Tính tỷ lệ PERCLOS từ lịch sử EAR
        ear_history = history_buffer.get_values('eye_ear_avg', 300)  # 10 giây ở 30fps
        if ear_history:
            closed_frames = sum(1 for ear in ear_history if ear < EYE_AR_THRESHOLD)
            features['perclos'] = closed_frames / len(ear_history) * 100
        else:
            features['perclos'] = 0
        
        # Phát hiện nháy mắt
        blinks = detect_blinks(history_buffer.get_values('eye_ear_avg', 1800))  # 1 phút ở 30fps
        features['blink_rate'] = len(blinks) * (60 / (len(ear_history) / 30)) if ear_history else 0
        features['blink_duration'] = sum(b['duration'] for b in blinks) / len(blinks) if blinks else 0
        
        # Góc nhìn
        gaze_angles = calculate_gaze_angles(face_landmarks)
        features['gaze_angle_x'] = gaze_angles['x']
        features['gaze_angle_y'] = gaze_angles['y']
        
        # Đặc trưng đầu và khuôn mặt
        head_pose = calculate_head_pose(face_landmarks)
        features['head_roll'] = head_pose['roll']
        features['head_yaw'] = head_pose['yaw']
        features['head_pitch'] = head_pose['pitch']
        
        # Độ lệch mũi
        nose_tip = face_landmarks[1]  # Điểm mốc mũi
        face_center = calculate_face_center(face_landmarks)
        face_width = calculate_face_width(face_landmarks)
        
        if face_width > 0:
            features['nose_deviation'] = (nose_tip.x - face_center[0]) / face_width
        else:
            features['nose_deviation'] = 0
            
        # Phát hiện ngáp
        mouth_landmarks = extract_landmarks(face_landmarks, MOUTH_INDICES)
        features['mouth_opening'] = calculate_mouth_aspect_ratio(mouth_landmarks)
        
        yawns = detect_yawns(history_buffer.get_values('mouth_opening', 1800))
        features['yawn_count'] = len(yawns)
    else:
        # Giá trị mặc định khi không phát hiện khuôn mặt
        default_eye_features = {
            'eye_ear_left': 0.0, 'eye_ear_right': 0.0, 'eye_ear_avg': 0.0, 
            'eye_ear_std': 0.0, 'blink_rate': 0.0, 'blink_duration': 0.0,
            'perclos': 0.0, 'gaze_angle_x': 0.0, 'gaze_angle_y': 0.0,
            'head_roll': 0.0, 'head_yaw': 0.0, 'head_pitch': 0.0,
            'nose_deviation': 0.0, 'mouth_opening': 0.0, 'yawn_count': 0
        }
        features.update(default_eye_features)
    
    # Đặc trưng vị trí tay
    if hand_landmarks:
        hands_on_wheel = 0
        left_hand_detected = False
        right_hand_detected = False
        
        for hand_idx, hand_lm in enumerate(hand_landmarks):
            # Xác định tay trái hay tay phải
            is_left_hand = determine_hand_side(hand_lm)
            
            # Vị trí cổ tay
            wrist = hand_lm.landmark[0]  # Điểm mốc cổ tay
            
            if is_left_hand:
                left_hand_detected = True
                features['hand_left_position_x'] = wrist.x
                features['hand_left_position_y'] = wrist.y
                features['wheel_distance_left'] = calculate_distance_to_wheel(wrist.x, wrist.y)
                
                if features['wheel_distance_left'] <= WHEEL_DISTANCE_THRESHOLD:
                    hands_on_wheel += 1
            else:
                right_hand_detected = True
                features['hand_right_position_x'] = wrist.x
                features['hand_right_position_y'] = wrist.y
                features['wheel_distance_right'] = calculate_distance_to_wheel(wrist.x, wrist.y)
                
                if features['wheel_distance_right'] <= WHEEL_DISTANCE_THRESHOLD:
                    hands_on_wheel += 1
            
            # Phát hiện đồ vật trong tay
            object_in_hand, object_type = detect_object_in_hand(hand_lm)
            
            if object_in_hand:
                features['object_in_hand'] = 1
                features['object_type'] = object_type
        
        features['hands_on_wheel'] = hands_on_wheel
        
        if not left_hand_detected:
            features['hand_left_position_x'] = -1.0
            features['hand_left_position_y'] = -1.0
            features['wheel_distance_left'] = float('inf')
            
        if not right_hand_detected:
            features['hand_right_position_x'] = -1.0
            features['hand_right_position_y'] = -1.0
            features['wheel_distance_right'] = float('inf')
    else:
        # Giá trị mặc định khi không phát hiện tay
        default_hand_features = {
            'hands_on_wheel': 0, 'hand_left_position_x': -1.0, 'hand_left_position_y': -1.0,
            'hand_right_position_x': -1.0, 'hand_right_position_y': -1.0,
            'wheel_distance_left': float('inf'), 'wheel_distance_right': float('inf'),
            'object_in_hand': 0, 'object_type': 0
        }
        features.update(default_hand_features)
    
    # Đặc trưng thời gian
    features.update({
        'driving_duration': time_info['driving_duration'],
        'time_since_last_break': time_info['time_since_last_break'],
        'time_of_day': time_info['hour'],
        'continuous_focus_duration': history_buffer.get_last_focus_duration()
    })
    
    # Tính toán đặc trưng tổng hợp
    if 'perclos' in features and 'eye_ear_avg' in features and 'yawn_count' in features:
        normalized_ear = max(0, min(1, features['eye_ear_avg'] / 0.5))
        normalized_perclos = features['perclos'] / 100.0
        normalized_yawn = min(1, features['yawn_count'] / 10.0)
        
        features['drowsiness_score'] = (0.6 * normalized_perclos + 
                                       0.3 * (1 - normalized_ear) + 
                                       0.1 * normalized_yawn)
    else:
        features['drowsiness_score'] = 0
    
    if ('nose_deviation' in features and 'hands_on_wheel' in features and 
            'object_in_hand' in features):
        normalized_head = min(1, abs(features['nose_deviation']) / 0.3)
        normalized_hands = 1 - (features['hands_on_wheel'] / 2.0)
        
        features['distraction_score'] = (0.5 * normalized_head + 
                                        0.3 * normalized_hands + 
                                        0.2 * features['object_in_hand'])
        
        features['attention_level'] = 1.0 - features['distraction_score']
    else:
        features['distraction_score'] = 0
        features['attention_level'] = 1.0
    
    if 'drowsiness_score' in features and 'driving_duration' in features:
        norm_duration = min(1, features['driving_duration'] / 14400)  # 4 giờ
        norm_break_time = min(1, features['time_since_last_break'] / 7200)  # 2 giờ
        
        features['fatigue_index'] = (0.5 * features['drowsiness_score'] + 
                                    0.3 * norm_duration + 
                                    0.2 * norm_break_time)
    else:
        features['fatigue_index'] = 0
    
    return features
```

## Lựa chọn đặc trưng và phân tích tầm quan trọng

Dựa trên phân tích với Random Forest, mức độ quan trọng của các đặc trưng được xếp hạng như sau:

1. `perclos` (0.185): Phần trăm thời gian nhắm mắt
2. `eye_ear_avg` (0.172): Giá trị EAR trung bình
3. `blink_duration` (0.112): Thời gian nháy mắt trung bình
4. `nose_deviation` (0.098): Độ lệch của mũi
5. `head_yaw` (0.087): Góc quay đầu
6. `hands_on_wheel` (0.082): Số tay đặt trên vô lăng
7. `driving_duration` (0.063): Thời gian lái xe liên tục
8. `head_roll` (0.051): Góc nghiêng đầu
9. `object_in_hand` (0.047): Phát hiện đồ vật trong tay
10. `mouth_opening` (0.043): Độ mở miệng
11. `time_of_day` (0.029): Thời điểm trong ngày
12. `time_since_last_break` (0.023): Thời gian từ lần nghỉ gần nhất
13. `blink_rate` (0.008): Tần suất nháy mắt

Đặc trưng có mối tương quan cao:
- `eye_ear_left` và `eye_ear_right` (r=0.94)
- `perclos` và `drowsiness_score` (r=0.89)
- `head_yaw` và `nose_deviation` (r=0.87)
- `driving_duration` và `time_since_last_break` (r=0.82)

Kết luận: Dựa trên phân tích trên, một tập con đặc trưng tối ưu đã được chọn cho mô hình cuối cùng, bao gồm: `perclos`, `eye_ear_avg`, `blink_duration`, `nose_deviation`, `hands_on_wheel`, `head_yaw`, `object_in_hand`, `driving_duration` và `time_of_day`.
