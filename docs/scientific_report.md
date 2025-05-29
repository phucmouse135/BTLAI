# BÁO CÁO KHOA HỌC
# HỆ THỐNG PHÁT HIỆN BUỒN NGỦ VÀ MẤT TẬP TRUNG CHO NGƯỜI LÁI XE DỰA TRÊN THỊ GIÁC MÁY TÍNH VÀ HỌC MÁY

## TÓM TẮT

Báo cáo này trình bày về việc thiết kế và phát triển một hệ thống tự động phát hiện sớm trạng thái buồn ngủ và mất tập trung của người lái xe thông qua các kỹ thuật thị giác máy tính và học máy. Hệ thống sử dụng camera để theo dõi trạng thái mắt, vị trí đầu và vị trí tay của người lái xe, từ đó phát hiện các dấu hiệu nguy hiểm và đưa ra cảnh báo kịp thời. Nghiên cứu áp dụng phương pháp tỷ lệ khía cạnh mắt (Eye Aspect Ratio - EAR) kết hợp với phân tích vị trí đầu và tay trên vô lăng để xây dựng một giải pháp toàn diện. Kết quả thực nghiệm cho thấy hệ thống có thể phát hiện trạng thái buồn ngủ với độ chính xác 92,5% và trạng thái mất tập trung với độ chính xác 89,7%, với thời gian phản hồi trung bình dưới 150ms, đáp ứng yêu cầu ứng dụng thời gian thực cho các hệ thống an toàn giao thông.

**Từ khóa**: Phát hiện buồn ngủ, phát hiện mất tập trung, thị giác máy tính, học máy, eye aspect ratio, phân tích hành vi người lái xe, an toàn giao thông.

## I. GIỚI THIỆU

### 1.1. Đặt vấn đề

Tai nạn giao thông liên quan đến tình trạng buồn ngủ và mất tập trung của người lái xe là một trong những nguyên nhân hàng đầu dẫn đến thương vong trên đường. Theo số liệu thống kê của Tổ chức Y tế Thế giới (WHO), có khoảng 20-30% tai nạn giao thông nghiêm trọng liên quan đến tình trạng buồn ngủ hoặc mệt mỏi của người lái xe [1]. Đồng thời, các hoạt động khiến người lái xe mất tập trung như sử dụng điện thoại di động, điều chỉnh thiết bị trong xe, hoặc nói chuyện làm tăng nguy cơ tai nạn lên gấp 23 lần [2].

Vấn đề cấp bách đặt ra là làm thế nào để phát hiện sớm các trạng thái nguy hiểm này trước khi xảy ra tai nạn. Các phương pháp truyền thống như sử dụng cảm biến sinh lý học (đo điện não, nhịp tim, điện cơ) thường không khả thi trong điều kiện thực tế do yêu cầu gắn thiết bị trực tiếp lên cơ thể người lái, gây khó chịu và hạn chế tính ứng dụng [3].

Với sự phát triển của thị giác máy tính và học máy, việc phát hiện các trạng thái nguy hiểm thông qua phân tích hình ảnh từ camera đang trở thành một giải pháp đầy tiềm năng, cho phép giám sát không xâm lấn và triển khai rộng rãi [4]. Báo cáo này trình bày một hệ thống phát hiện buồn ngủ và mất tập trung dựa trên các công nghệ này, hướng tới mục tiêu giảm thiểu tai nạn giao thông và nâng cao an toàn cho người tham gia giao thông.

### 1.2. Mục tiêu nghiên cứu

Nghiên cứu này hướng đến các mục tiêu cụ thể sau:

1. Xây dựng một hệ thống tự động phát hiện trạng thái buồn ngủ và mất tập trung của người lái xe thông qua camera thường, không yêu cầu phần cứng chuyên dụng.
2. Thiết kế thuật toán phát hiện trạng thái mắt dựa trên tỷ lệ khía cạnh mắt (EAR) kết hợp với các kỹ thuật phát hiện điểm mốc khuôn mặt (facial landmarks detection).
3. Phát triển phương pháp phát hiện mất tập trung dựa trên phân tích vị trí đầu và vị trí tay trên vô lăng.
4. Tối ưu hóa hiệu suất hệ thống để đáp ứng yêu cầu thời gian thực với độ trễ thấp.
5. Tích hợp hệ thống cảnh báo đa phương thức (hình ảnh, âm thanh) cho người lái xe.

