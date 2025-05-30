# Minh họa tính toán EAR (Eye Aspect Ratio)

## Nguyên lý tính toán

Eye Aspect Ratio (EAR) là một phép đo tỷ lệ giữa chiều cao và chiều rộng của mắt. Giá trị này được dùng để xác định trạng thái mở/nhắm của mắt, và là một trong những phương pháp hiệu quả để phát hiện buồn ngủ dựa trên trạng thái mắt.

```
         p2 ________ p3
           /        \
      p1  /          \  p4
          \          /
           \________/
           p6        p5

EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
```

Trong đó:
- p1 đến p6 là các điểm mốc (landmarks) của mắt
- ||p1-p4|| là khoảng cách Euclidean giữa điểm p1 và p4
- ||p2-p6|| và ||p3-p5|| đại diện cho chiều cao của mắt
- ||p1-p4|| đại diện cho chiều rộng của mắt

## Ví dụ tính toán cụ thể

Với các tọa độ điểm (đơn vị pixel):
- p1 = (130, 100)
- p2 = (145, 90)
- p3 = (155, 90)
- p4 = (170, 100)
- p5 = (155, 110)
- p6 = (145, 110)

Tính toán:
- ||p2-p6|| = √[(145-145)² + (90-110)²] = 20
- ||p3-p5|| = √[(155-155)² + (90-110)²] = 20
- ||p1-p4|| = √[(130-170)² + (100-100)²] = 40

EAR = (20 + 20) / (2 * 40) = 0.5

## Mối quan hệ giữa EAR và trạng thái mắt

```
   EAR
   0.5 ┼───────────────────────────────────────
       │                  Mắt mở
       │          ╭─────────────────────────────
   0.4 ┤         ╱
       │        ╱
       │       ╱
   0.3 ┤      ╱
       │     ╱
       │    ╱
   0.2 ┤───╱────────────────────────────────────
       │    Mắt nhắm         Vùng ngưỡng
       │
   0.1 ┤
       │
       │
   0.0 ┼───────────────────────────────────────
```

| Trạng thái mắt | Giá trị EAR |
|----------------|-------------|
| Mắt mở hoàn toàn | 0.30 - 0.50 |
| Mắt lim dim | 0.20 - 0.29 |
| Mắt nhắm | < 0.20 |

## Mã nguồn tính toán EAR

```python
def calculate_ear(eye_landmarks):
    """
    Tính Eye Aspect Ratio cho một mắt.
    
    Tham số:
        eye_landmarks: Danh sách các điểm mốc của mắt [p1, p2, p3, p4, p5, p6]
    
    Trả về:
        Giá trị EAR
    """
    # Tính khoảng cách dọc giữa các điểm mốc
    A = distance(eye_landmarks[1], eye_landmarks[5])  # p2-p6
    B = distance(eye_landmarks[2], eye_landmarks[4])  # p3-p5
    
    # Tính khoảng cách ngang
    C = distance(eye_landmarks[0], eye_landmarks[3])  # p1-p4
    
    # Tính EAR
    ear = (A + B) / (2.0 * C) if C > 0 else 0.0
    
    return ear

def distance(point1, point2):
    """Tính khoảng cách Euclidean giữa hai điểm."""
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def detect_eye_state(ear, threshold=0.2, consecutive_frames=3):
    """
    Phát hiện trạng thái mắt dựa trên giá trị EAR.
    
    Tham số:
        ear: Giá trị Eye Aspect Ratio
        threshold: Ngưỡng để xác định mắt nhắm
        consecutive_frames: Số khung hình liên tiếp cần xác nhận
    
    Trả về:
        "CLOSED" nếu mắt nhắm, "OPEN" nếu mắt mở
    """
    if ear < threshold:
        return "CLOSED"
    else:
        return "OPEN"
```

## Ứng dụng EAR trong phát hiện buồn ngủ

Phát hiện buồn ngủ được thực hiện bằng cách theo dõi giá trị EAR qua thời gian:

1. Nếu giá trị EAR dưới ngưỡng (thường là 0.2) trong một khoảng thời gian đủ dài (thường là 20-30 khung hình, tương đương khoảng 1 giây), người lái xe được xác định là đang buồn ngủ.

2. Tỷ lệ PERCLOS (PERcentage of eyelid CLOSure) được tính bằng phần trăm thời gian mắt nhắm trong một khoảng thời gian nhất định. Nếu PERCLOS > 20%, người lái xe được coi là đang trong trạng thái buồn ngủ.

```python
# Ví dụ: Phát hiện buồn ngủ
if eye_closed_frames > EYE_AR_CONSEC_FRAMES:
    # Người lái xe được xác định là buồn ngủ
    drowsy_state = True
    # Kích hoạt hệ thống cảnh báo
    alert_system.trigger("drowsy")
```
