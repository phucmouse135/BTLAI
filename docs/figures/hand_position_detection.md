## Minh họa phát hiện vị trí tay trên vô lăng

### Mô hình vùng vô lăng

```
                      |
                      |
                      |
          Wheel       |
         Center       |
           ⊙         |
          /|\         |
    Wheel | | Wheel   |
    Radius| | Radius  |
          \|/         |
        ___|___       |
       /       \      |
      /         \     |
     |           |    |
     |           |    |
      \         /     |
       \_______/      |
                      |
```

### Tính toán khoảng cách tay đến vô lăng

```
distance = √[(wrist_x - wheel_center_x)² + (wrist_y - wheel_center_y)²]

Nếu distance ≤ wheel_radius thì tay được xác định là đang ở trên vô lăng.
```

### Phát hiện cầm điện thoại

```
                 thumb_tip
                    ●
                   /
                  /
       ●─────────●─────●  index_tip
      /         wrist   \
     ●                   ●
    /                     \
   ●                       ●
                 
finger_spread = σ(finger_tip_coordinates)
tight_grip = mean(finger_spread) < threshold
pinch_distance = ||thumb_tip - index_tip||
pinch_detected = pinch_distance < threshold
```