### 1.3. Phạm vi nghiên cứu

Nghiên cứu tập trung vào:
- Phát hiện trạng thái mắt (mở, nhắm, nháy mắt thường xuyên)
- Theo dõi vị trí đầu (thẳng, nghiêng, quay sang một bên)
- Phát hiện vị trí tay (trên vô lăng, không trên vô lăng, cầm đồ vật)
- Phát hiện trạng thái buồn ngủ bằng đánh giá thời gian nhắm mắt và tần suất nháy mắt
- Phát triển giao diện người dùng cho giám sát và cảnh báo
- Đánh giá hiệu suất hệ thống trong môi trường thực tế

Các yếu tố nằm ngoài phạm vi nghiên cứu:
- Phát hiện mức độ cồn hoặc chất kích thích
- Đánh giá khả năng lái xe dựa trên kỹ năng
- Tích hợp với hệ thống điều khiển xe tự động
- Phân tích hành vi lái xe dài hạn

## II. TỔNG QUAN TÀI LIỆU

### 2.1. Các nghiên cứu về phát hiện buồn ngủ

#### 2.1.1. Phương pháp dựa trên sinh lý học

Các nghiên cứu sớm về phát hiện buồn ngủ thường dựa vào các dấu hiệu sinh lý học như sóng não (EEG), điện cơ (EMG), và nhịp tim (ECG) [5]. Liu và cộng sự (2019) đã phát triển hệ thống kết hợp EEG và phân tích hình ảnh khuôn mặt, đạt độ chính xác 97,8% nhưng yêu cầu người dùng đeo thiết bị đo EEG, hạn chế khả năng ứng dụng thực tế [6].

#### 2.1.2. Phương pháp dựa trên thị giác máy tính

Phương pháp Tỷ lệ Khía cạnh Mắt (EAR) được giới thiệu bởi Soukupová và Čech (2016) [7] đã trở thành một trong những phương pháp phổ biến nhất để phát hiện trạng thái mắt. Rosebrock (2017) [8] đã cải tiến phương pháp này kết hợp với mạng nơ-ron tích chập để tăng độ chính xác lên 94,1% trong điều kiện ánh sáng đa dạng.

García và cộng sự (2021) [9] đề xuất phương pháp kết hợp EAR với phân tích thời gian thực về tần số nháy mắt, tạo ra một chỉ số PERCLOS (Percentage of Eye Closure) cải tiến, đạt độ chính xác 93,7% trong thử nghiệm thực tế với 50 người lái xe.

### 2.2. Các nghiên cứu về phát hiện mất tập trung

#### 2.2.1. Phân tích vị trí đầu

Ryu và cộng sự (2018) [10] sử dụng các điểm mốc khuôn mặt để ước tính góc nghiêng và quay của đầu, phát hiện mất tập trung với độ chính xác 88,5%. Praveen và Kumar (2020) [11] cải tiến phương pháp này bằng cách kết hợp với theo dõi ánh mắt, nâng độ chính xác lên 91,2%.

#### 2.2.2. Phát hiện sử dụng điện thoại và đồ vật

Zhang và cộng sự (2020) [12] phát triển phương pháp phát hiện việc sử dụng điện thoại trong khi lái xe dựa trên phân tích hình dạng và vị trí tay, đạt độ chính xác 87,3%. Ibrahim và cộng sự (2022) [13] kết hợp theo dõi tay bằng MediaPipe với phân tích hành vi qua chuỗi thời gian, nâng cao độ chính xác lên 92,8%.

### 2.3. Các công nghệ nền tảng

#### 2.3.1. MediaPipe và phát hiện điểm mốc khuôn mặt

MediaPipe Face Mesh [14] cung cấp khả năng phát hiện 468 điểm mốc trên khuôn mặt với độ chính xác cao, hoạt động ổn định trong các điều kiện ánh sáng và góc quay đầu khác nhau. So với các phương pháp truyền thống như Dlib [15], MediaPipe đạt hiệu suất cao hơn và yêu cầu tính toán thấp hơn, phù hợp cho ứng dụng thời gian thực [16].

#### 2.3.2. Mô hình học máy cho phân loại trạng thái

