# Mathematical Formulas in Drowsiness Detection System

This document describes in detail the mathematical formulas used in the drowsiness and distraction detection system.

> Note: This is the English version of the document. The Vietnamese version is available at [formulas.md](formulas.md).

## I. Head Rotation Angle Calculation Formulas

### 1. Head Tilt Angle (Roll)

The head tilt angle is calculated based on the slope of the line connecting the two eyes relative to the horizontal axis:

```
eye_line = right_eye_center - left_eye_center
angle_rad = arctan2(eye_line[1], eye_line[0])
angle_deg = angle_rad × (180/π)
```

Where:
- `right_eye_center` is the average coordinate of the right eye landmarks `[x_right, y_right]`
- `left_eye_center` is the average coordinate of the left eye landmarks `[x_left, y_left]` 
- `arctan2(y, x)` is the two-parameter arctangent function returning an angle in the range [-π, π]
- The angle is converted from radians to degrees by multiplying by (180/π)

Then, the angle is normalized to the range -90° to 90°:

```
if angle_deg > 90:
    angle_deg = angle_deg - 180
elif angle_deg < -90:
    angle_deg = angle_deg + 180
```

### 2. Head Yaw Angle

The horizontal rotation (yaw) of the head is determined by the deviation of the nose relative to the midplane between the eyes:

```
face_center = (left_eye_center + right_eye_center) / 2
midpoint_x = (left_eye_center[0] + right_eye_center[0]) / 2
nose_deviation = (nose_tip[0] - midpoint_x) / face_width
```

Where:
- `nose_tip` is the coordinate of the nose tip `[nose_x, nose_y]`
- `midpoint_x` is the x-coordinate of the point between the two eyes
- `face_width` is the face width (maximum distance between facial landmarks horizontally)
- `nose_deviation` is the normalized deviation of the nose from the center axis of the face, positive when turning right, negative when turning left

### 3. Head Rotation State Detection Formula

```
is_tilted = |angle_deg| > 20
is_looking_sideways = |nose_deviation| > 0.15
```

Where:
- `is_tilted` is a flag indicating head tilt (TRUE if tilt angle exceeds 20°)
- `is_looking_sideways` is a flag indicating horizontal head rotation (TRUE if nose deviation exceeds 15% of face width)

## II. Hand-Wheel Distance Calculation Formulas

### 1. Euclidean Distance from Hand to Wheel

```
distance = √[(wrist_x - wheel_center_x)² + (wrist_y - wheel_center_y)²]
```

Where:
- `wrist_x, wrist_y` are the coordinates of the wrist point (MediaPipe landmark index 0) normalized in the range [0, 1]
- `wheel_center_x, wheel_center_y` are the estimated coordinates of the wheel center (typically `[0.5, 0.7]` in normalized space)
- `distance` is the normalized Euclidean distance from the wrist to the wheel center

### 2. Hand on Wheel Position Detection

```
is_hand_on_wheel = distance ≤ wheel_radius
```

Where:
- `wheel_radius` is the estimated radius of the steering wheel (typically around 0.2 in normalized space)
- `is_hand_on_wheel` is a flag indicating the hand is placed on the wheel

### 3. Phone Holding Detection Based on Hand Shape

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

Where:
- `finger_points` are the indices of the fingertip landmarks `[8, 12, 16, 20]`
- `finger_spread` is the standard deviation of fingertip coordinates
- `tight_grip` is a flag indicating fingers are close together
- `pinch_detected` is a flag indicating the thumb and index finger are pinched together
- `at_face_level` is a flag indicating the hand is raised to face level
- `is_holding_phone` is the result of phone holding detection

## III. Detection Threshold Formulas

### 1. Drowsiness Detection Threshold

Drowsiness state is determined when:

```
is_drowsy = (avg_ear < EAR_THRESHOLD) && (drowsy_frame_counter ≥ DROWSY_CONSEC_FRAMES)
```

Where:
- `avg_ear` is the average EAR value for both eyes
- `EAR_THRESHOLD` is the EAR threshold (default: 0.2)
- `drowsy_frame_counter` is the number of consecutive frames with EAR value below the threshold
- `DROWSY_CONSEC_FRAMES` is the minimum number of frames to confirm drowsiness state (default: 20)

### 2. Head Position Distraction Threshold

Head position distraction is determined when:

```
is_head_distracted = (is_tilted || is_looking_sideways) && (distracted_frame_counter ≥ DISTRACTED_CONSEC_FRAMES)
```

Where:
- `is_tilted` is a flag indicating head tilt (|angle_deg| > 20°)
- `is_looking_sideways` is a flag indicating horizontal head rotation (|nose_deviation| > 0.15)
- `distracted_frame_counter` is the number of consecutive frames with head tilt/rotation detection
- `DISTRACTED_CONSEC_FRAMES` is the minimum number of frames to confirm distraction (default: 25)

### 3. Phone Usage Distraction Threshold

Phone usage distraction is determined when:

```
is_phone_distracted = is_holding_phone && (distracted_head_hands_counter ≥ DISTRACTED_HEAD_HANDS_CONSEC_FRAMES)
```

Where:
- `is_holding_phone` is a flag indicating phone holding detection
- `distracted_head_hands_counter` is the number of consecutive frames with phone holding detection
- `DISTRACTED_HEAD_HANDS_CONSEC_FRAMES` is the minimum number of frames to confirm phone distraction (default: 20)

### 4. Head Out of Frame Detection Threshold

```
head_out_of_frame = (head_out_of_frame_counter ≥ HEAD_OUT_OF_FRAME_CONSEC_FRAMES)
```

Where:
- `head_out_of_frame_counter` is the number of consecutive frames where no face is detected
- `HEAD_OUT_OF_FRAME_CONSEC_FRAMES` is the minimum number of frames to confirm head is out of frame (default: 10)

### 5. Dynamic Threshold Adjustment Formula

The system includes a mechanism to dynamically adjust thresholds based on lighting conditions and environmental factors:

```
adjusted_ear_threshold = base_ear_threshold × (1 + light_compensation_factor)
```

Where:
- `base_ear_threshold` is the basic EAR threshold (default: 0.2)
- `light_compensation_factor` is an adjustment coefficient based on lighting conditions (range: -0.1 to +0.1)
