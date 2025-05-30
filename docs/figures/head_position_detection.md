## Minh họa phát hiện vị trí đầu

### Phát hiện góc nghiêng (Roll angle)

```
        LEFT_EYE            RIGHT_EYE
           ●                    ●
         /   \                /   \
        ●     ●              ●     ●
         \   /                \   /
           ●                    ●
           
eye_line_vector = RIGHT_EYE_CENTER - LEFT_EYE_CENTER
angle_rad = arctan2(eye_line_vector[1], eye_line_vector[0])
angle_deg = angle_rad × (180/π)
```

### Phát hiện góc quay ngang (Yaw angle)

```
             NOSE_TIP
                ●
               /|\
              / | \
             /  |  \
        ● ───┼───┼─── ●
    LEFT_EYE |   |   RIGHT_EYE
             |   |
             |   |
    midpoint_x = (LEFT_EYE[0] + RIGHT_EYE[0])/2
    nose_deviation = (NOSE_TIP[0] - midpoint_x) / face_width
```

### Giá trị ngưỡng phát hiện

```
- Đầu nghiêng: |angle_deg| > 20°
- Đầu quay ngang: |nose_deviation| > 0.15
```