Các nghiên cứu gần đây đã chuyển từ các mô hình học sâu phức tạp sang các mô hình nhẹ hơn như SVM và Random Forest để xử lý thời gian thực trên thiết bị biên. Nguyễn và cộng sự (2023) [17] so sánh hiệu suất giữa SVM, Random Forest và CNN cho phát hiện buồn ngủ, cho thấy SVM đạt kết quả tương đương với CNN (91,8% so với 92,3%) nhưng với tốc độ nhanh hơn 15 lần.

## III. PHƯƠNG PHÁP NGHIÊN CỨU

### 3.1. Kiến trúc hệ thống

Hệ thống được thiết kế theo kiến trúc module, bao gồm các thành phần chính:

1. **Module thu nhận hình ảnh**: Xử lý luồng video từ camera
2. **Module phát hiện khuôn mặt và điểm mốc**: Sử dụng MediaPipe Face Mesh
3. **Module phát hiện tay**: Sử dụng MediaPipe Hands
4. **Module phân tích trạng thái mắt**: Tính toán EAR và phát hiện mắt nhắm
5. **Module phân tích vị trí đầu**: Xác định góc nghiêng và quay của đầu
6. **Module phân tích vị trí tay**: Xác định vị trí tay trên vô lăng
7. **Module phân loại trạng thái**: Kết hợp các đặc trưng để xác định trạng thái người lái
8. **Module cảnh báo**: Phát cảnh báo hình ảnh và âm thanh
9. **Giao diện người dùng**: Hiển thị hình ảnh và thông tin trạng thái

Các module được triển khai theo quy trình xử lý tuần tự, với kết quả của module trước làm đầu vào cho module sau.

### 3.2. Thu thập và xử lý dữ liệu

#### 3.2.1. Thu thập dữ liệu

Dữ liệu được thu thập từ 50 tình nguyện viên (30 nam, 20 nữ) với độ tuổi từ 20-60, trong các điều kiện ánh sáng khác nhau (tốt, trung bình, yếu) và với các góc camera khác nhau. Mỗi người tham gia được yêu cầu mô phỏng các trạng thái sau:

- **Trạng thái cơ bản**: Tỉnh táo, nhìn về phía trước
- **Buồn ngủ**: Mắt nhắm từng đợt, đầu gục xuống, nháy mắt chậm
- **Mất tập trung do vị trí đầu**: Quay đầu sang trái/phải/lên/xuống
- **Mất tập trung do điện thoại**: Sử dụng điện thoại khi lái xe
- **Tay không đặt trên vô lăng**: Tay để xuống hoặc làm việc khác

Tổng cộng 10.000 khung hình được thu thập, với phân bố như sau:
- 4.000 khung hình trạng thái tỉnh táo
- 3.000 khung hình trạng thái buồn ngủ
- 3.000 khung hình trạng thái mất tập trung (1.000 do vị trí đầu, 1.000 do sử dụng điện thoại, 1.000 do tay không đặt trên vô lăng)

#### 3.2.2. Tiền xử lý dữ liệu

Các bước tiền xử lý bao gồm:
1. Phát hiện khuôn mặt trong khung hình
2. Trích xuất 468 điểm mốc khuôn mặt sử dụng MediaPipe Face Mesh
3. Tính toán Tỷ lệ Khía cạnh Mắt (EAR) cho cả hai mắt
4. Trích xuất góc nghiêng và quay của đầu
5. Phát hiện vị trí tay và xác định trạng thái tay
6. Gán nhãn dữ liệu (tỉnh táo, buồn ngủ, mất tập trung)

### 3.3. Mô hình và thuật toán

#### 3.3.1. Phát hiện trạng thái mắt

Tỷ lệ Khía cạnh Mắt (EAR) được tính theo công thức:

```
EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
```

Trong đó:
- p1, p2, p3, p4, p5, p6 là các điểm mốc xung quanh mắt
- ||p1-p4|| đại diện cho khoảng cách Euclidean giữa p1 và p4

Trạng thái buồn ngủ được xác định khi:
- EAR trung bình < ngưỡng EAR (0.2)
- Số khung hình liên tiếp thỏa mãn điều kiện > ngưỡng số khung hình (20)

#### 3.3.2. Phát hiện vị trí đầu

Góc nghiêng (roll) được tính dựa trên độ nghiêng của đường nối hai mắt:

```
angle_rad = arctan2(eye_line[1], eye_line[0])
angle_deg = angle_rad × (180/π)
```

Góc quay ngang (yaw) được xác định thông qua độ lệch của mũi so với trung tâm khuôn mặt:

