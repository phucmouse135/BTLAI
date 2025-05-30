## Phân tích và Mô tả Dữ liệu

### Phân bố số lượng mẫu dữ liệu

```
                             Phân bố dữ liệu thu thập
                             ┌────────────────────────┐
4,000 ┤                      █                        │
      │                      █                        │
3,500 ┤                      █                        │
      │                      █                        │
3,000 ┤                      █         █     █        │
      │                      █         █     █        │
2,500 ┤                      █         █     █        │
      │                      █         █     █        │
2,000 ┤                      █         █     █        │
      │                      █         █     █        │
1,500 ┤                      █         █     █        │
      │                      █         █     █        │
1,000 ┤                      █         █     █        │
      │                      █         █     █        │
  500 ┤                      █         █     █        │
      │                      █         █     █        │
    0 ┼──────────────────────█─────────█─────█────────┤
       Tỉnh táo       Buồn ngủ      Đầu    Tay/Điện thoại
                                    quay
```

### Phân tích giá trị EAR

| Trạng thái | EAR min | EAR max | EAR trung bình | Độ lệch chuẩn |
|------------|---------|---------|----------------|---------------|
| Mắt mở     | 0.25    | 0.35    | 0.30           | 0.03          |
| Mắt nhắm   | 0.10    | 0.19    | 0.15           | 0.05          |
| Mắt lim dim| 0.20    | 0.24    | 0.22           | 0.02          |

### Phân tích góc nghiêng đầu

| Vị trí đầu | Góc nghiêng min | Góc nghiêng max | Độ lệch mũi min | Độ lệch mũi max |
|------------|----------------|-----------------|----------------|-----------------|
| Thẳng      | -10°           | +10°            | -0.05          | +0.05           |
| Nghiêng    | -35°           | +35°            | -0.10          | +0.10           |
| Quay ngang | -15°           | +15°            | -0.30          | +0.30           |

### Phân tích thời gian phát hiện

Thời gian phản hồi trung bình của hệ thống:
- Phát hiện buồn ngủ: 125ms (±15ms)
- Phát hiện mất tập trung do đầu: 110ms (±10ms)
- Phát hiện mất tập trung do tay: 135ms (±20ms)

Thời gian phát hiện phụ thuộc đáng kể vào điều kiện ánh sáng, với thời gian phản hồi tăng khoảng 30% trong điều kiện ánh sáng yếu.

### Ma trận nhầm lẫn (Confusion Matrix)

**Ma trận nhầm lẫn cho phát hiện buồn ngủ:**

```
                         ┌────────────────────────────────────────┐
                         │        DỰ ĐOÁN                         │
                         │    Tỉnh táo      Buồn ngủ             │
         ┌───────────────┼─────────────────────────────────────────
         │  Tỉnh táo     │     94.2%          5.8%              │
THỰC TẾ  │               │                                      │
         │  Buồn ngủ     │     9.2%           90.8%             │
         └───────────────┴─────────────────────────────────────────
```

**Ma trận nhầm lẫn cho phát hiện mất tập trung do đầu:**

```
                         ┌────────────────────────────────────────┐
                         │        DỰ ĐOÁN                         │
                         │    Tập trung      Mất tập trung       │
         ┌───────────────┼─────────────────────────────────────────
         │  Tập trung    │     96.5%          3.5%              │
THỰC TẾ  │               │                                      │
         │Mất tập trung  │     8.2%           91.8%             │
         └───────────────┴─────────────────────────────────────────
```

**Ma trận nhầm lẫn cho phát hiện mất tập trung do tay:**

```
                         ┌────────────────────────────────────────┐
                         │        DỰ ĐOÁN                         │
                         │    Tập trung      Mất tập trung       │
         ┌───────────────┼─────────────────────────────────────────
         │  Tập trung    │     93.2%          6.8%              │
THỰC TẾ  │               │                                      │
         │Mất tập trung  │     15.3%          84.7%             │
         └───────────────┴─────────────────────────────────────────
```

### Phân tích đường cong ROC (ROC Curve)

```
    1.0 ┼─────────────╮───────────────────────
        │      ╱╲     │
        │     /  ╲    │
        │    /    ╲   │
    0.8 ┤   /      ╲  │
        │  /        ╲ │
TPR     │ /          ╲│
        │/            ╲
    0.6 ┤              ╲
        │              │
        │              │
        │              │
    0.4 ┤              │
        │              │
        │              │
        │              │
    0.2 ┤              │
        │              │
        │              │
        │              │
    0.0 ┼──────────────┴───────────────────────
        0.0   0.2   0.4   0.6   0.8   1.0
                     FPR

     — Buồn ngủ (AUC=0.93)
     — Mất tập trung do đầu (AUC=0.94)
     — Mất tập trung do tay (AUC=0.89)
```

Chú thích:
- TPR: True Positive Rate (Độ nhạy)
- FPR: False Positive Rate (1 - Độ đặc hiệu)
- AUC: Area Under the Curve (Diện tích dưới đường cong)
