# Hệ Thống Phát Hiện Buồn Ngủ: Hướng Dẫn Sử Dụng

Hướng dẫn này cung cấp thông tin về cách cài đặt, cấu hình và sử dụng Hệ Thống Phát Hiện Buồn Ngủ.

## Mục Lục
- [Cài Đặt](#cài-đặt)
- [Chạy Hệ Thống](#chạy-hệ-thống)
- [Giao Diện Người Dùng](#giao-diện-người-dùng)
- [Tùy Chọn Cấu Hình](#tùy-chọn-cấu-hình)
- [Cảnh Báo và Thông Báo](#cảnh-báo-và-thông-báo)
- [Xử Lý Sự Cố](#xử-lý-sự-cố)
- [Câu Hỏi Thường Gặp](#câu-hỏi-thường-gặp)

## Cài Đặt

### Yêu Cầu Hệ Thống
- Python 3.8 trở lên
- Webcam hoặc camera tương thích
- Hệ điều hành Windows, macOS, hoặc Linux

### Các Bước Thực Hiện

1. **Sao chép hoặc tải xuống kho lưu trữ**

2. **Cài đặt các gói phụ thuộc**
   ```bash
   pip install -r requirements.txt
   ```

3. **Xác minh cài đặt**
   ```bash
   python main.py --check
   ```

## Chạy Hệ Thống

### Khởi Động Ứng Dụng Giám Sát

Để bắt đầu ứng dụng giám sát người lái xe chính:

```bash
python main.py --mode ui
```

Thao tác này khởi chạy giao diện giám sát thời gian thực.

### Tùy Chọn Dòng Lệnh

Hệ thống hỗ trợ nhiều tùy chọn dòng lệnh:

```bash
python main.py --mode [ui|collect_data|train] [--options]
```

- `--mode ui`: Khởi động UI giám sát (mặc định)
- `--mode collect_data`: Khởi động công cụ thu thập dữ liệu
- `--mode train`: Huấn luyện mô hình với dữ liệu đã thu thập

Các tùy chọn bổ sung:
- `--camera_id [số]`: Chỉ định ID camera (mặc định: 0)
- `--ear_threshold [giá trị]`: Đặt ngưỡng Tỷ lệ Khía cạnh Mắt (mặc định: 0.2)
- `--confidence [giá trị]`: Đặt ngưỡng độ tin cậy (mặc định: 0.6)

Ví dụ:
```bash
# Khởi động UI với camera 1
python main.py --mode ui --camera_id 1

# Thu thập dữ liệu huấn luyện cho trạng thái 'focused'
python main.py --mode collect_data --data_class focused --samples 200

# Huấn luyện mô hình với các cài đặt tùy chỉnh
python main.py --mode train --test_size 0.3 --kernel rbf
```

## Giao Diện Người Dùng

Giao diện giám sát bao gồm một số thành phần chính:

![Tổng Quan UI](assets/images/ui_overview.png)

### Thành Phần Chính

1. **Hiển Thị Video**
   - Hiển thị nguồn cấp dữ liệu từ camera với các chú thích thời gian thực
   - Các điểm mốc khuôn mặt và kết quả phát hiện được hiển thị chồng lên

2. **Bảng Trạng Thái**
   - Trạng thái hiện tại của người lái xe: OK, BUỒN NGỦ, hoặc MẤT TẬP TRUNG
   - Giá trị EAR và ngưỡng
   - Chỉ báo vị trí đầu
   - Trạng thái vị trí tay

3. **Bảng Điều Khiển**
   - Danh sách thả xuống chọn camera
   - Thanh trượt điều chỉnh độ nhạy
   - Bật/tắt cảnh báo âm thanh
   - Nút lưu/tải cài đặt

4. **Bảng Số Liệu**
   - Hiển thị số liệu thời gian thực
   - Giá trị độ tin cậy phát hiện
   - Bộ đếm FPS (Khung hình mỗi giây)

### Các Điều Khiển Giao Diện

- **Nút Bắt Đầu/Dừng**: Điều khiển quá trình giám sát
- **Thanh Trượt Ngưỡng EAR**: Điều chỉnh độ nhạy phát hiện buồn ngủ
- **Thanh Trượt Độ Tin Cậy**: Điều chỉnh ngưỡng độ tin cậy phát hiện
- **Nút Bật/Tắt Âm Thanh**: Bật/tắt cảnh báo âm thanh
- **Nút Cài Đặt**: Mở hộp thoại cài đặt nâng cao
- **Nút Xuất**: Xuất nhật ký phát hiện và thống kê

## Tùy Chọn Cấu Hình

### Cấu Hình Cơ Bản

Cấu hình cơ bản có thể được điều chỉnh trực tiếp trong UI:

| Cài đặt | Mô tả | Mặc định | Phạm vi |
|---------|-------------|---------|-------|
| Ngưỡng EAR | Ngưỡng Tỷ lệ Khía cạnh Mắt để phát hiện buồn ngủ | 0.2 | 0.15-0.3 |
| Ngưỡng Độ Tin Cậy | Độ tin cậy tối thiểu cho phát hiện dương tính | 0.6 | 0.5-0.9 |
| Độ Trễ Cảnh Báo | Số giây trước khi kích hoạt cảnh báo | 2.0 | 0.5-5.0 |
| ID Camera | ID thiết bị camera sẽ sử dụng | 0 | Phụ thuộc hệ thống |

### Cấu Hình Nâng Cao

Các cài đặt nâng cao có thể được sửa đổi thông qua hộp thoại cài đặt hoặc tệp cấu hình:

- **Thông Số Phát Hiện**:
  - Độ tin cậy phát hiện khuôn mặt
  - Chất lượng phát hiện điểm mốc
  - Kích thước cửa sổ làm mịn thời gian

- **Cấu Hình Cảnh Báo**:
  - Lựa chọn tệp âm thanh
  - Tần suất cảnh báo
  - Thời lượng cảnh báo liên tục

- **Tùy Chọn UI**:
  - Hiển thị số liệu
  - Tùy chọn lớp phủ chú thích
  - Chọn giao diện

### Tệp Cấu Hình

Bạn có thể sửa đổi trực tiếp tệp `config/settings.json`:

```json
{
  "camera": {
    "device_id": 0,
    "width": 640,
    "height": 480,
    "fps": 30
  },
  "detection": {
    "ear_threshold": 0.2,
    "confidence_threshold": 0.6,
    "consecutive_frames": 3,
    "head_turned_threshold": 0.3,
    "head_tilted_threshold": 0.2
  },
  "alerts": {
    "sound_enabled": true,
    "drowsy_sound": "assets/sounds/drowsy_alert.wav",
    "distracted_sound": "assets/sounds/distracted_alert.wav",
    "continuous_alerts": true,
    "alert_interval": 3.0
  },
  "ui": {
    "show_landmarks": true,
    "show_fps": true,
    "show_metrics": true
  }
}
```

## Cảnh Báo và Thông Báo

Hệ thống cung cấp một số loại cảnh báo:

### Cảnh Báo Trực Quan

- **Chỉ Báo Trạng Thái**: Thay đổi màu sắc dựa trên trạng thái phát hiện
  - Xanh lá: Bình thường/OK
  - Vàng: Cảnh báo
  - Đỏ: Báo động (Buồn ngủ hoặc Mất tập trung)

- **Thông Báo Trên Màn Hình**: Cảnh báo văn bản mô tả vấn đề được phát hiện

### Cảnh Báo Âm Thanh

- **Cảnh Báo Buồn Ngủ**: Phát ra khi người lái xe có vẻ buồn ngủ
- **Cảnh Báo Mất Tập Trung**: Phát ra khi người lái xe có vẻ mất tập trung
- **Cảnh Báo Liên Tục**: Lặp lại cho đến khi người lái xe trở lại trạng thái an toàn

### Tùy Chỉnh Cảnh Báo

1. **Thay Đổi Âm Thanh Cảnh Báo**
   - Thay thế các tệp âm thanh trong thư mục `assets/sounds/`
   - Sử dụng hộp thoại cài đặt để chọn các tệp âm thanh khác nhau

2. **Độ Nhạy Cảnh Báo**
   - Điều chỉnh ngưỡng cho cảnh báo ít/nhiều
   - Sửa đổi cài đặt khung hình liên tiếp để phản ứng nhanh/chậm hơn

## Xử Lý Sự Cố

### Các Vấn Đề Phổ Biến và Giải Pháp

| Vấn đề | Nguyên Nhân Có Thể | Giải Pháp |
|-------|----------------|-----------|
| Không phát hiện camera | Vấn đề về trình điều khiển, sự cố phần cứng | Kiểm tra kết nối thiết bị, cài đặt lại trình điều khiển |
| FPS thấp | Độ phân giải cao, giới hạn CPU | Giảm độ phân giải trong cài đặt, đóng các ứng dụng khác |
| Cảnh báo buồn ngủ giả | Ánh sáng kém, ngưỡng EAR quá cao | Cải thiện ánh sáng, giảm ngưỡng EAR |
| Không phát hiện khuôn mặt | Ánh sáng kém, khuôn mặt ngoài khung hình | Điều chỉnh vị trí camera, cải thiện ánh sáng |
| Ứng dụng bị treo | Vấn đề bộ nhớ, thiếu gói phụ thuộc | Khởi động lại ứng dụng, cài đặt lại gói phụ thuộc |

### Tối Ưu Hóa Hiệu Suất

Nếu hệ thống chạy chậm:

1. **Giảm Độ Phân Giải**:
   ```json
   "camera": {
     "width": 320,
     "height": 240
   }
   ```

2. **Giảm Chất Lượng Xử Lý**:
   ```json
   "detection": {
     "landmark_quality": "fast"
   }
   ```

3. **Tắt Các Tính Năng**:
   ```json
   "ui": {
     "show_landmarks": false,
     "show_metrics": false
   }
   ```

### Nhật Ký Lỗi

Các nhật ký lỗi được lưu trữ trong thư mục `logs/`. Những thông tin này có thể hữu ích khi báo cáo sự cố.

## Câu Hỏi Thường Gặp

### Câu Hỏi Chung

**Hỏi: Phát hiện buồn ngủ chính xác đến mức nào?**  
Đáp: Hệ thống đạt độ chính xác khoảng 90% trong điều kiện thông thường. Độ chính xác phụ thuộc vào ánh sáng, chất lượng camera và hiệu chuẩn người dùng.

**Hỏi: Hệ thống có thể hoạt động vào ban đêm không?**  
Đáp: Có, nhưng cần đủ ánh sáng hồng ngoại hoặc ánh sáng cabin để camera có thể nhìn rõ khuôn mặt của người lái xe.

**Hỏi: Ứng dụng sử dụng bao nhiêu CPU?**  
Đáp: Mô hình dựa trên SVM thường sử dụng 20-30% CPU trên máy tính hiện đại. Mô hình CNN có thể yêu cầu nhiều tài nguyên hơn.

### Câu Hỏi Kỹ Thuật

**Hỏi: Tôi có thể sử dụng mô hình tùy chỉnh không?**  
Đáp: Có, bạn có thể huấn luyện các mô hình tùy chỉnh với `retrain_model.py` và tập dữ liệu của riêng bạn.

**Hỏi: Làm cách nào để thu thập dữ liệu huấn luyện riêng?**  
Đáp: Sử dụng chế độ thu thập dữ liệu:
```bash
python main.py --mode collect_data --data_class [trạng thái] --samples [số lượng]
```

**Hỏi: Hệ thống có thể tích hợp với các ứng dụng khác không?**  
Đáp: Có, bạn có thể sử dụng API được cung cấp trong `utils/helpers.py` để tích hợp với các hệ thống khác.

### Câu Hỏi Sử Dụng

**Hỏi: Tôi có nên đeo kính khi sử dụng hệ thống không?**  
Đáp: Hệ thống hoạt động với hầu hết các loại kính, nhưng kính phản quang cao hoặc kính màu có thể làm giảm độ chính xác.

**Hỏi: Làm cách nào để hiệu chuẩn hệ thống cho khuôn mặt của tôi?**  
Đáp: Hệ thống tự động thích ứng, nhưng để có kết quả tốt nhất, hãy thu thập một số dữ liệu huấn luyện ở vị trí lái xe thông thường của bạn.