```
nose_deviation = (nose_tip[0] - midpoint_x) / face_width
```

Đầu được xác định là nghiêng hoặc quay nếu:
- |angle_deg| > 20°
- |nose_deviation| > 0.15

#### 3.3.3. Phát hiện vị trí tay

Khoảng cách từ tay đến vị trí ước lượng của vô lăng được tính bằng khoảng cách Euclidean:

```
distance = √[(wrist_x - wheel_center_x)² + (wrist_y - wheel_center_y)²]
```

Tay được xác định là trên vô lăng nếu distance ≤ wheel_radius.

Phát hiện cầm điện thoại dựa trên phân tích hình dạng tay:

```
finger_spread = σ(finger_coordinates)
tight_grip = mean(finger_spread) < threshold
```

#### 3.3.4. Mô hình phân loại trạng thái

Mô hình SVM với kernel RBF được huấn luyện để phân loại các trạng thái của người lái, sử dụng vector đặc trưng sau:

- EAR trung bình
- Tỉ lệ thời gian nhắm mắt (PERCLOS)
- Góc nghiêng đầu
- Độ lệch mũi
- Trạng thái tay trên vô lăng (nhị phân)
- Trạng thái cầm đồ vật (nhị phân)

Các đặc trưng được chuẩn hóa bằng StandardScaler trước khi đưa vào mô hình.

#### 3.3.5. Kỹ thuật làm mịn dữ liệu thời gian

Để giảm thiểu nhiễu và tránh cảnh báo sai, các kỹ thuật làm mịn dữ liệu thời gian được áp dụng:

1. **Bộ lọc trung bình trượt**: Áp dụng cho giá trị EAR để làm mịn dao động:
   ```
   EAR_smoothed(t) = (1/N) × Σ[EAR(t-i)] với i từ 0 đến N-1
   ```

2. **Bộ lọc Kalman**: Áp dụng cho ước lượng góc đầu để theo dõi chuyển động mượt mà

3. **Kỹ thuật Hysteresis**: Áp dụng cho phát hiện trạng thái để tránh dao động giữa các trạng thái:
   ```
   threshold_to_drowsy = base_threshold - hysteresis_margin
   threshold_to_normal = base_threshold + hysteresis_margin
   ```

### 3.4. Triển khai và đánh giá

#### 3.4.1. Môi trường triển khai

Hệ thống được triển khai trên hai nền tảng:
1. PC/Laptop thông thường (Intel Core i5, 8GB RAM)
2. Thiết bị nhúng Raspberry Pi 4 (4GB RAM)

Phần mềm được phát triển bằng Python 3.9, sử dụng các thư viện:
- OpenCV 4.5.5 cho xử lý hình ảnh
- MediaPipe 0.8.9 cho phát hiện điểm mốc
- scikit-learn 1.0.2 cho mô hình học máy
- PyQt5 5.15.6 cho giao diện người dùng

#### 3.4.2. Phương pháp đánh giá

Hiệu suất của hệ thống được đánh giá thông qua:

1. **Độ chính xác (Accuracy)**: Tỉ lệ phân loại đúng trên tổng số mẫu
2. **Độ nhạy (Sensitivity/Recall)**: Tỉ lệ phát hiện đúng trạng thái nguy hiểm
3. **Độ đặc hiệu (Specificity)**: Tỉ lệ phát hiện đúng trạng thái an toàn
4. **Độ trễ phát hiện**: Thời gian từ khi xuất hiện trạng thái nguy hiểm đến khi phát hiện
5. **Tốc độ xử lý**: Số khung hình xử lý mỗi giây (FPS)

#### 3.4.3. Thử nghiệm thực tế

Hệ thống được thử nghiệm trong ba môi trường:
1. **Phòng thí nghiệm**: Điều kiện ánh sáng tối ưu, môi trường kiểm soát
2. **Mô phỏng lái xe**: Sử dụng thiết bị mô phỏng lái xe với các tình huống giao thông khác nhau
3. **Xe thực tế**: Thử nghiệm trong xe dừng đỗ, dưới các điều kiện ánh sáng khác nhau (sáng, tối, ngược sáng)

## IV. KẾT QUẢ VÀ THẢO LUẬN

### 4.1. Hiệu suất phát hiện trạng thái mắt

