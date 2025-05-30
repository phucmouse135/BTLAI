## Minh họa các phương pháp làm mịn dữ liệu

### Ví dụ về bộ lọc trung bình trượt cho dữ liệu EAR

```
Dữ liệu EAR gốc: [0.31, 0.30, 0.15, 0.14, 0.29, 0.30, 0.31, 0.32, 0.15, 0.16, 0.30, 0.31]

Kích thước cửa sổ N = 5:

EAR_smoothed(5) = (0.31 + 0.30 + 0.15 + 0.14 + 0.29) / 5 = 0.238
EAR_smoothed(6) = (0.30 + 0.15 + 0.14 + 0.29 + 0.30) / 5 = 0.236
EAR_smoothed(7) = (0.15 + 0.14 + 0.29 + 0.30 + 0.31) / 5 = 0.238
...
```

Kết quả sau khi làm mịn:
```
      ┌────────────────────────────────────────────┐
 0.35 ┤            ╭╮                       ╭╮     │
      │            ││                       ││     │
 0.30 ┤╭╮          ││                       ││     │
      │││          ││          ╭───╮        ││     │
 0.25 ┤││          ││         ╭╯   ╰╮       ││     │
      │││         ╭╯│         │     │       ││     │
 0.20 ┤││        ╭╯ │         │     │      ╭╯│     │
      │││        │  │         │     │     ╭╯ │     │
 0.15 ┤││        │  ╰╮        │     ╰╮   ╭╯  ╰╮    │
      │╰╯        │   ╰╮       │      ╰───╯    │    │
 0.10 ┤          │    ╰───────╯              ╰╮    │
      │          │                            │    │
 0.05 ┤          │                            │    │
      │          │                            │    │
 0.00 ┼──────────┴────────────────────────────┴────┤
       0  1  2  3  4  5  6  7  8  9 10 11 12 13 14

   — Dữ liệu gốc   --- Dữ liệu làm mịn
```

### Ví dụ về ứng dụng kỹ thuật Hysteresis

```
Ngưỡng EAR cơ bản = 0.20
Biên độ hysteresis = 0.02

Ngưỡng để chuyển từ tỉnh táo sang cảnh báo = 0.20 - 0.02 = 0.18
Ngưỡng để chuyển từ cảnh báo sang tỉnh táo = 0.20 + 0.02 = 0.22

Ví dụ trạng thái hiện tại là "Tỉnh táo":
- Nếu EAR < 0.18, chuyển sang "Cảnh báo"
- Nếu EAR ≥ 0.18, giữ nguyên "Tỉnh táo"

Ví dụ trạng thái hiện tại là "Cảnh báo":
- Nếu EAR > 0.22, chuyển sang "Tỉnh táo"
- Nếu EAR ≤ 0.22, giữ nguyên "Cảnh báo"
```

### Ví dụ về bộ lọc Kalman

Áp dụng bộ lọc Kalman một chiều để làm mịn dữ liệu góc nghiêng đầu:

```
Giả sử:
- x: góc nghiêng đầu
- A = 1 (ma trận chuyển trạng thái)
- H = 1 (ma trận đo lường)
- Q = 0.01 (độ nhiễu quá trình)
- R = 0.1 (độ nhiễu đo lường)
- P = 1 (ước tính ban đầu về độ không chắc chắn)

Vòng lặp Kalman:
1. Dự đoán:
   x̂_k|k-1 = A × x̂_k-1|k-1
   P_k|k-1 = A × P_k-1|k-1 × A + Q

2. Cập nhật:
   K_k = P_k|k-1 × H / (H × P_k|k-1 × H + R)
   x̂_k|k = x̂_k|k-1 + K_k × (z_k - H × x̂_k|k-1)
   P_k|k = (1 - K_k × H) × P_k|k-1
```