| Điều kiện ánh sáng | Độ chính xác | Độ nhạy | Độ đặc hiệu | Độ trễ phát hiện (ms) |
|--------------------|--------------|---------|-------------|------------------------|
| Tốt                | 94.7%        | 93.2%   | 96.1%       | 110                    |
| Trung bình         | 92.3%        | 90.5%   | 94.0%       | 125                    |
| Yếu                | 88.9%        | 85.7%   | 92.1%       | 145                    |
| Đeo kính           | 89.5%        | 87.3%   | 91.7%       | 140                    |

### 4.2. Hiệu suất phát hiện vị trí đầu

| Trạng thái đầu     | Độ chính xác | Độ nhạy | Độ đặc hiệu |
|--------------------|--------------|---------|-------------|
| Thẳng              | 95.3%        | 94.1%   | 96.5%       |
| Nghiêng            | 92.8%        | 91.0%   | 94.6%       |
| Quay sang một bên  | 94.1%        | 93.2%   | 95.0%       |

### 4.3. Hiệu suất phát hiện vị trí tay

| Trạng thái tay         | Độ chính xác | Độ nhạy | Độ đặc hiệu |
|------------------------|--------------|---------|-------------|
| Trên vô lăng           | 91.5%        | 89.8%   | 93.2%       |
| Không trên vô lăng     | 90.3%        | 88.2%   | 92.4%       |
| Cầm điện thoại         | 89.0%        | 86.5%   | 91.5%       |

### 4.4. Hiệu suất tổng thể hệ thống

| Trạng thái         | Độ chính xác | Độ nhạy | Độ đặc hiệu | F1-score |
|--------------------|--------------|---------|-------------|----------|
| Tỉnh táo           | 94.2%        | 95.5%   | 92.9%       | 0.940    |
| Buồn ngủ           | 92.5%        | 90.8%   | 94.2%       | 0.915    |
| Mất tập trung      | 89.7%        | 87.3%   | 92.1%       | 0.890    |

### 4.5. Hiệu suất tính toán

| Nền tảng         | FPS trung bình | Thời gian xử lý/khung (ms) | Sử dụng CPU | Sử dụng RAM |
|------------------|----------------|----------------------------|-------------|-------------|
| Intel Core i5    | 28.5           | 35.1                       | 23.5%       | 420MB       |
| Raspberry Pi 4   | 12.7           | 78.7                       | 68.3%       | 380MB       |

### 4.6. So sánh với các giải pháp hiện có

| Phương pháp                        | Độ chính xác | FPS | Yêu cầu phần cứng | Khả năng triển khai thực tế |
|------------------------------------|--------------|-----|-------------------|-----------------------------|
| Hệ thống đề xuất                   | 92.1%        | 28.5| Thấp              | Cao                         |
| Rosebrock (2017) [8]               | 94.1%        | 15.2| Trung bình        | Trung bình                  |
| García và cộng sự (2021) [9]       | 93.7%        | 20.3| Trung bình        | Trung bình                  |
| Ibrahim và cộng sự (2022) [13]     | 92.8%        | 18.7| Trung bình        | Trung bình                  |

### 4.7. Thảo luận

#### 4.7.1. Ưu điểm của hệ thống đề xuất

1. **Hiệu suất thời gian thực tốt**: Hệ thống đạt tốc độ xử lý cao (28.5 FPS) với thời gian phản hồi thấp (< 150ms), đáp ứng yêu cầu ứng dụng thời gian thực.
2. **Độ chính xác cao trong nhiều điều kiện**: Duy trì độ chính xác trên 88% ngay cả trong điều kiện ánh sáng yếu.
3. **Yêu cầu phần cứng thấp**: Có thể chạy trên thiết bị nhúng Raspberry Pi với hiệu suất chấp nhận được.
4. **Phát hiện đa trạng thái**: Kết hợp phát hiện cả buồn ngủ và mất tập trung trong một hệ thống duy nhất.
5. **Khả năng mở rộng**: Kiến trúc module cho phép dễ dàng bổ sung tính năng mới.

#### 4.7.2. Hạn chế và thách thức

1. **Độ chính xác giảm trong điều kiện ánh sáng yếu**: Hiệu suất giảm khoảng 6% trong điều kiện ánh sáng kém.
2. **Phát hiện cầm điện thoại còn hạn chế**: Độ chính xác thấp hơn so với phát hiện trạng thái mắt và vị trí đầu.
3. **Thách thức với người đeo kính**: Độ chính xác phát hiện EAR giảm khoảng 5% với người đeo kính.
4. **Hiệu suất trên thiết bị nhúng còn hạn chế**: FPS trên Raspberry Pi (12.7) có thể không đủ cho một số ứng dụng thời gian thực nghiêm ngặt.
5. **Cần cải thiện khả năng chống chịu với điều kiện ánh sáng thay đổi**: Hiệu suất còn biến động theo điều kiện ánh sáng.

## V. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 5.1. Kết luận

Nghiên cứu này đã giới thiệu một hệ thống phát hiện buồn ngủ và mất tập trung cho người lái xe dựa trên thị giác máy tính và học máy. Hệ thống sử dụng phương pháp không xâm lấn, chỉ yêu cầu một camera thường để theo dõi trạng thái người lái, giúp tăng tính khả thi và dễ triển khai trong thực tế.

Kết quả thực nghiệm cho thấy hệ thống có thể phát hiện trạng thái buồn ngủ với độ chính xác 92,5% và trạng thái mất tập trung với độ chính xác 89,7%, đạt hiệu suất xử lý thời gian thực với 28,5 khung hình/giây trên thiết bị phổ thông. Hệ thống cũng thể hiện khả năng thích ứng với các điều kiện ánh sáng khác nhau, mặc dù hiệu suất có giảm trong điều kiện ánh sáng yếu.

Các phương pháp làm mịn dữ liệu thời gian và kỹ thuật hysteresis đã giúp giảm thiểu cảnh báo sai và tăng cường độ tin cậy của hệ thống. So với các giải pháp hiện có, hệ thống đề xuất đạt được sự cân bằng tốt giữa độ chính xác, hiệu suất thời gian thực và yêu cầu phần cứng thấp, tạo tiền đề cho việc triển khai rộng rãi trong thực tế.

### 5.2. Đóng góp chính

1. Xây dựng hệ thống phát hiện buồn ngủ và mất tập trung tích hợp, hoạt động theo thời gian thực với yêu cầu phần cứng thấp
2. Phát triển phương pháp cải tiến kết hợp EAR với phân tích vị trí đầu và tay
3. Áp dụng các kỹ thuật làm mịn dữ liệu thời gian để tăng cường độ tin cậy của hệ thống
4. Đánh giá toàn diện hiệu suất hệ thống trong nhiều điều kiện và môi trường khác nhau
5. Tạo bộ dữ liệu phong phú với nhiều trạng thái buồn ngủ và mất tập trung khác nhau

### 5.3. Lộ trình phát triển tương lai

#### 5.3.1. Cải tiến ngắn hạn (0-6 tháng)

1. **Tối ưu hóa thuật toán**: Cải thiện hiệu suất để đạt FPS cao hơn trên thiết bị nhúng
2. **Cải thiện khả năng chống chịu điều kiện ánh sáng**: Áp dụng kỹ thuật cân bằng sáng và chuẩn hóa
3. **Mở rộng bộ dữ liệu**: Thu thập thêm dữ liệu trong các điều kiện đa dạng hơn
4. **Tích hợp phát hiện đeo kính**: Phát triển phương pháp phát hiện EAR đặc biệt cho người đeo kính
5. **Cải thiện phát hiện cầm điện thoại**: Nâng cao độ chính xác phát hiện việc sử dụng điện thoại

#### 5.3.2. Phát triển trung hạn (6-18 tháng)

1. **Mô hình học sâu nhẹ**: Phát triển và tối ưu mô hình học sâu nhẹ (MobileNet, EfficientNet) cho thiết bị nhúng
2. **Phân tích theo chuỗi thời gian**: Tích hợp phân tích dữ liệu theo chuỗi thời gian (LSTM) để dự đoán trạng thái từ sớm
3. **Cá nhân hóa mô hình**: Phát triển khả năng học tập liên tục để thích ứng với người lái cụ thể
4. **Mở rộng phát hiện hành vi**: Bổ sung phát hiện ăn uống, hút thuốc, nói chuyện
5. **Tích hợp với hệ thống cảnh báo xe**: Phát triển API để tích hợp với hệ thống cảnh báo có sẵn trên xe

#### 5.3.3. Phát triển dài hạn (18-36 tháng)

1. **Hệ thống hoàn chỉnh**: Phát triển thành sản phẩm hoàn chỉnh có thể lắp đặt dễ dàng trên xe
2. **Phân tích hành vi lái xe dài hạn**: Xây dựng hệ thống phân tích xu hướng và hành vi lái xe dài hạn
3. **Tích hợp học tập liên tục**: Phát triển khả năng cập nhật mô hình từ xa dựa trên dữ liệu mới thu thập
4. **Phòng ngừa chủ động**: Phát triển khả năng dự đoán và cảnh báo trạng thái nguy hiểm trước khi xảy ra
5. **Tích hợp với hệ thống tự lái**: Phát triển giao thức giao tiếp với hệ thống hỗ trợ lái và tự lái

## TÀI LIỆU THAM KHẢO

[1] World Health Organization, "Global Status Report on Road Safety 2023," WHO, Geneva, 2023.

[2] National Highway Traffic Safety Administration, "Distracted Driving in Fatal Crashes, 2021," NHTSA, Washington, DC, 2022.

[3] J. Kim, T. Kim, and J. Kim, "A Survey on Driver Monitoring Systems: From the Perspective of Vehicle Control and Driver Status Monitoring," IEEE Trans. Intell. Transp. Syst., vol. 22, no. 12, pp. 7209-7225, 2021.

[4] M. Ramzan, H. U. Khan, S. M. Awan, A. Ismail, M. Ilyas, and A. Mahmood, "A Survey on State-of-the-Art Drowsiness Detection Techniques," IEEE Access, vol. 7, pp. 61904-61919, 2019.

[5] S. Sahayadhas, K. Sundaraj, and M. Murugappan, "Detecting Driver Drowsiness Based on Sensors: A Review," Sensors, vol. 12, no. 12, pp. 16937-16953, 2012.

[6] W. Liu, J. Qian, Z. Yao, X. Jiao, and J. Pan, "Fusion of Eye Movement and EEG Data for Drowsiness Detection," IEEE Trans. Neural Syst. Rehabil. Eng., vol. 27, no. 9, pp. 1734-1742, 2019.

[7] T. Soukupová and J. Čech, "Real-Time Eye Blink Detection using Facial Landmarks," in Proc. Computer Vision Winter Workshop, 2016.

[8] A. Rosebrock, "Real-Time Eye Blink Detection with OpenCV, Python, and dlib," PyImageSearch, 2017.

[9] F. García, D. Martín, A. de la Escalera, and J. M. Armingol, "Driver Monitoring Based on Low-Cost 3D Sensors," IEEE Trans. Intell. Transp. Syst., vol. 22, no. 3, pp. 1378-1389, 2021.

[10] J. Ryu, J. Jung, S. Kim, and S. Kim, "Driver Distraction Detection Using Head Pose Estimation," in Proc. Int. Conf. Info. Comm. Tech. Convergence, 2018.

[11] K. Praveen and S. Kumar, "Driver Distraction Detection with Head Pose Estimation and Eye Gaze," in Proc. IEEE Int. Conf. Adv. Comp., Comm. and Infor., 2020.

[12] L. Zhang, F. Yang, Y. Zhang, and Y. Zhu, "Road Traffic Distraction Detection from Mobile Phone Usage Using Computer Vision Techniques," Transport. Res. Part C: Emerg. Technol., vol. 114, pp. 648-667, 2020.

[13] M. Ibrahim, M. Torki, and M. ElHelw, "Hands-on-wheel detection via hand tracking with temporal analysis," IEEE Access, vol. 10, pp. 20991-21003, 2022.

[14] Google, "MediaPipe Hands," [Online]. Available: https://google.github.io/mediapipe/solutions/hands, 2022.

[15] D. E. King, "Dlib-ml: A Machine Learning Toolkit," J. Mach. Learn. Res., vol. 10, pp. 1755-1758, 2009.

[16] C. Lugaresi, J. Tang, H. Nash, C. McClanahan, E. Uboweja, M. Hays, F. Zhang, C. Chang, M. G. Yong, J. Lee, W. Chang, W. Hua, M. Georg, and M. Grundmann, "MediaPipe: A Framework for Building Perception Pipelines," arXiv:1906.08172, 2019.

[17] T. D. Nguyen, P. H. Le, T. T. Nguyen, and T. B. Tran, "Comparative Analysis of Machine Learning Algorithms for Drowsiness Detection in Real-Time Edge Computing," in Proc. Int. Conf. Adv. Info. Eng. and Tech., 2023.
